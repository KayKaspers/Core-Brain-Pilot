# Project Manifest – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Überarbeitet in | CBP-WP-002 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

> **Formatabweichung.** NDF v1.0.0 sieht kanonisch
> `project-system/project-manifest.yaml` vor. Diese Markdown-Fassung ist
> **vorläufig für den Bootstrap** akzeptiert und vor G0 zu entscheiden —
> **AB-03**, OD-13.

## Identität

| Feld | Wert |
| --- | --- |
| Interner Arbeitstitel | Core Brain Pilot |
| Kurzform | CBP |
| WP-Präfix | `CBP-WP-` |
| Art | KI-Wissens- und Arbeitssystem, serverzentriert und portabel |
| Sichtbarkeit | privat |
| Sprache Dokumentation | Deutsch, UTF-8 mit echten Umlauten |
| Lizenz | **nicht festgelegt** (OD-23) |
| Öffentlicher Produktname | **nicht beschlossen** (OD-28) |

## Framework

| Feld | Wert |
| --- | --- |
| Framework | Nova Development Framework |
| Version | **v1.0.0** |
| Quelle | https://github.com/KayKaspers/Nova-Development-Framework/releases/tag/v1.0.0 |
| Bindung | verbindlich |
| v1.1-Planung | **nicht** übernommen |
| Zweites Governance-System | **ausgeschlossen** — Superpowers nur als Referenz |
| Abweichungen | AB-01 bis AB-10; AB-03 bis AB-08 nur vorläufig |

## Status

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Aktuelles Work Package | CBP-WP-002 (`in-review`) |
| Nächstes Gate | **G0 – Discovery and Scope Lock** |
| **Gate-Status** | **NOT PASSED** |
| G0-Kriterien | 41, davon 39 blockierend, 0 beantwortet |
| Capabilities gesamt | 29 |
| Capabilities implementiert | **0** |
| Angenommene ADRs | 0 |
| Scope gelockt | **nein** |

## Repository

| Feld | Wert |
| --- | --- |
| Pfad | `D:\Projects\Core-Brain-Pilot` |
| Branch | `main` |
| Commits | 2 |
| Remote | `origin` → `https://github.com/KayKaspers/Core-Brain-Pilot.git` |
| Commit-Autorität | ausschließlich Human Maintainer |

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
| `Second-Brain-Bauanleitung-Textfassung.md` | **A6** | außerhalb des Repositorys, abgeleitete Arbeitsrepräsentation |
| `docs/discovery/Core-Brain-Project-Handoff.md` | **A5** | im Repository, kanonisch, getrackt |
| Nova Development Framework v1.0.0 | **A1** | extern, öffentlich |

Die A6-Textfassung beansprucht keine höhere Autorität als die A4-PDF.

## Verzeichnisse

| Pfad | Inhalt | Klasse |
| --- | --- | --- |
| `docs/architecture/` | Definition, Prinzipien, Vertrauensgrenzen, Context Budgets | kanonisch |
| `docs/decisions/` | ADRs | kanonisch |
| `docs/discovery/` | Fragebogen, G0-Kriterien, Quellenabgleich, A5-Übergabe | kanonisch |
| `docs/ndf/` | NDF-Anwendung und Abweichungen | kanonisch |
| `docs/privacy/` | Datenklassen | kanonisch |
| `docs/product/` | Sperrliste | kanonisch |
| `project-brain/` | Projektgedächtnis | kanonisch |
| `project-system/` | Profil, Manifest, Matrix, Register, Queue, Prüfungen | kanonisch |
| `work-packages/` | Wortlaut freigegebener Work Packages | kanonisch |

Abgeleitete Daten haben in diesem Repository **kein** Verzeichnis. Sie werden
über [`.gitignore`](../.gitignore) ausgeschlossen.

> **Die Struktur ist nicht freigegeben.** Projektübergabe §13 nennt eine mögliche
> spätere Struktur `core/`, `deployments/`, `docs/`, `examples/` und stellt
> ausdrücklich fest, dass die konkrete Struktur noch geplant werden muss —
> OD-26, Widerspruch W-05.

## Autoritätsmodell

`A0` Human-Maintainer-Beschluss · `A1` Release, Tag, angenommener ADR ·
`A2` Projektstatus, WP-Queue · `A3` Roadmap, Gate-Doku · `A4` README,
erläuternde Doku · `A5` Projektchat-Übergabe · `A6` abgeleitete
Zusammenfassung, Wiki

**A6 überschreibt A0–A5 niemals automatisch.**

## Datenklassen

`public` · `internal` · `confidential` · `secret` · `excluded-from-ai`

Secrets gelangen nicht in Repository, Wissensbestand, Index, Context Pack oder
Modellkontext.

## Context Budgets

`B0` Micro · `B1` Lean · `B2` Standard · `B3` Extended · `B4` Exceptional

**Nicht zu verwechseln mit den NDF Prompt Modes** Full, Standard und Short.
„Lean" ist ausschließlich der Name von B1 (D-009).

## Sperrliste Phase 0

25 gesperrte Gegenstände, verbindlich in
[../docs/product/DO_NOT_START.md](../docs/product/DO_NOT_START.md).
