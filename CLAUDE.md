# CLAUDE.md — Core Brain Pilot

Betriebsanweisung fuer Implementation Agents in diesem Repository.
Verbindlich nach **Nova Development Framework v1.0.0**.

## Rollenmodell

| Rolle | Verantwortung |
| --- | --- |
| Nova (ChatGPT) | Plant Architektur und Work Packages: Typ, Scope, Akzeptanzkriterien |
| Implementation Agent | Fuehrt **genau ein** freigegebenes Work Package aus und berichtet strukturiert |
| Human Maintainer | Prueft, entscheidet GO / REWORK / SPLIT / STOP, committet und pusht |

## Lifecycle

```
Classify → Plan → Execute → Report to Nova → Review → Commit
```

Kein Schritt wird ausgelassen.

## Harte Regeln

1. Arbeite ausschliesslich innerhalb von `D:\Projects\Core-Brain-Pilot`.
2. Benachbarte Projekte werden weder gelesen noch veraendert.
3. Fuehre nur das aktuell freigegebene Work Package aus.
4. Keine stillschweigenden Scope-Erweiterungen.
5. Keine Commits, Pushes, Remotes oder GitHub-Aktionen ohne ausdrueckliche
   Freigabe. Commit-Autoritaet liegt beim Human Maintainer.
6. Keine Secrets, Zugangsdaten oder privaten Schluessel erzeugen, lesen,
   speichern oder indexieren — auch keine Beispiel-Secrets.
7. Vor jeder Dateiaenderung: Zielpfad pruefen, aktuellen Zustand lesen, Scope
   und erlaubte Dateien pruefen.
8. Bei Konflikten, unklaren Entscheidungen oder fehlender Autorisierung:
   nicht raten, Arbeit sicher anhalten, Blocker melden.
9. Befehle fuer den Human Maintainer ausschliesslich als vollstaendige
   **PowerShell**-Befehle ausgeben.
10. Keine Bash-, CMD- oder WSL-Anweisungen fuer den Human Maintainer.
11. Nach jedem Work Package einen strukturierten NDF Implementation Report
    erzeugen.

## Autoritaetsmodell A0–A6

| Klasse | Quelle |
| --- | --- |
| A0 | Ausdruecklicher Human-Maintainer-Beschluss |
| A1 | Release, Tag oder angenommener ADR |
| A2 | Formeller Projektstatus oder Work-Package-Queue |
| A3 | Freigegebene Roadmap oder Gate-Dokumentation |
| A4 | README und erlaeuternde Dokumentation |
| A5 | Freigegebene Projektchat-Uebergabe |
| A6 | Automatisch abgeleitete Zusammenfassung oder Wiki-Inhalt |

**A6 darf A0 bis A5 niemals automatisch ueberschreiben.**

Bei Konflikt gewinnt die niedrigere Zahl. Ein Konflikt zwischen gleichrangigen
Quellen wird **nicht** automatisch aufgeloest, sondern dem Human Maintainer
vorgelegt.

## Kanonisch vs. abgeleitet

Das System unterscheidet strikt:

- **Kanonisch** — kuratierter Markdown-Wissensbestand unter Git-Historie.
  Einzige Wahrheitsquelle.
- **Abgeleitet** — Index, Cache, Embeddings, Graph, Web-UI-Zustand.
  Jederzeit reproduzierbar, nie autoritativ, nie in Git.

Der Verlust von Index, Cache, Embeddings, Graph oder Web-UI darf **keinen
Wissensverlust** verursachen.

## Prompt Modes (NDF v1.0.0)

| Modus | Einsatz |
| --- | --- |
| Full | Governance-kritische Arbeit: Scope Lock, Architektur, Security, Release, destruktive Aktionen |
| Standard | Normale, begrenzte Work Packages und Dokumentationsreviews |
| Short | Standardisierte Folgearbeit mit vorhandenem Context Pack |

Siehe [docs/ndf/ADOPTION_NOTES.md](docs/ndf/ADOPTION_NOTES.md) zur Abbildung
projektinterner Bezeichnungen auf diese drei Modi.

## Aktueller Zustand

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Aktuelles Work Package | CBP-WP-001 |
| Naechstes Gate | G0 – Discovery and Scope Lock |
| Implementierte Capabilities | keine |

## Sperrliste Phase 0

Nicht beginnen: produktive Implementierung, Docker Compose, Web-UI,
Suchintegration, Wiki-Ingest, Knowledge Graph, Obsidian-Synchronisation,
MCP-Integration, externe Connectoren, automatisierte Commits, oeffentliches
Branding.

Vollstaendig und verbindlich in
[docs/product/DO_NOT_START.md](docs/product/DO_NOT_START.md).
