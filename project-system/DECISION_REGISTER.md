# Decision Register – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Überarbeitet in | CBP-WP-002 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

Register **getroffener** und **offener** Entscheidungen.

> **Ablageabweichung.** NDF v1.0.0 sieht `project-brain/DECISIONS.md` vor.
> Es existiert bewusst nur **eine** von beiden — siehe AB-04 in
> [../docs/ndf/ADOPTION_NOTES.md](../docs/ndf/ADOPTION_NOTES.md).

Ein Eintrag mit bindender Wirkung wird zusätzlich als ADR in
[../docs/decisions/](../docs/decisions/README.md) ausgefertigt und erhält
damit **A1**.

## Getroffene Entscheidungen

| ID | Entscheidung | Klasse | Datum | ADR |
| --- | --- | --- | --- | --- |
| D-001 | Das Projekt arbeitet verbindlich nach NDF v1.0.0; keine v1.1-Planung | A0 | 2026-07-20 | offen |
| D-002 | Phase 0 ist Discovery und Scope Lock; keine produktive Implementierung | A0 | 2026-07-20 | offen |
| D-003 | Commit-, Push- und Release-Autorität liegt ausschließlich beim Human Maintainer | A0 | 2026-07-20 | offen |
| D-004 | Markdown ist das kanonische Wissensformat | A2 | 2026-07-20 | offen |
| D-005 | Abgeleitete Daten werden nicht versioniert und sind nie autoritativ | A2 | 2026-07-20 | offen |
| D-006 | Fünf Datenklassen; Secrets nie in Repository, Index, Context Pack oder Modellkontext | A2 | 2026-07-20 | offen |
| D-007 | Keine `LICENSE`-Datei in Phase 0 | A0 | 2026-07-20 | — |
| D-008 | Register in `project-system/` statt `project-brain/`; keine Doppelstruktur | A2 | 2026-07-20 | offen |
| **D-009** | **Offizielle NDF Prompt Modes sind Full, Standard und Short. „Lean" ist kein Prompt Mode, sondern ausschließlich der Name des Context Budgets B1. B0–B4 bleiben ein separates Core-Brain-Modell.** | **A0** | 2026-07-20 | offen |
| **D-010** | **Die A5-Projektübergabe wird dauerhaft als kanonische Quelle im Repository geführt** | **A0** | 2026-07-20 | — |
| **D-011** | **Quellenklassifikation: PDF-Bauanleitung A4, Textfassung A6, Projektübergabe A5. Die Textfassung beansprucht keine höhere Autorität als die PDF** | **A0** | 2026-07-20 | — |
| **D-012** | **Neue und geänderte Dokumente verwenden UTF-8 mit echten deutschen Umlauten; die Transkription aus CBP-WP-001 wird aufgehoben** | **A0** | 2026-07-20 | — |
| **D-013** | **Dedizierte Linux-VM ist der Referenzbetrieb. Docker Compose ist eine vorgesehene, noch nicht implementierte Anwendungslaufzeit innerhalb dieser VM** | **A0** | 2026-07-20 | offen |
| **D-014** | **Wiki, Graph und eigene Web-UI beginnen nicht vor einem bestandenen Retrieval-Pilot-Gate** | **A0** | 2026-07-20 | offen |

**Hinweis zu D-004 bis D-006, D-008:** Diese Festlegungen tragen A2. Der
Quellenabgleich in CBP-WP-002 hat sie inhaltlich gegen die A5-Projektübergabe
bestätigt, ihre formale Bindung durch ADR steht aus — siehe OD-03.

**Neu in CBP-WP-002:** D-009 bis D-014 stammen aus den ausdrücklichen
Nova-Entscheidungen zu CBP-WP-002 und tragen deshalb A0.

## Geschlossene offene Entscheidungen

| ID | War offen | Geschlossen durch | Datum |
| --- | --- | --- | --- |
| **OD-12** | Prompt Mode „Lean" | **D-009** — „Lean" ist kein NDF Prompt Mode, sondern der Name von B1 | 2026-07-20 |
| **OD-02** | Definition der Context Budgets B0–B4 | [../docs/architecture/CONTEXT_BUDGETS.md](../docs/architecture/CONTEXT_BUDGETS.md); **Restpunkt:** Kalibrierung der Token-Richtwerte gegen den Benchmark, siehe OD-02b | 2026-07-20 |
| **OD-01** | Kriterien für Gate G0 | [../docs/discovery/G0_SCOPE_LOCK_CRITERIA.md](../docs/discovery/G0_SCOPE_LOCK_CRITERIA.md) — 41 Kriterien, 39 blockierend, fünfteilige Abschlussregel | 2026-07-20 |

## Offene Entscheidungen

Legende: **P0** blockiert G0 · **P1** vor Architekturentscheidung · **P2** später.

| ID | Offene Entscheidung | Prio | Adressat | Bezug |
| --- | --- | --- | --- | --- |
| OD-02b | Kalibrierung der Token-Richtwerte für B0–B4 gegen den Benchmark | P1 | Nova | CONTEXT_BUDGETS, OI-03 |
| OD-03 | Rang der Kernprinzipien und Capabilities: Ausfertigung als ADR (A1) oder Verbleib bei A2 | **P0** | Human Maintainer | OI-02, Ü-04 |
| OD-04 | Minimal nützlicher Funktionsumfang des Piloten | **P0** | Nova | Fragebogen 7.2 |
| OD-05 | Ablageort des kanonischen Wissensbestands: dieses oder ein eigenes Repository | **P0** | Human Maintainer | D-1, OD-26 |
| OD-06 | Quellen im ersten Scope und ausdrückliche Nicht-Quellen | **P0** | Nova | D-1, D-5 |
| OD-07 | Vergabeverfahren für Autoritätsklassen A0–A6 | **P0** | Nova | Übergabe §6 |
| OD-08 | Vergabeverfahren für Datenklassen | **P0** | Human Maintainer | D-4 |
| OD-09 | Rechtsgrundlage für personenbezogene Daten | **P0** | Human Maintainer | D-6 |
| OD-10 | Verfahren bei Secret in der Git-Historie | **P0** | Human Maintainer | D-8 |
| OD-11 | Repository dauerhaft privat? | **P0** | Human Maintainer | A-8 |
| OD-13 | Manifest auf `project-manifest.yaml` umstellen | P1 | Nova | AB-03 |
| OD-14 | NDF-Namensschema für Register übernehmen oder abweichen | P1 | Nova | AB-04 |
| OD-15 | Schnitt einer Wissenseinheit: Datei, Abschnitt oder Block | P1 | Nova | Fragebogen 4.9 |
| OD-16 | Bildungsvorschrift der stabilen Source-ID | P1 | Nova | Fragebogen 4.11 |
| OD-17 | Verpflichtende Frontmatter-Felder | P1 | Nova | Fragebogen 4.10, Übergabe §6 |
| OD-18 | Filterreihenfolge im Retrieval-Pfad | P1 | Nova | TRUST_BOUNDARIES TB-4 |
| OD-19 | Umfang und Format des Retrieval-Trace | P1 | Nova | Capability 15 |
| OD-20 | Programmiersprache, Suchmaschine, Embedding-Modell | P1 | Human Maintainer | Fragebogen 6.5, 6.6 |
| OD-21 | Zugriffsweg für Mehrgeräte-Nutzung | **P0** | Human Maintainer | C-6 |
| OD-22 | Sicherungsfrequenz und Sicherungsziel | **P0** | Human Maintainer | B-7, B-8 |
| OD-23 | Lizenzwahl | P1 | Human Maintainer | D-007, Fragebogen 7.3 |
| OD-24 | Akzeptable Ausfallzeit | P2 | Human Maintainer | Fragebogen 6.9 |
| **OD-25** | **qmd als produktiver Suchdienst — nur nach Installations-, Plattform-, Lizenz-, Wartungs- und Sicherheitsprüfung** | P1 | Human Maintainer | Übergabe §9, Bauanleitung Seite 2 |
| **OD-26** | **Endgültige Repository-Struktur — drei Vorstellungen stehen nebeneinander** | **P0** | Nova + Human Maintainer | W-05, OI-07 |
| **OD-27** | **Obsidian-Synchronisationsmodell — serverzentriert oder nativ auf mehreren Geräten** | **P0** | Human Maintainer | A-7, Fragebogen 3.7, 3.8 |
| **OD-28** | **Öffentlicher Produktname und Phase-7-Option** | P2 | Human Maintainer | Übergabe §1, §15 |
| **OD-29** | **Dauerhafte Behandlung der NDF-Abweichungen AB-03 bis AB-08** | **P0** | Nova + Human Maintainer | ADOPTION_NOTES |
| **OD-30** | **Backup- und Restore-Zielwerte: maximaler Datenverlust und maximale Wiederherstellungsdauer** | **P0** | Human Maintainer | F-4 |

## Zusammenfassung

| Kategorie | Anzahl |
| --- | --- |
| Getroffene Entscheidungen | 14 (davon 8 mit A0) |
| Geschlossene offene Entscheidungen | 3 |
| Offene Entscheidungen | 27 |
| davon **P0** (blockiert G0) | **14** |

**Keine offene Entscheidung wird als A0 geführt.** Die Spalte „Adressat"
benennt, wer entscheidet — nicht, dass bereits entschieden wäre.

## Pflege

Eine getroffene Entscheidung wird **nicht gelöscht**. Änderungen erfolgen durch
einen neuen Eintrag, der den alten als ersetzt kennzeichnet — analog zur
ADR-Supersession.
