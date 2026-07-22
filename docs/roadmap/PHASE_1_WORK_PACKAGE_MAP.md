# Phase 1 Work Package Map — CBP-WP-009 bis CBP-WP-014

| Feld | Wert |
| --- | --- |
| **Status aller Work Packages** | **`proposed`** |
| **Implementierung autorisiert** | **nein** |
| Stream-Grundlage | [PHASE_1_FOUNDATION_PLAN.md](PHASE_1_FOUNDATION_PLAN.md) (F1–F5) |
| Backlog-Grundlage | [PHASE_1_BACKLOG.md](PHASE_1_BACKLOG.md) (P1–P5) |
| Erfasst in | CBP-WP-008 |
| Autoritätsklasse | A3 |
| Stand | 2026-07-21 |

**Kein Work Package in dieser Karte ist freigegeben.** Keines steht auf
`active`. Ein Vorschlag wird erst durch eine ausdrückliche Freigabe des Human
Maintainers ausführbar — Regel 6 der Work Package Queue.

---

## Überblick

| ID | Titel | Typ | Stream | Status | Implementierung autorisiert |
| --- | --- | --- | --- | --- | --- |
| **CBP-WP-009** | Repository Boundary Decision | `docs-only`, interaktiv | F1 | **`in-review`** — ausgeführt 2026-07-21 | **nein** |
| **CBP-WP-010** | Pilot Source Mapping Specification | `docs-only`, interaktiv | F2 | **`in-review`** — ausgeführt 2026-07-21 | **nein** |
| **CBP-WP-011** | Technical Security Foundation Specification | `docs-only`, interaktiv | F3 | **`in-review`** — ausgeführt 2026-07-21 | **nein** |
| **CBP-WP-012** | Foundation Runtime Skeleton | implementation | F3 | **`committed`** — `1f55234` | **ausgeführt** |
| **CBP-WP-013** | Ingest Quarantine Minimum Viable Pipeline | implementation | F4 | **`in-review`** — ausgeführt 2026-07-22 | **ausgeführt** (A0 WITH NOTES) |
| **CBP-WP-014** | Deterministic Source Registry and Catalog | spätere Implementierung | F5 | **`proposed`** | **nein** |

**Die ersten drei sind `docs-only`.** CBP-WP-012 war das erste Paket mit
technischer Wirkung (committed); **CBP-WP-013** ist das zweite — ein lokaler,
synthetisch testbarer Quarantäneprototyp, `in-review`, **nicht produktiv**.

---

## CBP-WP-009 — Repository Boundary Decision

| Feld | Inhalt |
| --- | --- |
| **ID** | CBP-WP-009 |
| **Typ** | `docs-only`, **interaktiv** |
| **Ziel** | **OD-26 durch eine ausdrückliche Human-Entscheidung schließen** — Layoutoption und Bereichsmodell |
| **Voraussetzungen** | CBP-WP-008 committed |
| **Erlaubter Scope** | Entscheidungsfragebogen ausgeben; gegebene Entscheidung im Wortlaut aufzeichnen; ADR entwerfen; Register nachführen |
| **Verbotener Scope** | **Jede Reorganisation**; Datei oder Ordner verschieben; OD-26 ohne Human-Entscheidung schließen; OD-05, OD-06, OD-11 vorwegnehmen |
| **Nachweise** | Aufgezeichnete Entscheidung im Wortlaut; ADR mit Status; dokumentierte Bereichsgrenze |
| **Abbruchbedingungen** | Human Maintainer entscheidet nicht oder nur teilweise → anhalten, **nicht annehmen** (SB-12) |
| **Erwartete Risiken** | R-01, R-17 |
| **Review Gate** | Nova-Review, dann Human-Maintainer-Entscheidung |
| **Status** | **`in-review`** — ausgeführt am 2026-07-21 |
| **Ergebnis** | **OD-26 geschlossen** — D-029 (Layout-Option B) und D-030 (Modell W-3), [ADR-0007](../decisions/ADR-0007-repository-und-workspace-grenze.md) `accepted` |
| **Implementierung autorisiert** | **nein** |

**Die Entscheidung geht der Verschiebung voraus.** Eine Reorganisation wäre ein
eigenes, späteres Paket — **und ist es geblieben**: D-029 hält ausdrücklich
fest, dass das aktuelle Layout bis zu einem separaten, freigegebenen
Migrations-Work-Package bestehen bleibt.

## CBP-WP-010 — Pilot Source Mapping Specification

| Feld | Inhalt |
| --- | --- |
| **ID** | CBP-WP-010 |
| **Typ** | `docs-only`, interaktiv |
| **Ziel** | Konkrete Mappings für PS-02, PS-03, PS-04 spezifizieren; **OD-05 und OD-06 vorbereiten** |
| **Voraussetzungen** | **CBP-WP-009 entschieden** — ohne Bereichsgrenze kein Mapping |
| **Erlaubter Scope** | Mappingspezifikation je Slot **nach Human-Eingabe**; Ausschlussregeln; Freigabeverfahren |
| **Verbotener Scope** | **Keine Aktivierung**; kein Ingest; keine realen Pfade oder privaten Repository-URLs im Core Repository; keine Secrets |
| **Nachweise** | Mapping validiert; Quelle erreichbar; Rechte minimal; Ausschlüsse wirksam; keine Secrets; Datenklasse bestätigt; AI-Transfer-Regel getestet |
| **Abbruchbedingungen** | Ein realer Pfad oder Secret soll ins Core Repository → **sofort anhalten** (SB-02, SB-01) |
| **Erwartete Risiken** | **R-01**, R-27, R-03 |
| **Review Gate** | Nova-Review; Freigabe der Quellenauswahl durch den Human Maintainer |
| **Status** | **`in-review`** — ausgeführt am 2026-07-21 |
| **Ergebnis** | **D-031, D-032, D-033** (A0) · [ADR-0008](../decisions/ADR-0008-pilot-source-mapping-konvention.md) `accepted` · Spezifikation, Schema (31 Felder), Validierung (24 Regeln), Zustandsmodell (10 Zustände), 10 synthetische Beispiele, Aktivierungsgate (`NOT EVALUATED`) |
| **Implementierung autorisiert** | **nein** |

**Ausgefüllte Mappings gehören in den Operator Workspace**, nicht in dieses
Repository (ADR-0006). Jedes bleibt `enabled: false`.

**OD-05 und OD-06 blieben offen** — die Konvention steht, die konkreten Quellen
nicht. Das war beabsichtigt: Die Spezifikation ist unabhängig davon, welche
Quellen später angebunden werden.

## CBP-WP-011 — Technical Security Foundation Specification

| Feld | Inhalt |
| --- | --- |
| **ID** | CBP-WP-011 |
| **Typ** | `docs-only` |
| **Ziel** | Die zwölf Kontrollbereiche KB-01 bis KB-12 in prüfbare technische Kontrollen und **Abnahmetests** überführen |
| **Voraussetzungen** | CBP-WP-009; unabhängig von CBP-WP-010 |
| **Erlaubter Scope** | Kontrollspezifikation; Abnahmetestdefinition; Rollen- und Ressourcenzuordnung; Durchsetzungsreihenfolge |
| **Verbotener Scope** | **Noch keine Bereitstellung**; keine Installation; keine Portfestlegung; keine UID-Festlegung; keine Hostpfade |
| **Nachweise** | Je Kontrollbereich: Kontrolle, Nachweisform, **Negativtest**, Rollback — vollständig spezifiziert |
| **Abbruchbedingungen** | Eine Kontrolle ruht allein auf Promptregeln → als **nicht durchgesetzt** kennzeichnen (SB-03) |
| **Erwartete Risiken** | **R-25**, **R-27**, R-26 |
| **Review Gate** | Nova-Review; Abnahme der Testdefinition durch den Human Maintainer |
| **Status** | **`in-review`** — ausgeführt am 2026-07-21 |
| **Ergebnis** | **D-034 bis D-037** (A0) · [ADR-0009](../decisions/ADR-0009-technische-sicherheitsgrundlage.md) `accepted` · Spezifikation (18 Abschnitte), Identitätsmodell, Secret-Vertrag, Egress-Policy, Evidence-Policy, Abnahmematrix (31 Negativtests), Readiness Gate (24 Punkte, `NOT EVALUATED`). **OD-34 und OD-35 geschlossen** |
| **Implementierung autorisiert** | **nein** |

**Auflage 1 der G0-Entscheidung** beginnt hier — als Spezifikation, nicht als
Umsetzung. **Alle zwölf Kontrollen stehen auf `DOCUMENTED ONLY`.**

## CBP-WP-012 — Foundation Runtime Skeleton

| Feld | Inhalt |
| --- | --- |
| **ID** | CBP-WP-012 |
| **Typ** | **spätere Implementierung** |
| **Ziel** | Minimales, nicht privilegiertes Laufzeitgerüst mit durchgesetzten Kontrollen KB-01 bis KB-04 und KB-08 |
| **Voraussetzungen** | **CBP-WP-011 abgenommen**; ausdrückliche Freigabe des Human Maintainers |
| **Erlaubter Scope** | *Erst nach Autorisierung festzulegen* |
| **Verbotener Scope** | **Alles** — dieses Work Package ist **nicht autorisiert** |
| **Nachweise** | Rechte- und Identitätsauflistung; **bestandene Negativtests** zu KB-01 bis KB-04, KB-08 |
| **Abbruchbedingungen** | Root- oder Hostausführung; unerwarteter Schreibzugriff auf Canonical; Secretfund (SB-01, SB-04 der Stop-Bedingungen) |
| **Erwartete Risiken** | R-26, **R-25**, R-01 |
| **Review Gate** | Human-Maintainer-Freigabe **vor** Beginn, Nova-Review danach |
| **Status** | **`in-review`** — ausgeführt am 2026-07-21 |
| **Ergebnis** | Human-Autorisierung APPROVE WITH NOTES (A0); Stack A1, CLI B1, Struktur C1. Additiver Python-Skeleton, **9 Module**, lokale CLI, vier verweigernde Ports, **69 Tests bestanden**, `run` fail-closed (Exit 4). **Keine KB-Kontrolle durchgesetzt** — alle `DOCUMENTED ONLY` |
| **Implementierung autorisiert** | **ja, ausgeführt** — nur der lokale Skeleton, kein produktiver Betrieb |

**Erstes Work Package mit technischer Wirkung.** Bewusst als Gerüst
geschnitten: keine Suche, kein Retrieval, keine Oberfläche, keine angebundene
Quelle. **Die Umsetzung von KB-01…KB-12 auf der Ziel-VM steht aus** — der
Skeleton prüft lokal, er setzt nicht durch.

## CBP-WP-013 — Ingest Quarantine Minimum Viable Pipeline

| Feld | Inhalt |
| --- | --- |
| **ID** | CBP-WP-013 |
| **Typ** | **spätere Implementierung** |
| **Ziel** | Fail-closed-Pipeline mit zwölf Schritten und zehn Statuswerten, Markdown zuerst |
| **Voraussetzungen** | **CBP-WP-010 und CBP-WP-012**; ausdrückliche Freigabe |
| **Erlaubter Scope** | *Erst nach Autorisierung festzulegen* |
| **Verbotener Scope** | **Alles**; insbesondere produktiver Ingest, PDF-/Office-Parser, realistische Secrets |
| **Nachweise** | **Negativtests N-01 bis N-12 bestanden**; keine Quelle gelangt von `received` direkt nach indexiert |
| **Abbruchbedingungen** | Weg von Quarantäne nach kanonisch ohne Human Review; Secretfund; `excluded-from-ai` durchgebrochen |
| **Erwartete Risiken** | **R-32**, **R-31**, R-30, R-04, R-01 |
| **Review Gate** | Human-Maintainer-Freigabe vor Beginn; Abnahme der Negativtests danach |
| **Status** | **`proposed`** |
| **Implementierung autorisiert** | **nein** |

**PDF und Office bleiben `deferred`.** Tests laufen mit **synthetischen** Daten.

## CBP-WP-014 — Deterministic Source Registry and Catalog

| Feld | Inhalt |
| --- | --- |
| **ID** | CBP-WP-014 |
| **Typ** | **spätere Implementierung** |
| **Ziel** | Registry mit stabilen IDs, Revisionen, Tombstones und reproduzierbarem INDEX |
| **Voraussetzungen** | **CBP-WP-013**; ausdrückliche Freigabe; OD-16 entschieden |
| **Erlaubter Scope** | *Erst nach Autorisierung festzulegen* |
| **Verbotener Scope** | **Alles**; insbesondere Suchintegration und Retrieval-Implementierung |
| **Nachweise** | **Zwei Läufe, gleicher Indexzustand**; **Tombstone überlebt Rebuild**; Derived Cleanup wirksam; Rebuild aus kanonisch + Registry |
| **Abbruchbedingungen** | Registry nicht reproduzierbar; Index enthält gelöschte Quelle; fehlender Rollback |
| **Erwartete Risiken** | **R-10**, R-07, R-06 |
| **Review Gate** | Human-Maintainer-Freigabe vor Beginn; Abnahme des Rebuild-Nachweises danach |
| **Status** | **`proposed`** |
| **Implementierung autorisiert** | **nein** |

---

## Abhängigkeiten als gerichtete Reihenfolge

```text
CBP-WP-009 ─┬─► CBP-WP-010 ─────────────┐
            │                           ├─► CBP-WP-013 ─► CBP-WP-014
            └─► CBP-WP-011 ─► CBP-WP-012┘
```

| Regel | Inhalt |
| --- | --- |
| **A** | **CBP-WP-009 geht allen voraus** — ohne Bereichsgrenze kein Mapping und keine Ablage |
| **B** | CBP-WP-010 und CBP-WP-011 sind **parallel** möglich |
| **C** | CBP-WP-012 setzt **CBP-WP-011** voraus — erst spezifizieren, dann bauen |
| **D** | CBP-WP-013 setzt **CBP-WP-010 und CBP-WP-012** voraus |
| **E** | CBP-WP-014 setzt **CBP-WP-013** voraus — nur `approved` wird indexiert |

**Der breiteste Enabler ist der F3-Strang** (CBP-WP-011 → CBP-WP-012). Er
sollte früh beginnen, weil CBP-WP-013 und CBP-WP-014 ohne ihn nicht
durchsetzbar sind.

## Was diese Karte nicht enthält

| Backlogpunkt | Grund |
| --- | --- |
| **P6** Retrieval-Pilot V1 | setzt P5 voraus |
| **P7** Benchmark V0/V1 | setzt P6 voraus |
| **P8** `excluded-from-ai`-Negativtests | setzt P3 **und** P6 voraus |
| **P9** Backup-/Restore-/Rebuild-Test | setzt P5 voraus |
| **P10** Deployment Readiness Profil A | setzt P3 und P9 voraus |
| **P11** Web-UI und Mobile | **erst nach gemessenem Retrieval** — ausdrückliche G0-Auflage |

Die Karte schneidet bewusst nur **F1 bis F5**. Sie weiterzuführen, bevor die
ersten Nachweise vorliegen, wäre Planung ohne Rückkopplung.

## Status

**Stand nach CBP-WP-010:** CBP-WP-009 ist committed, CBP-WP-010 **ausgeführt**
(`in-review`). Die vier übrigen Work Packages **CBP-WP-011 bis CBP-WP-014**
stehen weiterhin auf **`proposed`** — keines ist freigegeben, keines steht auf
`active`, keines ist begonnen.

**Regeln A und B sind erfüllt:** Die Bereichsgrenze steht (009), die
Mappingkonvention steht (010). **CBP-WP-011 ist damit nicht mehr durch eine
fehlende Vorentscheidung blockiert** — es ist deshalb **nicht freigegeben**.

**Regel C bleibt bindend:** CBP-WP-013 braucht **beide** Vorgänger. Der
F3-Strang (011 → 012) hat noch nicht begonnen; ohne ihn ist das
Aktivierungsgate nicht durchlaufbar, weil acht seiner zwanzig Punkte
Nachweisstufe 4 verlangen.

**Implementierung autorisiert: nein.**

> **Ergänzung zu einem Migrations-Work-Package.** D-029 verlangt für die
> Überführung in die Zielstruktur ein **separates, ausdrücklich freigegebenes**
> Work Package mit nachvollziehbarer, schrittweiser, rücksetzbarer Planung ohne
> Verlust der Git-Historie. Ein solches Paket ist in dieser Karte **nicht**
> geschnitten und wäre von Nova zu spezifizieren.
