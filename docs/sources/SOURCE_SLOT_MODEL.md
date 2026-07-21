# Source Slot Model — logisches Schema

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-006 |
| Autoritätsklasse | A2 |
| Status | **Logisches Schema, keine ausführbare Konfiguration** |
| Ergänzt durch | **ADR-0008** (A1) — Mappingebene, [Schema](PILOT_SOURCE_MAPPING_SCHEMA.md) mit 31 Feldern |
| Stand | 2026-07-21 |

> **Zwei Ebenen, zwei Dokumente.** Dieses Modell beschreibt den **logischen
> Slot** (24 Felder): *Was für eine Quelle ist das, und was darf mit ihr
> geschehen?* Die **Mappingebene** — *Wo liegt sie in dieser Installation?* —
> steht seit CBP-WP-010 in
> [PILOT_SOURCE_MAPPING_SCHEMA.md](PILOT_SOURCE_MAPPING_SCHEMA.md).
> **Regel 8 gilt auf beiden Ebenen:** weder Slot noch Mapping noch Collection
> verleihen Autorität.

Dieses Dokument definiert das **Schema** eines Source Slots. Es ist keine
Konfigurationsdatei, kein Code und nicht ausführbar.

---

## Feldschema

| Feld | Typ | Bedeutung |
| --- | --- | --- |
| `slot_id` | Kennung | Stabile ID, z. B. `PS-02` |
| `name` | Text | Sprechender Name |
| `source_kind` | Aufzählung | `project-control`, `markdown-root`, `git-repository`, `chat-handoff`, `benchmark-fixture`, `document-archive`, `external-connector` |
| `owner` | Rolle | **Pflicht.** Wer verantwortet Inhalt und Freigabe |
| `canonical_location_type` | Aufzählung | `in-core-repository`, `operator-managed`, `external-system` — **Typ, nicht Pfad** |
| `deployment_mapping_required` | bool | Ob eine Installation eine konkrete Zuordnung braucht |
| `allowed_formats` | Liste | Im Pilot ausschließlich `markdown` |
| `collection` | Kennung | Logische Sammlung für Berechtigungen und Suche |
| `default_authority` | `A0`–`A6` | Voreinstellung ohne abweichende Angabe |
| `allowed_authority_classes` | Liste | Zulässiger Bereich |
| `default_data_class` | Aufzählung | `public`, `internal`, `confidential`, `excluded-from-ai` |
| `allowed_data_classes` | Liste | Zulässiger Bereich; **`secret` nie enthalten** |
| `ai_transfer_policy` | Aufzählung | `allowed`, `restricted`, `forbidden` |
| `local_search_policy` | Aufzählung | `allowed`, `metadata-only`, `forbidden` |
| `mobile_visibility` | Aufzählung | `allowed`, `authorized-only`, `forbidden` |
| `read_policy` | Aktionsklasse | `read` oder `forbidden` |
| `draft_policy` | Aktionsklasse | `draft` oder `forbidden` |
| `write_policy` | Aktionsklasse | `write with approval` oder `forbidden` |
| `publish_policy` | Aktionsklasse | `publish with approval` oder `forbidden` |
| `ingest_mode` | Aufzählung | `direct-canonical`, `via-quarantine`, `test-fixture` |
| `verification_required` | bool | Ob eine menschliche Verifikation nötig ist |
| `revision_strategy` | Aufzählung | `git-commit`, `content-hash`, `dataset-version` |
| `deletion_strategy` | Aufzählung | `tombstone`, `allowlist-removal`, `dataset-major` |
| `enabled` | bool | Ob der Slot aktiv ist |
| `status` | Aufzählung | `active`, `test-only`, `deferred` |

**`canonical_location_type` benennt eine Art, keinen Ort.** Der Ort entsteht
erst im Deployment Mapping.

---

## Validierungsregeln

| # | Regel | Verhalten bei Verletzung |
| --- | --- | --- |
| **1** | **Kein Slot ohne Owner** | Slot ungültig, keine Aktivierung |
| **2** | **Kein Slot ohne Datenklasse** | Slot ungültig |
| **3** | **Kein Slot ohne AI-Transfer-Regel** | Slot ungültig |
| **4** | **Kein Slot mit Secrets** | `secret` ist in `allowed_data_classes` unzulässig; Fund ist ein Blocker |
| **5** | **`excluded-from-ai` erzwingt `ai_transfer_policy: forbidden`** | Jede andere Kombination ist ungültig — die Klasse setzt die Regel, nicht umgekehrt |
| **6** | **Fail-closed bei Unbekanntem** | Ein unbekanntes Feld oder eine unbekannte Berechtigung führt zu **Verweigerung**, nicht zu einer Vorgabe |
| **7** | **Aktivierung benötigt ein Deployment Mapping** | Bei `deployment_mapping_required: true` und fehlendem Mapping bleibt `enabled: false` |
| **8** | **Ein Source Slot verleiht keine höhere Autorität** | Die Autorität stammt aus dem Dokument, nicht aus seiner Ablage. `default_authority` ist eine Voreinstellung, keine Beförderung |
| **9** | **A0 muss auf eine konkrete menschliche Entscheidung zurückführbar sein** | Ein A0-Dokument ohne benennbaren Beschluss ist ungültig |
| **10** | **Der Benchmark-Slot erzeugt keine reale Projektentscheidung** | PS-05 ist `test-only`; seine Fixtures dürfen nie in `DECISION_REGISTER.md`, einem ADR oder einem Statusdokument zitiert werden |

### Zu Regel 6 — fail-closed im Detail

| Situation | Verhalten |
| --- | --- |
| Unbekanntes Feld im Slot | Slot wird nicht aktiviert |
| Unbekannte Datenklasse | Behandlung wie `excluded-from-ai` — nicht wie `internal` |
| Unbekannte Berechtigung | `forbidden` |
| Fehlendes Mapping | `enabled: false` |
| Widersprüchliche Angaben | die **restriktivere** gewinnt |

Der Normalzustand ist Verweigerung. Eine Lücke wird nie zugunsten der
Verfügbarkeit ausgelegt.

### Zu Regel 8 — warum das wichtig ist

Ein Dokument im Projektrepository ist nicht deshalb A1, weil es dort liegt. Ein
README bleibt A4, auch neben ADRs. Andernfalls würde die Ablage zur
Autoritätsquelle — und ein Verschieben zur Beförderung.

---

## Schema-Beispiel

**Nicht ausführbar. Fiktiver Slot, keine realen Pfade.**

```yaml
# BEISPIEL — nicht ausführbar, rein illustrativ
slot_id: PS-XX-EXAMPLE
name: Beispiel Markdown Slot
source_kind: markdown-root
owner: human-maintainer
canonical_location_type: operator-managed
deployment_mapping_required: true      # Ort erst im Deployment Mapping
allowed_formats:
  - markdown
collection: example-collection
default_authority: A4
allowed_authority_classes: [A2, A3, A4, A5, A6]
default_data_class: internal
allowed_data_classes: [public, internal]   # secret niemals
ai_transfer_policy: allowed
local_search_policy: allowed
mobile_visibility: allowed
read_policy: read
draft_policy: draft
write_policy: write-with-approval
publish_policy: forbidden
ingest_mode: via-quarantine
verification_required: true
revision_strategy: content-hash
deletion_strategy: tombstone
enabled: false                         # kein Mapping, also nicht aktiv
status: deferred
```

**Der Slot steht auf `enabled: false`**, weil `deployment_mapping_required`
gesetzt und kein Mapping vorhanden ist — Regel 7 in Aktion.

### Gegenbeispiel: ungültiger Slot

```yaml
# UNGÜLTIG — verletzt Regel 5
slot_id: PS-XX-INVALID
default_data_class: excluded-from-ai
ai_transfer_policy: allowed            # Regel 5 verletzt
```

`excluded-from-ai` erzwingt `forbidden`. Diese Kombination wird nicht
korrigiert, sondern **abgelehnt** — eine stille Korrektur würde verbergen, dass
jemand die Regel nicht verstanden hat.

---

## Abbildung der Pilot-Slots

| Slot | `source_kind` | `location_type` | `mapping_required` | `ingest_mode` | `status` |
| --- | --- | --- | --- | --- | --- |
| PS-01 | `project-control` | `in-core-repository` | **nein** | `direct-canonical` | `active` |
| PS-02 | `markdown-root` | `operator-managed` | **ja** | `direct-canonical` | `active` |
| PS-03 | `git-repository` | `operator-managed` | **ja** | `direct-canonical` | `active` |
| PS-04 | `chat-handoff` | `operator-managed` | ja | `direct-canonical` | `active` |
| PS-05 | `benchmark-fixture` | `in-core-repository` | nein | `test-fixture` | `test-only` |
| PS-06 | `document-archive` | `operator-managed` | ja | **`via-quarantine`** | `deferred` |
| PS-07 | `external-connector` | `external-system` | ja | **`via-quarantine`** | `deferred` |

Beide zurückgestellten Slots tragen `via-quarantine` — sie sind genau deshalb
zurückgestellt, weil die Quarantäne noch nicht existiert (R-32).

## Abgrenzung

| Dieses Dokument | Nicht dieses Dokument |
| --- | --- |
| Logisches Schema | Ausführbare Konfiguration |
| Feldnamen und Wertebereiche | Konkrete Werte einer Installation |
| Validierungsregeln | Validierungscode |
| Slot-Definitionen | Deployment Mappings |

## Status

**Kein Slot ist aktiviert.** Es existiert keine Konfiguration, kein Mapping,
kein Index und keine angebundene Quelle. Dieses Schema beschreibt, wie ein
Source Slot aussehen muss — nicht, welche existieren.
