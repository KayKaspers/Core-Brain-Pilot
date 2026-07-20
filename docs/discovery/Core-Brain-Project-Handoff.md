<!--
source type: project handoff
authority class: A5
approval status: approved
canonical status: canonical project source
original content preserved: yes
-->

> **Metadaten.** Quellentyp: Projektübergabe · Autoritätsklasse: **A5** ·
> Freigabestatus: freigegeben · Kanonischer Status: kanonische Projektquelle ·
> Originalinhalt unverändert erhalten: **ja**
>
> Ergänzt in CBP-WP-002. Unterhalb dieser Zeile wurde kein Zeichen des
> fachlichen Inhalts verändert, gekürzt oder umformuliert.

---

# Projektübergabe: Serverbasiertes, portables KI-Wissenssystem

Du bist Nova im neuen Projektchat für ein serverbasiertes KI-Wissens- und Arbeitssystem.

Der vorläufige interne Arbeitstitel lautet:

> **Core Brain Pilot**

Der Name ist noch nicht als öffentlicher Produktname beschlossen. Prüfe später einen neutralen, verständlichen und markenfähigen Namen. Beginne aber nicht mit Branding oder einer öffentlichen Produktpositionierung.

## 1. Projektursprung

Das Projekt basiert auf der Idee eines strukturierten Second Brains mit:

* zentralem Markdown-Wissensbestand,
* deterministischem Datei- und Quellenindex,
* lokaler Volltext- und Bedeutungssuche,
* Brain-First-Retrieval-Regeln,
* gezieltem Laden weniger relevanter Quellen,
* optionaler, KI-gepflegter Wiki-Schicht,
* menschlich kontrollierter Konfliktauflösung,
* optionaler späterer Benutzeroberfläche.

Die zugrunde liegende Bauanleitung empfiehlt folgende Reihenfolge:

```text
Datenbasis ordnen
→ INDEX.md erstellen
→ lokale Hybridsuche einrichten
→ Brain-First-Regeln definieren
→ gegen den bisherigen Ablauf testen
→ erst danach Wiki und Oberfläche prüfen
```

Das zentrale Ziel ist nicht eine optisch beeindruckende Graphansicht, sondern ein Wissenssystem, das Informationen schnell findet, Quellen nachvollziehbar macht und Widersprüche sichtbar werden lässt. Die Anleitung behandelt Ordnung, Index, Suche und Regelwerk ausdrücklich als Fundament; Wiki und Oberfläche sind spätere Ausbaustufen.

Das analysierte Praxisbeispiel berichtet, dass der größte Tokenverbrauch nicht durch die eigentliche Frage entstand, sondern durch wiederholte und ungezielte Suchvorgänge. Die Lösung bestand darin, zuerst einen kleinen Katalog und einen Suchindex zu verwenden und anschließend nur wenige relevante Quellenabschnitte an Claude zu übergeben.

## 2. Ausgangsproblem

Der Human Maintainer arbeitet mit mehreren Core-Projekten und Claude Code.

Der aktuelle Zustand verursacht zu hohen Token- und Kontextverbrauch:

* umfangreiche NDF-Prompts,
* wiederholtes Laden stabiler Projektinformationen,
* Durchsuchen vieler Dateien,
* lange Projektchat-Verläufe,
* wiederholte Governance-Texte,
* fehlende kompakte Wiederaufnahme nach einer Session,
* verteiltes Wissen über Repositories, Chats und Dokumente.

In der Praxis kann das Claude-Nutzungslimit bereits nach wenigen umfangreichen Prompts erreicht sein. Mehrstündige Unterbrechungen sind für einen produktiven Projektablauf nicht akzeptabel.

Das primäre Produktziel lautet daher:

> Claude soll mit möglichst wenig Kontext genau die Informationen erhalten, die für den aktuellen Arbeitsschritt erforderlich sind.

Das System soll nicht Nutzungslimits umgehen. Es soll den vorhandenen Kontext und das verfügbare Kontingent wesentlich effizienter nutzen.

## 3. Betriebsziel

Das System soll nicht ausschließlich lokal auf einem einzelnen PC laufen.

Die primäre Referenzumgebung des Human Maintainers ist:

> **Proxmox**

Der erste produktive Pilot soll deshalb bevorzugt auf einer eigenen VM oder einer vergleichbar isolierten Instanz auf dem Proxmox-Server betrieben werden.

Dadurch soll möglich werden:

* zentraler und einheitlicher Wissensstand,
* Zugriff von mehreren PCs,
* mobile Nutzung,
* Fortsetzung derselben Arbeitsumgebung auf verschiedenen Geräten,
* zentral gepflegte Suchindizes,
* zentrale Backups,
* kontrollierte Berechtigungen,
* einheitliche Claude-Code- und Tool-Konfiguration.

## 4. Deployment-Neutralität

Obwohl Proxmox die erste Referenzplattform ist, darf das Projekt technisch und dokumentarisch nicht an Proxmox gekoppelt werden.

Die öffentliche Lösung soll später mindestens folgende Betriebsarten unterstützen oder klar dokumentieren können:

### Referenzprofil A – Proxmox

* eigene VM,
* optional später LXC, sofern Sicherheits- und Kompatibilitätsanforderungen erfüllt sind,
* getrennte System- und Datendisk,
* Backup über Proxmox und zusätzliche externe Sicherung.

### Referenzprofil B – allgemeine Linux-VM

Beispielsweise:

* Debian,
* Ubuntu Server,
* andere geeignete Linux-Distributionen.

Die Anwendung darf keine Proxmox-spezifischen APIs benötigen.

### Referenzprofil C – physischer Linux-Server oder Mini-PC

Für Self-Hoster ohne Hypervisor.

### Referenzprofil D – Containerbetrieb

Optional nach erfolgreicher VM-Referenz:

* Docker Compose,
* Podman Compose,
* vergleichbare OCI-Umgebungen.

Containerisierung ist kein Pflichtziel für die erste Phase, muss aber architektonisch möglich bleiben.

### Referenzprofil E – lokale Einzelplatzinstallation

Als einfache Einstiegsmöglichkeit für Nutzer ohne Server.

Diese Variante kann Einschränkungen bei Mehrgerätezugriff, Verfügbarkeit und zentralen Backups besitzen.

### Nicht verpflichtend in der ersten Phase

* Kubernetes,
* Cloud-native Plattform,
* Hochverfügbarkeitscluster,
* Multi-Tenant-SaaS,
* proprietäre Cloudabhängigkeit,
* Windows als Serverbetriebssystem,
* macOS als Serverplattform.

## 5. Architekturgrundsatz

Die Architektur muss zwischen **kanonischen Daten** und **abgeleiteten Daten** unterscheiden.

### Kanonisch

* freigegebene Markdown-Quellen,
* Projektentscheidungen,
* Handoffs,
* dokumentierte Statusinformationen,
* manuell bestätigte Wiki-Inhalte,
* Konfigurationen und Regeln.

### Abgeleitet und reproduzierbar

* Suchindex,
* Embeddings,
* Cache,
* Graphdaten,
* automatisch erzeugte Kataloge,
* Visualisierungen,
* temporäre Retrievalergebnisse.

Verbindliche Invariante:

```text
Der Verlust eines Indexes oder einer Oberfläche darf nicht zum Verlust des Wissens führen.
```

## 6. Quellen- und Autoritätsmodell

Für Core reicht die Aussage „Markdown ist die einzige Wahrheit“ nicht aus.

Unterschiedliche Dokumente besitzen unterschiedliche Autorität.

Verwende mindestens folgende Autoritätsklassen:

```text
A0 – ausdrücklicher Human-Maintainer-Beschluss
A1 – Release, Tag oder angenommener ADR
A2 – formeller Projektstatus oder Work-Package-Queue
A3 – freigegebene Roadmap oder Gate-Dokumentation
A4 – README und erläuternde Dokumentation
A5 – freigegebene Projektchat-Übergabe
A6 – automatisch abgeleitete Zusammenfassung oder Wiki-Inhalt
```

Regel:

```text
Eine abgeleitete A6-Aussage darf keine Aussage aus A0 bis A5 automatisch überschreiben.
```

Jede abgeleitete Aussage soll mindestens enthalten:

* Quellpfad,
* Quellentyp,
* Revision oder Prüfzeitpunkt,
* Autoritätsklasse,
* Aktualitätsstatus,
* Verifikationsstatus,
* mögliche Konfliktreferenzen.

## 7. Brain-First-Retrieval

Das System soll eine verbindliche Suchleiter erhalten:

```text
1. Projekt- oder Wissensindex lesen.
2. Quellentyp und notwendige Autoritätsklasse bestimmen.
3. Aktuellen Status prüfen, falls die Frage zeitabhängig ist.
4. Wiki nur als abgeleitete Orientierung prüfen.
5. Suche auf relevante Collection oder Projektgrenze beschränken.
6. Kandidaten zunächst über Titel, Pfad, Metadaten und Trefferabschnitt prüfen.
7. Nur die kleinste ausreichende Zahl von Quellen öffnen.
8. Nur relevante Abschnitte lesen.
9. Fakten, Ableitungen, Empfehlungen und Unsicherheit trennen.
10. Quellen und Revisionen im Ergebnis nennen.
```

Keine blinden Vollscans ganzer Repositories oder Wissensbestände.

Die ursprüngliche Ein-Datei-Regel wird für Core erweitert:

```text
Normalfall: eine Quelle
erweiterter Fall: höchstens drei Quellen
größerer Fall: begründete Eskalation oder Aufteilung der Aufgabe
```

## 8. Context Budgets

Entwirf ein einfaches Budgetmodell:

```text
B0 – Micro
B1 – Lean
B2 – Standard
B3 – Extended
B4 – Exceptional
```

Für jede Stufe sind zu definieren:

* geeignete Aufgaben,
* maximaler Quellenumfang,
* erlaubte Kontextarten,
* erwartete Rückmeldelänge,
* Reviewtiefe,
* Eskalationsbedingungen.

`B4` darf kein normaler Arbeitsmodus werden.

Wenn eine Aufgabe regelmäßig B4 benötigt, soll geprüft werden, ob:

* der Scope zu groß ist,
* das Work Package geteilt werden muss,
* der Index unzureichend ist,
* Quellen zu monolithisch sind,
* unnötiger Kontext geladen wird.

## 9. Geplante Systemkomponenten

Prüfe und plane mindestens folgende Komponenten:

### Wissensbestand

* strukturierte Markdown-Verzeichnisse,
* Inbox,
* Projekte,
* Entscheidungen,
* Handoffs,
* Wissen,
* Archiv,
* abgeleitetes Wiki.

### Quellenindex

Ein deterministisch erzeugter Index mit:

* Projekt,
* Pfad,
* Titel,
* Beschreibung,
* Quellentyp,
* Autoritätsklasse,
* Revision,
* Themen,
* relevanten Gates,
* Aktualitätsstatus.

### Lokale Suche

Evaluation von qmd oder einer vergleichbaren lokalen Hybrid-Suche:

* Volltextsuche,
* semantische Suche,
* Hybrid-Retrieval,
* lokale Modelle,
* getrennte Collections,
* serverseitiger Betrieb,
* CLI- und gegebenenfalls MCP-Anbindung.

Keine Vorentscheidung zugunsten von qmd ohne Installations-, Plattform-, Lizenz-, Wartungs- und Sicherheitsprüfung.

### Claude-Code-Arbeitsumgebung

* zentral auf dem Server,
* nicht als Root,
* kontrollierte Datei- und Toolberechtigungen,
* kein allgemeiner Schreibzugriff auf alle Repositories,
* persistente Terminal-Sitzungen,
* Zugriff von mehreren Geräten.

### Remotezugriff

Bevorzugt über ein privates Netz beziehungsweise VPN-Modell.

Zu prüfen:

* Tailscale,
* bestehendes VPN,
* WireGuard,
* vergleichbare sichere Lösung.

Keine öffentliche Freigabe interner Dienste als Standard.

### Browserbasierte Arbeitsumgebung

Evaluation von:

* code-server,
* SSH plus `tmux`,
* VS-Code Remote,
* andere geeignete Zugänge.

### Mobile Nutzung

Ziel:

* Wissen suchen und lesen,
* aktuellen Projektstatus prüfen,
* Claude-Code-Sitzung fortsetzen,
* kleine Entscheidungen oder Freigaben vorbereiten.

Eine vollständig komfortable mobile Entwicklungsumgebung ist kein Pflichtziel der ersten Phase.

### Obsidian

Obsidian ist optional.

Prüfe getrennt:

* serverzentrierte Bearbeitung ohne Dateisynchronisation,
* native Obsidian-Nutzung auf mehreren Geräten,
* Self-hosted LiveSync,
* offizielles Obsidian Sync,
* andere Synchronisationsvarianten.

Keine produktive Synchronisationslösung einführen, bevor sie mit einem Testbestand auf Konflikte, Datenverlust und Backupfähigkeit geprüft wurde.

### Wiki-Schicht

Die KI darf:

* Wiki-Entwürfe erstellen,
* Quellen verdichten,
* Links vorschlagen,
* mögliche Widersprüche markieren.

Die KI darf nicht:

* autoritative Quellen automatisch verändern,
* Konflikte selbst entscheiden,
* abgeleitete Inhalte als verifiziert markieren,
* Projektstatus oder Gates ändern.

### Oberfläche und Graph

Nicht Teil der ersten Umsetzung.

Eine Oberfläche wird erst geplant, wenn:

* Index und Suche funktionieren,
* Tokenersparnis belegt ist,
* Mehrgerätezugriff funktioniert,
* der Alltagsnutzen bestätigt ist.

## 10. Sicherheitsmodell

Verbindliche Regeln:

* keine Ausführung als Root,
* kein Betrieb direkt auf dem Proxmox-Host,
* keine Proxmox-API-Berechtigungen,
* keine pauschalen GitHub-Schreibrechte,
* keine Secrets im Wissensbestand,
* keine privaten Schlüssel im Index,
* keine öffentliche Freigabe von qmd, Datenbanken oder internen APIs,
* keine automatische Konfliktauflösung,
* keine automatischen Commits oder Pushes in der ersten Phase,
* keine Berechtigungsumgehung,
* keine unkontrollierten Plugins oder MCP-Server.

Berechtigungen sollen technisch umgesetzt werden, nicht nur durch Promptregeln.

Unterscheide:

```text
read
draft
write with approval
publish with approval
forbidden
```

## 11. Datenschutz

Der Suchindex und lokale Suchmodelle sollen bevorzugt serverseitig und selbst gehostet betrieben werden.

Gleichzeitig gilt:

> Claude Code selbst verwendet keinen vollständig lokalen Sprachmodellbetrieb.

Nur ausgewählte Inhalte dürfen an das verwendete Claude-Modell übertragen werden.

Daher müssen Daten mindestens klassifiziert werden als:

```text
public
internal
confidential
secret
excluded-from-ai
```

Für jede Klasse ist festzulegen:

* darf indexiert werden,
* darf lokal durchsucht werden,
* darf an Claude übertragen werden,
* darf im Wiki zusammengefasst werden,
* darf mobil angezeigt werden.

## 12. Backup- und Wiederherstellungsmodell

Mindestens:

```text
1. Git-Historie für kuratierte Markdown-Inhalte
2. regelmäßige Sicherung der Datendisk
3. Proxmox- oder VM-Backup
4. zusätzliche Kopie außerhalb des Proxmox-Hosts
```

Abgeleitete Indizes müssen reproduzierbar sein und benötigen nicht denselben Schutz wie kanonische Daten.

Vor größeren:

* Reorganisationen,
* Ingest-Läufen,
* Synchronisationsänderungen,
* Wiki-Migrationen

ist ein überprüfter Wiederherstellungspunkt erforderlich.

## 13. Öffentliche Produktfähigkeit

Die erste Umsetzung ist ein interner Pilot.

Trotzdem soll die Architektur von Anfang an öffentlich dokumentierbar bleiben.

Das bedeutet:

* keine privaten Pfade oder Namen im öffentlichen Kern,
* Konfiguration statt hart codierter Infrastruktur,
* Proxmox nur als Deployment Guide,
* Linux-VM als generischer Referenzbetrieb,
* saubere Trennung von Core und Deployment-Adaptern,
* reproduzierbare Installation,
* dokumentierte Abhängigkeiten,
* offene und kompatible Dateiformate,
* exportierbare Daten,
* keine Bindung an eine einzelne Oberfläche,
* keine Bindung an einen einzelnen Suchanbieter,
* keine Bindung an einen einzelnen VPN-Anbieter.

Mögliche spätere Struktur:

```text
core/
deployments/
  proxmox/
  linux-vm/
  docker/
  local/
docs/
examples/
```

Die konkrete Repository-Struktur ist noch nicht freigegeben und muss im Projekt geplant werden.

## 14. NDF-Nutzung

Das Projekt soll NDF v1.0.0 als Prozessgrundlage verwenden.

Dabei gilt wegen des aktuellen Tokenproblems:

* kompakte Work Packages,
* Lean Mode bevorzugen,
* keine vollständige Wiederholung stabiler Governance,
* kleine Handoffs,
* Context Budgets,
* Quellenreferenzen statt Volltexte,
* maximal ein aktives größeres Work Package,
* keine unnötige Skill-Erweiterung.

Superpowers darf als Referenz untersucht werden, aber nicht parallel als zweites Governance-System eingeführt werden.

## 15. Projektphasen

### Phase 0 – Discovery und Scope Lock

Ermitteln:

* konkrete Nutzerfälle,
* Datenklassen,
* Geräte,
* mobile Anforderungen,
* bestehende Proxmox-Umgebung,
* Backupmöglichkeiten,
* Netzwerkzugang,
* aktuelle Wissensquellen,
* Benchmarkfragen.

Noch keine produktive Installation.

### Phase 1 – Proxmox-Referenzumgebung

* dedizierte VM,
* Benutzer- und Rechtekonzept,
* Netzwerkzugriff,
* SSH,
* persistente Terminalsitzung,
* browserbasierter Zugriff,
* Backup-Grundlage.

### Phase 2 – Wissensfundament

* Verzeichnisstruktur,
* Source Authority,
* Index,
* Current State,
* erste kontrollierte Quellen,
* Git-Versionierung.

### Phase 3 – Retrieval-Pilot

* lokale Suchlösung,
* Collections,
* Brain-First-Regeln,
* Context Budgets,
* Quellenreferenzen,
* Benchmark gegen bisherigen Ablauf.

### Phase 4 – Mehrgeräte- und Mobile-Pilot

* mindestens zwei PCs,
* mindestens ein Mobilgerät,
* derselbe zentrale Stand,
* Session-Handoff,
* Zugriffskontrolle.

### Phase 5 – Wiki-Pilot

* begrenzter Themenbereich,
* keine Vollbestandsmigration,
* Konfliktkandidaten,
* Human Review,
* Auditlog.

### Phase 6 – Portabilität

* generische Linux-Installationsanleitung,
* Konfigurationsmodell,
* Proxmox-spezifischer Guide,
* Prüfung eines Containerprofils,
* Export- und Restore-Test.

### Phase 7 – Öffentliche Entscheidung

Entscheidung:

```text
internal only
open-source reference implementation
reusable framework
integration into existing Core project
separate public product
no-go
```

Keine automatische Entscheidung zugunsten eines neuen öffentlichen Produkts.

## 16. Erfolgskriterien

Der Pilot ist erfolgreich, wenn:

* derselbe Wissensstand von mehreren Geräten erreichbar ist,
* die Baselinefragen korrekt beantwortet werden,
* deutlich weniger Dateien geöffnet werden,
* deutlich weniger Kontext an Claude übertragen wird,
* die Antwortqualität nicht sinkt,
* Quellen und Revisionen nachvollziehbar sind,
* Konflikte nicht automatisch aufgelöst werden,
* Backups und Restore getestet sind,
* kein Proxmox-Lock-in entsteht,
* ein generischer Linux-Betrieb plausibel dokumentierbar ist.

## 17. Do-not-start

Noch nicht beginnen:

* öffentliche Produktveröffentlichung,
* endgültiges Branding,
* eigene Graph-Web-App,
* vollständiger Wiki-Ingest,
* automatische Repository-Änderungen,
* automatische Konfliktentscheidung,
* produktive Mehrgeräte-Synchronisation ohne Test-Vault,
* Kubernetes,
* Multi-Tenant-Betrieb,
* SaaS,
* Proxmox-API-Integration,
* neue NDF-Skills,
* CDF-Integration,
* CoreOps-Integration,
* CDS-Komponenten,
* öffentliche Cloudinstanz.

## 18. Erste Aufgabe im Projektchat

Beginne mit einer **Discovery- und Architekturphase**, nicht mit Installation.

Liefere:

1. Projektdefinition,
2. konkrete Problemformulierung,
3. drei bis fünf messbare Fähigkeiten,
4. Nutzer- und Geräteprofil,
5. Daten- und Datenschutzklassen,
6. Deployment-Anforderungen,
7. Proxmox-Referenzarchitektur,
8. deployment-neutrale Zielarchitektur,
9. Komponenten- und Vertrauensgrenzen,
10. Tool-Evaluationsmatrix,
11. Backup- und Restore-Konzept,
12. Benchmarkplan,
13. Risiko- und Entscheidungsregister,
14. phasenweisen Projektplan,
15. ersten kompakten NDF-Work-Package-Entwurf.

Stelle nur Fragen, die für Architektur, Datenschutz, Betrieb oder Scope zwingend benötigt werden.

Bündele die Fragen nach Möglichkeit, statt den Human Maintainer mit vielen einzelnen Rückfragen zu unterbrechen.

## 19. Erwartete offene Informationen

Folgende Informationen müssen im Projektchat erhoben werden:

* Proxmox-Version und Cluster- oder Einzelhostbetrieb,
* CPU, RAM und verfügbarer Speicher,
* vorhandene Backupziele,
* ZFS, LVM oder anderer Storage,
* bestehendes VPN oder Tailscale,
* DNS und Reverse Proxy,
* Android oder iOS,
* benötigte native Obsidian-Nutzung,
* Offlineanforderungen,
* Zahl der Geräte,
* gewünschte Wissensquellen,
* auszuschließende Daten,
* vorhandene Claude-Code-Nutzung,
* GitHub-Zugriff,
* erwartete Nutzerzahl,
* spätere öffentliche Zielgruppe.

## 20. Abschlussformat

Beende jede größere Projektphase mit:

# BEGIN CORE-BRAIN-HANDOFF

Enthalten sein müssen:

* aktueller Projektstatus,
* bestätigte Entscheidungen,
* offene Annahmen,
* aktive Risiken,
* aktuelles Work Package,
* erzielte Evidenz,
* nächstes Gate,
* nächster autorisierter Schritt,
* Do-not-start-Liste,
* Auswirkungen auf Core Vision, NDF und andere Core-Projekte.

Beende mit:

# END CORE-BRAIN-HANDOFF

## Leitprinzip

> Proxmox ist die erste Referenzplattform, nicht die Produktgrenze. Der Wissensbestand bleibt portabel, der Index bleibt reproduzierbar, Claude liest nur das Nötige und der Mensch entscheidet, was gilt.
