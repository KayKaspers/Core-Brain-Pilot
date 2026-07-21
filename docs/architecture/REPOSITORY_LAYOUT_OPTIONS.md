# Repository Layout Options — Entscheidungsvorlage

| Feld | Wert |
| --- | --- |
| **Status** | **ENTSCHIEDEN** — Option **B** gewählt |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-004 · **entschieden in CBP-WP-009** |
| Autoritätsklasse | A3 (Entscheidungsvorlage) |
| Betrifft | **OD-26 — geschlossen**, Widerspruch W-05, OI-07 |
| Stand | 2026-07-21 |

> **Entscheidung liegt vor.** Der Human Maintainer hat am 2026-07-21
> **Option B (Ziel-Monorepo)** als Zielstruktur gewählt — **D-029**, Autorität
> **A0**, festgehalten in
> [ADR-0007](../decisions/ADR-0007-repository-und-workspace-grenze.md).
>
> **Die Entscheidung autorisiert keine Verschiebung.** Das aktuelle Layout
> bleibt bestehen, bis ein separates, ausdrücklich freigegebenes
> Migrations-Work-Package vorliegt. Die Migration muss nachvollziehbar,
> schrittweise, rücksetzbar und **ohne Verlust der Git-Historie** geplant
> werden.
>
> **Sie autorisiert auch keine Veröffentlichung.** Wo dieses Dokument von
> „Open-Source-Fähigkeit" oder „veröffentlichbar" spricht, ist eine
> **Bauweise** gemeint — `publication-capable by design` —, kein
> Freigabezustand. Das Repository bleibt **privat**; eine Veröffentlichung
> benötigt eine separate **A0-Entscheidung** (OD-11), ebenso Lizenz (OD-23) und
> Produktname (OD-28).

**Es wurde keine Datei und kein Ordner verschoben.** Dieses Dokument
vergleicht, es reorganisiert nicht.

---

## Ausgangslage

Drei Strukturvorstellungen stehen nebeneinander:

| Quelle | Vorstellung | Klasse |
| --- | --- | --- |
| Projektübergabe §13 | `core/`, `deployments/`, `docs/`, `examples/` — ausdrücklich **noch nicht freigegeben** | A5 |
| NDF v1.0.0 | `project-manifest.yaml`, `project-brain/DECISIONS.md`, `prompts/claude/work-packages/` | A1 |
| Aktueller Stand | Struktur aus CBP-WP-001 | A2 |

Die Übergabe stellt selbst fest, dass die konkrete Struktur im Projekt geplant
werden muss. Daraus folgt der vorläufige Status von AB-03 bis AB-08.

---

## Option A — Aktuelles dokumentationsorientiertes Layout

```text
Core-Brain-Pilot/
├── docs/            architecture · decisions · discovery · ndf · operations
│                    · privacy · product · security
├── project-brain/   PROJECT_BRAIN.md
├── project-system/  Profil · Manifest · Matrix · Register · Queue · Prüfungen
└── work-packages/   CBP-WP-*.md
```

**Charakter:** Ein reines Dokumentationsrepository. Kein Code, keine Trennung
zwischen Produkt und Wissen.

| Kriterium | Bewertung |
| --- | --- |
| NDF-Konformität | **teilweise** — AB-03 bis AB-08 sind Abweichungen vom Kanon |
| Portabilität | neutral — nichts zu portieren |
| Schutz privater Wissensdaten | **schwach** — kein struktureller Ort für privaten Bestand; Trennung wäre reine Disziplin |
| Open-Source-Fähigkeit | **schwach** — Produkt und Projektinterna liegen zusammen |
| Deploymentprofile | kein Ort für profilspezifische Artefakte |
| Testbarkeit | kein Ort für Tests |
| Migrationsaufwand | **null** |

## Option B — Monorepo

```text
Core-Brain-Pilot/
├── core/         deployment-neutraler Kern
├── adapters/     Suche · UI · Backup · MCP
├── deployments/  proxmox/ · linux-vm/ · physical/ · docker/ · local/
├── config/       Konfigurationsvorlagen, keine Werte
├── docs/         Architektur, Betrieb, Sicherheit
├── examples/     Beispielbestände, synthetisch
└── tests/        Unit, Integration, Retrieval-Benchmark
```

**Charakter:** Alles in einem Repository, aber sauber nach Verantwortung
geschnitten. Entspricht der Skizze aus Projektübergabe §13, erweitert um
`adapters/`, `config/` und `tests/`.

| Kriterium | Bewertung |
| --- | --- |
| NDF-Konformität | **gut** — `project-system/`, `project-brain/` und `docs/ndf/` bleiben erhalten |
| Portabilität | **stark** — `deployments/` bildet die fünf Profile ab; der Kern bleibt frei davon |
| Schutz privater Wissensdaten | **mittel** — Trennung möglich, aber nicht erzwungen; ein Fehlgriff landet im selben Repository |
| Open-Source-Fähigkeit | **gut**, solange kein privater Bestand hineingerät |
| Deploymentprofile | **direkt abgebildet** — je Profil ein Verzeichnis |
| Testbarkeit | **gut** — `tests/` und `examples/` mit synthetischen Daten |
| Migrationsaufwand | mittel — Verschiebungen, aber keine inhaltlichen Änderungen |

## Option C — Getrenntes Core- und Wissens-Repository

```text
Core-Brain-Pilot/          veröffentlichungsfähig gebaut, nicht freigegeben
├── core/ adapters/ deployments/ config/ docs/ examples/ tests/
└── project-system/ project-brain/ work-packages/

Core-Brain-Vault/          dauerhaft privat
├── canonical/             kanonischer Wissensbestand
├── quarantine/            Ingest
└── .gitignore             derived niemals
```

**Charakter:** Zwei Repositories mit verschiedenem Lebenszyklus und
verschiedener Sichtbarkeit. Das Produkt kann veröffentlicht werden, ohne dass
der Wissensbestand je in dieselbe Historie gerät.

| Kriterium | Bewertung |
| --- | --- |
| NDF-Konformität | **gut** — NDF-Artefakte bleiben im Core-Repository |
| Portabilität | **stark** — wie B |
| Schutz privater Wissensdaten | **stark** — **strukturell** getrennt, nicht nur durch Disziplin. Ein versehentlicher Commit in das falsche Repository ist eine sichtbare Handlung |
| Open-Source-Fähigkeit | **stark** — der öffentliche Teil enthält konstruktiv keinen privaten Bestand |
| Deploymentprofile | wie B |
| Testbarkeit | wie B; Benchmark braucht synthetische Daten in `examples/` |
| Migrationsaufwand | **hoch** — zweites Repository, zwei Historien, doppelte Abläufe |

---

## Vergleich

| Kriterium | A | B | C |
| --- | --- | --- | --- |
| NDF-Konformität | teilweise | gut | gut |
| Portabilität | neutral | stark | stark |
| **Schutz privater Wissensdaten** | **schwach** | mittel | **stark** |
| **Open-Source-Fähigkeit** | schwach | gut | **stark** |
| Deploymentprofile | fehlt | direkt | direkt |
| Testbarkeit | fehlt | gut | gut |
| **Migrationsaufwand** | **null** | mittel | **hoch** |
| Betriebsaufwand | niedrig | niedrig | erhöht (zwei Repositories) |

---

## Empfehlung

**Option B jetzt, Option C als vorbereiteter Schritt — nicht Option A auf
Dauer.**

Begründung in drei Punkten:

**1. Option A ist als Zielzustand nicht tragfähig.** Sie hat keinen Ort für
Adapter, Deploymentprofile und Tests. Sobald Phase 2 beginnt, entsteht Struktur
ohnehin — dann besser geplant als gewachsen. Der Migrationsaufwand ist heute am
niedrigsten: es gibt keinen Code, der brechen könnte.

**2. Option C löst das wichtigste Risiko, aber noch nicht jetzt.** Die
strukturelle Trennung von Produkt und privatem Wissen ist die einzige Antwort
auf R-01, die nicht auf Disziplin beruht. Sie setzt aber zwei Entscheidungen
voraus, die offen sind: die Repository-Sichtbarkeit (OD-11) und der Ablageort
des kanonischen Bestands (OD-05). Solange beide offen sind, wäre C eine
Vorwegnahme.

**3. B ist der kleinste Schritt, der C nicht verbaut.** Wer B wählt, kann
später den Wissensbestand herauslösen, ohne den Kern anzufassen. Wer bei A
bleibt, muss zweimal migrieren.

**Konkreter Vorschlag:** Option B in einem eigenen Work Package nach G0
umsetzen und dabei `canonical/` von Beginn an so schneiden, dass eine spätere
Herauslösung nach C eine reine Verschiebung bleibt.

### Was die Empfehlung nicht entscheidet

- **AB-03 bis AB-08** bleiben offen (OD-29). Insbesondere die Frage
  `PROJECT_MANIFEST.md` gegen `project-manifest.yaml` (OD-13) ist unabhängig
  von der Layoutwahl.
- **OD-05** (Ablageort des kanonischen Bestands) und **OD-11**
  (Repository-Sichtbarkeit) müssen vor C beantwortet sein.
- Ob `examples/` synthetische Daten enthält, hängt am Benchmarkentwurf
  (G-1 bis G-6).

---

## Status

**ENTSCHIEDEN — Option B.** Keine Reorganisation durchgeführt, keine Datei
verschoben.

**OD-26 ist am 2026-07-21 geschlossen** — durch **D-029** (Layout, dieses
Dokument) und **D-030** (Bereichsmodell W-3,
[REPOSITORY_AND_WORKSPACE_PLAN.md](../roadmap/REPOSITORY_AND_WORKSPACE_PLAN.md)).
Beide Teilentscheidungen waren erforderlich; eine allein hätte OD-26 nicht
geschlossen.

Die damalige Empfehlung „Option B jetzt, Option C vorbereitet" ist bestätigt:
Option C entspricht Modell **W-2** und bleibt vorbereitet, aber **nicht
beschlossen**.

**Weiterhin offen:** AB-03 bis AB-08 (OD-29), OD-13 (Manifestformat), OD-11
(Sichtbarkeit) sowie Zeitpunkt und Zuschnitt der Migration.
