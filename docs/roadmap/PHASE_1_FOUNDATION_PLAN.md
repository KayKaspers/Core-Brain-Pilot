# Phase 1 Foundation Plan — F1 bis F5

| Feld | Wert |
| --- | --- |
| **Status** | **AUTHORIZED FOR PLANNING** |
| **Nicht** | **AUTHORIZED FOR IMPLEMENTATION** |
| Grundlage | G0 **PASSED WITH NOTES**, 2026-07-21, A0 |
| Erfasst in | CBP-WP-008 |
| Autoritätsklasse | A3 |
| Stand | 2026-07-21 |

Überführt die Backlogpunkte **P1 bis P5** aus
[PHASE_1_BACKLOG.md](PHASE_1_BACKLOG.md) in fünf planbare Streams.

> **Keine technische Umsetzung.** Jeder Stream trägt „Implementierung erlaubt:
> **nein**". Ausführbar wird ein Stream erst durch ein eigenes, freigegebenes
> Work Package.

---

## Streamübersicht

| Stream | Backlog | Titel | Blockiert durch |
| --- | --- | --- | --- |
| **F1** | P1 | Repository and Workspace Boundary | — |
| **F2** | P2 | Pilot Source Mapping | F1 |
| **F3** | P3 | Technical Security Foundation | — |
| **F4** | P4 | Ingest Quarantine and Security Scanning | F2, F3 |
| **F5** | P5 | Deterministic Source Registry and Catalog | F2, F4 |

```text
F1 ─────► F2 ─────┐
                  ├──► F4 ──► F5
F3 ───────────────┘
```

**F1 und F3 sind unabhängig und können parallel geplant werden.** F3 ist der
breiteste Enabler — F4 und alle späteren Betriebsschritte hängen daran.

---

## F1 — Repository and Workspace Boundary

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Die Grenze zwischen Core Repository, privatem Operator Workspace und Runtime Data Area entscheidungsreif festlegen; OD-26 vorbereiten |
| **Scope** | Bewertung der Layoutoptionen, Empfehlung, Migrationspfad, Abgrenzung der drei Bereiche |
| **Out of Scope** | Verschieben von Dateien oder Ordnern; OD-26 schließen; Repository-Sichtbarkeit (OD-11) entscheiden |
| **Eingaben** | `REPOSITORY_LAYOUT_OPTIONS.md`, ADR-0006, `PILOT_SOURCE_CONTRACT.md`, Übergabe §13 |
| **Ergebnisse** | [REPOSITORY_AND_WORKSPACE_PLAN.md](REPOSITORY_AND_WORKSPACE_PLAN.md); Entscheidungsvorlage für CBP-WP-009 |
| **Abhängigkeiten** | keine |
| **Relevante ADRs** | **ADR-0006** (bindend), ADR-0001, ADR-0003 |
| **Relevante Risiken** | R-01, R-17 |
| **Datenschutzwirkung** | **Hoch positiv** — die Bereichsgrenze ist der einzige Schutz gegen R-01, der nicht auf Disziplin beruht |
| **Nachweise** | Bewertete Optionen mit Vor- und Nachteilen; benannter Migrationspfad; ausdrückliche A0-Entscheidung zu OD-26 |
| **Abbruchbedingungen** | Eine Option würde privaten Bestand in die Historie des Core-Repositorys bringen · die Entscheidung präjudiziert OD-11 · ein Migrationspfad ist nicht ohne Datenverlust beschreibbar |
| **Rücksetzstrategie** | Rein dokumentarisch — es wurde nichts verschoben. Eine verworfene Empfehlung wird als `rejected` archiviert, nicht gelöscht |
| **Freigabepunkt** | **CBP-WP-009**, interaktiv, Human-Entscheidung zu OD-26 |
| **Implementierung erlaubt** | **nein** |
| **Stand** | **ERREICHT** — OD-26 am 2026-07-21 geschlossen (D-029 Layout-Option B, D-030 Modell W-3, [ADR-0007](../decisions/ADR-0007-repository-und-workspace-grenze.md)). **Keine Reorganisation autorisiert**; Migration bleibt eigenes Work Package. Core-Repository `publication-capable by design`, **nicht veröffentlicht**; Runtime-Daten gegliedert in **RT-1 / RT-2 / RT-3** |

## F2 — Pilot Source Mapping

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Ein Mapping-Schema definieren, mit dem PS-02, PS-03 und PS-04 später konkret zugeordnet werden können |
| **Scope** | Schema, Defaults, Validierungs- und Freigaberegeln, Nachweiskatalog |
| **Out of Scope** | **Reale Pfade, Repository-URLs, Aktivierung eines Mappings**; OD-05 und OD-06 schließen |
| **Eingaben** | `SOURCE_SLOT_MODEL.md`, `PILOT_SOURCE_CONTRACT.md`, ADR-0006, `DATA_CLASSIFICATION.md` |
| **Ergebnisse** | [PILOT_SOURCE_MAPPING_PLAN.md](PILOT_SOURCE_MAPPING_PLAN.md) |
| **Abhängigkeiten** | **F1** — ohne Bereichsgrenze ist unklar, wohin ein Mapping gehört |
| **Relevante ADRs** | ADR-0006, ADR-0003 |
| **Relevante Risiken** | R-01, R-03, R-27 |
| **Datenschutzwirkung** | **Hoch** — je Mapping werden Datenklasse, AI-Transfer und Sichtbarkeit gesetzt; Defaults sind restriktiv |
| **Nachweise** | Mapping validiert · Quelle erreichbar · Rechte minimal · Ausschlüsse wirksam · keine Secrets · Datenklasse bestätigt · AI-Transfer-Regel getestet |
| **Abbruchbedingungen** | Ein Mapping verlangt Schreibrechte ohne Begründung · eine Quelle enthält Secrets · eine Datenklasse ist nicht bestimmbar · ein Ausschluss greift nicht |
| **Rücksetzstrategie** | `enabled: false` setzen; Mapping-Revision erhöhen; bei Löschung Tombstone plus Derived Cleanup |
| **Freigabepunkt** | **CBP-WP-010**, konkrete Mappings erst nach Human-Eingabe |
| **Implementierung erlaubt** | **nein** |
| **Stand** | **SPEZIFIKATION ERREICHT** — Format, Collection-Strategie und Granularität am 2026-07-21 entschieden (D-031, D-032, D-033, [ADR-0008](../decisions/ADR-0008-pilot-source-mapping-konvention.md)); Schema, Validierung, Zustandsmodell und Aktivierungsgate liegen vor. **Kein Mapping erstellt; OD-05 und OD-06 bleiben offen** |

## F3 — Technical Security Foundation

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Das Berechtigungsmodell von einer Dokumentregel in technisch durchsetzbare Kontrollen überführen — planerisch |
| **Scope** | Zwölf Kontrollbereiche, Durchsetzungsreihenfolge, Negativtests, Rollback |
| **Out of Scope** | Bereitstellung, Software- oder Portauswahl, Benutzer-IDs, Hostpfade |
| **Eingaben** | `PERMISSION_MODEL.md`, ADR-0004, `COMPONENT_MODEL.md`, `TRUST_BOUNDARIES.md` |
| **Ergebnisse** | [TECHNICAL_SECURITY_FOUNDATION_PLAN.md](TECHNICAL_SECURITY_FOUNDATION_PLAN.md) |
| **Abhängigkeiten** | keine — **breitester Enabler** |
| **Relevante ADRs** | **ADR-0004**, ADR-0003 |
| **Relevante Risiken** | **R-25**, **R-27**, R-26, R-31, R-02, R-05 |
| **Datenschutzwirkung** | **Höchste im Plan** — ohne F3 bleibt jede Datenklassenregel wirkungslos |
| **Nachweise** | Je Kontrollbereich ein positiver Nachweis **und** ein Negativtest; Auflage 1 der G0-Entscheidung |
| **Abbruchbedingungen** | Eine Kontrolle lässt sich nur über Promptregeln durchsetzen · ein Negativtest schlägt fehl · Root- oder Hostbetrieb wäre nötig · Backup Storage wäre für die Anwendung beschreibbar |
| **Rücksetzstrategie** | Je Kontrolle eine sichere Abschaltung: **restriktiver werden ist immer erlaubt**, permissiver nur mit Freigabe |
| **Freigabepunkt** | **CBP-WP-011** (Spezifikation), später **CBP-WP-012** (Umsetzung) |
| **Implementierung erlaubt** | **nein** |

## F4 — Ingest Quarantine and Security Scanning

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Eine fail-closed Ingest-Pipeline planen: von der Registrierung bis zur Freigabe, mit Human Review vor Indexierung |
| **Scope** | Statusmodell, Freigabekette, Blocker, Negativtests |
| **Out of Scope** | Scanner installieren, PDF-/Office-Parser, produktiver Ingest |
| **Eingaben** | TB-1 und TB-2, `SECRET_INCIDENT_RESPONSE.md`, `DATA_CLASSIFICATION.md`, D-019 |
| **Ergebnisse** | [INGEST_QUARANTINE_PLAN.md](INGEST_QUARANTINE_PLAN.md) |
| **Abhängigkeiten** | **F2** (was aufgenommen wird) und **F3** (wer schreiben darf) |
| **Relevante ADRs** | ADR-0003, ADR-0004 |
| **Relevante Risiken** | **R-32**, R-04, R-01, R-03 |
| **Datenschutzwirkung** | **Hoch** — hier wird die Datenklasse erstmals verbindlich gesetzt |
| **Nachweise** | Kein Pfad von `received` zu `indexed` ohne Freigabe; Negativtests für Secret, `excluded-from-ai`, unbekannte Klasse, unerlaubtes Format, widerrufene Quelle, Tombstone, Sammelanfrage |
| **Abbruchbedingungen** | **Secret-Fund** — blockiert jeden weiteren Ingest · eine Quelle erreicht den Index ohne Freigabe · ein Scanfehler wird übergangen |
| **Rücksetzstrategie** | Quelle auf `quarantined` oder `revoked`; Derived Cleanup; bei Secret-Fund Incident-Prozess nach `SECRET_INCIDENT_RESPONSE.md` |
| **Freigabepunkt** | **CBP-WP-013** |
| **Implementierung erlaubt** | **nein** |

## F5 — Deterministic Source Registry and Catalog

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Ein deterministisches Metadatenregister planen: stabile IDs, Revisionen, Tombstones, reproduzierbarer INDEX |
| **Scope** | Registry-Modell, ID- und Hashregeln, Änderungs- und Löschereignisse, Index-Synchronisation, Rebuild-Vertrag |
| **Out of Scope** | Suchindex bauen, Embeddings, Suchprovider wählen |
| **Eingaben** | Rebuild-Vertrag aus `SYSTEM_ARCHITECTURE.md`, `SOURCE_SLOT_MODEL.md`, ADR-0003 |
| **Ergebnisse** | [SOURCE_REGISTRY_PLAN.md](SOURCE_REGISTRY_PLAN.md) |
| **Abhängigkeiten** | **F2** (Mappings) und **F4** (nur freigegebene Quellen) |
| **Relevante ADRs** | **ADR-0003**, ADR-0006 |
| **Relevante Risiken** | R-10, R-07, R-09 |
| **Datenschutzwirkung** | Mittel — die Registry führt Klassen, setzt sie aber nicht selbst fest |
| **Nachweise** | Zwei Läufe bei unverändertem Input ergeben denselben Zustand · gelöschte Quelle nach Rebuild nicht auffindbar · Registry und Suchindex getrennt |
| **Abbruchbedingungen** | Nichtdeterministisches Ergebnis · gelöschte Quelle bleibt im Index · Autoritätsklasse wird aus einem Pfad abgeleitet · Registry schreibt eine Quelle um |
| **Rücksetzstrategie** | Registry ist Metadatenbestand — Wiederherstellung aus Backup; Derived vollständig neu aufbaubar |
| **Freigabepunkt** | **CBP-WP-014** |
| **Implementierung erlaubt** | **nein** |

---

## Abhängigkeiten im Überblick

| Stream | Braucht | Ermöglicht |
| --- | --- | --- |
| F1 | — | F2 |
| F2 | F1 | F4, F5 |
| F3 | — | F4, Betrieb allgemein |
| F4 | F2, F3 | F5 |
| F5 | F2, F4 | Retrieval-Pilot (P6) |

**Wichtigste Enabler:**

1. **F3** — ohne technische Sicherheitsgrundlage bleiben alle Datenschutz- und
   Berechtigungsregeln wirkungslos. Blockiert F4 und den gesamten Betrieb.
2. **F1** — ohne Bereichsgrenze ist jedes Mapping ortlos.

## Bezug zu den G0-Auflagen

| Auflage | Stream |
| --- | --- |
| Technische Durchsetzung des Berechtigungsmodells | **F3** |
| Negativtests für `excluded-from-ai` | **F3** (Kontrollbereich 11), Nachweis in P8 |
| V0-/V1-Benchmark | nach F5, Backlogpunkt P7 |
| DRC auf `ready` | nach F3, Backlogpunkt P10 |
| Backup-, Restore- und Rebuild-Test | F5 liefert den Rebuild-Vertrag, Nachweis in P9 |

## Status

**AUTHORIZED FOR PLANNING.** Fünf Streams geplant, **keiner zur Umsetzung
autorisiert**. Es wurde nichts gebaut, nichts installiert, nichts angebunden,
nichts verschoben und nichts gemessen.

**Stand nach CBP-WP-009:** Der Entscheidungsteil von **F1 ist erreicht** —
OD-26 ist geschlossen. Damit ist **F2 nicht mehr blockiert**; die
Bereichsgrenze steht. **F1 ist damit nicht abgeschlossen**: die Migration in
die Zielstruktur ist weder geplant noch autorisiert.

**Stand nach CBP-WP-010:** Der Spezifikationsteil von **F2 ist erreicht** —
Mappingformat, Collection-Strategie und Granularität sind durch A0 entschieden,
Schema, Validierung, Zustandsmodell und Aktivierungsgate liegen vor. **F2 ist
damit nicht abgeschlossen**: Es existiert kein Mapping, keine angebundene
Quelle und kein Validator. **OD-05 und OD-06 bleiben offen**, das
Aktivierungsgate steht auf `NOT EVALUATED`.

**F4 bleibt blockiert** — es braucht zusätzlich **F3**, das noch nicht begonnen
hat.
