# Technical Debt – Strategic Knowledge Engine
Zuletzt aktualisiert: 2026-05-03

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
- **Beschreibung:** `topic` ist in `config/taxonomy.py` definiert und im Prompt Builder integriert, wird aber nicht in der Registry gespeichert und nicht für Retrieval/Scoring genutzt. Claude klassifiziert bereits korrekt mit Topic-Werten — diese werden aktuell per `LLM_DOMAIN_NORMALIZATION` auf `knowledge_domain` gemappt (Workaround). Saubere Lösung: Topic als eigene Dimension in Registry + Scoring einführen.
- **Aufwand:** mittel
- **Priorität:** mittel
- **Status:** offen

---

### TD-007 — Reklassifizierungs-Skript
- **Bereich:** Knowledge Construction / Operations
- **Beschreibung:** Bei Taxonomie-Änderungen müssen alle Dokumente reklassifiziert werden. Kein Skript vorhanden. Aktuell manueller Reset + vollständiges Re-Onboarding notwendig.
- **Aufwand:** mittel
- **Priorität:** niedrig
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
- **Beschreibung:** Kurze Keywords in `AUTHOR_ORIGIN_MAP` erzeugen False Positives durch Substring-Matches (z.B. `"ey"` matcht `"they"`, `"money"` etc., `"msg"` matcht `"messaging"`). Gelöst für `ey` und `msg` — aber weitere kurze Keywords könnten dasselbe Problem haben. Langfristig: Wort-Grenz-Matching statt einfachem Substring-Check.
- **Aufwand:** mittel
- **Priorität:** niedrig
- **Status:** offen

---

### TD-010 — Doc-ID enthält Origin aus LLM, nicht aus Governance
- **Bereich:** Knowledge Construction / Metadata
- **Beschreibung:** `generate_doc_id()` wird mit `origin` aus der LLM-Klassifikation aufgerufen, bevor Governance läuft. Wenn Governance die Origin korrigiert (z.B. `unknown` → `corporate`), spiegelt die Doc-ID nicht die finale Origin wider (z.B. `doc_unknown_allianz_6ae771` statt `doc_corporate_allianz_6ae771`). Funktional kein Problem — nur kosmetisch.
- **Aufwand:** klein
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
