"""KB-04 Enforcement Stage 1 — internes, read-only Contract- und Prüfmodell.

Umsetzung von Phase **B2A** aus CBP-WP-022 auf Grundlage von **ADR-0014**
(accepted, A1) und **D-060** (accepted, A0,
``KB-04_STAGE_1_CONTRACT_ACCEPTED``, ``ADR_NOT_REQUIRED``). Normative Authority
bleibt ``docs/security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md``.

Das Paket bildet das maschinenlesbare Teilmodell des Contract ab und prüft
beobachtete Zustände **ausschließlich lesend** dagegen.

Es implementiert **nicht** und autorisiert **nicht**: Initialisierung ·
Migration · Reparatur · ``chmod`` · ``chown`` · Besitz- oder
Gruppenänderung · Dateisystemmutation jeder Art · Mountänderung ·
Identitätsauflösung · reale UID-/GID-Bindung · reale Hostpfade ·
Runtimeintegration · Dienststartblockierung in einer realen Umgebung · CLI ·
Konfigurationsdatei · Deploymentänderung · RT-2 · Gateauswertung oder
-freigabe · Control-Hochstufung · Ausführung von NT-04 oder NT-05.

**Eine synthetisch oder deklariert festgestellte Konformität ist keine
KB-04-Evidenz.** ``ValidationResult.operationally_verified`` bleibt in diesem
Fall ``False``. **KB-04 bleibt `DOCUMENTED ONLY`.**

Das Paket ist **intern**: es wird nicht in ``core.core_brain`` re-exportiert
und begründet keine neue öffentliche Schnittstelle. Es importiert ausschließlich
aus der Python-Standardbibliothek, aus ``core.core_brain.errors`` und aus den
eigenen Modulen.

Der Import dieses Pakets hat keine Nebenwirkungen.
"""

from __future__ import annotations

from .aggregate import (
    REQUIRED_DIMENSIONS,
    Finding,
    FindingStatus,
    ValidationResult,
    aggregate_findings,
    canonical_json_bytes,
)
from .binding import (
    REQUIRED_BINDING_FIELDS,
    CollisionState,
    IdentityBinding,
    ValidationState,
    ValueOrigin,
    validate_binding,
    validate_binding_set,
)
from .contract import (
    CONTRACT_DOCUMENT_PATH,
    CONTRACT_DOCUMENT_SHA256,
    CONTRACT_REVISION,
    PATH_CLASSES,
    PROFILES,
    SPECIAL_BITS,
    WORLD_WRITE_BITS,
    Actor,
    Dimension,
    MountMode,
    ObjectKind,
    PathClass,
    PathClassSpec,
    PermissionProfile,
    ProfileSpec,
    ServiceRole,
    contract_model_sha256,
    normalize_document_bytes,
    path_class_spec,
    profile_spec,
    validate_contract,
)
from .paths import (
    PathResolution,
    StatLike,
    check_path,
    classify_link,
    classify_object_kind,
    detect_hardlink,
    resolve_within_root,
)
from .validator import (
    ContentClassification,
    HostObjectState,
    MountState,
    Observation,
    ObservationOrigin,
    RuntimeIdentityState,
    RuntimeObjectState,
    validate_observation,
)

__all__ = [
    # contract
    "CONTRACT_DOCUMENT_PATH",
    "CONTRACT_DOCUMENT_SHA256",
    "CONTRACT_REVISION",
    "PATH_CLASSES",
    "PROFILES",
    "SPECIAL_BITS",
    "WORLD_WRITE_BITS",
    "Actor",
    "Dimension",
    "MountMode",
    "ObjectKind",
    "PathClass",
    "PathClassSpec",
    "PermissionProfile",
    "ProfileSpec",
    "ServiceRole",
    "contract_model_sha256",
    "normalize_document_bytes",
    "path_class_spec",
    "profile_spec",
    "validate_contract",
    # binding
    "REQUIRED_BINDING_FIELDS",
    "CollisionState",
    "IdentityBinding",
    "ValidationState",
    "ValueOrigin",
    "validate_binding",
    "validate_binding_set",
    # paths
    "PathResolution",
    "StatLike",
    "check_path",
    "classify_link",
    "classify_object_kind",
    "detect_hardlink",
    "resolve_within_root",
    # validator
    "ContentClassification",
    "HostObjectState",
    "MountState",
    "Observation",
    "ObservationOrigin",
    "RuntimeIdentityState",
    "RuntimeObjectState",
    "validate_observation",
    # aggregate
    "REQUIRED_DIMENSIONS",
    "Finding",
    "FindingStatus",
    "ValidationResult",
    "aggregate_findings",
    "canonical_json_bytes",
]
