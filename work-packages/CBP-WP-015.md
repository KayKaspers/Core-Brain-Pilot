# CBP-WP-015 — Deterministic Source Mapping Draft Validator

| Feld | Wert |
| --- | --- |
| **ID** | CBP-WP-015 |
| **Titel** | Deterministic Source Mapping Draft Validator |
| **Typ** | implementation |
| **NDF Prompt Mode** | Full |
| **Context Budget** | B2 – Standard |
| **Modell / Effort** | Claude Opus 4.8 (`claude-opus-4-8`) / ultracode |
| **Status** | **in-review** |
| **Grundlage** | ADR-0012 (A1), D-046 bis D-049 (A0); präzisiert ADR-0008 (D-031…D-033) |
| **Stand** | 2026-07-27 |

---

## Ausgangslage — 19/31-Blocker und Reconciliation

Der erste WP-015-Prompt ging von **19** kanonischen Mapping-Feldern aus. Die
**Vorprüfung** ergab jedoch, dass der angenommene A1/A2-Vertrag
(PILOT_SOURCE_MAPPING_SCHEMA/SPECIFICATION/VALIDATION, ADR-0008) **31
Felddefinitionen** definiert. Der Implementation Agent hat **nicht** geraten,
sondern **BLOCKED** gemeldet (Stop-Bedingung „nicht genau 19 kanonische
Felder").

Ein anschließender **read-only Reconciliation-Lauf** bestätigte konsistent über
die drei kanonischen Dokumente: **31 Felddefinitionen**, **29 Pflichtfelder**,
**zwei optionale Felder** (`credential_reference`, `notes`), **24
Validierungsregeln** (V1–V24, davon acht Blocker). Der Feasibility Gate ergab
**PASS**. Auf dieser Basis wurde die Implementierung mit dem korrigierten
31-Feld-Premiss autorisiert.

## Human Authorization

**APPROVE WP-015 IMPLEMENTATION WITH NOTES** (A0). Teilentscheidungen **A1**
(Dokumentprofil), **B1** (Registry-Bindung), **C1** (Boundary/Draft), **D1**
(Report/Aktivierung). Nicht autorisiert: Vertragsänderung, zusätzliche Felder,
reale Quellen/Pfade/URLs, Source-Inhalt, Mapping-/Report-Speicherung,
Registry-Veränderung, Aktivierung, Ingest, Indexierung, Retrieval, Netzwerk,
Secret-Auflösung, RT-2-Speicherung, Deployment, Gate-Ausführung.

## Entscheidungen und ADR

- **D-046** — kanonisches JSON als JSON-MVP-Profil; 31 Felddefinitionen
  unverändert. **D-047** — externe read-only Registry-Bindung über `--source-id`
  / `--registry`; `source_id` kein Mapping-Feld. **D-048** — genau eine
  deaktivierte synthetische Boundary; kein neues Slot-Präfix, keine neuen Enums.
  **D-049** — nicht persistierter Report; `mapping_id` validiert, nicht berechnet;
  Aktivierung immer verweigert.
- **ADR-0012** — `accepted` (A1). Verhältnis zu D-031/D-032/D-033: präzisierend,
  nicht ändernd.

## Der 31-Feld-Vertrag

**29 Pflichtfelder:** `schema_version`, `mapping_id`, `slot_id`, `mapping_name`,
`source_boundary_type`, `deployment_profile`, `operator_reference`,
`location_reference`, `location_reference_type`, `collection`, `project`,
`enabled`, `read_only`, `allowed_subpaths`, `excluded_subpaths`,
`follow_symlinks`, `data_class`, `ai_transfer_policy`, `local_search_policy`,
`indexing_policy`, `mobile_visibility`, `revision_strategy`, `deletion_behavior`,
`verification_status`, `approval_status`, `approved_by`, `approved_at`,
`mapping_revision`, `previous_revision`. **Zwei optionale Felder:**
`credential_reference`, `notes`.

## Ziel · Scope · Out of Scope

**Ziel:** lokaler, synthetisch testbarer, read-only, fail-closed Validator für
Mapping-Entwürfe nach dem 31-Feld-Vertrag mit externer read-only
Registry-Bindung und nicht persistiertem, deterministischem Report.

**Scope:** Parser (JSON-MVP-Profil), Policy (18 Felder, fail-closed),
Vertrags-/Zustandsvalidierung, Registry-Bindung (exakt `collection`/`data_class`),
CLI `validate-draft` und `activation-check`, Tests, Evidenz, Doku, 19/31-Korrektur.

**Out of Scope:** Mapping-Store/-Record/-Event, Reportdatei, Mapping-Registry,
Aktivierung, Boundary-Anlage, Collection/Index/Context Pack, externer Transfer,
Netzwerk, Secret-Auflösung, Gate-Ausführung, CBP-WP-016.

## Trust Boundary · Dokumentprofil · Policy

Siehe [SOURCE_MAPPING_DRAFT_VALIDATOR.md](../docs/runtime/SOURCE_MAPPING_DRAFT_VALIDATOR.md).
JSON-MVP ohne BOM, ohne Duplikate, ohne `NaN`/`Infinity`, ohne unbekannte Felder,
29 Pflichtfelder. Policy erzwingt exakte Feldzahlen (31/29/2) und alle
Sicherheitsgrenzen fail-closed; Environment/CLI überschreiben nichts.

## Registry-Bindung · zulässige Abgleiche · verbotene Crosswalks

Read-only; Source vorhanden, gültig, `REGISTERED_DISABLED`, `source_reference`
synthetisch. **Nur** `collection`↔`collection_key` und `data_class`↔`data_class`,
exakt. **Kein** `project`↔`domain_key`/`namespace`, `ai_transfer_policy`↔
`ai_eligibility`, `location_reference`/`operator_reference`↔`source_id`.

## Boundary-Modell · mapping_id · Report · CLI · Exitcodes

Genau eine deaktivierte synthetische Boundary; `location_reference` =
`synthetic-placeholder-*`. `mapping_id` nur validiert (V4/V21), nie berechnet;
Bildungsvorschrift bleibt offen. Nicht persistierter, minimierter Report
(`VALID_DRAFT`/`BLOCKED`). CLI: `validate-draft` (Exit 0 nur bei `VALID_DRAFT`,
sonst 12; Policyfehler 2) und `activation-check` (immer 13). Exitcodes **12** und
**13** kollisionsfrei mit 0–11, 64, 70.

## Tests · Technische Evidenz

Sechs neue Testmodule (`test_mapping_policy/parser/validator/boundary/
registry_binding/cli`) plus Erweiterung von `test_cli.py` (Netzwerk-Guard über
beide Mapping-Kommandos, Import-Probe). **Ran 315 tests … OK** (Basislinie 212
bleibt grün). Vollständige Evidenz in
[SOURCE_MAPPING_DRAFT_EVIDENCE.md](../docs/runtime/SOURCE_MAPPING_DRAFT_EVIDENCE.md);
PowerShell-Ablauf in
[SOURCE_MAPPING_DRAFT_RUNBOOK.md](../docs/runtime/SOURCE_MAPPING_DRAFT_RUNBOOK.md).
Registry vor/nach bytegenau identisch; keine Mapping-/Reportdatei; Cleanup
bestätigt.

## 19/31-Korrektur · R-33

Transparente Korrekturhinweise in `docs/roadmap/PILOT_SOURCE_MAPPING_PLAN.md` und
`docs/roadmap/PHASE_1_EVIDENCE_PLAN.md` (19 → 31 Felddefinitionen, M1–M14 → 24
Regeln, wo erforderlich); historische Angaben und die Queue-Aussage zu
CBP-WP-008 bleiben als **abgelöste Planungsannahme** erhalten. **Genau ein** neuer
R-33-Konsistenzvorgang (der neunte), gespiegelt in RISK_REGISTER und
COMPLIANCE_CHECK, zählt **nur einmal**. Neue Basislinie: **neun
Konsistenzvorgänge in fünfzehn Work Packages**. **R-33 bleibt gemindert, nicht
geschlossen.**

## Stop-Bedingungen (eingehalten)

Keine der Stop-Bedingungen ausgelöst: HEAD `d0c0531`, sauberer Arbeitsbaum vor
Beginn, exakt 31 Felddefinitionen (29+2), kein zusätzliches Feld, kein
Pflichtmachen optionaler Felder, keine `mapping_id`-Berechnung, keine
Data-Class-Rangordnung, kein verbotener Crosswalk, kein neues Slot-Präfix, kein
neuer Enum-Wert, Python 3.13, keine externe Abhängigkeit, keine reale
Quelle/Pfad/URL, kein Source-Inhalt, keine Persistenz, kein Registry-Schreiben,
keine Aktivierung, kein Netzwerkversuch, kein Secret, kein Testfehler, keine
unerwartete Datei, keine Gate-Ausführung, kein CBP-WP-016.

## Akzeptanzkriterien

A1/B1/C1/D1 umgesetzt; ADR-0012 `accepted`; Vertrag bei 31 (29+2); JSON-MVP eng
validiert; Registry extern read-only, `collection`/`data_class` exakt; keine
verbotenen Crosswalks; genau eine synthetische deaktivierte Boundary; `mapping_id`
nur validiert; Report deterministisch, nicht persistent; Aktivierung immer
verweigert; Registry bytegenau unverändert; 19/31-Korrektur erledigt; genau ein
neuer R-33-Vorgang, R-33 offen; Testsuite grün; keine Gate-/Produktionsreife
vorgetäuscht. **Alle erfüllt.**

## Rückmeldung an Nova

Implementierung abgeschlossen und **in-review**. Kein Commit, kein Push
(Commit-Autorität liegt beim Human Maintainer). Nächstes vorgeschlagenes,
**nicht autorisiertes** Work Package: **CBP-WP-016 — Deterministic Mapping
Activation Gate Evaluator** (proposed).
