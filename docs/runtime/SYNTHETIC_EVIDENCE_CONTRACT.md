# Synthetic Evidence Contract 2.0 — Vertrag und Trust Boundary (CBP-WP-017)

| Feld | Wert |
| --- | --- |
| **Status** | **lokaler Prototyp** — synthetic-only, read-only, nicht persistent, fail-closed, **nicht produktionsbereit** |
| Grundlage | ADR-0007 (RT-1/RT-2/RT-3), ADR-0009 (Evidence-Policy); **D-051** (A0); WP-016-Gate-Evaluator |
| Erfasst in | CBP-WP-017 |
| Autoritätsklasse | A2 |
| Python | 3.13+ (nur Standardbibliothek) |
| Stand | 2026-07-28 |

Dieser Vertrag beschreibt das **Evidence-Bundle 2.0** mit eingebetteten
strukturierten Artefakten. Er ist eine **reine Konkretisierung** der
Evidence-Policy (ADR-0009) und bleibt gemäß ADR-0007 **RT-1** (rebuildable,
nicht autoritativ). Synthetische Evidenz ist ein Test-Fixture **ohne** A0- oder
operative Autorität; sie erfüllt **kein** Kriterium.

---

## Autoritäts- und Sicherheitsgrenzen

- **Formvalidität ≠ Gate-Erfüllung.** Ein formal gültiges, aktuelles
  synthetisches Artefakt setzt **nie** ein Kriterium auf `SATISFIED`.
- **Ausschließlich menschliche Entscheidungen 5, 16, 20** bleiben
  `HUMAN_DECISION_REQUIRED`.
- **Menschlich erzeugte operative Evidenz:** 15 (Operator Review), 18
  (Backup-Effekt), 19 (Rollback) bleiben `MISSING_EVIDENCE` — ein synthetisches
  Artefakt modelliert nur **Form/Bindung**, nie tatsächliche operative Evidenz.
- **Keine** Security-Foundation-Evaluation, **keine** DRC-Ausführung, **keine**
  Aktivierung, **keine** Gatefreigabe, **keine** Persistenz, **kein** RT-2, kein
  Netzwerk, keine Secrets, keine reale Source.

## Schemaversionierung

`evidence_schema_version` ist **exakt `"2.0"`**. Das abgelöste **1.0** und jede
unbekannte Version werden **fail-closed** abgewiesen
(`GATE_EVIDENCE_SCHEMA_UNSUPPORTED`, Exit 14, kein Report). Es gibt **keine**
parallele 1.0-Kompatibilitätslogik und **keine** Datenmigration, weil keine
produktive oder persistierte Evidenz existiert. `evidence_contract_revision`
ist `"2.0"`; die **Gate**-Vertragsrevision bleibt unverändert `"1.0"` (die 20
Kriterien ändern sich nicht).

## Top-Level-Bundle (geschlossen, 11 Felder)

`evidence_schema_version` (= `"2.0"`), `synthetic_test_only` (= `true`),
`source_id` (`src-[0-9a-f]{24}`), `mapping_id` (WP-015-Vertrag + Leak-Schutz),
`gate_contract_revision`, `evidence_contract_revision` (nicht leer),
`evidence_revision` (int ≥ 1), `mapping_draft_sha256`, `mapping_policy_sha256`,
`registry_record_sha256` (hex64), `criterion_evidence`. **Keine** Zusatzfelder.

## criterion_evidence und Artefakte

`criterion_evidence` ist eine Liste mit **exakt 20** Einträgen in fester
Reihenfolge 1..20, je `{criterion, artifacts}`. `artifacts` ist eine Liste
(**0..4** je Kriterium, **≤ 80** gesamt; leere Liste zulässig). Jedes Artefakt
hat **exakt 6** geschlossene Felder:

| Feld | Regel |
| --- | --- |
| `artifact_id` | `\Aart-[0-9a-f]{24}\Z` — opak, reportsicher, **kein** Pfad/URL/Locator/Secret/Host/Benutzer; nur gelesen, nie erzeugt/normalisiert |
| `artifact_sha256` | hex64 der kanonischen Artefaktbeschreibung **ohne** `artifact_sha256` |
| `binding_sha256` | hex64 der kanonischen Kriteriumsbindung |
| `producer_class` | geschlossenes Enum (nur Klasse, nie Person/Host/Instanz) |
| `evidence_revision` | int ≥ 1 |
| `synthetic_test_only` | **exakt** `true` |

## Hash-Berechnung (Canonical JSON: UTF-8, keine BOM, sortierte Schlüssel, kompakt, kein NaN/Infinity)

**Artefakt-Hash** = SHA-256 über `{artifact_id, binding_sha256, producer_class,
evidence_revision, synthetic_test_only}` — `artifact_sha256` ist **nicht** Teil
seiner eigenen Berechnung.

**Binding-Hash** = SHA-256 über `{source_id, mapping_id, criterion,
mapping_draft_sha256, mapping_policy_sha256, registry_record_sha256,
gate_contract_revision, gate_contract_sha256, evidence_contract_revision,
evidence_contract_sha256, evidence_revision}` (aktueller Snapshot).

**Evidence-Contract-Hash** (`evidence_contract_sha256()`) ist deterministisch
aus dem **vollständigen statischen Vertrag** abgeleitet (Schema-Version, Top-
Level-/Criterion-/Artefaktfelder, Producer-Klassen, Kriterienzuordnung,
Mengenlimits, Evaluationspriorität, Canonical-JSON-Regeln) — **keine**
Laufzeitdaten.

## Producer-Klassen und Kriterienzuordnung

| Klasse | Kriterien |
| --- | --- |
| `structural-form` | 1, 2, 3, 12, 13, 14 |
| `foundation-form` | 4, 5, 6, 7, 8, 9, 10, 11 |
| `operator-review-form` | 15 |
| `rt2-audit-form` | 17 |
| `backup-form` | 18 |
| `rollback-form` | 19 |
| `human-decision-form` | 16, 20 |

**Begründete Ergänzung:** Die Vorgabe ließ 16/20 ohne Klasse; da eine gültige
Formvalidierung für 16/20 zu belegen ist, deckt `human-decision-form` **nur die
Form** dieser reinen Human-Entscheidungen ab — es **erfüllt sie nie** (negative
Faltung; 16/20 bleiben `HUMAN_DECISION_REQUIRED`). Kriterium 5 bleibt
`foundation-form` (nur Form, nie Erfüllung). Die Zuordnung verändert **keine**
Autoritätsgrenze.

## Evaluationspriorität (deterministisch, fail-closed)

Nach dem strukturellen Loader-Fail-Close je Kriterium: **INVALID_EVIDENCE >
CONFLICTING_EVIDENCE > STALE_EVIDENCE > bestehendes Kriterienergebnis**.

- **INVALID** — `artifact_sha256` falsch (`GATE-EVID-INVALID-HASH`) oder
  Producer-Klasse für das Kriterium unzulässig (`GATE-EVID-INVALID-PRODUCER-CLASS`).
- **CONFLICTING** — ≥ 2 eindeutige Artefakte je Kriterium
  (`GATE-EVID-CONFLICT-HASH`) oder gleiche `artifact_id` mit anderem Hash
  (`GATE-EVID-CONFLICT-ARTIFACT-ID`). Identische Artefakte werden nach
  **vollständiger kanonischer Beschreibung dedupliziert**; stabile Sortierung
  `criterion → artifact_id → artifact_sha256`; **kein** „letzter Wert gewinnt",
  **keine** Reihenfolgeabhängigkeit, **kein** Zeitbezug.
- **STALE** — wohlgeformt, aber `binding_sha256` ≠ aktueller Snapshot
  (`GATE-EVID-STALE-BINDING`) oder `evidence_revision` ≠ Bundle
  (`GATE-EVID-STALE-EVIDENCE-REVISION`). **Keine Uhr, kein Datum, kein
  Dateialter** — rein revisions-/bindungsbasiert.

`MISSING_EVIDENCE` bleibt allein durch die bestehende Kriterienlogik bestimmt;
ein fehlendes Artefakt stuft **nichts** herab und erfüllt **nichts**.

## Report (A6, minimal erweitert)

Zusätzlich: `evidence_contract_revision`, `evidence_contract_sha256`,
`validated_artifact_count`, `invalid_artifact_count`, `stale_artifact_count`,
`conflicting_artifact_count` (eindeutige, deduplizierte Zähler). **Keine**
`artifact_id`, Rohartefakte, Producer-Personen, Pfade, URLs, Locators, Secrets,
Hostnamen, Zeitstempel, Notes, Freitext oder Stacktraces. Die Felder sind reine
**A6-Diagnose** und autorisieren/aktivieren/bestätigen **nichts**; `GateStatus`
bleibt `NOT_EVALUATED`/`BLOCKED`.

## Größenlimits

`criterion_evidence` = 20 · Artefakte je Kriterium **≤ 4** · Artefakte gesamt
**≤ 80** · Dateigröße **≤ 131072 B** (Worst Case 80 Artefakte ≈ 25 KB kompakt /
≈ 50 KB eingerückt; ~2,5× Reserve, hart begrenzt). Überschreitung ⇒ fail-closed.

## RT-Einordnung

Synthetische Evidenz ist **RT-1** (rebuildable, nicht autoritativ). Sie wird
**nicht** als **RT-2 Operational Evidence** behandelt: kein Aufbewahrungs-,
Backup- oder Restore-Anspruch, keine append-only Persistenz. `rt2-audit-form`
(Kriterium 17) modelliert nur die **Form** einer RT-2-Auditbereitstellung, nicht
deren Umsetzung.
