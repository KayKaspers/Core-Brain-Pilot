# Project Brain – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Überarbeitet in | CBP-WP-004 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

Kuratiertes Projektgedächtnis und Einstiegspunkt für jede neue Sitzung. Dieses
Dokument **verweist**, statt Inhalte zu duplizieren.

## Projektstatus

**Phase 0 – Discovery und Scope Lock.**

Das Repository enthält ausschließlich Dokumentation. Keine Implementierung,
keine Laufzeit, keine Installation, kein Index, kein Wissensbestand.

| Feld | Wert |
| --- | --- |
| Aktuelles Work Package | CBP-WP-004 (`in-review`) |
| Nächstes Gate | **G0 – Discovery and Scope Lock — NOT PASSED** |
| G0-Kriterien | **47**, dreistufig klassifiziert |
| davon blockierend | **25** Core Required (zuvor 45) |
| davon `accepted` | **18** |
| verbleibende Blocker | **7** (davon 6 Benchmark) |
| Implementierte Capabilities | **keine (0 von 29)** |
| Commits | 4 |

## Ziel

Ein serverzentriertes und portables KI-Wissens- und Arbeitssystem, das
Implementation Agents die kleinste ausreichende Menge relevanter, aktueller,
autoritativer und datenschutzrechtlich erlaubter Informationen bereitstellt.

**Das Problem dahinter:** zu hoher Token- und Kontextverbrauch. Das System soll
Limits nicht umgehen, sondern Kontext effizienter nutzen.

## Pilotumfang — festgelegt in CBP-WP-003

Der Human Discovery Intake hat den Umfang auf **Profilebene** entschieden.
Konkrete Infrastrukturwerte sind bewusst nicht erhoben.

| Dimension | Festlegung | Entscheidung |
| --- | --- | --- |
| Betriebsprofil | Proxmox-VM, dedizierte Linux-VM als Referenzbetrieb | D-015 |
| Anwendungslaufzeit | Docker Compose **bevorzugt** innerhalb der VM | D-016 |
| Portabilität | Weitere Profile bleiben dokumentierbar, kein Lock-in | D-017 |
| Nutzung | Einzelperson, 1 Nutzer; Multi-User kein Pflichtumfang | D-018 |
| Quellen im Pilot | Markdown-Verzeichnisse, Git-Repositories, Chat-Handoffs, Obsidian-Vault als Markdown | HDI A3 |
| Quellen später | PDF und Office **nur über kontrollierte Quarantäne** | D-019 |
| Datenklassen im Pilot | `public`, `internal` | HDI A4 |
| `confidential` | nicht im Pilot, Architektur muss die Klasse tragen | D-020 |
| `excluded-from-ai` | **von Anfang an im Modell**, Sperrwirkung mit Testdaten prüfen | D-021 |
| Personenbezogene Daten | nicht im Pilot; spätere Aufnahme nur nach gesonderter Prüfung | D-022 |
| Zugriff | privates VPN oder privates Netz, keine öffentliche Freigabe | D-023 |
| Web-UI und mobil | im Pilot — Web-UI erst nach funktionierendem Retrieval | D-024 |
| Obsidian nativ, Wiki, Connectoren, Graph | vertagt beziehungsweise nicht Pilotumfang | D-025 |

Vollständig in
[docs/discovery/HUMAN_DISCOVERY_INPUT.md](../docs/discovery/HUMAN_DISCOVERY_INPUT.md).

## Architekturstand

Kein Komponentenschnitt. Festgehalten sind Prinzipien, Grenzen und seit
CBP-WP-003 ein dreistufiges Kriterienmodell.

- 16 Kernprinzipien (A2, kein ADR) —
  [ARCHITECTURE_PRINCIPLES.md](../docs/architecture/ARCHITECTURE_PRINCIPLES.md)
- 6 Vertrauensgrenzen plus Sicherheitsmodell mit fünf Berechtigungsstufen,
  **keine durchgesetzt** —
  [TRUST_BOUNDARIES.md](../docs/architecture/TRUST_BOUNDARIES.md)
- 5 Datenklassen mit Flussmatrix —
  [DATA_CLASSIFICATION.md](../docs/privacy/DATA_CLASSIFICATION.md)
- Context Budgets B0–B4 —
  [CONTEXT_BUDGETS.md](../docs/architecture/CONTEXT_BUDGETS.md)
- **Kriterienmodell Core Required / Deployment Required / Conditional** (D-026)
  — [G0_SCOPE_LOCK_CRITERIA.md](../docs/discovery/G0_SCOPE_LOCK_CRITERIA.md)

**Invariante:** Der Verlust eines Indexes oder einer Oberfläche darf nicht zum
Verlust des Wissens führen.

**Klarstellung:** Index und Suche laufen lokal, die Sprachverarbeitung nicht.
Ausgewählte Inhalte werden an Claude übertragen — daraus entsteht die
Notwendigkeit der Datenklassifikation. **Standardwert: Übertragung wird
verweigert, bis eine Datenklasse sie erlaubt.**

## Entscheidungen

Angenommene ADRs: **5** — ADR-0001 bis ADR-0005, alle `accepted` und A0/A5-belegt.

26 getroffene Entscheidungen, davon 20 mit A0. 25 offene, davon 10 mit P0.
Geführt in
[project-system/DECISION_REGISTER.md](../project-system/DECISION_REGISTER.md).

**Ein Konflikt wurde durch A0 aufgelöst:** In CBP-WP-002 hatte ich Docker
Compose gestützt auf Projektübergabe §4 (A5) von „bevorzugt" zu „vorgesehen"
abgeschwächt. Der Human Maintainer bestätigt nun ausdrücklich „bevorzugte
Anwendungslaufzeit". **A0 schlägt A5**; die Abschwächung ist aufgehoben. Die
Nachführung in `PROJECT_DEFINITION.md` steht als OD-31 aus — die Datei war in
CBP-WP-003 nicht änderbar.

## Risiken

32 erfasste Risiken, davon 17 hoch. Sieben in CBP-WP-004 verändert. Geführt in
[project-system/RISK_REGISTER.md](../project-system/RISK_REGISTER.md).

**Weiterhin kritisch:** Berechtigungen ohne technische Durchsetzung und ohne
erhobene Zuordnung (R-25, R-27) · ungeprüfte Sperrwirkung von
`excluded-from-ai` (R-31) · fehlende Quarantäne für Nicht-Markdown-Quellen
(R-32) · 16 vertagte Deployment-Kriterien ohne zuständiges Gate (R-34) ·
kein Benchmark (R-21).

## Offene Fragen

- **G0:** 25 Core-Required-Kriterien, davon **7 noch nicht `accepted`** —
  [G0_SCOPE_LOCK_CRITERIA.md](../docs/discovery/G0_SCOPE_LOCK_CRITERIA.md)
- **Fragebogen:** 56 Fragen, davon 8 offen und Core Required —
  [DISCOVERY_QUESTIONS.md](../docs/discovery/DISCOVERY_QUESTIONS.md)
- **Fehlende Information:** OI-02, OI-06 bis OI-09 offen —
  [OPEN_INFORMATION.md](../docs/discovery/OPEN_INFORMATION.md)

Der dominierende Rest ist der **Benchmarkblock**: sechs der sieben Blocker.
Der siebte ist D-1 — die Quellenarten sind entschieden, der konkrete Bestand
nicht (OD-05, OD-06).

## Lessons Learned

**Aus CBP-WP-001:** Ein Work Package, das seine fachliche Substanz mitführt,
bleibt ausführbar, auch wenn hinterlegtes Projektwissen im Sitzungskontext
fehlt.

**Aus CBP-WP-002:** Zwei Ausführungsversuche endeten in der Vorprüfung mit
BLOCKED, beide vor jeder Dateiänderung. Ohne Vorprüfung wäre ein Quellenabgleich
mit erfundenen Seitenreferenzen entstanden. Der Abgleich fand außerdem eine
sachlich falsche Aussage im Fundament (Ü-01), die aus dem Work-Package-Wortlaut
allein nicht erkennbar war.

**Aus CBP-WP-003, erste Lektion:** Fortgeschriebene Kennzahlen driften. Die in
CBP-WP-002 berichteten Summen (41/39/35/55) waren falsch addiert; die
tatsächlichen Werte sind 47/45/38/56. Die Dokumente selbst waren korrekt — nur
die Summen. Konsequenz: Kennzahlen werden ausgezählt, nicht fortgeschrieben
(R-33).

**Aus CBP-WP-003, zweite Lektion:** Der erste Fragebogen mit 15 Fragen war
handwerklich korrekt, aber konzeptionell falsch — er hätte den allgemeinen
Scope Lock von einer konkreten Proxmox-Installation abhängig gemacht. Das
Nova-Review hat das erkannt und das dreistufige Kriterienmodell eingeführt.
Ergebnis: 20 Blocker weniger, ohne ein Kriterium zu streichen. Die Trennung
zwischen Produktentscheidung und Installationsdetail war die eigentliche
Erkenntnis.

## Nächste Arbeitspakete

Siehe
[project-system/WORK_PACKAGE_QUEUE.md](../project-system/WORK_PACKAGE_QUEUE.md).

Vorgeschlagen, **nicht freigegeben**: CBP-WP-004 — Generic Architecture and
Deployment Profiles.

## Rückmeldung an Nova

CBP-WP-003 ist ausgeführt. Sechs Antworten erhoben, 12 A0-Entscheidungen
erfasst, keine Antwort erfunden oder erweitert. Acht Core-Required-Kriterien
stehen auf `accepted`, vier auf `answered`.

Das dreistufige Kriterienmodell reduziert die G0-Blocker von 45 auf 25. Die 16
Deployment-Required-Kriterien sind **vertagt, nicht gestrichen** — sie brauchen
ein eigenes Gate (OD-33, R-34).

**G0 bleibt NOT PASSED.** 17 der 25 Core-Required-Kriterien sind noch nicht
`accepted`.

Zwei Lücken sind dem überarbeiteten Fragebogen selbst geschuldet, nicht dem
Human Maintainer: das Berechtigungsmodell (OI-08) und das Secret-Verfahren im
Schadensfall (OI-09) wurden nicht erhoben.
