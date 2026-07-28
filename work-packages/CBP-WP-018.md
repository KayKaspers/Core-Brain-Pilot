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
| **Aktuelle Phase** | **Phase B0 – Governance Foundation** |
| **Grundlage** | D-052 (A0); **ADR-0013** (A1); ADR-0007, ADR-0009; D-051 (partiell abgelöst) |
| **Stand** | 2026-07-28 |

---

## Phasenstand

- **Phase A — Architektur-/Governance-Review:** abgeschlossen; von Nova mit
  `REWORK PHASE A` bewertet (Control-Identität und Security-Contract-Binding
  waren unter Evidence 2.0 nicht lösbar).
- **Phase A.1 — Control Identity and Security-Contract Binding Reconciliation:**
  abgeschlossen und von Nova angenommen; bestätigte Blocker A/B; empfahl
  Evidence Schema **3.0** mit explizitem `control_id`, Security-Contract-Bindung,
  Scope S3 und `ADR_REQUIRED`.
- **Phase B0 — Governance Foundation (dieser Schritt):** **ADR-0013 angenommen**,
  **D-052 dokumentiert**, WP-018 als `in-review` registriert. **Rein
  dokumentarisch.**

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

## Technischer Stand (unverändert)

- **Implementierter Runtime-Code-Stand: Evidence Schema 2.0** (WP-017, `d3168c4`).
- **Evidence Schema 3.0 ist ausschließlich governance-seitig entschieden** — es
  existiert **kein** `control_id`, **keine** Producer-Klasse
  `security-control-form`, **kein** Security Contract und **keine** 3.0-Bindung
  im Code.
- **Kein** Runtime-Code, **keine** Tests, **keine** Runtime-/Security-Doku und
  **keine** Fixtures wurden in diesem Schritt verändert. Testbasis unverändert
  **451 Tests – OK**, compileall grün.
- Die technische Implementation und die Fixture-/Doku-Migration 2.0 → 3.0
  benötigen eine **gesonderte Nova- und Human-Freigabe** (spätere Phase B).

## Ziel (spätere technische Phase)

Geschlossener, deterministischer, **synthetic-only** Security-Readiness-
Formvertrag: statischer Security Contract (KB-Control→Kriterium-Matrix,
`security_contract_revision`/`_sha256`), `security-control-form`-Artefakte mit
`control_id`, Formprüfung mit **ausschließlich negativer** Faltung
(`INVALID_/CONFLICTING_/STALE_EVIDENCE`), minimal erweiterter A6-Report mit
Bindungszählern und Summeninvariante. **Keine** positive Gate-Erfüllung, **keine**
Security-Freigabe, **keine** reale Enforcement-Bewertung.

## Autoritätsgrenzen

Dieser Governance-Schritt autorisiert **keine** technische Implementation und
**nicht**: reale Source, Ziel-VM, Netzwerk, Secrets, Credentials, RT-2,
Persistenz, Enforcement, Security Readiness, Gate-Pass, Human Approval,
Aktivierung, DRC. Kriterium 5 bleibt Human-only; Kriterium 9 bleibt
non-security-structural; Gate-Kriterien 4/6/7/8/10/11 bleiben
`DEPENDENCY_BLOCKED`.

## Rückmeldung an Nova

Governance Foundation abgeschlossen, **in-review**. Kein Commit, kein Push
(Commit-Autorität beim Human Maintainer). **Keine** technische Implementation
begonnen. Kein nächstes Work Package vorgeschlagen (CBP-WP-019 ausdrücklich
**nicht** begonnen und **nicht** autorisiert).
