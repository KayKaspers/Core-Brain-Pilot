# CBP-WP-003 — Human Discovery Intake and G0 Evidence Capture

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-003 |
| Titel | Human Discovery Intake and G0 Evidence Capture |
| Typ | `docs-only` |
| Prompt Mode | **Full** (NDF v1.0.0) |
| Context Budget | **B1 – Lean** (Core Brain Pilot) |
| Phase | Phase 0 – Discovery und Scope Lock |
| Ausgeführt am | 2026-07-20 |
| Status | `in-review` |
| Autoritätsklasse | A2 |

Interaktives Work Package in zwei Phasen. Phase A wurde nach Nova-Review
einmal überarbeitet.

---

## Ziel

Die für G0 erforderlichen Informationen gebündelt beim Human Maintainer erheben
und in prüfbare Projektnachweise überführen.

## Scope

- Repository und Discovery-Dokumente read-only prüfen
- Einen einzigen gebündelten Fragebogen ausgeben
- Nur tatsächlich gegebene Antworten dokumentieren
- Antworten den P0-Fragen und G0-Kriterien zuordnen
- G0-Kriterien dreistufig klassifizieren
- Fehlerhafte Summen korrigieren
- Register nachführen

## Out of Scope

- G0 als bestanden erklären
- Fehlende Antworten erfinden oder plausibilisieren
- Benchmarkfragen erfinden
- Architekturdesign implementieren
- Scope Lock automatisch aussprechen
- Commit oder Push

## Erlaubte Dateien

**Erstellen:** `docs/discovery/HUMAN_DISCOVERY_INPUT.md`,
`work-packages/CBP-WP-003.md`

**Ändern, soweit durch Antworten erforderlich:** die Dokumente unter
`docs/discovery/`, `project-system/`, `project-brain/PROJECT_BRAIN.md`,
`README.md`.

Ausschließlich Markdown-Dateien innerhalb von `D:\Projects\Core-Brain-Pilot`.

## Verbotene Dateien

Dateien außerhalb des Projektordners, Anwendungscode, Dockerfile,
`compose.yaml`, Skripte, CI/CD, GitHub Actions, Datenbanken, Suchindex,
Embeddings, Modelle, Wiki-Ingest, Graph, MCP, Softwareinstallation,
Infrastrukturänderungen, Secrets, Zugangsdaten, `LICENSE`, Branch-Erstellung,
Remote-Änderungen, Commit, Push, GitHub-Issues, Releases.

## Inputs

1. Nova Development Framework v1.0.0
2. Repository-Stand auf `main` (Commit `18fda97`)
3. `docs/discovery/G0_SCOPE_LOCK_CRITERIA.md`
4. `docs/discovery/DISCOVERY_QUESTIONS.md`
5. `docs/discovery/OPEN_INFORMATION.md`
6. `docs/architecture/CONTEXT_BUDGETS.md`
7. `project-system/DECISION_REGISTER.md`
8. `project-system/RISK_REGISTER.md`
9. `project-system/PROJECT_MANIFEST.md`
10. `project-brain/PROJECT_BRAIN.md`
11. **Antworten des Human Maintainers** — Minimal Human Discovery Questionnaire

## Aufgaben

**Phase A:** Repository read-only prüfen, gebündelten Fragebogen ausgeben, auf
Antworten warten. Keine Dateiänderung.

**Phase B:** Antworten dokumentieren, klassifizieren, G0-Kriterien dreistufig
einordnen, Summen korrigieren, Blocker neu berechnen, Register nachführen,
genau ein Folge-Work-Package vorschlagen.

## Tests

Zwanzig Prüfungen. Schwerpunkte: alle dokumentierten Antworten stammen
tatsächlich vom Human Maintainer; keine unbeantwortete Frage ergänzt; keine
Antwort inhaltlich erweitert; `accepted` nur bei ausdrücklicher Entscheidung;
Infrastrukturangaben nicht pauschal als A0; G0 bleibt NOT PASSED; offene
P0-Fragen bleiben sichtbar; kein Commit, kein Push.

## Akzeptanzkriterien

Der Fragebogen deckt alle P0-Fragen ab, der Human Maintainer hat geantwortet,
die Antworten sind normalisiert dokumentiert, Antworten und Entscheidungen sind
sauber getrennt, betroffene G0-Kriterien sind aktualisiert, verbleibende Lücken
sind sichtbar, keine Information wurde erfunden, keine Secrets gespeichert, G0
wurde nicht automatisch bestanden, alle Prüfungen sind bestanden.

---

## Ausführungsverlauf

| Phase | Ergebnis |
| --- | --- |
| Vorprüfung | Alle zehn Punkte erfüllt. Arbeitsbaum sauber, 3 Commits, CBP-WP-002 committed (`18fda97`), G0 NOT PASSED |
| Phase A, Fassung 1 | **REWORK durch Nova.** 15 Fragen, zu stark auf eine konkrete Proxmox-Installation zugeschnitten; vermischte Produktentscheidungen, Deploymentdaten und funktionsabhängige Angaben |
| Phase A, Fassung 2 | Sechs kombinierte Fragen auf Profilebene. Keine Infrastrukturwerte, keine Netzwerkdetails, keine Rechtsgrundlage ohne PII-Bezug |
| Phase B | Sechs Antworten ausgewertet, 12 A0-Entscheidungen erfasst, G0-Kriterien dreistufig klassifiziert, Summen korrigiert |

### Befund aus der Vorprüfung: fehlerhafte Kennzahlen

Beim Auszählen der Grundlagen zeigte sich, dass die in CBP-WP-002 berichteten
Summen falsch addiert waren. Die Dokumente selbst waren vollständig und
korrekt; nur die Summenzeilen und der Report stimmten nicht.

| Kennzahl | Falsch berichtet | Korrekt |
| --- | --- | --- |
| G0-Kriterien gesamt | 41 | **47** |
| Blockierend, bisheriges Modell | 39 | **45** |
| P0-Fragen | 35 | **38** |
| Fragen gesamt | 55 | **56** |

Korrigiert in CBP-WP-003, erfasst als Risiko R-33.

### Architekturkorrektur durch Nova

Das dreistufige Kriterienmodell (Core Required, Deployment Required,
Conditional) wurde durch das Nova-Review eingeführt und als **D-026**
dokumentiert. Es reduziert die G0-Blocker von 45 auf **25**, ohne ein Kriterium
zu streichen: die 16 Deployment-Required-Kriterien werden einem späteren
Deployment-Readiness-Gate zugeordnet, die 6 Conditional-Kriterien blockieren
nur bei aktivierter Funktion.

Ein neuer Gate-Name wurde bewusst **nicht** eingeführt.

---

## Rückmeldung an Nova

Der Intake hat den Pilotumfang auf Profilebene festgelegt: Proxmox-VM mit
dedizierter Linux-VM, Docker Compose als bevorzugte Laufzeit darin,
Single-User, Markdown-orientierte Quellen, `public`/`internal` als
Pilotdatenklassen, privates Netz ohne öffentliche Freigabe, Web-UI und mobile
Nutzung im Pilot — die Web-UI erst nach funktionierendem Retrieval.

**Zwölf A0-Entscheidungen** (D-015 bis D-026) sind erfasst. Acht
Core-Required-Kriterien stehen auf `accepted`, vier auf `answered`, dreizehn
sind `open`.

**Bemerkenswert:** Die Antwort zu `excluded-from-ai` ist **strenger** als das
bisherige Fundament — die Klasse soll von Anfang an im Modell geführt und ihre
Sperrwirkung mit Testdaten nachgewiesen werden. Das macht aus dem bisher
abstrakten Risiko R-30 eine prüfbare Anforderung und erzeugt R-31.

**Ein Konflikt wurde durch A0 aufgelöst:** Der Human Maintainer bestätigt
Docker Compose als „bevorzugte" Laufzeit. In CBP-WP-002 hatte ich das gestützt
auf Projektübergabe §4 (A5) abgeschwächt. A0 schlägt A5 — die Abschwächung ist
aufgehoben. `PROJECT_DEFINITION.md` war in diesem Work Package nicht änderbar;
die Nachführung ist als OD-31 erfasst.

**G0 bleibt NOT PASSED.** 17 der 25 Core-Required-Kriterien sind noch nicht
`accepted`. Der größte zusammenhängende Block sind die sechs
Benchmark-Kriterien, gefolgt von vier Berechtigungskriterien (E-2 bis E-5) und
dem Secret-Verfahren (D-8).
