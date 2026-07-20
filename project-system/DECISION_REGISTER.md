# Decision Register – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Autoritaetsklasse | A2 |
| Stand | 2026-07-20 |

Register **offener** und **getroffener** Entscheidungen.

> **Ablageabweichung.** NDF v1.0.0 sieht `project-brain/DECISIONS.md` vor.
> CBP-WP-001 fordert diese Datei. Es existiert bewusst nur **eine** von beiden
> — siehe AB-04 in
> [../docs/ndf/ADOPTION_NOTES.md](../docs/ndf/ADOPTION_NOTES.md).

Ein Eintrag mit bindender Wirkung wird zusaetzlich als ADR in
[../docs/decisions/](../docs/decisions/README.md) ausgefertigt und erhaelt
damit **A1**.

## Getroffene Entscheidungen

| ID | Entscheidung | Klasse | Datum | ADR |
| --- | --- | --- | --- | --- |
| D-001 | Das Projekt arbeitet verbindlich nach NDF v1.0.0; keine v1.1-Planung | A0 | 2026-07-20 | offen |
| D-002 | Phase 0 ist Discovery und Scope Lock; keine produktive Implementierung | A0 | 2026-07-20 | offen |
| D-003 | Commit-, Push- und Release-Autoritaet liegt ausschliesslich beim Human Maintainer | A0 | 2026-07-20 | offen |
| D-004 | Markdown ist das kanonische Wissensformat | A2 | 2026-07-20 | offen |
| D-005 | Abgeleitete Daten werden nicht versioniert und sind nie autoritativ | A2 | 2026-07-20 | offen |
| D-006 | Fuenf Datenklassen; Secrets nie in Repository, Index, Context Pack oder Modellkontext | A2 | 2026-07-20 | offen |
| D-007 | Keine `LICENSE`-Datei in Phase 0 | A0 | 2026-07-20 | — |
| D-008 | Register in `project-system/` statt `project-brain/`; keine Doppelstruktur | A2 | 2026-07-20 | offen |

**Hinweis zu D-001 bis D-006 und D-008:** Diese Festlegungen stammen aus dem
Wortlaut von CBP-WP-001 und den Projektanweisungen. Ob sie bereits bindend
sind oder Vorschlaege zur Pruefung an G0 darstellen, ist nicht ausgewiesen —
siehe OI-02. Die Ausfertigung als ADR ist offen.

## Offene Entscheidungen

Legende: **P1** blockiert G0 · **P2** vor Implementierung · **P3** spaeter.

| ID | Offene Entscheidung | Prio | Adressat | Bezug |
| --- | --- | --- | --- | --- |
| OD-01 | Kriterien, die Gate G0 abschliessen | P1 | Nova | OI-04, Q-31 |
| OD-02 | Definition der Context Budgets B0–B4: Masseinheit und Schwellen | P1 | Nova | OI-03, Q-18 |
| OD-03 | Rang der 16 Kernprinzipien und 29 Capabilities: A0/A1 oder Vorschlag | P1 | Human Maintainer | OI-02 |
| OD-04 | Minimal nuetzlicher Funktionsumfang des Piloten | P1 | Nova | Q-01 |
| OD-05 | Ablageort des kanonischen Wissensbestands: dieses oder eigenes Repository | P1 | Human Maintainer | Q-05 |
| OD-06 | Quellen im ersten Scope und ausdrueckliche Nicht-Quellen | P1 | Nova | Q-04 |
| OD-07 | Vergabeverfahren fuer Autoritaetsklassen A0–A6 | P1 | Nova | Q-10 |
| OD-08 | Vergabeverfahren fuer Datenklassen | P1 | Human Maintainer | Q-14 |
| OD-09 | Rechtsgrundlage fuer personenbezogene Daten im Bestand | P1 | Human Maintainer | Q-15 |
| OD-10 | Verfahren bei Secret in der Git-Historie | P1 | Human Maintainer | Q-16 |
| OD-11 | Repository dauerhaft privat? | P1 | Human Maintainer | Q-29 |
| OD-12 | Prompt Mode "Lean": auf `Standard` umstellen oder als Synonym festschreiben | P2 | Nova | AB-01 |
| OD-13 | Manifest auf `project-manifest.yaml` umstellen | P2 | Nova | AB-03 |
| OD-14 | NDF-Namensschema fuer Register uebernehmen oder abweichen | P2 | Nova | AB-04, Q-30 |
| OD-15 | Schnitt einer Wissenseinheit: Datei, Abschnitt oder Block | P2 | Nova | Q-07 |
| OD-16 | Bildungsvorschrift der stabilen Source-ID | P2 | Nova | Q-08 |
| OD-17 | Verpflichtende Frontmatter-Felder | P2 | Nova | Q-09 |
| OD-18 | Filterreihenfolge im Retrieval-Pfad | P2 | Nova | Q-20 |
| OD-19 | Umfang und Format des Retrieval-Trace | P2 | Nova | Q-21 |
| OD-20 | Programmiersprache, Suchmaschine, Embedding-Modell | P2 | Human Maintainer | — |
| OD-21 | Zugriffsweg fuer Mehrgeraete-Nutzung | P2 | Human Maintainer | Q-23 |
| OD-22 | Sicherungsfrequenz und Sicherungsziel | P2 | Human Maintainer | Q-25 |
| OD-23 | Lizenzwahl | P2 | Human Maintainer | Q-28, D-007 |
| OD-24 | Akzeptable Ausfallzeit | P3 | Human Maintainer | Q-24 |

## Pflege

Eine getroffene Entscheidung wird **nicht geloescht**. Aenderungen erfolgen
durch einen neuen Eintrag, der den alten als ersetzt kennzeichnet — analog zur
ADR-Supersession.
