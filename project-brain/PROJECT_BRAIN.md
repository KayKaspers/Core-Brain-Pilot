# Project Brain – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Überarbeitet in | **CBP-WP-010** |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

Kuratiertes Projektgedächtnis und Einstiegspunkt für jede neue Sitzung. Dieses
Dokument **verweist**, statt Inhalte zu duplizieren.

## Projektstatus

**Phase 0 – COMPLETE.** G0 am 2026-07-21 als **PASSED WITH NOTES** freigegeben (A0). Phase 1 ist **AUTHORIZED FOR PLANNING** — keine Implementierung freigegeben.

Das Repository enthält ausschließlich Dokumentation. Keine Implementierung,
keine Laufzeit, keine Installation, kein Index, kein Wissensbestand.

| Feld | Wert |
| --- | --- |
| Aktuelles Work Package | **CBP-WP-010** (`in-review`) |
| Gate G0 | **PASSED WITH NOTES** — 2026-07-21 |
| G0-Kriterien | **47**, dreistufig klassifiziert |
| davon blockierend | **25** Core Required (zuvor 45) |
| davon `accepted` | **25** — alle |
| verbleibende Blocker | **0** |
| Phase 1 | AUTHORIZED FOR PLANNING — [Backlog](../docs/roadmap/PHASE_1_BACKLOG.md), [Foundation Plan](../docs/roadmap/PHASE_1_FOUNDATION_PLAN.md) |
| Geplante Work Packages | **CBP-WP-011 bis CBP-WP-014**, alle `proposed` |
| **Repository-Struktur** | **entschieden** — Ziel-Monorepo + Workspace W-3 (ADR-0007); **Migration nicht autorisiert** |
| **Mappingkonvention** | **entschieden** — ADR-0008; **0 Mappings, 0 Quellen**, Gate `NOT EVALUATED` |
| Implementierte Capabilities | **keine (0 von 29)** |
| Nachweise oberhalb Stufe 1 | **keine** |
| Commits | **10** |

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

Angenommene ADRs: **8** (ADR-0001 bis ADR-0008). ADR-0006 hält privaten
Bestand konstruktiv außerhalb des Kern-Repositorys (D-028); **ADR-0007**
(D-029, D-030) legt Zielstruktur und Bereichsgrenze fest und **schließt
OD-26**; **ADR-0008** (D-031, D-032, D-033) legt die Mappingkonvention fest.
Alle drei am 2026-07-21.

**33** getroffene Entscheidungen, davon **29** mit A0. **23** offene, davon
**5** mit P0. Geführt in
[project-system/DECISION_REGISTER.md](../project-system/DECISION_REGISTER.md).

> **Zählkorrektur in CBP-WP-008.** Dieses Dokument führte zuvor 26/20/25/10 und
> das Register 28/22/21/8. Die Auszählung ergab **28/24/22/6** — der **vierte**
> Zählfehler des Projekts, erfasst unter R-33. Die Werte oben sind in
> CBP-WP-009 erneut aus den Quelltabellen ausgezählt.

**Ein Konflikt wurde durch A0 aufgelöst:** In CBP-WP-002 hatte ich Docker
Compose gestützt auf Projektübergabe §4 (A5) von „bevorzugt" zu „vorgesehen"
abgeschwächt. Der Human Maintainer bestätigt ausdrücklich „bevorzugte
Anwendungslaufzeit". **A0 schlägt A5**; die Abschwächung ist aufgehoben. Die
Nachführung in `PROJECT_DEFINITION.md` erfolgte in CBP-WP-004; **OD-31 ist
geschlossen**.

## Risiken

32 erfasste Risiken, davon 17 hoch. Geführt in
[project-system/RISK_REGISTER.md](../project-system/RISK_REGISTER.md).

**Weiterhin kritisch:** Berechtigungen ohne technische Durchsetzung und ohne
erhobene Zuordnung (R-25, R-27) · ungeprüfte Sperrwirkung von
`excluded-from-ai` (R-31) · fehlende Quarantäne für Nicht-Markdown-Quellen
(R-32) · 16 vertagte Deployment-Kriterien ohne zuständiges Gate (R-34) ·
kein Benchmark (R-21).

**In CBP-WP-008 wurde kein Risiko geschlossen oder gemindert.** Die
Phase-1-Planung benennt je Risiko einen Schließungsweg und die dafür nötige
Nachweisstufe — beschritten ist keiner. Nach
[PHASE_1_EVIDENCE_PLAN.md](../docs/roadmap/PHASE_1_EVIDENCE_PLAN.md) stehen
sämtliche Artefakte auf **Stufe 1 `dokumentiert`**, und Stufe 1 schließt
definitionsgemäß kein Risiko.

## Offene Fragen

- **G0:** alle 25 Core-Required-Kriterien `accepted`, **0 Blocker** —
  [G0_SCOPE_LOCK_CRITERIA.md](../docs/discovery/G0_SCOPE_LOCK_CRITERIA.md)
- **Fragebogen:** 56 Fragen; **0 offen und Core Required**, 16 vertagt
  (Deployment Required), 1 offen ohne Core-Bezug (7.1 / OD-11) —
  [DISCOVERY_QUESTIONS.md](../docs/discovery/DISCOVERY_QUESTIONS.md)
- **Fehlende Information:** OI-02, OI-07 und OI-10 offen beziehungsweise
  teilweise aufgelöst —
  [OPEN_INFORMATION.md](../docs/discovery/OPEN_INFORMATION.md)

Der dominierende Rest ist **nicht mehr dokumentarisch, sondern technisch**:
**fünf** offene P0-Entscheidungen (OD-04, OD-07, OD-08, OD-11, OD-29) und
**null erbrachte technische Nachweise**. **OD-26 ist am 2026-07-21
geschlossen.**

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

## Lessons Learned aus CBP-WP-010

**Eine Gruppierung ist keine Berechtigung.** Die hybride Collection-Strategie
wäre ohne den Zusatz des Human Maintainers — dass die Collection nichts
verleiht — die riskanteste der drei Optionen gewesen. Bequeme Sortierordnungen
werden mit der Zeit zu impliziten Rechtequellen, wenn niemand das ausdrücklich
ausschließt.

**Ein Default, der „alles" bedeutet, ist ein Ausfall.** `allowed_subpaths: []`
nimmt **nichts** auf. Die naheliegende Lesart — leerer Filter gleich kein
Filter — ist der häufigste Weg zu unbeabsichtigtem Ingest und deshalb als
Beispiel 6 dokumentiert.

## Lessons Learned aus CBP-WP-009

**Eine zusammengesetzte offene Entscheidung schließt nicht durch eine Antwort.**
OD-26 sah wie eine Frage aus und waren zwei. Wäre nur Teil A entschieden worden,
hätte das Projekt eine Zielstruktur ohne Aussage darüber gehabt, wo private
Daten liegen — und umgekehrt. Die Trennung in Phase A hat das sichtbar gemacht.

## Lessons Learned aus CBP-WP-008

**Die Zählregel wirkt nachlaufend, nicht vorbeugend.** Der vierte Zählfehler
des Projekts entstand in CBP-WP-007 — **nachdem** die Regel eingeführt worden
war — und wurde erst ein Work Package später gefunden. Eine Dokumentregel macht
Fehler später sichtbar; sie verhindert sie nicht. R-33 bleibt deshalb offen.

**Zwei Dokumente können dieselben Bezeichner verschieden belegen.** Die
Layoutoptionen A/B/C aus CBP-WP-004 und ein zweiter, unabhängiger
Bereichsschnitt hätten in derselben Entscheidung kollidiert. Die
Arbeitsbereichsmodelle heißen deshalb **W-1/W-2/W-3**. OD-26 braucht beide
Antworten.

## Repository- und Bereichsgrenze — entschieden

**ADR-0007**, 2026-07-21, A0. Drei Bereiche mit verschiedenem Lebenszyklus:

| Bereich | Inhalt | Klasse | Sicherung |
| --- | --- | --- | --- |
| **Core Repository** | Code, Architektur, Governance, Tests, synthetische Fixtures, Deploymentvorlagen | **publication-capable by design** — nicht freigegeben | Git + Backup |
| **Privater Operator-Workspace** *(außerhalb)* | Konkrete Mappings, private Collections, **operatorbezogene kanonische Registry-Metadaten**, Verweise auf den Secret Store | **kanonisch** | **nur Backup** |
| **RT-1** Rebuildable Derived Data | Index, Embeddings, Cache, generierte Context Packs, Suchprojektionen | derived | **Rebuild** |
| **RT-2** Operational Evidence | Auditlogs, Approval- und Incident-Nachweise, Jobhistorie, Restore-Nachweise | **nicht reproduzierbar** | **Backup erforderlich** |
| **RT-3** Transient Runtime State | Temporäre Dateien, Locks, aktive Jobzustände, Puffer | flüchtig | **keine** — verwerfen |

**Das Core-Repository ist `publication-capable by design`, nicht
veröffentlicht.** Es bleibt privat; eine Veröffentlichung benötigt eine
separate **A0-Entscheidung** (OD-11).

**RT-2 ist kein Cache.** Auditnachweise sind nicht rekonstruierbar und brauchen
Aufbewahrung, Zugriffsschutz und Sicherung.

**Zielstruktur des Core-Repositorys:** `core/`, `adapters/`, `deployments/`,
`config/`, `docs/`, `examples/`, `tests/`.

**Nichts davon existiert.** Kein Verzeichnis angelegt, kein Workspace erzeugt,
keine Datei verschoben. Die Migration braucht ein eigenes, freigegebenes Work
Package und muss die Git-Historie erhalten.

## Mappingkonvention — entschieden

**ADR-0008**, 2026-07-21, A0. Drei Teilentscheidungen:

| Teil | Entscheidung | Grundsatz |
| --- | --- | --- |
| **A** (D-031) | YAML 1.2 Strict Subset, **JSON Schema als Vertragsgrenze** | **M-A** — was mehrdeutig geparst werden kann, ist unzulässig |
| **B** (D-032) | Fachliche Collection **plus** verpflichtender Slot | **M-B** — eine Collection verleiht nichts |
| **C** (D-033) | **Eine** Source Boundary je Mapping | **M-C** — was gemeinsam gemappt ist, wird gemeinsam widerrufen |

Verbindlich in
[PILOT_SOURCE_MAPPING_SPECIFICATION.md](../docs/sources/PILOT_SOURCE_MAPPING_SPECIFICATION.md):
31 Felder, 10 Zustände, 24 Validierungsregeln, 18 Negativtests, 20 Gate-Punkte.

**Nichts davon existiert.** Kein Mapping, keine angebundene Quelle, kein
Validator. Das
[Aktivierungsgate](../docs/operations/PILOT_MAPPING_ACTIVATION_GATE.md) steht
auf `NOT EVALUATED` und ist **ohne den F3-Strang nicht durchlaufbar** — acht
seiner zwanzig Punkte verlangen Nachweisstufe 4.

## Nächste Arbeitspakete

Siehe
[project-system/WORK_PACKAGE_QUEUE.md](../project-system/WORK_PACKAGE_QUEUE.md)
und [PHASE_1_WORK_PACKAGE_MAP.md](../docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md).

Vorgeschlagen, **nicht freigegeben**: **CBP-WP-011 — Technical Security
Foundation Specification** (`docs-only`, Full, B2 – Standard). CBP-WP-012 bis
CBP-WP-014 stehen ebenfalls auf `proposed`.

## Rückmeldung an Nova

CBP-WP-010 ist ausgeführt. **Die Mappingkonvention steht** — drei
A0-Entscheidungen, ADR-0008 `accepted`. **Es wurde kein Mapping erstellt, keine
Quelle angebunden und nichts aktiviert.**

**Drei Punkte zur Hervorhebung:**

1. **Grundsatz M-B ist die schärfste Folge.** Dass eine Collection weder
   Autorität noch Datenklasse noch AI-Transfer-Freigabe verleiht, verhindert
   dieselbe Fehlerklasse wie Slot-Regel 8: **die Sortierordnung darf nicht zur
   Rechtequelle werden.**
2. **Der Veröffentlichungsbegriff ist jetzt sichtbar geklärt.** ADR-0006 trägt
   einen datierten Klarstellungsnachtrag — *non-substantive clarification*, A1.
   Entscheidung und Status unverändert.
3. **Das Aktivierungsgate ist heute nicht durchlaufbar**, und das ist kein
   Mangel: Ohne durchgesetzte Dateirechte und Mount-Grenzen gibt es keinen
   Read-only-Nachweis. **Der F3-Strang ist der Engpass.**

**Kein Risiko wurde geschlossen.** Sämtliche Regeln sind dokumentarisch; alle
Nachweise stehen auf **Stufe 1 `dokumentiert`**.
