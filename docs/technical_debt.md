# Technical Debt – Strategic Knowledge Engine
Zuletzt aktualisiert: 2026-05-07

---

## Format

Jeder Eintrag enthält:
- **ID** — eindeutige Referenz
- **Bereich** — Subsystem
- **Beschreibung** — was ist das Problem
- **Aufwand** — klein / mittel / groß
- **Priorität** — hoch / mittel / niedrig
- **Status** — offen / in Arbeit / erledigt

---

## Offene Punkte

### TD-004 — Regressionstest auf Referenzdokumente begrenzen
- **Bereich:** Tests / Onboarding Validation
- **Beschreibung:** Aktuell werden beim Regressionstest (`--regression`) alle Dokumente neu eingespielt. Besser: 3–5 kuratierte Referenzdokumente als festes Test-Set, unabhängig vom produktiven Onboarding.
- **Aufwand:** mittel
- **Priorität:** niedrig
- **Status:** offen

---

### TD-005 — Topic als Klassifikationsdimension einführen
- **Bereich:** Knowledge Construction / Klassifikation
- **Beschreibung:** `topic` ist in `config/taxonomy.py` definiert und im Prompt Builder integriert, wird aber nicht in der Registry gespeichert und nicht für Retrieval/Scoring genutzt. Claude klassifiziert bereits korrekt mit Topic-Werten — diese werden aktuell per `LLM_DOMAIN_NORMALIZATION` auf `knowledge_domain` gemappt (Workaround). Saubere Lösung: Topic als eigene Dimension in Registry + Scoring einführen. Konkret sichtbar: 4 SZ-KI-Artikel haben den generischen Doc-ID-Prefix `kunstliche`, weil "Künstliche Intelligenz" kein KEYWORD in `_extract_topic` ist — ein dedizierter Topic würde hier präzisere IDs und besseres Retrieval ermöglichen.
- **Aufwand:** mittel
- **Priorität:** mittel
- **Status:** offen

---

### TD-007 — Reklassifizierungs-Skript
- **Bereich:** Knowledge Construction / Operations
- **Beschreibung:** Bei Taxonomie-Änderungen müssen betroffene Dokumente reklassifiziert werden. Kein Skript vorhanden — aktuell manueller Reset + vollständiges Re-Onboarding notwendig. Konkret ausstehend: 7 Dokumente mit Fehlklassifikation (6× falscher Document Type, 1× falsche Origin), identifiziert via `generate_snapshot.py`:
  - `doc_supervisory_insurance_83c73b` → research_report statt supervisory_guidance
  - `doc_supervisory_20250903versicherungsmarktbericht2024_2025_10cbfd` → research_report statt supervisory_guidance
  - `doc_consulting_dora_2024_d54141` → blog_article statt consulting_framework
  - `doc_consulting_insurance_2024_19f71c` → research_report statt consulting_framework
  - `doc_consulting_insurance_2030_131197` → research_report statt consulting_framework
  - `doc_vendor_heiseacademymycompany_6d0ccf` → research_report statt vendor_marketing
  - `doc_research_digitalesouveraenitaetbeltiosgdvwhitepaperausgabe22025_2025_913b5f` → Origin research_institution statt industry_association
- **Aufwand:** mittel
- **Priorität:** mittel
- **Status:** offen

---

### TD-008 — Ingestion-Layer für Web-Quellen
- **Bereich:** Knowledge Sources
- **Beschreibung:** Aktuell nur PDF, DOCX, TXT unterstützt. LinkedIn-Posts, Blog-Posts, Web-Artikel, Podcast-Transkripte fehlen. Lösung: Web-Scraper / Transkriptions-Layer oder manuelle TXT-Konvertierung.
- **Aufwand:** groß
- **Priorität:** niedrig
- **Status:** offen

---

### TD-009 — AUTHOR_ORIGIN_MAP Keyword-Qualität
- **Bereich:** Knowledge Construction / Governance
- **Beschreibung:** Kurze Keywords in `AUTHOR_ORIGIN_MAP` erzeugen False Positives durch Substring-Matches (z.B. `"ey"` matcht `"they"`, `"money"` etc., `"msg"` matcht `"messaging"`). Gelöst für `ey` und `msg` — aber weitere kurze Keywords könnten dasselbe Problem haben. Mit Einführung von `media` (2026-05-06) hinzugekommen: `"spiegel"` könnte in anderen Kontexten matchen. Langfristig: Wort-Grenz-Matching statt einfachem Substring-Check.
- **Aufwand:** mittel
- **Priorität:** niedrig
- **Status:** offen

---

### TD-012 — Chunk-Strategie überprüfen
- **Bereich:** Knowledge Construction / Chunking
- **Beschreibung:** Token-basiertes Chunking (600 Token, 80 Overlap) erzeugt thematisch gemischte Chunks in breiten Dokumenten (Research-Studien, Marktberichte). Einzelne Chunks enthalten mehrere Themen — Keywords der Query werden getroffen ohne inhaltliche Relevanz. Evaluieren: (1) Chunk-Size reduzieren auf 400 Token für fokussiertere Chunks, (2) semantisches Chunking an Absatz-/Abschnittsgrenzen. Voraussetzung: ausreichende Knowledge-Base-Größe für systematische Retrieval-Evaluation. Jede Änderung erfordert vollständiges Re-Onboarding.
- **Aufwand:** mittel
- **Priorität:** niedrig
- **Status:** offen

---

## Erledigt

### TD-001 — Doc-Hash Duplicate Check ✔
- **Erledigt:** 2026-05-03
- **Lösung:** `doc_hash` wird in `MetadataExtractor` berechnet, in `metadata` übergeben und in `RegistryBuilder._check_duplicate()` geprüft. Erkennt umbenannte Dateien zuverlässig.

### TD-002 — Doc-ID Stabilität und Eindeutigkeit ✔
- **Erledigt:** 2026-05-03
- **Lösung:** Neues Schema `doc_{origin_short}_{topic}_{year?}_{hash6}`. Origin aus Governance, Hash-Suffix für Eindeutigkeit. Keyword-Liste erweitert.

### TD-003 — Manueller Review-Schritt formalisieren ✔
- **Erledigt:** 2026-05-03
- **Lösung:** Validation-Fehler blockieren Registry-Eintrag und Archivierung. `review_required` ist Audit-Signal ohne harten Stop. Review-Report wird nach jedem Onboarding-Lauf geschrieben (`knowledge_base/audit/review_report.txt`) und in der Konsole angezeigt. Erfolgreich verarbeitete Dokumente werden automatisch von `intake/` nach `archive/` verschoben.

### TD-006 — Bias-Logik korrigieren ✔
- **Erledigt:** 2026-05-03
- **Lösung:** `bias.py` korrigiert: `"legislator"` statt `"regulator"` als Key. `"corporate"` als neue Origin-Kategorie mit Bias `"medium"` ergänzt.

### TD-010 — Doc-ID enthält Origin aus LLM, nicht aus Governance ✔
- **Erledigt:** 2026-05-03
- **Lösung:** `generate_doc_id()` wird nach `apply_governance_pipeline()` aufgerufen und verwendet `classification.get("origin")` — also die finale, governance-korrigierte Origin. Zusätzlich: `"corporate"` in `_normalize_origin()` ergänzt (fehlender Eintrag war der eigentliche Bug). `doc_unknown_allianz_*` → `doc_corporate_allianz_*`.

### TD-011 — Mindest-Score-Threshold im ContextBuilder ✔
- **Erledigt:** 2026-05-07
- **Lösung:** `min_document_score: 0.30` in `CONTEXT_CONFIG` (engine_config.py) eingeführt. `ContextBuilder` filtert Chunks via `_get_chunk_score()` vor Limitierung — Chunks von Dokumenten unterhalb des Schwellwerts werden ausgeschlossen. Score wird aus `chunk.document_metadata['score']` gelesen (setzt Score-Propagation aus QueryPipeline Schritt 5 voraus). Threshold ist config-driven und ohne Code-Change anpassbar.
