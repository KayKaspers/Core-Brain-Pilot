# ADR-0012 — Deterministic Source Mapping Draft Validator

| Feld | Wert |
| --- | --- |
| **Status** | **accepted** |
| Autorität nach Annahme | **A1** |
| Grundlage der Entscheidungen | **A0** — Human Maintainer (CBP-WP-015) |
| Erfasst in | CBP-WP-015 |
| Datum | 2026-07-27 |
| Verhältnis | präzisiert **ADR-0008** (D-031, D-032, D-033); baut auf **ADR-0007**, **ADR-0009**, **ADR-0011** auf |
| Entscheidungen | **D-046, D-047, D-048, D-049** (A0) |

Dieses ADR dokumentiert einen **lokalen, synthetisch testbaren, read-only und
fail-closed** Validator für **Mapping-Entwürfe** nach dem **angenommenen
31-Feld-Vertrag**. Es ändert den Vertrag **nicht**, aktiviert **nichts** und
speichert **nichts**.

---

## Human Authorization

**Decision:** APPROVE WP-015 IMPLEMENTATION WITH NOTES · **Authority:** A0 —
Human Maintainer.

Autorisiert ist ausschließlich ein lokaler, synthetisch testbarer, read-only und
fail-closed Validator für Mapping-Entwürfe nach dem angenommenen
31-Feld-Vertrag. **31** bezeichnet die Anzahl der kanonischen Felddefinitionen:
**29 Pflichtfelder** und **zwei optionale Felder**. Die optionalen Felder dürfen
**nicht** zu Pflichtfeldern gemacht werden.

**Nicht autorisiert:** Änderung/Reduzierung des Vertrags, zusätzliche
Mapping-Felder, reale Mapping-Dateien, reale Quellen, reale Pfade/URLs,
Source-Inhaltszugriff, Mapping-Speicherung, Report-Speicherung,
Registry-Veränderung, Mapping-/Source-Aktivierung, Ingest, Indexierung,
Retrieval, Netzwerkzugriff, Secret-Auflösung, RT-2-Speicherung, Deployment,
Gate-Ausführung.

Teilentscheidungen: **A1** (Dokumentprofil), **B1** (Registry-Bindung),
**C1** (Boundary-/Draft-Modell), **D1** (Ergebnis/Aktivierung).

---

## Verhältnis zu D-031, D-032, D-033 (ADR-0008)

| Bestehende Entscheidung | Bleibt unverändert | Präzisierung durch ADR-0012 |
| --- | --- | --- |
| **D-031** — YAML-1.2-strikter-Teilumfang mit JSON Schema als Vertragsgrenze | **ja** | **D-046** wählt **kanonisches JSON** als JSON-kompatibles MVP-Profil **innerhalb** dieses Teilumfangs. „JSON Schema bleibt tragend"; die Eingabeform ist eine Serialisierungswahl, **keine** Vertragsänderung |
| **D-032** — hybride Projekt-/Domänen-Collection plus Slot-Marker | **ja** | keine Änderung; `collection` wird **exakt** gegen Registry `collection_key` geprüft, **ohne** Normalisierung und **ohne** `project`/`domain`-Crosswalk |
| **D-033** — genau **eine** Source Boundary je Mapping | **ja** | **D-048** prüft genau **eine** deaktivierte synthetische Boundary mit bereits erlaubten Vertragswerten |

Die **31 Feldnamen**, ihre Pflicht-/Optionalität und alle bestehenden
Enum-Werte bleiben **unverändert**.

---

## Der vollständige 31-Feld-Vertrag

**29 Pflichtfelder (1–29):** `schema_version`, `mapping_id`, `slot_id`,
`mapping_name`, `source_boundary_type`, `deployment_profile`,
`operator_reference`, `location_reference`, `location_reference_type`,
`collection`, `project`, `enabled`, `read_only`, `allowed_subpaths`,
`excluded_subpaths`, `follow_symlinks`, `data_class`, `ai_transfer_policy`,
`local_search_policy`, `indexing_policy`, `mobile_visibility`,
`revision_strategy`, `deletion_behavior`, `verification_status`,
`approval_status`, `approved_by`, `approved_at`, `mapping_revision`,
`previous_revision`.

**Zwei optionale Felder (30–31):** `credential_reference`, `notes`.

Quelle: [PILOT_SOURCE_MAPPING_SCHEMA.md](../sources/PILOT_SOURCE_MAPPING_SCHEMA.md)
(„31 Felder"), [PILOT_SOURCE_MAPPING_SPECIFICATION.md](../sources/PILOT_SOURCE_MAPPING_SPECIFICATION.md)
und [PILOT_SOURCE_MAPPING_VALIDATION.md](../sources/PILOT_SOURCE_MAPPING_VALIDATION.md)
(V2 = „29 Pflichtfelder"; 24 Regeln, acht Blocker).

---

## Entscheidungen

### D-046 — Dokumentprofil (Teil A1)

Kanonisches JSON als JSON-kompatibles **MVP-Profil** des beschlossenen strikten
YAML-Teilumfangs; alle **31** Felddefinitionen bleiben unverändert. **Keine**
allgemeine YAML-Unterstützung, **kein** eigener allgemeiner YAML-Parser,
**keine** externe Abhängigkeit. **Fail-closed:** doppelte Schlüssel, `NaN`,
`Infinity`, BOM, ungültiges UTF-8, unbekannte Felder und ein fehlendes
Pflichtfeld blockieren; `credential_reference` und `notes` bleiben optional.

### D-047 — Externe read-only Registry-Bindung (Teil B1)

Bindung über `--source-id` und `--registry`. **`source_id` ist kein
Mapping-Feld**; das Mapping bleibt beim 31-Feld-Vertrag. Die Registry bleibt
**bytegenau unverändert**. Geprüft werden: Source existiert, Record strukturell
gültig, effektiver Zustand `REGISTERED_DISABLED` (RETIRED/unbekannt/beschädigt
blockieren), Registry `source_reference` beginnt mit `synthetic:`, `collection`
**exakt** gleich `collection_key`, `data_class` **exakt** gleich `data_class`.
**Verbotene Crosswalks:** `project`↔`domain_key`, `project`↔`namespace`,
`ai_transfer_policy`↔`ai_eligibility`, `location_reference`↔`source_id`,
`operator_reference`↔`source_id`.

### D-048 — Boundary- und Draft-Modell (Teil C1)

Genau **eine** deaktivierte synthetische Boundary mit bestehenden kanonischen
Feldern und ausschließlich bereits erlaubten Vertragswerten. **Kein** neues
`slot:synthetic:`-Präfix, **keine** neuen Enum-Werte. `slot_id` ∈
{`PS-02`, `PS-03`, `PS-04`}; `source_boundary_type` slotkonform (V6);
`location_reference_type` boundarykonform; `location_reference` = das im
kanonischen Vertrag belegte synthetische V7-Platzhalterformat
`synthetic-placeholder-*`; `allowed_subpaths`/`excluded_subpaths` leer;
`follow_symlinks=false`; `enabled=false`; `read_only=true`.

### D-049 — Ergebnis und Aktivierung (Teil D1)

Ausschließlich **deterministischer, nicht persistierter** Validierungsreport.
`mapping_id` wird nach dem bestehenden Vertrag **validiert** (V4/V21), **nicht
neu berechnet** und **nicht** normalisiert; es wird **keine** `map-`-plus-
SHA-256-Bildungsvorschrift eingeführt. `draft_sha256` und `policy_sha256` dürfen
deterministisch berechnet werden. Der Report wird **nicht gespeichert**, die
Registry **nicht verändert**. **`VALID_DRAFT` bedeutet keine Freigabe und keine
Aktivierung.** `activation-check` verweigert **unabhängig** vom
Validierungsergebnis (Exitcode 13).

---

## Dokumentprofil, Policy, Registry-Bindung — Zusammenfassung

- **Dokumentprofil:** kanonisches JSON (MVP), UTF-8 ohne BOM, Objekt oben, keine
  Duplikate, kein `NaN`/`Infinity`, keine unbekannten Felder, 29 Pflichtfelder.
- **Policy:** 18 Felder, exakte Feldzahlen (31/29/2), Profil
  `canonical-json-yaml-subset`, `required_mapping_schema_version = "1.0"`.
  Jede gelockerte `require_*`- oder `allow_*`-Grenze blockiert; Environment und
  CLI überschreiben **keine** Sicherheitswerte.
- **Zulässige Abgleiche:** nur `collection`↔`collection_key` und
  `data_class`↔`data_class`, exakt.

## mapping_id-Aussagegrenze

Der Validator prüft `mapping_id` (V4/V21: vorhanden, stabil, ortsunabhängig,
ohne Pfad-/Host-/Personenbestandteil), berechnet oder ersetzt sie aber **nie**.
**Die Bildungsvorschrift von `mapping_id` bleibt offen.**

## Reportmodell

Enthält `report_schema_version`, `mapping_id`, `source_id`, `draft_sha256`,
`policy_sha256`, `mapping_schema_version`, `validation_status` ∈
{`VALID_DRAFT`, `BLOCKED`}, sortierte/deduplizierte `reason_codes`,
`reason_count`, `canonical_contract_field_count` (31), `required_field_count`
(29), `present_field_count` (29/30/31), `boundary_count`,
`implementation_version`. **Keine** Uhr, Pfade, URLs, Source-Inhalte,
`source_reference`, kein Registry-Root, keine Snippets.

## Wirkungen

- **Datenschutz:** kein realer Pfad, keine URL, kein Source-Inhalt, keine
  `location_reference` mit realem Wert; V7-Grenze (ADR-0007) bleibt gewahrt.
- **Secret:** keine Secret-Auflösung; `credential_reference`/`notes`/alle Felder
  werden auf Secret-Muster geprüft (V8/V23), ein Fund blockiert.
- **Portabilität:** reine Standardbibliothek (Python 3.13+), keine externe
  Abhängigkeit, deterministische Serialisierung.
- **Integrität:** fail-closed; Registry read-only und bytegenau unverändert;
  keine Persistenz, keine Aktivierung.

## Verworfene Alternativen

1. **Allgemeiner YAML-Parser** — verworfen (parserabhängige Semantik, externe
   Abhängigkeit); stattdessen enges JSON-MVP-Profil (D-046).
2. **`source_id` als zusätzliches Mapping-Feld** — verworfen (verletzt den
   31-Feld-Vertrag); stattdessen externe CLI-Bindung (D-047).
3. **Neues `slot:synthetic:`-Präfix / neue Enum-Werte** — verworfen (Vertrags-
   und Enum-Erweiterung); stattdessen bestehende Werte (D-048).
4. **`mapping_id` per `map-`+SHA-256 berechnen** — verworfen (führt eine
   unbeschlossene Bildungsvorschrift ein); stattdessen nur Validierung (D-049).
5. **Persistierter Report / Mapping-Store** — verworfen (Persistenz nicht
   autorisiert); nicht persistierter Report (D-049).

## Offene Folgefragen

**OD-05, OD-06, OD-37 und OD-38 bleiben offen.** Die **Bildungsvorschrift von
`mapping_id` bleibt offen**. Das **Mapping Activation Gate** bleibt `NOT
EVALUATED`; seine deterministische Auswertung ist Gegenstand des
**vorgeschlagenen, nicht autorisierten** CBP-WP-016.

## Status

**accepted.** Es ist **kein** Mapping gespeichert, **keine** Source aktiviert,
**keine** Boundary aktiv, **keine** Collection und **kein** Index erzeugt.
`VALID_DRAFT` bedeutet ausschließlich Vertragskonformität eines synthetischen
Entwurfs — **keine** Freigabe.
