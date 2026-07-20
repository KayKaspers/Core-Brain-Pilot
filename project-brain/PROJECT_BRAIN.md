# Project Brain – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Autoritaetsklasse | A2 |
| Stand | 2026-07-20 |

Kuratiertes Projektgedaechtnis. Dieses Dokument ist der Einstiegspunkt fuer
jede neue Sitzung — es fasst zusammen und **verweist**, statt Inhalte zu
duplizieren.

## Projektstatus

**Phase 0 – Discovery und Scope Lock.**

Das Repository enthaelt ausschliesslich Dokumentation. Es existiert keine
Implementierung, keine Laufzeit, keine Installation, kein Index und kein
Wissensbestand.

| Feld | Wert |
| --- | --- |
| Aktuelles Work Package | CBP-WP-001 |
| Naechstes Gate | G0 – Discovery and Scope Lock |
| Implementierte Capabilities | keine (0 von 29) |
| Commits | keiner |
| Remote | keines |

## Ziel

Core Brain Pilot ist ein serverzentriertes und portables KI-Wissens- und
Arbeitssystem. Es soll Implementation Agents die kleinste ausreichende Menge
relevanter, aktueller, autoritativer und datenschutzrechtlich erlaubter
Informationen bereitstellen.

Vollstaendig in
[docs/architecture/PROJECT_DEFINITION.md](../docs/architecture/PROJECT_DEFINITION.md).

## Architekturstand

Es existiert **kein** Architekturentwurf im Sinne eines Komponentenschnitts.
Festgehalten sind bisher nur Prinzipien und Vertrauensgrenzen:

- 16 verbindliche Kernprinzipien —
  [ARCHITECTURE_PRINCIPLES.md](../docs/architecture/ARCHITECTURE_PRINCIPLES.md)
- 6 Vertrauensgrenzen TB-1 bis TB-6, keine davon durchgesetzt —
  [TRUST_BOUNDARIES.md](../docs/architecture/TRUST_BOUNDARIES.md)
- 5 Datenklassen, technisch nicht durchgesetzt —
  [DATA_CLASSIFICATION.md](../docs/privacy/DATA_CLASSIFICATION.md)

Tragende Invariante: **kanonisch vs. abgeleitet.** Der Verlust von Index,
Cache, Embeddings, Graph oder Web-UI darf keinen Wissensverlust verursachen.

## Entscheidungen

Angenommene ADRs: **0**.

Offene Entscheidungen werden gefuehrt in
[project-system/DECISION_REGISTER.md](../project-system/DECISION_REGISTER.md),
ADRs in [docs/decisions/](../docs/decisions/README.md).

> Abweichend von der NDF-Vorlage existiert **kein** `project-brain/DECISIONS.md`.
> Begruendung: AB-04 in [ADOPTION_NOTES.md](../docs/ndf/ADOPTION_NOTES.md).

## Risiken

Gefuehrt in
[project-system/RISK_REGISTER.md](../project-system/RISK_REGISTER.md).

Groesstes Risiko in Phase 0: vorgezogene Implementierung, die eine noch nicht
getroffene Architekturentscheidung praejudiziert. Gegenmassnahme ist die
Sperrliste in [DO_NOT_START.md](../docs/product/DO_NOT_START.md).

## Offene Fragen

31 Discovery-Fragen in
[docs/discovery/DISCOVERY_QUESTIONS.md](../docs/discovery/DISCOVERY_QUESTIONS.md),
davon 11 mit Prioritaet P1 (blockieren G0).

Fehlende Eingangsinformation in
[docs/discovery/OPEN_INFORMATION.md](../docs/discovery/OPEN_INFORMATION.md).
Besonders **OI-01**: zwei der vier in CBP-WP-001 genannten verbindlichen
Quellen lagen dem Implementation Agent nicht vor.

## Lessons Learned

Noch keine — das Projekt hat keine Historie.

Erste Beobachtung aus CBP-WP-001: Ein Work Package, das seine eigene fachliche
Substanz vollstaendig mitfuehrt, bleibt auch dann ausfuehrbar, wenn hinterlegtes
Projektwissen im Sitzungskontext fehlt. Das hat OI-01 von einem Blocker zu
einer dokumentierten Luecke reduziert.

## Naechste Arbeitspakete

Siehe [project-system/WORK_PACKAGE_QUEUE.md](../project-system/WORK_PACKAGE_QUEUE.md).

Vorgeschlagen, **nicht freigegeben**: CBP-WP-002 — Gate-G0-Kriterien und
Beantwortung der P1-Discovery-Fragen.

## Rueckmeldung an Nova

CBP-WP-001 ist ausgefuehrt: dokumentarisches Fundament steht, 23 Dateien,
kein Code, kein Commit, kein Remote, keine Secrets.

Zehn NDF-Abweichungen sind in
[ADOPTION_NOTES.md](../docs/ndf/ADOPTION_NOTES.md) als AB-01 bis AB-10
dokumentiert. Entscheidungsbedarf besteht bei drei Punkten: Prompt Mode "Lean"
gegen NDF Full/Standard/Short (AB-01), Manifest als Markdown statt YAML
(AB-03), Registerablage in `project-system/` statt `project-brain/` (AB-04).

Blockierend fuer G0: die Definition der Gate-Kriterien (OI-04) und der Context
Budgets B0–B4 (OI-03).
