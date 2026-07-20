# ADR-0001 — Deployment-neutraler Core mit austauschbaren Adaptern

| Feld | Wert |
| --- | --- |
| Status | **accepted** |
| Datum | 2026-07-20 |
| Entscheider | Human Maintainer |
| Supersedes | — |
| Superseded by | — |
| Belegt durch | D-017 (A0), Projektübergabe §4 und §13 (A5) |

## Kontext

Core Brain Pilot soll auf einer Proxmox-VM pilotiert werden, aber langfristig
auf mindestens fünf Betriebsprofilen dokumentierbar bleiben. Ohne eine
ausdrückliche Trennung sickern Plattformannahmen — Pfade, Dienstnamen,
Backupmechanismen, Netzwerktopologie — in den Kern ein und erzeugen einen
Lock-in, der später nur durch Umbau auflösbar wäre (Risiko R-19).

Projektübergabe §13 verlangt zusätzlich, dass die Architektur von Anfang an
öffentlich dokumentierbar bleibt.

## Entscheidung

Der Core ist **deployment-neutral**. Sämtliche plattform- und
technologiespezifischen Bestandteile liegen in **austauschbaren Adaptern** und
in **Deploymentprofilen**, niemals im Kern.

Konkret:

1. Der Kern kennt keine Proxmox-API und setzt keinen Hypervisor voraus.
2. Suchmaschine, Web-UI, Backup und MCP/API sind Adapter hinter stabilen
   internen Schnittstellen.
3. Fünf Referenzprofile A bis E bleiben dokumentierbar.
4. Ein Adapterwechsel berührt den kanonischen Bestand nicht.
5. Kanonische Inhalte liegen in offenen, exportierbaren Formaten — primär
   Markdown unter Git.

## Alternativen

**Auf Proxmox optimieren.** Verworfen: widerspricht dem Leitprinzip „Proxmox
ist die erste Referenzplattform, nicht die Produktgrenze" und verhindert die
öffentliche Verwertbarkeit.

**Abstraktion erst später einziehen.** Verworfen: Plattformannahmen sind billig
zu vermeiden und teuer zu entfernen. Profil B ist der laufende Nachweis, dass
der Kern frei von ihnen ist.

**Vollständige Abstraktion aller Bestandteile.** Verworfen: überzogen. Der
kanonische Bestand und die Policy-Schicht sind bewusst **nicht** austauschbar —
sie sind das Produkt.

## Konsequenzen

**Leichter:** Wechsel von Suchmaschine, Web-UI oder Backupsoftware; Betrieb
ohne Hypervisor; Veröffentlichung des Kerns.

**Schwerer:** Jede plattformnahe Optimierung braucht einen Adapter. Profil B
muss dauerhaft mitgedacht werden, auch wenn niemand es sofort betreibt.

**Geschlossene Türen:** Proxmox-API-Integration ist ausgeschlossen und steht
auf der Sperrliste.

## Bezug

Prinzip 14 · Capability 29 · G0-Kriterium F-5 · Risiko R-19 ·
[../architecture/SYSTEM_ARCHITECTURE.md](../architecture/SYSTEM_ARCHITECTURE.md) ·
[../architecture/DEPLOYMENT_PROFILES.md](../architecture/DEPLOYMENT_PROFILES.md)
