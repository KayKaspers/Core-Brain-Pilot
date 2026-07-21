# Human-Maintainer-Fragebogen — Discovery Phase 0

| Feld | Wert |
| --- | --- |
| Gate G0 | **PASSED WITH NOTES** — 2026-07-21, A0 |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Überarbeitet in | CBP-WP-008 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

Dies ist der **einzige** Fragebogen des Projekts. **Keine Frage wird durch
Annahme beantwortet.**

## Prioritäten und Kriterienklassen

| Prio | Bedeutung |
| --- | --- |
| **P0** | Blockiert G0 — **nur noch, wenn Core Required** |
| **P1** | Vor der Architekturentscheidung erforderlich |
| **P2** | Später beantwortbar |

Seit CBP-WP-003 gilt zusätzlich die Klasse des zugehörigen G0-Kriteriums:

| Klasse | Wirkung |
| --- | --- |
| **Core** | Blockiert G0 |
| **Depl** | Deployment Required — blockiert erst die Installation |
| **Cond** | Conditional — blockiert nur bei aktivierter Funktion |

Antwortstände stammen aus
[HUMAN_DISCOVERY_INPUT.md](HUMAN_DISCOVERY_INPUT.md) (Kürzel **HDI**).

---

## 1 — Infrastruktur

| # | Frage | Prio | G0 | Klasse | Status |
| --- | --- | --- | --- | --- | --- |
| 1.1 | Proxmox-Version | P0 | B-1 | Depl | offen, vertagt |
| 1.2 | Einzelhost oder Cluster | P0 | B-2 | Depl | offen, vertagt |
| 1.3 | CPU-Kerne für die VM | P0 | B-3 | Depl | offen, vertagt |
| 1.4 | RAM für die VM | P0 | B-4 | Depl | offen, vertagt |
| 1.5 | Speicher, System- und Datendisk | P0 | B-5 | Depl | offen, vertagt |
| 1.6 | Storage-Technologie | P0 | B-6 | Depl | offen, vertagt |
| 1.7 | Backupziele, Verfahren, Frequenz | P0 | B-7 | Depl | offen, vertagt |
| 1.8 | Backupkopie außerhalb des Hosts | P0 | B-8 | Depl | offen, vertagt |
| 1.9 | Linux-Distribution für die VM | P1 | F-1 | Depl | offen |
| 1.10 | VM-Ressourcengröße | P1 | F-1 | Depl | offen |

Die Antwort auf HDI A1 legt das **Profil** fest (Proxmox-VM), nicht die Werte.
Sämtliche konkreten Werte bleiben bewusst unerhoben.

## 2 — Netzwerk

| # | Frage | Prio | G0 | Klasse | Status |
| --- | --- | --- | --- | --- | --- |
| 2.1 | Bestehendes VPN | P0 | C-1 | Depl | **HDI A5** — privates Netz gewählt, Technologie offen |
| 2.2 | Tailscale oder WireGuard | P0 | C-2 | Depl | **HDI A5** — Auswahl im Deployment-Schritt |
| 2.3 | Erlaubte ausgehende Verbindungen | P0 | C-5 | Depl | Grundsatz akzeptiert (D-023), Allowlist offen |
| 2.4 | Mobile Zugriffsmethode | P0 | C-6 | Depl | **HDI A5** — über privates Netz, Methode offen |
| 2.5 | DNS | P1 | C-3 | Cond | offen, nicht aktiviert |
| 2.6 | Reverse Proxy | P1 | C-4 | Cond | offen, nicht aktiviert |

## 3 — Geräte und Nutzung

| # | Frage | Prio | G0 | Klasse | Status |
| --- | --- | --- | --- | --- | --- |
| 3.1 | Primärer Nutzer | P0 | A-1 | **Core** | **`accepted`** |
| 3.2 | Erwartete Nutzerzahl | P0 | A-2 | **Core** | **`accepted`** — 1 im Pilot |
| 3.3 | Zahl der Geräte nach Typ | P0 | A-3 | Depl | offen |
| 3.4 | Desktop-Arbeitsfälle | P0 | A-4 | **Core** | **HDI A6** — `accepted` |
| 3.5 | Mobile Arbeitsfälle, Android oder iOS | P0 | A-5 | **Core** | **HDI A6** — `accepted`; Plattform offen |
| 3.6 | Offlineanforderungen | P0 | A-6 | Cond | offen, nicht aktiviert |
| 3.7 | Native Obsidian-Nutzung | P0 | A-7 | Cond | **HDI A6** — `accepted`, vertagt (D-025) |
| 3.8 | Obsidian-Synchronisationsmodell | P1 | A-7 | Cond | vertagt |

## 4 — Daten

| # | Frage | Prio | G0 | Klasse | Status |
| --- | --- | --- | --- | --- | --- |
| 4.1 | Gewünschte Wissensquellen | P0 | D-1 | **Core** | **`accepted`** — PILOT_SOURCE_CONTRACT (CBP-WP-006) |
| 4.2 | Größenordnung | P0 | D-2 | Depl | offen, bewusst nicht erhoben |
| 4.3 | Dateiformate | P0 | D-3 | **Core** | **`accepted`** |
| 4.4 | Datenklasse je Quelle | P0 | D-4 | **Core** | **HDI A4** — `accepted` auf Profilebene |
| 4.5 | Ausgeschlossene Daten | P0 | D-5 | **Core** | **HDI A4** — `accepted` (D-021) |
| 4.6 | Personenbezogene Daten und Rechtsgrundlage | P0 | D-6 | Cond | **HDI A4** — `not-applicable` für den Pilot (D-022) |
| 4.7 | Vertrauliche Informationen | P0 | D-7 | Cond | **HDI A4** — `not-applicable` für den Pilot (D-020) |
| 4.8 | Verfahren bei Secret in der Git-Historie | P0 | D-8 | **Core** | **`accepted`** — SECRET_INCIDENT_RESPONSE (CBP-WP-004) |
| 4.9 | Schnitt einer Wissenseinheit | P1 | — | — | offen |
| 4.10 | Verpflichtende Frontmatter-Felder | P1 | — | — | offen |
| 4.11 | Bildung der stabilen Source-ID | P1 | — | — | offen |
| 4.12 | Wann gilt Wissen als veraltet | P1 | — | — | offen |

## 5 — Claude und GitHub

| # | Frage | Prio | G0 | Klasse | Status |
| --- | --- | --- | --- | --- | --- |
| 5.1 | Aktuelle Claude-Desktop-Nutzung | P0 | E-1 | Depl | offen |
| 5.2 | Erlaubte Repository-Zugriffe | P0 | E-2 | **Core** | **`accepted`** — PERMISSION_MODEL |
| 5.3 | GitHub-Zugriffe | P0 | E-3 | **Core** | **`accepted`** — PERMISSION_MODEL |
| 5.4 | Berechtigungsstufen je Bereich | P0 | E-4 | **Core** | **`accepted`** — Matrix 9×12 |
| 5.5 | Freigabeverfahren | P0 | E-5 | **Core** | **`accepted`** — sechsstufiger Ablauf |

Dieser Block ist der größte zusammenhängende Core-Required-Rest neben dem
Benchmark. Erfasst als OD-32.

## 6 — Betrieb

| # | Frage | Prio | G0 | Klasse | Status |
| --- | --- | --- | --- | --- | --- |
| 6.1 | VM als Referenzbetrieb bestätigt | P0 | F-1 | **Core** | **HDI A1** — `accepted` (D-015) |
| 6.2 | Docker Compose als Pilotlaufzeit bestätigt | P0 | F-2 | **Core** | **HDI A1** — `accepted` (D-016) |
| 6.3 | Backup- und Restore-Zielwerte | P0 | F-4 | Depl | offen, vertagt |
| 6.4 | Bedingungen für UI- und Wiki-Start | P0 | F-6 | **Core** | **HDI A6** — `accepted` (D-024, D-025) |
| 6.5 | Suchlösung, qmd gesetzt oder Kandidat | P1 | — | Depl | offen (OD-25) |
| 6.6 | Datenbank und Web-UI-Technologie | P1 | — | Depl | offen |
| 6.7 | Backupsoftware | P1 | B-7 | Depl | offen |
| 6.8 | Mehrschreiberschutz | P1 | — | — | durch D-018 entschärft (Single-User) |
| 6.9 | Akzeptable Ausfallzeit | P2 | — | Depl | offen |

## 7 — Scope und spätere Zielgruppe

| # | Frage | Prio | G0 | Klasse | Status |
| --- | --- | --- | --- | --- | --- |
| 7.1 | Repository dauerhaft privat | P0 | — | — | **offen** — OD-11; **nicht Teil von A-8** |
| 7.2 | Explizite Nicht-Ziele | P0 | A-8 | **Core** | **`accepted`** — 11 Nicht-Ziele in DO_NOT_START |
| 7.3 | Lizenz | P1 | — | — | offen (OD-23) |
| 7.4 | Spätere öffentliche Zielgruppe | P2 | — | — | offen |
| 7.5 | Öffentlicher Produktname | P2 | — | — | offen (OD-28) |
| 7.6 | Phase-7-Option | P2 | — | — | offen |

---

## Zusammenfassung

> **Korrektur.** Die in CBP-WP-002 berichteten Summen waren fehlerhaft. Die
> Fragen selbst waren vollständig; nur die Summenzeile stimmte nicht.

| Prio | Falsch berichtet | **Korrekt** |
| --- | --- | --- |
| **P0** | 35 | **38** |
| P1 | 16 | **14** |
| P2 | 4 | **4** |
| **Summe** | 55 | **56** |

### Stand nach G0

| Kategorie | Anzahl |
| --- | --- |
| P0-Fragen gesamt | 38 |
| davon einem `accepted` Core-Kriterium zugeordnet | **19** |
| davon `not-applicable` (Conditional) | 2 |
| davon **vertagt** (Deployment Required, DRC) | 16 |
| davon weiterhin offen ohne Core-Bezug | **1** (7.1 Repository-Sichtbarkeit, OD-11) |

**Alle 25 Core-Required-Kriterien sind `accepted`.** Die 16 vertagten Fragen
bleiben **sichtbar offen** und werden im
[DRC](../operations/DEPLOYMENT_READINESS_CHECK.md) geprüft — Status
`NOT EVALUATED`.

Die P1- und P2-Fragen bleiben offen und sind nicht G0-relevant.
## Bearbeitung

Beantwortete Fragen werden **nicht gelöscht**. Die Antwort wird ergänzt, der
Status des zugehörigen G0-Kriteriums nachgeführt, und bei bindender Wirkung
entsteht ein ADR.
