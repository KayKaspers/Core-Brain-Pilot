# Mapping Activation Gate Evaluator — Trust Boundary und Vertrag (CBP-WP-016)

| Feld | Wert |
| --- | --- |
| **Status** | **lokaler Prototyp** — read-only, nicht persistent, fail-closed, **nicht produktionsbereit** |
| Grundlage | **PILOT_MAPPING_ACTIVATION_GATE.md** (A3), ADR-0008, ADR-0007, ADR-0009, ADR-0012; **D-050** (A0) |
| Erfasst in | CBP-WP-016 |
| Autoritätsklasse | A2 |
| Python | 3.13+ (nur Standardbibliothek) |
| Stand | 2026-07-27 |

Der Evaluator prüft **read-only**, ob ein synthetischer Mapping-Kandidat und
seine synthetische Evidenz **ausreichend vollständig** sind, um einem Menschen
zur Gate-Prüfung vorgelegt zu werden. Er ist **kein Gate-Executor**, **keine
Aktivierungsinstanz** und **keine A0-Entscheidungsinstanz**.

---

## Scope und Non-Goals

**Scope:** deterministische, nicht persistierte Bewertung der **20 kanonischen
Gate-Kriterien** gegen einen synthetischen `VALID_DRAFT`-Kandidaten, einen
synthetischen `REGISTERED_DISABLED`-Registry-Record und ein synthetisches,
gehashtes Evidenz-Bundle.

**Non-Goals (nicht implementiert):** Gate-Ausführung, Gatefreigabe,
Gate-Statusmutation, Mapping-/Source-/Boundary-Aktivierung, `APPROVED FOR
ACTIVATION`, `REVOKED`, reale Sources/Locators, Source-Inhaltszugriff,
Registry-/Mapping-Schreibzugriff, Persistenz, Netzwerk, Secret-Auflösung,
RT-2-Speicherung, DRC-Ausführung/-Freigabe, Security-Foundation-Freigabe.

## Trust Boundary

| Innerhalb | Außerhalb |
| --- | --- |
| Read-only-Lesen von Draft, Policy, Registry-Record, Evidenz-Bundle | jede Schreiboperation, jede Persistenz |
| Reine Kriterienbewertung (keine Uhr, kein Zufall, keine I/O in der Kernlogik) | Gate-Ausführung, Aktivierung, Human-Entscheidung |
| Nicht persistierter A6-Report auf stdout | Reportdatei, Gate-Statusänderung |

## Kriterienmodell (20, feste Reihenfolge 1..20)

Die 20 Punkte entsprechen exakt `PILOT_MAPPING_ACTIVATION_GATE.md`. **Security
Foundation und DRC sind keine Kriterien 21/22**; ihre Wirkung erfolgt
ausschließlich über die abhängigen Kriterien (4–11, 17).

| ID | Kriterium | Stufe | MVP-Resultat |
| -: | --- | -: | --- |
| 1 | mapping-stored-outside-core | 2 | OUT_OF_SYNTHETIC_SCOPE |
| 2 | schema-valid | 2 | SATISFIED (bei VALID_DRAFT) |
| 3 | no-unknown-fields | 2 | SATISFIED (bei VALID_DRAFT) |
| 4 | secret-scan-passed | 4 | DEPENDENCY_BLOCKED |
| 5 | data-class-confirmed | 4 | HUMAN_DECISION_REQUIRED |
| 6 | ai-transfer-consistent | 4 | DEPENDENCY_BLOCKED |
| 7 | minimal-rights-confirmed | 4 | DEPENDENCY_BLOCKED |
| 8 | read-only-proven | 4 | DEPENDENCY_BLOCKED |
| 9 | allowlist-non-empty | 4 | MISSING_EVIDENCE (deakt. Draft) |
| 10 | exclusions-negative-tested | 4 | DEPENDENCY_BLOCKED |
| 11 | symlink-behavior-checked | 4 | DEPENDENCY_BLOCKED |
| 12 | source-reachable | 3 | OUT_OF_SYNTHETIC_SCOPE |
| 13 | revision-graspable | 2 | SATISFIED (bei VALID_DRAFT) |
| 14 | tombstone-conflict-excluded | 2 | SATISFIED (bei VALID_DRAFT) |
| 15 | operator-review-done | 3 | MISSING_EVIDENCE (menschl. erzeugte operative Evidenz) |
| 16 | human-approval-done | 6 | HUMAN_DECISION_REQUIRED |
| 17 | rt2-audit-provisioned | 3 | MISSING_EVIDENCE |
| 18 | backup-effect-classified | 2 | MISSING_EVIDENCE |
| 19 | rollback-defined | 2 | MISSING_EVIDENCE |
| 20 | activation-separately-authorized | 6 | HUMAN_DECISION_REQUIRED |

Verteilung im gültigen synthetischen Fall: **4 SATISFIED** (2, 3, 13, 14),
**6 DEPENDENCY_BLOCKED** (4, 6, 7, 8, 10, 11), **3 HUMAN_DECISION_REQUIRED**
(5, 16, 20), **5 MISSING_EVIDENCE** (9, 15, 17, 18, 19), **2
OUT_OF_SYNTHETIC_SCOPE** (1, 12) — **16 blockierende** Kriterien.

## Technische Einzelresultate (geschlossen, ≠ Gate-Status)

`SATISFIED`, `MISSING_EVIDENCE`, `INVALID_EVIDENCE`, `STALE_EVIDENCE`,
`CONFLICTING_EVIDENCE`, `HUMAN_DECISION_REQUIRED`, `OUT_OF_SYNTHETIC_SCOPE`,
`DEPENDENCY_BLOCKED`. Diese sind **eindeutig getrennt** von den Gate-Status.

## Gate-Statusumfang

**Ausgabestatus des MVP:** ausschließlich `NOT_EVALUATED` (nicht ausgeführt)
oder **`BLOCKED`** (ausgeführt). Eine **ausgeführte** Evaluation mit fehlender
Evidenz ergibt **immer** `BLOCKED`, **nie** `NOT_EVALUATED`.

`READY FOR ACTIVATION DECISION`, `APPROVED FOR ACTIVATION` und `REVOKED` bleiben
kanonische Vertragswerte des **realen** Gates, sind im synthetischen MVP **nicht
erreichbar** und werden **nie** emittiert (E1/E2). Insbesondere setzt `READY FOR
ACTIVATION DECISION` gültige **A0**-Human-Approval-Evidenz voraus; synthetische
Human-Evidenz ist ein Test-Fixture **ohne** A0-Autorität.

## Human-only- und Abhängigkeitsgrenzen

- **Ausschließlich menschliche Entscheidungen (nie synthetisch erfüllbar):**
  5, 16, 20 — ihr Resultat ist `HUMAN_DECISION_REQUIRED`; der Evaluator trifft
  die Entscheidung **nie** selbst.
- **Menschlich erzeugte operative Evidenz:** Kriterium **15** (Operator Review)
  ist **keine** Gate-Entscheidung und **keine** A0-Freigabe. Der Evaluator prüft
  nur Existenz/Form/Integrität/Revision/Bindung des Review-Nachweises; ein
  synthetischer Review-Record besitzt keine operative Autorität und erfüllt das
  Kriterium **nicht** (`MISSING_EVIDENCE`). 15 wird **nicht** mit 16 (Human
  Approval) oder 20 (Aktivierung) gleichgesetzt.
- **Bedingte Human-Pfade:** V11 (nur bei `read_only:false`) und V14 (nur bei
  `follow_symlinks:true`) — für den zugelassenen Fixture (`read_only=true`,
  `follow_symlinks=false`) **nicht** ausgelöst; ein solcher Draft ist ohnehin
  kein `VALID_DRAFT` und blockiert bereits über die Bindung.
- **Security Foundation Readiness Gate** (`NOT EVALUATED`) und **DRC**
  (`NOT EVALUATED`) sind **keine** direkten Gate-Kriterien; sie wirken indirekt
  über die abhängigen Punkte 4–11, 17.

## Eingabemodell und Bindung

Das geschlossene, versionierte Evidenz-Bundle bindet: `source_id`, `mapping_id`,
`gate_contract_revision`, `evidence_revision`, `mapping_draft_sha256`,
`mapping_policy_sha256`, `registry_record_sha256`, `synthetic_test_only` und die
geschlossene Kriterien-Evidenzliste (20 Einträge, `evidence_ref` = `null` oder
synthetischer Marker). Fail-closed: BOM, ungültiges UTF-8, kein Objekt,
doppelte Schlüssel, `NaN`/`Infinity`, unbekannte/fehlende Felder, unbekannte
Version, nicht synthetisch, reale Pfade/URLs/Secrets werden abgewiesen.

**Bindungs-Blocker (`GATE-BIND-*`):** Draft nicht `VALID_DRAFT`, Registry nicht
gebunden, Source nicht `REGISTERED_DISABLED`, Draft-/Policy-/Record-Hash-Mismatch,
Source-ID-/Mapping-ID-/Vertragsrevisions-Mismatch. `mapping_id` wird nur
**validiert**, nie erzeugt, normalisiert oder ersetzt.

## Report (A6, deterministisch, minimiert, nicht persistent)

Felder: `report_schema_version`, `source_id`, `mapping_id`,
`mapping_draft_sha256`, `mapping_policy_sha256`, `registry_record_sha256`,
`gate_contract_revision`, `gate_contract_sha256`, `evaluation_status`,
`criterion_results` (20, feste Ordnung), `blocker_codes`/`blocker_count`,
`missing_evidence_codes`/`_count`, `human_decision_codes`/`_count`,
`evidence_count`, `implementation_version`. **Keine** Uhr/Datum/Zufall, **keine**
Pfade, URLs, Locators, `source_reference`, Snippets, Secrets, Notes. Code-Listen
sortiert und dedupliziert; Hashes über kanonische Darstellung; JSON mit
sortierten Schlüsseln.

**Feste Semantik:** `evaluation_status` ist **niemals** eine Gatefreigabe oder
Aktivierungsautorisierung; der Report besitzt ausschließlich **A6**-Autorität
und überschreibt A0–A5 nicht.

**ID-Leak-Schutz:** `source_id` und `mapping_id` sind **opake, vertraglich
validierte** IDs. Eine `source_id`, die nicht exakt `src-[0-9a-f]{24}` ist
(Pfad, URL, Locator, Secret, Path Traversal, UNC), wird **fail-closed
abgewiesen** (Exit 14) und gelangt **nie** in den Report oder die Diagnostik.

`mapping_id` ist ein **Pflichtfeld**. Der Wert wird ausschließlich **gelesen und
validiert** — nie erzeugt, normalisiert, ersetzt oder auf `null` redigiert.
Geprüft werden die kanonische Syntax `[A-Za-z0-9][A-Za-z0-9._-]*` (Wiederverwendung
des WP-015-Vertrags), die bestehende Pfad-/URL-Prüfung und die bestehende
Secret-Vokabel (report-sichere Substring-Prüfung, keine zweite Scanner-
Architektur). Eine fehlende, syntaktisch ungültige oder nicht report-sichere
(pfad-/URL-/secretverdächtige) `mapping_id` **blockiert fail-closed vor der
Reporterzeugung** (Exit 14): **kein Report**, kein `null`-Fallback, kein Echo
des Werts, kein Stacktrace — nur ein stabiler `GATE_EVIDENCE_*`-Reason-Code. Nur
ein gültiger, report-sicherer Wert gelangt **unverändert** in den Report; jede
ausgeführte Evaluation trägt damit stets eine gültige `mapping_id` (nie `null`).

## CLI und Exitcodes

`source-mapping activation-evaluate --draft --policy --registry --source-id
--evidence --synthetic-test-only [--json]`. Der bestehende
`source-mapping activation-check` bleibt unverändert (verweigert weiterhin,
Exitcode 13) — **keine** stille Umdeutung.

| Code | Bedeutung |
| --- | --- |
| **14** MAPPING_GATE_EVALUATION_BLOCKED | ausgeführte Evaluation (immer BLOCKED) bzw. fail-closed Evidenzabweisung |
| 2 CONFIG_INVALID | ungültige Mapping-Policy |
| 64 / 70 | USAGE_ERROR / INTERNAL_ERROR (unverändert) |

Exitcode **14** ist kollisionsfrei mit 0–13, 64, 70. **Kein** Exitcode 0 im
Evaluationspfad (der MVP endet immer BLOCKED).

## Aussagegrenzen

**Nicht produktionsbereit.** Kein Gate ausgeführt, keine Aktivierung, keine reale
Source, kein persistentes Ergebnis. **Mapping Activation Gate**, **Security
Foundation Readiness Gate** und **DRC** bleiben `NOT EVALUATED`; **0 von 29**
Capabilities `implemented`.
