"""Mapping Activation Gate Evaluator — CBP-WP-016.

Ein lokaler, synthetisch testbarer, **read-only**, nicht persistenter und
fail-closed Evaluator der **Review-Bereitschaft** eines Mapping-Activation-Gate-
Kandidaten. Er modelliert die **20 kanonischen Gate-Kriterien** (ADR-0008,
`PILOT_MAPPING_ACTIVATION_GATE.md`) und implementiert **nicht**: Gate-Ausführung,
Gatefreigabe, Gate-Statusmutation, Mapping-/Source-/Boundary-Aktivierung, reale
Sources/Locators, Source-Inhaltszugriff, Registry-/Mapping-Schreibzugriff,
Persistenz, Netzwerkzugriff, Secret-Auflösung, RT-2-Speicherung, DRC-Ausführung
oder Security-Foundation-Freigabe.

Der einzige Ausgabestatus des synthetischen MVP ist ``BLOCKED`` (bzw. der nicht
ausgeführte Zustand ``NOT_EVALUATED``). ``READY FOR ACTIVATION DECISION``,
``APPROVED FOR ACTIVATION`` und ``REVOKED`` bleiben kanonische Vertragswerte des
realen Gates, sind im MVP **nicht** erreichbar und werden **nie** emittiert.

Der Report besitzt ausschließlich **A6**-Autorität und ist **keine** Gatefreigabe
und **keine** Aktivierungsautorisierung.

Der Import dieses Pakets hat keine Nebenwirkungen.
"""

from __future__ import annotations

from .evaluator import build_report, evaluate_criteria
from .evidence import EvidenceBundle, load_evidence
from .models import (
    CANONICAL_GATE_STATES,
    CRITERION_PRODUCER_CLASS,
    EVIDENCE_CONTRACT_REVISION,
    EVIDENCE_SCHEMA_VERSION,
    GATE_CONTRACT_REVISION,
    GATE_CRITERIA,
    GATE_CRITERION_COUNT,
    MAX_ARTIFACTS_PER_CRITERION,
    MAX_ARTIFACTS_TOTAL,
    PRODUCER_CLASSES,
    Criterion,
    CriterionOutcome,
    CriterionResult,
    GateEvaluationReport,
    GateReasonCode,
    GateStatus,
    evidence_contract_sha256,
    gate_contract_sha256,
)
from .provenance import (
    ArtifactDescriptor,
    canonical_artifact_sha256,
    canonical_binding_sha256,
    evaluate_criterion_artifacts,
)
from .service import run_activation_evaluate

__all__ = [
    "CANONICAL_GATE_STATES",
    "CRITERION_PRODUCER_CLASS",
    "EVIDENCE_CONTRACT_REVISION",
    "EVIDENCE_SCHEMA_VERSION",
    "GATE_CONTRACT_REVISION",
    "GATE_CRITERIA",
    "GATE_CRITERION_COUNT",
    "MAX_ARTIFACTS_PER_CRITERION",
    "MAX_ARTIFACTS_TOTAL",
    "PRODUCER_CLASSES",
    "Criterion",
    "CriterionOutcome",
    "CriterionResult",
    "GateEvaluationReport",
    "GateReasonCode",
    "GateStatus",
    "evidence_contract_sha256",
    "gate_contract_sha256",
    "EvidenceBundle",
    "load_evidence",
    "ArtifactDescriptor",
    "canonical_artifact_sha256",
    "canonical_binding_sha256",
    "evaluate_criterion_artifacts",
    "evaluate_criteria",
    "build_report",
    "run_activation_evaluate",
]
