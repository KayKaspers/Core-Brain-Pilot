# CBP-WP-006 — G0 Scope-Lock Review and Pilot Source Contract

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-006 |
| Titel | G0 Scope-Lock Review and Pilot Source Contract |
| Typ | `docs-only` |
| Prompt Mode | **Full** (NDF v1.0.0) |
| Context Budget | **B1 – Lean** (Core Brain Pilot) |
| Phase | Phase 0 – Discovery und Scope Lock |
| Ausgeführt am | 2026-07-21 |
| Status | `in-review` |
| Autoritätsklasse | A2 |

---

## Ziel

Die dokumentarische Vorbereitung von Phase 0 abschließen: Pilot Source
Contract, logisches Source-Slot-Modell, vollständige G0-Evidenzmatrix und eine
entscheidungsreife G0-Review-Unterlage.

Der Pilot Source Contract präzisiert **D-1** auf der allgemeinen Produkt- und
Pilot-Scope-Ebene. Konkrete Windows-, Linux-, Mount-, Repository- oder
Netzwerkpfade gehören **nicht** in G0.

**Keine Quellen einbinden. Keine Suche implementieren. Keinen Benchmark
ausführen. Kein Deployment beginnen.**

## Scope

- Pilot Source Contract mit logischen Source Slots
- Deployment-neutrales Source-Slot-Schema mit Validierungsregeln
- ADR-0006 als **Vorschlag** zur Source-Boundary-Entscheidung
- Nachweisbasierte Bewertung von D-1
- G0-Evidenzmatrix über alle 25 Core-Required-Kriterien
- Entscheidungsreife G0-Review-Unterlage mit leerem Entscheidungsblock
- Statusnachführung in den Registern

## Out of Scope

- G0 als bestanden erklären
- ADR-0006 als `accepted` markieren
- OD-05, OD-06 oder OD-26 schließen
- Quellen anbinden, Deployment Mappings festlegen
- Suche, Index, Embeddings, Retrieval implementieren
- Benchmark ausführen, DRC ausführen
- Konkrete private Pfade oder Repository-URLs
- Commit, Push, Branch, Remote-Änderung

## Inputs

NDF v1.0.0 · Repository-Stand auf `main` (Commit `70132b3`) ·
`G0_SCOPE_LOCK_CRITERIA.md` · `HUMAN_DISCOVERY_INPUT.md` ·
`SOURCE_RECONCILIATION.md` · `SYSTEM_ARCHITECTURE.md` · `COMPONENT_MODEL.md` ·
`DEPLOYMENT_PROFILES.md` · `REPOSITORY_LAYOUT_OPTIONS.md` ·
`CONTEXT_BUDGETS.md` · `DATA_CLASSIFICATION.md` · `PERMISSION_MODEL.md` ·
`SECRET_INCIDENT_RESPONSE.md` · `DEPLOYMENT_READINESS_CHECK.md` · die fünf
Dokumente unter `docs/benchmark/` · `benchmarks/README.md` ·
`PROJECT_MANIFEST.md` · `DECISION_REGISTER.md` · `RISK_REGISTER.md` ·
`WORK_PACKAGE_QUEUE.md` · `CAPABILITY_MATRIX.md` · `PROJECT_BRAIN.md` ·
`CBP-WP-005.md`

Keine externe Recherche.

## Erlaubte Dateien

**Erstellen:** `docs/sources/PILOT_SOURCE_CONTRACT.md` ·
`docs/sources/SOURCE_SLOT_MODEL.md` ·
`docs/decisions/ADR-0006-logische-source-slots.md` ·
`docs/discovery/G0_EVIDENCE_MATRIX.md` ·
`docs/discovery/G0_SCOPE_LOCK_REVIEW.md` · `work-packages/CBP-WP-006.md`

**Ändern:** `README.md` · `G0_SCOPE_LOCK_CRITERIA.md` · `OPEN_INFORMATION.md` ·
`docs/decisions/README.md` · `PROJECT_BRAIN.md` · die Dokumente unter
`project-system/`

## Verbotene Dateien

Konkrete private Produktivpfade · echte Repository-Zugangsdaten · private
Repository-URLs als allgemeine Vorgabe · reale Wissensquellen · Dateien
außerhalb des Projektordners · Anwendungscode · Dockerfile · `compose.yaml` ·
Skripte · CI/CD · Datenbanken · Suchindex · Embeddings · Modelle ·
Search-Provider-Auswahl · qmd-Installation · Retrieval-Implementierung ·
Benchmarkausführung · produktiver Ingest · Wiki-Ingest · Knowledge Graph ·
MCP- oder Web-UI-Implementierung · Infrastrukturänderung · DRC-Ausführung ·
G0 eigenständig als PASSED · ADR-0006 eigenständig als accepted ·
Repository-Reorganisation · `LICENSE` · Branch · Remote-Änderung · Commit ·
Push · GitHub-Issue · Release

## Aufgaben

1. Pilot Source Contract
2. Source-Slot-Modell
3. Source-Boundary-Entscheidung (ADR-0006, `proposed`)
4. D-1-Nachweis
5. G0-Evidenzmatrix
6. G0-Scope-Lock-Review
7. G0-Status
8. Register und Status

## Prüfungen

28 Prüfungen. Schwerpunkte: mindestens fünf aktive oder Test-Slots · PDF/Office
und Connectoren `deferred` · kein realer privater Pfad · jeder Slot mit Owner,
Datenklasse, AI-Transfer-Regel und Löschmodell · `excluded-from-ai`
fail-closed · Benchmark-A0 ohne reale Projektgeltung · Deployment Mapping
separat · D-1 vollständig belegt · alle 25 Core-Kriterien in der Matrix · keine
unbelegte `accepted`-Markierung · dokumentarische Erfüllung nicht als
technische Implementierung dargestellt · DRC bleibt NOT EVALUATED · G0 bleibt
NOT PASSED · Entscheidungsblock leer · ADR-0006 `proposed` · OD-05, OD-06,
OD-26 offen · kein Commit, kein Push.

## Akzeptanzkriterien

Pilot Source Contract vorhanden · deployment-neutrales Slot-Modell vorhanden ·
D-1 nachweisbasiert bewertet · alle 25 Core-Kriterien in einer Evidenzmatrix ·
entscheidungsreife G0-Unterlage · Criteria Readiness und Gate Approval klar
getrennt · G0 nicht eigenmächtig freigegeben · DRC nicht ausgeführt · keine
Quelle angebunden · keine Implementierung begonnen · alle Prüfungen bestanden.

---

## Ergebnis

| Artefakt | Umfang |
| --- | --- |
| Pilot Source Contract | 7 logische Source Slots — 4 `active`, 1 `test-only`, 2 `deferred` |
| Source-Slot-Modell | 24 Felder, 10 Validierungsregeln, 2 Schema-Beispiele |
| ADR-0006 | **`proposed`** — Trennung von Kern und privatem Bestand |
| G0-Evidenzmatrix | 25 Kriterien, 5 Matrixprüfungen, Summenzeile |
| G0-Review | 19 Abschnitte, 5 Entscheidungsoptionen, **leerer** Entscheidungsblock |
| D-1 | `answered` → **`accepted`** |
| Core-Kriterien | **25 accepted, 0 answered, 0 open** |
| Gate-Status | **NOT PASSED** — READY FOR HUMAN DECISION |

## Rückmeldung an Nova

**Der letzte Core-Blocker ist aufgelöst.** D-1 steht auf `accepted`, gestützt
auf den Pilot Source Contract, das Slot-Modell und ADR-0006. Alle 25
Core-Required-Kriterien sind nachweisbasiert belegt; 18 davon durch eine
ausdrückliche A0-Entscheidung.

**Die entscheidende Trennung** liegt in ADR-0006: der allgemeine Kern enthält
keinen privaten Wissensbestand. Quellen werden über logische Slots definiert
und erst im Deployment Mapping konkret zugeordnet. Damit ließ sich D-1
schließen, **ohne** OD-05, OD-06 oder OD-11 vorwegzunehmen — alle drei bleiben
offen.

**Vier Punkte, die ich hervorhebe:**

1. **D-1 `accepted` heißt nicht, dass eine Quelle angebunden ist.** Es heißt,
   dass der zulässige Quellenraum definiert und begrenzt ist. Ich habe das in
   Kriterium, Matrix und Review dreifach vermerkt, weil genau diese
   Verwechslung naheliegt.

2. **Sechzehn der 25 Kriterien beschreiben Kontrollen, die nicht existieren.**
   Die Evidenzmatrix führt eine eigene Spalte dafür. Für einen Scope Lock ist
   das korrekt — G0 sperrt den Scope, nicht die Implementierung — aber es darf
   nicht als Reife gelesen werden.

3. **Der Entscheidungsblock ist leer und bleibt es.** Ich habe eine Empfehlung
   abgegeben (APPROVE G0 WITH NOTES, mit drei Auflagen), keine Freigabe. G0
   steht formal weiterhin auf **NOT PASSED**.

4. **ADR-0006 ist `proposed`.** Die Source-Boundary-Entscheidung ist die
   folgenreichste dieses Work Packages — sie legt fest, dass privater Bestand
   nie in das Kern-Repository gerät. Sie braucht einen eigenen Beschluss und
   sollte nicht im G0-Beschluss untergehen.

**Criteria complete ≠ Gate approved.** Die Unterlage ist entscheidungsreif; die
Entscheidung steht aus.
