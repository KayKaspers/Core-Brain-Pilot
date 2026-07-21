# Pilot Source Contract

| Feld | Wert |
| --- | --- |
| **Status** | **PROPOSED FOR G0 ACCEPTANCE** |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-006 |
| Autoritätsklasse | A3 (Entscheidungsvorlage) |
| Belegt | G0-Kriterium **D-1** |
| Stand | 2026-07-21 |

Dieser Vertrag definiert den produktiven Quellenumfang des ersten Piloten über
**logische Source Slots** — produktunabhängig und deployment-neutral.

---

## Die tragende Unterscheidung

| Ebene | Gegenstand | Wo entschieden |
| --- | --- | --- |
| **Logical Source Slot** | Welche **Art** von Quelle aufgenommen werden darf und welche Regeln dafür gelten | **hier, für G0** |
| **Deployment Mapping** | Die **konkrete Zuordnung** eines Slots zu einem Pfad, Repository, Volume oder System einer bestimmten Installation | später, im [DRC](../operations/DEPLOYMENT_READINESS_CHECK.md) oder bei der Einrichtung einer Collection |

> **G0 benötigt den Logical Source Contract. Ein konkretes Deployment benötigt
> zusätzlich das Deployment Mapping.**

**Private lokale Pfade, Repository-URLs und Fremdsysteme dürfen im allgemeinen
Core-Repository nicht vorausgesetzt werden.** Dieses Dokument enthält deshalb
keinen einzigen realen Pfad. Wo eine Angabe nötig wäre, steht der Verweis auf
das Deployment Mapping.

## Statuswerte

| Pilotstatus | Bedeutung |
| --- | --- |
| `active` | Im ersten produktiven Pilot vorgesehen |
| `test-only` | Nur Testartefakt, nie produktiv |
| `deferred` | Ausdrücklich zurückgestellt |

---

## PS-01 — Core Project Control

| Feld | Wert |
| --- | --- |
| **ID** | PS-01 |
| **Zweck** | Projektsteuerung: das System soll seinen eigenen Zustand kennen |
| **Quelleigentümer** | Human Maintainer |
| **Zulässige Formate** | Markdown |
| **Standard-Datenklasse** | `internal`; einzelne Dokumente `public` |
| **Autoritätsregel** | **A0 bis A5** je Dokumenttyp — A0 Beschlüsse, A1 angenommene ADRs, A2 Status und Register, A3 Roadmap und Gates, A4 README, A5 Handoffs |
| **AI-Transfer** | `allowed` für `public` und `internal` |
| **Indexierbarkeit** | ja |
| **Schreibregel** | Nur über den autorisierten Review-Pfad; Indexer und Retrieval haben **kein** Schreibrecht |
| **Freigabeverfahren** | Human Maintainer, `write with approval`; Push `publish with approval` |
| **Revisionsmodell** | Git-Historie; Revision je Dokument im Frontmatter |
| **Löschmodell** | Tombstone im Löschprotokoll; Git-Historie bleibt |
| **Pilotstatus** | **`active`** |
| **Deployment Mapping** | **nicht erforderlich** — der Slot ist das Projektrepository selbst |

**Inhalt:** README · ADRs · Project Manifest · Project Brain · Decision
Register · Risk Register · Work Packages · freigegebene Status- und
Gate-Dokumente.

**Enthält keine privaten Wissensbestände.** PS-01 ist der einzige Slot, der
ohne Deployment Mapping auskommt — und der einzige, der im allgemeinen
Core-Repository liegt.

## PS-02 — Operator Markdown Knowledge Root

| Feld | Wert |
| --- | --- |
| **ID** | PS-02 |
| **Zweck** | Der eigentliche Wissensbestand des Betreibers |
| **Quelleigentümer** | Betreiber (im Pilot: Human Maintainer) |
| **Zulässige Formate** | **Markdown** |
| **Standard-Datenklasse** | `internal`; je Quelle oder Collection abweichend zuweisbar |
| **Autoritätsregel** | A2 bis A6 je Dokument; **A0 und A1 nur mit ausdrücklicher Kennzeichnung** |
| **AI-Transfer** | je Datenklasse; `confidential` nur begründet, `excluded-from-ai` **nie** |
| **Indexierbarkeit** | ja, außer `excluded-from-ai` und `secret` |
| **Schreibregel** | **Standardmäßig `read-only` für Indexer und Retrieval.** Änderungen ausschließlich über den autorisierten Review-Pfad |
| **Freigabeverfahren** | Aufnahme einer Collection: Human Maintainer. Klassenänderung: Human Maintainer |
| **Revisionsmodell** | Content Hash plus Änderungszeitpunkt; Git, sofern der Bestand versioniert ist |
| **Löschmodell** | Tombstone; Entfernung aus Index, Embeddings, Cache und Context Packs nach dem Rebuild-Vertrag |
| **Pilotstatus** | **`active`** |
| **Deployment Mapping** | **erforderlich** — konkreter Ort wird erst dort festgelegt |

**Inhalt:** vom Betreiber ausdrücklich freigegebene Markdown-Verzeichnisse;
optional ein Obsidian-Vault, behandelt als **normaler Markdown-Bestand**, nicht
als Obsidian-Integration.

**Keine Secrets.** Der Fund eines Secrets ist ein Blocker nach
[SECRET_INCIDENT_RESPONSE.md](../security/SECRET_INCIDENT_RESPONSE.md).

## PS-03 — Selected Git Repositories

| Feld | Wert |
| --- | --- |
| **ID** | PS-03 |
| **Zweck** | Projektwissen aus ausgewählten Repositories |
| **Quelleigentümer** | Human Maintainer |
| **Zulässige Formate** | Markdown; weitere Textformate nur nach gesonderter Freigabe |
| **Standard-Datenklasse** | `internal` |
| **Autoritätsregel** | A1 bis A5 je Dokumenttyp |
| **AI-Transfer** | je Datenklasse |
| **Indexierbarkeit** | ja, nur für Bereiche der Allowlist |
| **Schreibregel** | **Standard im Pilot: `read`.** `draft` nur in ausdrücklich freigegebenen Workspaces. **Kein automatischer Commit oder Push** |
| **Freigabeverfahren** | **Repository-Allowlist**, gepflegt durch den Human Maintainer; Lese- und Schreibrechte getrennt geführt |
| **Revisionsmodell** | Git-Commit-Referenz |
| **Löschmodell** | Entfernung aus der Allowlist plus Index-Rebuild; Tombstone für entfernte Bereiche |
| **Pilotstatus** | **`active`** |
| **Deployment Mapping** | **erforderlich** — konkrete Repository-URLs sind Deployment- oder Betreiberkonfiguration und **nicht Bestandteil dieses Vertrags** |

Ein Repository außerhalb der Allowlist ist **nicht** zugänglich — auch nicht
lesend. Default deny gilt auch hier.

## PS-04 — Approved Chat Handoffs

| Feld | Wert |
| --- | --- |
| **ID** | PS-04 |
| **Zweck** | Kompakte Projektübergaben als kuratierte Wissensquelle |
| **Quelleigentümer** | Human Maintainer |
| **Zulässige Formate** | Markdown |
| **Standard-Datenklasse** | `internal` |
| **Autoritätsregel** | **A5 erst nach ausdrücklicher Freigabe.** Automatisch erzeugte Zusammenfassungen bleiben **A6** |
| **AI-Transfer** | `allowed` für `internal` |
| **Indexierbarkeit** | ja |
| **Schreibregel** | Nur über den Review-Pfad |
| **Freigabeverfahren** | Ausdrückliche Freigabe je Handoff; **Herkunft und Prüfzeitpunkt sind Pflichtfelder** |
| **Revisionsmodell** | Revision plus Prüfzeitpunkt |
| **Löschmodell** | Tombstone |
| **Pilotstatus** | **`active`** |
| **Deployment Mapping** | erforderlich, sofern außerhalb von PS-01 abgelegt |

**Keine unkontrollierten vollständigen Chatarchive.** Ein Rohprotokoll ist kein
Handoff: es ist unkuratiert, enthält Denkschritte und potenziell Secrets oder
ausgeschlossene Inhalte.

**Keine Secrets, keine `excluded-from-ai`-Inhalte.**

## PS-05 — Synthetic Benchmark Fixtures

| Feld | Wert |
| --- | --- |
| **ID** | PS-05 |
| **Zweck** | Messbarkeit des Retrieval-Pfads gegen eine konstruierte Grundwahrheit |
| **Quelleigentümer** | Human Maintainer (Dataset Owner) |
| **Zulässige Formate** | Markdown |
| **Standard-Datenklasse** | gemischt; Etiketten auf harmlosem Text |
| **Autoritätsregel** | **A0 bis A6 — ausschließlich innerhalb des Benchmarks** |
| **AI-Transfer** | je Fixture; `excluded-from-ai`-Fixtures **nie** |
| **Indexierbarkeit** | nur in einer **getrennten Testcollection**, nie im produktiven Index |
| **Schreibregel** | Nur über Dataset Governance |
| **Freigabeverfahren** | [DATASET_GOVERNANCE.md](../benchmark/DATASET_GOVERNANCE.md), MAJOR-Versionierung |
| **Revisionsmodell** | Dataset-Version plus Revision je Fixture |
| **Löschmodell** | MAJOR-Version, Tombstone im Dataset |
| **Pilotstatus** | **`test-only`** |
| **Deployment Mapping** | nicht erforderlich — liegt unter `benchmarks/` |

> **Kein produktiver Wissensbestand.** Die Autorität eines Fixtures endet an der
> Korpusgrenze. Das **synthetische A0-Fixture besitzt keine reale
> Projektgeltung** und darf niemals als Beleg für eine Core-Brain-Entscheidung
> zitiert werden — kritischer Fehler 9 der Evaluationsrubrik.

---

## Deferred Source Slots

### PS-06 — PDF and Office Documents

| Feld | Wert |
| --- | --- |
| **Pilotstatus** | **`deferred`** |
| **Voraussetzung** | Quarantäne-, Parser- und Freigabepipeline (TB-1, TB-2, Capability 5) |
| **Grund** | D-019: PDF und Office gelangen **nicht ungeprüft** in den kanonischen Bestand |

Nicht Bestandteil des ersten produktiven Markdown-Retrieval-Piloten. Ein
Benchmark über Formate, die das System nicht sicher aufnehmen kann, misst
nichts. Erfasst als Risiko R-32.

### PS-07 — External Connectors

| Feld | Wert |
| --- | --- |
| **Pilotstatus** | **`deferred`** |
| **Betrifft** | Gmail, Slack, Drive, Notion und vergleichbare Systeme |
| **Voraussetzung** | Je Connector ein eigener Datenschutz-, ACL-, Sync- und **Löschprozess** |
| **Grund** | D-025; Sperrliste `DO_NOT_START.md` |

Der Löschprozess ist der schwierigste Teil: ein Connector, der Inhalte holt,
aber Löschungen im Quellsystem nicht nachvollzieht, erzeugt einen Bestand, der
Gelöschtes weiterführt.

---

## Übersicht

| Slot | Name | Pilotstatus | Mapping nötig | Standardklasse |
| --- | --- | --- | --- | --- |
| PS-01 | Core Project Control | **`active`** | nein | `internal` |
| PS-02 | Operator Markdown Knowledge Root | **`active`** | **ja** | `internal` |
| PS-03 | Selected Git Repositories | **`active`** | **ja** | `internal` |
| PS-04 | Approved Chat Handoffs | **`active`** | ja | `internal` |
| PS-05 | Synthetic Benchmark Fixtures | `test-only` | nein | gemischt |
| PS-06 | PDF and Office Documents | `deferred` | — | — |
| PS-07 | External Connectors | `deferred` | — | — |

**Vier aktive Slots, ein Testslot, zwei zurückgestellte.**

## Ausgeschlossene Inhalte — slotübergreifend

| Ausgeschlossen | Regel |
| --- | --- |
| **Secrets** | In **jedem** Slot verboten. Auch synthetisch. Fund = Blocker |
| **`excluded-from-ai`** | Niemals an ein externes Modell; lokal klassifizierbar |
| **Personenbezogene Daten** | Nicht im ersten Pilot (D-022); spätere Aufnahme nur nach gesonderter Prüfung |
| **`confidential`** | Nicht im ersten Pilot (D-020); architektonisch getragen |
| **Unkuratierte Chatarchive** | Kein zulässiger Handoff |
| **Repositories außerhalb der Allowlist** | Default deny |

## Was dieser Vertrag nicht leistet

Er benennt **keine konkrete Quelle**. Er legt fest, welche **Arten** von
Quellen zulässig sind und unter welchen Regeln — nicht, welches Verzeichnis
oder welches Repository tatsächlich angebunden wird.

| Offen | Register |
| --- | --- |
| Ablageort des kanonischen Bestands | **OD-05** |
| Konkrete Quellen und Nicht-Quellen im ersten Scope | **OD-06** |
| Repository-Layout | **OD-26** |
| Konkrete Deployment Mappings | DRC, `not-evaluated` |

**Diese vier Punkte bleiben offen.** Dieser Vertrag schließt sie nicht und darf
sie nicht schließen.

## Status

**PROPOSED FOR G0 ACCEPTANCE.** Es wurde **keine Quelle angebunden**, kein
Index gebaut, kein Mapping erzeugt. Der Vertrag beschreibt den zulässigen
Quellenraum — er füllt ihn nicht.
