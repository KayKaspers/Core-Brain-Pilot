# Project Brain – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Überarbeitet in | **CBP-WP-016** |
| Autoritätsklasse | A2 |
| Stand | 2026-07-22 |

Kuratiertes Projektgedächtnis und Einstiegspunkt für jede neue Sitzung. Dieses
Dokument **verweist**, statt Inhalte zu duplizieren.

## Projektstatus

**Phase 0 – COMPLETE.** G0 am 2026-07-21 als **PASSED WITH NOTES** freigegeben (A0). Phase 1 ist **AUTHORIZED FOR PLANNING**.

Das Repository enthält Dokumentation, seit CBP-WP-012 einen **lokalen,
fail-closed Foundation Runtime Skeleton** und seit CBP-WP-013 einen **lokalen,
synthetisch testbaren Ingest-Quarantäneprototyp** (beide
Python-Standardbibliothek). **Keine operative Wirkung:** keine angebundene
Quelle, kein Index, kein Wissensbestand, keine durchgesetzte
Sicherheitskontrolle, keine Promotion. `run` und `quarantine release`
verweigern deterministisch.

| Feld | Wert |
| --- | --- |
| Aktuelles Work Package | **keines aktiv** — zuletzt abgeschlossen **CBP-WP-018** (`committed`: Phase B0 `4dec921`, Phase B1 `5ee2e83`); ADR-0013/D-052/D-053 |
| Gate G0 | **PASSED WITH NOTES** — 2026-07-21 |
| G0-Kriterien | **47**, dreistufig klassifiziert |
| davon blockierend | **25** Core Required (zuvor 45) |
| davon `accepted` | **25** — alle |
| verbleibende Blocker | **0** |
| Phase 1 | AUTHORIZED FOR PLANNING — [Backlog](../docs/roadmap/PHASE_1_BACKLOG.md), [Foundation Plan](../docs/roadmap/PHASE_1_FOUNDATION_PLAN.md) |
| Geplante Work Packages | **keine** — CBP-WP-018 ist `committed` (Phase B0 `4dec921`, Phase B1 `5ee2e83`, ADR-0013/D-052/D-053); **kein nächstes Work Package autorisiert oder vorgeschlagen** |
| **Repository-Struktur** | **entschieden** — Ziel-Monorepo + Workspace W-3 (ADR-0007); **Migration nicht autorisiert** |
| **Mappingkonvention** | **entschieden** — ADR-0008; **0 Mappings, 0 Quellen**, Gate `NOT EVALUATED` |
| **Sicherheitsgrundlage** | **spezifiziert** — ADR-0009; **12 Kontrollen `DOCUMENTED ONLY`** |
| **Runtime Skeleton** | **lokal implementiert** (CBP-WP-012) — `run` fail-closed, nicht produktionsbereit |
| **Ingest-Quarantäne MVP** | **lokaler Prototyp** (CBP-WP-013, ADR-0010) — synthetic-only, fail-closed, keine Promotion, nicht produktiv |
| **Source-Registry MVP** | **lokaler Prototyp** (CBP-WP-014, ADR-0011) — synthetic-only, fail-closed, **deaktiviert**, `activate` verweigert, nicht produktiv |
| **Source-Mapping-Draft-Validator MVP** | **lokaler Prototyp** (CBP-WP-015, ADR-0012) — synthetic-only, read-only, fail-closed, **31-Feld-Vertrag** (29+2), externe read-only Registry-Bindung, `mapping_id` nur validiert, `activation-check` verweigert, nicht produktiv |
| **Mapping-Activation-Gate-Evaluator MVP** | **lokaler Prototyp** (CBP-WP-016, D-050) — synthetic-only, read-only, nicht persistent, fail-closed; **20 Gate-Kriterien**, Ausgabestatus nur `NOT_EVALUATED`/`BLOCKED`; `activation-evaluate` endet immer `BLOCKED` (Exit 14); nicht produktiv |
| **Synthetic Evidence Contract 3.0 MVP** | **lokaler Prototyp** (CBP-WP-018, ADR-0013, D-052/D-053, `committed` `5ee2e83`) — Evidence-Schema 3.0 mit eingebetteten Artefakten, `security-control-form` + `control_id`, Provenance-/Binding-Hashes inkl. Security-Contract-Bindung, deterministische Invalid-/Stale-/Conflict-Erkennung, **negative-evidence-only**; Schema 1.0 **und 2.0** fail-closed; kein RT-2/Persistenz/Aktivierung; **558 Tests**, nicht produktiv |
| **Security Foundation Readiness Contract MVP** | **lokaler Prototyp** (CBP-WP-018, ADR-0013, D-053, `committed` `5ee2e83`) — statischer, reiner Vertrag 1.0 ohne I/O/Uhr/Zufall/Netz; **12 Controls / 7 runtime-scoped / 11 `(criterion, control_id)`-Bindungen**; nur synthetische Formprüfung, rein negativ; Kriterium 5 Human-only, Kriterium 9 non-security-structural; **keine** Security-Evaluation/Enforcement/Readiness; Readiness Gate `NOT EVALUATED`, nicht produktiv |
| Implementierte Capabilities | **keine (0 von 29)** — Bausteine belegt; Capability 5/6 bleiben `planned` |
| Nachweise oberhalb Stufe 1 | **keine** (lokale Bausteine, keine KB-Kontrolle) |
| Commits | **14** |

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

Angenommene ADRs: **13** (ADR-0001 bis ADR-0013; **ADR-0013** legt Evidence
Schema 3.0 mit Security-Control-Identität und Contract-Binding fest, D-052;
technisch umgesetzt unter **D-053**).
ADR-0006 hält privaten
Bestand konstruktiv außerhalb des Kern-Repositorys (D-028); **ADR-0007**
(D-029, D-030) legt Zielstruktur und Bereichsgrenze fest und **schließt
OD-26**; **ADR-0008** (D-031…D-033) legt die Mappingkonvention fest;
**ADR-0009** (D-034…D-037) die technische Sicherheitsgrundlage und **schließt
OD-34 und OD-35** (alle vier am 2026-07-21); **ADR-0010** (D-038…D-041) den
Ingest-Quarantäne-MVP und **ADR-0011** (D-042…D-045) den
Source-Registry-MVP (beide 2026-07-22); **ADR-0012** (D-046…D-049) den
Source-Mapping-Draft-Validator (2026-07-27), der **ADR-0008** präzisiert und
den 31-Feld-Vertrag unverändert lässt.

**45** getroffene Entscheidungen, davon **41** mit A0. **23** offene, davon
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

## Technische Sicherheitsgrundlage — spezifiziert

**ADR-0009**, 2026-07-21, A0. Vier Teilentscheidungen:

| Teil | Entscheidung | Grundsatz |
| --- | --- | --- |
| **A** (D-034) | Getrennte Identitäten: **Control Plane** und **Data Worker** | **S-A** — Verarbeitung erteilt keine Freigabe |
| **B** (D-035) | Versionierter Referenzvertrag `cbp-secret:v1:…`, OS-geschützter Datei-Provider | **S-B** — Eine Referenz ist kein Secret |
| **C** (D-036) | Egress **deny-by-default**, vierfach gebunden | **S-C** — Eine Netzwerkerlaubnis ist keine Datenfreigabe |
| **D** (D-037) | RT-2 **append-only und verkettet** | **S-D** — Ein überschreibbarer Nachweis ist kein Nachweis |

**Zwölf Kontrollbereiche** KB-01…KB-12, **neunstufige Durchsetzungsreihenfolge**
(Promptregeln nur auf Stufe 9), **32 Negativtests plus 1 Positivtest**, **16 Stop-Bedingungen**,
Readiness Gate mit **24 Punkten**.

**Nichts davon existiert.** Alle zwölf stehen auf **DOCUMENTED ONLY**, kein
Test wurde ausgeführt. **OD-34 und OD-35 sind geschlossen** — die konkrete
RT-2-Aufbewahrungsdauer bleibt **Deployment Required**.

## Runtime Skeleton — lokal implementiert

**CBP-WP-012**, 2026-07-21, erste technische Umsetzung. Human-Autorisierung
APPROVE WITH NOTES (A0), Stack A1 (Python 3.13, Standardbibliothek), CLI B1,
additive Struktur C1.

| Gegenstand | Wert |
| --- | --- |
| Runtime-Module | 9 unter `core/core_brain/` |
| CLI | `version`, `validate-config`, `doctor`, `run` |
| Ports | 4, alle **verweigernd** |
| Tests | **69 bestanden**, 0 fehlgeschlagen (67 + 2 Netzwerk-Guard) |
| Python | 3.13.14, keine Abhängigkeiten |
| `run` | verweigert (Exit 4) |

**Keine KB-Kontrolle durchgesetzt.** Der Doctor meldet `PASS`/`NOT APPLICABLE`
als **Skeleton-Ergebnisse**, kein Deploymentnachweis. Alle drei Gates bleiben
`NOT EVALUATED`.

## Lessons Learned aus CBP-WP-012

**Ein grüner Testlauf ist erst nach der Auszählung glaubwürdig.** Der erste
Lauf fand zwei Fehler — beide in den Tests, nicht im Code: `mock.patch` ohne
`create=True` scheitert auf Windows, und ein Grep traf Prosa im Docstring statt
echter Nutzung. Die berichtete Zahl (67 im Erstlauf, 69 nach dem im
Nova-REWORK ergänzten Netzwerk-Guard) stammt jeweils aus dem grünen Lauf, nicht
aus einer Annahme (R-33).

**Ein `PASS` braucht eine Grenze.** Der Doctor meldet Erfolg für Skeleton-
Prüfungen; ohne den ausdrücklichen Zusatz „kein Deploymentnachweis" wäre daraus
schnell „Sicherheitsgrundlage implementiert" geworden — dieselbe Übererweiterung
wie „veröffentlichbar" in CBP-WP-009 und „gültig" in CBP-WP-010.

## Ingest-Quarantäne MVP — lokal implementiert

**CBP-WP-013**, 2026-07-22, zweite technische Umsetzung. Human-Autorisierung
APPROVE WITH NOTES (A0), A1/B1/C1/D1; **A0-Modellsubstitution** auf Opus 4.8
(Fable 5 nicht verfügbar). Festgehalten in **ADR-0010** (D-038…D-041).

| Gegenstand | Wert |
| --- | --- |
| Quarantäne-Module | 6 unter `core/core_brain/quarantine/` |
| CLI | `quarantine scan`, `stage`, `inspect`, `release` |
| Zustände | `READY_FOR_HUMAN_REVIEW`, `REVIEW_REQUIRED`, `BLOCKED` |
| Exitcodes | 0 / 5 / 6 / 7 |
| Store | content-addressed, außerhalb Repo, atomar, idempotent |
| Tests | **137 bestanden** (Basislinie 69), 0 fehlgeschlagen |
| `release` | verweigert immer (Exit 7) |

**Synthetic-only-Grenze technisch durchgesetzt** (Flag + `synthetic:`-Präfix +
Marker). **Keine reale Quelle, kein Mapping, keine Promotion, keine
Indexierung.** Scanner ist ein **Indikator**, keine vollständige Secret-/PII-
Erkennung. **R-01, R-32, R-33 bleiben offen**; Capability 5/6 bleiben `planned`.

## Source-Registry MVP — lokal implementiert

**CBP-WP-014**, 2026-07-22, dritte technische Umsetzung. Human-Autorisierung
APPROVE WITH NOTES (A0), A1/B1/C1/D1. Festgehalten in **ADR-0011** (D-042…D-045).

| Gegenstand | Wert |
| --- | --- |
| Registry-Module | 6 unter `core/core_brain/registry/` |
| CLI | `source-registry validate-definition`, `register`, `list`, `inspect`, `retire`, `activate` |
| Zustände | `REGISTERED_DISABLED`, `RETIRED` |
| Exitcodes | 8 / 9 / 10 / 11 (neu) |
| Speicher | unveränderliche Records, append-only Events, atomarer Katalog, außerhalb Repo |
| Tests | **212 bestanden** (Basislinie 137), 0 fehlgeschlagen |
| `activate` | verweigert immer (Exit 11) |

**Synthetic-only-Grenze technisch durchgesetzt.** Source ID deterministisch aus
Namespace und Source Key; Records und Katalog **ohne** Pfad, URL, Inhalt oder
Mapping-Locator. **Keine reale Quelle, kein Mapping, keine Aktivierung, keine
Indexierung.** **R-33 bleibt offen**; Capability 2/3/7 bleiben nicht vollständig
`implemented`.

## Source-Mapping-Draft-Validator MVP — lokal implementiert

**CBP-WP-015**, 2026-07-27, vierte technische Umsetzung. Human-Autorisierung
APPROVE WITH NOTES (A0), A1/B1/C1/D1. Festgehalten in **ADR-0012** (D-046…D-049).
Ein Reconciliation-Lauf klärte zuvor den **19/31-Blocker**: der angenommene
Vertrag hat **31 Felddefinitionen**, nicht 19.

| Gegenstand | Wert |
| --- | --- |
| Mapping-Module | 6 unter `core/core_brain/mapping/` |
| CLI | `source-mapping validate-draft`, `activation-check` |
| Vertrag | **31 Felddefinitionen** (29 Pflicht + 2 optional), unverändert |
| Dokumentprofil | kanonisches JSON (MVP), BOM/Duplikate/`NaN`/`Infinity` fail-closed |
| Registry-Bindung | extern, **read-only**; nur `collection`/`data_class` exakt |
| `mapping_id` | nur validiert (V4/V21), **nie berechnet** |
| Report | nicht persistiert, deterministisch, minimiert |
| Exitcodes | 12 / 13 (neu) |
| Tests | **315 bestanden** (Basislinie 212), 0 fehlgeschlagen |
| `activation-check` | verweigert immer (Exit 13) |

**Synthetic-only- und read-only-Grenze technisch durchgesetzt.** Kein realer
Pfad, keine URL, kein Source-Inhalt, keine `source_reference` im Report; die
Registry bleibt bytegenau unverändert. **Kein Mapping gespeichert, keine
Aktivierung, keine verbotenen Crosswalks** (`project`↔`domain`,
`ai_transfer`↔`ai_eligibility`). **R-33 bleibt offen** (neunter
Konsistenzvorgang, 19/31-Korrektur); die Bildungsvorschrift von `mapping_id`
bleibt offen; Capability 2/7 bleiben nicht vollständig `implemented`.

## Nächste Arbeitspakete

Siehe
[project-system/WORK_PACKAGE_QUEUE.md](../project-system/WORK_PACKAGE_QUEUE.md)
und [PHASE_1_WORK_PACKAGE_MAP.md](../docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md).

**CBP-WP-016 — Deterministic Mapping Activation Gate Evaluator** ist unter der
A0-Freigabe **D-050** (APPROVE WITH NOTES, A1/B1-eng/C1/D1) implementiert und
**committed** (`04c427c`). **CBP-WP-017 — Synthetic Evidence Contract &
Provenance Foundation** ist unter **D-051** (APPROVE WITH NOTES, A2/B1/C2/D1/E2)
implementiert und **committed** (`d3168c4`). **CBP-WP-018 — Security Foundation
Readiness Contract & Synthetic Form-Validator** ist **`committed`**: **ADR-0013**
(Evidence Schema 3.0) angenommen, **D-052** (Governance Foundation, `committed`
`4dec921`) und **D-053** (Technical Implementation, `committed` `5ee2e83`)
dokumentiert; der Runtime-Stand ist damit **Evidence Schema 3.0** mit statischem
**Security Contract 1.0** (12 Controls, 7 runtime-scoped, 11 Bindungen),
**558 Tests – OK**. **Kein Work Package ist aktiv**; zuletzt abgeschlossen ist
**CBP-WP-018**. Ein weiteres Work Package ist **nicht** vorgeschlagen und
**nicht autorisiert**; CBP-WP-019 ist nicht registriert, nicht begonnen und
nicht autorisiert. Alle drei Gates bleiben `NOT EVALUATED`.

## Rückmeldung an Nova

CBP-WP-012 ist ausgeführt — **das erste Artefakt mit technischer Wirkung**. Ein
lokaler, fail-closed Runtime Skeleton, 69 Tests bestanden, `run` verweigert.
**Es wurde nichts angebunden, nichts aufgelöst, nichts verbunden und nichts
gestartet.**

**Drei Punkte zur Hervorhebung:**

1. **Ein `PASS` im Doctor ist kein Deploymentnachweis.** Keine der sechs
   `PASS`-Zeilen belegt eine durchgesetzte KB-Kontrolle. Sie bleiben
   `DOCUMENTED ONLY`; der reale Nachweis entsteht auf der Ziel-VM.
2. **`run` verweigert strukturell.** Selbst mit beiden Gate-Status auf
   `ACCEPTED` startet keine Runtime — ein Test belegt das. Der Skeleton *kann*
   nicht produktiv laufen.
3. **Zwei Testdefekte, keine Codedefekte.** Die Testzahl (67 → 69) stammt aus dem
   grünen Lauf nach der Korrektur.

**Kein Risiko wurde geschlossen.** R-25, R-26, R-27, R-30, R-31, R-32 und R-20
bleiben offen — ein Skeleton ist keine durchgesetzte Kontrolle.
