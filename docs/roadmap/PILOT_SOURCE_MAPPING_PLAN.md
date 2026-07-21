# Pilot Source Mapping Plan — Schema der Deployment Mappings

| Feld | Wert |
| --- | --- |
| **Status** | **ABGELÖST** — die verbindliche Fassung ist [PILOT_SOURCE_MAPPING_SPECIFICATION.md](../sources/PILOT_SOURCE_MAPPING_SPECIFICATION.md) (CBP-WP-010, ADR-0008) |
| Stream | F2 · Backlogpunkt P2 |
| Erfasst in | CBP-WP-008 |
| Autoritätsklasse | A3 |
| Betrifft | **OD-05**, **OD-06** (beide bleiben offen) |
| Stand | 2026-07-21 |

> **Planungsdokument aus CBP-WP-008, inhaltlich abgelöst.** Die verbindliche
> Mappingdefinition steht seit CBP-WP-010 in
> [PILOT_SOURCE_MAPPING_SPECIFICATION.md](../sources/PILOT_SOURCE_MAPPING_SPECIFICATION.md),
> [PILOT_SOURCE_MAPPING_SCHEMA.md](../sources/PILOT_SOURCE_MAPPING_SCHEMA.md)
> und [ADR-0008](../decisions/ADR-0008-pilot-source-mapping-konvention.md).
> Dieses Dokument bleibt als Planungsstand erhalten und wird **nicht**
> rückwirkend umgeschrieben; bei Abweichungen gilt die Spezifikation.
>
> **Klarstellung zum Veröffentlichungsbegriff (CBP-WP-010):** Wo dieses
> Dokument das Core-Repository als „veröffentlichbar" bezeichnet, ist
> **`publication-capable by design`** gemeint — eine Bauweise, **keine
> öffentliche Freigabe**. Das Repository bleibt privat; Veröffentlichung,
> Lizenz, Branding und Release benötigen je eine separate **A0-Entscheidung**
> (OD-11, OD-23, OD-28). Es besteht keine pauschale Zusicherung, dass der
> aktuelle Gesamtinhalt ohne erneute Prüfung veröffentlicht werden darf.

Dieses Dokument definiert das **Schema** eines Deployment Mappings. Es enthält
**keinen realen Pfad, keine private Repository-URL, keine Hostangabe und kein
Secret**. Es ist keine Konfigurationsdatei und nicht ausführbar.

---

## Geltungsbereich

Geplant wird die spätere Erstellung konkreter Mappings für drei Slots aus dem
[Pilot Source Contract](../sources/PILOT_SOURCE_CONTRACT.md):

| Slot | Name | `source_kind` | Mapping erforderlich |
| --- | --- | --- | --- |
| **PS-02** | Operator Markdown Knowledge Root | `markdown-root` | **ja** |
| **PS-03** | Selected Git Repositories | `git-repository` | **ja** |
| **PS-04** | Approved Chat Handoffs | `chat-handoff` | **ja** |

**Nicht** geplant werden PS-01 und PS-05 (kein Mapping erforderlich) sowie
PS-06 und PS-07 (`deferred`, bis die Quarantäne existiert).

## Abgrenzung zum Source Slot Model

**ADR-0006** trennt zwei Ebenen. Diese Trennung ist der Zweck des Dokuments:

| Ebene | Dokument | Beantwortet | Ablage |
| --- | --- | --- | --- |
| **Logischer Slot** | [SOURCE_SLOT_MODEL.md](../sources/SOURCE_SLOT_MODEL.md) — 24 Felder | *Was für eine Quelle ist das, und was darf mit ihr geschehen?* | Core Repository (`publication-capable by design`, **nicht freigegeben**) |
| **Deployment Mapping** | dieses Schema — 19 Felder | *Wo liegt sie in genau dieser Installation?* | **Private Operator Workspace** |

Ein Slot ohne Mapping ist gültig, aber inaktiv (Slot-Regel 7). Ein Mapping ohne
Slot ist **ungültig** — es gibt nichts, dessen Regeln es erben könnte.

**Das Mapping erweitert niemals die Rechte des Slots.** Es kann nur einschränken.

---

## Feldschema — 19 Felder

| # | Feld | Typ | Vorgabe | Bedeutung |
| --- | --- | --- | --- | --- |
| 1 | `mapping_id` | Kennung | — | Stabile ID des Mappings |
| 2 | `slot_id` | Kennung | — | **Pflicht.** Verweis auf einen existierenden Slot |
| 3 | `deployment_profile` | Aufzählung | — | `A`–`E` gemäß [DEPLOYMENT_PROFILES.md](../architecture/DEPLOYMENT_PROFILES.md) |
| 4 | `operator` | Rolle | — | **Pflicht.** Wer dieses Mapping verantwortet |
| 5 | `location_reference` | Referenz | — | **Verweis** auf den Ort — nie ein Klartextpfad im Core Repository |
| 6 | `collection` | Kennung | — | Logische Sammlung für Berechtigungen und Suche |
| 7 | `enabled` | bool | **`false`** | Ein Mapping ist nach dem Anlegen **nie** automatisch aktiv |
| 8 | `read_only` | bool | **`true`** | Schreibzugriff ist die begründungspflichtige Ausnahme |
| 9 | `allowed_subpaths` | Liste | **leer** | Aufnahmeregeln; **leer bedeutet: nichts wird aufgenommen** |
| 10 | `excluded_subpaths` | Liste | — | Ausschlussregeln; **gewinnen immer** gegen `allowed_subpaths` |
| 11 | `data_class` | Aufzählung | **`unknown`** | `public`, `internal`, `confidential`, `excluded-from-ai`; **nie `secret`** |
| 12 | `ai_transfer_policy` | Aufzählung | **`forbidden`** | `allowed`, `restricted`, `forbidden` |
| 13 | `indexing_policy` | Aufzählung | **`none`** | `none`, `metadata-only`, `full` |
| 14 | `mobile_visibility` | Aufzählung | **`forbidden`** | `allowed`, `authorized-only`, `forbidden` |
| 15 | `verification_status` | Aufzählung | **`unverified`** | `unverified`, `verified`, `rejected` |
| 16 | `approved_by` | Rolle | leer | **Nur ein Mensch.** Leer, solange `unverified` |
| 17 | `approved_at` | Zeitpunkt | leer | Zeitpunkt der Freigabe |
| 18 | `revision` | Kennung | — | Fassung des Mappings; jede Änderung erhöht sie |
| 19 | `deletion_behavior` | Aufzählung | **`tombstone-and-cleanup`** | `tombstone-and-cleanup`, `tombstone-only` |

### Vorgabewerte sind fail-closed

| Feld | Vorgabe | Wirkung |
| --- | --- | --- |
| `enabled` | **`false`** | Ein neues Mapping tut nichts, bis jemand es bewusst aktiviert |
| `read_only` | **`true`** | Schreiben ist die Ausnahme, nicht der Normalfall |
| `allowed_subpaths` | **leer** | Eine leere Aufnahmeregel nimmt **nichts** auf — nicht alles |
| `data_class` | **`unknown`** | Erzwingt eine bewusste Zuweisung |
| `ai_transfer_policy` | **`forbidden`** | Übertragung wird gewährt, nicht angenommen |
| `indexing_policy` | **`none`** | Kein Mapping indexiert versehentlich |
| `mobile_visibility` | **`forbidden`** | Mobile Sichtbarkeit ist eine Entscheidung |
| `verification_status` | **`unverified`** | Der Ausgangszustand ist ungeprüft |

**Feld 9 ist die wichtigste dieser Vorgaben.** Ein leerer Filter, der „alles"
bedeutet, ist die häufigste Ursache für unbeabsichtigten Ingest.

---

## Regeln

| # | Regel | Verhalten bei Verletzung |
| --- | --- | --- |
| **M1** | **Keine realen Pfade, keine privaten Repository-URLs, keine Secrets in diesem Repository** | Blocker; SECRET_INCIDENT_RESPONSE, wenn ein Secret betroffen ist |
| **M2** | `enabled` ist standardmäßig **`false`** | Aktivierung ohne bewusste Setzung ist ungültig |
| **M3** | `read_only` ist standardmäßig **`true`** | `read_only: false` erfordert eine benennbare A0-Entscheidung |
| **M4** | **Unbekannte Datenklasse ist fail-closed** | `data_class: unknown` wird wie `excluded-from-ai` behandelt — **nicht** wie `internal` |
| **M5** | **`excluded-from-ai` erlaubt niemals externe Übertragung** | `ai_transfer_policy` muss `forbidden` sein; jede andere Kombination wird **abgelehnt**, nicht korrigiert |
| **M6** | **Freigabe vor Aktivierung** | `enabled: true` erfordert `verification_status: verified` mit `approved_by` und `approved_at` |
| **M7** | `verified` setzt ausschließlich ein Mensch | Maschinell gesetztes `verified` ist ungültig |
| **M8** | **Mappingänderungen werden versioniert** | Jede Änderung erhöht `revision`; die Vorfassung bleibt nachvollziehbar |
| **M9** | **Gelöschte Mappings erzeugen Tombstones und Derived Cleanup** | Alle abgeleiteten Daten zur betroffenen Quelle werden entfernt |
| **M10** | `excluded_subpaths` gewinnen gegen `allowed_subpaths` | Bei Überschneidung wird ausgeschlossen |
| **M11** | Ein Mapping erweitert nie die Rechte des Slots | Die **restriktivere** Angabe gewinnt |
| **M12** | Unbekanntes Feld oder unbekannter Wert | **Verweigerung**, keine Vorgabe |
| **M13** | Höchstens ein `enabled` Mapping je `slot_id` und Deployment | Zweites Mapping wird abgelehnt |
| **M14** | Ein `test-only` Slot erhält kein produktives Mapping | PS-05 bleibt Fixture |

**M4 und M5 in einem Satz:** Was nicht ausdrücklich klassifiziert und erlaubt
ist, verlässt das System nicht.

---

## Illustratives Beispiel

**Nicht ausführbar. Platzhalter, kein realer Ort.**

```yaml
# BEISPIEL — rein illustrativ, keine Konfiguration
mapping_id: MAP-XX-EXAMPLE
slot_id: PS-XX-EXAMPLE
deployment_profile: B
operator: human-maintainer
location_reference: workspace-reference-placeholder   # kein realer Pfad
collection: example-collection
enabled: false                    # M6: nicht freigegeben
read_only: true
allowed_subpaths: []              # nimmt NICHTS auf
excluded_subpaths:
  - excluded-by-policy-placeholder
data_class: unknown               # M4: wird wie excluded-from-ai behandelt
ai_transfer_policy: forbidden
indexing_policy: none
mobile_visibility: forbidden
verification_status: unverified
approved_by:
approved_at:
revision: 1
deletion_behavior: tombstone-and-cleanup
```

Das Beispiel ist bewusst wirkungslos: nicht freigegeben, nicht aktiviert, ohne
Aufnahmeregel, ohne bestätigte Datenklasse. Genau so entsteht ein Mapping.

---

## Spätere Nachweise

Diese Nachweise sind in **CBP-WP-010** zu erbringen. Keiner von ihnen existiert
heute.

| # | Nachweis | Inhalt |
| --- | --- | --- |
| **1** | **Mapping validiert** | Alle 19 Felder gesetzt; M1 bis M14 geprüft |
| **2** | **Quelle erreichbar** | Der referenzierte Ort existiert und ist lesbar |
| **3** | **Rechte minimal** | `read_only: true`; kein Schreibrecht über das Nötige hinaus |
| **4** | **Ausschlüsse wirksam** | Ein Pfad in `excluded_subpaths` wird nachweislich **nicht** aufgenommen |
| **5** | **Keine Secrets** | Secret-Scan über den gemappten Bereich ohne Fund |
| **6** | **Datenklasse bestätigt** | `data_class` ist nicht `unknown` und menschlich bestätigt |
| **7** | **AI-Transfer-Regel getestet** | Bei `forbidden`: Inhalt erreicht nachweislich keinen Modellkontext |

**Nachweis 4 und 7 sind Negativtests.** Sie gelten nur als bestanden, wenn der
verbotene Fall **tatsächlich scheitert** — nicht, wenn eine Warnung erscheint.

---

## Ablage und Datenschutz

| Gegenstand | Ablage |
| --- | --- |
| Dieses Schema | Core Repository — `publication-capable by design` |
| Ausgefüllte Mappings | **Private Operator Workspace** |
| Zugangsdaten | **Secret Store** — nie in einem Mapping |
| Ingest-Ergebnisse | Runtime Data Area |

Der Grund steht in [ADR-0006](../decisions/ADR-0006-logische-source-slots.md)
und in [REPOSITORY_AND_WORKSPACE_PLAN.md](REPOSITORY_AND_WORKSPACE_PLAN.md):
Ausgefüllte Mappings sind der Ort, an dem private Pfade und
Repository-Adressen zuerst entstehen. Landen sie in der Git-Historie des Core
Repositorys, ist das **R-01**.

## Was offen bleibt

| Punkt | Register | Status |
| --- | --- | --- |
| Ablageort des kanonischen Bestands | **OD-05** | **offen** |
| Konkrete Quellen und Nicht-Quellen | **OD-06** | **offen** |
| Repository-Struktur | OD-26 | offen |
| Secret-Store-Technologie | nicht registriert | Aufnahme vorgeschlagen (CBP-WP-009) |

Dieses Schema beschreibt, **wie** ein Mapping aussehen muss — nicht, welche
existieren und worauf sie zeigen. **OD-05 und OD-06 bleiben offen** und werden
ausschließlich durch den Human Maintainer geschlossen.

## Status

**PROPOSED.** **Es existiert kein Mapping.** Kein Slot ist aktiviert, keine
Quelle angebunden, kein Ingest ausgeführt.

**Implementierung erlaubt: nein.**
