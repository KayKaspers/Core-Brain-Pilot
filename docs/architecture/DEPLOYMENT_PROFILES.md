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

## Pilot Profile-A Target Specification

**Status: dokumentiertes Zielbild — nicht bereitgestellt.** Festgelegt durch
**D-054** (CBP-WP-019) auf Grundlage der Angaben des Human Maintainers.

| Feld | Zielwert |
| --- | --- |
| Virtualisierung | dedizierte QEMU/KVM-VM auf **Proxmox VE** |
| Hosttopologie | **Einzelhost** |
| Gast | **Ubuntu Server 26.04 LTS**, amd64 |
| vCPU | **4** |
| RAM | **8 GiB** |
| Systemdisk | **64 GiB** |
| Datendisk | **250 GiB**, **getrennte** virtuelle Disk |
| Storageklasse | **NVMe-basierter LVM-Thin-Pool**, snapshot-fähig |
| Netz | **private virtuelle Bridge** |
| Adressierung | **statisch reservierte Adresse im privaten LAN** |
| Fernzugriff | **WireGuard** über vorhandenes privates Gateway |
| Anwendungslaufzeit | **Docker Compose innerhalb der VM** |
| Backup — Stufe 1 | vollständiges **Proxmox-VM-Backup**, **wöchentlich**, auf **physisch separate NAS** |
| Backup — Stufe 2 | **kanonische CBP-Daten täglich** gesichert |
| Abgeleitete Daten | vollständig reproduzierbar — **kein** eigenes Backup; Rebuild aus kanonisch + Registry |
| RPO | **24 Stunden** — getragen von der **täglichen kanonischen Sicherung** |
| RTO | **8 Stunden** |

### Aussagegrenzen

Ausdrücklich gilt:

| Grenze | Bedeutung |
| --- | --- |
| **Keine Produktmindestanforderung** | Die Werte sind **Pilotwerte** eines konkreten Deployments, keine Systemvoraussetzung des Produkts |
| **Keine Proxmox-API-Berechtigung** | Der Dienst erhält **keinen** Hypervisor-Zugriff |
| **Kein Betrieb auf dem Hypervisor-Host** | Ausführung ausschließlich in der Gast-VM |
| **Keine öffentliche Freigabe** | Erreichbarkeit nur im privaten Netz oder über WireGuard; Egress bleibt **deny-by-default** |
| **Keine konkrete Adresse** | Nur die abstrakte Klasse „statisch reservierte Adresse im privaten LAN" wird dokumentiert |
| **Keine konkrete NAS-Kennung** | Nur die abstrakte Klasse „physisch separate NAS" wird dokumentiert |
| **Keine Installation ausgeführt** | Es wurde nichts erstellt, verändert, gestartet oder verbunden |
| **Zielbild, nicht deployed** | Die Spezifikation beschreibt ein geplantes Deployment. Alle 19 DRC-Einzelkriterien sind `ready`; der **DRC-Gesamtstatus** lautet seit **2026-07-29** **APPROVED BY HUMAN MAINTAINER** (Profil A). Das ist eine **dokumentarische** Freigabe — **keine** Installation, **keine** Bereitstellung, **keine** Betriebsfreigabe. Die erste kontrollierte Bereitstellung bleibt einem **separaten, ausdrücklich autorisierten** Work Package vorbehalten |

**WireGuard und die Proxmox-Backuptechnik bleiben austauschbare,
deploymentspezifische Entscheidungen** — sie sind **keine** Produktabhängigkeit
und binden die deployment-neutrale Architektur (ADR-0001) nicht.

## Bewusst offene Entscheidungen

| Punkt | Status |
| --- | --- |
| Linux-Distribution für Profil A | **entschieden** — Ubuntu Server 26.04 LTS (D-054, DRC-02 `ready`) |
| VM-Ressourcengröße | **entschieden** — 4 vCPU / 8 GiB / 64 + 250 GiB (D-054, DRC-04…06 `ready`) |
| VPN- beziehungsweise Netzwerktechnologie | **entschieden** — WireGuard als Deploymentwahl (D-054, DRC-08 `ready`); D-023 legt weiterhin nur das Profil fest |
| Backupsoftware und -ziel | **entschieden** — wöchentliches Proxmox-VM-Backup auf physisch separate NAS plus tägliche Sicherung kanonischer Daten (D-054, DRC-11/12/13 `ready`) |
| Suchmaschine, Datenbank, Web-UI-Technologie | **weiterhin offen** (OD-20, OD-25) — **nicht** Gegenstand des DRC |
| Nativer Betrieb ohne Container in B und C | offen, zu dokumentieren |
| Gerätezahl, Secret-Deploymentwerte, Betriebsverantwortung, RT-2-Retention | **entschieden** — DRC-10, DRC-17, DRC-18, DRC-19 stehen auf `ready` (D-054) |

Die Prüfung dieser Punkte erfolgt im
[Deployment Readiness Check](../operations/DEPLOYMENT_READINESS_CHECK.md),
**nicht** an Gate G0.

## Status

**Keine Installation, keine Compose-Datei, keine Infrastrukturbewertung.**
Die reale Umgebung wurde in Phase 0 bewusst nicht geprüft.

### Backupmodell — Abgrenzung

Das Backupmodell ist **zweistufig**. Die beiden Stufen dürfen nicht vermengt
werden:

| Stufe | Gegenstand | Frequenz | Zweck |
| --- | --- | --- | --- |
| **1** | vollständiges **VM-Backup** (Proxmox VE) | **wöchentlich** | Wiederherstellung der gesamten Maschine |
| **2** | **kanonische CBP-Daten** | **täglich** | Trägt das **RPO von 24 Stunden** |

**Das wöchentliche VM-Backup allein würde ein RPO von 24 Stunden nicht
belegen.** Erst die tägliche Sicherung der kanonischen Daten trägt diesen
Zielwert. Vollständig reproduzierbare abgeleitete Daten werden **nicht**
gesichert, sondern aus kanonischem Bestand und Registry **wieder aufgebaut**.

> **Die konkrete technische Umsetzung der täglichen kanonischen Sicherung ist
> nicht ausgeführt und nicht festgelegt.** Bestätigt sind ausschließlich
> **Frequenz** und **Zielklasse**; das Werkzeug bleibt Bestandteil des späteren
> Deployments. Es wurde **kein** Backupjob eingerichtet und **kein** Restore
> ausgeführt.
