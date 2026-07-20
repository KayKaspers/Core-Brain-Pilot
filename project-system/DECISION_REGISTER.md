# Decision Register – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Überarbeitet in | CBP-WP-004 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

> **Ablageabweichung.** NDF v1.0.0 sieht `project-brain/DECISIONS.md` vor.
> Es existiert bewusst nur **eine** von beiden — AB-04.

## Getroffene Entscheidungen

### Aus CBP-WP-001 und CBP-WP-002

| ID | Entscheidung | Klasse | Datum | ADR |
| --- | --- | --- | --- | --- |
| D-001 | Verbindlich nach NDF v1.0.0; keine v1.1-Planung | A0 | 2026-07-20 | offen |
| D-002 | Phase 0 ist Discovery und Scope Lock; keine produktive Implementierung | A0 | 2026-07-20 | offen |
| D-003 | Commit-, Push- und Release-Autorität ausschließlich beim Human Maintainer | A0 | 2026-07-20 | offen |
| D-004 | Markdown ist das kanonische Wissensformat | A2 | 2026-07-20 | offen |
| D-005 | Abgeleitete Daten werden nicht versioniert und sind nie autoritativ | A2 | 2026-07-20 | offen |
| D-006 | Fünf Datenklassen; Secrets nie in Repository, Index, Context Pack oder Modellkontext | A2 | 2026-07-20 | offen |
| D-007 | Keine `LICENSE`-Datei in Phase 0 | A0 | 2026-07-20 | — |
| D-008 | Register in `project-system/`; keine Doppelstruktur | A2 | 2026-07-20 | offen |
| D-009 | NDF Prompt Modes sind Full, Standard, Short. „Lean" ist ausschließlich der Name von B1 | A0 | 2026-07-20 | offen |
| D-010 | A5-Projektübergabe dauerhaft als kanonische Quelle im Repository | A0 | 2026-07-20 | — |
| D-011 | Quellenklassifikation: PDF A4, Textfassung A6, Übergabe A5 | A0 | 2026-07-20 | — |
| D-012 | UTF-8 mit echten deutschen Umlauten | A0 | 2026-07-20 | — |
| D-013 | Dedizierte Linux-VM ist Referenzbetrieb; Docker Compose vorgesehene Laufzeit darin | A0 | 2026-07-20 | offen |
| D-014 | Wiki, Graph und Web-UI nicht vor bestandenem Retrieval-Pilot-Gate | A0 | 2026-07-20 | offen |

### Neu aus CBP-WP-003 — Human Discovery Intake

Alle folgenden Entscheidungen wurden vom Human Maintainer **ausdrücklich**
getroffen. Quelle jeweils
[../docs/discovery/HUMAN_DISCOVERY_INPUT.md](../docs/discovery/HUMAN_DISCOVERY_INPUT.md).

| ID | Entscheidung | Status | Autorität | Quelle | Datum | Betroffene Kriterien | Konsequenz |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **D-015** | Erstes Pilotprofil ist eine Proxmox-VM mit dedizierter Linux-VM als Referenzbetrieb | `accepted` | **A0** | HDI A1 | 2026-07-20 | F-1 | Referenzprofil A ist gewählt; Profile B–E bleiben dokumentierbar |
| **D-016** | Docker Compose ist die **bevorzugte** Anwendungslaufzeit innerhalb dieser VM | `accepted` | **A0** | HDI A1 | 2026-07-20 | F-2 | Präzisiert D-013 und **hebt die Abschwächung Ü-02 aus CBP-WP-002 auf** — siehe Hinweis unten |
| **D-017** | Deployment-Neutralität wird beibehalten: allgemeine Linux-VM, Docker/OCI und Einzelplatz bleiben dokumentierbare Profile | `accepted` | **A0** | HDI A1 | 2026-07-20 | F-5 | Kein Proxmox-Lock-in; Capability 29 bestätigt |
| **D-018** | Multi-User und Multi-Tenant sind kein Pflichtumfang des ersten Piloten; spätere Teamnutzung darf nicht verhindert werden | `accepted` | **A0** | HDI A2 | 2026-07-20 | A-1, A-2 | Single-User als Einstieg; Architektur bleibt erweiterbar |
| **D-019** | PDF- und Office-Dokumente gelangen nicht ungeprüft in den kanonischen Bestand; kontrollierte Ingest- und Quarantäne-Pipeline erforderlich | `accepted` | **A0** | HDI A3 | 2026-07-20 | D-1, D-3 | Capability 5 (Ingest-Quarantäne) wird Voraussetzung für Nicht-Markdown-Quellen |
| **D-020** | `confidential` ist nicht Teil des ersten Piloten, muss aber architektonisch unterstützt werden | `accepted` | **A0** | HDI A4 | 2026-07-20 | D-7 | D-7 wird `not-applicable` für den Pilot; Klasse bleibt im Modell |
| **D-021** | `excluded-from-ai` ist von Anfang an im Daten- und Berechtigungsmodell zu führen; Sperrwirkung mit synthetischen oder unkritischen Testdaten zu prüfen | `accepted` | **A0** | HDI A4 | 2026-07-20 | D-5 | Macht R-30 zu einer konkret prüfbaren Anforderung; **strenger als das bisherige Fundament** |
| **D-022** | Personenbezogene Daten sind nicht Teil des ersten Piloten; spätere Aufnahme erfordert vorher eine gesonderte Datenschutz- und Rechtsgrundlagenprüfung | `accepted` | **A0** | HDI A4 | 2026-07-20 | D-6 | D-6 wird `not-applicable`; OD-09 wird vertagt statt geschlossen |
| **D-023** | Zugriff nur über privates VPN oder privates Netz; keine öffentliche Freigabe interner Dienste | `accepted` | **A0** | HDI A5 | 2026-07-20 | C-5 (Grundsatz) | Zugriffsprofil festgelegt; Technologiewahl bleibt Deployment Required |
| **D-024** | Web-UI und mobile Nutzung gehören zum Pilotumfang; die Web-UI aber erst nach funktionierendem Index, Suche, Brain-First-Retrieval und Benchmark | `accepted` | **A0** | HDI A6 | 2026-07-20 | A-4, A-5, F-6 | Präzisiert D-014 mit einer konkreten Vorbedingung |
| **D-025** | Native Obsidian-Nutzung, Wiki-Pilot und externe Connectoren werden vertagt; Knowledge Graph ist nicht Pilotumfang | `accepted` | **A0** | HDI A6 | 2026-07-20 | A-7 | Vier Conditional-Kriterien bleiben inaktiv |
| **D-026** | Dreistufiges Kriterienmodell: Core Required, Deployment Required, Conditional. G0 sperrt den allgemeinen Produkt-Scope, nicht die Installationsdetails | `accepted` | **A0** | Nova-Review CBP-WP-003 | 2026-07-20 | alle 47 | Blocker von 45 auf 25 reduziert; separates Deployment-Readiness-Gate später zu definieren |

> **Hinweis zu D-016.** In CBP-WP-002 hatte ich „bevorzugte Anwendungslaufzeit"
> zu „vorgesehene" abgeschwächt (Ü-02), gestützt auf Projektübergabe §4 (A5),
> wonach Containerisierung kein Pflichtziel der ersten Phase ist. Der Human
> Maintainer hat nun ausdrücklich „bevorzugte Anwendungslaufzeit" bestätigt.
> **A0 schlägt A5** — die Abschwächung ist damit aufgehoben.
>
> **Nachgeführt in CBP-WP-004:** `docs/architecture/PROJECT_DEFINITION.md`
> trägt jetzt die korrigierte Formulierung mit ausdrücklicher Abgrenzung
> („bevorzugt, aber nicht einzige Laufzeit und keine Produktgrenze"). OD-31 ist
> damit geschlossen; festgehalten in **ADR-0002**.

## Geschlossene offene Entscheidungen

| ID | War offen | Geschlossen durch | Datum |
| --- | --- | --- | --- |
| OD-12 | Prompt Mode „Lean" | D-009 | 2026-07-20 |
| OD-02 | Definition der Context Budgets | CONTEXT_BUDGETS.md; Restpunkt OD-02b | 2026-07-20 |
| OD-01 | Kriterien für Gate G0 | G0_SCOPE_LOCK_CRITERIA.md, dreistufig klassifiziert | 2026-07-20 |
| **OD-21** | Zugriffsweg für Mehrgeräte-Nutzung | **D-023** — privates VPN/Netz; Technologie bleibt Deployment Required | 2026-07-20 |
| **OD-27** | Obsidian-Synchronisationsmodell | **D-025** — serverzentriert zuerst, native Nutzung vertagt | 2026-07-20 |
| **OD-10** | Verfahren bei Secret in der Git-Historie | [SECRET_INCIDENT_RESPONSE.md](../docs/security/SECRET_INCIDENT_RESPONSE.md) — 14 Schritte, Rotation vor Cleanup. **Technische Unterstützung bleibt offen** | 2026-07-20 |
| **OD-32** | Berechtigungsstufen je Bereich und Freigabeverfahren | [PERMISSION_MODEL.md](../docs/security/PERMISSION_MODEL.md) und ADR-0004 — 9 Rollen × 12 Ressourcen. **Technische Durchsetzung bleibt offen** | 2026-07-20 |
| **OD-31** | Nachführungen außerhalb des CBP-WP-003-Scopes | CBP-WP-004: D-016 in `PROJECT_DEFINITION.md` korrigiert, Kriterienzahl auf 47 aktualisiert, Korrektur-Notiz in `CBP-WP-002.md` ergänzt | 2026-07-20 |
| **OD-33** | Definition des Deployment-Readiness-Gates | [DEPLOYMENT_READINESS_CHECK.md](../docs/operations/DEPLOYMENT_READINESS_CHECK.md) und ADR-0005 — DRC vollständig dokumentiert und in G0, Manifest, Profil, README und Brain verlinkt | 2026-07-20 |

## Vertagte Entscheidungen

Nicht geschlossen, aber für den Pilotumfang **nicht mehr blockierend**:

| ID | Entscheidung | Grund der Vertagung |
| --- | --- | --- |
| OD-09 | Rechtsgrundlage für personenbezogene Daten | D-022 — keine PII im Pilot; Prüfung vor späterer Aufnahme |
| OD-20 | Programmiersprache, Suchmaschine, Embedding-Modell | Deployment Required |
| OD-22 | Sicherungsfrequenz und Sicherungsziel | Deployment Required |
| OD-30 | Backup- und Restore-Zielwerte | Deployment Required |

Vertagt heißt **nicht erledigt**. Diese Punkte gehören in das
Deployment-Readiness-Gate.

## Offene Entscheidungen

Legende: **P0** blockiert G0 · **P1** vor Architekturentscheidung · **P2** später.

| ID | Offene Entscheidung | Prio | Adressat | Bezug |
| --- | --- | --- | --- | --- |
| OD-03 | Rang der Kernprinzipien: weitere ADRs über ADR-0001 bis ADR-0005 hinaus | P1 | Human Maintainer | teilweise durch ADR-0001…0005 |
| OD-04 | Minimal nützlicher Funktionsumfang des Piloten | **P0** | Nova | A-8 |
| OD-05 | Ablageort des kanonischen Wissensbestands | **P0** | Human Maintainer | D-1 |
| OD-06 | Quellen im ersten Scope und ausdrückliche Nicht-Quellen | **P0** | Nova | D-1, D-5 |
| OD-07 | Vergabeverfahren für Autoritätsklassen A0–A6 | **P0** | Nova | — |
| OD-08 | Vergabeverfahren für Datenklassen | **P0** | Human Maintainer | D-4 |
| OD-11 | Repository dauerhaft privat? | **P0** | Human Maintainer | A-8 |
| OD-29 | Dauerhafte Behandlung der NDF-Abweichungen AB-03 bis AB-08 | **P0** | Nova + Human Maintainer | ADOPTION_NOTES |
| OD-02b | Kalibrierung der Token-Richtwerte für B0–B4 | P1 | Nova | CONTEXT_BUDGETS |
| OD-13 | Manifest auf `project-manifest.yaml` umstellen | P1 | Nova | AB-03 |
| OD-14 | NDF-Namensschema für Register | P1 | Nova | AB-04 |
| OD-15 | Schnitt einer Wissenseinheit | P1 | Nova | — |
| OD-16 | Bildungsvorschrift der stabilen Source-ID | P1 | Nova | — |
| OD-17 | Verpflichtende Frontmatter-Felder | P1 | Nova | — |
| OD-18 | Filterreihenfolge im Retrieval-Pfad | P1 | Nova | TB-4 |
| OD-19 | Umfang und Format des Retrieval-Trace | P1 | Nova | — |
| OD-23 | Lizenzwahl | P1 | Human Maintainer | D-007 |
| OD-25 | qmd als produktiver Suchdienst — nur nach Prüfung | P1 | Human Maintainer | — |
| OD-26 | Endgültige Repository-Struktur | **P0** | Nova + Human Maintainer | W-05 |
| OD-24 | Akzeptable Ausfallzeit | P2 | Human Maintainer | — |
| OD-28 | Öffentlicher Produktname und Phase-7-Option | P2 | Human Maintainer | — |

## Zusammenfassung

| Kategorie | Anzahl |
| --- | --- |
| Getroffene Entscheidungen | **26** (davon 20 mit A0) |
| Angenommene ADRs | **5** (ADR-0001 bis ADR-0005, alle A1) |
| Neu in CBP-WP-003 | 12 (D-015 bis D-026) |
| Neu in CBP-WP-004 | 0 Entscheidungen, 5 ADRs |
| Geschlossene offene Entscheidungen | **9** (davon 4 in CBP-WP-004) |
| Vertagte Entscheidungen | 4 |
| Offene Entscheidungen | **21** |
| davon **P0** | **8** |

**Keine offene Entscheidung wird als A0 geführt.** Keine Entscheidung wurde aus
reinen Sachangaben abgeleitet — die Infrastrukturangaben aus dem Intake sind
Human-Evidenz, keine Beschlüsse.

## Pflege

Eine getroffene Entscheidung wird **nicht gelöscht**. Änderungen erfolgen durch
einen neuen Eintrag, der den alten als ersetzt kennzeichnet.
