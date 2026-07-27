"""Deterministische, read-only Validierung eines Mapping-Entwurfs (CBP-WP-015).

Der Validator wendet den **angenommenen 31-Feld-Vertrag** an und prüft
zusätzlich die synthetische, deaktivierte Draft-Repräsentation. Er **berechnet
`mapping_id` nicht** (Bildungsvorschrift offen) und **verändert nichts**.

Cross-Field-Regeln stammen aus SCHEMA/VALIDATION (V6, V10, V16). Es werden
keine neuen Enum-Werte, kein neues Slot-Präfix und keine neue Rangordnung
eingeführt. Der Import hat keine Nebenwirkungen.
"""

from __future__ import annotations

import re
from typing import Any, Final

from .models import (
    AI_TRANSFER_POLICIES,
    BOUNDARY_LOCATION_TYPES,
    DATA_CLASSES,
    DEPLOYMENT_PROFILES,
    LOCATION_PLACEHOLDER_PREFIX,
    MAPPING_FIELDS,
    OPTIONAL_MAPPING_FIELDS,
    REQUIRED_MAPPING_FIELDS,
    REVISION_STRATEGIES,
    SLOT_BOUNDARY,
    SLOT_IDS,
    MappingPolicy,
    MappingReasonCode,
)

__all__ = [
    "validate_contract_and_state",
    "compare_to_registry",
    "present_field_count",
    "boundary_count",
    "mapping_id_of",
]

R = MappingReasonCode
_URL_MARKERS: Final[tuple[str, ...]] = (
    "://",
    "http:",
    "https:",
    "ftp:",
    "file:",
    "www.",
)
_SECRET_RE: Final[re.Pattern[str]] = re.compile(
    r"\b(password|passwd|secret|token|api_key|apikey|access_key|private_key"
    r"|client_secret|bearer)\b\s*[:=]\s*\S",
    re.IGNORECASE,
)
# Freie Stringfelder, die pfad-/URL-/secretfrei sein müssen.
_SAFE_STRING_FIELDS: Final[tuple[str, ...]] = (
    "mapping_id",
    "mapping_name",
    "operator_reference",
    "location_reference",
    "collection",
    "project",
)
_MAPPING_ID_RE: Final[re.Pattern[str]] = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._-]*\Z")


def present_field_count(draft: dict[str, Any]) -> int:
    """Zählt die im Entwurf vorhandenen kanonischen Vertragsfelder."""
    return len(set(draft) & set(MAPPING_FIELDS))


def boundary_count(draft: dict[str, Any]) -> int:
    """Gibt die Zahl beschriebener Source Boundaries zurück (0 oder 1)."""
    return 1 if isinstance(draft.get("source_boundary_type"), str) else 0


def mapping_id_of(draft: dict[str, Any]) -> str | None:
    """Gibt die bereitgestellte ``mapping_id`` zurück (nicht berechnet)."""
    value = draft.get("mapping_id")
    return value if isinstance(value, str) else None


def validate_contract_and_state(
    draft: dict[str, Any], policy: MappingPolicy
) -> list[MappingReasonCode]:
    """Prüft Vertrag und synthetischen Draft-Zustand (ohne Registry).

    Returns:
        Liste blockierender Gründe. Leer, wenn alle Prüfungen bestehen.
    """
    reasons: list[MappingReasonCode] = []

    # 1 — Unbekannte und fehlende Felder.
    unknown = set(draft) - set(MAPPING_FIELDS)
    if unknown:
        reasons.append(R.UNKNOWN_FIELD)
    missing = REQUIRED_MAPPING_FIELDS - set(draft)
    if missing:
        reasons.append(R.MISSING_FIELD)

    # 2 — Schema-Version.
    if draft.get("schema_version") != policy.required_mapping_schema_version:
        reasons.append(R.SCHEMA_VERSION)

    # 3 — Feldsicherheit (Pfad/URL/dotdot) auf freien Stringfeldern.
    for field in _SAFE_STRING_FIELDS:
        value = draft.get(field)
        if isinstance(value, str):
            safety = _path_url_reason(value)
            if safety is not None:
                reasons.append(safety)

    # 4 — Secret-Indikatoren (V8) auf freien Textfeldern.
    for field in ("mapping_name", "notes"):
        value = draft.get(field)
        if isinstance(value, str) and _SECRET_RE.search(value):
            reasons.append(R.SECRET_INDICATOR)

    # 5 — Slot, Boundary, Location-Type, Revision-Strategie.
    slot = draft.get("slot_id")
    boundary = draft.get("source_boundary_type")
    loc_type = draft.get("location_reference_type")
    if slot not in SLOT_IDS:
        reasons.append(R.SLOT_INVALID)
    else:
        if boundary != SLOT_BOUNDARY[slot]:
            reasons.append(R.BOUNDARY_SLOT_MISMATCH)
        if draft.get("revision_strategy") not in REVISION_STRATEGIES[slot]:
            reasons.append(R.REVISION_STRATEGY_MISMATCH)
    if isinstance(boundary, str) and boundary in BOUNDARY_LOCATION_TYPES:
        if loc_type not in BOUNDARY_LOCATION_TYPES[boundary]:
            reasons.append(R.LOCATION_TYPE_MISMATCH)

    # 6 — location_reference: kanonischer synthetischer V7-Platzhalter.
    location = draft.get("location_reference")
    if not (
        isinstance(location, str)
        and location.startswith(LOCATION_PLACEHOLDER_PREFIX)
        and _path_url_reason(location) is None
    ):
        reasons.append(R.LOCATION_NOT_SYNTHETIC)

    # 7 — Einfache Enum- und Typprüfungen weiterer Felder.
    if draft.get("deployment_profile") not in DEPLOYMENT_PROFILES:
        reasons.append(R.ENUM_VALUE)
    if draft.get("data_class") not in DATA_CLASSES:
        reasons.append(R.ENUM_VALUE)
    if draft.get("ai_transfer_policy") not in AI_TRANSFER_POLICIES:
        reasons.append(R.ENUM_VALUE)
    if draft.get("deletion_behavior") not in {
        "tombstone-and-cleanup",
        "tombstone-only",
    }:
        reasons.append(R.ENUM_VALUE)

    # 8 — mapping_id (V4/V21): vorhanden, stabil, ohne Pfad/Host/Person.
    mid = draft.get("mapping_id")
    if not (isinstance(mid, str) and mid and _MAPPING_ID_RE.match(mid)):
        reasons.append(R.MAPPING_ID_INVALID)

    # 9 — Synthetischer, deaktivierter Draft-Zustand (restriktivste Werte).
    reasons.extend(_draft_state_reasons(draft))

    # 10 — data_class/ai_transfer_policy-Kompatibilität (V10).
    if draft.get("data_class") in {"unknown", "excluded-from-ai"} and draft.get(
        "ai_transfer_policy"
    ) != "forbidden":
        reasons.append(R.DATA_CLASS_AI_INCOMPATIBLE)

    return reasons


def _draft_state_reasons(draft: dict[str, Any]) -> list[MappingReasonCode]:
    reasons: list[MappingReasonCode] = []
    if draft.get("enabled") is not False:
        reasons.append(R.ENABLED_TRUE)
    if draft.get("read_only") is not True:
        reasons.append(R.READ_ONLY_FALSE)
    if draft.get("follow_symlinks") is not False:
        reasons.append(R.FOLLOW_SYMLINKS_TRUE)
    if draft.get("allowed_subpaths") != []:
        reasons.append(R.ALLOWED_SUBPATHS_NONEMPTY)
    if draft.get("excluded_subpaths") != []:
        reasons.append(R.EXCLUDED_SUBPATHS_NONEMPTY)
    if draft.get("approval_status") != "not-approved":
        reasons.append(R.APPROVAL_NOT_DRAFT)
    if draft.get("verification_status") != "unverified":
        reasons.append(R.VERIFICATION_NOT_DRAFT)
    if draft.get("ai_transfer_policy") != "forbidden":
        reasons.append(R.AI_TRANSFER_NOT_FORBIDDEN)
    if draft.get("indexing_policy") != "none":
        reasons.append(R.INDEXING_NOT_NONE)
    if draft.get("local_search_policy") != "forbidden":
        reasons.append(R.LOCAL_SEARCH_NOT_FORBIDDEN)
    if draft.get("mobile_visibility") != "forbidden":
        reasons.append(R.MOBILE_NOT_FORBIDDEN)
    if draft.get("approved_by") is not None:
        reasons.append(R.APPROVED_BY_NOT_NULL)
    if draft.get("approved_at") is not None:
        reasons.append(R.APPROVED_AT_NOT_NULL)
    if draft.get("credential_reference", None) is not None:
        reasons.append(R.CREDENTIAL_REFERENCE_VALUE)
    return reasons


def compare_to_registry(
    draft: dict[str, Any],
    *,
    collection_key: str,
    data_class: str,
    source_reference: str,
    policy: MappingPolicy,
) -> list[MappingReasonCode]:
    """Vergleicht ausschließlich die belegten Felder gegen den Registry-Record.

    **Nur** `collection` ↔ `collection_key` (exakt) und `data_class` ↔
    `data_class` (exakt) sowie `source_reference` synthetisch. **Kein**
    `project`/`domain`-Crosswalk, **keine** `ai`-Gleichsetzung.
    """
    reasons: list[MappingReasonCode] = []
    if not source_reference.startswith("synthetic:"):
        reasons.append(R.SOURCE_REF_NOT_SYNTHETIC)
    if policy.require_collection_exact_match and draft.get("collection") != collection_key:
        reasons.append(R.COLLECTION_MISMATCH)
    if policy.require_data_class_exact_match and draft.get("data_class") != data_class:
        reasons.append(R.DATA_CLASS_MISMATCH)
    return reasons


def _path_url_reason(value: str) -> MappingReasonCode | None:
    if "/" in value or "\\" in value:
        return R.PATH_INDICATOR
    if ".." in value:
        return R.DOTDOT
    lowered = value.lower()
    if any(marker in lowered for marker in _URL_MARKERS):
        return R.URL_INDICATOR
    return None
