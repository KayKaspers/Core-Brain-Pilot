# Source Mapping Draft Validator — Trust Boundary und Vertrag (CBP-WP-015)

| Feld | Wert |
| --- | --- |
| **Status** | **lokaler Prototyp** — read-only, fail-closed, **nicht produktionsbereit** |
| Grundlage | **ADR-0012** (A1), ADR-0008 (D-031…D-033), ADR-0007, ADR-0011 |
| Erfasst in | CBP-WP-015 |
| Autoritätsklasse | A2 |
| Python | 3.13+ (nur Standardbibliothek) |
| Stand | 2026-07-27 |

Dieser Validator prüft **synthetische Mapping-Entwürfe** gegen den angenommenen
**31-Feld-Vertrag** und eine **extern, read-only** gebundene Source-Registry. Er
**speichert nichts**, **aktiviert nichts**, öffnet **keine** Verbindung und liest
**keinen** Source-Inhalt.

---

## Trust Boundary

| Innerhalb | Außerhalb (nicht Bestandteil) |
| --- | --- |
| Lesen eines synthetischen Entwurfs (kanonisches JSON, ≤ `max_draft_bytes`) | reale Mapping-Dateien, reale Quellen, Source-Inhalt |
| Read-only-Lesen genau eines Registry-Records und seiner Retirement-Events | jede Registry-Schreiboperation (Lock, Record, Event, Katalog) |
| Deterministischer, nicht persistierter Report auf stdout | Report-Datei, Mapping-Store, Mapping-Record, Mapping-Event |
| Fail-closed-Verweigerung mit stabilem Reason Code | Aktivierung, Ingest, Indexierung, Retrieval, Netzwerk, Secret-Auflösung |

Die Grenze ist eine **lokale Testgrenze**, **keine** produktive Sicherheits-,
Isolations- oder Deployment-Grenze und **kein** Gate.

## Verhältnis zu D-031 bis D-033

- **D-031** (YAML-Teilumfang, JSON Schema als Vertragsgrenze) — präzisiert durch
  **D-046**: kanonisches JSON als JSON-kompatibles MVP-Profil **innerhalb** des
  Teilumfangs. Keine allgemeine YAML-Unterstützung.
- **D-032** (hybride Collection) — unverändert; `collection` wird exakt gegen
  `collection_key` geprüft, ohne Normalisierung, ohne `project`/`domain`-Crosswalk.
- **D-033** (genau eine Boundary) — präzisiert durch **D-048**: genau eine
  deaktivierte synthetische Boundary.

## Der 31-Feld-Vertrag

**31 Felddefinitionen** = **29 Pflichtfelder** (Felder 1–29) + **zwei optionale
Felder** (`credential_reference`, `notes`). Datentypen, Enums und Cross-Field-
Regeln stammen aus SCHEMA/VALIDATION; der Validator **fügt kein Feld hinzu,
entfernt keines, benennt keines um** und **berechnet `mapping_id` nicht**.

## Dokumentprofil und Parser

Akzeptiert ausschließlich: UTF-8 **ohne BOM**, kanonisch verarbeitbares JSON,
JSON-Objekt oben, **keine** doppelten Schlüssel, kein `NaN`, kein `Infinity`,
keine Kommentare, keine unbekannten Felder, alle 29 Pflichtfelder. Verstöße
liefern stabile `MAP-PARSE-*`-Gründe.

## Policy

18 Felder; exakte Feldzahlen (31/29/2); Profil `canonical-json-yaml-subset`;
`required_mapping_schema_version = "1.0"`. Jede gelockerte `require_*`-Grenze
und jede gesetzte `allow_*`-Grenze **blockiert**. **Environment und CLI
überschreiben keine Sicherheitswerte.**

## Registry-Bindung (read-only)

`--source-id` + `--registry`; `source_id` ist **kein** Mapping-Feld. Geprüft:
Source-ID-Format, Record vorhanden und strukturell gültig, effektiver Lifecycle
`REGISTERED_DISABLED` (RETIRED/unbekannt/beschädigt blockieren),
`source_reference` beginnt mit `synthetic:`.

### Zulässige Abgleiche

| Mapping-Feld | Registry-Feld | Regel |
| --- | --- | --- |
| `collection` | `collection_key` | **exakt**, ohne Normalisierung |
| `data_class` | `data_class` | **exakt**, keine Rangordnung |

### Verbotene Crosswalks

`project`↔`domain_key`, `project`↔`namespace`,
`ai_transfer_policy`↔`ai_eligibility`, `location_reference`↔`source_id`,
`operator_reference`↔`source_id`. **Keiner** ist implementiert.

## Boundary-Prüfung

Nur kanonische Felder: `slot_id` ∈ {PS-02, PS-03, PS-04}, `source_boundary_type`
slotkonform (V6), `location_reference_type` boundarykonform, `location_reference`
= belegter synthetischer V7-Platzhalter `synthetic-placeholder-*`,
`allowed_subpaths`/`excluded_subpaths` leer, `follow_symlinks=false`. Kein neues
Präfix, keine neuen Enum-Werte.

## mapping_id-Aussagegrenze

`mapping_id` wird nach **V4/V21** validiert (vorhanden, stabil, ortsunabhängig,
ohne Pfad-/Host-/Personenbestandteil), **nicht berechnet**, **nicht ersetzt**,
**nicht** stillschweigend normalisiert. **Die Bildungsvorschrift bleibt offen.**

## draft_sha256 und Report

`draft_sha256` = SHA-256 der Roh-Entwurfsbytes; `policy_sha256` = SHA-256 der
Policy-Datei. Der **nicht persistierte** Report enthält
`report_schema_version`, `mapping_id`, `source_id`, `draft_sha256`,
`policy_sha256`, `mapping_schema_version`, `validation_status` ∈
{`VALID_DRAFT`, `BLOCKED`}, sortierte/deduplizierte `reason_codes`,
`reason_count`, `canonical_contract_field_count` (**31**),
`required_field_count` (**29**), `present_field_count` (**29/30/31**),
`boundary_count`, `implementation_version`. **Keine** Uhr, Pfade, URLs,
Source-Inhalte, `source_reference`, kein Registry-Root, keine Snippets.

## Exitcodes

| Code | Name | Bedeutung |
| --- | --- | --- |
| 0 | OK | **nur** `VALID_DRAFT` — Vertragskonformität eines synthetischen Entwurfs |
| 2 | CONFIG_INVALID | Policy strukturell ungültig |
| 4 | RUNTIME_START_BLOCKED | `run` verweigert (unverändert) |
| 12 | SOURCE_MAPPING_DRAFT_BLOCKED | Entwurf blockiert |
| 13 | SOURCE_MAPPING_ACTIVATION_BLOCKED | `activation-check` verweigert immer |
| 64 / 70 | USAGE_ERROR / INTERNAL_ERROR | unverändert |

**Exitcode 0 bedeutet nicht** approved, mapped, activated, ingestible, indexed
oder retrievable. Kollisionsfrei mit 0–11, 64, 70.

## Keine Persistenz, keine Aktivierung

Kein Mapping-Store, -Record, -Event, keine Reportdatei, keine Mapping-Registry,
keine Mapping- oder Source-Aktivierung, keine Boundary, kein Collection- oder
Index-Eintrag, kein Context Pack, kein externer Transfer. `activation-check`
verweigert **unabhängig** vom Validierungsergebnis (Exitcode 13).

## Aussagegrenzen

Dieser Prototyp ist **nicht produktionsbereit**. **Mapping Activation Gate**,
**Security Foundation Readiness Gate** und **DRC** bleiben `NOT EVALUATED`. Es
ist **keine** Capability vollständig `implemented` (0 von 29).
