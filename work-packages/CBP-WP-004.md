# CBP-WP-004 — Generic Architecture and Deployment Profiles

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-004 |
| Titel | Generic Architecture and Deployment Profiles |
| Typ | `docs-only` |
| Prompt Mode | **Full** (NDF v1.0.0) |
| Context Budget | **B2 – Standard** (Core Brain Pilot) |
| Phase | Phase 0 – Discovery und Scope Lock |
| Ausgeführt am | 2026-07-20 |
| Status | `in-review` |
| Autoritätsklasse | A2 |

---

## Ziel

Die allgemeine, deployment-neutrale Zielarchitektur von Core Brain Pilot
definieren und dabei sechs Dinge klar trennen: deployment-unabhängige
Core-Funktionen, austauschbare technische Adapter, Deploymentprofile,
Deployment-Readiness, Berechtigungs- und Freigaberegeln sowie
Secret-Incident-Response.

Die Architektur soll so weit präzisiert sein, dass anschließend ein
reproduzierbarer Benchmark- und Retrieval-Pilot geplant werden kann.

**Noch keine Anwendung implementieren.**

## Scope

- Logische Systemarchitektur in Schichten
- Logische Komponenten mit Vertrauensgrenzen und Schreibrechten
- Fünf Deploymentprofile A bis E
- Deployment Readiness Check für die 16 Deployment-Required-Kriterien
- Berechtigungsmodell mit Rollen-/Ressourcenmatrix
- Secret-Incident-Response-Prozess
- Canonical-/Derived-Trennung mit Rebuild-Vertrag
- Nicht-Ziele auf G0-Kriterium A-8 mappen
- Kennzahlkorrekturen und historische Korrekturhinweise
- Repository-Layout-Optionen als Entscheidungsvorlage
- ADRs nach bestehender Konvention
- G0-Nachführung

## Out of Scope

- G0 als bestanden erklären
- Benchmarkfragen erfinden
- Anwendungscode, Compose-Datei, Container, Web-UI, MCP
- Softwareinstallation, Infrastrukturänderung, Bewertung realer Infrastruktur
- Repository-Reorganisation, Verschieben von Dateien
- Commit, Push, Branch, Remote-Änderung
- Breite Internet- oder GitHub-Recherche

## Inputs

NDF v1.0.0 · Repository-Stand auf `main` (Commit `b1a6c2f`) ·
`PROJECT_DEFINITION.md` · `ARCHITECTURE_PRINCIPLES.md` · `TRUST_BOUNDARIES.md` ·
`CONTEXT_BUDGETS.md` · `G0_SCOPE_LOCK_CRITERIA.md` · `HUMAN_DISCOVERY_INPUT.md` ·
`SOURCE_RECONCILIATION.md` · `DATA_CLASSIFICATION.md` · `DO_NOT_START.md` ·
`PROJECT_MANIFEST.md` · `DECISION_REGISTER.md` · `RISK_REGISTER.md` ·
`CAPABILITY_MATRIX.md` · `WORK_PACKAGE_QUEUE.md` · `PROJECT_BRAIN.md` ·
`CBP-WP-002.md` · `CBP-WP-003.md`

Die Architektur wurde ausschließlich aus diesen freigegebenen Projektquellen
und Entscheidungen abgeleitet. Keine externe Recherche.

## Erlaubte Dateien

**Erstellen:** `SYSTEM_ARCHITECTURE.md` · `COMPONENT_MODEL.md` ·
`DEPLOYMENT_PROFILES.md` · `REPOSITORY_LAYOUT_OPTIONS.md` ·
`DEPLOYMENT_READINESS_CHECK.md` · `PERMISSION_MODEL.md` ·
`SECRET_INCIDENT_RESPONSE.md` · ADRs nach bestehender Konvention ·
`work-packages/CBP-WP-004.md`

**Ändern:** README, CLAUDE.md, die Dokumente unter `docs/architecture/`,
`docs/decisions/`, `docs/discovery/`, `docs/ndf/`, `docs/privacy/`,
`docs/product/`, `project-brain/`, `project-system/` sowie `CBP-WP-002.md` und
`CBP-WP-003.md`.

## Verbotene Dateien

Dateien außerhalb des Projektordners · Anwendungscode · Dockerfile ·
`compose.yaml` · Containerstart · Skripte · CI/CD · GitHub Actions ·
Datenbanken · Suchindex · Embeddings · Modelle · produktiver Ingest ·
Wiki-Ingest · Graph · MCP-Implementierung · Web-UI-Implementierung ·
Softwareinstallation · Infrastrukturänderung · echte Secrets oder
Credential-Beispiele · `LICENSE` · Branch-Erstellung · Remote-Änderung ·
Commit · Push · GitHub-Issue · Release · Repository-Reorganisation

## Aufgaben

1. Allgemeine Systemarchitektur in 9 Schichten
2. Komponenten und Vertrauensgrenzen, 14 logische Komponenten
3. Fünf Deploymentprofile A bis E
4. Deployment Readiness Check (DRC)
5. Berechtigungsmodell
6. Secret-Incident-Response
7. Canonical-/Derived-Präzisierung mit Rebuild-Vertrag
8. Nicht-Ziele auf A-8 mappen
9. Korrekturen und Nachführungen
10. Repository-Layout-Entscheidung vorbereiten

Ergänzend: ADRs, G0-Nachführung, Work-Package-Queue, Work-Package-Dokument.

## Prüfungen

Dreißig Prüfungen. Schwerpunkte: Architektur ohne Proxmox funktionsfähig
beschrieben · keine Proxmox-API-Abhängigkeit · Canonical und Derived getrennt ·
nur ein autorisierter Schreibpfad · alle fünf Aktionsklassen und
Durchsetzungsebenen · `excluded-from-ai` fail-closed · Rotation vor History
Cleanup · Derived nach Secret-Vorfall gelöscht und neu aufgebaut · DRC mappt
alle 16 Kriterien und steht auf NOT EVALUATED · Kennzahlen 47/25/16/6 ·
historische Zahlen mit sichtbarer Korrektur-Notiz · G0 bleibt NOT PASSED ·
Benchmark G-1 bis G-6 offen · keine Capability `implemented` · keine
Compose-Datei · keine Datei verschoben · kein Commit, kein Push.

## Akzeptanzkriterien

Deployment-neutrale Systemarchitektur liegt vor · logische Komponenten und
Vertrauensgrenzen dokumentiert · alle fünf Profile beschrieben · DRC übernimmt
alle Deployment-Required-Kriterien · Berechtigungsmodell vollständig · 
Secret-Incident-Response vorhanden · Canonical-/Derived-Trennung mit
Rebuild-Vertrag · Kennzahlen korrigiert · historische Korrekturen
nachvollziehbar · G0-Nachweise aktualisiert · G0 nicht vorzeitig bestanden ·
keine Implementierung begonnen · alle Prüfungen bestanden.

---

## Rückmeldung an Nova

Die Architektur steht als logisches Modell: neun Schichten, vierzehn
Komponenten, fünf Profile. Der Kern ist ohne Proxmox vollständig beschreibbar —
Profil B ist der laufende Neutralitätsnachweis.

**Die tragende Regel** ist in COMPONENT_MODEL als Tabelle ausgeführt: von
vierzehn Komponenten darf **eine** kanonische Inhalte verändern — der Review-
und Approval-Workflow, nach menschlicher Entscheidung. Suchdienst, Web-UI,
Indexer und Agenten sind konstruktiv ausgeschlossen.

**Fortschritt an G0:** `accepted` von 8 auf **18**, verbleibende Blocker von 17
auf **7**. Zehn Kriterien neu belegt: A-1, A-2, D-3 aus dem Intake, A-8 über
die Nicht-Ziel-Liste, D-8 über die Secret-Incident-Response, E-2 bis E-5 über
das Berechtigungsmodell, F-3 über ADR-0003.

**Sechs der sieben verbleibenden Blocker sind der Benchmarkblock.** Er ist der
letzte große geschlossene Bereich vor G0 — daher der Vorschlag CBP-WP-005.

**Zwei Einschränkungen, die ich nicht wegformuliere:**

1. Bei D-8 und E-2 bis E-5 ist die **dokumentarische** Anforderung erfüllt, die
   technische Durchsetzung existiert nicht. R-25 und R-27 bleiben deshalb
   ausdrücklich `offen`, nicht `gemindert`. Ein Berechtigungsmodell auf Papier
   ist keine Zugriffskontrolle.
2. **D-1 wurde bewusst nicht auf `accepted` gehoben.** Der Intake liefert
   Quellen*arten*, das Kriterium verlangt Pfade oder Systeme. Es bleibt
   `answered`, bis OD-05 und OD-06 entschieden sind — eine Aufwertung wäre eine
   erfundene Entscheidung gewesen.

**Ein Konflikt wurde aufgelöst:** ADR-0002 hält fest, dass die A0-Bestätigung
„Docker Compose bevorzugt" die A5-gestützte Abschwächung Ü-02 aus CBP-WP-002
aufhebt. `PROJECT_DEFINITION.md` ist entsprechend korrigiert; OD-31 geschlossen.

**Der DRC** (ADR-0005) gibt den 16 vertagten Deployment-Kriterien einen festen
Ort mit fail-closed-Regel und Status NOT EVALUATED. Damit ist R-34 gemindert.
OD-33 ist geschlossen, weil der DRC dokumentiert **und** in G0, Manifest,
Profil, README und Project Brain verlinkt ist.

**Repository-Layout:** Empfehlung Option B (Monorepo) mit vorbereitetem Weg zu
Option C (getrenntes Wissens-Repository). Status **PROPOSED**, keine Datei
verschoben, OD-26 bleibt offen.

**G0 bleibt NOT PASSED.**
