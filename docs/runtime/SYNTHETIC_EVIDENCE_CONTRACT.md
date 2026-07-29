# Synthetic Evidence Contract 3.0 — Vertrag und Trust Boundary (CBP-WP-018)

| Feld | Wert |
| --- | --- |
| **Status** | **lokaler Prototyp** — synthetic-only, read-only, nicht persistent, fail-closed, **nicht produktionsbereit** |
| Grundlage | **ADR-0013** (A1); **D-052**, **D-053** (A0); ADR-0007 (RT-1/RT-2/RT-3), ADR-0009 (Evidence-Policy, 12 KB-Kontrollen); WP-016-Gate-Evaluator |
| Erfasst in | CBP-WP-018 (Schema 3.0); zuvor CBP-WP-017 (Schema 2.0, abgelöst) |
| Autoritätsklasse | A2 |
| Python | 3.13+ (nur Standardbibliothek) |
| Stand | 2026-07-29 |

Dieser Vertrag beschreibt das **Evidence-Bundle 3.0** mit eingebetteten
strukturierten Artefakten und **Security-Control-Identität**. Er ist eine
**reine Konkretisierung** der Evidence-Policy (ADR-0009) und bleibt gemäß
ADR-0007 **RT-1** (rebuildable, nicht autoritativ). Synthetische Evidenz ist ein
Test-Fixture **ohne** A0- oder operative Autorität; sie erfüllt **kein**
Kriterium.

---

## Autoritäts- und Sicherheitsgrenzen

- **Formvalidität ≠ Gate-Erfüllung.** Ein formal gültiges, aktuelles
  synthetisches Artefakt setzt **nie** ein Kriterium auf `SATISFIED`.
- **Ausschließlich menschliche Entscheidungen 5, 16, 20** bleiben
  `HUMAN_DECISION_REQUIRED`.
- **Menschlich erzeugte operative Evidenz:** 15 (Operator Review), 18
  (Backup-Effekt), 19 (Rollback) bleiben `MISSING_EVIDENCE` — ein synthetisches
  Artefakt modelliert nur **Form/Bindung**, nie tatsächliche operative Evidenz.
- **Ein `security-control-form`-Artefakt belegt nur die Form einer
  KB-Control-Bindung** — **keine** Implementierung, Durchsetzung, Wirksamkeit,
  Security Readiness, keinen bestandenen Negativtest, keine Human Approval und
  keine Aktivierungsbereitschaft (siehe
  [SECURITY_FOUNDATION_READINESS_CONTRACT.md](SECURITY_FOUNDATION_READINESS_CONTRACT.md)).
- **Keine** Security-Foundation-Evaluation, **keine** DRC-Ausführung, **keine**
  Aktivierung, **keine** Gatefreigabe, **keine** Persistenz, **kein** RT-2, kein
  Netzwerk, keine Secrets, keine reale Source.

## Schemaversionierung

`evidence_schema_version` ist **exakt `"3.0"`**. Die abgelösten **1.0**
(WP-016) und **2.0** (WP-017) sowie jede unbekannte Version werden
**fail-closed** abgewiesen (`GATE_EVIDENCE_SCHEMA_UNSUPPORTED`, Exit 14, kein
Report). Es gibt **keine** Kompatibilitätsschicht und **keine**
Laufzeit-Datenmigration, weil keine produktive oder persistierte Evidenz
existiert — nur Test-Fixtures. `evidence_contract_revision` ist `"3.0"`; die
**Gate**-Vertragsrevision **und** der Gate-Contract-Hash bleiben unverändert
(die 20 Kriterien ändern sich nicht).

## Top-Level-Bundle (geschlossen, 13 Felder)

`evidence_schema_version` (= `"3.0"`), `synthetic_test_only` (= `true`),
`source_id` (`src-[0-9a-f]{24}`), `mapping_id` (WP-015-Vertrag + Leak-Schutz),
`gate_contract_revision`, `evidence_contract_revision` (nicht leer),
**`security_contract_revision`** (nicht leer),
**`security_contract_sha256`** (hex64), `evidence_revision` (int ≥ 1),
`mapping_draft_sha256`, `mapping_policy_sha256`, `registry_record_sha256`
(hex64), `criterion_evidence`. **Keine** Zusatzfelder.

Strukturell wohlgeformte, aber **veraltete** Security-Contract-Werte sind
**kein** Loader-Schemafehler: sie laden und werden für vorhandene
Security-Control-Artefakte als `STALE_EVIDENCE` ausgewertet.

## criterion_evidence und Artefakte

`criterion_evidence` ist eine Liste mit **exakt 20** Einträgen in fester
Reihenfolge 1..20, je `{criterion, artifacts}`. `artifacts` ist eine Liste
(**0..4** je Kriterium, **≤ 80** gesamt; leere Liste zulässig).

Das Artefaktschema ist **bedingt geschlossen**: Nicht-Security-Artefakte haben
**exakt 6** Felder, `security-control-form`-Artefakte **exakt 7**.

| Feld | Regel |
| --- | --- |
| `artifact_id` | `\Aart-[0-9a-f]{24}\Z` — opak, reportsicher, **kein** Pfad/URL/Locator/Secret/Host/Benutzer; nur gelesen, nie erzeugt/normalisiert. Wird **nie** als `control_id` interpretiert |
| `artifact_sha256` | hex64 der kanonischen Artefaktbeschreibung **ohne** `artifact_sha256` |
| `binding_sha256` | hex64 der kanonischen Bindung |
| `producer_class` | geschlossenes Enum (nur Klasse, nie Person/Host/Instanz) |
| `control_id` | **nur** bei `security-control-form`: geschlossenes Enum `KB-01`..`KB-12`, Syntax `\AKB-(0[1-9]\|1[0-2])\Z`. Bei **jeder anderen** Klasse **verboten** |
| `evidence_revision` | int ≥ 1 |
| `synthetic_test_only` | **exakt** `true` |

Fehlendes `control_id` bei `security-control-form`, vorhandenes `control_id` bei
einer anderen Klasse und jede unbekannte Control-ID werden fail-closed
abgewiesen — **ohne** Echo des abgewiesenen Werts.

## Hash-Berechnung (Canonical JSON: UTF-8, keine BOM, sortierte Schlüssel, kompakt, kein NaN/Infinity)

**Artefakt-Hash** = SHA-256 über `{artifact_id, binding_sha256, producer_class,
evidence_revision, synthetic_test_only}`, bei `security-control-form`
zusätzlich `control_id`. `artifact_sha256` ist **nicht** Teil seiner eigenen
Berechnung.

**Binding-Hash (nicht-Security)** = SHA-256 über `{source_id, mapping_id,
criterion, mapping_draft_sha256, mapping_policy_sha256, registry_record_sha256,
gate_contract_revision, gate_contract_sha256, evidence_contract_revision,
evidence_contract_sha256, evidence_revision}` (aktueller Snapshot).

**Binding-Hash (Security-Control)** = zusätzlich `control_id`,
`security_contract_revision` und `security_contract_sha256` — insgesamt 14
Komponenten. Jede Drift einer einzelnen Komponente ändert den Hash.

**Evidence-Contract-Hash** (`evidence_contract_sha256()`) ist deterministisch
aus dem **vollständigen statischen Vertrag** abgeleitet (Schema-Version, Top-
Level-Felder inkl. Security-Contract-Feldern, **bedingte** Artefakt- und
Binding-Feldmengen, `control_id`-Regeln, Producer-Klassen, Kriterienzuordnung,
Mengenlimits, Evaluationspriorität, Canonical-JSON-Regeln) — **keine**
Laufzeitdaten. Er **unterscheidet sich** vom 2.0-Hash.

## Producer-Klassen und Kriterienzuordnung

| Klasse | Kriterien |
| --- | --- |
| `structural-form` | 1, 2, 3, 12, 13, 14 |
| `security-control-form` | 4, 6, 7, 8, 10, 11 |
| `foundation-form` | 5, 9 |
| `operator-review-form` | 15 |
| `rt2-audit-form` | 17 |
| `backup-form` | 18 |
| `rollback-form` | 19 |
| `human-decision-form` | 16, 20 |

**Begründete Ergänzung:** Die Vorgabe ließ 16/20 ohne Klasse; da eine gültige
Formvalidierung für 16/20 zu belegen ist, deckt `human-decision-form` **nur die
Form** dieser reinen Human-Entscheidungen ab — es **erfüllt sie nie** (negative
Faltung; 16/20 bleiben `HUMAN_DECISION_REQUIRED`). **Kriterium 5** bleibt
`foundation-form` und **Human-only**; **Kriterium 9** bleibt `foundation-form`
und **non-security-structural** — beide akzeptieren **kein**
`security-control-form`. Die Zuordnung verändert **keine** Autoritätsgrenze.

## Security-Control-Bindungen

Die Bindungsidentität eines Security-Control-Artefakts ist
**`(criterion, control_id)`**, nicht das Kriterium allein. Der statische
Security Contract (Revision **1.0**) definiert **12** dokumentierte Kontrollen,
**7** runtime-scoped Kontrollen und **11** kanonische
`(criterion, control_id)`-Bindungen. Mehrere Kontrollen desselben Kriteriums
(z. B. 7 → KB-02/KB-04/KB-07) sind getrennte Bindungen und erzeugen **keinen**
Konflikt allein aufgrund ihrer Anzahl. Vollständige Beschreibung:
[SECURITY_FOUNDATION_READINESS_CONTRACT.md](SECURITY_FOUNDATION_READINESS_CONTRACT.md).

## Evaluationspriorität (deterministisch, fail-closed)

Nach dem strukturellen Loader-Fail-Close je Kriterium: **INVALID_EVIDENCE >
CONFLICTING_EVIDENCE > STALE_EVIDENCE > bestehendes Kriterienergebnis**.

- **INVALID** — `artifact_sha256` falsch (`GATE-EVID-INVALID-HASH`);
  Producer-Klasse für das Kriterium unzulässig
  (`GATE-EVID-INVALID-PRODUCER-CLASS`, u. a. `security-control-form` auf
  Kriterium 5 oder 9); oder **aktueller** Security Contract **+** darin
  unzulässiges `(criterion, control_id)`-Paar
  (`GATE-EVID-INVALID-CONTROL-BINDING`).
- **CONFLICTING** — ≥ 2 eindeutige Artefakte derselben Bindung
  (`GATE-EVID-CONFLICT-HASH`) oder gleiche `artifact_id` mit anderem Hash
  (`GATE-EVID-CONFLICT-ARTIFACT-ID`). Identische Artefakte werden nach
  **vollständiger kanonischer Beschreibung dedupliziert**; stabile Sortierung
  `artifact_id → artifact_sha256`; **kein** „letzter Wert gewinnt",
  **keine** Reihenfolgeabhängigkeit, **kein** Zeitbezug.
- **STALE** — wohlgeformt, aber `binding_sha256` ≠ aktueller Snapshot
  (`GATE-EVID-STALE-BINDING`), `evidence_revision` ≠ Bundle
  (`GATE-EVID-STALE-EVIDENCE-REVISION`) oder Security-Contract-Revision/-Hash
  veraltet (`GATE-EVID-STALE-SECURITY-CONTRACT`). **Keine Uhr, kein Datum, kein
  Dateialter** — rein revisions-/bindungsbasiert.

**Invalid gegen Stale:** Bei einem **alten** Security Contract wird ein
historisch plausibles Paar **nicht** nachträglich als aktuelle
Invalid-Behauptung umklassifiziert (⇒ `STALE_EVIDENCE`). Ein
Artifact-Hash-Integritätsfehler bleibt aufgrund der Priorität dennoch
`INVALID_EVIDENCE`.

**Gruppierung:** Security-Control-Artefakte werden nach
`(criterion, control_id)` gruppiert, alle übrigen je Kriterium. Mehrere
Bindungen desselben Kriteriums werden zum **schwersten negativen** Verdikt
aggregiert (`INVALID` › `CONFLICTING` › `STALE` › bestehendes Ergebnis).

`MISSING_EVIDENCE` bleibt allein durch die bestehende Kriterienlogik bestimmt;
ein fehlendes Artefakt stuft **nichts** herab und erfüllt **nichts**.

## Report (A6, minimal erweitert)

Aus WP-017: `evidence_contract_revision`, `evidence_contract_sha256`,
`validated_artifact_count`, `invalid_artifact_count`, `stale_artifact_count`,
`conflicting_artifact_count` (eindeutige, deduplizierte Zähler).

Neu in WP-018: `security_contract_revision`, `security_contract_sha256`,
`documented_control_count` (= 12), `runtime_scoped_control_count` (= 7),
`runtime_scoped_binding_count` (= 11), `valid_form_binding_count`,
`missing_form_binding_count`, `invalid_form_binding_count`,
`stale_form_binding_count`, `conflicting_form_binding_count`,
`operationally_unevaluated_binding_count` (= 11). Es gilt die
**Summeninvariante** `valid + missing + invalid + stale + conflicting = 11`.

**Keine** `control_id`, `artifact_id`, Rohartefakte, Artefakt-/Binding-Hashes,
Control-Inhalte, Zielsystemdetails, Producer-Personen, Pfade, URLs, Locators,
Secrets, Hostnamen, Zeitstempel, Notes, Freitext oder Stacktraces. Aggregate
wie `ready_control_count`, `passed_control_count`, `enforced_control_count`,
`approved_control_count`, `security_ready` oder `security_passed` existieren
**nicht**. Die Felder sind reine **A6-Diagnose** und
autorisieren/aktivieren/bestätigen **nichts**; `GateStatus` bleibt
`NOT_EVALUATED`/`BLOCKED`.

## Größenlimits

`criterion_evidence` = 20 · Artefakte je Kriterium **≤ 4** · Artefakte gesamt
**≤ 80** · Dateigröße **≤ 131072 B**. Der Worst Case aus **80
Security-Control-Artefakten** (das größte Artefakt, da mit `control_id`) bleibt
auch eingerückt serialisiert unter dem Limit und ist testabgedeckt.
Überschreitung ⇒ fail-closed.

## RT-Einordnung

Synthetische Evidenz ist **RT-1** (rebuildable, nicht autoritativ). Sie wird
**nicht** als **RT-2 Operational Evidence** behandelt: kein Aufbewahrungs-,
Backup- oder Restore-Anspruch, keine append-only Persistenz. `rt2-audit-form`
(Kriterium 17) modelliert nur die **Form** einer RT-2-Auditbereitstellung, nicht
deren Umsetzung.
