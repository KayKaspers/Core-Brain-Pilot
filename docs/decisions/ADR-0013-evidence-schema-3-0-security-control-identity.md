# ADR-0013 — Evidence Schema 3.0: Security-Control Identity and Contract Binding

| Feld | Wert |
| --- | --- |
| **Status** | **accepted** |
| Autorität nach Annahme | **A1** |
| Grundlage der Entscheidungen | **A0** — Human Maintainer (CBP-WP-018) |
| Erfasst in | CBP-WP-018 (Phase B0 — Governance Foundation) |
| Datum | 2026-07-28 |
| Verhältnis | baut auf **ADR-0007** (RT-1/RT-2/RT-3) und **ADR-0009** (Sicherheitsgrundlage) auf; präzisiert das in **D-051** festgelegte Evidence-Modell (WP-017) und **löst dessen Teilentscheidungen C2 (Evidence Schema 2.0) und D1 (ADR_NOT_REQUIRED) partiell ab** |
| Entscheidungen | **D-052** (A0) |
| Supersedes | — (D-051 bleibt historisch gültig; nur C2/D1 partiell abgelöst) |
| Superseded by | — |

Dieses ADR legt eine **projektweite** Änderung des Evidence-Artefaktmodells fest:
die Einführung einer expliziten **Security-Control-Identität** (`control_id`) und
einer **Security-Contract-Bindung** im Evidence-Artefakt, umgesetzt als neues
geschlossenes **Evidence Schema 3.0**. Es ist ein **Governance-Schritt**: Er
autorisiert **keine** technische Implementation, **keine** Migration und
**keinen** Runtime-Code. Der tatsächlich implementierte Code-Stand bleibt
**Evidence Schema 2.0**.

---

## Human Authorization

**Decision:** APPROVE CBP-WP-018 GOVERNANCE FOUNDATION WITH NOTES · **Authority:**
A0 — Human Maintainer (D-052). Autorisiert ist ausschließlich dieser
dokumentarische Governance-Schritt (ADR-0013, D-052, WP-018-Registrierung,
Statusspiegel). **Nicht autorisiert:** technische Implementation von Schema 3.0,
`control_id`/`security-control-form`/Security-Contract im Code, Fixture- oder
Runtime-Doku-Migration, Security-Evaluation/-Enforcement, Gatefreigabe,
Aktivierung, reale Source, Ziel-VM, Netzwerk, Secrets, RT-2, Persistenz, DRC.

## Kontext

Evidence Schema 2.0 (WP-017, D-051) besitzt **keine** explizite
Security-Control-Identität. Das geschlossene Artefaktmodell enthält exakt:

```text
artifact_id
artifact_sha256
binding_sha256
producer_class
evidence_revision
synthetic_test_only
```

Es enthält **kein** `control_id`. Damit sind **mehrere Controls innerhalb
desselben Gate-Kriteriums nicht eindeutig darstellbar**. Beispiel Kriterium 7
hängt von **KB-02, KB-04 und KB-07** ab. Die bestehende Konfliktgruppierung
erfolgt **je Kriterium** (`evaluate_criterion_artifacts`: mehr als ein
distinktes, nicht-invalides Artefakt je Kriterium ⇒ `CONFLICTING_EVIDENCE`).
Dadurch würden drei **verschiedene** Controls für Kriterium 7 fälschlich als
**Konflikt** interpretiert.

Der vorhandene Binding-Vertrag (`canonical_binding_sha256`) umfasst elf Eingaben
(`source_id`, `mapping_id`, `criterion`, `mapping_draft_sha256`,
`mapping_policy_sha256`, `registry_record_sha256`, `gate_contract_revision`,
`gate_contract_sha256`, `evidence_contract_revision`, `evidence_contract_sha256`,
`evidence_revision`) und enthält **kein** `control_id`, **kein**
`security_contract_revision` und **kein** `security_contract_sha256`.
**Security-Contract-Drift ist unter Schema 2.0 nicht nachweisbar.**

Die WP-018-Phase-A-Annahme „Evidence 2.0 unverändert, keine neuen Felder" war
**widersprüchlich**: Eine belastbare Control-Identität und Security-Contract-
Bindung **erzwingt** eine Änderung des Evidence-Artefaktmodells und damit eine
neue Schema-Version. Das ist eine **projektweite** Änderung des in D-051
festgelegten Evidence Contracts und damit ADR-pflichtig.

## Entscheidung

**Ein neues geschlossenes Evidence Schema 3.0 wird eingeführt.**

**1. Schema und Producer-Klasse.** `evidence_schema_version = "3.0"`;
`evidence_contract_revision = "3.0"`. Neue Producer-Klasse
**`security-control-form`**. Für `security-control-form` ist `control_id`
**zwingend erforderlich**; für **alle anderen** Producer-Klassen ist `control_id`
**zwingend verboten** (geschlossen-konditionales Schema).

**2. Runtime-Identität.** Die Runtime-Identität eines Security-Control-
Formartefakts ist das Paar **`(criterion, control_id)`**. Ein Artefakt
repräsentiert **genau ein** Control **und genau ein** Gate-Kriterium; es darf
**nicht** mehrere Controls oder Kriterien abdecken.

**3. Contract-Binding.** Für `security-control-form` wird der kanonische
Binding-Vertrag um `control_id`, `security_contract_revision` und
`security_contract_sha256` erweitert. Der vollständige Binding-Vertrag umfasst
damit mindestens:

```text
source_id
mapping_id
criterion
control_id
mapping_draft_sha256
mapping_policy_sha256
registry_record_sha256
gate_contract_revision
gate_contract_sha256
evidence_contract_revision
evidence_contract_sha256
security_contract_revision
security_contract_sha256
evidence_revision
```

Für andere Producer-Klassen bleibt die nicht security-gebundene Binding-Semantik
erhalten, soweit dies im geschlossenen Schema-3.0-Vertrag ausdrücklich definiert
ist.

**4. Security Contract.** Ein **separater statischer** Security Contract wird
vorgesehen (`security_contract_revision`, `security_contract_sha256`). Er enthält
ausschließlich statische Vertragsdaten: **zwölf dokumentierte KB-Controls**,
**sieben runtime-scoped KB-Controls**, **elf runtime-scoped
`(criterion, control_id)`-Bindungen** und die Control-to-Criterion-Matrix.
**Keine** Zielsystem- oder Runtime-Daten.

**5. Scope (S3, zweistufig).**

```text
documented_control_count:     12
runtime_scoped_control_count:  7
runtime_scoped_binding_count: 11
```

Runtime-scoped Controls: **KB-02, KB-03, KB-04, KB-07, KB-08, KB-10, KB-11**.
Runtime-scoped Bindungen:

```text
(KB-08, 4)
(KB-10, 6)  (KB-11, 6)
(KB-02, 7)  (KB-04, 7)  (KB-07, 7)
(KB-03, 8)  (KB-04, 8)
(KB-11, 10)
(KB-03, 11) (KB-04, 11)
```

Nicht runtime-scoped: **KB-01, KB-05, KB-06, KB-09, KB-12**. Diese fünf Controls
sind **nicht** unwichtig, erfüllt oder implementiert — sie besitzen nur keine
eindeutige Mapping-Gate-Kriteriumsidentität und gehören zum breiteren
24-Punkte-Security-Foundation-Readiness-Gate.

**6. Kriterium 5.** Bleibt **`HUMAN_DECISION_REQUIRED`**; **nicht** Teil der
runtime-scoped Security-Control-Bindungen. **Kein** Artefakt ersetzt die Human
Decision.

**7. Kriterium 9.** Bleibt **`non-security-structural`**: gehört zu **keiner**
KB-Control-Bindung, fließt **nicht** in Security-Control- oder Binding-Zähler ein,
behält seine bestehende strukturelle Bewertung und wird durch WP-018 **nicht**
neu interpretiert. Die vorhandene Producer-Zuordnung aus Schema 2.0 wird erst in
der späteren technischen Implementation konsistent migriert; dieser
Governance-Schritt verändert **keinen** Runtime-Code.

**8. Ergebnissemantik (negative-evidence-only).** Security-Control-Formartefakte
werden **ausschließlich negativ** integriert
(`INVALID_EVIDENCE`/`CONFLICTING_EVIDENCE`/`STALE_EVIDENCE`). Ein gültiges
Formartefakt erzeugt **kein** `SATISFIED`, entfernt **kein**
`DEPENDENCY_BLOCKED`, bestätigt **keine** technische Durchsetzung, bestätigt
**keine** Security Readiness, ersetzt **keine** Human Decision und autorisiert
**keine** Aktivierung.

**9. Invalid/Stale-Abgrenzung.** `STALE_EVIDENCE`: Artefakt bindet sich an eine
**ältere** Security-Contract-Revision oder einen älteren Security-Contract-Hash.
`INVALID_EVIDENCE`: Artefakt behauptet den **aktuellen** Security Contract,
verwendet aber ein darin **nicht zulässiges** `(control_id, criterion)`-Paar
(oder verletzt Integrität/Producer-Klasse/Form).

**10. Conflict.** Konfliktgruppierung nach **`(criterion, control_id)`**.
Mehrere **verschiedene** Controls innerhalb desselben Kriteriums sind **kein**
Konflikt. Mehrere nicht identische aktuelle Artefakte für **dasselbe Paar** sind
ein Konflikt. **Keine** automatische Auflösung, **kein** „letzter Wert gewinnt",
kein Zeitbezug.

**11. Versionierung.** Evidence Schema **1.0 fail-closed**, Evidence Schema
**2.0 fail-closed**, Evidence Schema **3.0** die einzige akzeptierte Version
**nach** der technischen Migration. Es existieren **keine** produktiven oder
persistenten Evidence-2.0-Daten; nur synthetische Fixtures und Dokumentation
werden später migriert.

**12. Contract-Auswirkungen.**

```text
evidence_contract_revision:  2.0 → 3.0
evidence_contract_sha256:    ändert sich
security_contract_revision:  neu
security_contract_sha256:    neu
gate_contract_revision:      unverändert
gate_contract_sha256:        unverändert
```

**13. Report-Zähler (spätere Implementation).** Der A6-Report unterscheidet:
`documented_control_count`, `runtime_scoped_control_count`,
`runtime_scoped_binding_count`, `valid_form_binding_count`,
`missing_form_binding_count`, `invalid_form_binding_count`,
`stale_form_binding_count`, `conflicting_form_binding_count`,
`operationally_unevaluated_binding_count`. Summeninvariante:

```text
valid + missing + invalid + stale + conflicting
= runtime_scoped_binding_count = 11
```

**Keine** Zähler mit `ready`/`passed`/`enforced`/`approved`. **Keine**
`human_decision_control_count`.

## Alternativen

- **Allgemeines Subject-Binding (`subject_type`/`subject_id`):** wiederverwendbar
  für spätere Contracts, aber **unnötige Generalisierung** (nur KB-Controls sind
  aktuell nötig), höhere Schema-/Enum-Komplexität. Verworfen zugunsten des
  expliziten, engeren `control_id`.
- **Separater eingebetteter `security_control_evidence`-Bereich:** stärkste
  Trennung, aber **doppeltes Artefaktmodell** (verdoppelte Wartungs- und
  Leak-Fläche). Verworfen.
- **Evidence Schema 2.0 unverändert:** kann Control-Identität und
  Security-Contract-Drift **nicht** abbilden. Verworfen (Kernursache der
  Blocker).
- **Minor-Version `2.1`:** suggeriert fälschlich Rückwärtskompatibilität eines
  geschlossenen Schemas; das Projekt nutzt ganzzahlige Major-Versionen (1.0 →
  2.0). Verworfen zugunsten **3.0**.

## Konsequenzen

- **Leichter:** eindeutige Control-Identität; Mehrfachcontrols je Kriterium
  darstellbar; deterministisch berechenbare Per-Bindungs-Zähler mit
  Summeninvariante; Security-Contract-Drift als `STALE_EVIDENCE` erkennbar.
- **Schwerer:** Breaking Schema-Bump 2.0 → 3.0 mit Fixture- und
  Runtime-Doku-Migration (spätere Implementation); geschlossen-konditionale
  Feldmenge je Producer-Klasse; `evidence_contract_sha256` ändert sich.
- **Türen schließen sich:** Evidence 2.0/1.0 werden nach Migration fail-closed
  abgewiesen; keine implizite Rückwärtskompatibilität.
- **Unverändert:** Gate Contract (20 Kriterien, `gate_contract_sha256`);
  negative-evidence-only; GateStatus-Umfang (`NOT_EVALUATED`/`BLOCKED`);
  Human-only-Grenze (5/16/20); RT-1-Charakter der synthetischen Evidenz.

## Autoritätsgrenzen

Dieses ADR autorisiert **keine** technische Implementation. Es autorisiert
**nicht**: reale Source, Ziel-VM, Netzwerk, Secrets, Credentials, RT-2,
Persistenz, Enforcement, Security Readiness, Gate-Pass, Human Approval oder
Aktivierung. Eine synthetisch gültige Form ist **keine** Sicherheitswirkung.

## Bezug

- **ADR-0007** (RT-1/RT-2/RT-3): synthetische Evidenz bleibt **RT-1**.
- **ADR-0009** (Technische Sicherheitsgrundlage): KB-01…KB-12, 24-Punkte-
  Readiness-Gate — Grundlage der Control-to-Criterion-Matrix.
- **D-051** (WP-017): A2/B1/E2 bleiben gültig; **C2 (Schema 2.0)** und **D1
  (ADR_NOT_REQUIRED)** partiell abgelöst.
- **D-052** (WP-018): konsolidierte A0-Freigabe dieses Governance-Schritts.
- **CBP-WP-016/017/018**; Mapping-Gate-Kriterien **4, 6, 7, 8, 10, 11**
  (`DEPENDENCY_BLOCKED`), **5** (Human-only), **9** (strukturell).
