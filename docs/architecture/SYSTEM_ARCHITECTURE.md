# System Architecture — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-004 |
| Autoritätsklasse | A2 |
| Status | **Logische Zielarchitektur, nicht implementiert** |
| Stand | 2026-07-20 |

Dieses Dokument beschreibt eine **logische** Architektur. Es legt keine
konkrete Implementierung, keine Container, Ports, Datenbanknamen oder Produkte
fest. Nichts davon existiert.

---

## Grundsatz

> **Der Core ist deployment-neutral.** Alles Plattformspezifische liegt in
> austauschbaren Adaptern und in Deploymentprofilen — niemals im Kern.

Die Architektur ist ohne Proxmox vollständig funktionsfähig beschreibbar.
Proxmox ist Referenzprofil A, nicht Voraussetzung. Es existiert keine
Proxmox-API-Abhängigkeit.

## Schichtenübersicht

```text
┌──────────────────────────────────────────────────────────────────┐
│ 1  CLIENT LAYER                                                  │
│    Web-UI · Agent Client (Claude Desktop) · CLI · Mobile View    │
│    · spätere MCP-Clients                                         │
└───────────────────────────┬──────────────────────────────────────┘
                            │  nur über
┌───────────────────────────▼──────────────────────────────────────┐
│ 2  ACCESS LAYER          privates Netz / VPN · AuthN · AuthZ     │
│    keine öffentliche Standardfreigabe                            │
└───────────────────────────┬──────────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────────┐
│ 3  APPLICATION LAYER     Core API · Review- und Approval-Flow    │
│    Current State · Handoff-Zugriff · UI-Adapter                  │
└───────────────────────────┬──────────────────────────────────────┘
                            │
╔═══════════════════════════▼══════════════════════════════════════╗
║ 4  RETRIEVAL POLICY LAYER            ► ► ► TB-4 ◄ ◄ ◄            ║
║    Datenklasse · Quellenberechtigung · Autorität · Aktualität    ║
║    Verifikation · Context Budget · KI-Übertragungsregel · Trace  ║
║    FAIL-CLOSED. Einzige Stelle, an der Daten das System          ║
║    Richtung externes Modell verlassen dürfen.                    ║
╚═══════════════════════════╦══════════════════════════════════════╝
                            │
┌───────────────────────────▼──────────────────────────────────────┐
│ 5  CONTEXT LAYER         Context Pack Compiler · Quellenmanifest │
│    Abschnittsreferenzen · Pack Hash · Ablaufzeit · Ausschluss    │
└───────────────────────────┬──────────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────────┐
│ 6  SEARCH LAYER          deterministischer Quellenindex          │
│    Volltext-Adapter · semantischer Adapter · Hybrid/Rerank       │
│    keine feste Bindung an einen Anbieter                         │
└───────────────────────────┬──────────────────────────────────────┘
                            │ liest
┌───────────────────────────▼──────────────────────────────────────┐
│ 7  SOURCE & INGEST LAYER                                         │
│    Source Registry · Quarantäne · Klassifikation · Freigabe      │
│    ► KANONISCHER WISSENSBESTAND ◄ · Source Manifest · Tombstones │
└───────────┬──────────────────────────────────────────────────────┘
            │ Einbahnstraße (TB-3), nie zurück
┌───────────▼──────────────────────────────────────────────────────┐
│ 8  DERIVED DATA LAYER    Index · Embeddings · Cache · Packs      │
│    Audit-/Jobstatus · späterer Knowledge Graph                   │
│    vollständig reproduzierbar, nie autoritativ                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ 9  OPERATIONS LAYER      Backup · Restore · Rebuild · Healthcheck│
│    Vault Doctor · Evaluation & Regression                        │
│    quer zu allen Schichten                                       │
└──────────────────────────────────────────────────────────────────┘
```

**Zwei Richtungsregeln lesen sich aus dem Bild:**

1. Der kanonische Bestand (Schicht 7) speist die abgeleiteten Daten (Schicht 8).
   Rückfluss ist ausgeschlossen — Vertrauensgrenze TB-3.
2. Jeder Weg von Daten nach außen führt durch Schicht 4. Es gibt keinen
   Seitenpfad an der Policy vorbei.

---

## Schicht 1 — Client Layer

| Komponente | Verantwortung | Eingaben | Ausgaben | Vertrauen | Rechte | Klasse | Austauschbar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Web-UI | Darstellung, Review, Freigabe anstoßen | Nutzeraktionen | API-Aufrufe | niedrig | `read`, `draft` | — | **ja**, vollständig |
| Agent Client (Claude Desktop) | Arbeitsschritte ausführen, Context Packs konsumieren | Context Packs | Vorschläge, Entwürfe | niedrig | `read`, `draft` | — | ja |
| CLI | Betrieb, Rebuild, Diagnose | Kommandos | Statusausgaben | mittel | `read`, betriebliche Aktionen | — | ja |
| Mobile Read/Review View | Suchen, Lesen, Status, kleine Freigaben | Nutzeraktionen | API-Aufrufe | niedrig | `read`, begrenzt `write with approval` | — | ja |
| Spätere MCP-Clients | Programmatischer Lesezugriff | Anfragen | Antworten | niedrig | **`read` only** | — | ja |

**Kein Client schreibt direkt in den kanonischen Bestand.** Jeder Client geht
durch Schicht 2 und 3.

Die Web-UI beginnt erst nach funktionierendem Index, Suche,
Brain-First-Retrieval und Benchmark (D-024).

## Schicht 2 — Access Layer

| Komponente | Verantwortung | Eingaben | Ausgaben | Vertrauen | Rechte | Klasse | Austauschbar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Netzgrenze | Erreichbarkeit nur im privaten Netz oder VPN | Verbindungen | zugelassene Verbindungen | Grenze | — | — | ja, Technologie offen |
| Authentifizierung | Identität feststellen | Anmeldung | Sitzung | Grenze | — | — | ja |
| Autorisierung | Aktionsklasse je Rolle und Ressource durchsetzen | Sitzung, Anfrage | erlaubt/verweigert | **Durchsetzungspunkt** | — | — | ja |

**Keine öffentliche Standardfreigabe** (D-023). Kein Dienst dieser Architektur
ist ohne ausdrückliche Entscheidung aus dem Internet erreichbar.

Details in [../security/PERMISSION_MODEL.md](../security/PERMISSION_MODEL.md).

## Schicht 3 — Application Layer

| Komponente | Verantwortung | Eingaben | Ausgaben | Vertrauen | Rechte | Klasse | Austauschbar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Core API | Einziger Einstiegspunkt für alle Clients | autorisierte Anfragen | Antworten, Jobs | mittel | orchestriert, schreibt nicht selbst | — | **nein** — Kern |
| Review- und Approval-Workflow | Freigabezustände führen, Human Approval einholen | Entwürfe, Konflikte | Freigaben, Ablehnungen | mittel | **einziger autorisierter Schreibpfad nach kanonisch** | steuert kanonisch | nein |
| Current State / Handoff | Kompakten Projektzustand liefern | kanonische Quellen | Statusdokumente | mittel | `read` | kanonisch (lesend) | ja |
| UI-Adapter | UI-Technologie an die Core API binden | API | UI-Modelle | niedrig | `read`, `draft` | — | **ja** |

## Schicht 4 — Retrieval Policy Layer

Die schärfste Grenze des Systems. Entspricht TB-4 in
[TRUST_BOUNDARIES.md](TRUST_BOUNDARIES.md).

| Filter | Prüft | Verhalten bei Unklarheit |
| --- | --- | --- |
| Datenklasse | Ist die Klasse für das Ziel freigegeben? | **verweigern** |
| Quellenberechtigung | Darf die anfragende Rolle diese Collection sehen? | **verweigern** |
| Autoritätsklasse | Reicht der A0–A6-Rang für die Frage? | **verweigern** |
| Aktualität | Veraltet oder superseded? | **verweigern** |
| Verifikationsstatus | Bestätigt oder nur abgeleitet? | kennzeichnen |
| Context Budget | Innerhalb B0–B4? | kürzen, nicht überschreiten |
| Externe KI-Übertragungsregel | Darf dieser Inhalt ein externes Modell erreichen? | **verweigern** |
| Retrieval Trace | Was wurde betrachtet, gefiltert, verworfen — und warum? | immer erzeugen |

**Standardwert: Übertragung an externe KI wird verweigert, bis eine Datenklasse
sie ausdrücklich erlaubt.** `secret` und `excluded-from-ai` passieren diese
Schicht **nie** — fail-closed, ohne Ausnahme, ohne Debug-Modus.

Die Reihenfolge der Filter ist noch nicht festgelegt (OD-18).

## Schicht 5 — Context Layer

| Komponente | Verantwortung | Eingaben | Ausgaben | Vertrauen | Rechte | Klasse | Austauschbar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Context Pack Compiler | Reproduzierbares Kontextpaket bauen | gefilterte Treffer, Budget | Context Pack | mittel | `read` kanonisch, `write` derived | derived | ja |
| Quellenmanifest | Welche Quellen mit welcher Revision im Pack sind | Quellenmetadaten | Manifest | mittel | `read` | derived | nein |
| Abschnittsreferenzen | Zeigt auf Abschnitte, nicht ganze Dateien | Trefferpositionen | Referenzen | mittel | `read` | derived | nein |
| Pack Hash | Identität und Reproduzierbarkeit | Packinhalt | Hash | hoch | — | derived | nein |
| Ablaufzeit | Packs veralten, statt stillschweigend weiterzugelten | Zeitpunkt | Gültigkeit | mittel | — | derived | nein |
| Ausschlussgründe | Was wurde weggelassen und warum | Filterergebnisse | Begründungsliste | mittel | — | derived | nein |

**Reproduzierbarkeit:** Gleicher kanonischer Stand, gleiche Anfrage, gleiches
Budget ergeben denselben Pack Hash. Ohne diese Eigenschaft ist ein Agentenlauf
nicht nachvollziehbar.

Context Packs enthalten Nutzdaten und gehören **nicht** ins Repository.

## Schicht 6 — Search Layer

| Komponente | Verantwortung | Eingaben | Ausgaben | Vertrauen | Rechte | Klasse | Austauschbar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Deterministischer Quellenindex | Gleicher Input → gleicher Index | kanonische Quellen | Indexeinträge | mittel | `read` kanonisch, `write` derived | derived | nein (Vertrag), ja (Technik) |
| Volltextsuchadapter | Stichwortsuche | Anfrage | Treffer | niedrig | `read` derived | derived | **ja** |
| Semantischer Suchadapter | Bedeutungssuche, lokale Modelle | Anfrage | Treffer | niedrig | `read` derived | derived | **ja** |
| Hybrid-/Reranking-Adapter | Ergebnisse kombinieren und ordnen | Trefferlisten | geordnete Liste | niedrig | `read` derived | derived | **ja** |

> **Keine feste Bindung an qmd** oder einen anderen Anbieter. qmd ist Kandidat
> mit Prüfvorbehalt (OD-25): Installations-, Plattform-, Lizenz-, Wartungs- und
> Sicherheitsprüfung stehen aus.

Suchdienste laufen **lokal und selbst gehostet**. Sie dürfen den kanonischen
Bestand **nicht** verändern.

## Schicht 7 — Source and Ingest Layer

| Komponente | Verantwortung | Eingaben | Ausgaben | Vertrauen | Rechte | Klasse | Austauschbar |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Source Registry | Welche Quellen existieren, mit ID, Hash, Klasse, Owner | Quellenmeldungen | Registereinträge | mittel | `write` kanonisch **nach Freigabe** | **kanonisch** | nein |
| Quarantäne | Ungeprüftes Material aufnehmen (TB-1) | externe Quellen | Kandidaten | **niedrig** | `write` quarantäne | Quarantäne | nein |
| Klassifikation | Datenklasse und Autoritätsklasse zuweisen | Kandidaten | klassifizierte Kandidaten | mittel | `write` quarantäne | Quarantäne | nein |
| Freigabe (Promotion) | Menschlicher Kurationsschritt (TB-2) | klassifizierte Kandidaten | kanonische Inhalte | **hoch** | **`write with approval`** | kanonisch | nein |
| Kanonischer Wissensbestand | Einzige Wahrheitsquelle | freigegebene Inhalte | Quellen | **hoch** | nur über Freigabepfad | **kanonisch** | nein |
| Source Manifest | Bestandsverzeichnis mit Revisionen | kanonischer Bestand | Manifest | hoch | `read` | kanonisch | nein |
| Tombstones | Löschungen nachvollziehbar halten | Löschvorgänge | Grabsteine | hoch | `write with approval` | kanonisch | nein |

**Kein automatischer Pfad von Quarantäne nach kanonisch.** PDF- und
Office-Dokumente gelangen ausschließlich über diesen Weg (D-019).

## Schicht 8 — Derived Data Layer

Alles hier ist **reproduzierbar und niemals autoritativ**.

| Komponente | Verantwortung | Klasse | Bei Verlust |
| --- | --- | --- | --- |
| Suchindex | Auffindbarkeit | derived | Rebuild |
| Embeddings | Bedeutungssuche | derived | Rebuild |
| Cache | Beschleunigung | derived | Rebuild oder Verzicht |
| Temporäre Context Packs | Agentenkontext | derived | Neu erzeugen |
| Audit- und Jobstatus | Nachvollziehbarkeit von Läufen | derived | Historie geht verloren, kein Wissensverlust |
| Späterer Knowledge Graph | Übersicht | derived | Rebuild; **nicht Pilotumfang** (D-025) |

**Invariante:** Der vollständige Verlust dieser Schicht verursacht **keinen
Wissensverlust**.

## Schicht 9 — Operations Layer

| Komponente | Verantwortung | Klasse | Bemerkung |
| --- | --- | --- | --- |
| Backup | Kanonischen Bestand sichern | — | Vier Stufen; Ziel außerhalb des Hosts |
| Restore | Kanonischen Bestand wiederherstellen | — | **Muss getestet sein**, nicht nur eingerichtet |
| Rebuild | Derived aus Canonical neu erzeugen | — | Siehe Rebuild-Vertrag unten |
| Healthcheck | Betriebsbereitschaft prüfen | — | — |
| Vault Doctor | Bestandsintegrität prüfen | — | Klassen, Waisen, Hashes, Widersprüche |
| Evaluation und Regression | Retrieval-Qualität messen | — | Benchmark, noch nicht definiert |

Backup Storage ist für Web-UI, Suche und Agenten **nicht beschreibbar**.

---

## Kanonisch und abgeleitet

### Kanonisch

- Freigegebene Markdown-Quellen
- Projektentscheidungen
- Handoffs
- Bestätigte Statusinformationen
- Konfigurationen und Regeln
- Manuell bestätigte Wiki-Inhalte, falls später eingeführt

Kanonische Inhalte liegen in **offenen, exportierbaren Formaten**, primär
Markdown unter Git.

### Abgeleitet

- Kataloge
- Suchindex
- Embeddings
- Cache
- Graphdaten
- Automatisch erzeugte Wiki-Entwürfe
- Retrieval-Traces
- Temporäre Context Packs
- Visualisierungen

### Rebuild-Vertrag

Ein Rebuild erzeugt die abgeleitete Schicht vollständig neu.

**Benötigte Inputs**

| Input | Zweck |
| --- | --- |
| Kanonischer Bestand mit Revision | Quelle der Wahrheit |
| Source Manifest | Welche Quellen zählen dazu |
| Klassifikationszuordnung | Datenklasse und Autoritätsklasse je Quelle |
| Tombstone-Liste | Was ist gelöscht oder gesperrt |
| Indexkonfiguration mit Version | Reproduzierbarkeit der Segmentierung |
| Embedding-Modellkennung mit Version | Vergleichbarkeit der Vektoren |
| Ausschlussregeln | `secret` und `excluded-from-ai` |

**Festzuhaltende Versionen**

Kanonische Revision · Indexer-Version · Embedding-Modell und -Version ·
Konfigurationsversion · Zeitpunkt des Laufs. Ohne diese fünf Angaben ist ein
Rebuild nicht vergleichbar.

**Verifikation eines vollständigen Rebuilds**

1. Zahl der indexierten Quellen entspricht dem Source Manifest abzüglich
   Ausschlüssen und Tombstones.
2. Keine Quelle der Klasse `secret` oder `excluded-from-ai` ist im Index.
3. Stichprobe kanonischer Dokumente ist über Volltext und Semantik auffindbar.
4. Der Benchmark läuft ohne Regression gegen den vorherigen Stand.
5. Zwei aufeinanderfolgende Rebuilds bei unverändertem Input erzeugen denselben
   Indexzustand (Determinismus).

**Entfernen gelöschter oder gesperrter Quellen**

1. Quelle erhält im kanonischen Bestand einen Tombstone.
2. Inkrementeller Lauf entfernt alle zugehörigen Indexeinträge und Embeddings.
3. Cache-Einträge mit Bezug zur Quelle werden invalidiert.
4. Context Packs, die die Quelle enthalten, verfallen.
5. Der Vault Doctor prüft, dass keine Waisen zurückbleiben.

Eine reine Löschung in der Quelle ohne diesen Weg gilt **nicht** als entfernt.

Dieser Abschnitt belegt G0-Kriterium **F-3**.

---

## Was diese Architektur bewusst nicht festlegt

- Programmiersprache, Framework, Datenbank
- Konkrete Suchmaschine oder Embedding-Modell
- Container-, Port- oder Volumennamen
- Web-UI-Technologie
- VPN-Produkt

Diese Festlegungen gehören in Adapter und Deploymentprofile, nicht in den Kern.
Siehe [DEPLOYMENT_PROFILES.md](DEPLOYMENT_PROFILES.md) und
[COMPONENT_MODEL.md](COMPONENT_MODEL.md).

## Status

**Nicht implementiert.** Keine Komponente dieser Architektur existiert. Phase 0
erlaubt ausschließlich Dokumentation.
