"""Datenmodelle des Mapping-Activation-Gate-Evaluators (CBP-WP-016).

Der Evaluator modelliert die **20 kanonischen Gate-Kriterien** aus
`docs/operations/PILOT_MAPPING_ACTIVATION_GATE.md` (A3). Er ist ein lokaler,
synthetisch testbarer, **read-only**, nicht persistenter und fail-closed
Evaluator der **Review-Bereitschaft** — **kein** Gate-Executor, **keine**
Aktivierungsinstanz und **keine** A0-Entscheidungsinstanz.

Der Ausgabestatus des synthetischen MVP ist ausschließlich ``NOT_EVALUATED``
oder ``BLOCKED``. ``READY FOR ACTIVATION DECISION``, ``APPROVED FOR
ACTIVATION`` und ``REVOKED`` bleiben kanonische Vertragswerte des **realen**
Gates, sind im MVP aber **nicht** erreichbar und werden **nie** emittiert.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum
from typing import Final

__all__ = [
    "REPORT_SCHEMA_VERSION",
    "EVIDENCE_SCHEMA_VERSION",
    "EVIDENCE_CONTRACT_REVISION",
    "GATE_CONTRACT_REVISION",
    "IMPLEMENTATION_VERSION",
    "GATE_CRITERION_COUNT",
    "MAX_ARTIFACTS_PER_CRITERION",
    "MAX_ARTIFACTS_TOTAL",
    "PRODUCER_CLASSES",
    "CRITERION_PRODUCER_CLASS",
    "CANONICAL_GATE_STATES",
    "GateStatus",
    "CriterionResult",
    "GateReasonCode",
    "Criterion",
    "GATE_CRITERIA",
    "CriterionOutcome",
    "GateEvaluationReport",
    "gate_contract_sha256",
    "evidence_contract_sha256",
    "canonical_json_bytes",
]

REPORT_SCHEMA_VERSION = "1.0"
# Evidence-Schema/-Vertrag CBP-WP-017: Version 2.0 (eingebettete strukturierte
# Artefakte). Version 1.0 (WP-016) wird fail-closed abgewiesen — es existiert
# keine persistierte oder produktive 1.0-Evidenz (nur Test-Fixtures).
EVIDENCE_SCHEMA_VERSION = "2.0"
EVIDENCE_CONTRACT_REVISION = "2.0"
GATE_CONTRACT_REVISION = "1.0"
IMPLEMENTATION_VERSION = "0.1.0.dev0"
GATE_CRITERION_COUNT = 20

# Mengenlimits des Evidenz-Bundles (fail-closed bei Überschreitung).
MAX_ARTIFACTS_PER_CRITERION = 4
MAX_ARTIFACTS_TOTAL = 80

# Geschlossene Producer-Klassen (nur Klassen, **nie** Personen/Hosts/Instanzen).
PRODUCER_CLASSES: Final[tuple[str, ...]] = (
    "structural-form",
    "foundation-form",
    "operator-review-form",
    "backup-form",
    "rollback-form",
    "rt2-audit-form",
    "human-decision-form",
)

# Feste Kriterien→Producer-Klassen-Zuordnung (jedes Kriterium genau eine Klasse).
# `human-decision-form` deckt die reinen Human-Entscheidungen 16/20 ab (Form,
# **nie** Erfüllung); Kriterium 5 bleibt `foundation-form` (Form, **nie**
# Erfüllung). Die Zuordnung ändert **keine** Autoritätsgrenze — 5/16/20 bleiben
# `HUMAN_DECISION_REQUIRED`, 15/18/19 bleiben operative `MISSING_EVIDENCE`.
CRITERION_PRODUCER_CLASS: Final[dict[int, str]] = {
    1: "structural-form", 2: "structural-form", 3: "structural-form",
    4: "foundation-form", 5: "foundation-form", 6: "foundation-form",
    7: "foundation-form", 8: "foundation-form", 9: "foundation-form",
    10: "foundation-form", 11: "foundation-form",
    12: "structural-form", 13: "structural-form", 14: "structural-form",
    15: "operator-review-form",
    16: "human-decision-form",
    17: "rt2-audit-form",
    18: "backup-form",
    19: "rollback-form",
    20: "human-decision-form",
}

# Vollständige kanonische Gate-Statusmenge (PILOT_MAPPING_ACTIVATION_GATE.md).
# **Nur zur Referenz** — die drei letzten sind vom MVP **nicht** erreichbar und
# werden **nie** ausgegeben oder persistiert.
CANONICAL_GATE_STATES: Final[tuple[str, ...]] = (
    "NOT EVALUATED",
    "BLOCKED",
    "READY FOR ACTIVATION DECISION",
    "APPROVED FOR ACTIVATION",
    "REVOKED",
)


class GateStatus(StrEnum):
    """Die **einzigen** vom MVP modellierbaren Gate-Ausgabestatuswerte.

    Keiner bedeutet Freigabe oder Aktivierung. ``NOT_EVALUATED`` beschreibt
    ausschließlich den **nicht ausgeführten** Zustand; eine ausgeführte
    Evaluation mit fehlender Evidenz ergibt **immer** ``BLOCKED``.
    """

    NOT_EVALUATED = "NOT_EVALUATED"
    BLOCKED = "BLOCKED"


class CriterionResult(StrEnum):
    """Geschlossene technische Einzelresultate — **getrennt** von GateStatus."""

    SATISFIED = "SATISFIED"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    INVALID_EVIDENCE = "INVALID_EVIDENCE"
    STALE_EVIDENCE = "STALE_EVIDENCE"
    CONFLICTING_EVIDENCE = "CONFLICTING_EVIDENCE"
    HUMAN_DECISION_REQUIRED = "HUMAN_DECISION_REQUIRED"
    OUT_OF_SYNTHETIC_SCOPE = "OUT_OF_SYNTHETIC_SCOPE"
    DEPENDENCY_BLOCKED = "DEPENDENCY_BLOCKED"


class GateReasonCode(StrEnum):
    """Stabile Bindungs-Blocker im ``GATE-BIND-``-Namensraum (read-only)."""

    BIND_DRAFT_NOT_VALID = "GATE-BIND-DRAFT-NOT-VALID"
    BIND_REGISTRY_NOT_BOUND = "GATE-BIND-REGISTRY-NOT-BOUND"
    BIND_SOURCE_NOT_REGISTERED_DISABLED = "GATE-BIND-SOURCE-NOT-REGISTERED-DISABLED"
    BIND_DRAFT_HASH_MISMATCH = "GATE-BIND-DRAFT-HASH-MISMATCH"
    BIND_POLICY_HASH_MISMATCH = "GATE-BIND-POLICY-HASH-MISMATCH"
    BIND_RECORD_HASH_MISMATCH = "GATE-BIND-RECORD-HASH-MISMATCH"
    BIND_SOURCE_ID_MISMATCH = "GATE-BIND-SOURCE-ID-MISMATCH"
    BIND_MAPPING_ID_MISMATCH = "GATE-BIND-MAPPING-ID-MISMATCH"
    BIND_CONTRACT_REVISION_MISMATCH = "GATE-BIND-CONTRACT-REVISION-MISMATCH"
    # Kompatibilitätskonstante (WP-016): historisch ungenutzt; die konkrete
    # Stale-Revisionslogik von WP-017 nutzt `EVID_STALE_EVIDENCE_REVISION`.
    BIND_EVIDENCE_REVISION_INVALID = "GATE-BIND-EVIDENCE-REVISION-INVALID"
    # CBP-WP-017 — kriteriumsbezogene, rein negative Artefakt-Evidenzblocker.
    EVID_INVALID_HASH = "GATE-EVID-INVALID-HASH"
    EVID_INVALID_PRODUCER_CLASS = "GATE-EVID-INVALID-PRODUCER-CLASS"
    EVID_CONFLICT_ARTIFACT_ID = "GATE-EVID-CONFLICT-ARTIFACT-ID"
    EVID_CONFLICT_HASH = "GATE-EVID-CONFLICT-HASH"
    EVID_STALE_BINDING = "GATE-EVID-STALE-BINDING"
    EVID_STALE_EVIDENCE_REVISION = "GATE-EVID-STALE-EVIDENCE-REVISION"


@dataclass(frozen=True, slots=True)
class Criterion:
    """Ein kanonisches Gate-Kriterium (unveränderlich)."""

    criterion_id: int
    code: str
    key: str
    nachweisstufe: int
    #: Fixes MVP-Resultat; ``None`` bedeutet: aus Draft/Bindung abgeleitet.
    mvp_result: CriterionResult | None
    human_only: bool


# Die 20 kanonischen Gate-Punkte in **fester** Reihenfolge 1..20.
# Security Foundation und DRC sind **keine** Kriterien 21/22; ihre Wirkung
# erfolgt ausschließlich über die abhängigen Kriterien (4–11, 17).
GATE_CRITERIA: Final[tuple[Criterion, ...]] = (
    Criterion(1, "GATE-CRIT-01", "mapping-stored-outside-core", 2,
              CriterionResult.OUT_OF_SYNTHETIC_SCOPE, False),
    Criterion(2, "GATE-CRIT-02", "schema-valid", 2, None, False),
    Criterion(3, "GATE-CRIT-03", "no-unknown-fields", 2, None, False),
    Criterion(4, "GATE-CRIT-04", "secret-scan-passed", 4,
              CriterionResult.DEPENDENCY_BLOCKED, False),
    Criterion(5, "GATE-CRIT-05", "data-class-confirmed", 4,
              CriterionResult.HUMAN_DECISION_REQUIRED, True),
    Criterion(6, "GATE-CRIT-06", "ai-transfer-consistent", 4,
              CriterionResult.DEPENDENCY_BLOCKED, False),
    Criterion(7, "GATE-CRIT-07", "minimal-rights-confirmed", 4,
              CriterionResult.DEPENDENCY_BLOCKED, False),
    Criterion(8, "GATE-CRIT-08", "read-only-proven", 4,
              CriterionResult.DEPENDENCY_BLOCKED, False),
    Criterion(9, "GATE-CRIT-09", "allowlist-non-empty", 4, None, False),
    Criterion(10, "GATE-CRIT-10", "exclusions-negative-tested", 4,
              CriterionResult.DEPENDENCY_BLOCKED, False),
    Criterion(11, "GATE-CRIT-11", "symlink-behavior-checked", 4,
              CriterionResult.DEPENDENCY_BLOCKED, False),
    Criterion(12, "GATE-CRIT-12", "source-reachable", 3,
              CriterionResult.OUT_OF_SYNTHETIC_SCOPE, False),
    Criterion(13, "GATE-CRIT-13", "revision-graspable", 2, None, False),
    Criterion(14, "GATE-CRIT-14", "tombstone-conflict-excluded", 2, None, False),
    # Kriterium 15 ist **menschlich erzeugte operative Evidenz** (Operator
    # Review), **keine** ausschließlich menschliche Gate-Entscheidung wie 5/16/20
    # und **keine** A0-Freigabe. Der Evaluator prüft nur Existenz/Form/Bindung
    # des Review-Nachweises; ein synthetischer Review-Record besitzt keine
    # operative Autorität ⇒ MISSING_EVIDENCE. `human_only=False`.
    Criterion(15, "GATE-CRIT-15", "operator-review-done", 3,
              CriterionResult.MISSING_EVIDENCE, False),
    Criterion(16, "GATE-CRIT-16", "human-approval-done", 6,
              CriterionResult.HUMAN_DECISION_REQUIRED, True),
    Criterion(17, "GATE-CRIT-17", "rt2-audit-provisioned", 3,
              CriterionResult.MISSING_EVIDENCE, False),
    Criterion(18, "GATE-CRIT-18", "backup-effect-classified", 2,
              CriterionResult.MISSING_EVIDENCE, False),
    Criterion(19, "GATE-CRIT-19", "rollback-defined", 2,
              CriterionResult.MISSING_EVIDENCE, False),
    Criterion(20, "GATE-CRIT-20", "activation-separately-authorized", 6,
              CriterionResult.HUMAN_DECISION_REQUIRED, True),
)


@dataclass(frozen=True, slots=True)
class CriterionOutcome:
    """Ergebnis eines einzelnen Kriteriums in fester Position."""

    criterion_id: int
    code: str
    nachweisstufe: int
    result: CriterionResult

    def to_dict(self) -> dict[str, object]:
        """Minimierte, deterministische Darstellung (kein Freitext)."""
        return {
            "criterion_id": self.criterion_id,
            "code": self.code,
            "nachweisstufe": self.nachweisstufe,
            "result": self.result.value,
        }


@dataclass(frozen=True, slots=True)
class GateEvaluationReport:
    """Nicht persistierter, deterministischer, minimierter A6-Evaluierungsreport.

    Er enthält **keine** Uhr, kein Datum, keinen Zufall, keinen Pfad, keine URL,
    keine ``source_reference``, keinen Locator, keinen Source-Inhalt, kein
    Snippet, kein Secret und keine Notes. ``evaluation_status`` ist **niemals**
    eine Freigabe oder Aktivierung.
    """

    report_schema_version: str
    source_id: str
    # Pflichtfeld: Eine ausgeführte Evaluation trägt **immer** eine gültige,
    # report-sichere `mapping_id`. Ein fehlender, ungültiger oder nicht
    # report-sicherer Wert blockiert fail-closed **vor** der Reporterzeugung
    # (kein null-Fallback, keine Redaktion) — siehe `service.run_activation_evaluate`.
    mapping_id: str
    mapping_draft_sha256: str
    mapping_policy_sha256: str
    registry_record_sha256: str | None
    gate_contract_revision: str
    gate_contract_sha256: str
    evidence_contract_revision: str
    evidence_contract_sha256: str
    evaluation_status: GateStatus
    criterion_results: tuple[CriterionOutcome, ...]
    blocker_codes: tuple[str, ...]
    blocker_count: int
    missing_evidence_codes: tuple[str, ...]
    missing_evidence_count: int
    human_decision_codes: tuple[str, ...]
    human_decision_count: int
    evidence_count: int
    validated_artifact_count: int
    invalid_artifact_count: int
    stale_artifact_count: int
    conflicting_artifact_count: int
    implementation_version: str = IMPLEMENTATION_VERSION

    def to_dict(self) -> dict[str, object]:
        """Kanonische, minimierte JSON-Darstellung (stabile Schlüsselordnung)."""
        return {
            "report_schema_version": self.report_schema_version,
            "source_id": self.source_id,
            "mapping_id": self.mapping_id,
            "mapping_draft_sha256": self.mapping_draft_sha256,
            "mapping_policy_sha256": self.mapping_policy_sha256,
            "registry_record_sha256": self.registry_record_sha256,
            "gate_contract_revision": self.gate_contract_revision,
            "gate_contract_sha256": self.gate_contract_sha256,
            "evidence_contract_revision": self.evidence_contract_revision,
            "evidence_contract_sha256": self.evidence_contract_sha256,
            "evaluation_status": self.evaluation_status.value,
            "criterion_results": [c.to_dict() for c in self.criterion_results],
            "blocker_codes": list(self.blocker_codes),
            "blocker_count": self.blocker_count,
            "missing_evidence_codes": list(self.missing_evidence_codes),
            "missing_evidence_count": self.missing_evidence_count,
            "human_decision_codes": list(self.human_decision_codes),
            "human_decision_count": self.human_decision_count,
            "evidence_count": self.evidence_count,
            "validated_artifact_count": self.validated_artifact_count,
            "invalid_artifact_count": self.invalid_artifact_count,
            "stale_artifact_count": self.stale_artifact_count,
            "conflicting_artifact_count": self.conflicting_artifact_count,
            "implementation_version": self.implementation_version,
        }


def canonical_json_bytes(data: object) -> bytes:
    """Deterministische kanonische JSON-Bytes (sortierte Schlüssel, kein Raum)."""
    return json.dumps(
        data, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")


def gate_contract_sha256() -> str:
    """SHA-256 über die kanonische Serialisierung des 20-Kriterien-Vertrags."""
    material = [
        {
            "criterion_id": c.criterion_id,
            "code": c.code,
            "key": c.key,
            "nachweisstufe": c.nachweisstufe,
        }
        for c in GATE_CRITERIA
    ]
    payload = {"revision": GATE_CONTRACT_REVISION, "criteria": material}
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def evidence_contract_sha256() -> str:
    """SHA-256 über den **vollständigen statischen** Evidence-Vertrag (WP-017).

    Der Hash bindet ausschließlich statische Vertragsbestandteile — Schema-
    Version, Vertragsrevision, geschlossene Feldmengen, erlaubte Producer-
    Klassen, Kriterienzuordnung, Mengenlimits und die feste Evaluationspriorität.
    Er enthält **keine** Laufzeitdaten; identischer Vertrag ⇒ identischer Hash.
    """
    payload = {
        "evidence_schema_version": EVIDENCE_SCHEMA_VERSION,
        "evidence_contract_revision": EVIDENCE_CONTRACT_REVISION,
        "top_level_fields": [
            "evidence_schema_version", "synthetic_test_only", "source_id",
            "mapping_id", "gate_contract_revision", "evidence_contract_revision",
            "evidence_revision", "mapping_draft_sha256", "mapping_policy_sha256",
            "registry_record_sha256", "criterion_evidence",
        ],
        "criterion_evidence_fields": ["criterion", "artifacts"],
        "artifact_fields": [
            "artifact_id", "artifact_sha256", "binding_sha256",
            "producer_class", "evidence_revision", "synthetic_test_only",
        ],
        "artifact_hash_fields": [
            "artifact_id", "binding_sha256", "producer_class",
            "evidence_revision", "synthetic_test_only",
        ],
        "binding_fields": [
            "source_id", "mapping_id", "criterion", "mapping_draft_sha256",
            "mapping_policy_sha256", "registry_record_sha256",
            "gate_contract_revision", "gate_contract_sha256",
            "evidence_contract_revision", "evidence_contract_sha256",
            "evidence_revision",
        ],
        "producer_classes": list(PRODUCER_CLASSES),
        "criterion_producer_class": {
            str(k): v for k, v in sorted(CRITERION_PRODUCER_CLASS.items())
        },
        "max_artifacts_per_criterion": MAX_ARTIFACTS_PER_CRITERION,
        "max_artifacts_total": MAX_ARTIFACTS_TOTAL,
        "evaluation_priority": [
            "INVALID_EVIDENCE", "CONFLICTING_EVIDENCE", "STALE_EVIDENCE",
            "base_criterion_outcome",
        ],
        "canonical_json": ["utf-8", "no-bom", "sorted-keys",
                           "compact-separators", "no-nan-infinity"],
    }
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
