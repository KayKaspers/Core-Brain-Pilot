# CBP-WP-018 – Security Foundation Readiness Contract & Synthetic Form-Validator

| Feld | Wert |
| --- | --- |
| **ID** | CBP-WP-018 |
| **Titel** | Security Foundation Readiness Contract & Synthetic Form-Validator |
| **Typ** | implementation (Governance-Phase vorangestellt) |
| **NDF Prompt Mode** | Full |
| **Context Budget** | B2 – Standard |
| **Modell / Effort** | Claude Opus 4.8 (`claude-opus-4-8`) / ultracode |
| **Status** | **in-review** |
| **Aktuelle Phase** | **Phase B1 – Technical Implementation** |
| **Technische Implementation** | **implemented, pending Nova review and Human commit** |
| **Grundlage** | D-052, **D-053** (A0); **ADR-0013** (A1); ADR-0007, ADR-0009; D-051 (partiell abgelöst) |
| **Stand** | 2026-07-29 |

---

## Phasenstand

- **Phase A — Architektur-/Governance-Review:** abgeschlossen; von Nova mit
  `REWORK PHASE A` bewertet (Control-Identität und Security-Contract-Binding
  waren unter Evidence 2.0 nicht lösbar).
- **Phase A.1 — Control Identity and Security-Contract Binding Reconciliation:**
  abgeschlossen und von Nova angenommen; bestätigte Blocker A/B; empfahl
  Evidence Schema **3.0** mit explizitem `control_id`, Security-Contract-Bindung,
  Scope S3 und `ADR_REQUIRED`.
- **Phase B0 — Governance Foundation:** abgeschlossen und committed
  (`4dec921`); **ADR-0013 angenommen**, **D-052 dokumentiert**, WP-018 als
  `in-review` registriert. **Rein dokumentarisch.**
- **Phase B0.1 — R-33-Konsistenzkorrektur:** abgeschlossen (ADR-Indexzahl
  11 → 13 als 14. Konsistenzvorgang; R-33 = **14/18**).
- **Phase B1 — Technical Implementation (dieser Schritt):** **D-053
  dokumentiert**; Evidence Schema **2.0 → 3.0** vollständig migriert,
  `security-control-form` + `control_id` eingeführt, statischer Security
  Contract implementiert, elf `(criterion, control_id)`-Bindungen synthetisch
  formgeprüft, rein negative Faltung, A6-Report um Contract- und
  Binding-Zähler erweitert. **Uncommitted — Commit-Autorität beim Human
  Maintainer.**

## Governance-Entscheidung (D-052 / ADR-0013)

**D-052 (A0):** APPROVE CBP-WP-018 GOVERNANCE FOUNDATION WITH NOTES — A1 neue
Producer-Klasse `security-control-form` mit Pflichtfeld `control_id`,
Runtime-Identität `(criterion, control_id)`; B1 Evidence Schema **3.0** (1.0 und
2.0 fail-closed); C1 Security Contract vollständig im Artefakt-Binding
(`control_id`, `security_contract_revision`, `security_contract_sha256`); D1
Scope **S3** (12 dokumentierte / 7 runtime-scoped Controls / 11 Bindungen); E1
**ADR-0013 `accepted`**.

**ADR-0013 (A1):** Evidence Schema 3.0 — Security-Control Identity and Contract
Binding. Siehe [ADR-0013](../docs/decisions/ADR-0013-evidence-schema-3-0-security-control-identity.md).

**Partielle Ablösung von D-051:** weiterhin gültig A2 (eingebettete Artefakte),
B1 (negative-evidence-only), E2 (minimal erweiterter Report); **abgelöst** C2
(Evidence Schema 2.0) und D1 (ADR_NOT_REQUIRED). D-051 bleibt historisch gültig
und wird **nicht** umgeschrieben.

## Governance-Entscheidung Phase B1 (D-053)

**D-053 (A0):** APPROVE CBP-WP-018 TECHNICAL IMPLEMENTATION WITH NOTES — A1
ADR-0013 technisch umgesetzt; B1 einzige akzeptierte Schema-Version **3.0**
(1.0 und 2.0 fail-closed), Gate-Vertrag unverändert; C1 separater statischer
Security Contract (12 / 7 / 11); D1 **negative-evidence-only**; E1 Report mit
Contract-Revision, Contract-Hash und eindeutigen Binding-Zählern, **ohne**
öffentliche Readiness-Aggregation.

## Technischer Stand (Phase B1, uncommitted)

- **Implementierter Runtime-Code-Stand: Evidence Schema 3.0.** Schema 1.0
  (WP-016) und 2.0 (WP-017) werden fail-closed abgewiesen. Es existiert **keine**
  produktive oder persistierte Evidenz — nur Test-Fixtures.
- Neues Modul `core/core_brain/gate/security_contract.py` (Revision **1.0**):
  rein statisch, ohne I/O, Uhr, Zufall oder Netz; 12 dokumentierte Controls, 7
  runtime-scoped Controls, 11 `(criterion, control_id)`-Bindungen.
- Producer-Klasse `security-control-form` (Kriterien 4/6/7/8/10/11) mit
  Pflichtfeld `control_id`; **jede andere** Klasse verbietet `control_id`.
- Bindungsidentität `(criterion, control_id)`; mehrere Controls desselben
  Kriteriums sind getrennte Bindungen und erzeugen **keinen** Konflikt.
- Rein negative Faltung mit Priorität `INVALID > CONFLICTING > STALE >
  Basisergebnis`; A6-Report um Contract-Revision/-Hash und fünf Binding-Zähler
  (Summeninvariante = 11) erweitert.
- **Testbasis: 558 Tests – OK** (Basislinie 451), `compileall` Exit 0.
- **Kein Commit, kein Push.** Nachweise in
  [MAPPING_ACTIVATION_GATE_EVIDENCE.md](../docs/runtime/MAPPING_ACTIVATION_GATE_EVIDENCE.md).

## Autoritätsgrenzen

Die technische Implementation autorisiert **nicht**: reale Source, Ziel-VM,
Netzwerk, Secrets, Credentials, RT-2, Persistenz, reale Security-Evaluation,
Enforcement, Security Readiness, Gate-Pass, Human Approval, Aktivierung, DRC.
Kriterium 5 bleibt Human-only; Kriterium 9 bleibt non-security-structural;
Gate-Kriterien 4/6/7/8/10/11 bleiben `DEPENDENCY_BLOCKED` — auch bei elf
gültigen Formbindungen. `GateStatus` bleibt `NOT_EVALUATED`/`BLOCKED`; alle drei
Gates bleiben `NOT EVALUATED`; **0 von 29** Capabilities `implemented`.

## Rückmeldung an Nova

Phase B1 technisch abgeschlossen, **in-review**. Kein Commit, kein Push
(Commit-Autorität beim Human Maintainer). Kein nächstes Work Package
vorgeschlagen (CBP-WP-019 ausdrücklich **nicht** begonnen und **nicht**
autorisiert).
