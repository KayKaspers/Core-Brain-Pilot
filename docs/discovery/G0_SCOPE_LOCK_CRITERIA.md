# G0 – Discovery and Scope Lock — Kriterien

| Feld | Wert |
| --- | --- |
| Gate | **G0 – Discovery and Scope Lock** |
| **Gate-Status** | **NOT PASSED** |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-002, überarbeitet in CBP-WP-003 |
| Autoritätsklasse | A3 (Gate-Dokumentation) |
| Stand | 2026-07-20 |

Dieses Dokument definiert objektiv prüfbare Kriterien für G0. Es erklärt G0
**nicht** als bestanden und darf das auch nicht.

---

## Kriterienklassen

G0 sperrt den **allgemeinen Produkt- und Architektur-Scope**, nicht sämtliche
Details einer späteren Installation. Dazu werden drei Klassen unterschieden.

| Klasse | Bedeutung | Blockiert G0? |
| --- | --- | --- |
| **Core Required** | Allgemeine, produktweite Architektur- und Sicherheitsregeln, unabhängig von der konkreten Installation | **ja** |
| **Deployment Required** | Angaben, die erst unmittelbar vor dem Aufbau eines gewählten Deploymentprofils benötigt werden | **nein** — später |
| **Conditional** | Angaben, die nur erforderlich sind, wenn eine bestimmte Funktion oder Datenart tatsächlich verwendet wird | **nur bei aktivierter Funktion** |

> **Ein unbekannter Infrastrukturwert verhindert den allgemeinen Scope Lock
> nicht.** Er verhindert eine spätere Installation.

### Fail-closed für Deployment Required

Deployment-Required-Kriterien werden **nicht gestrichen**, sondern vertagt. Eine
spätere Installation muss **fail-closed** arbeiten: fehlt eine dafür notwendige
Deploymentangabe, wird nicht installiert. Die Prüfung dieser Klasse erfolgt in
einem **separaten Deployment-Readiness-Gate**, das in einem späteren Work
Package zu definieren ist.

*Ein neuer Gate-Name wird hier bewusst noch nicht eingeführt.*

## Statuswerte

| Status | Bedeutung |
| --- | --- |
| `open` | Nicht beantwortet |
| `answered` | Beantwortet, noch nicht als Entscheidung angenommen |
| `accepted` | Ausdrücklich entschieden und angenommen |
| `blocked` | Beantwortung hängt an einer anderen offenen Entscheidung |
| `not-applicable` | Für den aktuellen Pilotumfang nicht einschlägig |

**Nachweis** bedeutet eine überprüfbare Angabe. Eine Absichtserklärung ist kein
Nachweis.

---

## A — Nutzer und Scope

| ID | Kriterium | Klasse | Status | Nachweis | Autorität |
| --- | --- | --- | --- | --- | --- |
| A-1 | Primärer Nutzer benannt | **Core** | `answered` | HDI A2 — Einzelperson | A0 |
| A-2 | Erwartete Nutzerzahl | **Core** | `answered` | HDI A2 — 1 im ersten Pilot | A0 |
| A-3 | Zahl der Geräte | Deployment | `open` | — | A0 |
| A-4 | Desktop-Anforderungen | **Core** | `accepted` | HDI A6 — Web-UI im Pilot, nach Retrieval | A0 |
| A-5 | Mobile-Anforderungen | **Core** | `accepted` | HDI A6 — Suche, Lesen, Status, Handoffs, kleine Freigaben | A0 |
| A-6 | Offlineanforderungen | Conditional | `open` | Funktion nicht aktiviert | A0 |
| A-7 | Native Obsidian-Nutzung | Conditional | `accepted` | HDI A6 — **später**, nicht Pilotumfang | A0 |
| A-8 | Explizite Nicht-Ziele | **Core** | `open` | HDI A6 liefert funktionale Abgrenzungen; Repository-Sichtbarkeit und vollständige Nicht-Ziel-Liste fehlen | A0 |

## B — Infrastruktur

| ID | Kriterium | Klasse | Status | Nachweis | Autorität |
| --- | --- | --- | --- | --- | --- |
| B-1 | Proxmox-Version | Deployment | `open` | bewusst nicht erhoben | A0 |
| B-2 | Einzelhost oder Cluster | Deployment | `open` | bewusst nicht erhoben | A0 |
| B-3 | Verfügbare CPU | Deployment | `open` | bewusst nicht erhoben | A0 |
| B-4 | Verfügbarer RAM | Deployment | `open` | bewusst nicht erhoben | A0 |
| B-5 | Verfügbarer Speicher | Deployment | `open` | bewusst nicht erhoben | A0 |
| B-6 | Storage-Technologie | Deployment | `open` | bewusst nicht erhoben | A0 |
| B-7 | Backupziele | Deployment | `open` | — | A0 |
| B-8 | Externe Backupkopie | Deployment | `open` | — | A0 |

## C — Netzwerk und Zugriff

| ID | Kriterium | Klasse | Status | Nachweis | Autorität |
| --- | --- | --- | --- | --- | --- |
| C-1 | Bestehendes VPN | Deployment | `open` | HDI A5 — Profil festgelegt, Technologie offen | A0 |
| C-2 | Tailscale oder WireGuard | Deployment | `open` | HDI A5 — Auswahl im Deployment-Readiness-Schritt | A0 |
| C-3 | DNS | Conditional | `open` | Funktion nicht aktiviert | A0 |
| C-4 | Reverse Proxy | Conditional | `open` | Funktion nicht aktiviert | A0 |
| C-5 | Erlaubte ausgehende Verbindungen | Deployment | `open` | Grundsatz „keine öffentliche Freigabe" akzeptiert (D-023); Allowlist offen | A0 |
| C-6 | Mobile Zugriffsmethode | Deployment | `open` | HDI A5 — über privates Netz, Methode offen | A0 |

## D — Datenbestand

| ID | Kriterium | Klasse | Status | Nachweis | Autorität |
| --- | --- | --- | --- | --- | --- |
| D-1 | Gewünschte Quellen | **Core** | `answered` | HDI A3 — Markdown, Git, Chat-Handoffs, Obsidian-Vault als Markdown | A0 |
| D-2 | Größenordnung | Deployment | `open` | bewusst nicht erhoben, keine Dateiinventur | A0 |
| D-3 | Dateiformate | **Core** | `answered` | HDI A3 — Markdown zuerst; PDF/Office später über Quarantäne | A0 |
| D-4 | Datenklassen zugeordnet | **Core** | `accepted` | HDI A4 — Profilebene entschieden | A0 |
| D-5 | Ausgeschlossene Daten | **Core** | `accepted` | HDI A4 — `excluded-from-ai` von Anfang an im Modell, Sperrwirkung mit Testdaten prüfen | A0 |
| D-6 | Personenbezogene Daten | Conditional | `not-applicable` | HDI A4 — nicht im Pilot; spätere Aufnahme erfordert vorherige Prüfung | A0 |
| D-7 | Vertrauliche Informationen | Conditional | `not-applicable` | HDI A4 — `confidential` nicht im Pilot, Architektur muss die Klasse unterstützen | A0 |
| D-8 | **Secret-Verfahren im Schadensfall** | **Core** | **`open`** | Verbot bestätigt, **Ablauf nicht** | A0 |

## E — Claude und Repositories

| ID | Kriterium | Klasse | Status | Nachweis | Autorität |
| --- | --- | --- | --- | --- | --- |
| E-1 | Aktuelle Claude-Desktop-Nutzung | Deployment | `open` | — | A0 |
| E-2 | Erlaubte Repository-Zugriffe | **Core** | **`open`** | — | A0 |
| E-3 | GitHub-Zugriffe | **Core** | **`open`** | — | A0 |
| E-4 | Berechtigungsstufen je Bereich | **Core** | **`open`** | — | A0 |
| E-5 | Freigabeverfahren | **Core** | **`open`** | — | A0 |

## F — Architektur

| ID | Kriterium | Klasse | Status | Nachweis | Autorität |
| --- | --- | --- | --- | --- | --- |
| F-1 | VM als Referenzbetrieb | **Core** | **`accepted`** | HDI A1 — dedizierte Linux-VM auf Proxmox (D-015) | A0 |
| F-2 | Docker Compose als Pilotlaufzeit | **Core** | **`accepted`** | HDI A1 — bevorzugte Laufzeit innerhalb der VM (D-016) | A0 |
| F-3 | Trennung canonical / derived als ADR | **Core** | `open` | Prinzip dokumentiert, ADR fehlt | A1 |
| F-4 | Backup- und Restore-Zielwerte | Deployment | `open` | — | A0 |
| F-5 | Deployment-Neutralität | **Core** | **`accepted`** | HDI A1 — weitere Profile bleiben dokumentierbar (D-017) | A0 |
| F-6 | UI- und Wiki-Gates | **Core** | **`accepted`** | HDI A6 — Web-UI erst nach Index/Suche/Retrieval/Benchmark; Wiki nach Retrieval-Pilot (D-024, D-025) | A0 |

## G — Benchmark

| ID | Kriterium | Klasse | Status | Nachweis | Autorität |
| --- | --- | --- | --- | --- | --- |
| G-1 | Mindestens 30 Benchmarkfragen | **Core** | `open` | — | A2 |
| G-2 | Kategorien definiert | **Core** | `open` | — | A2 |
| G-3 | Erfolgsmetriken definiert | **Core** | `open` | — | A2 |
| G-4 | Baseline-Verfahren definiert | **Core** | `open` | — | A2 |
| G-5 | Datenschutzfälle enthalten | **Core** | `open` | mindestens 3 Fragen | A2 |
| G-6 | Konfliktfälle enthalten | **Core** | `open` | mindestens 3 Fragen | A2 |

### Vorgaben aus den Quellen

**Baseline-Verfahren** (Bauanleitung, Seite 3): Dieselbe Frage in zwei frischen
Sessions — einmal ohne System, einmal mit Index, Suche und Regeln. Verglichen
werden Tokenverbrauch, Zeit und Kontextfüllstand.

**Erfolgsmetriken** (Projektübergabe §16): derselbe Wissensstand von mehreren
Geräten · Baselinefragen korrekt beantwortet · deutlich weniger Dateien
geöffnet · deutlich weniger Kontext übertragen · Antwortqualität sinkt nicht ·
Quellen und Revisionen nachvollziehbar · Konflikte nicht automatisch aufgelöst ·
Backups und Restore getestet · kein Proxmox-Lock-in · generischer Linux-Betrieb
plausibel dokumentierbar.

---

## Sichere Standardwerte

Architekturdefaults, die unabhängig von der konkreten Installation gelten. Sie
sind **keine Behauptungen über die reale Infrastruktur**.

| # | Standardwert |
| --- | --- |
| 1 | Single-User-Betrieb als Einstieg |
| 2 | Privater Zugriff |
| 3 | Keine öffentliche Dienstfreigabe |
| 4 | Keine Secrets in Wissensbestand, Index oder Context Packs |
| 5 | **Übertragung an externe KI standardmäßig verweigert**, bis eine Datenklasse sie erlaubt |
| 6 | Trennung von canonical und derived |
| 7 | Keine automatische Konfliktauflösung |
| 8 | Keine automatischen Commits oder Pushes |
| 9 | Keine Obsidian-Synchronisation als Standard |
| 10 | Backup muss vor produktivem Betrieb eingerichtet **und getestet** sein |
| 11 | Optionale Funktionen bleiben deaktiviert, bis sie bewusst gewählt werden |

Standardwert 5 ist die schärfste Regel: Der Normalzustand ist **Verweigerung**,
nicht Freigabe.

---

## Abschlussregel

**G0 ist nur bestanden, wenn alle fünf Bedingungen erfüllt sind:**

1. **Alle Core-Required-Kriterien sind `accepted`.**
2. **Keine kritische Datenschutzfrage ist offen** — D-4, D-5, D-8 sind
   `accepted`. D-6 und D-7 sind `not-applicable`, solange die Datenarten nicht
   im Pilot vorkommen.
3. **Keine kritische Betriebsfrage des allgemeinen Scopes ist offen** — F-1,
   F-2, F-3, F-5, F-6 sind `accepted`.
4. **Ein messbarer Benchmarkplan existiert** — G-1 bis G-6 sind `accepted`.
5. **Der Human Maintainer gibt G0 ausdrücklich frei.**

Bedingung 5 ist eigenständig. Kein Implementation Agent und kein automatisches
Verfahren stellt das Bestehen fest.

**Deployment-Required-Kriterien blockieren G0 nicht.** Sie blockieren die
spätere Installation und werden im Deployment-Readiness-Gate geprüft.

**Conditional-Kriterien blockieren nur bei aktivierter Funktion.** Derzeit ist
keine der sechs bedingten Funktionen für den Pilot aktiviert.

---

## Aktueller Stand

### Gesamtzahlen

> **Korrektur.** Die in CBP-WP-002 berichteten Summen waren fehlerhaft addiert.
> Die Kriterien selbst waren vollständig; nur die Summenzeilen stimmten nicht.

| Kennzahl | Falsch berichtet | **Korrekt** |
| --- | --- | --- |
| G0-Kriterien gesamt | 41 | **47** |
| Blockierend im bisherigen Modell | 39 | **45** |
| P0-Fragen | 35 | **38** |
| Fragen gesamt | 55 | **56** |

### Verteilung nach Klassen

| Klasse | Anzahl | Blockiert G0 |
| --- | --- | --- |
| **Core Required** | **25** | **ja** |
| Deployment Required | 16 | nein |
| Conditional | 6 | nur bei aktivierter Funktion |
| **Summe** | **47** | |

### Blocker im neuen Modell

| Kennzahl | Wert |
| --- | --- |
| Blockierend, bisheriges Modell | 45 |
| **Blockierend, dreistufiges Modell** | **25** |
| davon `accepted` | **8** |
| davon `answered` | 4 |
| davon `open` | **13** |
| davon `blocked` | 0 |
| **Noch nicht `accepted` (verbleibende Blocker)** | **17** |

Aktive Conditional-Blocker: **0** — keine bedingte Funktion ist im Pilotumfang
aktiviert.

Die acht `accepted`-Kriterien: A-4, A-5, D-4, D-5, F-1, F-2, F-5, F-6.
Die vier `answered`-Kriterien: A-1, A-2, D-1, D-3.

### Die 13 offenen Core-Required-Kriterien

| ID | Kriterium |
| --- | --- |
| A-8 | Explizite Nicht-Ziele, einschließlich Repository-Sichtbarkeit |
| D-8 | Secret-Verfahren im Schadensfall |
| E-2 | Erlaubte Repository-Zugriffe |
| E-3 | GitHub-Zugriffe |
| E-4 | Berechtigungsstufen je Bereich |
| E-5 | Freigabeverfahren |
| F-3 | Trennung canonical / derived als ADR |
| G-1 … G-6 | Benchmarkplan, sechs Kriterien |

Das sind 13 Kriterien: A-8, D-8, E-2, E-3, E-4, E-5, F-3 und G-1 bis G-6.

Zusätzlich vier `answered`, die noch in `accepted` überführt werden müssen:
A-1, A-2, D-1, D-3. Zusammen **17 verbleibende Blocker**.

**Gate-Status: NOT PASSED.**

## Pflege

Ein Kriterium wechselt den Status nur im Rahmen eines freigegebenen Work
Packages und nur mit hinterlegtem Nachweis. Der Wechsel nach `accepted`
erfordert die Autorität aus der Spalte „Autorität". Ein Implementation Agent
setzt kein Kriterium eigenmächtig auf `accepted`.

Nachweis „HDI" verweist auf
[HUMAN_DISCOVERY_INPUT.md](HUMAN_DISCOVERY_INPUT.md).
