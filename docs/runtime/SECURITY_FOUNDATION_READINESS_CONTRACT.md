# Security Foundation Readiness Contract 1.0 (CBP-WP-018)

| Feld | Wert |
| --- | --- |
| **Status** | **lokaler Prototyp** — synthetic-form-only, read-only, nicht persistent, fail-closed, **nicht produktionsbereit** |
| Grundlage | **ADR-0013** (A1); **D-052**, **D-053** (A0); ADR-0009 (12 KB-Kontrollen), ADR-0007 (RT-1/RT-2/RT-3) |
| Erfasst in | CBP-WP-018, Phase B1 |
| Autoritätsklasse | A2 |
| Modul | `core/core_brain/gate/security_contract.py` |
| Contract-Revision | **1.0** |
| Python | 3.13+ (nur Standardbibliothek) |
| Stand | 2026-07-29 |

Dieser Vertrag beschreibt, **welche `(criterion, control_id)`-Bindungen eine
synthetische Formprüfung erwartet**. Er ist ein **statischer** Deskriptor ohne
Laufzeitdaten und gemäß ADR-0007 **RT-1** (rebuildable, nicht autoritativ).

---

## Was dieser Vertrag nicht ist

Der Security Contract bestätigt **nicht**:

- technische Implementierung einer Kontrolle,
- Durchsetzung (Enforcement),
- Wirksamkeit,
- **Security Readiness**,
- einen bestandenen Negativtest,
- Human Approval,
- Aktivierungsbereitschaft.

Er führt **keine** reale Security-Evaluation aus: kein Netzwerkzugriff, keine
Port-, Prozess- oder Dateirechteprüfung, keine Ziel-VM, keine
Secret-Auflösung, kein RT-2, keine Persistenz.

**Das Security Foundation Readiness Gate bleibt `NOT EVALUATED`.** Die zwölf
Kontrollen aus ADR-0009 bleiben `DOCUMENTED ONLY`.

## Zwölf dokumentierte Kontrollen

`KB-01` bis `KB-12` (ADR-0009). Die geschlossene ID-Syntax ist

```text
\AKB-(0[1-9]|1[0-2])\Z
```

Freie Strings, Pfade, URLs, Hostnamen, Benutzernamen, Secrets und
Credential-Werte sind als `control_id` ausgeschlossen; ein abweichender Wert
wird fail-closed abgewiesen, **ohne** den Wert zu echoen.

## Sieben runtime-scoped Kontrollen

```text
KB-02  KB-03  KB-04  KB-07  KB-08  KB-10  KB-11
```

Nur diese besitzen eine Mapping-Gate-Kriteriumsidentität.

## Fünf nicht runtime-scoped Kontrollen

```text
KB-01  KB-05  KB-06  KB-09  KB-12
```

Sie sind Teil des breiteren Readiness-Gates. Ihre Einordnung als *nicht
runtime-scoped* bedeutet **nicht**, dass sie unwichtig, erfüllt,
implementiert, evaluiert oder durchgesetzt wären.

## Elf runtime-scoped Bindungen

Sortiert nach Kriterium aufsteigend, dann `control_id` lexikografisch:

| Kriterium | Control |
| --- | --- |
| 4 | KB-08 |
| 6 | KB-10 |
| 6 | KB-11 |
| 7 | KB-02 |
| 7 | KB-04 |
| 7 | KB-07 |
| 8 | KB-03 |
| 8 | KB-04 |
| 10 | KB-11 |
| 11 | KB-03 |
| 11 | KB-04 |

Die Bindungsidentität ist **`(criterion, control_id)`** — nicht das Kriterium
allein. Mehrere Kontrollen desselben Kriteriums sind dadurch getrennte
Bindungen und erzeugen **keinen** Konflikt allein aufgrund ihrer Anzahl.

### Kriterium 5

Kriterium 5 (`data-class-confirmed`) bleibt **Human-only**
(`HUMAN_DECISION_REQUIRED`) und trägt **keine** KB-Bindung. Ein
`security-control-form`-Artefakt für Kriterium 5 ist `INVALID_EVIDENCE`.

### Kriterium 9

Kriterium 9 (`allowlist-non-empty`) ist ausdrücklich
**non-security-structural**: keine KB-Bindung, kein Eingang in einen
Security-Control-Zähler, kein akzeptiertes `security-control-form`, unverändert
strukturelle Semantik.

## Contract-Hash

`security_contract_sha256()` ist der SHA-256 des vollständigen statischen
Deskriptors: Revision, dokumentierte / runtime-scoped / nicht runtime-scoped
Kontrollen, die elf Bindungen, `non_security_structural_criteria`,
`required_producer_class`, `control_id_syntax`, `synthetic_form_only`,
`binding_identity`, `negative_evidence_only` und die Canonical-JSON-Regeln.

Canonical JSON: UTF-8, keine BOM, sortierte Schlüssel, kompakte Separatoren,
keine `NaN`/`Infinity`, **keine Uhr**, keine Laufzeitdaten, keine I/O. Gleicher
Vertrag ⇒ gleicher Hash.

Das Modul ist **rein statisch** (Pure Core): kein Datei-, Netz-, ENV-, Uhr-
oder Zufallszugriff, keine Mutation. Der Import hat keine Nebenwirkungen.

## Bindung der Security-Control-Artefakte

Ein `security-control-form`-Artefakt bindet zusätzlich an `control_id`,
`security_contract_revision` und `security_contract_sha256` — siehe
[SYNTHETIC_EVIDENCE_CONTRACT.md](SYNTHETIC_EVIDENCE_CONTRACT.md).

## Per-Bindungs-Verdikte

Für jede der elf erwarteten Bindungen entsteht **genau ein** Verdikt:

| Verdikt | Bedeutung | Wirkung auf das Kriterium |
| --- | --- | --- |
| `MISSING` | kein Artefakt für die erwartete Bindung | **kein** Override |
| `VALID` | genau ein eindeutiges, aktuelles, integres Artefakt | **kein** Override — **kein** `SATISFIED` |
| `INVALID` | Integritäts-, Zuordnungs- oder Vertragsverstoß | `INVALID_EVIDENCE` |
| `STALE` | Vertrags- oder Snapshot-Drift | `STALE_EVIDENCE` |
| `CONFLICTING` | mehrere unterschiedliche aktuelle Artefakte derselben Bindung | `CONFLICTING_EVIDENCE` |

Priorität je Bindung: **`INVALID` › `CONFLICTING` › `STALE` › `VALID` ›
`MISSING`**.

### Invalid gegen Stale

- **aktueller** Security Contract **+** darin unzulässiges Paar ⇒
  `INVALID_EVIDENCE`
- **ältere** Contract-Revision **oder** älterer Contract-Hash ⇒
  `STALE_EVIDENCE`

Bei einem alten Vertrag wird ein historisch plausibles Paar **nicht**
nachträglich als aktuelle Invalid-Behauptung umklassifiziert. Ein
Artifact-Hash-Integritätsfehler bleibt aufgrund der Priorität dennoch
`INVALID_EVIDENCE`.

### Konflikte

Gruppierung ausschließlich nach `(criterion, control_id)`. Exakte Duplikate
werden dedupliziert. Es gibt **kein** „letzter Wert gewinnt", keine
Reihenfolgepriorität, keine Uhr und keine automatische Konfliktauflösung.

## Aggregation zum Gate-Kriterium

Mehrere Bindungen desselben Kriteriums werden deterministisch zum
**schwersten negativen** Verdikt zusammengefasst:

```text
irgendeine Bindung INVALID      → INVALID_EVIDENCE
sonst irgendeine CONFLICTING    → CONFLICTING_EVIDENCE
sonst irgendeine STALE          → STALE_EVIDENCE
sonst                           → bestehendes CriterionOutcome
```

`MISSING` und `VALID` erzeugen **keinen** Override.

## Negative-evidence-only

Ein vollständiges und gültiges Elf-Bindungs-Formset:

- erzeugt **kein** `SATISFIED`,
- entfernt **kein** `DEPENDENCY_BLOCKED` (Kriterien 4, 6, 7, 8, 10, 11),
- setzt **kein** Gate auf `READY FOR ACTIVATION DECISION`,
- simuliert **keine** Human Decision.

Der Gate-Ausgabestatus bleibt `NOT_EVALUATED` oder `BLOCKED`.

## Report-Felder

```text
security_contract_revision
security_contract_sha256
documented_control_count                 = 12
runtime_scoped_control_count             = 7
runtime_scoped_binding_count             = 11
valid_form_binding_count
missing_form_binding_count
invalid_form_binding_count
stale_form_binding_count
conflicting_form_binding_count
operationally_unevaluated_binding_count  = 11
```

**Summeninvariante:**

```text
valid + missing + invalid + stale + conflicting = 11
```

`operationally_unevaluated_binding_count = 11` hält fest, dass **alle** elf
Bindungen operativ **unevaluiert** sind — Formprüfung ist keine Evaluation.

Der Report enthält **keine** `control_id`, keine `artifact_id`, keine
Artefakt-/Binding-Hashes, keine Control-Inhalte, keine Zielsystemdetails,
keine Pfade, URLs, Hosts, Benutzer, Secrets, Credentials, Zeitstempel, Notes
oder Freitexte — nur Contract-Revisionen, Contract-Hashes, stabile
Reason-Codes und deterministische Zähler.

Aggregatfelder wie `ready_control_count`, `passed_control_count`,
`enforced_control_count`, `approved_control_count`, `security_ready` oder
`security_passed` existieren **nicht** und werden nicht eingeführt.

## Reason-Codes

```text
GATE-EVID-INVALID-CONTROL-BINDING
GATE-EVID-STALE-SECURITY-CONTRACT
```

Ergänzend gelten die bestehenden WP-017-Codes (`GATE-EVID-INVALID-HASH`,
`GATE-EVID-INVALID-PRODUCER-CLASS`, `GATE-EVID-CONFLICT-ARTIFACT-ID`,
`GATE-EVID-CONFLICT-HASH`, `GATE-EVID-STALE-BINDING`,
`GATE-EVID-STALE-EVIDENCE-REVISION`). Codes sind stabil, enthalten **keine**
Rohwerte und **keine** Control-ID im Text und werden deterministisch sortiert.

## Verwandte Dokumente

- [SYNTHETIC_EVIDENCE_CONTRACT.md](SYNTHETIC_EVIDENCE_CONTRACT.md) — Evidence
  Schema 3.0, Artefakt- und Binding-Verträge
- [MAPPING_ACTIVATION_GATE_EVALUATOR.md](MAPPING_ACTIVATION_GATE_EVALUATOR.md)
  — die 20 Gate-Kriterien
- [MAPPING_ACTIVATION_GATE_RUNBOOK.md](MAPPING_ACTIVATION_GATE_RUNBOOK.md) —
  Bedienung und Exitcodes
- `docs/decisions/ADR-0013` — Evidence Schema 3.0 (A1)
- `docs/decisions/ADR-0009` — technische Sicherheitsgrundlage (A1)
