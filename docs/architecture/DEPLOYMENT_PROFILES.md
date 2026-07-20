# Deployment Profiles — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-004 |
| Autoritätsklasse | A2 |
| Status | **Beschreibung, keine Installation** |
| Stand | 2026-07-20 |

Fünf Betriebsprofile für denselben deployment-neutralen Core. Kein Profil
verlangt Änderungen am Kern.

---

## Zentrale Unterscheidung

> **Docker Compose** ist eine **Anwendungslaufzeit** — es startet und verbindet
> die Anwendungsbestandteile.
>
> **Proxmox** ist eine **Infrastrukturplattform** — es stellt die virtuelle
> Maschine bereit, in der eine Laufzeit läuft.
>
> Beides liegt auf verschiedenen Ebenen und darf nicht vermischt werden. Profil
> A kombiniert beides; Profil D verwendet Compose ohne Proxmox; Profil B und C
> können ganz ohne Container auskommen.

Docker Compose ist die **bevorzugte** Pilotlaufzeit (D-016) — nicht die einzige
unterstützte und **keine Produktabhängigkeit**.

## Statuswerte

| Status | Bedeutung |
| --- | --- |
| `reference` | Referenzprofil des Piloten |
| `planned` | Vorgesehen, dokumentierbar zu halten |
| `later` | Später zu betrachten |
| `limited` | Unterstützt, aber mit dokumentierten Einschränkungen |

---

## Profil A — Proxmox-VM

**Status: `reference`** · Referenzprofil des Piloten (D-015)

| Feld | Festlegung |
| --- | --- |
| **Zielgruppe** | Betreiber mit vorhandenem Proxmox-Host |
| **Voraussetzungen** | Proxmox-Host; Kapazität für eine dedizierte Linux-VM; getrennte System- und Datenspeicherbereiche; Backupziel plus externe Kopie |
| **Unterstützte Kernfunktionen** | Alle. Kanonischer Bestand, Index, Suche, Retrieval, Context Packs, Review, Backup/Restore/Rebuild, Web-UI, mobiler Zugriff |
| **Einschränkungen** | Keine funktionalen. Betriebliche Abhängigkeit vom Hypervisor |
| **Sicherheitsgrenze** | VM-Grenze. **Kein Betrieb auf dem Proxmox-Host.** **Keine Proxmox-API-Berechtigung.** **Keine Ausführung als Root.** Erreichbarkeit nur im privaten Netz |
| **Datenpfade** | Kanonisch auf der Datendisk; abgeleitet getrennt davon; Backup auf ein separates Ziel und zusätzlich außerhalb des Hosts |
| **Backupverantwortung** | Betreiber. Vier Stufen: Git-Historie, Datendisk-Sicherung, VM-Backup, externe Kopie |
| **Mobile/Mehrgeräte** | Ja, über privates Netz oder VPN |
| **Anwendungslaufzeit** | Docker Compose **bevorzugt** innerhalb der VM |

Proxmox ist hier **erste Referenzplattform, nicht Produktgrenze**. Die
Architektur bleibt ohne Proxmox vollständig funktionsfähig.

## Profil B — Allgemeine Linux-VM

**Status: `planned`**

| Feld | Festlegung |
| --- | --- |
| **Zielgruppe** | Betreiber mit beliebigem Hypervisor oder Cloud-VM |
| **Voraussetzungen** | Linux-VM (Debian, Ubuntu Server oder vergleichbar); getrennte Datenablage; Backupziel |
| **Unterstützte Kernfunktionen** | Alle — **identische Core-Architektur wie Profil A** |
| **Einschränkungen** | Keine funktionalen. Backup liegt vollständig beim Betreiber, ohne Hypervisor-Komfort |
| **Sicherheitsgrenze** | VM-Grenze; **kein hypervisorspezifischer Code**; kein Root; privates Netz |
| **Datenpfade** | Wie A, ohne Proxmox-spezifische Sicherung |
| **Backupverantwortung** | Betreiber, vollständig eigenständig |
| **Mobile/Mehrgeräte** | Ja |
| **Anwendungslaufzeit** | Docker Compose **oder dokumentierter nativer Betrieb** |

Dieses Profil ist der **Nachweis der Deployment-Neutralität**. Was hier nicht
läuft, ist im Kern falsch platziert.

## Profil C — Physischer Linux-Server oder Mini-PC

**Status: `planned`**

| Feld | Festlegung |
| --- | --- |
| **Zielgruppe** | Self-Hoster ohne Hypervisor |
| **Voraussetzungen** | Linux-Host; getrennte Datenablage; **externes Backupziel zwingend** |
| **Unterstützte Kernfunktionen** | Alle |
| **Einschränkungen** | **Hardwareausfall ist das dominierende Risiko.** Keine Snapshot-Ebene, keine schnelle Migration; Wiederherstellung bedeutet Neuaufsetzen plus Restore |
| **Sicherheitsgrenze** | Host-Grenze statt VM-Grenze — **eine Isolationsschicht weniger**. Kein Root; privates Netz; sorgfältige Dienstetrennung |
| **Datenpfade** | Gleiche Datenverträge wie A und B |
| **Backupverantwortung** | Betreiber. Externe Kopie ist hier **nicht optional** |
| **Mobile/Mehrgeräte** | Ja |
| **Anwendungslaufzeit** | Compose oder nativ |

## Profil D — Docker/OCI auf bestehendem Linux

**Status: `later`**

| Feld | Festlegung |
| --- | --- |
| **Zielgruppe** | Betreiber mit vorhandener Container-Umgebung |
| **Voraussetzungen** | Linux mit Docker, Podman oder vergleichbarer OCI-Umgebung |
| **Unterstützte Kernfunktionen** | Alle, sofern Volumes und Netzgrenzen korrekt gesetzt sind |
| **Einschränkungen** | **Hostverantwortung liegt beim Betreiber.** Der Host ist nicht Teil der Lieferung. **Kein Kubernetes-Pflichtumfang** |
| **Sicherheitsgrenze** | Containergrenze — schwächer als eine VM-Grenze. Erforderlich: **nicht-privilegierte Benutzer-IDs**, restriktive Mount-Modi (kanonisch lesend, wo möglich), getrennte Netzwerke, **kein Root im Container** |
| **Datenpfade** | Persistente Volumes für kanonisch und abgeleitet, **getrennt**; Backupvolume von der Anwendung nicht beschreibbar |
| **Backupverantwortung** | Betreiber, auf Hostebene |
| **Mobile/Mehrgeräte** | Ja |
| **Anwendungslaufzeit** | Container ist hier zugleich das Profil |

Containerisierung ist **kein Pflichtziel der ersten Phase**, muss aber
architektonisch möglich bleiben (Projektübergabe §4).

## Profil E — Lokaler Einzelplatz

**Status: `limited`**

| Feld | Festlegung |
| --- | --- |
| **Zielgruppe** | Einstieg ohne Server |
| **Voraussetzungen** | Ein Arbeitsplatzrechner |
| **Unterstützte Kernfunktionen** | Kanonischer Bestand, Index, Suche, Retrieval, Context Packs, Review — lokal |
| **Einschränkungen** | **Kein zentraler Mehrgerätezugriff.** Verfügbarkeit nur bei laufendem Rechner. Kein gemeinsamer Stand über Geräte. Mobile Nutzung praktisch nicht gegeben |
| **Sicherheitsgrenze** | Betriebssystem-Benutzergrenze — **die schwächste der fünf** |
| **Datenpfade** | Lokal; abgeleitet getrennt von kanonisch |
| **Backupverantwortung** | **Vollständig beim Nutzer.** Ohne externe Kopie besteht ein Totalverlustrisiko |
| **Mobile/Mehrgeräte** | **Nein** beziehungsweise stark eingeschränkt |

Profil E erfüllt das Projektziel „derselbe Wissensstand von mehreren Geräten"
(Projektübergabe §16) **nicht**. Es ist ein Einstieg, kein Zielzustand.

---

## Vergleich

| Kriterium | A Proxmox-VM | B Linux-VM | C Physisch | D Container | E Einzelplatz |
| --- | --- | --- | --- | --- | --- |
| Status | `reference` | `planned` | `planned` | `later` | `limited` |
| Isolationsstärke | VM | VM | Host | Container | OS-Benutzer |
| Mehrgeräte | ja | ja | ja | ja | **nein** |
| Mobile Nutzung | ja | ja | ja | ja | **nein** |
| Zentrale Backups | ja | ja | ja | ja | **nein** |
| Hypervisor nötig | ja | ja | nein | nein | nein |
| Compose bevorzugt | **ja** | optional | optional | inhärent | nein |
| Hardwareausfall-Risiko | mittel | mittel | **hoch** | mittel | **hoch** |

## Was in allen Profilen gleich bleibt

Diese Zusagen sind **profilunabhängig**. Verletzt ein Profil sie, ist das
Profil falsch beschrieben, nicht der Core:

1. Kanonische Inhalte in offenen, exportierbaren Formaten (Markdown, Git)
2. Strikte Trennung kanonisch / abgeleitet
3. Abgeleitete Daten vollständig reproduzierbar
4. Kein Verlust kanonischen Wissens bei Verlust der abgeleiteten Schicht
5. Retrieval Policy Gateway als einzige Ausgabegrenze, fail-closed
6. `secret` und `excluded-from-ai` erreichen nie ein externes Modell
7. Kein Betrieb als Root
8. Keine öffentliche Standardfreigabe interner Dienste
9. Nur ein autorisierter Schreibpfad nach kanonisch
10. Keine automatische Konfliktentscheidung
11. Keine automatischen Commits oder Pushes

## Bewusst offene Entscheidungen

| Punkt | Status |
| --- | --- |
| Linux-Distribution für Profil A | offen, Deployment Required |
| VM-Ressourcengröße | offen, Deployment Required |
| VPN- beziehungsweise Netzwerktechnologie | offen, Deployment Required (D-023 legt nur das Profil fest) |
| Backupsoftware und -ziel | offen, Deployment Required |
| Suchmaschine, Datenbank, Web-UI-Technologie | offen (OD-20, OD-25) |
| Nativer Betrieb ohne Container in B und C | offen, zu dokumentieren |

Die Prüfung dieser Punkte erfolgt im
[Deployment Readiness Check](../operations/DEPLOYMENT_READINESS_CHECK.md),
**nicht** an Gate G0.

## Status

**Keine Installation, keine Compose-Datei, keine Infrastrukturbewertung.**
Die reale Umgebung wurde in Phase 0 bewusst nicht geprüft.
