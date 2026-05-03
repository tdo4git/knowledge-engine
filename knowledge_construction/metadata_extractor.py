import hashlib
from pathlib import Path


class MetadataExtractor:

    def extract(self, file_path):

        path = Path(file_path)

        metadata = {}

        metadata["source_file"] = path.name
        metadata["doc_hash"] = self._compute_hash(path)

        metadata["title"] = self._infer_title(path)
        metadata["year"] = self._infer_year(path)

        return metadata


    def _compute_hash(self, path):

        sha256 = hashlib.sha256()

        with open(path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)

        return sha256.hexdigest()


    def _infer_title(self, path):

        name = path.stem
        title = name.replace("_", " ")
        return title


    def _infer_year(self, path):

        name = path.stem

        for token in name.split("_"):
            if token.isdigit() and len(token) == 4:
                return int(token)

        return None