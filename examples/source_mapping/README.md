# Source Mapping Draft — synthetische Beispiele (CBP-WP-015)

| Feld | Wert |
| --- | --- |
| **Klassifikation** | **synthetic · non-operational · test-only** |
| Grundlage | **ADR-0008** (A1), **ADR-0012** (A1), D-031 bis D-033, D-046 bis D-049 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-27 |

> **Sämtliche Beispiele sind erfunden.** Sie enthalten **keine realen Pfade,
> keine realen Repository-Namen, keine realen Benutzer- oder
> Organisationsnamen, keine realen Credential References und keine
> realistischen Secrets.**
>
> **Kein Beispiel darf kopiert und aktiviert werden.** `VALID_DRAFT` bedeutet
> **keine** Freigabe, **kein** gespeichertes Mapping, **keine** Aktivierung,
> **keinen** Ingest, **keine** Indexierung und **kein** Retrieval.

---

## Dokumentprofil

Der Validator akzeptiert **kanonisches JSON** als JSON-kompatibles MVP-Profil
des beschlossenen strikten YAML-Teilumfangs (D-046). Es wird **keine**
allgemeine YAML-Unterstützung behauptet. Verlangt sind: UTF-8 **ohne BOM**, ein
JSON-Objekt auf oberster Ebene, **keine** doppelten Schlüssel, **kein** `NaN`,
**kein** `Infinity`, **keine** unbekannten Felder und alle **29 Pflichtfelder**.
Die zwei optionalen Felder `credential_reference` und `notes` dürfen fehlen
oder `null` sein — sie werden **nicht** zu Pflichtfeldern gemacht.

Der Vertrag umfasst **31 Felddefinitionen**: **29 Pflichtfelder** und **zwei
optionale Felder**. Der Validator ändert den Vertrag **nicht** und berechnet
`mapping_id` **nicht** (Bildungsvorschrift offen).

## Registry-Bindung (extern, read-only)

Jeder Aufruf verlangt `--registry` und `--source-id`. `source_id` ist **kein**
Mapping-Feld. Die Registry wird **ausschließlich read-only** gelesen und bleibt
bytegenau unverändert. Der referenzierte Record muss existieren, strukturell
gültig und im Zustand `REGISTERED_DISABLED` sein; seine `source_reference` muss
mit `synthetic:` beginnen. Geprüft werden **ausschließlich**:

- `collection` **exakt** gleich Registry `collection_key`,
- `data_class` **exakt** gleich Registry `data_class`.

**Nicht** verglichen werden `project`↔`domain_key`/`namespace`,
`ai_transfer_policy`↔`ai_eligibility`, `location_reference`↔`source_id` und
`operator_reference`↔`source_id`.

## Synthetischer, deaktivierter 31-Feld-Entwurf (PS-02)

Dieser Entwurf ist gültig **und wirkungslos**. `location_reference` verwendet
das im kanonischen Vertrag belegte synthetische V7-Platzhalterformat
`synthetic-placeholder-*` (siehe
[PILOT_SOURCE_MAPPING_EXAMPLES.md](../../docs/sources/PILOT_SOURCE_MAPPING_EXAMPLES.md)).
`data_class` und `collection` müssen zum gebundenen Registry-Record passen.

```json
{
  "schema_version": "1.0",
  "mapping_id": "MAP-EXAMPLE-0001",
  "slot_id": "PS-02",
  "mapping_name": "Beispiel Markdown Root",
  "source_boundary_type": "markdown-root",
  "deployment_profile": "B",
  "operator_reference": "role-operator-placeholder",
  "location_reference": "synthetic-placeholder-markdown-root",
  "location_reference_type": "local-directory",
  "collection": "example-domain-alpha",
  "project": "example-project-alpha",
  "enabled": false,
  "read_only": true,
  "allowed_subpaths": [],
  "excluded_subpaths": [],
  "follow_symlinks": false,
  "data_class": "internal",
  "ai_transfer_policy": "forbidden",
  "local_search_policy": "forbidden",
  "indexing_policy": "none",
  "mobile_visibility": "forbidden",
  "revision_strategy": "content-hash",
  "deletion_behavior": "tombstone-and-cleanup",
  "verification_status": "unverified",
  "approval_status": "not-approved",
  "approved_by": null,
  "approved_at": null,
  "mapping_revision": 1,
  "previous_revision": null,
  "credential_reference": null,
  "notes": "Synthetisches Beispiel. Nicht aktivieren."
}
```

Die deaktivierte synthetische Boundary hält ausschließlich bereits erlaubte
Vertragswerte: `enabled=false`, `read_only=true`, `follow_symlinks=false`,
leere `allowed_subpaths`/`excluded_subpaths`, `approval_status=not-approved`,
`verification_status=unverified`, `ai_transfer_policy=forbidden`,
`indexing_policy=none`, `local_search_policy=forbidden`,
`mobile_visibility=forbidden`, `approved_by=null`, `approved_at=null` sowie
`credential_reference` fehlend oder `null`.

## Report

Der Report wird **nicht gespeichert**. Er enthält **keine** Uhr, **keine**
Pfade, **keine** URLs, **keinen** Source-Inhalt, **keine** `source_reference`,
**keinen** Registry-Root und **keine** Snippets. Zulässige
`validation_status`-Werte sind ausschließlich `VALID_DRAFT` und `BLOCKED`.

## Ausführung

Der lauffähige, PowerShell-basierte Ablauf steht in
[docs/runtime/SOURCE_MAPPING_DRAFT_RUNBOOK.md](../../docs/runtime/SOURCE_MAPPING_DRAFT_RUNBOOK.md).
