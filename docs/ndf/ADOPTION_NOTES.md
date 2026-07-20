# NDF Adoption Notes — dokumentierte Abweichungen

| Feld | Wert |
| --- | --- |
| Framework | Nova Development Framework **v1.0.0** |
| Erfasst in | CBP-WP-001, überarbeitet in CBP-WP-002 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

Grundsatz: **keine parallelen doppelten Strukturen.** Wo NDF und Work Package
unterschiedliche Pfade vorsehen, existiert genau **eine** Datei.

## Status der Abweichungen

| Status | Bedeutung |
| --- | --- |
| `decided` | Entschieden, dauerhaft |
| `provisionally accepted for bootstrap` | Für den Bootstrap akzeptiert, **nicht** dauerhaft bestätigt |
| `requires decision before G0` | Muss vor dem Scope Lock entschieden werden |

> **Wichtig.** AB-03 bis AB-08 sind **nicht** dauerhaft akzeptiert. Sie tragen
> alle den Status `provisionally accepted for bootstrap` **und**
> `requires decision before G0`. Projektübergabe §13 stellt ausdrücklich fest,
> dass die konkrete Repository-Struktur noch nicht freigegeben ist. Erfasst als
> OD-29, offener Widerspruch W-05.

## Übersicht

| ID | Abweichung | Status |
| --- | --- | --- |
| AB-01 | Prompt Mode „Lean" | **`decided`** |
| AB-02 | Context Budgets B0–B4 kein NDF-Konzept | **`decided`** |
| AB-03 | Manifest als Markdown statt YAML | `provisionally accepted for bootstrap` · `requires decision before G0` |
| AB-04 | Register in `project-system/` | `provisionally accepted for bootstrap` · `requires decision before G0` |
| AB-05 | `project-brain/` schlank | `provisionally accepted for bootstrap` · `requires decision before G0` |
| AB-06 | `work-packages/` flach | `provisionally accepted for bootstrap` · `requires decision before G0` |
| AB-07 | `docs/ndf/` ohne WORKFLOW/QUALITY_GATES/RELEASE_PROCESS | `provisionally accepted for bootstrap` · `requires decision before G0` |
| AB-08 | COMPLIANCE_CHECK und HEALTH_SCORE ergänzt | `provisionally accepted for bootstrap` · `requires decision before G0` |
| AB-09 | Dokumentationssprache Deutsch | `decided` |
| AB-10 | Umlaut-Transkription | **aufgehoben** |

## Geprüfte NDF-Dokumente

`README.md` · `framework/standards/WORK_PACKAGE_TYPES.md` ·
`framework/standards/WORK_PACKAGE_LIFECYCLE.md` ·
`docs/agent-workflows/NDF_PROMPT_MODES.md` ·
`docs/agent-workflows/NDF_CONTEXT_ECONOMY.md` ·
`docs/workflow/NOVA_CHATGPT_ROLE.md` · `framework/project-system/templates/` ·
`framework/project-starter/templates/` ·
`framework/project-starter/templates/project-system-folder-structure.md`

## Übernommene Konventionen

Rollenmodell Nova → Implementation Agent → Human Maintainer · Lifecycle
`Classify → Plan → Execute → Report to Nova → Review → Commit` · WP-Typ
`docs-only` · Prompt Modes Full/Standard/Short · fünf Kontextschichten ·
Compact Context Summary · Context Packs · Verzeichnisnamen `project-system/`
und `project-brain/` · Dateinamen in Großbuchstaben · Statuswert `planned` ·
Queue-Spalten `ID | Title | Priority | Status | Prompt` · Regel „keine autonomen
Commits oder Pushes" · Fail-closed- und documentation-only-Haltung (ADR-0032) ·
kein `LICENSE`

---

## AB-01 — Prompt Mode „Lean" · `decided`

**Feststellung.** CBP-WP-001 deklarierte `Prompt Mode: Lean`. NDF v1.0.0 kennt
genau drei Modi: **Full**, **Standard**, **Short**.

Der Quellenabgleich hat den Ursprung geklärt: **Projektübergabe §14 (A5)**
empfiehlt „Lean Mode bevorzugen" als NDF-Nutzungsregel. Gleichzeitig heißt B1
in Projektübergabe §8 „Lean". Die Übergabe hat den Budgetnamen auf die
Prompt-Ebene übertragen.

**Entscheidung (D-009, A0).** „Lean" ist **kein** NDF Prompt Mode, sondern
ausschließlich der Name des Context Budgets **B1**. Die Absicht der Übergabe —
sparsamer Kontext — wird über die Context Budgets abgebildet.

CBP-WP-001 wurde rückwirkend als **Standard Prompt Mode** eingeordnet.

Siehe Widerspruch W-01, geschlossene Entscheidung OD-12.

## AB-02 — Context Budgets B0–B4 · `decided`

**Feststellung.** NDF v1.0.0 kennt keine benannten Budgetstufen; die Context
Economy arbeitet mit fünf Kontextschichten, Compact Context Summary und Context
Packs.

**Entscheidung (D-009, A0).** Beides wird getrennt geführt:

| Konzept | Herkunft | Gegenstand |
| --- | --- | --- |
| Context Economy, Schichten 1–5 | NDF v1.0.0 (A1) | Kontext eines **Agentenauftrags** |
| Context Budgets B0–B4 | Core Brain Pilot, Übergabe §8 (A5) | Umfang eines **Retrieval-Ergebnisses** |

Definiert in
[../architecture/CONTEXT_BUDGETS.md](../architecture/CONTEXT_BUDGETS.md).
Verwechslungsrisiko als R-24 erfasst.

## AB-03 — Projektmanifest als Markdown · vorläufig

NDF v1.0.0 sieht `project-system/project-manifest.yaml` vor. CBP-WP-001 erlaubte
nur Markdown, `.gitignore` und Ordner.

**Vorläufig:** `PROJECT_MANIFEST.md`. **Empfehlung:** Umstellung auf
`project-manifest.yaml`, Markdown-Fassung **ersetzen**, nicht ergänzen. OD-13.

## AB-04 — Register in `project-system/` · vorläufig

NDF sieht `project-brain/DECISIONS.md` und `RISKS.md` vor; CBP-WP-001 forderte
`project-system/DECISION_REGISTER.md` und `RISK_REGISTER.md`.

Die NDF-Pendants wurden **bewusst nicht** zusätzlich angelegt.
`PROJECT_BRAIN.md` verweist auf die Register. OD-14.

## AB-05 — `project-brain/` schlank · vorläufig

Nur `PROJECT_BRAIN.md` angelegt. `DECISIONS.md` und `RISKS.md` siehe AB-04,
offene Fragen in `docs/discovery/`. `LESSONS_LEARNED` wird angelegt, sobald es
Projekthistorie gibt; die Abschnitte sind als Gliederung erhalten.

## AB-06 — `work-packages/` flach · vorläufig

NDF sieht `prompts/claude/work-packages/` vor. Das flache Verzeichnis ist
agent-neutral — passend zur Werkzeugneutralität.

## AB-07 — `docs/ndf/` reduziert · vorläufig

NDF sieht `WORKFLOW.md`, `QUALITY_GATES.md` und `RELEASE_PROCESS.md` vor.
Angelegt sind `README.md` und `ADOPTION_NOTES.md`.

`QUALITY_GATES.md` und `RELEASE_PROCESS.md` fehlen weiterhin bewusst: Die
G0-Kriterien liegen jetzt in
[../discovery/G0_SCOPE_LOCK_CRITERIA.md](../discovery/G0_SCOPE_LOCK_CRITERIA.md),
ein allgemeines Gate-Dokument wäre derzeit Duplikat. Ein Releaseprozess ohne
Implementierung und Lizenzentscheidung bleibt Spekulation.

## AB-08 — COMPLIANCE_CHECK und HEALTH_SCORE ergänzt · vorläufig

Beide gehören zur kanonischen NDF-Ordnerstruktur, waren aber in der
Zielstruktur von CBP-WP-001 nicht aufgeführt. Offengelegte Ergänzung, keine
stillschweigende Scope-Erweiterung.

## AB-09 — Sprache Deutsch · `decided`

Projektdokumentation auf Deutsch. Englische NDF-Fachbegriffe (Work Package,
Context Pack, Gate, Prompt Mode, Capability) bleiben unübersetzt, damit sie auf
die NDF-Quellen zurückführbar sind. Dateinamen folgen dem englischen
NDF-Schema in Großbuchstaben.

## AB-10 — Umlaut-Transkription · **aufgehoben**

**Frühere Fassung:** CBP-WP-001 verwendete `ae`, `oe`, `ue`, `ss` statt
Umlauten, zur Vermeidung von Encoding-Problemen.

**Aufgehoben durch D-012 (A0).** Neue und geänderte Dokumente verwenden UTF-8
mit echten deutschen Umlauten. In CBP-WP-002 wurden alle geänderten Dateien
entsprechend umgestellt.

---

## Handoff-Abschlussformat

*Ergänzt in CBP-WP-002 als F-12. Quelle: Projektübergabe §20.*

Jede größere Projektphase endet mit einem Block:

```text
# BEGIN CORE-BRAIN-HANDOFF
...
# END CORE-BRAIN-HANDOFF
```

Pflichtbestandteile: aktueller Projektstatus · bestätigte Entscheidungen ·
offene Annahmen · aktive Risiken · aktuelles Work Package · erzielte Evidenz ·
nächstes Gate · nächster autorisierter Schritt · Do-not-start-Liste ·
Auswirkungen auf Core Vision, NDF und andere Core-Projekte.

Dieses Format ergänzt den NDF Implementation Report, es ersetzt ihn nicht: Der
Report geht an Nova nach jedem Work Package, der Core-Brain-Handoff schließt
eine **Phase** ab.

Bisher wurde kein Core-Brain-Handoff erzeugt — Phase 0 läuft noch.

## Nicht übernommen

| Gegenstand | Grund |
| --- | --- |
| v1.1-Planung | Ausdrücklich untersagt |
| `.claude/`-Skills-Bibliothek | Nicht Gegenstand der bisherigen Work Packages; neue NDF-Skills stehen auf der Sperrliste |
| `scripts/`, `build/`, `.github/` | Skripte und CI-Workflows verboten |
| `LICENSE` | Ausdrücklich verboten; Lizenzwahl offen (OD-23) |
| `branding/` | Öffentliches Branding gesperrt |
| `academy/`, `examples/` | Bestandteile des Framework-Repositorys, nicht eines Zielprojekts |
