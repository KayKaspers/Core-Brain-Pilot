# CBP-WP-002 — Source Reconciliation und G0 Scope-Lock-Definition

| Feld | Wert |
| --- | --- |
| ID | CBP-WP-002 |
| Titel | Source Reconciliation und G0 Scope-Lock-Definition |
| Typ | `docs-only` |
| Prompt Mode | **Full** (NDF v1.0.0) |
| Context Budget | **B2 – Standard** (Core Brain Pilot) |
| Phase | Phase 0 – Discovery und Scope Lock |
| Ausführungsversuche | 3 (zwei BLOCKED, einer ausgeführt) |
| Ausgeführt am | 2026-07-20 |
| Status | `in-review` |
| Autoritätsklasse | A2 |

Dieses Dokument hält den Auftrag und seinen Verlauf fest. Das Ergebnis steht im
Implementation Report an Nova.

---

## Ziel

Das in CBP-WP-001 erzeugte dokumentarische Fundament gegen die beiden
ursprünglichen Projektquellen abgleichen und anschließend objektiv prüfbare
Kriterien für **G0 – Discovery and Scope Lock** definieren.

## Scope

- Bestehende Projektdokumentation korrigieren
- Fehlende Aussagen aus den Originalquellen ergänzen
- Zu stark formulierte Aussagen abschwächen
- Widersprüche dokumentieren
- Context Budgets B0–B4 definieren
- Offene Discovery-Informationen konsolidieren
- G0-Kriterien definieren
- Den nächsten Discovery-Schritt vorbereiten

## Out of Scope

- G0 als bestanden erklären
- Unbeantwortete Infrastrukturfragen erfinden
- Anwendungscode implementieren
- Docker Compose erstellen
- Eine Web-UI beginnen
- Suchsoftware installieren
- Ein Wiki erzeugen
- Commit oder Push ausführen

## Erlaubte Dateien

**Erstellen:** `docs/discovery/SOURCE_RECONCILIATION.md`,
`docs/discovery/G0_SCOPE_LOCK_CRITERIA.md`,
`docs/architecture/CONTEXT_BUDGETS.md`, `work-packages/CBP-WP-002.md`

**Ändern:** `README.md`, `CLAUDE.md`, die Dokumente unter `docs/architecture/`,
`docs/discovery/`, `docs/ndf/`, `docs/privacy/`, `docs/product/`, sowie
`project-brain/PROJECT_BRAIN.md` und alle Dateien unter `project-system/`.

**Zusätzlich erlaubt:** knapper Metadatenkopf in
`docs/discovery/Core-Brain-Project-Handoff.md`, ohne den fachlichen Inhalt zu
verändern.

## Verbotene Dateien

Dateien außerhalb von `D:\Projects\Core-Brain-Pilot`, Anwendungscode,
Dockerfile, `compose.yaml`, Skripte, CI/CD, Datenbanken, Suchindex, Embeddings,
Wiki-Ingest, Graph, Secrets, `LICENSE`, Remote-Änderungen, Branch-Erstellung,
Commit, Push, Softwareinstallation.

## Inputs

Verbindliche Quellenreihenfolge:

1. Ausdrückliche Vorgaben dieses Work Packages
2. `docs/discovery/Core-Brain-Project-Handoff.md` — **A5**
3. `Bauanleitung_Second-Brain.pdf` — **A4**, sechs Inhaltsseiten
4. `Second-Brain-Bauanleitung-Textfassung.md` — **A6**, abgeleitete
   Arbeitsrepräsentation, Seitenmarker 1 bis 6
5. Nova Development Framework **v1.0.0**
6. Aktueller Inhalt des lokalen Repositorys

Keine Inhalte aus einer späteren NDF-Version.

## Aufgaben

1. `SOURCE_RECONCILIATION.md` erstellen
2. Context Budgets B0–B4 definieren
3. Objektive G0-Kriterien erstellen
4. Discovery-Fragen konsolidieren
5. Decision-, Risk- und Work-Package-Register bereinigen
6. Capabilities nach P0, P1, P2 und Deferred priorisieren
7. `work-packages/CBP-WP-002.md` erstellen
8. Genau ein Folge-Work-Package vorschlagen, nicht ausführen

## Tests

Zwanzig Prüfungen der ursprünglichen Fassung, ergänzt um zehn zusätzliche
Prüfungen zur Quellenbehandlung. Vollständige Ergebnisse mit Evidenz im
Implementation Report.

Schwerpunkte: beide Originalquellen gelesen; Seitenreferenzen ausschließlich
Seite 1 bis 6; keine visuelle PDF-Prüfung behauptet; OI-01 nur nach
dokumentierter Provenienz geschlossen; keine Capability `implemented`; alle
Capabilities priorisiert; AB-03 bis AB-08 nicht stillschweigend dauerhaft
akzeptiert; keine erfundene Discovery-Antwort; kein Commit, kein Push.

## Akzeptanzkriterien

CBP-WP-002 ist COMPLETE, wenn beide Originalquellen abgeglichen wurden, die
Quellenlücke OI-01 nachvollziehbar geschlossen ist, alle relevanten
Abweichungen dokumentiert sind, Context Budgets B0–B4 definiert sind,
G0-Kriterien objektiv prüfbar vorliegen, der Human-Maintainer-Fragebogen
konsolidiert ist, Decision-, Risk- und Capability-Register konsistent sind, G0
nicht vorzeitig als bestanden markiert wurde, kein Implementierungsscope
begonnen wurde und alle Prüfungen bestanden sind.

---

## Ausführungsverlauf

| Versuch | Ergebnis | Ursache |
| --- | --- | --- |
| 1 | **BLOCKED** in der Vorprüfung | Arbeitsbaum nicht sauber (untracked A5-Übergabe); PDF-Fließtext im lokalen Werkzeug nicht extrahierbar |
| 2 | **BLOCKED** in der Vorprüfung | A6-Textfassung am angegebenen Pfad nicht vorhanden; Inputs-Ordner leer |
| 3 | **ausgeführt** | Alle zwölf Vorprüfungspunkte erfüllt |

Beide Blocker-Meldungen erfolgten vor jeder Dateiänderung. In den Versuchen 1
und 2 wurde kein Schreibvorgang ausgeführt.

### Behebung zwischen den Versuchen

Der Human Maintainer hat die A5-Übergabe committet und gepusht (Commit
`03a29f5`) und die beiden Quelldateien nach
`D:\Projects\Core-Brain-Pilot-Inputs` bereitgestellt. Nova hat die
Quellenklassifikation A4/A5/A6 festgelegt und die Verwendung der Textfassung
für die maschinenlesbare Auswertung freigegeben.

### Einschränkung der Quellenauswertung

Der Fließtext der PDF war im lokalen Werkzeug nicht zuverlässig extrahierbar.
Für die maschinenlesbare Auswertung wurde die A6-Textfassung verwendet. Eine
**visuelle Detailprüfung der PDF wird nicht behauptet.** Alle Seitenreferenzen
stützen sich auf die Seitenmarker der Textfassung.

---

## Rückmeldung an Nova

Der Quellenabgleich bestätigt 20 Aussagen des Fundaments, ergänzt 16 fehlende
Inhalte, schwächt 5 zu starke Formulierungen ab und erfasst 5 Widersprüche.

Die wichtigste inhaltliche Korrektur ist **Ü-01**: Das Fundament behauptete,
es bestehe keine Notwendigkeit, Wissensbestand an externe Dienste zu senden.
Projektübergabe §11 stellt das Gegenteil klar — Claude Code verwendet keinen
vollständig lokalen Modellbetrieb, ausgewählte Inhalte werden übertragen.
Lokal sind Index und Suchmodelle. Die alte Formulierung hätte den Zweck der
Datenklassifikation untergraben.

Der wichtigste Widerspruch ist **W-01**: Projektübergabe §14 empfiehlt „Lean
Mode", den NDF v1.0.0 nicht kennt. Aufgelöst durch D-009 — „Lean" ist
ausschließlich der Name des Context Budgets B1.

**G0 bleibt NOT PASSED.** 41 Kriterien liegen vor, 39 blockierend, keines
beantwortet.

> ### ⚠ Nachkorrektur der Kennzahlen
>
> Die beiden Zahlen im Absatz darüber sind **fehlerhaft**. Sie bleiben im
> Wortlaut stehen, damit die historische Ausführung nachvollziehbar bleibt.
>
> | Kennzahl | Ursprünglich berichtet | Reproduzierbar ausgezählt |
> | --- | --- | --- |
> | G0-Kriterien gesamt | 41 | **47** |
> | Blockierend (damaliges Modell) | 39 | **45** |
> | P0-Fragen | 35 | **38** |
> | Fragen gesamt | 55 | **56** |
>
> **Ursache:** Die Summen wurden fortgeschrieben statt ausgezählt. Die
> Kriterien- und Fragendokumente selbst waren vollständig und korrekt — nur die
> Summenzeilen und der Implementation Report stimmten nicht.
>
> **Korrigiert in:** CBP-WP-003. **Erfasst als:** Risiko R-33. **Konsequenz:**
> Kennzahlen werden seither ausgezählt, nicht aus dem Vorbericht übernommen.
>
> Diese Notiz wurde in CBP-WP-004 ergänzt (OD-31). Der übrige Inhalt dieses
> Dokuments ist unverändert. Der konsolidierte Fragebogen enthält 55 Fragen, davon 35 mit P0.

Entscheidungsbedarf besteht bei 14 P0-Entscheidungen, insbesondere OD-26
(Repository-Struktur, drei Vorstellungen nebeneinander) und OD-29 (dauerhafte
Behandlung der Abweichungen AB-03 bis AB-08, derzeit nur vorläufig für den
Bootstrap akzeptiert).
