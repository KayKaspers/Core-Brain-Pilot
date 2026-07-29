"""Mapping Activation Gate Evaluator — CBP-WP-016/017/018.

Ein lokaler, synthetisch testbarer, **read-only**, nicht persistenter und
fail-closed Evaluator der **Review-Bereitschaft** eines Mapping-Activation-Gate-
Kandidaten. Er modelliert die **20 kanonischen Gate-Kriterien** (ADR-0008,
`PILOT_MAPPING_ACTIVATION_GATE.md`), bindet synthetische Evidenz an einen
statischen **Security Contract** über elf `(criterion, control_id)`-Bindungen
(ADR-0013) und implementiert **nicht**: Gate-Ausführung, Gatefreigabe,
Gate-Statusmutation, Mapping-/Source-/Boundary-Aktivierung, reale
Sources/Locators, Source-Inhaltszugriff, Registry-/Mapping-Schreibzugriff,
Persistenz, Netzwerkzugriff, Secret-Auflösung, RT-2-Speicherung, DRC-Ausführung,
reale Security-Evaluation oder Security-Foundation-Freigabe.

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
    SECURITY_CONTROL_PRODUCER_CLASS,
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
    BindingVerdict,
    SecurityBindingResult,
    canonical_artifact_sha256,
    canonical_binding_sha256,
    evaluate_criterion_artifacts,
    evaluate_security_binding,
)
from .security_contract import (
    CONTROL_ID_RE,
    DOCUMENTED_CONTROLS,
    NON_RUNTIME_SCOPED_CONTROLS,
    NON_SECURITY_STRUCTURAL_CRITERIA,
    RUNTIME_SCOPED_BINDINGS,
    RUNTIME_SCOPED_CONTROLS,
    RUNTIME_SCOPED_CRITERIA,
    SECURITY_CONTRACT_REVISION,
    is_runtime_scoped_binding,
    security_contract_sha256,
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
    "SECURITY_CONTROL_PRODUCER_CLASS",
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
    "BindingVerdict",
    "SecurityBindingResult",
    "canonical_artifact_sha256",
    "canonical_binding_sha256",
    "evaluate_criterion_artifacts",
    "evaluate_security_binding",
    "evaluate_criteria",
    "build_report",
    "run_activation_evaluate",
    # Security Contract (CBP-WP-018 / ADR-0013)
    "SECURITY_CONTRACT_REVISION",
    "CONTROL_ID_RE",
    "DOCUMENTED_CONTROLS",
    "RUNTIME_SCOPED_CONTROLS",
    "NON_RUNTIME_SCOPED_CONTROLS",
    "RUNTIME_SCOPED_BINDINGS",
    "RUNTIME_SCOPED_CRITERIA",
    "NON_SECURITY_STRUCTURAL_CRITERIA",
    "is_runtime_scoped_binding",
    "security_contract_sha256",
]
