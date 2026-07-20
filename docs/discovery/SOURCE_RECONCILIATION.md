# Source Reconciliation — Abgleich gegen die Originalquellen

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-002 |
| Autoritätsklasse dieses Dokuments | A2 |
| Stand | 2026-07-20 |

Dieses Dokument gleicht das in CBP-WP-001 erzeugte dokumentarische Fundament
gegen die Originalquellen ab. Es enthält keine langen Volltextkopien, sondern
kurze Paraphrasen mit präzisen Referenzen.

---

## 1. Identifikation der Quellen

| Quelle | Rolle | Klasse | Umfang |
| --- | --- | --- | --- |
| `Bauanleitung_Second-Brain.pdf` | **Originalquelle**, externe erläuternde Referenzdokumentation | **A4** | sechs Inhaltsseiten |
| `Second-Brain-Bauanleitung-Textfassung.md` | **abgeleitete Arbeitsrepräsentation** der PDF, nur zur maschinenlesbaren Auswertung | **A6** | Seitenmarker 1 bis 6 |
| `docs/discovery/Core-Brain-Project-Handoff.md` | **freigegebene Projektübergabe**, projektspezifische Erweiterung des ursprünglichen Plans | **A5** | 20 Abschnitte |

### Quellenbeziehung

```text
Bauanleitung_Second-Brain.pdf          (A4, Original, sechs Inhaltsseiten)
        │
        └── abgeleitet ──> Second-Brain-Bauanleitung-Textfassung.md   (A6)
                            Seitenmarker 1–6, nur Arbeitsrepräsentation

Core-Brain-Project-Handoff.md          (A5, freigegebene Übergabe)
        └── erweitert den Plan der Bauanleitung projektspezifisch
```

**A6 überschreibt A4 nicht.** Die Textfassung beansprucht keine höhere
Autorität als die PDF. Wo beide abweichen würden, gilt die PDF.

### Einschränkung der Auswertung — ausdrücklich dokumentiert

Drei Punkte, die für die Bewertung dieses Abgleichs wesentlich sind:

1. Der Fließtext der PDF war im lokalen Werkzeug **nicht zuverlässig
   extrahierbar**. Eine Textextraktion lieferte über 287 Einheiten hinweg nur
   rund 13.000 Zeichen, überwiegend Überschriftenfragmente. Das
   Seitenrendering stand nicht zur Verfügung.
2. Für die maschinenlesbare Auswertung wurde deshalb die **begleitende
   Textfassung (A6)** verwendet, deren Seitenmarker laut Freigabe den sechs
   Inhaltsseiten der PDF entsprechen.
3. Eine **visuelle Detailprüfung der PDF wird ausdrücklich nicht behauptet.**
   Alle Seitenreferenzen in diesem Dokument stützen sich auf die Seitenmarker
   der Textfassung, nicht auf eine eigene Sichtung des PDF-Layouts. Die 287
   Einheiten des fehlerhaften lokalen Extraktors werden nirgends als
   Seitenzahlen verwendet.

### Seitenzuordnung der Bauanleitung

| Seite | Inhalt |
| --- | --- |
| Seite 1 | Zentrale Frage, Fähigkeiten zuerst, Graph nicht als Fundament |
| Seite 2 | Datenbasis ordnen, `INDEX.md`, lokale qmd-Suche |
| Seite 3 | Brain-First-Protokoll, Baseline-Test, Wiki erst danach |
| Seite 4 | Unveränderte Rohquellen, Widerspruchsworkflow, Human Decision |
| Seite 5 | Oberfläche und Graph zuletzt, Mockups und kleine Schritte |
| Seite 6 | Spec, Plan, Tests, deterministische Verarbeitung, Markdown als Wahrheitsschicht |

---

## 2. Bereits korrekt übernommene Aussagen

Das Fundament aus CBP-WP-001 stimmt in folgenden Punkten mit den Quellen
überein:

| # | Aussage im Repository | Quelle |
| --- | --- | --- |
| 1 | Markdown ist der kanonische Wissensbestand | Bauanleitung, Seite 6; Übergabe §5 |
| 2 | Trennung kanonisch / abgeleitet | Übergabe §5 |
| 3 | Indexverlust darf keinen Wissensverlust verursachen | Übergabe §5, wörtliche Invariante |
| 4 | Autoritätsklassen A0–A6, A6 überschreibt A0–A5 nicht automatisch | Übergabe §6 |
| 5 | Fünf Datenklassen `public` bis `excluded-from-ai` | Übergabe §11 |
| 6 | Context Budgets B0–B4 mit den Namen Micro bis Exceptional | Übergabe §8 |
| 7 | B4 darf kein Normalmodus werden, Eskalationsfragen | Übergabe §8 |
| 8 | Keine automatische Konfliktauflösung, Mensch entscheidet | Bauanleitung, Seite 4; Übergabe §10 |
| 9 | Rohquellen bleiben unverändert | Bauanleitung, Seite 4 |
| 10 | Brain-First-Retrieval als Prinzip | Bauanleitung, Seite 3; Übergabe §7 |
| 11 | Deterministischer Quellenindex | Bauanleitung, Seite 6; Übergabe §9 |
| 12 | Proxmox erste Referenzplattform, nicht Produktgrenze | Übergabe §4, Leitprinzip |
| 13 | Deployment-neutrale Architektur | Übergabe §4, §13 |
| 14 | Keine automatischen Commits oder Pushes in der ersten Phase | Übergabe §10 |
| 15 | Oberfläche und Graph zuletzt | Bauanleitung, Seite 5; Übergabe §9 |
| 16 | Wiki nur als abgeleitete Schicht, KI darf nicht autoritativ ändern | Bauanleitung, Seite 4; Übergabe §9 |
| 17 | Backup, Restore, Rebuild als Anforderung | Übergabe §12 |
| 18 | Reproduzierbare abgeleitete Daten | Übergabe §5 |
| 19 | Jede Behauptung benötigt einen Prüfpunkt | Bauanleitung, Seite 6 |
| 20 | Phase 0 ohne produktive Installation | Übergabe §15 |

---

## 3. Fehlende Aussagen — ergänzt

Folgende Inhalte der Originalquellen fehlten im Fundament und wurden in
CBP-WP-002 ergänzt.

### F-01 — Das eigentliche Ausgangsproblem fehlte

**Quelle:** Übergabe §2, §3

Das Repository beschrieb das Ziel („kleinste ausreichende Menge"), nicht aber
das Problem, aus dem es entsteht: zu hoher Token- und Kontextverbrauch durch
umfangreiche Prompts, wiederholtes Laden stabiler Projektinformationen,
Durchsuchen vieler Dateien und lange Projektchat-Verläufe. Die Übergabe hält
fest, dass das Claude-Nutzungslimit bereits nach wenigen umfangreichen Prompts
erreicht sein kann und mehrstündige Unterbrechungen nicht akzeptabel sind.

Ebenfalls fehlte die ausdrückliche Klarstellung, dass das System **keine
Nutzungslimits umgehen** soll, sondern vorhandenen Kontext effizienter nutzt.

**Ergänzt in:** `docs/architecture/PROJECT_DEFINITION.md`

### F-02 — Brain-First war Prinzip, aber keine Suchleiter

**Quelle:** Übergabe §7 (zehn Schritte); Bauanleitung, Seite 3 (fünf Schritte)

Das Repository nannte Brain-First als Prinzip, ohne die konkrete Reihenfolge.
Ebenfalls fehlte die Quellenzahlregel: Normalfall eine Quelle, erweiterter Fall
höchstens drei, darüber begründete Eskalation oder Aufteilung.

**Ergänzt in:** `docs/architecture/ARCHITECTURE_PRINCIPLES.md`,
`docs/architecture/CONTEXT_BUDGETS.md`

### F-03 — Pflichtmetadaten abgeleiteter Aussagen

**Quelle:** Übergabe §6

Jede abgeleitete Aussage soll Quellpfad, Quellentyp, Revision oder
Prüfzeitpunkt, Autoritätsklasse, Aktualitätsstatus, Verifikationsstatus und
mögliche Konfliktreferenzen führen. Diese sieben Felder fehlten vollständig.

**Ergänzt in:** `docs/architecture/ARCHITECTURE_PRINCIPLES.md`

### F-04 — Sicherheitsmodell mit Berechtigungsstufen

**Quelle:** Übergabe §10

Es fehlten: kein Betrieb als Root, kein Betrieb direkt auf dem Proxmox-Host,
keine Proxmox-API-Berechtigungen, keine pauschalen GitHub-Schreibrechte, keine
öffentliche Freigabe interner Dienste, keine unkontrollierten Plugins oder
MCP-Server. Ebenso fehlten die fünf Berechtigungsstufen `read`, `draft`,
`write with approval`, `publish with approval`, `forbidden` sowie die
Forderung, Berechtigungen **technisch** und nicht nur über Promptregeln
umzusetzen.

**Ergänzt in:** `docs/architecture/TRUST_BOUNDARIES.md`

### F-05 — Fünf Referenzprofile statt zwei Plattformen

**Quelle:** Übergabe §4

Das Repository kannte nur Proxmox und Docker Compose. Die Übergabe definiert
fünf Referenzprofile A bis E sowie eine Liste dessen, was in der ersten Phase
ausdrücklich nicht verpflichtend ist.

**Ergänzt in:** `docs/architecture/PROJECT_DEFINITION.md`

### F-06 — Datenschutzmatrix mit den Dimensionen der Quelle

**Quelle:** Übergabe §11

Die Quelle verlangt je Datenklasse fünf Festlegungen: darf indexiert werden,
darf lokal durchsucht werden, darf an Claude übertragen werden, darf im Wiki
zusammengefasst werden, darf mobil angezeigt werden. Das Repository führte eine
abweichende Matrix.

**Korrigiert in:** `docs/privacy/DATA_CLASSIFICATION.md`

### F-07 — Vierstufiges Backupmodell und geprüfter Wiederherstellungspunkt

**Quelle:** Übergabe §12

Es fehlten die vier Stufen (Git-Historie, Sicherung der Datendisk, Proxmox-
oder VM-Backup, zusätzliche Kopie außerhalb des Hosts) sowie die Forderung
eines **überprüften** Wiederherstellungspunkts vor Reorganisationen,
Ingest-Läufen, Synchronisationsänderungen und Wiki-Migrationen.

**Ergänzt in:** `docs/architecture/PROJECT_DEFINITION.md`

### F-08 — Phasenmodell 0 bis 7

**Quelle:** Übergabe §15

Das Repository vermerkte „Phase 1+ noch nicht geplant". Die Übergabe definiert
acht Phasen von Discovery bis zur öffentlichen Entscheidung.

**Ergänzt in:** `docs/architecture/PROJECT_DEFINITION.md`,
`project-system/PROJECT_PROFILE.md`

### F-09 — Zehn Erfolgskriterien des Piloten

**Quelle:** Übergabe §16

Vollständig gefehlt. Sie sind die Grundlage des Benchmarkplans und damit
G0-relevant.

**Ergänzt in:** `docs/discovery/G0_SCOPE_LOCK_CRITERIA.md`

### F-10 — Do-not-start-Liste war unvollständig

**Quelle:** Übergabe §17

Die Übergabe nennt 16 Punkte. Das Repository führte 11. Es fehlten unter
anderem: produktive Mehrgeräte-Synchronisation ohne Test-Vault, neue
NDF-Skills, CDF-Integration, CoreOps-Integration, CDS-Komponenten, öffentliche
Cloudinstanz, endgültiges Branding als eigener Punkt.

**Ergänzt in:** `docs/product/DO_NOT_START.md`

### F-11 — Erwartete offene Informationen

**Quelle:** Übergabe §19

Sechzehn konkret zu erhebende Informationen. Sie bilden das Rückgrat der
G0-Kriterien und des Fragebogens.

**Ergänzt in:** `docs/discovery/G0_SCOPE_LOCK_CRITERIA.md`,
`docs/discovery/DISCOVERY_QUESTIONS.md`

### F-12 — Handoff-Abschlussformat

**Quelle:** Übergabe §20

Jede größere Projektphase endet mit einem Block zwischen
`# BEGIN CORE-BRAIN-HANDOFF` und `# END CORE-BRAIN-HANDOFF` mit zehn
Pflichtbestandteilen.

**Ergänzt in:** `docs/ndf/ADOPTION_NOTES.md`

### F-13 — Superpowers als Referenz, nicht als zweites Governance-System

**Quelle:** Übergabe §14

**Ergänzt in:** `docs/product/DO_NOT_START.md`

### F-14 — qmd als benannter Kandidat mit Prüfvorbehalt

**Quelle:** Bauanleitung, Seite 2 (qmd als lokale Bedeutungssuche);
Übergabe §9 (keine Vorentscheidung ohne Installations-, Plattform-, Lizenz-,
Wartungs- und Sicherheitsprüfung)

**Ergänzt in:** `project-system/DECISION_REGISTER.md` als OD-25

### F-15 — Sechs-Schritte-Bauprozess

**Quelle:** Bauanleitung, Seite 6

Datenbasis ordnen, Brainstorming, Spezifikation, Plan, Bauen in kleinen
prüfbaren Aufgaben, Praxistest gegen den bisherigen Ablauf.

**Ergänzt in:** `docs/architecture/ARCHITECTURE_PRINCIPLES.md`

### F-16 — Baseline-Vergleich als Messverfahren

**Quelle:** Bauanleitung, Seite 3

Dieselbe Frage in zwei frischen Sessions, einmal ohne und einmal mit System;
verglichen werden Tokenverbrauch, Zeit und Kontextfüllstand. Die Quelle hält
fest, dass der Nutzen bei einfachen Fragen geringer ausfällt und bei tief
vergrabenem Wissen steigt.

**Ergänzt in:** `docs/discovery/G0_SCOPE_LOCK_CRITERIA.md`

---

## 4. Zu stark formulierte Aussagen — abgeschwächt

### Ü-01 — „Keine Notwendigkeit, Wissensbestand an externe Dienste zu senden"

**Fundstelle:** `ARCHITECTURE_PRINCIPLES.md`, Prinzip 5 (Fassung CBP-WP-001)

Diese Formulierung war **sachlich falsch**. Übergabe §11 stellt ausdrücklich
klar, dass Claude Code keinen vollständig lokalen Sprachmodellbetrieb
verwendet und ausgewählte Inhalte an das Claude-Modell übertragen werden.
Lokal sind **Index und Suchmodelle**, nicht die Sprachverarbeitung.

Genau daraus entsteht die Notwendigkeit der Datenklassifikation. Die alte
Formulierung hätte den Zweck der Datenklassen untergraben.

**Korrigiert in:** `docs/architecture/ARCHITECTURE_PRINCIPLES.md`

### Ü-02 — Docker Compose als „bevorzugte" Laufzeit

**Fundstelle:** `README.md`, `PROJECT_DEFINITION.md`, `PROJECT_PROFILE.md`

Übergabe §4 führt Container als **Referenzprofil D**, ausdrücklich „kein
Pflichtziel für die erste Phase", das architektonisch möglich bleiben muss.
Referenzbetrieb sind Profil A (Proxmox-VM) und Profil B (allgemeine Linux-VM).

Abgeschwächt zu: dedizierte Linux-VM ist der Referenzbetrieb, Docker Compose
eine vorgesehene, noch nicht implementierte Anwendungslaufzeit innerhalb dieser
VM. Das deckt sich mit Nova-Entscheidung 15 und 16 aus CBP-WP-002.

**Korrigiert in:** `README.md`, `docs/architecture/PROJECT_DEFINITION.md`,
`project-system/PROJECT_PROFILE.md`

### Ü-03 — „Kein Mehrmandantenbetrieb, keine öffentliche Bereitstellung"

**Fundstelle:** `PROJECT_DEFINITION.md`

Als Aussage über Phase 0 richtig, als Produkteigenschaft zu stark. Übergabe
§13 verlangt, dass die Architektur **von Anfang an öffentlich dokumentierbar**
bleibt, und §15 Phase 7 hält die öffentliche Entscheidung ausdrücklich offen.

**Präzisiert in:** `docs/architecture/PROJECT_DEFINITION.md`

### Ü-04 — 16 Kernprinzipien als „verbindlich"

**Fundstelle:** `ARCHITECTURE_PRINCIPLES.md`

Die Prinzipien tragen A2 und sind nicht als ADR ausgefertigt. „Verbindlich" bei
gleichzeitigem A2-Vermerk war widersprüchlich. Der Abgleich bestätigt zwar
inhaltlich fast alle Prinzipien aus A5-Quelle, ihre formale Bindung bleibt aber
bis zu einem ADR offen.

**Präzisiert in:** `docs/architecture/ARCHITECTURE_PRINCIPLES.md`; siehe OD-03

### Ü-05 — Capability 27 „read-only MCP/API"

**Fundstelle:** `CAPABILITY_MATRIX.md`

Keine der beiden Originalquellen nennt eine read-only MCP-/API-Schnittstelle.
Übergabe §10 verlangt lediglich „keine unkontrollierten Plugins oder
MCP-Server". Die Capability stammt aus dem Wortlaut von CBP-WP-001 (A2), nicht
aus den Quellen.

**Provenienz vermerkt in:** `project-system/CAPABILITY_MATRIX.md`

---

## 5. Erkannte Widersprüche

Widersprüche werden markiert, nicht automatisch entschieden — entsprechend
Bauanleitung, Seite 4 und Übergabe §10.

### W-01 — „Lean Mode" gegen die NDF-Prompt-Modes

| Seite | Aussage |
| --- | --- |
| Übergabe §14 (A5) | „Lean Mode bevorzugen" als NDF-Nutzungsregel |
| NDF v1.0.0 (A1) | Kennt nur Full, Standard und Short |
| Übergabe §8 (A5) | B1 heißt „Lean" |

**Status: entschieden.** Nova-Entscheidung 5 und 6 zu CBP-WP-002 legen fest:
„Lean" ist **kein** offizieller NDF Prompt Mode, sondern ausschließlich der
Name des Context Budgets **B1**. Die Absicht der Übergabe — sparsamer Kontext —
wird über die Context Budgets abgebildet, nicht über einen erfundenen
Prompt Mode.

Vermutlicher Ursprung: Die Übergabe wurde verfasst, bevor die NDF-Modi
abgeglichen waren, und hat den Budgetnamen B1 auf die Prompt-Ebene übertragen.

Dokumentiert als AB-01, geschlossen als OD-12.

### W-02 — Ein-Datei-Regel gegen Drei-Quellen-Regel

| Seite | Aussage |
| --- | --- |
| Bauanleitung, Seite 3 (A4) | „Genau eine beste Datei öffnen" |
| Übergabe §7 (A5) | Normalfall eine Quelle, erweiterter Fall höchstens drei, darüber Eskalation |

**Status: aufgelöst, kein echter Konflikt.** Die Übergabe erweitert die Regel
ausdrücklich und benennt das selbst. A5 ist hier die spätere,
projektspezifische Quelle. Übernommen wurde die Drei-Quellen-Regel, verankert
in den Context Budgets.

### W-03 — Lokale Suche gegen Übertragung an Claude

| Seite | Aussage |
| --- | --- |
| Bauanleitung, Seite 2 (A4) | qmd-Modelle laufen lokal, offline nutzbar |
| Übergabe §11 (A5) | Claude Code verwendet keinen vollständig lokalen Modellbetrieb |

**Status: aufgelöst.** Kein Widerspruch, sondern zwei Ebenen: Index und Suche
lokal, Sprachverarbeitung nicht. Das Repository hatte beides vermengt — siehe
Ü-01.

### W-04 — Wiki-Position in der Suchleiter

| Seite | Aussage |
| --- | --- |
| Bauanleitung, Seite 3 (A4) | Wiki als Schritt 2 der Suchleiter |
| Übergabe §7 (A5) | Wiki als Schritt 4, „nur als abgeleitete Orientierung" |

**Status: aufgelöst.** Die Übergabe schiebt das Wiki nach hinten und schwächt
seine Rolle ab — konsistent mit dem A6-Rang abgeleiteter Inhalte. Übernommen
wurde die Fassung der Übergabe.

### W-05 — Repository-Struktur

| Seite | Aussage |
| --- | --- |
| Übergabe §13 (A5) | Mögliche spätere Struktur `core/`, `deployments/`, `docs/`, `examples/`; ausdrücklich noch nicht freigegeben |
| Repository (A2) | Struktur aus CBP-WP-001 mit `project-system/`, `project-brain/`, `work-packages/` |
| NDF v1.0.0 (A1) | Kanonische Struktur mit `project-manifest.yaml`, `project-brain/DECISIONS.md` |

**Status: offen, nicht entschieden.** Drei Strukturvorstellungen nebeneinander.
Die Übergabe stellt selbst klar, dass die konkrete Struktur noch nicht
freigegeben ist. Das stützt die Behandlung von AB-03 bis AB-08 als vorläufig.

Dokumentiert als OD-26.

---

## 6. Vorgenommene Korrekturen

| # | Korrektur | Datei |
| --- | --- | --- |
| K-01 | Prinzip lokale Suche sachlich richtiggestellt (Ü-01) | `ARCHITECTURE_PRINCIPLES.md` |
| K-02 | Brain-First-Suchleiter und Quellenzahlregel ergänzt (F-02) | `ARCHITECTURE_PRINCIPLES.md` |
| K-03 | Sieben Pflichtmetadaten abgeleiteter Aussagen ergänzt (F-03) | `ARCHITECTURE_PRINCIPLES.md` |
| K-04 | Sechs-Schritte-Bauprozess ergänzt (F-15) | `ARCHITECTURE_PRINCIPLES.md` |
| K-05 | „Verbindlich" zu A2-Status präzisiert (Ü-04) | `ARCHITECTURE_PRINCIPLES.md` |
| K-06 | Ausgangsproblem Token- und Kontextverbrauch ergänzt (F-01) | `PROJECT_DEFINITION.md` |
| K-07 | Fünf Referenzprofile A–E ergänzt (F-05) | `PROJECT_DEFINITION.md` |
| K-08 | Phasenmodell 0–7 ergänzt (F-08) | `PROJECT_DEFINITION.md` |
| K-09 | Backupmodell vierstufig ergänzt (F-07) | `PROJECT_DEFINITION.md` |
| K-10 | Compose-Formulierung abgeschwächt (Ü-02) | `PROJECT_DEFINITION.md`, `README.md`, `PROJECT_PROFILE.md` |
| K-11 | Öffentliche Dokumentierbarkeit präzisiert (Ü-03) | `PROJECT_DEFINITION.md` |
| K-12 | Sicherheitsmodell und fünf Berechtigungsstufen ergänzt (F-04) | `TRUST_BOUNDARIES.md` |
| K-13 | Datenschutzmatrix auf Quellendimensionen umgestellt (F-06) | `DATA_CLASSIFICATION.md` |
| K-14 | Do-not-start-Liste auf 16 Punkte erweitert (F-10, F-13) | `DO_NOT_START.md` |
| K-15 | Handoff-Abschlussformat ergänzt (F-12) | `ADOPTION_NOTES.md` |
| K-16 | Provenienz von Capability 27 vermerkt (Ü-05) | `CAPABILITY_MATRIX.md` |
| K-17 | Umlaut-Transkription aufgehoben, echte Umlaute in geänderten Dateien | AB-10, alle geänderten Dateien |

---

## 7. Weiterhin offene Punkte

| # | Offener Punkt | Bezug |
| --- | --- | --- |
| 1 | Repository-Struktur nicht freigegeben; drei Vorstellungen nebeneinander | W-05, OD-26 |
| 2 | qmd nur Kandidat, Prüfung ausstehend | F-14, OD-25 |
| 3 | Rang der Kernprinzipien formal ungeklärt | Ü-04, OD-03 |
| 4 | Sämtliche Infrastrukturangaben der Übergabe §19 unbeantwortet | F-11, G0 Bereich B/C |
| 5 | Benchmarkfragen noch nicht formuliert | F-09, F-16, G0 Bereich G |
| 6 | AB-03 bis AB-08 nur vorläufig akzeptiert | ADOPTION_NOTES |
| 7 | Öffentlicher Produktname offen | Übergabe §1 |

---

## 8. Liste aller in CBP-WP-002 geänderten Dateien

**Erstellt**

- `docs/discovery/SOURCE_RECONCILIATION.md`
- `docs/discovery/G0_SCOPE_LOCK_CRITERIA.md`
- `docs/architecture/CONTEXT_BUDGETS.md`
- `work-packages/CBP-WP-002.md`

**Geändert**

- `docs/discovery/Core-Brain-Project-Handoff.md` (nur Metadatenkopf)
- `docs/architecture/PROJECT_DEFINITION.md`
- `docs/architecture/ARCHITECTURE_PRINCIPLES.md`
- `docs/architecture/TRUST_BOUNDARIES.md`
- `docs/discovery/DISCOVERY_QUESTIONS.md`
- `docs/discovery/OPEN_INFORMATION.md`
- `docs/privacy/DATA_CLASSIFICATION.md`
- `docs/product/DO_NOT_START.md`
- `docs/ndf/ADOPTION_NOTES.md`
- `README.md`
- `project-brain/PROJECT_BRAIN.md`
- `project-system/PROJECT_PROFILE.md`
- `project-system/PROJECT_MANIFEST.md`
- `project-system/CAPABILITY_MATRIX.md`
- `project-system/DECISION_REGISTER.md`
- `project-system/RISK_REGISTER.md`
- `project-system/WORK_PACKAGE_QUEUE.md`
- `project-system/COMPLIANCE_CHECK.md`
- `project-system/HEALTH_SCORE.md`

---

## 9. Nachweis: keine Originalquelle wurde automatisch verändert

| Quelle | Ort | Veränderung |
| --- | --- | --- |
| `Bauanleitung_Second-Brain.pdf` | außerhalb des Repositorys | **keine** — ausschließlich lesend geöffnet |
| `Second-Brain-Bauanleitung-Textfassung.md` | außerhalb des Repositorys | **keine** — ausschließlich lesend geöffnet |
| `Core-Brain-Project-Handoff.md` | `docs/discovery/` | **nur Metadatenkopf vorangestellt** |

Beim Handoff wurde ausschließlich ein Metadatenblock **oberhalb** der
ursprünglichen Überschrift eingefügt, wie in CBP-WP-002 ausdrücklich erlaubt.
Unterhalb dieses Blocks wurde kein Zeichen des fachlichen Inhalts umformuliert,
gekürzt oder korrigiert. Die Prüfung erfolgte über `git diff`; die Änderung
besteht ausschließlich aus hinzugefügten Zeilen am Dateianfang.

Das entspricht der Regel „Rohquellen bleiben unverändert" aus
Bauanleitung, Seite 4.
