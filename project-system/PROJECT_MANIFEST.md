# Project Manifest – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Autoritaetsklasse | A2 |
| Stand | 2026-07-20 |

> **Formatabweichung.** NDF v1.0.0 sieht kanonisch
> `project-system/project-manifest.yaml` vor. CBP-WP-001 fordert eine
> Markdown-Datei und erlaubt ausschliesslich Markdown, `.gitignore` und
> Ordner. Begruendung und Umstellungsempfehlung: **AB-03** in
> [../docs/ndf/ADOPTION_NOTES.md](../docs/ndf/ADOPTION_NOTES.md).

## Identitaet

| Feld | Wert |
| --- | --- |
| Name | Core Brain Pilot |
| Kurzform | CBP |
| WP-Praefix | `CBP-WP-` |
| Art | KI-Wissens- und Arbeitssystem |
| Sichtbarkeit | privat |
| Sprache Dokumentation | Deutsch |
| Lizenz | **nicht festgelegt** (Q-28) |

## Framework

| Feld | Wert |
| --- | --- |
| Framework | Nova Development Framework |
| Version | **v1.0.0** |
| Quelle | https://github.com/KayKaspers/Nova-Development-Framework/releases/tag/v1.0.0 |
| Bindung | verbindlich |
| v1.1-Planung | **nicht** uebernommen |
| Abweichungen | AB-01 bis AB-10 |

## Status

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Aktuelles Work Package | CBP-WP-001 |
| Naechstes Gate | G0 – Discovery and Scope Lock |
| Capabilities gesamt | 29 |
| Capabilities implementiert | **0** |
| Angenommene ADRs | 0 |
| Scope gelockt | nein |

## Repository

| Feld | Wert |
| --- | --- |
| Pfad | `D:\Projects\Core-Brain-Pilot` |
| Branch | `main` |
| Commits | 0 |
| Remote | **keines** |
| Commit-Autoritaet | ausschliesslich Human Maintainer |

## Rollen

| Rolle | Traeger | Verantwortung |
| --- | --- | --- |
| Planung | Nova (ChatGPT) | Architektur und Work Packages |
| Ausfuehrung | Implementation Agent | Genau ein freigegebenes Work Package |
| Freigabe | Human Maintainer | Review, GO/REWORK/SPLIT/STOP, Commit, Push |

## Verzeichnisse

| Pfad | Inhalt | Klasse |
| --- | --- | --- |
| `docs/architecture/` | Definition, Prinzipien, Vertrauensgrenzen | kanonisch |
| `docs/decisions/` | ADRs | kanonisch |
| `docs/discovery/` | Offene Fragen, fehlende Information | kanonisch |
| `docs/ndf/` | NDF-Anwendung und Abweichungen | kanonisch |
| `docs/privacy/` | Datenklassen | kanonisch |
| `docs/product/` | Sperrliste | kanonisch |
| `project-brain/` | Projektgedaechtnis | kanonisch |
| `project-system/` | Profil, Manifest, Matrix, Register, Queue | kanonisch |
| `work-packages/` | Wortlaut freigegebener Work Packages | kanonisch |

Abgeleitete Daten haben in diesem Repository **kein** Verzeichnis. Sie werden
ueber [`.gitignore`](../.gitignore) ausgeschlossen.

## Autoritaetsmodell

`A0` Human-Maintainer-Beschluss · `A1` Release, Tag, angenommener ADR ·
`A2` Projektstatus, WP-Queue · `A3` Roadmap, Gate-Doku · `A4` README,
erlaeuternde Doku · `A5` Projektchat-Uebergabe · `A6` abgeleitete
Zusammenfassung, Wiki

**A6 ueberschreibt A0–A5 niemals automatisch.**

## Datenklassen

`public` · `internal` · `confidential` · `secret` · `excluded-from-ai`

Secrets gelangen nicht in Repository, Wissensbestand, Index, Context Pack oder
Modellkontext. Siehe
[../docs/privacy/DATA_CLASSIFICATION.md](../docs/privacy/DATA_CLASSIFICATION.md).

## Sperrliste Phase 0

Produktive Implementierung · Docker Compose · Web-UI · Suchintegration ·
Wiki-Ingest · Knowledge Graph · Obsidian-Synchronisation · MCP-Integration ·
externe Connectoren · automatisierte Commits · oeffentliches Branding

Verbindlich in
[../docs/product/DO_NOT_START.md](../docs/product/DO_NOT_START.md).
