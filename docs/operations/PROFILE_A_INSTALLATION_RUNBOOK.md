# Profile-A Installation Runbook

| Feld | Wert |
| --- | --- |
| Gegenstand | spätere kontrollierte Bereitstellung des Profil-A-Bundles |
| Erfasst in | **CBP-WP-020** (D-055) |
| Autoritätsklasse | A3 |
| **Status** | **nicht ausgeführt** — dieses Runbook beschreibt, es handelt nicht |
| Stand | 2026-07-29 |

## Zweck und Aussagegrenze

Dieses Runbook beschreibt, **wie** eine spätere Bereitstellung von Profil A
ablaufen würde. Es ist **keine** Bereitstellung, **keine** Anleitung zur
sofortigen Ausführung und **keine** Freigabe.

**In CBP-WP-020 wurde keine reale Handlung ausgeführt:** keine VM erstellt,
kein Container gestartet, kein Netzwerk konfiguriert, kein Secret aufgelöst,
kein Backup ausgeführt.

| Nicht belegt durch dieses Runbook |
| --- |
| eine erfolgte Installation |
| eine Betriebs- oder Produktivfreigabe |
| eine wirksame Sicherheitskontrolle (**12 bleiben `DOCUMENTED ONLY`**) |
| ein ausgeführter Security-Negativtest (**0 von 32**, D-056) |
| eine Gateauswertung (beide **`NOT EVALUATED`**) |
| ein CBP- oder RT-2-Restore-Nachweis (**R-20 bleibt offen**) |

## Erforderliches Human Gate

**Eine Bereitstellung nach diesem Runbook ist derzeit nicht autorisiert.**

Voraussetzung ist ein **separates Folge-Work-Package** mit:

1. abgeschlossenem und committetem CBP-WP-020,
2. eigener ausdrücklicher Human-Maintainer-Autorisierung,
3. eigenem Infrastruktur- und Sicherheitsplan,
4. eigenem Human Gate vor der ersten realen Handlung.

**CBP-WP-020 nimmt keine Bereitstellung vorweg.**

## Voraussetzungen für eine spätere Bereitstellung

| Voraussetzung | Stand |
| --- | --- |
| DRC Profil A freigegeben | **erfüllt** — `APPROVED BY HUMAN MAINTAINER`, rein dokumentarisch |
| Bundle offline validiert | **erfüllt** — Validator meldet `PROFILE-A-BUNDLE VALID` |
| Folge-Work-Package autorisiert | **offen** |
| Dedizierte Profil-A-VM vorhanden | **offen** |
| Lokaler Operator-Workspace eingerichtet | **offen** |

## Ablauf einer späteren Bereitstellung

### 1 — Zielsystem

- **Keine Installation auf dem Proxmox-Hypervisor-Host.** Der Dienst läuft
  ausschließlich in einer **dedizierten Profil-A-VM**.
- **Keine Proxmox-API-Berechtigung** für den Dienst.
- Gast: Ubuntu Server 26.04 LTS amd64; Ressourcen nach der
  Profil-A-Zielspezifikation.

### 2 — Lokaler Operator-Workspace

- Der Operator-Workspace liegt **außerhalb des öffentlichen Repositorys**
  (Bereichsmodell W-3, ADR-0007).
- `deployments/profile-a/operator.env.example` **in den lokalen
  Operator-Workspace kopieren**.
- **Alle Pflichtwerte dort lokal befüllen** — Images sowie UID und GID beider
  Service-Identitäten.
- **Eine befüllte Operator-Datei wird niemals zurück ins Repository kopiert.**

### 3 — Secret-Provider

- Der `file`-Provider wird **lokal** gemappt (OS-geschützt, nur für die
  berechtigten Service- und Betreiberrollen lesbar).
- **Keine Secret-Werte** in Environment, Compose, Config oder Repository — nur
  **Referenzen** nach `cbp-secret:v1:file:<opaque-id>`.
- Unbekannter Provider und fehlende Referenz **blockieren fail-closed**.

### 4 — Offline-Validierung vor jeder Compose-Auswertung

- **Vor jeder späteren Compose-Auswertung** ist der Offline-Validator
  auszuführen; siehe
  [PROFILE_A_VALIDATION_RUNBOOK.md](PROFILE_A_VALIDATION_RUNBOOK.md).
- Bei Exitcode ungleich 0: **anhalten**.

### 5 — Docker und Compose

- **Docker- und Compose-Prüfungen erfolgen erst im separaten
  Deployment-Work-Package**, nicht hier und nicht in CBP-WP-020.

### 6 — Netzwerk und Egress

- Spätere Prüfung: private Netzgrenze, keine öffentliche Freigabe, Egress
  **deny-by-default** auf **Host- und Dienstebene**.
- Die sechs bestätigten Zielklassen werden erst dort zu konkreten Zielen
  aufgelöst — **nicht im Repository**.

### 7 — Backup

- **Wöchentliches vollständiges VM-Backup** auf eine physisch separate
  NAS-Zielklasse.
- **Tägliche Sicherung der kanonischen Daten** — sie trägt das **RPO von 24
  Stunden**; das wöchentliche VM-Backup allein belegt es **nicht**.
- Die konkrete technische Umsetzung der täglichen Sicherung ist **nicht
  festgelegt** und **nicht Bestandteil von CBP-WP-020**.

## Abbruchbedingungen

**Sofort anhalten**, wenn:

| Bedingung |
| --- |
| der Offline-Validator einen Fehler meldet |
| ein Secret-Wert in Repository, Environment, Compose oder Log auftaucht |
| eine reale Adresse, ein Hostname oder ein Hostpfad ins Repository gelangen soll |
| der Dienst als root oder auf dem Hypervisor-Host laufen soll |
| eine Portpublikation oder öffentliche Freigabe verlangt wird |
| Backup-Storage oder RT-2 direkt gemountet werden soll |
| eine Handlung ohne das erforderliche Human Gate erfolgen soll |

## Ausdrücklich nicht Bestandteil

**Kein automatisches Deployment. Keine reale Handlung durch CBP-WP-020.**
Dieses Runbook enthält **keine** konkreten IP-Adressen, Domains, URLs,
NAS-Freigaben, Hostnamen, UID- oder GID-Werte, Hostpfade, realen
Secret-Referenzen oder Secret-Werte.
