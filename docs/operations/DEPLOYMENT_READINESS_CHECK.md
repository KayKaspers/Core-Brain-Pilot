# Deployment Readiness Check (DRC)

| Feld | Wert |
| --- | --- |
| Prüfmodell | **Deployment Readiness Check**, Abkürzung **DRC** |
| **Status** | **NOT EVALUATED** |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-004 |
| Autoritätsklasse | A3 |
| Stand | 2026-07-20 |

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

| Status | Bedeutung |
| --- | --- |
| `not-evaluated` | Nicht geprüft — Ausgangszustand |
| `ready` | Nachweis erbracht und angenommen |
| `blocked` | Nachweis fehlt oder ist unzureichend; Installation gesperrt |
| `not-applicable` | Für das gewählte Profil nicht einschlägig |

---

## Kriterienkatalog

Alle 16 Deployment-Required-Kriterien aus
[G0_SCOPE_LOCK_CRITERIA.md](../discovery/G0_SCOPE_LOCK_CRITERIA.md) sind hier
abgebildet. Die Spalte **G0-Herkunft** stellt die Rückverfolgbarkeit sicher.

| ID | Kategorie | G0-Herkunft | Profilbezug | Erforderlicher Nachweis | Owner | Status | Blockiert Deployment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DRC-01 | Gewähltes Deploymentprofil | — | alle | Ausdrückliche Profilwahl A–E; für den Pilot durch D-015 auf **A** festgelegt | Human Maintainer | `not-evaluated` | **ja** |
| DRC-02 | Konkrete Plattformversion | **B-1** | A, B, C, D | Versionsstring der Plattform beziehungsweise Distribution | Human Maintainer | `not-evaluated` | **ja** |
| DRC-03 | Hosttopologie | **B-2** | A | Einzelhost oder Cluster; bei Cluster Knotenzahl | Human Maintainer | `not-evaluated` | **ja** |
| DRC-04 | CPU | **B-3** | alle | Zusagbare Kernzahl | Human Maintainer | `not-evaluated` | **ja** |
| DRC-05 | RAM | **B-4** | alle | Zusagbare Speichergröße | Human Maintainer | `not-evaluated` | **ja** |
| DRC-06 | System- und Datenspeicher | **B-5** | alle | Kapazität, **getrennt** nach System und Daten | Human Maintainer | `not-evaluated` | **ja** |
| DRC-07 | Storage-Technologie | **B-6** | A, B, C | ZFS, LVM oder andere; Snapshot-Fähigkeit | Human Maintainer | `not-evaluated` | **ja** |
| DRC-08 | Privater Netzwerkzugriff | **C-1, C-2** | alle außer E | Gewählte Lösung: bestehendes VPN, Tailscale, WireGuard oder vergleichbar. **Profil bereits durch D-023 festgelegt**, Technologie offen | Human Maintainer | `not-evaluated` | **ja** |
| DRC-09 | Ausgehende Netzwerkverbindungen | **C-5** | alle | Allowlist der erlaubten Ziele. Grundsatz „keine öffentliche Freigabe" durch D-023 bereits entschieden | Human Maintainer | `not-evaluated` | **ja** |
| DRC-10 | Benutzer und Geräte | **A-3, C-6** | alle | Gerätezahl nach Typ; mobile Zugriffsmethode | Human Maintainer | `not-evaluated` | **ja** |
| DRC-11 | Backupziel | **B-7** | alle | Ziel, Verfahren, Zuständigkeit | Human Maintainer | `not-evaluated` | **ja** |
| DRC-12 | Externe Backupkopie | **B-8** | alle | Ziel **außerhalb** des Hosts, oder ausdrückliche Risikoübernahme | Human Maintainer | `not-evaluated` | **ja** |
| DRC-13 | Backupfrequenz | **B-7** | alle | Intervall je Datenklasse (kanonisch / abgeleitet) | Human Maintainer | `not-evaluated` | **ja** |
| DRC-14 | RPO | **F-4** | alle | Maximal tolerierter Datenverlust, als Zeitwert | Human Maintainer | `not-evaluated` | **ja** |
| DRC-15 | RTO | **F-4** | alle | Maximale Wiederherstellungsdauer, als Zeitwert | Human Maintainer | `not-evaluated` | **ja** |
| DRC-16 | Restore-Testverfahren | **F-4** | alle | Beschriebener und **durchgeführter** Wiederherstellungstest | Human Maintainer | `not-evaluated` | **ja** |
| DRC-17 | Secret-Verwaltung | **E-1** | alle | Wo und wie Betriebsgeheimnisse verwaltet werden — **getrennt vom Wissensbestand**. Keine Werte, nur das Verfahren | Human Maintainer | `not-evaluated` | **ja** |
| DRC-18 | Betriebsverantwortung | **D-2, E-1** | alle | Wer betreibt, patcht, überwacht; Bestandsgrößenordnung für die Dimensionierung | Human Maintainer | `not-evaluated` | **ja** |

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

**16 von 16 abgedeckt.** Die 18 DRC-Kriterien entstehen, weil einige
G0-Kriterien in mehrere Prüfpunkte zerfallen — etwa F-4 in RPO, RTO und
Restore-Test.

## Profilabhängigkeit

| Kriterium | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| DRC-03 Hosttopologie | ja | `n/a` | `n/a` | `n/a` | `n/a` |
| DRC-07 Storage-Technologie | ja | ja | ja | Host | `n/a` |
| DRC-08 Privates Netz | ja | ja | ja | ja | `n/a` |
| DRC-10 Mehrgeräte/mobil | ja | ja | ja | ja | eingeschränkt |
| DRC-12 Externe Kopie | ja | ja | **zwingend** | ja | **zwingend** |
| Alle übrigen | ja | ja | ja | ja | ja |

`n/a` bedeutet `not-applicable` — nicht „erfüllt".

## Abschlussregel

Der DRC gilt für ein Profil als bestanden, wenn:

1. Alle für dieses Profil einschlägigen Kriterien auf `ready` stehen.
2. Kein Kriterium auf `blocked` steht.
3. **DRC-16 ist erbracht** — der Restore-Test wurde tatsächlich durchgeführt,
   nicht nur beschrieben. Eine ungeprüfte Sicherung ist keine Sicherung (R-20).
4. Der Human Maintainer gibt die Installation ausdrücklich frei.

Bedingung 4 ist eigenständig. Kein Implementation Agent stellt fest, dass der
DRC bestanden ist.

## Aktueller Stand

| Kennzahl | Wert |
| --- | --- |
| DRC-Kriterien | 18 |
| abgedeckte G0-Deployment-Kriterien | **16 von 16** |
| `ready` | **0** |
| `blocked` | 0 |
| `not-applicable` | 0 |
| `not-evaluated` | **18** |

**DRC-Status: NOT EVALUATED.**

**Es wurde keine reale Infrastruktur bewertet oder bereitgestellt.** Die
Angaben zu Proxmox, CPU, RAM, Storage, Netzwerk und Backup sind in Phase 0
bewusst nicht erhoben worden.

## Verbleibende offene Entscheidungen

| Punkt | Register |
| --- | --- |
| Linux-Distribution und VM-Ressourcengröße | Fragebogen 1.9, 1.10 |
| VPN-Technologie | DRC-08, OD-21 vertagt |
| Backupsoftware, -ziel und -frequenz | OD-22 |
| RPO- und RTO-Zielwerte | OD-30 |
| Betriebsverantwortung | DRC-18 |

## Pflege

Ein DRC-Kriterium wechselt den Status nur mit hinterlegtem Nachweis und nur für
ein benanntes Profil. Der DRC wird bei jedem Profilwechsel **neu** ausgeführt —
ein für Profil A bestandener DRC sagt nichts über Profil D aus.
