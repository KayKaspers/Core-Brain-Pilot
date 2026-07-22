# Architecture Decision Records — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Angenommene ADRs | **11** |
| Vorgeschlagene ADRs | 0 |
| Überarbeitet in | **CBP-WP-014** |
| Stand | 2026-07-22 |

Dieses Verzeichnis enthält Architecture Decision Records. Ein angenommener ADR
hat Autoritätsklasse **A1** und bindet nachfolgende Arbeit.

## Aktueller Stand

**Elf angenommene ADRs.** Fünf aus CBP-WP-004, jeder durch eine ausdrückliche
A0-Entscheidung oder eine A5-Originalquelle belegt; **ADR-0006** am 2026-07-21
angenommen (D-028); **ADR-0007** am selben Tag (D-029, D-030); **ADR-0008**
(D-031, D-032, D-033) und **ADR-0009** (D-034 bis D-037) ebenfalls; **ADR-0010**
am 2026-07-22 (D-038 bis D-041, Ingest-Quarantäne-MVP); **ADR-0011** am selben
Tag (D-042 bis D-045, Source-Registry-MVP).

Alle elf tragen **A1** und binden nachfolgende Arbeit. Es steht kein Vorschlag
mehr offen.

> **ADR-0006 trägt seit CBP-WP-010 einen Klarstellungsnachtrag** — *non-substantive
> clarification*, A1. Entscheidung und Status sind unverändert; der Nachtrag
> stellt klar, dass „veröffentlichbar" eine Architekturabsicht beschreibt und
> **keine öffentliche Freigabe**.

| ADR | Titel | Status | Belegt durch |
| --- | --- | --- | --- |
| [ADR-0001](ADR-0001-deployment-neutraler-core.md) | Deployment-neutraler Core mit austauschbaren Adaptern | `accepted` | D-017 |
| [ADR-0002](ADR-0002-referenzprofil-und-pilotlaufzeit.md) | Proxmox-VM als Referenz, Docker Compose als bevorzugte Pilotlaufzeit | `accepted` | D-015, D-016 |
| [ADR-0003](ADR-0003-canonical-derived-trennung.md) | Strikte Trennung von kanonischen und abgeleiteten Daten | `accepted` | Übergabe §5, D-005 |
| [ADR-0004](ADR-0004-technisches-permission-enforcement.md) | Technische Durchsetzung von Berechtigungen | `accepted` | Übergabe §10, D-023 |
| [ADR-0005](ADR-0005-deployment-readiness-check.md) | Deployment Readiness Check als eigenes Prüfmodell | `accepted` | D-026 |
| [ADR-0006](ADR-0006-logische-source-slots.md) | Logische Source Slots statt eingebetteter Wissensbestände | **`accepted`** | **D-028 (A0), 2026-07-21** |
| [ADR-0007](ADR-0007-repository-und-workspace-grenze.md) | Repository-Zielstruktur und Workspace-Grenze | **`accepted`** | **D-029, D-030 (A0), 2026-07-21** |
| [ADR-0008](ADR-0008-pilot-source-mapping-konvention.md) | Pilot Source Mapping Konvention | **`accepted`** | **D-031, D-032, D-033 (A0), 2026-07-21** |
| [ADR-0009](ADR-0009-technische-sicherheitsgrundlage.md) | Technische Sicherheitsgrundlage | **`accepted`** | **D-034 bis D-037 (A0), 2026-07-21** |
| [ADR-0010](ADR-0010-ingest-quarantaene-mvp.md) | Ingest-Quarantäne MVP | **`accepted`** | **D-038 bis D-041 (A0), 2026-07-22** |
| [ADR-0011](ADR-0011-deterministische-source-registry.md) | Deterministische Source Registry und Catalog | **`accepted`** | **D-042 bis D-045 (A0), 2026-07-22** |

Weitere Kandidaten sind in
[project-system/DECISION_REGISTER.md](../../project-system/DECISION_REGISTER.md)
als offene Entscheidungen geführt. Neue oder weitergehende
Architekturentscheidungen bleiben `proposed`, bis der Human Maintainer sie
annimmt.

## Namenskonvention

```
ADR-NNNN-kurzer-titel.md
```

Fortlaufend ab `ADR-0001`. Nummern werden nicht wiederverwendet, auch nicht
nach Ablehnung.

## Status

| Status | Bedeutung | Autorität |
| --- | --- | --- |
| `proposed` | Vorgeschlagen, nicht bindend | A3 |
| `accepted` | Angenommen und bindend | **A1** |
| `rejected` | Abgelehnt, aus Nachvollziehbarkeit erhalten | — |
| `superseded` | Durch späteren ADR ersetzt | historisch |

Ein ADR wird **nie gelöscht** und nie rückwirkend umgeschrieben. Änderungen
erfolgen durch einen neuen ADR, der den alten auf `superseded` setzt.

## Struktur eines ADR

```markdown
# ADR-NNNN — Titel

| Feld | Wert |
| --- | --- |
| Status | proposed \| accepted \| rejected \| superseded |
| Datum | YYYY-MM-DD |
| Entscheider | Human Maintainer |
| Supersedes | — |
| Superseded by | — |
| Belegt durch | Quelle mit Autoritätsklasse |

## Kontext
Welche Situation zwingt zu einer Entscheidung?

## Entscheidung
Was wird festgelegt? Aktiv und eindeutig formuliert.

## Alternativen
Was wurde erwogen und aus welchem Grund verworfen?

## Konsequenzen
Was wird dadurch leichter, was schwerer? Welche Türen schließen sich?

## Bezug
Betroffene Prinzipien, Capabilities, Kriterien, Work Packages.
```

## Wer entscheidet

Ein ADR wird durch den **Human Maintainer** angenommen. Nova kann einen ADR
vorschlagen, ein Implementation Agent kann einen Entwurf im Status `proposed`
verfassen — die Annahme bleibt menschlich.

Die fünf ADRs aus CBP-WP-004 tragen `accepted`, weil sie ausschließlich bereits
getroffene A0-Entscheidungen (D-015 bis D-026) und belegte A5-Quellen
dokumentieren. Sie führen keine neue Festlegung ein.

## Verhältnis zum Autoritätsmodell

Ein angenommener ADR (A1) schlägt README (A4), abgeleitete Zusammenfassungen
(A6) und Projektchat-Übergaben (A5). Er wird seinerseits nur durch einen
ausdrücklichen Human-Maintainer-Beschluss (A0) oder einen späteren ADR
verdrängt.
