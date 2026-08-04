"""Identitätsbindungsmodell der KB-04-Stufe 1 (Contract §8).

Das Modell bildet die **Form** einer Bindung ab, niemals ihren realen Wert.
Alle Identitäts- und Gruppenangaben sind **opake Referenzen**: das Modul löst
keine Benutzer- oder Gruppennamen auf, ermittelt keine UID- oder GID-Werte und
erzeugt keine Defaults.

Verbindlich (Contract §8): **keine sicheren Defaults für lokale Identitäten**,
**keine stille Ableitung** bei fehlenden Angaben, **keine automatische
Fallback-Identität**. Eine Bindung ist erst gültig, wenn sie **positiv**
validiert wurde.

Reguläre Vertragsabweichungen werden zu ``Finding`` — nicht zu Exceptions.

Der Import dieses Moduls hat keine Nebenwirkungen.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final, Iterable, Sequence

from ..errors import ReasonCode
from .aggregate import Finding, FindingStatus
from .contract import (
    Dimension,
    PathClass,
    PermissionProfile,
    ServiceRole,
)

__all__ = [
    "ValueOrigin",
    "ValidationState",
    "CollisionState",
    "IdentityBinding",
    "REQUIRED_BINDING_FIELDS",
    "validate_binding",
    "validate_binding_set",
]


class ValueOrigin(StrEnum):
    """Herkunft der lokalen Bindungswerte (Contract §8).

    Ausschließlich ``OPERATOR_WORKSPACE`` ist zulässig. ``REPOSITORY``,
    ``DERIVED`` und ``DEFAULT`` sind verbotene Werteklassen und werden allein
    deshalb geführt, damit ihre Ablehnung prüfbar ist.
    """

    OPERATOR_WORKSPACE = "operator-workspace"
    REPOSITORY = "repository"
    DERIVED = "derived"
    DEFAULT = "default"


class ValidationState(StrEnum):
    """Validierungszustand einer Bindung."""

    UNVALIDATED = "unvalidated"
    VALIDATED = "validated"
    REJECTED = "rejected"


class CollisionState(StrEnum):
    """Kollisionszustand einer Bindung."""

    NONE = "none"
    DUPLICATE_ROLE = "duplicate-role"
    DUPLICATE_IDENTITY = "duplicate-identity"
    CROSS_BOUND = "cross-bound"


#: Die zehn Pflichtfelder aus Contract §8.
REQUIRED_BINDING_FIELDS: Final[tuple[str, ...]] = (
    "role_id",
    "host_identity_ref",
    "container_identity_ref",
    "expected_effective_identity",
    "primary_group_ref",
    "path_class_refs",
    "profile_ref",
    "value_origin",
    "validation_state",
    "collision_state",
)

#: Pfadklassen, die keine Bindung tragen dürfen (Contract §8: verbotene Werte).
_FORBIDDEN_PATH_CLASSES: Final[frozenset[PathClass]] = frozenset(
    {PathClass.PC_09, PathClass.PC_10, PathClass.PC_11}
)


@dataclass(frozen=True, slots=True)
class IdentityBinding:
    """Deklarierte Bindung einer abstrakten Rolle an lokale Identitäten.

    Sämtliche ``*_ref``-Felder sind **opake Referenzen** ohne Auflösungspflicht
    und ohne Wertsemantik. Das Modell prüft ihre Anwesenheit und Form, niemals
    ihren Inhalt.
    """

    role_id: ServiceRole | str
    host_identity_ref: str
    container_identity_ref: str
    expected_effective_identity: str
    primary_group_ref: str
    path_class_refs: tuple[PathClass, ...]
    profile_ref: PermissionProfile
    value_origin: ValueOrigin
    validation_state: ValidationState
    collision_state: CollisionState
    read_group_refs: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Gibt eine deterministische, JSON-taugliche Darstellung zurück."""
        return {
            "collision_state": self.collision_state.value,
            "container_identity_ref": self.container_identity_ref,
            "expected_effective_identity": self.expected_effective_identity,
            "host_identity_ref": self.host_identity_ref,
            "path_class_refs": [str(p) for p in self.path_class_refs],
            "primary_group_ref": self.primary_group_ref,
            "profile_ref": self.profile_ref.value,
            "read_group_refs": sorted(self.read_group_refs),
            "role_id": str(self.role_id),
            "validation_state": self.validation_state.value,
            "value_origin": self.value_origin.value,
        }


def _finding(
    reason: ReasonCode,
    detail: str,
    *,
    status: FindingStatus = FindingStatus.VIOLATION,
) -> Finding:
    """Baut einen Bindungsbefund der Dimension D-IV."""
    return Finding(
        path_class=PathClass.PC_11,
        relative_path="<identity-binding>",
        dimension=Dimension.D_IV,
        status=status,
        reason=reason,
        detail=detail,
        origin=None,
    )


def validate_binding(binding: IdentityBinding | None) -> tuple[Finding, ...]:
    """Prüft die Form einer einzelnen Identitätsbindung.

    Read-only, deterministisch, ohne Auflösung realer Identitäten. Eine
    fehlende Bindung ist **fail-closed** und erzeugt genau einen Befund.

    Args:
        binding: Die zu prüfende Bindung oder ``None``.

    Returns:
        Die Befunde in deterministischer Reihenfolge. Ein leeres Tupel
        bedeutet: die Form ist vertragskonform. Das ist **keine** Aussage über
        die Richtigkeit der realen Werte.
    """
    if binding is None:
        return (
            _finding(ReasonCode.KB04_BINDING_MISSING, "no binding supplied"),
        )

    findings: list[Finding] = []

    # Keine stille Ableitung: jedes Pflichtfeld muss belegt sein.
    for name in ("host_identity_ref", "container_identity_ref",
                 "expected_effective_identity", "primary_group_ref"):
        value = getattr(binding, name)
        if not isinstance(value, str) or not value.strip():
            findings.append(
                _finding(
                    ReasonCode.KB04_BINDING_MISSING,
                    f"empty required field: {name}",
                )
            )

    if isinstance(binding.role_id, str) and not isinstance(
        binding.role_id, ServiceRole
    ):
        try:
            ServiceRole(binding.role_id)
        except ValueError:
            findings.append(
                _finding(ReasonCode.KB04_ROLE_UNKNOWN, "unknown role")
            )

    if not binding.path_class_refs:
        findings.append(
            _finding(
                ReasonCode.KB04_BINDING_MISSING, "no path class referenced"
            )
        )
    for path_class in binding.path_class_refs:
        if path_class in _FORBIDDEN_PATH_CLASSES:
            findings.append(
                _finding(
                    ReasonCode.KB04_PATHCLASS_UNKNOWN,
                    f"path class not bindable: {path_class.value}",
                )
            )

    # Kein unsicherer Default, kein Fallback, keine Repositoryherkunft.
    if binding.value_origin is not ValueOrigin.OPERATOR_WORKSPACE:
        findings.append(
            _finding(
                ReasonCode.KB04_BINDING_MISSING,
                f"forbidden value origin: {binding.value_origin.value}",
            )
        )

    if binding.collision_state is not CollisionState.NONE:
        findings.append(
            _finding(
                ReasonCode.KB04_BINDING_COLLISION,
                f"collision: {binding.collision_state.value}",
            )
        )

    # Eine Bindung gilt erst nach positiver Validierung. ``unvalidated`` ist
    # nicht feststellbar und damit fail-closed, ``rejected`` ist eine
    # Verletzung.
    if binding.validation_state is ValidationState.UNVALIDATED:
        findings.append(
            _finding(
                ReasonCode.KB04_STATE_INDETERMINATE,
                "binding not validated",
                status=FindingStatus.INDETERMINATE,
            )
        )
    elif binding.validation_state is ValidationState.REJECTED:
        findings.append(
            _finding(ReasonCode.KB04_BINDING_MISSING, "binding rejected")
        )

    # Lesegruppen sind nur dort zulässig, wo eine Gruppe lesen muss.
    if binding.read_group_refs and binding.profile_ref not in (
        PermissionProfile.PP_2,
        PermissionProfile.PP_3A,
    ):
        findings.append(
            _finding(
                ReasonCode.KB04_GROUP_MISMATCH,
                f"read groups not allowed for {binding.profile_ref.value}",
            )
        )

    return tuple(sorted(findings))


def validate_binding_set(
    bindings: Sequence[IdentityBinding] | Iterable[IdentityBinding],
) -> tuple[Finding, ...]:
    """Prüft eine Menge von Bindungen zusätzlich auf Kollisionen.

    Zwei Rollen auf derselben Identität sind **fail-closed** — die Trennung
    der Identitäten ist der Zweck (KB-02). Eine doppelt gebundene Rolle
    ebenfalls.

    Args:
        bindings: Die zu prüfenden Bindungen.

    Returns:
        Die Befunde aller Einzelprüfungen zuzüglich der Kollisionsbefunde, in
        deterministischer Reihenfolge.
    """
    items = tuple(bindings)
    findings: list[Finding] = []
    for binding in items:
        findings.extend(validate_binding(binding))

    seen_roles: dict[str, int] = {}
    seen_identities: dict[str, int] = {}
    for binding in items:
        seen_roles[str(binding.role_id)] = seen_roles.get(
            str(binding.role_id), 0
        ) + 1
        key = binding.expected_effective_identity
        seen_identities[key] = seen_identities.get(key, 0) + 1

    for role, count in sorted(seen_roles.items()):
        if count > 1:
            findings.append(
                _finding(
                    ReasonCode.KB04_BINDING_COLLISION,
                    f"duplicate role binding: {role}",
                )
            )
    for identity, count in sorted(seen_identities.items()):
        if count > 1:
            findings.append(
                _finding(
                    ReasonCode.KB04_BINDING_COLLISION,
                    "two roles share one effective identity",
                )
            )
            break

    return tuple(sorted(findings))
