from collections import defaultdict
from pathlib import Path
from typing import Optional
import yaml

from .perspective_mapping import PERSPECTIVE_MAP


class PerspectiveOrchestrator:

    def __init__(self, config_path: Optional[str] = None):

        if config_path is None:
            config_path = Path(__file__).parent / "perspective_config.yaml"

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def orchestrate(self, scored_chunks: list, content_intent: str, k: int = 6) -> list:

        scored_chunks = sorted(
            scored_chunks,
            key=lambda x: getattr(x, "score", getattr(x, "similarity_score", 0)),
            reverse=True
        )
        
        perspective_groups = self._group_by_perspective(scored_chunks)

        self._sort_groups_by_score(perspective_groups)

        result = self._apply_quotas(
            perspective_groups,
            content_intent,
            k
        )

        result = self._apply_fallback(
            result,
            perspective_groups,
            k
        )

        result = self._apply_normative_guard(
            result,
            perspective_groups,
            content_intent
        )

        return result[:k]

    # ---------------------------------------------------------
    # Helper
    # ---------------------------------------------------------

    def _get_origin(self, chunk):
        return chunk.document_metadata.get("origin", "unknown")

    def _get_score(self, chunk):
        return getattr(chunk, "score", getattr(chunk, "similarity_score", 0))

    # ---------------------------------------------------------
    # Step 1: Gruppierung
    # ---------------------------------------------------------

    def _group_by_perspective(self, chunks):

        groups = defaultdict(list)

        for chunk in chunks:

            origin = self._get_origin(chunk)
            perspective = PERSPECTIVE_MAP.get(origin, "other")

            groups[perspective].append(chunk)

        return groups

    # ---------------------------------------------------------
    # Step 2: Sortierung
    # ---------------------------------------------------------

    def _sort_groups_by_score(self, groups):

        for perspective in groups:

            groups[perspective].sort(
                key=lambda x: self._get_score(x),
                reverse=True
            )

    # ---------------------------------------------------------
    # Step 3: Quoten
    # ---------------------------------------------------------

    def _apply_quotas(self, groups, content_intent, k):

        quotas = self.config.get(content_intent, {})

        result = []

        for perspective, ratio in quotas.items():

            target_n = int(k * ratio)
            candidates = groups.get(perspective, [])

            result.extend(candidates[:target_n])

        return result

    # ---------------------------------------------------------
    # Step 4: Fallback
    # ---------------------------------------------------------

    def _apply_fallback(self, result, groups, k):

        if len(result) >= k:
            return result

        remaining = []

        for group in groups.values():
            remaining.extend(group)

        remaining.sort(
            key=lambda x: self._get_score(x),
            reverse=True
        )

        for chunk in remaining:

            if chunk not in result:
                result.append(chunk)

            if len(result) >= k:
                break

        return result

    # ---------------------------------------------------------
    # Step 5: Normative Guard
    # ---------------------------------------------------------

    def _apply_normative_guard(self, result, groups, content_intent):

        if content_intent != "normative":
            return result

        has_regulatory = any(
            PERSPECTIVE_MAP.get(self._get_origin(chunk)) == "regulatory"
            for chunk in result
        )

        if has_regulatory:
            return result

        regulatory_chunks = groups.get("regulatory", [])

        if not regulatory_chunks:
            return result

        result[-1] = regulatory_chunks[0]

        return result