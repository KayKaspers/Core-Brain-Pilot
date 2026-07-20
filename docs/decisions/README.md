# Architecture Decision Records — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Angenommene ADRs | **0** |
| Stand | 2026-07-20 |

Dieses Verzeichnis enthaelt Architecture Decision Records. Ein angenommener ADR
hat Autoritaetsklasse **A1** und bindet nachfolgende Arbeit.

## Aktueller Stand

Es existiert **noch kein ADR**. Alle bisherigen Festlegungen sind Entwuerfe zur
Pruefung an Gate G0 und tragen A2 oder niedriger.

Kandidaten fuer die ersten ADRs sind in
[project-system/DECISION_REGISTER.md](../../project-system/DECISION_REGISTER.md)
als offene Entscheidungen gefuehrt.

## Namenskonvention

```
ADR-NNNN-kurzer-titel.md
```

Fortlaufend ab `ADR-0001`. Nummern werden nicht wiederverwendet, auch nicht
nach Ablehnung.

## Status

| Status | Bedeutung | Autoritaet |
| --- | --- | --- |
| `proposed` | Vorgeschlagen, nicht bindend | A3 |
| `accepted` | Angenommen und bindend | **A1** |
| `rejected` | Abgelehnt, aus Nachvollziehbarkeit erhalten | — |
| `superseded` | Durch spaeteren ADR ersetzt | historisch |

Ein ADR wird **nie geloescht** und nie rueckwirkend umgeschrieben. Aenderungen
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

## Kontext
Welche Situation zwingt zu einer Entscheidung?

## Entscheidung
Was wird festgelegt? Aktiv und eindeutig formuliert.

## Alternativen
Was wurde erwogen und aus welchem Grund verworfen?

## Konsequenzen
Was wird dadurch leichter, was schwerer? Welche Tueren schliessen sich?

## Bezug
Betroffene Prinzipien, Capabilities, Work Packages.
```

## Wer entscheidet

Ein ADR wird durch den **Human Maintainer** angenommen. Nova kann einen ADR
vorschlagen, ein Implementation Agent kann einen Entwurf im Status `proposed`
verfassen — die Annahme bleibt menschlich.

## Verhaeltnis zum Autoritaetsmodell

Ein angenommener ADR (A1) schlaegt README (A4), abgeleitete Zusammenfassungen
(A6) und Projektchat-Uebergaben (A5). Er wird seinerseits nur durch einen
ausdruecklichen Human-Maintainer-Beschluss (A0) oder einen spaeteren ADR
verdraengt.
