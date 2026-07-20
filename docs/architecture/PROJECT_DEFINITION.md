# Project Definition — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Status dieses Dokuments | Entwurf zur Scope-Lock-Prüfung an Gate G0 |
| Überarbeitet in | CBP-WP-002 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

## Definition

Core Brain Pilot ist ein **serverzentriertes und portables KI-Wissens- und
Arbeitssystem**.

Ziel ist, Claude und anderen Implementation Agents nur die **kleinste
ausreichende Menge** relevanter, aktueller, autoritativer und
datenschutzrechtlich erlaubter Informationen bereitzustellen.

## Das Ausgangsproblem

Das Ziel ergibt sich aus einem konkreten Problem, nicht aus einem
Architekturideal.

Der Human Maintainer arbeitet mit mehreren Core-Projekten und Claude Code. Der
aktuelle Zustand verursacht zu hohen Token- und Kontextverbrauch durch:

- umfangreiche NDF-Prompts,
- wiederholtes Laden stabiler Projektinformationen,
- Durchsuchen vieler Dateien,
- lange Projektchat-Verläufe,
- wiederholte Governance-Texte,
- fehlende kompakte Wiederaufnahme nach einer Session,
- verteiltes Wissen über Repositories, Chats und Dokumente.

In der Praxis kann das Claude-Nutzungslimit bereits nach wenigen umfangreichen
Prompts erreicht sein. Mehrstündige Unterbrechungen sind für einen produktiven
Projektablauf nicht akzeptabel.

**Primäres Produktziel:**

> Claude soll mit möglichst wenig Kontext genau die Informationen erhalten, die
> für den aktuellen Arbeitsschritt erforderlich sind.

> **Abgrenzung.** Das System soll **keine Nutzungslimits umgehen.** Es soll den
> vorhandenen Kontext und das verfügbare Kontingent wesentlich effizienter
> nutzen.

Ein analysiertes Praxisbeispiel zeigt, dass der größte Tokenverbrauch nicht
durch die eigentliche Frage entstand, sondern durch wiederholte und ungezielte
Suchvorgänge.

*Quelle: Projektübergabe §1, §2. Ergänzt in CBP-WP-002 als F-01.*

## Zielsetzung im Detail

„Kleinste ausreichende Menge" trägt vier gleichrangige Filterdimensionen. Ein
Ergebnis muss **alle vier** erfüllen:

| Dimension | Bedeutung |
| --- | --- |
| Relevanz | Bezug zur konkreten Aufgabe |
| Aktualität | nicht veraltet, nicht superseded |
| Autorität | A0–A6-Rang ausreichend für die Fragestellung |
| Datenschutz | Datenklasse für den Zielkontext freigegeben |

Ein Treffer, der nur drei Dimensionen erfüllt, wird nicht ausgeliefert.

## Plattform und Portabilität

**Proxmox** ist die **erste Referenzplattform**, ausdrücklich **nicht die
Produktgrenze**. Der Referenzbetrieb ist eine **dedizierte Linux-VM**.

### Fünf Referenzprofile

| Profil | Betriebsart | Status |
| --- | --- | --- |
| **A** | Proxmox — eigene VM, getrennte System- und Datendisk, Backup über Proxmox plus externe Sicherung; LXC optional später bei erfüllten Sicherheitsanforderungen | erste Referenz |
| **B** | Allgemeine Linux-VM (Debian, Ubuntu Server, andere) — **keine Proxmox-spezifischen APIs** | generischer Referenzbetrieb |
| **C** | Physischer Linux-Server oder Mini-PC, für Self-Hoster ohne Hypervisor | vorgesehen |
| **D** | Containerbetrieb: Docker Compose, Podman Compose, vergleichbare OCI-Umgebungen | optional nach erfolgreicher VM-Referenz |
| **E** | Lokale Einzelplatzinstallation, mit Einschränkungen bei Mehrgerätezugriff, Verfügbarkeit und zentralen Backups | Einstiegsmöglichkeit |

> **Zu Docker Compose.** Containerisierung ist **kein Pflichtziel der ersten
> Phase**, muss aber architektonisch möglich bleiben. Docker Compose ist eine
> vorgesehene, **noch nicht implementierte** Anwendungslaufzeit innerhalb der
> dedizierten Linux-VM.
>
> *Abgeschwächt in CBP-WP-002 als Ü-02 — die vorherige Fassung bezeichnete
> Compose als „bevorzugte" Laufzeit.*

### Nicht verpflichtend in der ersten Phase

Kubernetes · Cloud-native Plattform · Hochverfügbarkeitscluster ·
Multi-Tenant-SaaS · proprietäre Cloudabhängigkeit · Windows als
Serverbetriebssystem · macOS als Serverplattform.

*Quelle: Projektübergabe §4. Ergänzt in CBP-WP-002 als F-05.*

Zum Zeitpunkt dieses Dokuments ist **nichts davon installiert oder
implementiert**.

## Nutzungskontext

- Private Nutzung durch einen Human Maintainer
- Mehrgeräte-Nutzung einschließlich mobiler Zugriffe
- Kein Mehrmandantenbetrieb **in Phase 0**

> **Präzisierung.** „Keine öffentliche Bereitstellung" gilt für Phase 0, nicht
> als Produkteigenschaft. Projektübergabe §13 verlangt, dass die Architektur
> **von Anfang an öffentlich dokumentierbar** bleibt; §15 Phase 7 hält die
> öffentliche Entscheidung ausdrücklich offen.
>
> *Präzisiert in CBP-WP-002 als Ü-03.*

## Abgrenzung

Core Brain Pilot ist **nicht**:

- ein allgemeiner Dokumentenspeicher,
- ein Ersatz für die Git-Historie kuratierter Inhalte,
- ein autonom handelnder Agent — jede kuratierende Entscheidung bleibt
  menschlich kontrolliert,
- ein Weg, Nutzungslimits zu umgehen.

Öffentliches Branding und eine öffentliche Produktpositionierung sind in
Phase 0 gesperrt.

## Kanonisch vs. abgeleitet

| Klasse | Beispiele | Eigenschaft |
| --- | --- | --- |
| Kanonisch | Freigegebene Markdown-Quellen, Projektentscheidungen, Handoffs, dokumentierte Statusinformationen, manuell bestätigte Wiki-Inhalte, Konfigurationen und Regeln | Einzige Wahrheitsquelle, versioniert in Git |
| Abgeleitet | Suchindex, Embeddings, Cache, Graphdaten, automatisch erzeugte Kataloge, Visualisierungen, temporäre Retrievalergebnisse | Reproduzierbar, nie autoritativ |

**Invariante:**

> Der Verlust eines Indexes oder einer Oberfläche darf nicht zum Verlust des
> Wissens führen.

*Quelle: Projektübergabe §5.*

## Backup- und Wiederherstellungsmodell

Mindestens vier Stufen:

```text
1. Git-Historie für kuratierte Markdown-Inhalte
2. regelmäßige Sicherung der Datendisk
3. Proxmox- oder VM-Backup
4. zusätzliche Kopie außerhalb des Proxmox-Hosts
```

Abgeleitete Indizes müssen reproduzierbar sein und benötigen nicht denselben
Schutz wie kanonische Daten.

**Vor größeren Reorganisationen, Ingest-Läufen, Synchronisationsänderungen und
Wiki-Migrationen ist ein überprüfter Wiederherstellungspunkt erforderlich.**
Überprüft heißt: die Wiederherstellung wurde tatsächlich getestet, nicht nur
die Sicherung angelegt.

*Quelle: Projektübergabe §12. Ergänzt in CBP-WP-002 als F-07.*

## Phasenmodell

| Phase | Inhalt | Status |
| --- | --- | --- |
| **Phase 0** | **Discovery und Scope Lock** — Nutzerfälle, Datenklassen, Geräte, mobile Anforderungen, Proxmox-Umgebung, Backupmöglichkeiten, Netzwerkzugang, Wissensquellen, Benchmarkfragen. Keine produktive Installation | **laufend** |
| Phase 1 | Proxmox-Referenzumgebung — dedizierte VM, Benutzer- und Rechtekonzept, Netzwerkzugriff, SSH, persistente Terminalsitzung, browserbasierter Zugriff, Backup-Grundlage | nicht begonnen |
| Phase 2 | Wissensfundament — Verzeichnisstruktur, Source Authority, Index, Current State, erste kontrollierte Quellen, Git-Versionierung | nicht begonnen |
| Phase 3 | Retrieval-Pilot — lokale Suchlösung, Collections, Brain-First-Regeln, Context Budgets, Quellenreferenzen, Benchmark gegen den bisherigen Ablauf | nicht begonnen |
| Phase 4 | Mehrgeräte- und Mobile-Pilot — mindestens zwei PCs, mindestens ein Mobilgerät, derselbe zentrale Stand, Session-Handoff, Zugriffskontrolle | nicht begonnen |
| Phase 5 | Wiki-Pilot — begrenzter Themenbereich, keine Vollbestandsmigration, Konfliktkandidaten, Human Review, Auditlog | nicht begonnen |
| Phase 6 | Portabilität — generische Linux-Installationsanleitung, Konfigurationsmodell, Proxmox-Guide, Containerprofil-Prüfung, Export- und Restore-Test | nicht begonnen |
| Phase 7 | Öffentliche Entscheidung — internal only, Open-Source-Referenzimplementierung, wiederverwendbares Framework, Integration in bestehendes Core-Projekt, eigenes öffentliches Produkt oder no-go | nicht begonnen |

**Keine automatische Entscheidung zugunsten eines neuen öffentlichen
Produkts.**

*Quelle: Projektübergabe §15. Ergänzt in CBP-WP-002 als F-08.*

## Leitprinzip

> Proxmox ist die erste Referenzplattform, nicht die Produktgrenze. Der
> Wissensbestand bleibt portabel, der Index bleibt reproduzierbar, Claude liest
> nur das Nötige und der Mensch entscheidet, was gilt.

*Quelle: Projektübergabe, Leitprinzip.*

## Offene Punkte für Gate G0

Der Scope ist **nicht** gelockt.

- [G0_SCOPE_LOCK_CRITERIA.md](../discovery/G0_SCOPE_LOCK_CRITERIA.md) — 41 Kriterien
- [DISCOVERY_QUESTIONS.md](../discovery/DISCOVERY_QUESTIONS.md) — Fragebogen
- [OPEN_INFORMATION.md](../discovery/OPEN_INFORMATION.md) — fehlende Information
- [SOURCE_RECONCILIATION.md](../discovery/SOURCE_RECONCILIATION.md) — Quellenabgleich
