# G0 – Discovery and Scope Lock — Kriterien

| Feld | Wert |
| --- | --- |
| Gate | **G0 – Discovery and Scope Lock** |
| **Gate-Status** | **NOT PASSED** |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-002 |
| Autoritätsklasse | A3 (Gate-Dokumentation) |
| Stand | 2026-07-20 |

Dieses Dokument definiert objektiv prüfbare Kriterien für G0. Es erklärt G0
**nicht** als bestanden und darf das auch nicht.

## Statuswerte

| Status | Bedeutung |
| --- | --- |
| `open` | Nicht beantwortet |
| `answered` | Beantwortet, noch nicht geprüft |
| `accepted` | Beantwortet, geprüft und vom Human Maintainer angenommen |
| `blocked` | Beantwortung hängt an einer anderen offenen Entscheidung |

**Nachweis** bedeutet eine überprüfbare Angabe: ein Wert, ein Dokumentverweis,
ein Kommandoergebnis. Eine Absichtserklärung ist kein Nachweis.

---

## A — Nutzer und Scope

| ID | Kriterium | Nachweis | Owner | Status | Autorität | Blockiert G0 |
| --- | --- | --- | --- | --- | --- | --- |
| A-1 | Primärer Nutzer benannt | Rollenangabe | Human Maintainer | `open` | A0 | **ja** |
| A-2 | Erwartete Nutzerzahl | Zahl | Human Maintainer | `open` | A0 | **ja** |
| A-3 | Zahl der Geräte | Zahl, aufgeschlüsselt nach Typ | Human Maintainer | `open` | A0 | **ja** |
| A-4 | Desktop-Anforderungen | Liste der Arbeitsfälle | Human Maintainer | `open` | A0 | **ja** |
| A-5 | Mobile-Anforderungen | Liste, Android oder iOS benannt | Human Maintainer | `open` | A0 | **ja** |
| A-6 | Offlineanforderungen | ja/nein je Anwendungsfall | Human Maintainer | `open` | A0 | **ja** |
| A-7 | Native Obsidian-Nutzung erforderlich | ja/nein mit Begründung | Human Maintainer | `open` | A0 | **ja** |
| A-8 | Explizite Nicht-Ziele | Liste | Nova + Human Maintainer | `open` | A0 | **ja** |

Grundlage: Projektübergabe §19, §15 Phase 0.

## B — Proxmox und Infrastruktur

| ID | Kriterium | Nachweis | Owner | Status | Autorität | Blockiert G0 |
| --- | --- | --- | --- | --- | --- | --- |
| B-1 | Proxmox-Version | Versionsstring | Human Maintainer | `open` | A0 | **ja** |
| B-2 | Einzelhost oder Cluster | Angabe, bei Cluster Knotenzahl | Human Maintainer | `open` | A0 | **ja** |
| B-3 | Verfügbare CPU | Kerne, für die VM zusagbar | Human Maintainer | `open` | A0 | **ja** |
| B-4 | Verfügbarer RAM | GB, für die VM zusagbar | Human Maintainer | `open` | A0 | **ja** |
| B-5 | Verfügbarer Speicher | GB, getrennt nach System und Daten | Human Maintainer | `open` | A0 | **ja** |
| B-6 | Storage-Technologie | ZFS, LVM oder andere | Human Maintainer | `open` | A0 | **ja** |
| B-7 | Backupziele | Ziel, Verfahren, Frequenz | Human Maintainer | `open` | A0 | **ja** |
| B-8 | Externe Backupkopie außerhalb des Hosts | Ziel benannt oder ausdrücklich verneint | Human Maintainer | `open` | A0 | **ja** |

Grundlage: Projektübergabe §12, §19.

## C — Netzwerk und Zugriff

| ID | Kriterium | Nachweis | Owner | Status | Autorität | Blockiert G0 |
| --- | --- | --- | --- | --- | --- | --- |
| C-1 | Bestehendes VPN vorhanden | ja/nein, Produkt | Human Maintainer | `open` | A0 | **ja** |
| C-2 | Tailscale oder WireGuard | Angabe oder „keines" | Human Maintainer | `open` | A0 | **ja** |
| C-3 | DNS | interne Auflösung beschrieben | Human Maintainer | `open` | A0 | nein |
| C-4 | Reverse Proxy | vorhanden/geplant/keiner | Human Maintainer | `open` | A0 | nein |
| C-5 | Erlaubte ausgehende Verbindungen | Liste der Ziele | Human Maintainer | `open` | A0 | **ja** |
| C-6 | Mobile Zugriffsmethode | Verfahren beschrieben | Human Maintainer | `open` | A0 | **ja** |

Grundlage: Projektübergabe §9 (Remotezugriff), §10, §19.
Randbedingung aus §10: keine öffentliche Freigabe interner Dienste als Standard.

## D — Datenbestand

| ID | Kriterium | Nachweis | Owner | Status | Autorität | Blockiert G0 |
| --- | --- | --- | --- | --- | --- | --- |
| D-1 | Gewünschte Quellen | Liste mit Pfaden oder Systemen | Human Maintainer | `open` | A0 | **ja** |
| D-2 | Größenordnung | Dateizahl und Volumen | Human Maintainer | `open` | A0 | **ja** |
| D-3 | Dateiformate | Liste | Human Maintainer | `open` | A0 | **ja** |
| D-4 | Datenklassen zugeordnet | Zuordnung je Quelle | Human Maintainer | `open` | A0 | **ja** |
| D-5 | Ausgeschlossene Daten | Liste, `excluded-from-ai` benannt | Human Maintainer | `open` | A0 | **ja** |
| D-6 | Personenbezogene Daten | Umfang und Rechtsgrundlage | Human Maintainer | `open` | A0 | **ja** |
| D-7 | Vertrauliche Informationen | Umfang, Behandlung | Human Maintainer | `open` | A0 | **ja** |
| D-8 | Secret-Verfahren | Verfahren bei Fund in der Historie | Human Maintainer | `open` | A0 | **ja** |

Grundlage: Projektübergabe §11, §19.
D-6 bis D-8 sind die **kritischen Datenschutzfragen** im Sinne der
Abschlussregel.

## E — Claude und Repositories

| ID | Kriterium | Nachweis | Owner | Status | Autorität | Blockiert G0 |
| --- | --- | --- | --- | --- | --- | --- |
| E-1 | Aktuelle Claude-Desktop-Nutzung | Beschreibung des Ist-Zustands | Human Maintainer | `open` | A0 | **ja** |
| E-2 | Erlaubte Repository-Zugriffe | Liste, Lese- und Schreibrechte getrennt | Human Maintainer | `open` | A0 | **ja** |
| E-3 | GitHub-Zugriffe | Umfang, keine pauschalen Schreibrechte | Human Maintainer | `open` | A0 | **ja** |
| E-4 | Erlaubte Schreibrechte | Zuordnung zu den fünf Berechtigungsstufen | Human Maintainer | `open` | A0 | **ja** |
| E-5 | Freigabeverfahren | Beschreibung des Ablaufs | Human Maintainer | `open` | A0 | **ja** |

Grundlage: Projektübergabe §9 (Claude-Code-Arbeitsumgebung), §10, §19.
Berechtigungsstufen: `read`, `draft`, `write with approval`,
`publish with approval`, `forbidden`.

## F — Architektur

| ID | Kriterium | Nachweis | Owner | Status | Autorität | Blockiert G0 |
| --- | --- | --- | --- | --- | --- | --- |
| F-1 | VM als Referenzbetrieb bestätigt oder abgelehnt | Entscheidung | Human Maintainer | `open` | A0 | **ja** |
| F-2 | Docker Compose als Pilotlaufzeit bestätigt oder abgelehnt | Entscheidung | Human Maintainer | `open` | A0 | **ja** |
| F-3 | Trennung canonical / derived festgeschrieben | ADR | Nova + Human Maintainer | `open` | A1 | **ja** |
| F-4 | Backup- und Restore-Zielwerte | RPO und RTO als Zahlen | Human Maintainer | `open` | A0 | **ja** |
| F-5 | Deployment-Neutralität bestätigt | ADR mit Referenzprofilen A–E | Nova + Human Maintainer | `open` | A1 | **ja** |
| F-6 | UI- und Wiki-Gates definiert | Bedingungen benannt | Nova | `open` | A3 | **ja** |

Grundlage: Projektübergabe §4, §5, §12, §9 (Oberfläche und Graph).
Zu F-6: Übergabe §9 nennt als Bedingungen, dass Index und Suche funktionieren,
Tokenersparnis belegt ist, Mehrgerätezugriff funktioniert und der Alltagsnutzen
bestätigt ist.

## G — Benchmark

| ID | Kriterium | Nachweis | Owner | Status | Autorität | Blockiert G0 |
| --- | --- | --- | --- | --- | --- | --- |
| G-1 | Mindestens **30** Benchmarkfragen geplant | Fragenliste | Nova + Human Maintainer | `open` | A2 | **ja** |
| G-2 | Kategorien definiert | Kategorienliste mit Verteilung | Nova | `open` | A2 | **ja** |
| G-3 | Erfolgsmetriken definiert | Metriken mit Zielwerten | Nova + Human Maintainer | `open` | A2 | **ja** |
| G-4 | Baseline-Verfahren definiert | Verfahrensbeschreibung | Nova | `open` | A2 | **ja** |
| G-5 | Datenschutzfälle enthalten | mindestens 3 Fragen | Nova | `open` | A2 | **ja** |
| G-6 | Konfliktfälle enthalten | mindestens 3 Fragen | Nova | `open` | A2 | **ja** |

### Vorgaben aus den Quellen

**Baseline-Verfahren** (Bauanleitung, Seite 3): Dieselbe Frage in zwei frischen
Sessions — einmal ohne System, einmal mit Index, Suche und Regeln. Verglichen
werden Tokenverbrauch, Zeit und Kontextfüllstand. Die Quelle hält fest, dass
der Nutzen bei einfachen Fragen geringer ausfällt und bei tief vergrabenem oder
über mehrere Dateien verteiltem Wissen steigt — die Fragenmenge muss beide
Sorten enthalten.

**Erfolgsmetriken** aus Projektübergabe §16, zehn Kriterien:

| # | Erfolgskriterium |
| --- | --- |
| 1 | Derselbe Wissensstand ist von mehreren Geräten erreichbar |
| 2 | Die Baselinefragen werden korrekt beantwortet |
| 3 | Deutlich weniger Dateien werden geöffnet |
| 4 | Deutlich weniger Kontext wird an Claude übertragen |
| 5 | Die Antwortqualität sinkt nicht |
| 6 | Quellen und Revisionen sind nachvollziehbar |
| 7 | Konflikte werden nicht automatisch aufgelöst |
| 8 | Backups und Restore sind getestet |
| 9 | Kein Proxmox-Lock-in entsteht |
| 10 | Ein generischer Linux-Betrieb ist plausibel dokumentierbar |

„Deutlich weniger" ist zu quantifizieren — das ist Gegenstand von G-3.

---

## Abschlussregel

**G0 ist nur bestanden, wenn alle fünf Bedingungen erfüllt sind:**

1. **Alle blockierenden Kriterien sind `accepted`.**
2. **Keine kritische Datenschutzfrage ist offen** — D-4 bis D-8 sind `accepted`.
3. **Keine kritische Betriebsfrage ist offen** — B-7, B-8, C-5, F-4 sind `accepted`.
4. **Ein messbarer Benchmarkplan existiert** — G-1 bis G-6 sind `accepted`.
5. **Der Human Maintainer gibt G0 ausdrücklich frei.**

Bedingung 5 ist eigenständig. Auch wenn die Bedingungen 1 bis 4 erfüllt sind,
gilt G0 erst mit ausdrücklicher Freigabe (A0) als bestanden. Kein
Implementation Agent und kein automatisches Verfahren stellt das Bestehen fest.

## Aktueller Stand

| Kennzahl | Wert |
| --- | --- |
| Kriterien gesamt | **41** |
| davon blockierend | **39** |
| davon nicht blockierend | 2 (C-3, C-4) |
| Status `accepted` | **0** |
| Status `answered` | 0 |
| Status `open` | **41** |
| Human-Maintainer-Freigabe | **nicht erteilt** |

**Gate-Status: NOT PASSED.**

Es ist kein einziges Kriterium beantwortet. Die Antworten sind über den
konsolidierten Fragebogen in
[DISCOVERY_QUESTIONS.md](DISCOVERY_QUESTIONS.md) zu erheben.

## Pflege

Ein Kriterium wechselt den Status nur im Rahmen eines freigegebenen Work
Packages und nur mit hinterlegtem Nachweis. Der Wechsel nach `accepted`
erfordert die Autorität aus der Spalte „Autorität". Ein Implementation Agent
setzt kein Kriterium eigenmächtig auf `accepted`.
