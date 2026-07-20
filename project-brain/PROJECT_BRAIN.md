# Project Brain – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Überarbeitet in | CBP-WP-002 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

Kuratiertes Projektgedächtnis und Einstiegspunkt für jede neue Sitzung. Dieses
Dokument **verweist**, statt Inhalte zu duplizieren.

## Projektstatus

**Phase 0 – Discovery und Scope Lock.**

Das Repository enthält ausschließlich Dokumentation. Es existiert keine
Implementierung, keine Laufzeit, keine Installation, kein Index und kein
Wissensbestand.

| Feld | Wert |
| --- | --- |
| Aktuelles Work Package | CBP-WP-002 (`in-review`) |
| Nächstes Gate | **G0 – Discovery and Scope Lock — NOT PASSED** |
| G0-Kriterien | 41, davon 39 blockierend, **0 beantwortet** |
| Implementierte Capabilities | **keine (0 von 29)** |
| Commits | 2 |
| Remote | `origin`, gepusht |

## Ziel

Ein serverzentriertes und portables KI-Wissens- und Arbeitssystem, das
Implementation Agents die kleinste ausreichende Menge relevanter, aktueller,
autoritativer und datenschutzrechtlich erlaubter Informationen bereitstellt.

**Das Problem dahinter:** zu hoher Token- und Kontextverbrauch. Das
Claude-Nutzungslimit kann bereits nach wenigen umfangreichen Prompts erreicht
sein. Das System soll Limits nicht umgehen, sondern Kontext effizienter nutzen.

Vollständig in
[docs/architecture/PROJECT_DEFINITION.md](../docs/architecture/PROJECT_DEFINITION.md).

## Architekturstand

Kein Komponentenschnitt. Festgehalten sind Prinzipien und Grenzen:

- 16 Kernprinzipien (A2, nicht als ADR ausgefertigt) —
  [ARCHITECTURE_PRINCIPLES.md](../docs/architecture/ARCHITECTURE_PRINCIPLES.md)
- 6 Vertrauensgrenzen TB-1 bis TB-6 plus Sicherheitsmodell mit fünf
  Berechtigungsstufen, **keine davon durchgesetzt** —
  [TRUST_BOUNDARIES.md](../docs/architecture/TRUST_BOUNDARIES.md)
- 5 Datenklassen mit Flussmatrix, technisch nicht durchgesetzt —
  [DATA_CLASSIFICATION.md](../docs/privacy/DATA_CLASSIFICATION.md)
- Context Budgets B0–B4 —
  [CONTEXT_BUDGETS.md](../docs/architecture/CONTEXT_BUDGETS.md)

**Tragende Invariante:** Der Verlust eines Indexes oder einer Oberfläche darf
nicht zum Verlust des Wissens führen.

**Wichtige Klarstellung aus dem Quellenabgleich:** Index und Suche laufen
lokal, die Sprachverarbeitung nicht. Claude Code verwendet keinen vollständig
lokalen Modellbetrieb — ausgewählte Inhalte werden übertragen. Genau daraus
entsteht die Notwendigkeit der Datenklassifikation.

## Entscheidungen

Angenommene ADRs: **0**.

14 getroffene Entscheidungen, davon 8 mit A0-Rang; 27 offene, davon 14 mit P0.
Geführt in
[project-system/DECISION_REGISTER.md](../project-system/DECISION_REGISTER.md).

Die wichtigsten Festlegungen aus CBP-WP-002: NDF Prompt Modes sind Full,
Standard und Short — „Lean" ist ausschließlich der Name von B1 (D-009). Die
dedizierte Linux-VM ist der Referenzbetrieb, Docker Compose eine noch nicht
implementierte Laufzeit darin (D-013). Wiki, Graph und Web-UI beginnen nicht
vor einem bestandenen Retrieval-Pilot-Gate (D-014).

> Abweichend von der NDF-Vorlage existiert **kein**
> `project-brain/DECISIONS.md` — AB-04 in
> [ADOPTION_NOTES.md](../docs/ndf/ADOPTION_NOTES.md).

## Risiken

29 erfasste Risiken, davon 14 mit Schweregrad hoch. Geführt in
[project-system/RISK_REGISTER.md](../project-system/RISK_REGISTER.md).

Die gravierendsten offenen Punkte: Berechtigungen bestehen nur als Promptregel
und nicht technisch (R-25). Die Datenschutzklassifikation existiert ohne
technische Durchsetzung (R-30). Restore wurde nie geprobt (R-20).

## Offene Fragen

- **Fragebogen:** 55 Fragen, davon 35 mit P0 —
  [DISCOVERY_QUESTIONS.md](../docs/discovery/DISCOVERY_QUESTIONS.md)
- **G0-Kriterien:** 41, davon 39 blockierend —
  [G0_SCOPE_LOCK_CRITERIA.md](../docs/discovery/G0_SCOPE_LOCK_CRITERIA.md)
- **Fehlende Information:** OI-05, OI-06, OI-07 offen —
  [OPEN_INFORMATION.md](../docs/discovery/OPEN_INFORMATION.md)

Der größte inhaltliche Block: sämtliche Infrastruktur-, Netzwerk- und
Datenangaben aus Projektübergabe §19 sind unbeantwortet.

## Lessons Learned

**Aus CBP-WP-001:** Ein Work Package, das seine fachliche Substanz vollständig
mitführt, bleibt auch dann ausführbar, wenn hinterlegtes Projektwissen im
Sitzungskontext fehlt.

**Aus CBP-WP-002:** Zwei Ausführungsversuche endeten in der Vorprüfung mit
BLOCKED — einmal wegen unsauberem Arbeitsbaum und unlesbarem PDF, einmal wegen
fehlender Quelldatei. Beide Abbrüche erfolgten vor jeder Dateiänderung und
haben nichts beschädigt. Die Vorprüfung hat funktioniert; ohne sie wäre im
ersten Versuch ein Quellenabgleich mit erfundenen Seitenreferenzen entstanden.

**Zweite Lektion:** Der Abgleich hat eine sachlich falsche Aussage im Fundament
gefunden (Ü-01, „keine Notwendigkeit, Wissensbestand an externe Dienste zu
senden"). Aus dem Work-Package-Wortlaut allein war das nicht erkennbar — erst
die Originalquelle hat es offengelegt. Das rechtfertigt den Aufwand des
Abgleichs.

## Nächste Arbeitspakete

Siehe
[project-system/WORK_PACKAGE_QUEUE.md](../project-system/WORK_PACKAGE_QUEUE.md).

Vorgeschlagen, **nicht freigegeben**: CBP-WP-003 — Human Discovery Intake and
G0 Evidence Capture.

## Rückmeldung an Nova

CBP-WP-002 ist ausgeführt. Der Quellenabgleich gegen A5-Übergabe und
A6-Textfassung bestätigt 20 Aussagen, ergänzt 16 fehlende Inhalte, schwächt 5
zu starke Formulierungen ab und erfasst 5 Widersprüche. OI-01, OI-03 und OI-04
sind geschlossen.

**G0 bleibt NOT PASSED** — 41 Kriterien liegen vor, keines ist beantwortet.

Entscheidungsbedarf: 14 P0-Entscheidungen, insbesondere OD-26
(Repository-Struktur — drei Vorstellungen nebeneinander) und OD-29 (AB-03 bis
AB-08 sind nur vorläufig für den Bootstrap akzeptiert und vor G0 zu
entscheiden).

Einschränkung: Der PDF-Fließtext war lokal nicht extrahierbar; die Auswertung
stützt sich auf die A6-Textfassung. Eine visuelle Detailprüfung der PDF wird
nicht behauptet (R-22, R-23).
