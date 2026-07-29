# Deployment Readiness Check (DRC)

| Feld | Wert |
| --- | --- |
| Prüfmodell | **Deployment Readiness Check**, Abkürzung **DRC** |
| **Status** | **APPROVED BY HUMAN MAINTAINER** — für **Profil A**, 2026-07-29; alle 19 Einzelkriterien `ready` (CBP-WP-019, D-054). **Keine Installations-, Betriebs- oder Security-Freigabe** |
| Phase | Erfasst in Phase 0; **erstmals vollständig erhoben in Phase 1** |
| Erfasst in | CBP-WP-004 · **erhoben in CBP-WP-019** |
| Autoritätsklasse | A3 |
| Prüfpunkte | **19** (17 G0-abgeleitet + 2 ohne G0-Herkunft) |
| Stand | 2026-07-29 |

---

## Was der DRC ist — und was nicht

| Ist | Ist nicht |
| --- | --- |
| Ein **fail-closed Prüfmodell** vor einer konkreten Installation | Ein zusätzliches Governance-Framework |
| Eine Checkliste je Deploymentprofil | Ein Ersatz für NDF v1.0.0 |
| Pro Profil **separat** auszuführen | Einmal global bestanden |
| Nachweisbasiert | Durch Absichtserklärung erfüllbar |

**Fail-closed bedeutet:** Fehlt ein für das gewählte Profil erforderlicher
Nachweis, wird **nicht installiert**. Ein unbekannter Wert ist kein
„vermutlich in Ordnung".

**Der DRC ist nicht automatisch bestanden.** Sein Ausgangszustand ist
`NOT EVALUATED`, und er bleibt es, bis ein Mensch die Nachweise erbringt.

## Verhältnis zu G0

| Gate | Sperrt | Kriterienklasse |
| --- | --- | --- |
| **G0 – Discovery and Scope Lock** | Den allgemeinen Produkt- und Architektur-Scope | **Core Required** (25) |
| **DRC** | Eine **konkrete Installation** eines gewählten Profils | **Deployment Required** (16) |

Die 16 Deployment-Required-Kriterien **blockieren G0 nicht**. Sie sind hierher
verlagert — **vertagt, nicht gestrichen**. Genau dafür existiert dieses
Dokument: damit sie nicht vergessen werden (Risiko R-34).

Der DRC ist auch **kein Ersatz** für die spätere Betriebsphase. Er prüft die
Bereitschaft vor der Installation, nicht den laufenden Betrieb.

## Statuswerte

### Je Prüfpunkt

Diese vier Werte sind **unverändert** und gelten ausschließlich für einzelne
Prüfpunkte:

| Status | Bedeutung |
| --- | --- |
| `not-evaluated` | Nicht geprüft — Ausgangszustand |
| `ready` | Nachweis erbracht und angenommen |
| `blocked` | Nachweis fehlt oder ist unzureichend; Installation gesperrt |
| `not-applicable` | Für das gewählte Profil nicht einschlägig |

### Gesamtstatus je Profil

Der Gesamtstatus ist **getrennt** von den Einzelwerten und wird **nie**
automatisch aus ihnen abgeleitet:

| Gesamtstatus | Bedeutung | Wer stellt fest |
| --- | --- | --- |
| **NOT EVALUATED** | Keine Gesamtentscheidung getroffen — Ausgangszustand | — |
| **BLOCKED** | Mindestens ein einschlägiger Prüfpunkt `blocked` oder ungeprüft | Prüfung oder Mensch |
| **APPROVED BY HUMAN MAINTAINER** | Die Deployment-Readiness-Werte des Profils sind **dokumentiert und angenommen** | **ausschließlich der Human Maintainer** |

**`APPROVED BY HUMAN MAINTAINER` ist eine dokumentarische Feststellung, keine
technische.** Sie besagt, dass die erforderlichen Werte erhoben und akzeptiert
sind — **nicht**, dass installiert, bereitgestellt, betrieben oder eine
Sicherheitskontrolle geprüft werden darf.

---

## Kriterienkatalog

Alle 16 Deployment-Required-Kriterien aus
[G0_SCOPE_LOCK_CRITERIA.md](../discovery/G0_SCOPE_LOCK_CRITERIA.md) sind hier
abgebildet. Die Spalte **G0-Herkunft** stellt die Rückverfolgbarkeit sicher.

> **Struktur seit CBP-WP-019 (D-054).** Der Katalog umfasst **19 Prüfpunkte**:
> **17** sind aus den **16** Deployment-Required-G0-Kriterien abgeleitet (drei
> Kriterien fächern auf, zwei Paare fallen zusammen), **zwei** besitzen **keine
> unmittelbare G0-Herkunft** — **DRC-01** (Profilwahl, aus D-015) und
> **DRC-19** (RT-2-Aufbewahrung, aus D-037 / OD-35 / RET-2). Die Zahl **16**
> der G0-Kriterien bleibt unverändert; der **historische G0-Nachweis wird nicht
> geändert**.

| ID | Kategorie | G0-Herkunft | Profilbezug | Erforderlicher Nachweis | Owner | Status | Blockiert Deployment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DRC-01 | Gewähltes Deploymentprofil | — | alle | Ausdrückliche Profilwahl A–E; für den Pilot durch D-015 auf **A** festgelegt | Human Maintainer | **`ready`** | **ja** |
| DRC-02 | Konkrete Plattformversion | **B-1** | A, B, C, D | Versionsstring der Plattform beziehungsweise Distribution | Human Maintainer | **`ready`** | **ja** |
| DRC-03 | Hosttopologie | **B-2** | A | Einzelhost oder Cluster; bei Cluster Knotenzahl | Human Maintainer | **`ready`** | **ja** |
| DRC-04 | CPU | **B-3** | alle | Zusagbare Kernzahl | Human Maintainer | **`ready`** | **ja** |
| DRC-05 | RAM | **B-4** | alle | Zusagbare Speichergröße | Human Maintainer | **`ready`** | **ja** |
| DRC-06 | System- und Datenspeicher | **B-5** | alle | Kapazität, **getrennt** nach System und Daten | Human Maintainer | **`ready`** | **ja** |
| DRC-07 | Storage-Technologie | **B-6** | A, B, C | ZFS, LVM oder andere; Snapshot-Fähigkeit | Human Maintainer | **`ready`** | **ja** |
| DRC-08 | Privater Netzwerkzugriff | **C-1, C-2** | alle außer E | Gewählte Lösung: bestehendes VPN, Tailscale, WireGuard oder vergleichbar. **Profil bereits durch D-023 festgelegt**, Technologie offen | Human Maintainer | **`ready`** | **ja** |
| DRC-09 | Ausgehende Netzwerkverbindungen | **C-5** | alle | Allowlist der erlaubten Ziele **als Zielklassen**. Grundsatz „keine öffentliche Freigabe" durch D-023 bereits entschieden | Human Maintainer | **`ready`** | **ja** |
| DRC-10 | Benutzer und Geräte | **A-3, C-6** | alle | Gerätezahl nach Typ; mobile Zugriffsmethode. **Bestätigt:** **2** Desktop-/Notebook-Geräte, **3** mobile Geräte; mobiler Zugriff über **WireGuard** | Human Maintainer | **`ready`** | **ja** |
| DRC-11 | Backupziel | **B-7** | alle | Ziel, Verfahren, Zuständigkeit. **Bestätigt:** integrierte **Proxmox-VE-Backupfunktion** auf **physisch separate NAS** im privaten Netzwerk; Zuständigkeit **Human Maintainer / Betreiber** | Human Maintainer | **`ready`** | **ja** |
| DRC-12 | Externe Backupkopie | **B-8** | alle | Ziel **außerhalb** des Hosts, oder ausdrückliche Risikoübernahme | Human Maintainer | **`ready`** | **ja** |
| DRC-13 | Backupfrequenz | **B-7** | alle | Intervall je Datenklasse (kanonisch / abgeleitet). **Bestätigt:** vollständiges **VM-Backup wöchentlich**; **kanonische CBP-Daten täglich**; vollständig reproduzierbare abgeleitete Daten **ohne** eigenes Backup (Rebuild aus kanonisch + Registry) | Human Maintainer | **`ready`** | **ja** |
| DRC-14 | RPO | **F-4** | alle | Maximal tolerierter Datenverlust, als Zeitwert | Human Maintainer | **`ready`** | **ja** |
| DRC-15 | RTO | **F-4** | alle | Maximale Wiederherstellungsdauer, als Zeitwert | Human Maintainer | **`ready`** | **ja** |
| DRC-16 | **Restore-Test des Betreiber-Backup-Regimes** | **F-4** | alle | Beschriebener und **tatsächlich durchgeführter** Wiederherstellungstest der vorgesehenen **Betreiber-Backuptechnik** beziehungsweise derselben Plattform- und Werkzeugklasse. Der Test darf auf einem **anderen kontrollierten System** derselben Klasse erbracht worden sein. **Nicht Gegenstand:** CBP-Daten, RT-2, Security-Control-Evidenz, Mapping-Evidenz | Human Maintainer | **`ready`** | **ja** |
| DRC-17 | Secret-Verwaltung | **E-1** | alle | Wo und wie Betriebsgeheimnisse verwaltet werden — **getrennt vom Wissensbestand**. Keine Werte, nur das Verfahren. **Bestätigt (inkl. OD-34-Restpunkte):** Providerklasse **betriebssystemgeschützter Datei-Provider**; registrierter Providertyp **`file`**; Schutzklasse **nur berechtigte Service- und Betreiberrollen lesbar**; berechtigte Service-Identitätsklassen **`svc-control-plane`** und **`svc-data-worker`**; Rotation **kontrollierter manueller Austausch der Referenz**; Widerruf **alte Referenz sperren und ersetzen**; Rolle **Human Maintainer / Betreiber** | Human Maintainer | **`ready`** | **ja** |
| DRC-18 | Betriebsverantwortung | **D-2, E-1** | alle | Wer betreibt, patcht, überwacht; Bestandsgrößenordnung für die Dimensionierung. **Bestätigt:** Betrieb, Updates/Patches sowie Überwachung und Störungsbehandlung durch die Rolle **Human Maintainer / Betreiber**; erwartete Bestandsgrößenordnung **1.000 bis 10.000 Dokumente** | Human Maintainer | **`ready`** | **ja** |
| **DRC-19** | **RT-2-Aufbewahrung** | **—** *(Post-G0, aus D-037 / OD-35 / RET-2)* | alle | Aufbewahrungsdauer **je `retention_class`**, Lösch- beziehungsweise Archivierungsverfahren, Owner-Rolle. **Bestätigt:** **Mindestaufbewahrung 365 Tage** für **alle** `retention_class`-Werte einschließlich Security- und Incident-Evidenz; **danach dauerhafte Aufbewahrung**; **keine automatische Löschung**; **kein separates Archiv**; Owner **Human Maintainer / Betreiber** | Human Maintainer | **`ready`** | **ja** |

### DRC-16 — Aussagegrenze

**DRC-16 belegt ausschließlich, dass die Backup- und Wiederherstellungskette des
Betreibers real erprobt ist** — dass eine Sicherung mit der vorgesehenen
Werkzeugklasse tatsächlich zurückgespielt werden kann. Genau das adressiert
R-20 („eine ungeprüfte Sicherung ist keine Sicherung").

**DRC-16 belegt ausdrücklich nicht:**

| Nicht belegt | Zuständig |
| --- | --- |
| Restore der künftigen CBP-VM | Deployment, später |
| Restore von CBP-Daten oder kanonischen Registry-Metadaten | Security Foundation Readiness Gate, **Punkt 19** |
| Restore von **RT-2 Operational Evidence** | Security Foundation Readiness Gate, **Punkt 19** |
| Integritätsprüfung einer RT-2-Hashkette | Security Foundation Readiness Gate, **Punkt 19** |
| Automatisierter oder repository-verifizierter Nachweis | — |

Der Nachweis ist eine **Human-Maintainer-Attestation**. Der spätere
CBP-/RT-2-Restore mit Integritätsprüfung bleibt **Nachweisstufe 5** im
[Security Foundation Readiness Gate](SECURITY_FOUNDATION_READINESS_GATE.md)
(Punkt 19) und ist **nicht erbracht**. **R-20 bleibt offen.**

### DRC-09 — Egress-Zielklassen

Dokumentiert werden ausschließlich **Zielklassen**, keine Domains, Adressen oder
Endpunkte:

```text
- Betriebssystem-Paket- und Security-Repositories
- ausdrücklich benötigte Container-Registries
- DNS-Dienste
- NTP-Zeitdienste
- Zertifikats-, Renewal- und Revocation-Dienste
- ausdrücklich freigegebene Git-/Artefaktquellen
```

**Alle nicht ausdrücklich freigegebenen Ziele sind verboten** (deny-by-default,
KB-10). Die **technische Enforcement-Prüfung bleibt offen** — die Allowlist ist
dokumentiert, nicht durchgesetzt.

### Abdeckung der 16 Deployment-Required-Kriterien

| G0-Kriterium | DRC |
| --- | --- |
| A-3 Zahl der Geräte | DRC-10 |
| B-1 Plattformversion | DRC-02 |
| B-2 Einzelhost oder Cluster | DRC-03 |
| B-3 CPU | DRC-04 |
| B-4 RAM | DRC-05 |
| B-5 Speicher | DRC-06 |
| B-6 Storage-Technologie | DRC-07 |
| B-7 Backupziele | DRC-11, DRC-13 |
| B-8 Externe Backupkopie | DRC-12 |
| C-1 Bestehendes VPN | DRC-08 |
| C-2 Tailscale/WireGuard | DRC-08 |
| C-5 Ausgehende Verbindungen | DRC-09 |
| C-6 Mobile Zugriffsmethode | DRC-10 |
| D-2 Größenordnung | DRC-18 |
| E-1 Claude-Desktop-Nutzung | DRC-17, DRC-18 |
| F-4 Backup-/Restore-Zielwerte | DRC-14, DRC-15, DRC-16 |

**16 von 16 abgedeckt** — auf **17** Prüfpunkte, weil einige G0-Kriterien in
mehrere zerfallen (F-4 in RPO, RTO und Restore-Test; B-7 in Ziel und Frequenz;
E-1 in Secret-Verwaltung und Betriebsverantwortung) und zwei Paare
zusammenfallen (C-1/C-2 auf DRC-08; A-3/C-6 auf DRC-10).

**Zwei Prüfpunkte haben keine unmittelbare G0-Herkunft** und sind in dieser
Abdeckungstabelle bewusst **nicht** enthalten:

| Prüfpunkt | Herkunft | Warum kein G0-Kriterium |
| --- | --- | --- |
| **DRC-01** Profilwahl | **D-015** | Die Profilwahl steuert die Anwendbarkeit der übrigen Punkte; sie ist keine erhobene Infrastrukturangabe |
| **DRC-19** RT-2-Aufbewahrung | **D-037 / OD-35 / RET-2** (CBP-WP-019, D-054) | Post-G0-Erweiterung: RT-2 als nicht reproduzierbare Evidenzklasse entstand erst mit ADR-0007/ADR-0009, nach dem G0-Kriterienschnitt |

**17 + 2 = 19 Prüfpunkte.** Die Zahl der Deployment-Required-G0-Kriterien bleibt
**16**; der historische G0-Nachweis in
[G0_SCOPE_LOCK_CRITERIA.md](../discovery/G0_SCOPE_LOCK_CRITERIA.md) wird
**nicht rückwirkend geändert**.

## Profilabhängigkeit

| Kriterium | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| DRC-03 Hosttopologie | ja | `n/a` | `n/a` | `n/a` | `n/a` |
| DRC-07 Storage-Technologie | ja | ja | ja | Host | `n/a` |
| DRC-08 Privates Netz | ja | ja | ja | ja | `n/a` |
| DRC-10 Mehrgeräte/mobil | ja | ja | ja | ja | eingeschränkt |
| DRC-12 Externe Kopie | ja | ja | **zwingend** | ja | **zwingend** |
| DRC-19 RT-2-Aufbewahrung | ja | ja | ja | ja | ja |
| Alle übrigen | ja | ja | ja | ja | ja |

`n/a` bedeutet `not-applicable` — nicht „erfüllt".

## Abschlussregel

Der DRC gilt für ein Profil als bestanden, wenn:

1. Alle für dieses Profil einschlägigen Kriterien auf `ready` stehen.
2. Kein Kriterium auf `blocked` steht.
3. **DRC-16 ist erbracht** — der Restore-Test wurde tatsächlich durchgeführt,
   nicht nur beschrieben. Eine ungeprüfte Sicherung ist keine Sicherung (R-20).
   Maßgeblich ist der **Prüfumfang des Betreiber-Backup-Regimes**; der
   CBP-/RT-2-Restore ist **nicht** Gegenstand dieser Bedingung, sondern des
   Security Foundation Readiness Gate (Punkt 19).
4. Der Human Maintainer entscheidet ausdrücklich über den Gesamtstatus.

Bedingung 4 ist eigenständig. Kein Implementation Agent stellt fest, dass der
DRC bestanden ist.

> **Präzisierung durch die Freigabe vom 2026-07-29 (Profil A).** Der Human
> Maintainer hat Bedingung 4 ausgeübt und den Gesamtstatus auf
> **APPROVED BY HUMAN MAINTAINER** gesetzt — **ausdrücklich beschränkt auf die
> dokumentarische Deployment-Readiness**. Die Freigabe der **tatsächlichen
> Installation** ist damit **nicht** erteilt; sie bleibt einem **separaten,
> ausdrücklich autorisierten Work Package** vorbehalten. Der DRC bestätigt, dass
> die erforderlichen Werte vorliegen — **nicht**, dass installiert werden darf.

## Aktueller Stand

Vollständige Erhebung für **Profil A** durch den Human Maintainer
(CBP-WP-019, **D-054**).

| Kennzahl | Wert |
| --- | --- |
| DRC-Prüfpunkte | **19** |
| davon G0-abgeleitet | **17** (aus 16 G0-Kriterien) |
| davon ohne G0-Herkunft | **2** — DRC-01, DRC-19 |
| abgedeckte G0-Deployment-Kriterien | **16 von 16** |
| `ready` | **19** |
| `blocked` | **0** |
| `not-applicable` | **0** |
| `not-evaluated` | **0** |

**DRC-Gesamtstatus: APPROVED BY HUMAN MAINTAINER** — Profil A, **2026-07-29**.

**Der Gesamtstatus wurde nicht automatisch aus den 19 Einzelstatuswerten
abgeleitet.** Er beruht ausschließlich auf der **ausdrücklichen Entscheidung des
Human Maintainers** vom 2026-07-29 (Abschlussregel 4). Kein Implementation Agent
hat den DRC für bestanden erklärt.

**Es wurde keine reale Infrastruktur bewertet, geprüft oder bereitgestellt.**
Die dokumentierten Angaben sind **Zusagen des Human Maintainers**, keine vom
Repository verifizierten Messwerte. Es fand **kein** Zugriff auf Hypervisor,
Speicher, Netzwerk oder Sicherungsziel statt.

### Human-Maintainer-Freigabe — Profil A

| Feld | Wert |
| --- | --- |
| Profil | **A** |
| Einzelkriterien | **19 `ready`**, 0 `blocked` |
| Gesamtstatus | **APPROVED BY HUMAN MAINTAINER** |
| Freigabedatum | **2026-07-29** |
| Autorität | **Human Maintainer** (A0) |
| Rechtsgrund | Ausführung des in **D-054** vorgesehenen Human Gates — **keine** zusätzliche Decision |

**Genehmigter Bedeutungsumfang.** Die für Profil A erforderlichen
Deployment-Readiness-Werte sind **dokumentiert und vom Human Maintainer
akzeptiert**. Eine erste kontrollierte technische Bereitstellung darf in einem
**späteren, ausdrücklich autorisierten Work Package vorbereitet** werden.

**Ausdrücklich nicht genehmigt.** Die Freigabe ist **keine**:

| Nicht genehmigt |
| --- |
| Installation · Bereitstellung · Betriebsfreigabe · Produktivfreigabe |
| Security-Readiness-Freigabe |
| Bestätigung **implementierter**, **getesteter** oder **erzwungener** Sicherheitskontrollen |
| Mapping-Aktivierung · Gate-Ausführung · Gatefreigabe |
| Capability-Freigabe · Source-Aktivierung |
| RT-2-Betriebsfreigabe |
| Backup- oder Restore-Evidenz für CBP beziehungsweise RT-2 |

**Der nächste technische Schritt ist weiterhin nicht autorisiert.** Die zwölf
KB-Kontrollen bleiben `DOCUMENTED ONLY`; Mapping Activation Gate und Security
Foundation Readiness Gate bleiben `NOT EVALUATED`; Capabilities bleiben
**0 von 29**. **CBP-WP-020 ist nicht registriert, nicht begonnen und nicht
autorisiert.**

## Verbleibende offene Punkte

**Alle 19 Einzelkriterien sind erhoben und angenommen.** Es ist **kein**
Prüfpunkt `blocked` oder `not-evaluated`, und die Gesamtfreigabe für **Profil A**
ist erteilt.

Weiterhin offen bleiben — **außerhalb** des DRC:

| Punkt | Ort |
| --- | --- |
| CBP-/RT-2-Restore mit Integritätsprüfung | Security Foundation Readiness Gate, **Punkt 19** — nicht erbracht |
| RT-2-Backup-Nachweis | Security Foundation Readiness Gate, **Punkt 18** — nicht erbracht |
| Durchsetzung von KB-01…KB-12 | Security Foundation Readiness Gate — `NOT EVALUATED` |
| **R-20** (Restore-Evidenz) | **offen** — durch diese Freigabe **nicht** geschlossen |

**Geschlossen durch CBP-WP-019 (D-054):** Linux-Distribution und
VM-Ressourcengröße · VPN-Technologie (Restpunkt zu **OD-21**, das bereits durch
**D-023** geschlossen ist) · Backuptechnik, -ziel und -frequenz (**OD-22**) ·
RPO- und RTO-Zielwerte (**OD-30**) · Gerätezahl und Zugriffsmethode ·
Secret-Provider-Deploymentwerte (**OD-34-Restpunkte**) · Betriebsverantwortung
und Bestandsgrößenordnung · RT-2-Aufbewahrung (**OD-35 / RET-2**).

**Nicht Gegenstand des DRC:** Programmiersprache, Suchmaschine und
Embedding-Modell (**OD-20**) bleiben einem späteren Capability-Paket
zugeordnet — sie sind Produktarchitektur, keine Deploymentbereitschaft.

## Pflege

Ein DRC-Kriterium wechselt den Status nur mit hinterlegtem Nachweis und nur für
ein benanntes Profil. Der DRC wird bei jedem Profilwechsel **neu** ausgeführt —
ein für Profil A bestandener DRC sagt nichts über Profil D aus.
