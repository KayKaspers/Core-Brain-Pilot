# Architecture Decision Records — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Angenommene ADRs | **5** |
| Vorgeschlagene ADRs | **1** (ADR-0006) |
| Überarbeitet in | CBP-WP-006 |
| Stand | 2026-07-20 |

Dieses Verzeichnis enthält Architecture Decision Records. Ein angenommener ADR
hat Autoritätsklasse **A1** und bindet nachfolgende Arbeit.

## Aktueller Stand

Fünf **angenommene** ADRs aus CBP-WP-004, jeder durch eine ausdrückliche
A0-Entscheidung oder eine A5-Originalquelle belegt — plus **ein Vorschlag** aus
CBP-WP-006.

**ADR-0006 ist `proposed`, nicht `accepted`.** Er trägt A3 und wird erst durch
die Annahme des Human Maintainers bindend. Ein Implementation Agent nimmt
keinen ADR an.

| ADR | Titel | Status | Belegt durch |
| --- | --- | --- | --- |
| [ADR-0001](ADR-0001-deployment-neutraler-core.md) | Deployment-neutraler Core mit austauschbaren Adaptern | `accepted` | D-017 |
| [ADR-0002](ADR-0002-referenzprofil-und-pilotlaufzeit.md) | Proxmox-VM als Referenz, Docker Compose als bevorzugte Pilotlaufzeit | `accepted` | D-015, D-016 |
| [ADR-0003](ADR-0003-canonical-derived-trennung.md) | Strikte Trennung von kanonischen und abgeleiteten Daten | `accepted` | Übergabe §5, D-005 |
| [ADR-0004](ADR-0004-technisches-permission-enforcement.md) | Technische Durchsetzung von Berechtigungen | `accepted` | Übergabe §10, D-023 |
| [ADR-0005](ADR-0005-deployment-readiness-check.md) | Deployment Readiness Check als eigenes Prüfmodell | `accepted` | D-026 |
| [ADR-0006](ADR-0006-logische-source-slots.md) | Logische Source Slots statt eingebetteter Wissensbestände | **`proposed`** | Übergabe §13, ADR-0001 |

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
