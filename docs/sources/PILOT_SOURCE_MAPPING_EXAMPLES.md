# Pilot Source Mapping Examples — synthetisch

| Feld | Wert |
| --- | --- |
| **Klassifikation** | **synthetic · non-operational · test-only** |
| Grundlage | **ADR-0008** (A1), [Schema](PILOT_SOURCE_MAPPING_SCHEMA.md), [Validation](PILOT_SOURCE_MAPPING_VALIDATION.md) |
| Erfasst in | CBP-WP-010 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

> **Sämtliche Beispiele sind erfunden.** Sie enthalten **keine realen Pfade,
> keine realen Repository-Namen, keine realen Benutzer- oder
> Organisationsnamen, keine realen Credential References und keine
> realistischen Secrets.**
>
> **Kein Beispiel darf kopiert und aktiviert werden.** Alle Platzhalter sind
> als solche erkennbar; reservierte Beispieldomains nach RFC 2606
> (`example.invalid`) und Pfadplatzhalter der Form
> `synthetic-placeholder-*`.
>
> Diese Datei ist **kein Mappingbestand**. Sie liegt bewusst im
> Core-Repository, weil sie nichts Privates enthält.

---

## 1 — Gültiges PS-02-Mapping

**synthetic · non-operational · test-only**

```yaml
schema_version: "1.0"
mapping_id: "MAP-EXAMPLE-0001"
slot_id: "PS-02"
mapping_name: "Beispiel Markdown Root"
source_boundary_type: "markdown-root"
deployment_profile: "B"
operator_reference: "role-operator-placeholder"
location_reference: "synthetic-placeholder-markdown-root"
location_reference_type: "local-directory"
collection: "example-domain-alpha"
project: "example-project-alpha"
enabled: false
read_only: true
allowed_subpaths:
  - "notes"
  - "decisions"
excluded_subpaths:
  - "notes/private"
follow_symlinks: false
data_class: "internal"
ai_transfer_policy: "restricted"
local_search_policy: "allowed"
indexing_policy: "none"
mobile_visibility: "authorized-only"
revision_strategy: "content-hash"
deletion_behavior: "tombstone-and-cleanup"
verification_status: "unverified"
approval_status: "not-approved"
approved_by: null
approved_at: null
mapping_revision: 1
previous_revision: null
credential_reference: null
notes: "Synthetisches Beispiel. Nicht aktivieren."
```

**Gültig, aber wirkungslos.** `enabled: false`, `indexing_policy: none`,
`approval_status: not-approved` — genau so beginnt jedes Mapping. Die Allowlist
ist gesetzt, `notes/private` gewinnt gegen `notes` (V13).

## 2 — Gültiges PS-03-Mapping

**synthetic · non-operational · test-only**

```yaml
schema_version: "1.0"
mapping_id: "MAP-EXAMPLE-0002"
slot_id: "PS-03"
mapping_name: "Beispiel Git Repository"
source_boundary_type: "git-repository"
deployment_profile: "B"
operator_reference: "role-operator-placeholder"
location_reference: "https://git.example.invalid/synthetic-placeholder-repo.git"
location_reference_type: "git-remote"
collection: "example-domain-beta"
project: "example-project-beta"
enabled: false
read_only: true
allowed_subpaths:
  - "docs"
excluded_subpaths:
  - "docs/internal-drafts"
follow_symlinks: false
data_class: "public"
ai_transfer_policy: "allowed"
local_search_policy: "allowed"
indexing_policy: "none"
mobile_visibility: "allowed"
revision_strategy: "git-commit"
deletion_behavior: "tombstone-and-cleanup"
verification_status: "unverified"
approval_status: "not-approved"
approved_by: null
approved_at: null
mapping_revision: 1
previous_revision: null
credential_reference: null
notes: "Synthetisches Beispiel. Reservierte Domain example.invalid."
```

`revision_strategy: git-commit` ist für PS-03 verpflichtend (V16). Die Domain
ist nach RFC 2606 reserviert und **nicht auflösbar**.

## 3 — Gültiges PS-04-Mapping

**synthetic · non-operational · test-only**

```yaml
schema_version: "1.0"
mapping_id: "MAP-EXAMPLE-0003"
slot_id: "PS-04"
mapping_name: "Beispiel Handoff Root"
source_boundary_type: "handoff-root"
deployment_profile: "B"
operator_reference: "role-operator-placeholder"
location_reference: "synthetic-placeholder-handoff-root"
location_reference_type: "local-directory"
collection: "example-domain-alpha"
project: "example-project-alpha"
enabled: false
read_only: true
allowed_subpaths:
  - "approved"
excluded_subpaths:
  - "approved/raw-transcripts"
follow_symlinks: false
data_class: "internal"
ai_transfer_policy: "restricted"
local_search_policy: "allowed"
indexing_policy: "none"
mobile_visibility: "forbidden"
revision_strategy: "handoff-revision"
deletion_behavior: "tombstone-and-cleanup"
verification_status: "unverified"
approval_status: "not-approved"
approved_by: null
approved_at: null
mapping_revision: 1
previous_revision: null
credential_reference: null
notes: "Synthetisches Beispiel. Nur freigegebene Handoffs, keine Rohmitschriften."
```

`approved/raw-transcripts` ist ausgeschlossen — PS-04-Regel 2 untersagt
vollständige unkontrollierte Chatarchive.

---

## 4 — Ungültig: `enabled: true` ohne Approval

**synthetic · non-operational · test-only**

```yaml
# UNGÜLTIG — verletzt V17 und V24
schema_version: "1.0"
mapping_id: "MAP-EXAMPLE-0004"
slot_id: "PS-02"
enabled: true                     # <-- Verstoß
verification_status: "unverified" # <-- nicht verifiziert
approval_status: "not-approved"   # <-- nicht freigegeben
approved_by: null
approved_at: null
```

| Verletzt | Wirkung |
| --- | --- |
| **V17** | Kein Human Approval | `human-review-required` |
| **V18** | Nicht verifiziert | `fail` |
| **V24** | Aktivierungsgate unvollständig | `fail` |

`enabled` wird auf `false` **zurückgesetzt**, nicht toleriert. Zustandsregel
**Z11** verbietet den Weg von `draft` nach `enabled` ohnehin.

## 5 — Ungültig: `unknown` data_class

**synthetic · non-operational · test-only**

```yaml
# UNGÜLTIG bei Aktivierung — verletzt V9
schema_version: "1.0"
mapping_id: "MAP-EXAMPLE-0005"
slot_id: "PS-02"
data_class: "unknown"             # <-- Ausgangszustand, kein Betriebszustand
ai_transfer_policy: "forbidden"
enabled: true                     # <-- Verstoß
```

**`unknown` wird fail-closed behandelt** — wie `excluded-from-ai`, **nicht** wie
`internal`. Ergebnis: **`blocked`**, Stop-Bedingung **SB-07**.

Als `draft` wäre dieses Mapping gültig. Unzulässig ist die **Aktivierung**.

## 6 — Ungültig: leere Allowlist bei Aktivierung

**synthetic · non-operational · test-only**

```yaml
# UNGÜLTIG — verletzt V12
schema_version: "1.0"
mapping_id: "MAP-EXAMPLE-0006"
slot_id: "PS-02"
allowed_subpaths: []              # <-- nimmt NICHTS auf
excluded_subpaths: []
data_class: "internal"
enabled: true                     # <-- Verstoß
```

**Eine leere Allowlist bedeutet „nichts", nicht „alles".** Sie ist der
Ausgangszustand und blockiert die Aktivierung. Die naheliegende Fehlannahme —
leerer Filter gleich kein Filter — ist genau der Grund für diese Regel.

## 7 — Ungültig: Secret im `notes`-Feld

**synthetic · non-operational · test-only**

```yaml
# UNGÜLTIG — verletzt V8
schema_version: "1.0"
mapping_id: "MAP-EXAMPLE-0007"
slot_id: "PS-03"
credential_reference: null
notes: "TODO: <SYNTHETIC-SECRET-PLACEHOLDER-DO-NOT-USE>"   # <-- Verstoß
```

> **Der Platzhalter ist kein Secret und ähnelt keinem.** Er steht für ein
> erkennbares Muster ohne Geheimwert. Es wird **kein Secret erzeugt**, um eine
> Secret-Erkennung zu demonstrieren — das wäre genau der Vorgang, den die
> Kontrolle verhindern soll.

| Wirkung | |
| --- | --- |
| Ergebnis | **`blocked`** |
| Schweregrad | **`blocker`** |
| Stop-Bedingung | **SB-02** |
| Verfahren | [SECRET_INCIDENT_RESPONSE.md](../security/SECRET_INCIDENT_RESPONSE.md) — **Rotation vor History Cleanup** |

**`notes` ist der häufigste Leckagepfad.** Freitextfelder sind der Ort, an dem
Regeln umgangen werden — deshalb unterliegen sie derselben Prüfung wie jedes
andere Feld.

## 8 — Ungültig: externe Übertragung bei `excluded-from-ai`

**synthetic · non-operational · test-only**

```yaml
# UNGÜLTIG — verletzt V10
schema_version: "1.0"
mapping_id: "MAP-EXAMPLE-0008"
slot_id: "PS-02"
data_class: "excluded-from-ai"
ai_transfer_policy: "allowed"     # <-- Verstoß
mobile_visibility: "allowed"      # <-- zusätzlich unzulässig
```

**`excluded-from-ai` erzwingt `forbidden`.** Diese Kombination wird
**abgelehnt, nicht stillschweigend korrigiert** — eine automatische Korrektur
würde verbergen, dass jemand die Regel nicht verstanden hat.

Ergebnis: **`blocked`**. Erreicht der Inhalt tatsächlich einen Modellkontext,
greift Stop-Bedingung **SB-03**.

## 9 — Ungültig: mehrere Source Boundaries

**synthetic · non-operational · test-only**

```yaml
# UNGÜLTIG bei C1 — verletzt Granularitätsentscheidung D-033
schema_version: "1.0"
mapping_id: "MAP-EXAMPLE-0009"
slot_id: "PS-03"
source_boundary_type: "git-repository"
location_reference:                        # <-- Verstoß: Sequenz statt einzelner Wert
  - "https://git.example.invalid/synthetic-placeholder-repo-a.git"
  - "https://git.example.invalid/synthetic-placeholder-repo-b.git"
```

**`location_reference` ist ein String, keine Sequenz.** Zwei Repositories
brauchen **zwei Mappings** mit eigenen IDs, Revisionen, Datenklassen und
Freigaben.

> **Grundsatz M-C:** Was gemeinsam gemappt ist, wird gemeinsam widerrufen.
> Ein Widerruf für Repository A würde hier B mit deaktivieren — oder, schlimmer,
> A weiterlaufen lassen, weil B noch gebraucht wird.

Ergebnis: `fail` gegen V6 und das Schema (Typverstoß).

## 10 — Tombstone

**synthetic · non-operational · test-only**

```yaml
schema_version: "1.0"
mapping_id: "MAP-EXAMPLE-0010"
slot_id: "PS-02"
mapping_name: "Beispiel entfernter Markdown Root"
source_boundary_type: "markdown-root"
deployment_profile: "B"
operator_reference: "role-operator-placeholder"
location_reference: null
location_reference_type: "local-directory"
collection: "example-domain-alpha"
project: "example-project-alpha"
enabled: false
read_only: true
allowed_subpaths: []
excluded_subpaths: []
follow_symlinks: false
data_class: "internal"
ai_transfer_policy: "forbidden"
local_search_policy: "forbidden"
indexing_policy: "none"
mobile_visibility: "forbidden"
revision_strategy: "content-hash"
deletion_behavior: "tombstone-and-cleanup"
verification_status: "unverified"
approval_status: "revoked"
approved_by: null
approved_at: null
mapping_revision: 3
previous_revision: 2
credential_reference: null
notes: "Tombstone. Quelle entfernt, Derived Cleanup ausgefuehrt. Begruendung: synthetisches Beispiel."
```

| Eigenschaft | Wirkung |
| --- | --- |
| `approval_status: revoked` | Deaktivierung erzwungen (Z8) |
| `location_reference: null` | Ort entfernt, Eintrag bleibt |
| `deletion_behavior` | **Derived Cleanup** ausgeführt (D3) |
| Revisionskette | 2 → 3 lückenlos erhalten (V16) |
| `mapping_id` | **wird nie wiederverwendet** (D5, V21) |

**Der Tombstone ist kanonisch und wird gesichert** (D6). Ein Rebuild darf ihn
**nie** überschreiben (D4) — sonst kehrt die gelöschte Quelle zurück, was
Stop-Bedingung **SB-08** auslöst.

---

## Verwendungshinweis

| # | Regel |
| --- | --- |
| 1 | Diese Beispiele sind **Dokumentation**, kein Konfigurationsvorrat |
| 2 | **Kein Beispiel kopieren und mit realen Werten füllen** — reale Mappings entstehen ausschließlich im privaten Operator-Workspace |
| 3 | Die Platzhalter sind bewusst **nicht** auflösbar |
| 4 | Die gültigen Beispiele 1 bis 3 sind **wirkungslos**: nicht aktiviert, nicht freigegeben, nicht indexiert |
| 5 | Die ungültigen Beispiele 4 bis 9 dienen als Vorlage für die **Negativtests NT-01 bis NT-18** |

## Status

**synthetic · non-operational · test-only.** Es existiert kein reales Mapping,
keine angebundene Quelle, kein Index. **Kein Beispiel ist aktiviert oder
aktivierbar.**

**Implementierung erlaubt: nein.**
