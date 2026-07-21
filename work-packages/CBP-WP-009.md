# CBP-WP-009 — Repository Boundary Decision

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-009 |
| Titel | Repository Boundary Decision |
| Typ | `docs-only`, **interactive** |
| Prompt Mode | **Full** (NDF v1.0.0) |
| Context Budget | **B1 – Lean** (Core Brain Pilot) |
| Claude-Code-Modell | **Claude Opus 4.8** (`claude-opus-4-8`) |
| Claude-Code-Effort | **xhigh** |
| Phase | Phase 1 – Planung |
| Ausgeführt am | 2026-07-21 |
| Ablauf | **interaktiv**, zwei Phasen · **plus Nova-REWORK-Korrekturlauf** |
| Status | `in-review` |
| Autoritätsklasse | A2 |

> **Dieses Work Package enthält einen Nova-REWORK-Korrekturlauf.** Die
> Erstausführung wurde als COMPLETE berichtet; zwei abgeleitete Aussagen waren
> jedoch unzulässig erweitert beziehungsweise zu pauschal. Siehe
> [Nova-REWORK-Nachtrag](#nova-rework-nachtrag) am Ende. Die Erstausführung
> unten ist **nicht** umgeschrieben.

---

## Ziel

**OD-26 durch zwei getrennte, ausdrückliche Human-Maintainer-Entscheidungen
schließen:**

1. Zielstruktur des allgemeinen Core-Repositorys
2. Grenze zwischen Core-Repository, privatem Operator-Bereich und
   Runtime-Daten

Eine Entscheidung zu nur einem Teil hätte OD-26 **nicht** geschlossen.

## Interaktiver Ablauf

| Phase | Inhalt | Ergebnis |
| --- | --- | --- |
| **A** | Repository read-only prüfen, bestehende Optionen abgleichen, **einen** Entscheidungsfragebogen ausgeben, keine Datei verändern | 16 Vorprüfungspunkte bestanden, Fragebogen ausgegeben, **0 Dateiänderungen** |
| **B** | Nur die tatsächlich getroffenen Entscheidungen dokumentieren, ADR erstellen, OD-26 schließen, Status und Register aktualisieren | Beide Entscheidungen aufgezeichnet, ADR-0007 `accepted` |

## Human-Entscheidungen

Beide am **2026-07-21**, Autorität **A0**, Quelle: direkte
Human-Maintainer-Entscheidung. Wortlaut unverändert übernommen, keine Auflage
ergänzt oder erweitert.

### Teil A — Zielstruktur des Core-Repositorys

**SELECT A2 – Ziel-Monorepo nach Layout-Option B**

Zielbereiche: `core/`, `adapters/`, `deployments/`, `config/`, `docs/`,
`examples/`, `tests/`.

**Autorisiert keine Verschiebung, Umbenennung oder Reorganisation.** Das
aktuelle Layout bleibt bis zu einem separaten, ausdrücklich freigegebenen
Migrations-Work-Package. Die Migration muss **nachvollziehbar, schrittweise,
rücksetzbar und ohne Verlust der Git-Historie** geplant werden.

### Teil B — Grenze zum privaten Operator-Bereich

**SELECT B3 – privater Operator-Workspace außerhalb des Core-Repositorys**

Private und produktive Wissensbestände, konkrete Source Mappings, private
Collection-Konfigurationen und **operatorbezogene kanonische
Registry-Metadaten** liegen außerhalb. Runtime-Daten bilden einen dritten,
separaten Bereich. **Secrets nirgends im Klartext** — nur Verweise auf einen
getrennten Secret Store. **Eine Runtime-Kopie der Source Registry ist nie die
einzige Quelle kanonischer Registry-Metadaten.**

Vollständiger Wortlaut in
[ADR-0007](../docs/decisions/ADR-0007-repository-und-workspace-grenze.md).

## Scope

- Read-only-Vorprüfung, Optionsabgleich, **ein** Entscheidungsfragebogen
- Beide Entscheidungen im Wortlaut aufzeichnen
- ADR-0007 nach vorhandener Konvention erstellen
- OD-26 schließen
- Status und Register nachführen
- Titelkorrektur in der Work-Package-Queue

## Out of Scope

- Entscheidungen erfinden, ergänzen oder erweitern
- Dateiänderung vor der Human-Antwort
- **Repository-Reorganisation, Verschiebung, Umbenennung**
- Zielverzeichnisse anlegen
- Privaten Workspace oder privates Repository anlegen
- Source Mapping erstellen, Registry implementieren
- Secret-Store-Auswahl
- OD-05, OD-06, OD-11, OD-34 schließen
- Commit, Push, Branch, Remote-Änderung, Issue, Release

## Inputs

NDF v1.0.0 · Repository-Stand auf `main` (Commit `47a336d`) ·
`REPOSITORY_LAYOUT_OPTIONS.md` · `REPOSITORY_AND_WORKSPACE_PLAN.md` ·
`PHASE_1_FOUNDATION_PLAN.md` · `PHASE_1_WORK_PACKAGE_MAP.md` ·
`PILOT_SOURCE_CONTRACT.md` · `SOURCE_SLOT_MODEL.md` · `ADR-0006` ·
`SYSTEM_ARCHITECTURE.md` · `COMPONENT_MODEL.md` · `DATA_CLASSIFICATION.md` ·
`PERMISSION_MODEL.md` · `DEPLOYMENT_READINESS_CHECK.md` ·
`DECISION_REGISTER.md` · `RISK_REGISTER.md` · `WORK_PACKAGE_QUEUE.md` ·
`PROJECT_MANIFEST.md` · `PROJECT_PROFILE.md` · `PROJECT_BRAIN.md` ·
`CBP-WP-008.md` · `README.md` · `CLAUDE.md` · **Antworten des Human
Maintainers**

## Aufgaben

| # | Aufgabe | Ergebnis |
| --- | --- | --- |
| 1 | Phase A — Vorprüfung und Entscheidungsfragebogen | 16 Punkte bestanden, 0 Dateiänderungen |
| 2 | Phase B — Entscheidungen prüfen und aufzeichnen | D-029, D-030 |
| 3 | ADR-0007 erstellen | `accepted`, A1 |
| 4 | OD-26 schließen | geschlossen, 2026-07-21 |
| 5 | Quelldokumente nachführen | Layoutoptionen, Workspace-Plan |
| 6 | Foundation Plan und Work-Package-Karte nachführen | F1-Entscheidungsteil erreicht |
| 7 | Status und Register | 13 Dokumente |
| 8 | Titelkorrektur Queue | Fehler aus CBP-WP-008 |

## Prüfungen

25 Prüfungen. Schwerpunkte: Entscheidungen stammen direkt vom Human
Maintainer · nichts ergänzt oder erweitert · Teil A und Teil B getrennt
dokumentiert · ADR-Status entspricht den Entscheidungen · OD-26 nur bei zwei
SELECT-Entscheidungen geschlossen · **keine Reorganisation** · **kein
Workspace angelegt** · keine privaten Pfade gespeichert · Core, Workspace und
Runtime getrennt · Registry-Schema und konkrete Metadaten getrennt ·
`.gitignore` nicht als Sicherheitsgrenze · ADR-0006 bleibt `accepted` ·
OD-05, OD-06, OD-34 bleiben offen · G0 bleibt PASSED WITH NOTES · Phase 1
bleibt AUTHORIZED FOR PLANNING · DRC bleibt NOT EVALUATED · Benchmark bleibt
nicht ausgeführt · keine Capability `implemented` · **Summen ausgezählt** ·
genau ein Folge-Work-Package · kein Commit, kein Push, `origin` unverändert.

## Akzeptanzkriterien

Beide Teilentscheidungen eindeutig erhoben · Auswirkungen dokumentiert ·
korrekter ADR vorhanden · OD-26 entsprechend behandelt · Core-, Operator- und
Runtime-Grenzen eindeutig · **keine Reorganisation** · keine privaten Daten
oder Pfade gespeichert · **keine Implementierung begonnen** · alle Prüfungen
bestanden.

---

## Ergebnis

| Gegenstand | Wert |
| --- | --- |
| **OD-26** | `open` → **`geschlossen`** (2026-07-21) |
| Neue A0-Entscheidungen | **D-029** (Teil A), **D-030** (Teil B) |
| **ADR-0007** | **`accepted`** (A1) |
| Angenommene ADRs | 6 → **7** |
| Getroffene Entscheidungen | 28 → **30** (davon **26** mit A0) |
| Offene Entscheidungen | 22 → **21**, davon **5** mit P0 |
| Repository-Reorganisation | **keine** |
| Angelegte Verzeichnisse | **keine** |
| Operator-Workspace | **nicht angelegt** |
| **Capabilities `implemented`** | **0 von 29**, unverändert |
| Geschlossene Risiken | **0** |
| **Commit / Push** | **nein / nein** |

## Rückmeldung an Nova

**OD-26 ist geschlossen** — durch zwei getrennte A0-Entscheidungen, wie
vorgesehen. Der Human Maintainer hat beide Nova-Empfehlungen bestätigt: **A2**
(Ziel-Monorepo nach Layout-Option B) und **B3** (Modell W-3).

**Es wurde nichts verschoben, nichts angelegt und nichts umbenannt.** Die
Top-Level-Struktur ist unverändert.

**Vier Punkte, die ich hervorhebe:**

1. **Die Trennung in zwei Teilfragen hat sich als notwendig erwiesen.** Beide
   Antworten sind unabhängig voneinander und wären einzeln unvollständig
   gewesen. Die Bezeichner A1/A2/A3 und B1/B2/B3 kollidieren bewusst nicht mit
   den Modellnamen W-1/W-2/W-3 aus der Vorlage.

2. **Der Operator-Workspace ist ab jetzt der kritischste
   Sicherungsgegenstand.** Er enthält kanonische Registry-Metadaten, die aus
   dem Index nicht rekonstruierbar sind — Grenze **G5** der Entscheidung. Sein
   Verlust wäre ein Wissensverlust, kein Cache-Verlust. **R-20 bleibt offen**:
   ein Restore wurde nie durchgeführt.

3. **Die Auflage zur Git-Historie ist neu und bindend.** D-029 verlangt eine
   Migration ohne Verlust der Historie. Ein entsprechendes
   Migrations-Work-Package ist in der Karte **nicht** geschnitten und wäre von
   Nova zu spezifizieren.

4. **Kein Risiko wurde geschlossen.** R-01 ist durch B3 **strukturell
   gemindert**, bleibt aber `teilweise gemindert`: Die Struktur verhindert den
   häufigsten Weg, nicht jeden, und es gibt weiterhin keine automatische
   Erkennung. Eine Strukturentscheidung ist kein technischer Nachweis.

**Ein Befund aus der Vorprüfung, den ich korrigiert habe:** Die
Übersichtstabelle der Work-Package-Queue trug noch die Titel eines verworfenen
Entwurfs der Work-Package-Karte. Der Fehler stammt aus CBP-WP-008 und war
mitcommittet; der Detailblock derselben Datei war korrekt. Sichtbar korrigiert,
Historie nicht umgeschrieben.

**Nächstes vorgeschlagenes Work Package: CBP-WP-010 — Pilot Source Mapping
Specification** (`docs-only`, interaktiv, Full, B1 – Lean). **Nicht ausführen**
ohne ausdrückliche Freigabe.

---

## Nova-REWORK-Nachtrag

| Feld | Wert |
| --- | --- |
| Ausführung | **Nova REWORK correction run** |
| Datum | 2026-07-21 |
| Ursprünglicher Reportstatus | **COMPLETE** |
| Human-Entscheidungen | **unverändert** — D-029 und D-030 nicht angetastet |
| ADR-0007 | bleibt **`accepted`** |
| OD-26 | bleibt **geschlossen** |
| Commit vor der Korrektur | **nicht erfolgt** |

**Die Erstausführung wird nicht stillschweigend umgeschrieben.** Der Bericht
oben bleibt im Wortlaut stehen; die beiden beanstandeten Aussagen sind unten
benannt und in den Zieldokumenten korrigiert.

### Befund 1 — unzulässig erweiterte Veröffentlichungsformulierung

**Ursprünglich:** „Das Core Repository ist **vollständig veröffentlichbar**",
sowie „Core-Historie bleibt klein und vollständig veröffentlichbar".

**Warum das falsch war:** Die Human-Entscheidung legt eine
**veröffentlichungsfähige Bereichstrennung** fest. Sie erteilt **keine**
öffentliche Freigabe. Meine Formulierung nahm eine Entscheidung vorweg, die
niemand getroffen hat — OD-11 (Sichtbarkeit), OD-23 (Lizenz) und OD-28
(Produktname) sind offen, und die Sperrliste untersagt öffentliches Branding
und Release weiterhin.

**Korrektur:** Das Core-Repository wird als **`publication-capable by design`**
beschrieben — eine **Bauweise**: privater Bestand, produktive Mappings und
Secrets sind ausgeschlossen; synthetische Fixtures, allgemeiner Code,
Architektur, Governance und Vorlagen sind zulässig. **Das Repository bleibt
zunächst privat.** Eine Veröffentlichung benötigt eine **separate,
ausdrückliche A0-Entscheidung**.

### Befund 2 — unzureichende Runtime-Datenklassifikation

**Ursprünglich:** Index, Cache, Context Packs, Jobs **und Auditdaten**
gemeinsam als „ausschließlich Derived Data, reproduzierbar, nie versioniert".

**Warum das falsch war:** Audit-, Approval- und Incident-Nachweise sind **nicht
reproduzierbar**. Ein verlorener Auditnachweis lässt sich durch keinen Rebuild
wiederherstellen. Sie als Cache zu behandeln hätte bedeutet, sie ohne
Sicherungspflicht zu führen.

**Korrektur:** Der Runtime-Bereich zerfällt in drei Unterklassen:

| Klasse | Reproduzierbar | Sicherungspflicht |
| --- | --- | --- |
| **RT-1** Rebuildable Derived Data | **ja** | nein |
| **RT-2** Operational Evidence | **nein** | **ja** — plus Aufbewahrung, Zugriffsschutz, ggf. Integritätsnachweise |
| **RT-3** Transient Runtime State | entfällt | nein — kontrolliert verwerfen, nie alleinige Statuswahrheit |

**Keine Technologie gewählt.** Append-only oder gleichwertiger
Manipulationsschutz für RT-2 ist zulässig, aber nicht bestimmt.

### Ausgeführte Korrekturen

| # | Korrektur | Dokumente |
| --- | --- | --- |
| 1 | `publication-capable by design` statt „vollständig veröffentlichbar"; Sichtbarkeit ausdrücklich privat; Freigabe benötigt A0 | ADR-0007, REPOSITORY_AND_WORKSPACE_PLAN, REPOSITORY_LAYOUT_OPTIONS, PROJECT_MANIFEST, PROJECT_PROFILE, PROJECT_BRAIN, README, CLAUDE |
| 2 | RT-1 / RT-2 / RT-3 definiert; Auditdaten nicht mehr als reproduzierbar geführt | ADR-0007, REPOSITORY_AND_WORKSPACE_PLAN, PROJECT_BRAIN, PROJECT_MANIFEST, CLAUDE, PHASE_1_FOUNDATION_PLAN |
| 3 | Registry-Grenze präzisiert: Schema im Core, kanonische Metadaten im Workspace, **Runtime-Projektion ist nicht die Registry** (RG-1…RG-4) | ADR-0007, REPOSITORY_AND_WORKSPACE_PLAN |
| 4 | Grenzen **G9** (RT-2 kein Cache) und **G10** (RT-3 nie alleinige Statuswahrheit) ergänzt | ADR-0007 |
| 5 | Backupwirkung von drei auf **fünf** Sicherungsverträge erweitert | ADR-0007 |
| 6 | R-01 auf den **Veröffentlichungspfad** begrenzt; Status `offen` | RISK_REGISTER, ADR-0007 |
| 7 | R-20 um Operator-Registry **und** RT-2 erweitert | RISK_REGISTER, ADR-0007 |

### Neue Prüfevidenz

| Prüfung | Ergebnis |
| --- | --- |
| „vollständig veröffentlichbar" kommt in keinem CBP-WP-009-Dokument mehr als **Aussage** vor — nur noch als Zitat des Befunds in diesem Nachtrag | bestanden |
| `publication-capable by design` in ADR-0007 definiert, mit Bedeutet-/Bedeutet-nicht-Tabelle | bestanden |
| Repository-Sichtbarkeit ausdrücklich **privat** | bestanden |
| Öffentliche Freigabe ausdrücklich A0-pflichtig | bestanden |
| RT-1, RT-2, RT-3 definiert | bestanden |
| Auditnachweise **nicht** als reproduzierbar dargestellt | bestanden |
| RT-2 mit Aufbewahrung, Zugriffsschutz und Backupanforderung | bestanden |
| Runtime-Projektion ausdrücklich **nicht** die kanonische Registry | bestanden |
| R-01 als `offen` geführt, Wirkungsbereich benannt | bestanden |
| R-20 umfasst Workspace **und** RT-2 | bestanden |
| **Kein Risiko geschlossen** | bestanden |
| D-029 und D-030 unverändert | bestanden |
| Keine Reorganisation, kein Workspace, kein Runtime-Verzeichnis angelegt | bestanden |
| Keine Technologie für Backup, Audit oder Secret Store gewählt | bestanden |

### Was ich daraus mitnehme

**Beide Befunde sind derselbe Fehler in zwei Formen:** Ich habe aus einer
Entscheidung eine Eigenschaft abgeleitet, die sie nicht zusicherte. „Privater
Bestand ist ausgeschlossen" wurde zu „veröffentlichbar"; „liegt im
Runtime-Bereich" wurde zu „reproduzierbar". In beiden Fällen war die
Ableitung bequemer als die Entscheidung — und in beiden Fällen hätte sie
später eine Lücke gedeckt, die niemand mehr gesucht hätte.
