# Permission Model — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-004 |
| Autoritätsklasse | A2 |
| Status | **Modell dokumentiert, technisch nicht durchgesetzt** |
| Stand | 2026-07-20 |

Belegt G0-Kriterien **E-2, E-3, E-4, E-5**.

---

## Verbindliche Grundsätze

### 1. Default deny

Was nicht ausdrücklich erlaubt ist, ist verboten. Bei **unklarer Berechtigung
gilt `forbidden`** — nicht „vermutlich in Ordnung".

### 2. Promptregeln sind keine Sicherheitsgrenze

> Eine Berechtigung, die nur als Anweisung im Prompt steht, ist keine
> Berechtigung — sie ist eine Bitte.

Projektübergabe §10 verlangt technische Umsetzung. Ein Modell, das seine
eigenen Regeln durchsetzen soll, ist keine Zugriffskontrolle.

### 3. Technische Durchsetzungsebenen

| Ebene | Mechanismus | Wogegen sie schützt |
| --- | --- | --- |
| **OS-Dateirechte** | Benutzer, Gruppen, Modi; kanonischer Bestand für Dienstkonten nicht schreibbar | Direktzugriff unter Umgehung der Anwendung |
| **Container-User und Mount-Modi** | Nicht-privilegierte UIDs; kanonische Volumes lesend eingebunden, wo möglich; kein Root im Container | Ausbruch aus einer kompromittierten Komponente |
| **API-Autorisierung** | Rolle und Aktionsklasse je Endpunkt; serverseitig geprüft | Clients, die mehr verlangen als vorgesehen |
| **Netzwerkgrenzen** | Privates Netz oder VPN; getrennte Netze je Komponente; keine öffentliche Standardfreigabe | Zugriff von außen |
| **Approval-Zustände** | Schreibende Wirkung tritt erst nach dokumentierter Freigabe ein | Unbeabsichtigte und automatische Änderungen |

Eine Ebene allein genügt nicht. Sie greifen kumulativ.

### 4. Kein allgemeiner Schreibzugriff für Claude

Der Implementation Agent erhält **keinen** pauschalen Schreibzugriff auf alle
Repositories und **keine** pauschalen GitHub-Schreibrechte.

### 5. Indexer und Retrieval Service ohne kanonische Schreibrechte

Beide lesen kanonisch und schreiben ausschließlich abgeleitet.

### 6. Web-UI ohne administrative Hostrechte

Die Oberfläche ist eine austauschbare Darstellungsschicht, kein Adminwerkzeug.

### 7. Backup Storage ist für Web-UI, Suche und Claude nicht beschreibbar

Wer die Sicherung überschreiben kann, hat keine Sicherung.

### 8. Secret Store ist vom Wissensbestand getrennt

Getrennte Ablage, getrennte Rechte, getrennter Lebenszyklus. Secrets gehören
nie in kanonische Quellen, Git, Index, Embeddings, Wiki, Context Packs oder
Modellkontext.

### 9. `publish with approval` umfasst insbesondere

Push · Release · Veröffentlichung · **produktive Status- oder Gateänderung**.

Das Setzen eines Gates auf „bestanden" ist eine Veröffentlichungshandlung, kein
Verwaltungsschritt.

### 10. `excluded-from-ai` ist fail-closed gegenüber externer KI

| Erlaubt | Verboten |
| --- | --- |
| lokal klassifizieren | **an ein externes Modell übertragen** |
| gegebenenfalls lokal durchsuchen | in Context Packs aufnehmen |
| — | in Wiki-Entwürfe verdichten |

**Niemals** heißt: kein Debug-Modus, kein Testfall, keine Ausnahme.

### 11. Bei unklarer Berechtigung gilt `forbidden`

---

## Aktionsklassen

| Klasse | Bedeutung |
| --- | --- |
| `read` | Lesen erlaubt |
| `draft` | Entwurf erstellen erlaubt; keine Wirkung ohne Freigabe |
| `write with approval` | Schreiben nach ausdrücklicher, dokumentierter Freigabe |
| `publish with approval` | Veröffentlichen, pushen, releasen, Gate ändern — nach Freigabe |
| `forbidden` | Kein Zugriff; auch kein lesender |

`draft` ist die wichtigste Stufe für Agentenarbeit: sie erlaubt Produktivität
ohne Wirkung.

## Rollen

| Rolle | Charakter | Vertrauen |
| --- | --- | --- |
| **Human Maintainer** | Entscheidet, gibt frei, committet, pusht | höchstes |
| **Claude Desktop Implementation Agent** | Führt ein Work Package aus, erzeugt Entwürfe | niedrig |
| **Retrieval Service** | Filtert und liefert Kontext | mittel, technisch |
| **Indexer** | Baut abgeleitete Daten | mittel, technisch |
| **Web-UI** | Darstellung und Antragstellung | niedrig |
| **Read-only MCP/API Client** | Programmatischer Lesezugriff | niedrig |
| **Backup Service** | Sichert und stellt wieder her | mittel, privilegiert im Datenpfad |
| **Mobile Client** | Suchen, Lesen, kleine Freigaben | niedrig |
| **Späterer Reviewer** | Prüft und gibt frei, ohne Betriebsrechte | mittel |

## Ressourcen

`canonical sources` · `project decisions` · `handoffs` · `ingest quarantine` ·
`derived index` · `context packs` · `workspaces` · `audit logs` ·
`backup storage` · `secret store` · `git repository` · `github remote`

---

## Rollen-/Ressourcenmatrix

Legende: **R** `read` · **D** `draft` · **WA** `write with approval` ·
**PA** `publish with approval` · **✗** `forbidden`

| Ressource | Human Maintainer | Claude Agent | Retrieval Service | Indexer | Web-UI | MCP/API | Backup Service | Mobile Client | Reviewer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **canonical sources** | WA | **D** | R | R | R | R | R | R | **D** |
| **project decisions** | WA | **D** | R | R | R | R | R | R | **D** |
| **handoffs** | WA | **D** | R | R | R | R | R | R | R |
| **ingest quarantine** | WA | **D** | R | R | D | ✗ | R | ✗ | **D** |
| **derived index** | R | R | R | **WA*** | R | R | R | R | R |
| **context packs** | R | R | **WA*** | ✗ | R | R | ✗ | R | R |
| **workspaces** | WA | **WA*** | ✗ | ✗ | D | ✗ | R | ✗ | D |
| **audit logs** | R | ✗ | append | append | R | R | R | ✗ | R |
| **backup storage** | WA | **✗** | **✗** | **✗** | **✗** | **✗** | WA | ✗ | ✗ |
| **secret store** | WA | **✗** | ✗ | ✗ | **✗** | **✗** | R** | **✗** | **✗** |
| **git repository** | WA | **D** | ✗ | ✗ | ✗ | ✗ | R | ✗ | D |
| **github remote** | **PA** | **✗** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

**\*** Schreibrecht ausschließlich auf **abgeleitete** Daten beziehungsweise
den eigenen Arbeitsbereich — nie auf kanonisch.

**\*\*** Nur soweit für die Sicherung technisch unvermeidbar; bevorzugt wird
der Secret Store getrennt gesichert.

### Die harten Zellen

| Zelle | Regel |
| --- | --- |
| Claude → `github remote` | **`forbidden`.** Push ist ausschließlich Sache des Human Maintainers |
| Claude → `backup storage` | **`forbidden`** |
| Claude → `secret store` | **`forbidden`** — auch lesend |
| Claude → `canonical sources` | nur **`draft`**, niemals direktes Schreiben |
| Web-UI → `secret store`, `backup storage` | **`forbidden`** |
| Retrieval Service, Indexer → `canonical` | nur **`read`** |
| Mobile Client → `secret store` | **`forbidden`** |
| Alle außer Human Maintainer → `github remote` | **`forbidden`** |

## Datenklassen im Berechtigungsmodell

| Datenklasse | Indexierbar | Lokal durchsuchbar | An externe KI | In Context Packs | Mobil |
| --- | --- | --- | --- | --- | --- |
| `public` | ja | ja | ja | ja | ja |
| `internal` | ja | ja | ja | ja | ja |
| `confidential` | ja | ja | **nur begründet** | nur begründet | autorisiert |
| `secret` | **nie** | **nie** | **nie** | **nie** | **nie** |
| `excluded-from-ai` | **nie** | lokal möglich | **nie** | **nie** | **nie** |

`confidential` ist **nicht Teil des ersten Piloten** (D-020), muss aber
architektonisch getragen werden. `excluded-from-ai` ist **von Anfang an
technisch zu modellieren** und später mit Testdaten zu prüfen (D-021).

## Freigabeverfahren

Belegt G0-Kriterium **E-5**.

```text
1. Antrag        Agent, Web-UI oder Reviewer erzeugt einen Entwurf (draft)
                 → keine Wirkung
2. Einordnung    Review Queue erfasst Gegenstand, Ressource, Aktionsklasse,
                 Datenklasse, betroffene Kriterien
3. Prüfung       Human Maintainer prüft Inhalt, Herkunft und Autorität
4. Entscheidung  GO · GO WITH NOTES · REWORK · SPLIT · STOP
5. Wirkung       Erst jetzt wirkt der Schreibpfad; ausschließlich über den
                 Review-/Approval-Workflow
6. Protokoll     Audit-Eintrag mit Zeitpunkt, Rolle, Ressource, Entscheidung
                 — ohne Secrets, ohne geschützte Inhalte
```

Für `publish with approval` gilt zusätzlich: **eine gesonderte Freigabe je
Vorgang.** Eine Freigabe für einen Commit ist keine Freigabe für einen Push.

## G0-Zuordnung

| Kriterium | Beleg | Status |
| --- | --- | --- |
| **E-2** Erlaubte Repository-Zugriffe | Matrixzeile `git repository`; Claude nur `draft` | dokumentarisch erfüllt |
| **E-3** GitHub-Zugriffe | Matrixzeile `github remote`; nur Human Maintainer, `publish with approval` | dokumentarisch erfüllt |
| **E-4** Berechtigungsstufen je Bereich | Vollständige Rollen-/Ressourcenmatrix, 9 Rollen × 12 Ressourcen | dokumentarisch erfüllt |
| **E-5** Freigabeverfahren | Sechsstufiger Ablauf oben | dokumentarisch erfüllt |

> **Wichtige Einschränkung.** Erfüllt ist die **dokumentarische** Anforderung.
> Die **technische Durchsetzung** existiert nicht und darf **nicht** als
> `implemented` bezeichnet werden. Risiken R-25 und R-27 bleiben offen; ihr
> Nachweis gehört in spätere Gates, insbesondere den
> [DRC](../operations/DEPLOYMENT_READINESS_CHECK.md).

## Status

**Nicht durchgesetzt.** Es existiert keine Anwendung, kein Dienstkonto, keine
API und kein Container. Dieses Dokument beschreibt den Sollzustand.
