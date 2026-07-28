"""Geschlossenes, versioniertes synthetisches Evidenz-Bundle 2.0 (CBP-WP-017).

Das Bundle **bindet** die synthetische Evaluation an genau eine Eingabe: Source
ID, Mapping ID, Gate-/Evidence-Vertragsrevision, Evidenzrevision, die
SHA-256-Hashes von Draft, Policy und Registry-Record sowie **eingebettete
strukturierte Artefakte** je Kriterium. Es enthält **keine** realen Pfade, URLs,
Locators, Credential- oder Secret-Werte.

Fail-closed: BOM, ungültiges UTF-8, kein Objekt, doppelte Schlüssel, ``NaN``,
``Infinity``, unbekannte Felder, fehlende Pflichtfelder, unbekannte
Schema-Version (insb. das abgelöste 1.0), nicht synthetische Bundles/Artefakte,
ungültige IDs/Hashes/Producer-Klassen und Mengenüberschreitungen werden
abgewiesen. Synthetische Evidenz ist ausschließlich ein Test-Fixture **ohne**
A0-/operative Autorität; sie erfüllt **kein** Kriterium.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from ..errors import GateEvidenceError, ReasonCode
from .models import (
    EVIDENCE_SCHEMA_VERSION,
    GATE_CRITERION_COUNT,
    MAX_ARTIFACTS_PER_CRITERION,
    MAX_ARTIFACTS_TOTAL,
    PRODUCER_CLASSES,
)
from .provenance import ArtifactDescriptor

__all__ = ["EvidenceBundle", "REQUIRED_EVIDENCE_FIELDS", "load_evidence"]

# Deterministisches Größenlimit: Worst Case 80 Artefakte (~25 KB kompakt,
# ~50 KB eingerückt) plus Rahmen; 128 KiB bietet ~2,5× Reserve und bleibt hart
# begrenzt (WP-016 nutzte 64 KiB für das artefaktfreie 1.0-Bundle).
_MAX_EVIDENCE_BYTES: Final[int] = 131072
_BOM = b"\xef\xbb\xbf"
_SOURCE_ID_RE: Final[re.Pattern[str]] = re.compile(r"\Asrc-[0-9a-f]{24}\Z")
_MAPPING_ID_RE: Final[re.Pattern[str]] = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._-]*\Z")
_HEX64_RE: Final[re.Pattern[str]] = re.compile(r"\A[0-9a-f]{64}\Z")
_ARTIFACT_ID_RE: Final[re.Pattern[str]] = re.compile(r"\Aart-[0-9a-f]{24}\Z")
_PRODUCER_CLASSES: Final[frozenset[str]] = frozenset(PRODUCER_CLASSES)

REQUIRED_EVIDENCE_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "evidence_schema_version",
        "synthetic_test_only",
        "source_id",
        "mapping_id",
        "gate_contract_revision",
        "evidence_contract_revision",
        "evidence_revision",
        "mapping_draft_sha256",
        "mapping_policy_sha256",
        "registry_record_sha256",
        "criterion_evidence",
    }
)

_ARTIFACT_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "artifact_id",
        "artifact_sha256",
        "binding_sha256",
        "producer_class",
        "evidence_revision",
        "synthetic_test_only",
    }
)


@dataclass(frozen=True, slots=True)
class EvidenceBundle:
    """Validiertes, synthetisches Evidenz-Bundle 2.0 (read-only Bindung)."""

    evidence_schema_version: str
    synthetic_test_only: bool
    source_id: str
    mapping_id: str
    gate_contract_revision: str
    evidence_contract_revision: str
    evidence_revision: int
    mapping_draft_sha256: str
    mapping_policy_sha256: str
    registry_record_sha256: str
    criterion_artifacts: dict[int, tuple[ArtifactDescriptor, ...]]
    total_artifact_count: int


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
    """Lädt und validiert ein synthetisches Evidenz-Bundle 2.0 fail-closed.

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
        # Insbesondere das abgelöste 1.0 wird hier fail-closed abgewiesen.
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

    for field in ("gate_contract_revision", "evidence_contract_revision"):
        value = data[field]
        if not (isinstance(value, str) and value):
            raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, field)

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

    criterion_artifacts, total = _validate_criterion_evidence(data["criterion_evidence"])

    return EvidenceBundle(
        evidence_schema_version=version,
        synthetic_test_only=True,
        source_id=source_id,
        mapping_id=mapping_id,
        gate_contract_revision=data["gate_contract_revision"],
        evidence_contract_revision=data["evidence_contract_revision"],
        evidence_revision=revision,
        mapping_draft_sha256=data["mapping_draft_sha256"],
        mapping_policy_sha256=data["mapping_policy_sha256"],
        registry_record_sha256=data["registry_record_sha256"],
        criterion_artifacts=criterion_artifacts,
        total_artifact_count=total,
    )


def _validate_criterion_evidence(
    entries: Any,
) -> tuple[dict[int, tuple[ArtifactDescriptor, ...]], int]:
    """Prüft die geschlossene 20er-Kriterienliste mit eingebetteten Artefakten."""
    if not isinstance(entries, list) or len(entries) != GATE_CRITERION_COUNT:
        raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "criterion_evidence")
    result: dict[int, tuple[ArtifactDescriptor, ...]] = {}
    total = 0
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or set(entry) != {"criterion", "artifacts"}:
            raise _reject(
                ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "criterion_evidence entry"
            )
        cid = entry["criterion"]
        # Feste, lückenlose Reihenfolge 1..20 (kein Duplikat, keine Lücke).
        if (
            not isinstance(cid, int)
            or isinstance(cid, bool)
            or cid != index + 1
        ):
            raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "criterion id")
        arts = _validate_artifacts(entry["artifacts"])
        result[cid] = arts
        total += len(arts)
    if total > MAX_ARTIFACTS_TOTAL:
        raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "artifacts total")
    return result, total


def _validate_artifacts(items: Any) -> tuple[ArtifactDescriptor, ...]:
    """Prüft die (0..4) Artefakte eines Kriteriums fail-closed."""
    if not isinstance(items, list):
        raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "artifacts")
    if len(items) > MAX_ARTIFACTS_PER_CRITERION:
        raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "artifacts per criterion")
    out: list[ArtifactDescriptor] = []
    for item in items:
        if not isinstance(item, dict) or set(item) != _ARTIFACT_FIELDS:
            raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "artifact entry")
        aid = item["artifact_id"]
        if not (isinstance(aid, str) and _ARTIFACT_ID_RE.match(aid)):
            raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "artifact_id")
        for field in ("artifact_sha256", "binding_sha256"):
            value = item[field]
            if not (isinstance(value, str) and _HEX64_RE.match(value)):
                raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, field)
        producer = item["producer_class"]
        if producer not in _PRODUCER_CLASSES:
            raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "producer_class")
        rev = item["evidence_revision"]
        if not isinstance(rev, int) or isinstance(rev, bool) or rev < 1:
            raise _reject(ReasonCode.GATE_EVIDENCE_INVALID_VALUE, "artifact revision")
        if item["synthetic_test_only"] is not True:
            raise _reject(
                ReasonCode.GATE_EVIDENCE_NOT_SYNTHETIC, "artifact synthetic_test_only"
            )
        out.append(
            ArtifactDescriptor(
                artifact_id=aid,
                artifact_sha256=item["artifact_sha256"],
                binding_sha256=item["binding_sha256"],
                producer_class=producer,
                evidence_revision=rev,
                synthetic_test_only=True,
            )
        )
    return tuple(out)
