"""Geschlossenes, versioniertes synthetisches Evidenz-Bundle (CBP-WP-016).

Das Bundle **bindet** die synthetische Evaluation an genau eine Eingabe: Source
ID, Mapping ID, Gate-Vertragsrevision, Evidenzrevision und die SHA-256-Hashes
von Draft, Policy und Registry-Record. Es enthält **keine** realen Pfade, URLs,
``source_reference``, Credential- oder Secret-Werte.

Fail-closed: BOM, ungültiges UTF-8, kein Objekt, doppelte Schlüssel, ``NaN``,
``Infinity``, unbekannte Felder, fehlende Pflichtfelder, unbekannte
Schema-Version und nicht synthetische Bundles werden abgewiesen. Synthetische
Human-Evidenz ist ausschließlich ein Test-Fixture **ohne** A0-Autorität; das
Bundle kann eine Human-Entscheidung niemals erfüllen.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from ..errors import GateEvidenceError, ReasonCode
from .models import EVIDENCE_SCHEMA_VERSION, GATE_CRITERION_COUNT

__all__ = ["EvidenceBundle", "REQUIRED_EVIDENCE_FIELDS", "load_evidence"]

_MAX_EVIDENCE_BYTES: Final[int] = 65536
_BOM = b"\xef\xbb\xbf"
_SOURCE_ID_RE: Final[re.Pattern[str]] = re.compile(r"\Asrc-[0-9a-f]{24}\Z")
_MAPPING_ID_RE: Final[re.Pattern[str]] = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._-]*\Z")
_HEX64_RE: Final[re.Pattern[str]] = re.compile(r"\A[0-9a-f]{64}\Z")
_SYNTH_REF_RE: Final[re.Pattern[str]] = re.compile(r"\Asynthetic-[A-Za-z0-9._-]+\Z")

REQUIRED_EVIDENCE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "evidence_schema_version",
        "synthetic_test_only",
        "source_id",
        "mapping_id",
        "gate_contract_revision",
        "evidence_revision",
        "mapping_draft_sha256",
        "mapping_policy_sha256",
        "registry_record_sha256",
        "criterion_evidence",
    }
)


@dataclass(frozen=True, slots=True)
class EvidenceBundle:
    """Validiertes, synthetisches Evidenz-Bundle (read-only Bindung)."""

    evidence_schema_version: str
    synthetic_test_only: bool
    source_id: str
    mapping_id: str
    gate_contract_revision: str
    evidence_revision: int
    mapping_draft_sha256: str
    mapping_policy_sha256: str
    registry_record_sha256: str
    provided_evidence_count: int


def _reject(reason: ReasonCode, detail: str = "") -> GateEvidenceError:
    return GateEvidenceError(reason, detail)


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    for key, _ in pairs:
        if key in seen:
            raise _reject(ReasonCode.GATE_EVIDENCE_PARSE_ERROR, "duplicate key")
        seen.add(key)
    return dict(pairs)


def _reject_constant(_token: str) -> Any:
    raise _reject(ReasonCode.GATE_EVIDENCE_PARSE_ERROR, "nan/infinity")


def load_evidence(path: Path) -> EvidenceBundle:
    """Lädt und validiert ein synthetisches Evidenz-Bundle fail-closed.

    Raises:
        GateEvidenceError: Bei jedem strukturellen Verstoß.
    """
    if not path.is_file():
        raise _reject(ReasonCode.GATE_EVIDENCE_FILE_MISSING, path.name)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise _reject(ReasonCode.GATE_EVIDENCE_NOT_READABLE, path.name) from exc
    if len(raw) > _MAX_EVIDENCE_BYTES:
        raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "too large")
    if raw[:3] == _BOM:
        raise _reject(ReasonCode.GATE_EVIDENCE_PARSE_ERROR, "bom")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _reject(ReasonCode.GATE_EVIDENCE_PARSE_ERROR, "utf8") from exc
    try:
        data = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except GateEvidenceError:
        raise
    except (ValueError, RecursionError) as exc:
        raise _reject(ReasonCode.GATE_EVIDENCE_PARSE_ERROR, "json") from exc
    if not isinstance(data, dict):
        raise _reject(ReasonCode.GATE_EVIDENCE_PARSE_ERROR, "not object")
    return _validate(data)


def _validate(data: dict[str, Any]) -> EvidenceBundle:
    version = data.get("evidence_schema_version")
    if version != EVIDENCE_SCHEMA_VERSION:
        raise _reject(ReasonCode.GATE_EVIDENCE_SCHEMA_UNSUPPORTED, "version")

    unknown = sorted(set(data) - REQUIRED_EVIDENCE_FIELDS)
    if unknown:
        raise _reject(ReasonCode.GATE_EVIDENCE_UNKNOWN_FIELD, ", ".join(unknown))
    missing = sorted(REQUIRED_EVIDENCE_FIELDS - set(data))
    if missing:
        raise _reject(ReasonCode.GATE_EVIDENCE_MISSING_FIELD, ", ".join(missing))

    if data["synthetic_test_only"] is not True:
        raise _reject(ReasonCode.GATE_EVIDENCE_NOT_SYNTHETIC, "synthetic_test_only")

    source_id = data["source_id"]
    if not (isinstance(source_id, str) and _SOURCE_ID_RE.match(source_id)):
        raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "source_id")

    mapping_id = data["mapping_id"]
    if not (isinstance(mapping_id, str) and _MAPPING_ID_RE.match(mapping_id)):
        raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "mapping_id")

    if not isinstance(data["gate_contract_revision"], str):
        raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "gate_contract_revision")

    revision = data["evidence_revision"]
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "evidence_revision")

    for field in (
        "mapping_draft_sha256",
        "mapping_policy_sha256",
        "registry_record_sha256",
    ):
        value = data[field]
        if not (isinstance(value, str) and _HEX64_RE.match(value)):
            raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, field)

    provided = _validate_criterion_evidence(data["criterion_evidence"])

    return EvidenceBundle(
        evidence_schema_version=version,
        synthetic_test_only=True,
        source_id=source_id,
        mapping_id=mapping_id,
        gate_contract_revision=data["gate_contract_revision"],
        evidence_revision=revision,
        mapping_draft_sha256=data["mapping_draft_sha256"],
        mapping_policy_sha256=data["mapping_policy_sha256"],
        registry_record_sha256=data["registry_record_sha256"],
        provided_evidence_count=provided,
    )


def _validate_criterion_evidence(entries: Any) -> int:
    """Prüft die geschlossene Kriterien-Evidenzliste (genau 20 Einträge).

    Ein ``evidence_ref`` ist ``null`` oder ein synthetischer Marker
    ``synthetic-*`` **ohne** Pfad, URL oder Secret. Die Referenzen erfüllen
    **kein** Kriterium — sie sind reine Provenienz (fail-closed).

    Returns:
        Anzahl nicht-``null`` Evidenzreferenzen.
    """
    if not isinstance(entries, list) or len(entries) != GATE_CRITERION_COUNT:
        raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "criterion_evidence")
    seen: set[int] = set()
    provided = 0
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"criterion", "evidence_ref"}:
            raise _reject(
                ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "criterion_evidence entry"
            )
        cid = entry["criterion"]
        if (
            not isinstance(cid, int)
            or isinstance(cid, bool)
            or not (1 <= cid <= GATE_CRITERION_COUNT)
            or cid in seen
        ):
            raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "criterion id")
        seen.add(cid)
        ref = entry["evidence_ref"]
        if ref is None:
            continue
        if not (isinstance(ref, str) and _SYNTH_REF_RE.match(ref)):
            raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "evidence_ref")
        provided += 1
    return provided
