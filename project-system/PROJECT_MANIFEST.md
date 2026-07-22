# Project Manifest – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Überarbeitet in | **CBP-WP-014** |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

> **Formatabweichung.** NDF v1.0.0 sieht `project-system/project-manifest.yaml`
> vor. Diese Markdown-Fassung ist **vorläufig für den Bootstrap** akzeptiert —
> AB-03, OD-13.

## Identität

| Feld | Wert |
| --- | --- |
| Interner Arbeitstitel | Core Brain Pilot |
| Kurzform | CBP |
| WP-Präfix | `CBP-WP-` |
| Art | KI-Wissens- und Arbeitssystem, serverzentriert und portabel |
| Sichtbarkeit | **privat** · **dauerhafte Sichtbarkeit offen** (OD-11). Core-Repository ist `publication-capable by design` — **keine Veröffentlichungsfreigabe**; diese benötigt A0 |
| Sprache Dokumentation | Deutsch, UTF-8 mit echten Umlauten |
| Lizenz | **nicht festgelegt** (OD-23) |
| Öffentlicher Produktname | **nicht beschlossen** (OD-28) |

## Framework

| Feld | Wert |
| --- | --- |
| Framework | Nova Development Framework **v1.0.0**, verbindlich |
| v1.1-Planung | **nicht** übernommen |
| Zweites Governance-System | **ausgeschlossen** |
| Abweichungen | AB-01 bis AB-10; AB-03 bis AB-08 nur vorläufig |

## Status

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 – COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Aktuelles Work Package | **CBP-WP-014** (`in-review`) |
| **Gate-Status G0** | **PASSED WITH NOTES** — 2026-07-21, A0 |
| Nächstes Prüfmodell | **Deployment Readiness Check** — `NOT EVALUATED` |
| Phase-1-Planung | Streams F1–F5; CBP-WP-015 **`proposed`** |
| **Runtime Skeleton** | **lokal implementiert** (CBP-WP-012) — `run` fail-closed; keine KB-Kontrolle durchgesetzt |
| **Ingest-Quarantäne MVP** | **lokaler Prototyp** (CBP-WP-013, ADR-0010) — synthetic-only, fail-closed, keine Promotion, **nicht produktiv** |
| **Source-Registry MVP** | **lokaler Prototyp** (CBP-WP-014, ADR-0011) — synthetic-only, fail-closed, **deaktiviert**, `activate` verweigert, **212 Tests**, **nicht produktiv** |
| **Mappingkonvention** | **entschieden** — ADR-0008 (D-031, D-032, D-033) |
| **Mapping Activation Gate** | **`NOT EVALUATED`** — 0 Mappings, 0 angebundene Quellen |
| **Repository-Zielstruktur** | **entschieden** — Monorepo, ADR-0007 (D-029); **Migration nicht autorisiert** |
| **Bereichsmodell** | **W-3** — Operator-Workspace außerhalb (D-030); **nicht angelegt** |
| **Veröffentlichung** | **nicht freigegeben** — Repository bleibt privat; benötigt separate A0-Entscheidung |
| Technische Nachweise | **0** — alle Artefakte auf Stufe 1 `dokumentiert` |
| G0-Kriterien | **47** |
| davon blockierend (Core Required) | **25** |
| davon `accepted` | **25** — alle |
| Kriterienstand | 25 von 25 `accepted` |
| Capabilities implementiert | **0** von 29 — Capability 2/3/5/6/7 bleiben nicht vollständig `implemented` |
| Angenommene ADRs | **11** |
| Scope gelockt | **ja** — mit Auflagen |

## Repository

| Feld | Wert |
| --- | --- |
| Pfad | `D:\Projects\Core-Brain-Pilot` |
| Branch | `main` |
| Commits | **12** |
| Remote | `origin` → `https://github.com/KayKaspers/Core-Brain-Pilot.git` |
| Commit-Autorität | ausschließlich Human Maintainer |

## Pilotumfang

Festgelegt im Human Discovery Intake, CBP-WP-003. Profilebene, keine
Installationswerte.

| Dimension | Festlegung |
| --- | --- |
| Betriebsprofil | Proxmox-VM mit dedizierter Linux-VM (D-015) |
| Anwendungslaufzeit | Docker Compose bevorzugt innerhalb der VM (D-016) |
| Portabilität | Linux-VM, Docker/OCI, Einzelplatz bleiben dokumentierbar (D-017) |
| Nutzung | Einzelperson; Multi-User kein Pflichtumfang (D-018) |
| Quellen im Pilot | Markdown, Git, Chat-Handoffs, Obsidian-Vault als Markdown |
| Datenklassen im Pilot | `public`, `internal` |
| Zugriff | privates VPN oder privates Netz, keine öffentliche Freigabe (D-023) |
| Im Pilot | Web-UI (nach Retrieval), mobile Nutzung (D-024) |
| Vertagt | native Obsidian-Nutzung, Wiki-Pilot, externe Connectoren, Graph (D-025) |

## Kriterienmodell

| Klasse | Anzahl | Blockiert G0 | Zuständiges Gate |
| --- | --- | --- | --- |
| **Core Required** | 25 | **ja** | G0 |
| Deployment Required | 16 | nein | [Deployment Readiness Check](../docs/operations/DEPLOYMENT_READINESS_CHECK.md) — **NOT EVALUATED** |
| Conditional | 6 | nur bei aktivierter Funktion | je nach Funktion |

## Sichere Standardwerte

Architekturdefaults, **keine Behauptungen über die reale Infrastruktur**:

1. Single-User-Betrieb als Einstieg
2. Privater Zugriff
3. Keine öffentliche Dienstfreigabe
4. Keine Secrets in Wissensbestand, Index oder Context Packs
5. **Übertragung an externe KI standardmäßig verweigert**, bis eine Datenklasse sie erlaubt
6. Trennung von canonical und derived; Runtime-Daten getrennt in **RT-1**
   (reproduzierbar), **RT-2 Operational Evidence** (**nicht** reproduzierbar,
   aufbewahrungs- und sicherungspflichtig) und **RT-3** (flüchtig)
7. Keine automatische Konfliktauflösung
8. Keine automatischen Commits oder Pushes
9. Keine Obsidian-Synchronisation als Standard
10. Backup muss vor produktivem Betrieb eingerichtet **und getestet** sein
11. Optionale Funktionen bleiben deaktiviert, bis sie bewusst gewählt werden

## Rollen

| Rolle | Träger | Verantwortung |
| --- | --- | --- |
| Planung | Nova (ChatGPT) | Architektur und Work Packages |
| Ausführung | Implementation Agent (Claude Desktop) | Genau ein freigegebenes Work Package |
| Freigabe | Human Maintainer | Review, GO / GO WITH NOTES / REWORK / SPLIT / STOP, Commit, Push, Veröffentlichung |

## Quellen

| Quelle | Klasse | Ort |
| --- | --- | --- |
| `Bauanleitung_Second-Brain.pdf` | **A4** | außerhalb des Repositorys, sechs Inhaltsseiten |
| `Second-Brain-Bauanleitung-Textfassung.md` | **A6** | außerhalb des Repositorys |
| `docs/discovery/Core-Brain-Project-Handoff.md` | **A5** | im Repository, getrackt |
| `docs/discovery/HUMAN_DISCOVERY_INPUT.md` | **A2** mit einzelnen A0-Entscheidungen | im Repository |
| Nova Development Framework v1.0.0 | **A1** | extern |

## Autoritätsmodell

`A0` Human-Maintainer-Beschluss · `A1` Release, Tag, ADR · `A2` Projektstatus,
WP-Queue · `A3` Roadmap, Gate-Doku · `A4` README, erläuternde Doku ·
`A5` Projektchat-Übergabe · `A6` abgeleitete Zusammenfassung

**A6 überschreibt A0–A5 niemals automatisch.**

## Datenklassen

`public` · `internal` · `confidential` · `secret` · `excluded-from-ai`

Secrets gelangen nicht in Repository, Wissensbestand, Index, Context Pack oder
Modellkontext. Das **Verfahren im Schadensfall ist definiert**
([SECRET_INCIDENT_RESPONSE.md](../docs/security/SECRET_INCIDENT_RESPONSE.md),
OD-10 geschlossen) — **automatische Erkennung fehlt weiterhin** (R-01).

## Context Budgets

`B0` Micro · `B1` Lean · `B2` Standard · `B3` Extended · `B4` Exceptional

**Nicht zu verwechseln mit den NDF Prompt Modes** Full, Standard, Short.
„Lean" ist ausschließlich der Name von B1 (D-009).

## Sperrliste Phase 0

25 gesperrte Gegenstände in
[../docs/product/DO_NOT_START.md](../docs/product/DO_NOT_START.md).
