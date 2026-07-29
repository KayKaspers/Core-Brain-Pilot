# CBP-WP-019 — Deployment Readiness Intake and Profile-A Target Specification

| Feld | Wert |
| --- | --- |
| Titel | **Deployment Readiness Intake and Profile-A Target Specification** |
| Typ | **docs-only, interaktiv** (Human-Maintainer-Intake) |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Status | **`committed`** |
| Phase | **complete** |
| Abgeschlossene Phasen | **B1** · **B1.1** · **B1.2** · **C – Post-Commit Reconciliation** |
| A0-Entscheidung | **D-054** (konsolidiert, A/B/C/D/E/F/G/H) |
| ADR | **not required** (`ADR_NOT_REQUIRED`) |
| DRC | **19 Prüfpunkte** — **19 `ready`**, **0 `blocked`**; Gesamtstatus **APPROVED BY HUMAN MAINTAINER** |
| Human-Maintainer-Gesamtfreigabe | **erteilt am 2026-07-29** für **Profil A** — rein dokumentarisch, **keine** Installations-, Betriebs-, Security- oder Capability-Freigabe |
| Capabilities | **0 von 29** — unverändert |
| Gates | Mapping Activation `NOT EVALUATED` · Security Foundation Readiness `NOT EVALUATED` |
| Tests | **558 – OK**, compileall Exit 0 (docs-only, unverändert) |
| Commit | **`3c437f2`** — `CBP-WP-019: approve profile A deployment readiness` |
| Commit-Autorität | **Human Maintainer** — erstellt und nach `origin/main` gepusht |
| Abschlussdatum | **2026-07-29** |
| R-20 | **offen** |
| R-33 | **16 Konsistenzvorgänge in 19 Work Packages** (nach Post-Commit-Reconciliation) |

---

## Zweck

Die 18 bestehenden Deployment-Required-Prüfpunkte durch **ausdrückliche
Human-Maintainer-Eingabe** belegen, den Katalog um die fehlende
RT-2-Aufbewahrung erweitern und daraus die **Zielspezifikation für Profil A**
ableiten. Das Paket löst damit die oberste Blockierbedingung des Projekts:
ohne Deploymentwerte kein Zielsystem, ohne Zielsystem keine durchgesetzte
Sicherheitsgrundlage, ohne diese keine Gateauswertung und keine Aktivierung.

---

## Phase-A- und Phase-A.1-Befunde

### Phase A — Architektur- und Vollständigkeitsanalyse (read-only)

| Befund | Ergebnis |
| --- | --- |
| DRC-Struktur | **18** Prüfpunkte gegenüber **16** Deployment-Required-G0-Kriterien; die Differenz erklärt sich aus Auffächerung (B-7→2, F-4→3, E-1→2), Zusammenfall (C-1+C-2→DRC-08, A-3+C-6→DRC-10) und **einem** Punkt ohne G0-Herkunft (DRC-01) |
| Statusmodell | Genau vier Werte; `ready` bezeichnet eine **dokumentierte, nachgewiesene Voraussetzung**, keine technische Prüfung des Zielsystems |
| Gesamtstatus | **Nicht** aus den Einzelstatuswerten ableitbar — ausschließlich Human-Maintainer-Feststellung (Abschlussregel 4) |
| OD-21 | **Bereits geschlossen** durch **D-023**; der DRC führte irreführend „vertagt". Offen war nur der Technologie-Restpunkt |
| Coverage-Lücken | Drei Deployment-Required-Verpflichtungen ohne eigenen Prüfpunkt: **RT-2-Aufbewahrungsdauer**, **OD-20**, **OD-34-Restpunkte** |

### Phase A.1 — DRC-Lifecycle-Reconciliation (read-only)

Geprüft wurde der gemeldete Zyklus: alle 18 Punkte blockieren die Installation,
DRC-16 verlangt einen durchgeführten Restore-Test — der scheinbar erst nach
einer Bereitstellung möglich ist.

**Ergebnis: der Zyklus entsteht ausschließlich aus einer nicht quellengedeckten
Lesart von DRC-16.** Drei unabhängige kanonische Belege:

| Beleg | Aussage |
| --- | --- |
| **Standardwert 10** (G0_SCOPE_LOCK_CRITERIA, PROJECT_MANIFEST, R-20) | Backup muss **vor produktivem Betrieb** eingerichtet und getestet sein — nicht vor der Installation |
| **D-027 / G0_SCOPE_LOCK_REVIEW §16** | Führt „DRC auf `ready`" (Bedingung 2) und „Backup eingerichtet und getestet" (Bedingung 4) als **getrennte** Bedingungen |
| **Security Foundation Readiness Gate, Punkt 19** (KB-12, Stufe 5) | Der **CBP-Datenrestore mit Integritätsprüfung** hat bereits einen eigenen, nachgelagerten Ort |

**Es existieren zwei verschiedene Restore-Nachweise.** DRC-16 entstammt **F-4**
und betrifft das **Backup-Regime des Betreibers** — vor der Bereitstellung real
erprobbar. Readiness-Gate-Punkt 19 betrifft **CBP-Daten und RT-2** — zwingend
nachgelagert, da beide vor dem Deployment nicht existieren.

**Empfohlenes und übernommenes Lifecycle-Modell: L0** — ein einstufiger DRC mit
ausdrücklicher Klarstellung des DRC-16-Prüfumfangs. L1 hätte eine bereits auf
A0-Ebene bestehende Trennung dupliziert; L2 hätte „durchgeführt" unzulässig
abgeschwächt; L3 hätte eine neue Trust Boundary erzeugt.

---

## Human-Maintainer-Eingaben (A0)

Alle Angaben sind **Zusagen des Human Maintainers**, keine vom Repository
verifizierten Messwerte. Es fand **kein** Zugriff auf Hypervisor, Speicher, Netz
oder Sicherungsziel statt.

### Infrastruktur

| Feld | Angabe |
| --- | --- |
| Deploymentprofil | **Profil A** — dedizierte Proxmox-VM |
| Virtualisierungsplattform | **Proxmox VE 9.2.5** |
| Topologie | **Einzelhost** |
| Host-Ressourcenklasse | x86_64, sechs physische CPU-Kerne, rund 31 GiB RAM |
| Primärer VM-Storage | **NVMe-basierter LVM-Thin-Pool** |
| Snapshot-Fähigkeit | vorhanden |
| Private Netzgrenze | **privates LAN** |
| Remotezugang | **WireGuard** auf vorhandener UniFi-Gateway-Infrastruktur |

### Referenz-VM

| Feld | Angabe |
| --- | --- |
| Gastbetriebssystem | **Ubuntu Server 26.04 LTS**, amd64 |
| vCPU / RAM | **4** / **8 GiB** |
| Systemdisk / Datendisk | **64 GiB** / **250 GiB**, zwei **getrennte** virtuelle Disks |
| Anwendungslaufzeit | **Docker Compose innerhalb der VM** |

### Backup

| Feld | Angabe |
| --- | --- |
| Backuptechnik | integrierte Backupfunktion von **Proxmox VE** |
| Backupziel | **physisch separate NAS** im privaten lokalen Netzwerk |
| **VM-Backup** | **wöchentlich** (vollständige Maschine) |
| **Kanonische CBP-Daten** | **täglich** gesichert |
| Abgeleitete Daten | vollständig reproduzierbar — **kein** zwingendes separates Backup, Rebuild aus kanonisch + Registry |
| RPO / RTO | **24 Stunden** / **8 Stunden** — das RPO wird von der **täglichen kanonischen Sicherung** getragen, **nicht** vom wöchentlichen VM-Backup |

### Restore-Nachweis

**Zulässige Aussage:** Human-Maintainer-Attestation eines **erfolgreichen
Restore-Tests des Betreiber-Backup-Regimes auf einem anderen System derselben
Plattform- und Werkzeugklasse.**

**Ausdrücklich nicht behauptet:**

- kein aktueller Restore der künftigen CBP-VM,
- kein Restore von CBP-Daten,
- kein Restore von RT-2,
- keine Integritätsprüfung einer RT-2-Hashkette,
- kein Restore gegen die konkrete neue VM,
- kein automatisierter oder repository-verifizierter Nachweis.

---

## DRC-16 — Abgrenzung

**Neuer Titel:** *Restore-Test des Betreiber-Backup-Regimes.*

**Erforderlicher Nachweis:** beschriebener und **tatsächlich durchgeführter**
Wiederherstellungstest der vorgesehenen Betreiber-Backuptechnik beziehungsweise
derselben Plattform- und Werkzeugklasse. Der Test darf auf einem **anderen
kontrollierten System** erbracht worden sein.

**Nicht Gegenstand:** CBP-Daten · RT-2 · Security-Control-Evidenz ·
Mapping-Evidenz.

**Status `ready`**, Nachweisart **Human-Maintainer-Attestation**. Die
Anforderung „durchgeführt" bleibt vollständig erhalten — sie wird auf den
Prüfumfang bezogen, der vor einer Bereitstellung überhaupt existieren kann.
**R-20 bleibt offen**, weil der CBP-/RT-2-Restore aussteht.

---

## DRC-19 — Erweiterung

| Feld | Wert |
| --- | --- |
| ID | **DRC-19** |
| Kategorie | **RT-2-Aufbewahrung** |
| G0-Herkunft | **keine** — Post-G0-Erweiterung aus **D-037 / OD-35 / RET-2** |
| Profilbezug | alle |
| Nachweis | Aufbewahrungsdauer je `retention_class`, Lösch- beziehungsweise Archivierungsverfahren, Owner-Rolle |
| Owner | **Human Maintainer / Betreiber** |
| Status | **`ready`** |
| Blockiert Deployment | **ja** |
| **Mindestaufbewahrung** | **365 Tage** — für **alle** `retention_class`-Werte inkl. Security- und Incident-Evidenz |
| **Nach Ablauf** | **dauerhafte Aufbewahrung** |
| Automatische Löschung | **nein** |
| Separates Archiv | **nein** |

**Semantische Klarstellung.** Die tatsächliche Aufbewahrung ist **unbefristet**;
die 365 Tage sind die bestätigte **Mindestaufbewahrung**, keine Löschfrist. Es
werden **keine neuen `retention_class`-Namen eingeführt**. **RT-2 ist weiterhin
nicht implementiert** — keine Retention-Engine, kein Speicher, kein Backup, kein
Restore-Nachweis.

**Struktur nach der Erweiterung:** 19 Prüfpunkte = **17** aus den **16**
Deployment-Required-G0-Kriterien abgeleitet + **2** ohne unmittelbare
G0-Herkunft (**DRC-01**, **DRC-19**). Die Zahl der G0-Kriterien bleibt **16**;
der **historische G0-Nachweis wurde nicht geändert**.

---

## DRC-Statusmatrix

| DRC | Status | Begründung |
| --- | --- | --- |
| DRC-01 | `ready` | Profil A ausdrücklich bestätigt |
| DRC-02 | `ready` | Ubuntu Server 26.04 LTS amd64 festgelegt |
| DRC-03 | `ready` | Einzelhost bestätigt |
| DRC-04 | `ready` | 4 vCPU festgelegt |
| DRC-05 | `ready` | 8 GiB RAM festgelegt |
| DRC-06 | `ready` | 64 GiB System und 250 GiB Daten getrennt |
| DRC-07 | `ready` | NVMe-basierter LVM-Thin-Storage, snapshotfähig |
| DRC-08 | `ready` | WireGuard als Deploymentwahl bestätigt |
| DRC-09 | `ready` | abstrakte Egress-Allowlist festgelegt |
| DRC-10 | `ready` | **2** Desktop-/Notebook-Geräte, **3** mobile Geräte; Zugriff über WireGuard |
| DRC-11 | `ready` | Proxmox-Backup auf physisch separate NAS |
| DRC-12 | `ready` | Kopie außerhalb des Proxmox-Hosts |
| DRC-13 | `ready` | **wöchentliches VM-Backup** und **tägliche kanonische Sicherung** |
| DRC-14 | `ready` | RPO 24 Stunden |
| DRC-15 | `ready` | RTO 8 Stunden |
| DRC-16 | `ready` | Human-Attestation erfolgreicher Proxmox-Restores |
| DRC-17 | `ready` | Providerklasse, Providertyp `file`, Schutzklasse, Service-Identitäten, Rotation und Widerruf bestätigt |
| DRC-18 | `ready` | Rollen und Bestandsgrößenordnung **1.000–10.000 Dokumente** bestätigt |
| DRC-19 | `ready` | Retention-Policy vollständig bestätigt — mindestens 365 Tage, danach dauerhaft |

**19 gesamt · 19 `ready` · 0 `blocked` · 0 `not-evaluated` · 0 `not-applicable`.**

**Gesamtstatus: APPROVED BY HUMAN MAINTAINER** — Profil A, **2026-07-29**.
Alle 19 Einzelkriterien tragen dokumentierte Human-Maintainer-Eingaben und stehen
auf `ready`. Der Gesamtstatus wurde **nicht** automatisch aus den Einzelwerten
abgeleitet (Abschlussregel 4); er beruht ausschließlich auf der ausdrücklichen
Entscheidung des Human Maintainers. **Kein Implementation Agent hat den DRC für
bestanden erklärt.** Die Freigabe ist **rein dokumentarisch** und **weder** eine
Installations-, **noch** eine Betriebs-, Security-Readiness-, Mapping- oder
Capability-Freigabe.

---

## Profil-A-Zielbild

Dokumentiert in
[DEPLOYMENT_PROFILES.md](../docs/architecture/DEPLOYMENT_PROFILES.md), Abschnitt
*Pilot Profile-A Target Specification*: Proxmox-VE-VM, Einzelhost, Ubuntu Server
26.04 LTS amd64, 4 vCPU, 8 GiB RAM, 64 GiB System- und 250 GiB Datendisk,
NVMe-LVM-Thin, private Bridge mit statisch reservierter Adresse im privaten LAN,
WireGuard-Fernzugriff, Docker Compose in der VM, tägliches Proxmox-Backup auf
physisch separate NAS, RPO 24 h, RTO 8 h.

**Ausdrücklich:** keine Produktmindestanforderung · keine
Proxmox-API-Berechtigung · kein Betrieb auf dem Hypervisor-Host · keine
öffentliche Freigabe · keine konkrete Adresse · keine konkrete NAS-Kennung ·
**keine Installation ausgeführt** · Zielbild dokumentiert, **nicht deployed**.

---

## Offene Punkte

| Punkt | Zuständig |
| --- | --- |
| CBP-/RT-2-Restore mit Integritätsprüfung | Security Foundation Readiness Gate, **Punkt 19** — nicht erbracht |
| RT-2-Backup-Nachweis | Security Foundation Readiness Gate, **Punkt 18** — nicht erbracht |
| Durchsetzung von KB-01…KB-12 | Security Foundation Readiness Gate — `NOT EVALUATED` |
| **R-20** | **offen** — durch die DRC-Freigabe **nicht** geschlossen |

**Alle 19 DRC-Einzelkriterien sind erhoben und angenommen**, und die
**Gesamtfreigabe für Profil A ist am 2026-07-29 erteilt**. Es ist **kein**
Prüfpunkt `blocked` oder `not-evaluated`. **Der nächste technische Schritt ist
weiterhin nicht autorisiert.**

**Weiterhin außerhalb des DRC:** **OD-20** (Programmiersprache, Suchmaschine,
Embedding-Modell) bleibt einem späteren Capability-Paket zugeordnet — die
Programmiersprache ist durch CBP-WP-012 bereits faktisch festgelegt, Suchmaschine
und Embedding-Modell gehören zu Capability 9 (mit OD-25).

---

## Aussageschutz

Dieses Work Package belegt **nicht**:

| Nicht belegt | Tatsächlicher Stand |
| --- | --- |
| Eine Kontrolle sei implementiert, getestet oder enforced | **12 KB-Kontrollen `DOCUMENTED ONLY`** |
| Das Deployment sei bereit | DRC **APPROVED BY HUMAN MAINTAINER** ist **dokumentarisch**; **keine Installation, keine Bereitstellung** |
| Eine Installation sei freigegeben | **nein** — die Bereitstellung bleibt einem separaten, ausdrücklich autorisierten Work Package vorbehalten |
| Das Security Gate sei ausgewertet | **NOT EVALUATED** |
| Das Mapping Gate sei freigegeben | **NOT EVALUATED** |
| Eine Capability sei implementiert | **0 von 29** |
| RT-2 existiere | kein Speicher, keine Verkettung, kein Backup |

**Es wurde keine reale Infrastruktur berührt.** Kein Hypervisor-, NAS-, Netz-
oder Zielsystemzugriff; keine Portprüfung, keine Prozessprüfung, keine
Secret-Auflösung.

---

## Do-not-start-Scope

Nicht durchgeführt und nicht autorisiert: Installation · VM-Erstellung ·
Änderung von Proxmox-Host, NAS oder Netzwerkinfrastruktur · Netzwerkzugriff ·
Zielsystem-, Port- oder Prozessprüfung · UID-/GID-Ermittlung · Dokumentation
konkreter Adressen · Secret-Auflösung oder Secret-Werte · Runtime-Code ·
Teständerungen · RT-2-Erzeugung · Persistenz · Backupausführung · neuer
Restore-Test · CBP-Datenrestore · Security-Evaluation · Enforcement ·
Mapping-Gate-Ausführung · Gatefreigabe · Betriebsfreigabe · Capability-Freigabe ·
Aktivierung · ADR · weitere Decision · neue Risiko-ID · Commit · Push · Tag ·
Release · CBP-WP-020.

**R-33 bleibt in diesem uncommitteten Lauf unverändert bei 15 Konsistenzvorgängen
in 18 Work Packages.** `RISK_REGISTER.md` und `COMPLIANCE_CHECK.md` wurden
**nicht** verändert.

---

## Abschluss — Post-Commit-Reconciliation (Phase C)

| Feld | Wert |
| --- | --- |
| Status | **`committed`** |
| Phase | **complete** |
| Commit | **`3c437f2`** |
| Commit-Betreff | `CBP-WP-019: approve profile A deployment readiness` |
| Parent | `707003d` |
| Geänderte Pfade im Commit | **13** (12 modifiziert, 1 neu) |
| Commit-Autorität | **Human Maintainer** |
| Push nach `origin/main` | **bestätigt** — lokaler HEAD und `origin/main` identisch |
| Abschlussdatum | **2026-07-29** |
| Human DRC Decision | **APPROVED BY HUMAN MAINTAINER**, Profil **A** |
| DRC | **19 `ready`**, **0 `blocked`** |
| Capabilities | **0 von 29** |
| Runtime-Gates | Mapping Activation `NOT EVALUATED` · Security Foundation Readiness `NOT EVALUATED` |
| R-20 | **offen** |
| R-33 | **16 / 19** nach der Post-Commit-Reconciliation |

**Kein Work Package ist aktiv.** Zuletzt abgeschlossen ist **CBP-WP-019**. Ein
**nächstes autorisiertes Work Package existiert nicht**; **CBP-WP-020 ist nicht
registriert, nicht begonnen und nicht autorisiert**.

**Die Post-Commit-Reconciliation ist kein neues fachliches Work Package.** Sie
hat weder eine Entscheidung getroffen noch einen Vertrag geändert: **keine neue
Decision, kein ADR, keine neue Risiko-ID, keine Änderung am DRC-Vertrag, keine
Änderung an D-054**.

**Unverändert und ausdrücklich nicht erfolgt:** keine Installation, keine
Bereitstellung, keine Betriebs- oder Produktivfreigabe, keine
Security-Readiness-Freigabe, keine Mapping-Aktivierung, keine Gateauswertung,
keine Capability-Freigabe, keine Source-Aktivierung, kein RT-2, keine
Persistenz, keine Folgeautorisierung.
