"""Traceability- und NT-Vorbereitungsfixtures (CBP-WP-022, Phase B2C-T-R).

Kein ``test_``-Praefix: das Modul wird von ``unittest discover`` nicht als
Testmodul entdeckt. Es ist **ausschliesslich Test-Support** und wird von
keinem Produktionsmodul importiert.

Normative Quelle aller Inhalte ist **Contract §15** — zwoelf positive und
dreiunddreissig negative Testkennungen — sowie ergaenzend §16 (NT-04/NT-05)
und §10.6 (PP-3b-Pruefkette). Die Aufteilung folgt **D-061** (A0) und
**D-062** (A0): **37** ``SYNTHETIC_COVERED``, **2**
``SYNTHETIC_COVERAGE_GAP`` und **6** ``B2D_REAL_ONLY`` ueber **45**
Kennungen.

Aussagegrenzen, verbindlich:

* **Synthetisch abdeckbar ist nicht synthetisch abgedeckt.**
* **Eine dokumentierte Abdeckungsluecke ist keine Bestehensaussage.**
* **Eine vollstaendige Matrix ist keine vollstaendige technische Abdeckung.**
* **Eine Vorbereitung ist kein Nachweis, ein Fixture keine NT-Ausfuehrung,
  eine synthetische Abdeckung keine operative Evidenz.**

Dieses Modul erzeugt **kein** Evidence-Schema-3.0-Artefakt, **keine**
Security-Control-Form, **keine** Gate-Eingabe und **schreibt keine Datei**.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Final

__all__ = [
    "TraceabilityDisposition",
    "PreparationStatus",
    "ExecutionStatus",
    "ContractTestTrace",
    "RealOnlyPreparation",
    "CONTRACT_TEST_TRACEABILITY",
    "REAL_ONLY_PREPARATIONS",
    "SYNTHETIC_COVERED_CONTRACT_TEST_IDS",
    "SYNTHETIC_COVERAGE_GAP_CONTRACT_TEST_IDS",
    "B2D_REAL_ONLY_CONTRACT_TEST_IDS",
    "ALLOWED_TEST_MODULES",
    "CONTRACT_DOES_NOT_SPECIFY",
    "GAP_CONTRACT_SECTION",
    "B2D_TARGET",
    "traceability_manifest_dict",
    "traceability_manifest_sha256",
]

#: Neutraler Marker fuer Details, die der Contract **nicht** eindeutig festlegt.
#: Es wird ausdruecklich **kein Wert erfunden**.
CONTRACT_DOES_NOT_SPECIFY: Final[str] = "CONTRACT_DOES_NOT_SPECIFY"

#: Contractabschnitt der beiden Abdeckungsluecken (Schreibzeitvalidierung).
GAP_CONTRACT_SECTION: Final[str] = "10.3"

#: Abstraktes Ziel der real-only Faelle. Keine Instanz, kein Host, kein Pfad.
B2D_TARGET: Final[str] = "B2D — Profile-A Deployment Integration"

#: Herkunft der Vorbereitung beziehungsweise der spaeter noetigen Ausfuehrung.
_SYNTHETIC: Final[str] = "SYNTHETIC"
_OBSERVED: Final[str] = "OBSERVED — reale Profil-A-Instanz, Nachweisstufe 4"

#: Die sechs zulaessigen Quellmodule funktionaler KB-04-Abdeckung.
ALLOWED_TEST_MODULES: Final[tuple[str, ...]] = (
    "tests.test_kb04_aggregate",
    "tests.test_kb04_contract",
    "tests.test_kb04_initialization_guard",
    "tests.test_kb04_initialization_plan",
    "tests.test_kb04_paths",
    "tests.test_kb04_validator",
)


def _c(suffix: str) -> str:
    """Testkennung in ``tests.test_kb04_contract``."""
    return f"tests.test_kb04_contract.{suffix}"


def _p(suffix: str) -> str:
    """Testkennung in ``tests.test_kb04_paths``."""
    return f"tests.test_kb04_paths.{suffix}"


def _v(suffix: str) -> str:
    """Testkennung in ``tests.test_kb04_validator``."""
    return f"tests.test_kb04_validator.{suffix}"


def _a(suffix: str) -> str:
    """Testkennung in ``tests.test_kb04_aggregate``."""
    return f"tests.test_kb04_aggregate.{suffix}"


def _pl(suffix: str) -> str:
    """Testkennung in ``tests.test_kb04_initialization_plan``."""
    return f"tests.test_kb04_initialization_plan.{suffix}"


def _g(suffix: str) -> str:
    """Testkennung in ``tests.test_kb04_initialization_guard``."""
    return f"tests.test_kb04_initialization_guard.{suffix}"


class TraceabilityDisposition(StrEnum):
    """Kanonische Disposition einer Contract-Testkennung (D-062)."""

    SYNTHETIC_COVERED = "SYNTHETIC_COVERED"
    SYNTHETIC_COVERAGE_GAP = "SYNTHETIC_COVERAGE_GAP"
    B2D_REAL_ONLY = "B2D_REAL_ONLY"


class PreparationStatus(StrEnum):
    """Vorbereitungsstatus. Es gibt **nur** diesen einen Wert."""

    PREPARED_ONLY = "PREPARED_ONLY"


class ExecutionStatus(StrEnum):
    """Ausfuehrungsstatus. Es gibt **nur** diesen einen Wert."""

    NOT_EXECUTED = "NOT_EXECUTED"


@dataclass(frozen=True, slots=True)
class ContractTestTrace:
    """Ein Eintrag der Traceability-Matrix zu genau einer Contractkennung.

    ``covered_by`` traegt **ausschliesslich** vollstaendig qualifizierte
    unittest-Kennungen vorhandener funktionaler KB-04-Tests. Fuer
    ``SYNTHETIC_COVERAGE_GAP`` und ``B2D_REAL_ONLY`` ist es **leer** — ein
    leeres ``covered_by`` ist die Aussage *nicht abgedeckt*, niemals
    *bestanden*.
    """

    contract_test_id: str
    contract_title: str
    disposition: TraceabilityDisposition
    coverage_note: str
    covered_by: tuple[str, ...] = ()
    synthetic_support_tests: tuple[str, ...] = ()
    coverage_gap: str = ""
    gap_contract_section: str = ""
    gap_reason_code: str = ""
    b2d_target: str = ""
    real_scope: str = ""
    required_execution_origin: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Deterministische, pfadfreie Abbildung des Eintrags."""
        return {
            "contract_test_id": self.contract_test_id,
            "contract_title": self.contract_title,
            "coverage_gap": self.coverage_gap,
            "coverage_note": self.coverage_note,
            "covered_by": list(self.covered_by),
            "disposition": self.disposition.value,
            "gap_contract_section": self.gap_contract_section,
            "gap_reason_code": self.gap_reason_code,
            "b2d_target": self.b2d_target,
            "real_scope": self.real_scope,
            "required_execution_origin": self.required_execution_origin,
            "synthetic_support_tests": list(self.synthetic_support_tests),
        }


@dataclass(frozen=True, slots=True)
class RealOnlyPreparation:
    """Deklarative Vorbereitung eines ausschliesslich real pruefbaren Falls.

    Es gibt bewusst **kein** Feld ``passed``, **kein** Feld ``conform`` und
    **kein** ``operationally_verified``. Der Status ist unveraenderlich
    ``PREPARED_ONLY``/``NOT_EXECUTED``.
    """

    contract_test_id: str
    contract_title: str
    b2d_target: str
    related_nt: str
    required_profile: str
    real_scope: str
    success_condition: str
    preconditions: tuple[str, ...]
    execution_steps_summary: tuple[str, ...]
    required_dimensions: tuple[str, ...]
    expected_reason_codes: tuple[str, ...]
    forbidden_claims: tuple[str, ...]
    preparation_status: PreparationStatus = PreparationStatus.PREPARED_ONLY
    execution_status: ExecutionStatus = ExecutionStatus.NOT_EXECUTED
    preparation_origin: str = _SYNTHETIC
    required_execution_origin: str = _OBSERVED
    synthetic_support_tests: tuple[str, ...] = field(default=())

    def to_dict(self) -> dict[str, Any]:
        """Deterministische, pfadfreie Abbildung der Vorbereitung."""
        return {
            "contract_test_id": self.contract_test_id,
            "contract_title": self.contract_title,
            "b2d_target": self.b2d_target,
            "execution_status": self.execution_status.value,
            "execution_steps_summary": list(self.execution_steps_summary),
            "expected_reason_codes": list(self.expected_reason_codes),
            "forbidden_claims": list(self.forbidden_claims),
            "preconditions": list(self.preconditions),
            "preparation_origin": self.preparation_origin,
            "preparation_status": self.preparation_status.value,
            "real_scope": self.real_scope,
            "related_nt": self.related_nt,
            "required_dimensions": list(self.required_dimensions),
            "required_execution_origin": self.required_execution_origin,
            "required_profile": self.required_profile,
            "success_condition": self.success_condition,
            "synthetic_support_tests": list(self.synthetic_support_tests),
        }


_COVERED = TraceabilityDisposition.SYNTHETIC_COVERED
_GAP = TraceabilityDisposition.SYNTHETIC_COVERAGE_GAP
_REAL = TraceabilityDisposition.B2D_REAL_ONLY

#: Gemeinsamer Lueckentext der beiden §10.3-Faelle. Er benennt ausdruecklich
#: die fehlende Schreibzeitvalidierung **und** die fehlenden funktionalen
#: Tests und schliesst eine Ersatzzuordnung aus.
_GAP_NOTE: Final[str] = (
    "Contract §10.3 Schreibzeitvalidierung ist nicht implementiert: es gibt "
    "keine Schreibzeitvalidierungsfunktion, keine Pruefung atomarer "
    "Ersetzung und keine Pruefung des temporaeren Schreibkontexts; "
    "KB04-WRITE-CONTRACT-VIOLATION ist ausschliesslich deklariert und hat "
    "keinen produktiven Verwendungsort. Es existiert kein funktionaler Test. "
    "Der Fall bleibt grundsaetzlich synthetisch testbar und ist kein "
    "B2D-real-only-Fall. Eine Ersatzzuordnung zu Root-Boundary-Tests ist "
    "unzulaessig — sie pruefen einen anderen Gegenstand mit einem anderen "
    "ReasonCode. Eine Umsetzung verlangt eine eigene Scopefreigabe sowie "
    "eine erneute ADR- und Decision-Erforderlichkeitspruefung."
)

CONTRACT_TEST_TRACEABILITY: Final[tuple[ContractTestTrace, ...]] = (
    # ------------------------------------------------------------ positiv
    ContractTestTrace(
        contract_test_id="KB04-T-P01",
        contract_title="PP-1 Datei — PC-02, data-worker, 0600, korrekter Owner",
        disposition=_COVERED,
        covered_by=(
            _c("TestPermissionProfiles.test_pp1_modes"),
            _v("TestOwnerGroupAndMode.test_correct_file_mode_is_conform"),
            _v("TestOwnerGroupAndMode.test_correct_owner_is_conform"),
        ),
        coverage_note=(
            "Die PP-1-Dateimodi 0600/0700 sind im Contract-Teilmodell "
            "festgeschrieben; die Konformitaetspruefung von Owner und "
            "Dateimodus ist profilparametrisiert und wird ueber das "
            "Profilspec des gebundenen Profils ausgewertet."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-P02",
        contract_title="PP-1 Verzeichnis — PC-06, data-worker, 0700",
        disposition=_COVERED,
        covered_by=(
            _c("TestPermissionProfiles.test_pp1_modes"),
            _v("TestOwnerGroupAndMode.test_correct_directory_mode_is_conform"),
        ),
        coverage_note=(
            "test_pp1_modes fixiert den Verzeichnismodus 0700; die "
            "Verzeichniskonformitaet wird gegen den Verzeichnismodus des "
            "gebundenen Profils geprueft. test_pp1_modes stuetzt P01 und "
            "P02, weil es Datei- und Verzeichnismodus desselben Profils "
            "gemeinsam festlegt."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-P03",
        contract_title="PP-2 Datei — PC-03, control-plane, 0640, Lesegruppe",
        disposition=_COVERED,
        covered_by=(
            _c("TestPermissionProfiles.test_pp2_modes"),
            _v("TestBindingForm.test_read_groups_allowed_for_pp2"),
            _v("TestObservationDimensions.test_conforming_observation_has_no_violation"),
        ),
        coverage_note=(
            "Die konforme Referenzbeobachtung ist genau der Fall PC-03 mit "
            "PP-2 und Modus 0640; test_pp2_modes fixiert die Modi, "
            "test_read_groups_allowed_for_pp2 die kontrollierte Lesegruppe."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-P04",
        contract_title="PP-2 Verzeichnis — PC-04, control-plane, 0750 bzw. 2750",
        disposition=_COVERED,
        covered_by=(
            _c("TestPermissionProfiles.test_only_pp2_allows_setgid_directories"),
            _c("TestPermissionProfiles.test_pp2_modes"),
            _v("TestOwnerGroupAndMode.test_correct_directory_mode_is_conform"),
            _v("TestOwnerGroupAndMode.test_setgid_directory_allowed_for_pp2"),
        ),
        coverage_note=(
            "Beide zulaessigen Auspraegungen sind belegt: 0750 ueber die "
            "Verzeichniskonformitaet und 2750 ueber die setgid-Ausnahme, die "
            "ausschliesslich PP-2 gewaehrt wird."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-P05",
        contract_title=(
            "PP-3a Leseberechtigung — PC-01, Owner ausserhalb der "
            "Service-Identitaeten, lesbar und nicht schreibbar"
        ),
        disposition=_COVERED,
        covered_by=(
            _c("TestPathClasses.test_canonical_store_has_no_writer"),
            _c("TestPermissionProfiles.test_pp3a_modes_and_no_world_read"),
            _v("TestMountAndRuntimeObject.test_read_only_area_must_not_be_writable"),
        ),
        coverage_note=(
            "Die Anforderung *nicht schreibbar* wird positiv belegt, indem "
            "eine Schreibfaehigkeit im PC-01-Bereich mit PP-3a und "
            "maintainer-owned Owner als Verletzung erkannt wird; das "
            "Contractmodell belegt zusaetzlich, dass PC-01 keine "
            "Schreibrolle besitzt."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-P06",
        contract_title="PP-3b bundle-fixiert — PC-07, 0444/0555",
        disposition=_COVERED,
        covered_by=(
            _c("TestPermissionProfiles.test_pp3b_modes"),
            _v("TestPP3bBoundary.test_non_secret_runtime_config_is_conform"),
            _v("TestPP3bBoundary.test_world_read_is_permitted_only_under_pp3b"),
        ),
        coverage_note=(
            "Die bundle-fixierten Modi 0444/0555 sind im Teilmodell "
            "festgeschrieben; die Konformitaet eines als nicht geheim "
            "klassifizierten PC-07-Artefakts einschliesslich der "
            "World-Read-Ausnahme ist belegt."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-P07",
        contract_title="PP-4 nicht vorhanden — PC-09 und PC-10",
        disposition=_COVERED,
        covered_by=(
            _c("TestPathClasses.test_pp4_classes_are_not_mounted"),
            _c("TestPermissionProfiles.test_pp4_is_not_present"),
            _v("TestMountAndRuntimeObject.test_not_present_area_absent_is_conform"),
        ),
        coverage_note=(
            "PP-4 traegt keinen Modus und ist not-present; PC-09 und PC-10 "
            "sind nicht eingebunden, und die Abwesenheit eines "
            "PP-4-Bereichs wird als konform gewertet."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-P08",
        contract_title="Host-/Container-Bindung vollstaendig und effektiv passend",
        disposition=_COVERED,
        covered_by=(
            _v("TestBindingForm.test_complete_binding_is_clean"),
            _v("TestBindingForm.test_ten_required_fields_declared"),
            _v("TestRuntimeIdentity.test_matching_identity_is_conform"),
        ),
        coverage_note=(
            "Vollstaendigkeit ueber die zehn Pflichtfelder, formale "
            "Gueltigkeit ueber die befundfreie Bindung und die effektive "
            "Uebereinstimmung ueber die Dimension D-IV."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-P09",
        contract_title="read-only Mount — PC-01, PP-3a, ro beidseitig",
        disposition=_COVERED,
        covered_by=(
            _c("TestPathClasses.test_canonical_store_has_no_writer"),
            _v("TestMountAndRuntimeObject.test_expected_mount_mode_is_conform"),
        ),
        coverage_note=(
            "Der erwartete Mountmodus fuehrt zu einer konformen Dimension "
            "D-II; der Mountmodus wird je Pfadklasse aus dem "
            "Contract-Teilmodell bezogen, in dem PC-01 read-only und ohne "
            "Schreibrolle gefuehrt wird."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-P10",
        contract_title=(
            "atomare Ersetzung — PC-03, PP-2, temporaeres Objekt im gleichen "
            "Schreibkontext, konform und ohne unsicheren Zwischenzustand"
        ),
        disposition=_GAP,
        coverage_note=(
            "Nicht abgedeckt. Der Fall bleibt vollstaendig in der Matrix "
            "sichtbar und wird weder als abgedeckt noch als bestanden "
            "gefuehrt."
        ),
        coverage_gap=_GAP_NOTE,
        gap_contract_section=GAP_CONTRACT_SECTION,
        gap_reason_code="",
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-P11",
        contract_title=(
            "neue leere Zielstruktur — PC-02, setup, PP-1; Preflight, Plan "
            "und Post-Validation vollstaendig und idempotent"
        ),
        disposition=_COVERED,
        covered_by=(
            _pl("TestNewAbsent.test_absent_target_is_applicable"),
            _pl("TestNewEmpty.test_empty_target_is_planned"),
            _pl("TestPP4AndAlreadyInitialized.test_already_initialized_has_zero_operations"),
            _pl("TestPP4AndAlreadyInitialized.test_verify_reports_conform_when_initialized"),
        ),
        coverage_note=(
            "Beide zulaessigen Ausgangszustaende — Ziel fehlt und Ziel ist "
            "leer — fuehren zu einem anwendbaren Plan; die Post-Validation "
            "bestaetigt den initialisierten Zustand, und ein bereits "
            "initialisiertes Ziel erzeugt null Operationen, was die "
            "Idempotenz belegt."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-P12",
        contract_title=(
            "PP-3b ueber alle vier Dimensionen nach §10.6 — PC-07, zwoelf "
            "Pruefungen, konform und ohne Schreibfaehigkeit"
        ),
        disposition=_REAL,
        coverage_note=(
            "Die Kennung wird als B2D-real-only gefuehrt, weil ihr "
            "abschliessender D-I-Nachweis eine reale Profil-A-Instanz "
            "verlangt. Die synthetischen Vorpruefungen decken D-II, D-III "
            "und D-IV modellhaft ab; sie geben P12 nicht als vollstaendig "
            "bestanden aus."
        ),
        synthetic_support_tests=(
            _a("TestOperationalVerification.test_synthetic_conform_is_not_verified"),
            _v("TestObservationDimensions.test_all_four_dimensions_present"),
            _v("TestPP3bBoundary.test_non_secret_runtime_config_is_conform"),
            _v("TestPP3bBoundary.test_world_write_stays_forbidden_under_pp3b"),
        ),
        b2d_target=B2D_TARGET,
        real_scope=(
            "die reale Dimension D-I — der Host-Quellzustand des "
            "PP-3b-Artefakts, der nach §10.6 Pruefung 8 separat zu pruefen "
            "oder offen auszuweisen ist"
        ),
        required_execution_origin=_OBSERVED,
    ),
    # ------------------------------------------------------------ negativ
    ContractTestTrace(
        contract_test_id="KB04-T-N01",
        contract_title="world-writable Datei — PC-02, abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _c("TestPermissionProfiles.test_no_profile_is_world_writable"),
            _v("TestOwnerGroupAndMode.test_world_writable_file_is_violation"),
        ),
        coverage_note=(
            "Ein world-writable Dateimodus wird als Verletzung mit "
            "KB04-MODE-WORLD-BITS erkannt; zusaetzlich traegt kein "
            "modelliertes Profil ein World-Schreibbit."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N02",
        contract_title="world-writable Verzeichnis — PC-06, abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _v("TestOwnerGroupAndMode.test_world_writable_directory_is_violation"),
        ),
        coverage_note=(
            "Ein world-writable Verzeichnismodus wird unabhaengig von der "
            "Objektart als KB04-MODE-WORLD-BITS abgelehnt."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N03",
        contract_title="falscher Owner — PC-03, abgelehnt",
        disposition=_COVERED,
        covered_by=(_v("TestOwnerGroupAndMode.test_wrong_owner_is_violation"),),
        coverage_note=(
            "Ein von der Rollenbindung abweichender Owner erzeugt "
            "KB04-OWNER-MISMATCH."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N04",
        contract_title="falsche Gruppe — PC-04, abgelehnt",
        disposition=_COVERED,
        covered_by=(_v("TestOwnerGroupAndMode.test_wrong_group_is_violation"),),
        coverage_note=(
            "Eine von der Rollenbindung abweichende Gruppe erzeugt "
            "KB04-GROUP-MISMATCH."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N05",
        contract_title="falscher Modus — PC-05, abgelehnt",
        disposition=_COVERED,
        covered_by=(_v("TestOwnerGroupAndMode.test_wrong_file_mode_is_violation"),),
        coverage_note=(
            "Ein vom Profilmodus abweichender Dateimodus erzeugt "
            "KB04-MODE-MISMATCH."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N06",
        contract_title="verbotene Supplementary Group — abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _v("TestBindingForm.test_read_groups_forbidden_for_pp1"),
            _v("TestRuntimeIdentity.test_unexpected_supplementary_group_is_violation"),
        ),
        coverage_note=(
            "Sowohl eine nicht deklarierte Supplementary Group der "
            "Runtimeidentitaet als auch eine unter PP-1 unzulaessige "
            "Lesegruppe der Bindung erzeugen KB04-GROUP-MISMATCH."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N07",
        contract_title=(
            "Retrieval kann Canonical schreiben — PC-01, Schreibversuch "
            "scheitert"
        ),
        disposition=_REAL,
        coverage_note=(
            "Ausschliesslich real pruefbar: nur eine reale Profil-A-Instanz "
            "kann belegen, dass der Schreibvorgang auf Betriebssystemebene "
            "scheitert. Der Fall wird niemals als bestanden ausgegeben."
        ),
        b2d_target=B2D_TARGET,
        real_scope=(
            "das tatsaechliche Scheitern des Schreibversuchs auf "
            "Betriebssystemebene, nicht erst in der Anwendung"
        ),
        required_execution_origin=_OBSERVED,
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N08",
        contract_title=(
            "Ingest schreibt Canonical unkontrolliert — PC-01, Schreibversuch "
            "scheitert"
        ),
        disposition=_REAL,
        coverage_note=(
            "Ausschliesslich real pruefbar, Erwartung und Fehlerklassen wie "
            "bei KB04-T-N07. Der Fall wird niemals als bestanden ausgegeben."
        ),
        b2d_target=B2D_TARGET,
        real_scope=(
            "das tatsaechliche Scheitern des unkontrollierten "
            "Ingest-Schreibvorgangs auf Betriebssystemebene"
        ),
        required_execution_origin=_OBSERVED,
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N09",
        contract_title="Host-/Container-Identitaet weicht ab — Startsperre",
        disposition=_COVERED,
        covered_by=(_v("TestRuntimeIdentity.test_identity_mismatch_is_violation"),),
        coverage_note=(
            "Eine von der Bindung abweichende effektive Identitaet erzeugt "
            "KB04-IDENTITY-MISMATCH."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N10",
        contract_title="Bindung fehlt — abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _v("TestBindingForm.test_missing_binding_is_fail_closed"),
            _v("TestRuntimeIdentity.test_identity_without_binding_is_violation"),
        ),
        coverage_note=(
            "Eine fehlende Bindung ist fail-closed — sowohl bei der reinen "
            "Bindungspruefung als auch bei der Beobachtungsvalidierung "
            "entsteht KB04-BINDING-MISSING."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N11",
        contract_title="Bindung kollidiert — abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _v("TestBindingForm.test_collision_state_is_fail_closed"),
            _v("TestBindingForm.test_duplicate_role_collides"),
            _v("TestBindingForm.test_shared_identity_collides"),
        ),
        coverage_note=(
            "Alle drei Kollisionsformen — erklaerter Kollisionszustand, "
            "doppelte Rolle und geteilte Identitaet — erzeugen "
            "KB04-BINDING-COLLISION."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N12",
        contract_title="unbekannte Rolle — abgelehnt",
        disposition=_COVERED,
        covered_by=(_v("TestRuntimeIdentity.test_role_mismatch_is_violation"),),
        coverage_note=(
            "Eine Runtimerolle, die der gebundenen Rolle widerspricht, "
            "erzeugt KB04-ROLE-UNKNOWN."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N13",
        contract_title="unbekannte Pfadklasse — PC-11, abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _v("TestBindingForm.test_unbindable_path_class_is_rejected"),
            _v("TestUnknownPathClass.test_pc_11_is_forbidden_not_neutral"),
        ),
        coverage_note=(
            "PC-11 ist fail-closed und nicht neutral; bindbar ist sie "
            "ebenfalls nicht. Beide Wege erzeugen KB04-PATHCLASS-UNKNOWN."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N14",
        contract_title="Symlink-Escape — PC-02, blockiert",
        disposition=_REAL,
        coverage_note=(
            "Ausschliesslich real pruefbar: nur eine reale Profil-A-Instanz "
            "kann die tatsaechliche Blockade der Aufloesung belegen. Der "
            "Fall wird niemals als bestanden ausgegeben."
        ),
        b2d_target=B2D_TARGET,
        real_scope=(
            "die tatsaechliche Blockade der Symlinkaufloesung — die "
            "Aufloesung wird verweigert, nicht gefolgt"
        ),
        required_execution_origin=_OBSERVED,
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N15",
        contract_title="Hardlink — PC-03, abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _p("TestCheckPath.test_hardlink_is_rejected"),
            _p("TestLinkClassification.test_hardlink_detected_on_regular_file"),
            _v("TestOwnerGroupAndMode.test_host_hardlink_is_violation"),
        ),
        coverage_note=(
            "Erkennung, Pfadpruefung und Beobachtungsvalidierung erzeugen "
            "uebereinstimmend KB04-LINK-HARDLINK."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N16",
        contract_title="Path Traversal — PC-04, abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _p("TestCheckPath.test_outside_root_is_violation"),
            _p("TestRootBoundary.test_parent_is_outside"),
            _p("TestRootBoundary.test_traversal_is_resolved_not_string_matched"),
        ),
        coverage_note=(
            "Die Root-Boundary wird ueber normalisierte Aufloesung und "
            "nicht ueber String-Praefixe durchgesetzt; ein Ergebnis "
            "ausserhalb der Root erzeugt KB04-PATH-OUTSIDE-ROOT."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N17",
        contract_title=(
            "unbekannte Objektart — FIFO, Socket, Device, PC-02, abgelehnt"
        ),
        disposition=_COVERED,
        covered_by=(
            _p("TestCheckPath.test_device_is_rejected"),
            _p("TestCheckPath.test_fifo_is_rejected"),
            _p("TestCheckPath.test_socket_is_rejected"),
            _v("TestOwnerGroupAndMode.test_wrong_object_kind_is_violation"),
        ),
        coverage_note=(
            "Alle drei im Contract genannten Objektarten werden einzeln "
            "abgelehnt; die Beobachtungsvalidierung lehnt eine unzulaessige "
            "Objektart ebenfalls mit KB04-OBJECT-KIND-INVALID ab."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N18",
        contract_title="read-write Mount fuer read-only Rolle — PC-01, abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _v("TestMountAndRuntimeObject.test_read_only_area_must_not_be_writable"),
            _v("TestMountAndRuntimeObject.test_wrong_mount_mode_is_violation"),
        ),
        coverage_note=(
            "Ein vom erwarteten Modus abweichender Mount und eine "
            "Schreibfaehigkeit in einem read-only Bereich erzeugen beide "
            "KB04-MOUNT-MODE-MISMATCH."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N19",
        contract_title="Zustand nicht feststellbar — beliebige Klasse, abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _g("TestObservabilityGuards.test_permission_error_is_indeterminate"),
            _p("TestCheckPath.test_missing_state_is_indeterminate"),
        ),
        coverage_note=(
            "Ein fehlender Zustand und ein nicht lesbarer Zustand fuehren "
            "beide zu KB04-STATE-INDETERMINATE; nicht feststellbar ist "
            "nicht erfuellt."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N20",
        contract_title=(
            "Bestand erfordert Reparatur — PC-05, plan-only ohne Apply"
        ),
        disposition=_COVERED,
        covered_by=(
            _g("TestNonEmptyTarget.test_migration_plan_is_not_applicable"),
            _g("TestNonEmptyTarget.test_unknown_file_requires_migration"),
        ),
        coverage_note=(
            "Ein vorgefundener Bestand erzeugt KB04-MIGRATION-REQUIRED und "
            "einen nicht anwendbaren Plan ohne Operationen — plan-only, "
            "kein Apply."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N21",
        contract_title="Reparatur ohne RT-2 — gesperrt",
        disposition=_COVERED,
        covered_by=(
            _g("TestNonEmptyTarget.test_non_directory_entry_requires_repair"),
            _g("TestNonEmptyTarget.test_repair_is_never_applicable"),
        ),
        coverage_note=(
            "Ein reparaturbeduerftiger Bestand erzeugt "
            "KB04-REPAIR-RT2-REQUIRED, und der Plan ist niemals anwendbar."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N22",
        contract_title=(
            "partielle Initialisierung — PC-02, abgelehnt, Bereich gilt als "
            "nicht vorbereitet"
        ),
        disposition=_COVERED,
        covered_by=(
            _g("TestNonEmptyTarget.test_partial_structure_is_not_applicable"),
            _g("TestNonEmptyTarget.test_partial_structure_is_reported"),
        ),
        coverage_note=(
            "Eine teilweise vorhandene Struktur erzeugt KB04-INIT-PARTIAL "
            "und bleibt nicht anwendbar."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N23",
        contract_title=(
            "nicht unterstuetzte Plattform — nicht feststellbar, fail-closed"
        ),
        disposition=_COVERED,
        covered_by=(
            _g("TestObservabilityGuards.test_unsupported_platform_is_indeterminate"),
            _g("TestObservabilityGuards.test_unsupported_platform_is_never_applicable"),
            _g("TestObservabilityGuards.test_unsupported_platform_never_reports_success"),
        ),
        coverage_note=(
            "Fehlende POSIX-Semantik erzeugt KB04-PLATFORM-UNSUPPORTED, "
            "bleibt nicht anwendbar und meldet niemals Erfolg."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N24",
        contract_title="verbotene Zusatzbits — PC-06, abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _v("TestOwnerGroupAndMode.test_setgid_directory_forbidden_for_pp1"),
            _v("TestOwnerGroupAndMode.test_setuid_is_violation"),
            _v("TestOwnerGroupAndMode.test_sticky_bit_is_violation"),
        ),
        coverage_note=(
            "setuid, sticky und ein setgid-Verzeichnis ausserhalb der "
            "PP-2-Ausnahme erzeugen jeweils KB04-MODE-SPECIAL-BITS."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N25",
        contract_title=(
            "Schreibzeitverletzung — PC-03, temporaeres Objekt ausserhalb des "
            "gleichwertigen Sicherheitskontexts, Vorgang abgelehnt"
        ),
        disposition=_GAP,
        coverage_note=(
            "Nicht abgedeckt. Der Fall bleibt vollstaendig in der Matrix "
            "sichtbar und wird weder als abgedeckt noch als bestanden "
            "gefuehrt."
        ),
        coverage_gap=_GAP_NOTE,
        gap_contract_section=GAP_CONTRACT_SECTION,
        gap_reason_code="KB04-WRITE-CONTRACT-VIOLATION",
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N26",
        contract_title=(
            "PP-3b-Artefakt enthaelt Secretmaterial — PC-07, abgelehnt, nicht "
            "als PP-3b klassifizierbar"
        ),
        disposition=_COVERED,
        covered_by=(_v("TestPP3bBoundary.test_sensitive_or_secret_is_violation"),),
        coverage_note=(
            "Eine Klassifikation als sensibel oder geheim erzeugt "
            "KB04-CONTRACT-INVALID; das Fixture verwendet ausschliesslich "
            "einen synthetischen Marker, niemals einen Wert."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N27",
        contract_title="PP-3b ausserhalb PC-07 verwendet — abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _c("TestPermissionProfiles.test_pp3b_is_exclusive_to_pc_07"),
            _c("TestPermissionProfiles.test_pp3b_is_used_by_exactly_one_path_class"),
            _v("TestPP3bBoundary.test_pp3b_is_not_used_outside_pc_07"),
        ),
        coverage_note=(
            "Die Exklusivitaet von PP-3b fuer PC-07 ist im Teilmodell "
            "verankert und wird zusaetzlich ueber die tatsaechliche "
            "Profilzuordnung aller Pfadklassen belegt."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N28",
        contract_title="Host-Quellrechte nicht feststellbar — PC-07, abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _v("TestObservationDimensions.test_missing_host_is_indeterminate"),
            _v("TestPP3bBoundary.test_unclassified_is_indeterminate"),
        ),
        coverage_note=(
            "Ein fehlender Hostzustand macht die Dimension D-I "
            "unbestimmbar; im PC-07-Kontext fuehrt auch eine nicht "
            "feststellbare Klassifikation zu KB04-STATE-INDETERMINATE."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N29",
        contract_title=(
            "Runtimeobjekt erscheint read-only, Hostquelle nicht positiv "
            "validiert — PC-07, abgelehnt, D-III belegt D-I nicht (MT-10)"
        ),
        disposition=_COVERED,
        covered_by=(
            _a("TestAggregationBasics.test_single_indeterminate_prevents_pass"),
            _a("TestOperationalVerification.test_missing_dimension_defeats_verification"),
            _v("TestObservationDimensions.test_missing_host_is_indeterminate"),
        ),
        coverage_note=(
            "test_missing_host_is_indeterminate stuetzt N28 und N29, weil "
            "es genau den Zustand herstellt, den beide beschreiben: D-III "
            "liegt vor, D-I nicht. N28 wertet dies als Nichtfeststellbarkeit "
            "der Host-Quellrechte, N29 zusaetzlich als fehlenden Beleg von "
            "D-I durch D-III; die Aggregation zeigt, dass ein einzelner "
            "unbestimmter Befund jede Erfuellung verhindert."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N30",
        contract_title="Mount ist read-write — PC-07, abgelehnt",
        disposition=_COVERED,
        covered_by=(
            _v("TestMountAndRuntimeObject.test_read_only_area_must_not_be_writable"),
            _v("TestMountAndRuntimeObject.test_wrong_mount_mode_is_violation"),
        ),
        coverage_note=(
            "Ein vom erwarteten read-only Modus abweichender Mount erzeugt "
            "KB04-MOUNT-MODE-MISMATCH. Die beiden Tests stuetzen N18 und "
            "N30, weil der Contract fuer beide Pfadklassen denselben "
            "Mountvertrag und dieselbe Fehlerklasse vorsieht."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N31",
        contract_title="Runtime kann das Artefakt veraendern — PC-07, abgelehnt",
        disposition=_REAL,
        coverage_note=(
            "Ausschliesslich real pruefbar: die tatsaechliche "
            "Unveraenderbarkeit auf einer Profil-A-Instanz kann synthetisch "
            "nicht belegt werden. Der Fall wird niemals als bestanden "
            "ausgegeben."
        ),
        b2d_target=B2D_TARGET,
        real_scope=(
            "der tatsaechliche Nachweis, dass die Runtime keine "
            "Schreibfaehigkeit auf das PP-3b-Artefakt besitzt — nach §10.6 "
            "Pruefung 6 negativ zu belegen"
        ),
        required_execution_origin=_OBSERVED,
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N32",
        contract_title=(
            "Unerwartete Identitaet kann auf das Artefakt zugreifen — PC-07, "
            "abgelehnt"
        ),
        disposition=_COVERED,
        covered_by=(
            _v("TestRuntimeIdentity.test_identity_mismatch_is_violation"),
            _v("TestRuntimeIdentity.test_unexpected_supplementary_group_is_violation"),
        ),
        coverage_note=(
            "Der Contract nennt fuer N32 beide Fehlerklassen; eine "
            "abweichende effektive Identitaet erzeugt "
            "KB04-IDENTITY-MISMATCH, eine unerwartete Supplementary Group "
            "KB04-GROUP-MISMATCH. Die beiden Tests stuetzen zusaetzlich N09 "
            "beziehungsweise N06, dort jedoch fuer die jeweils andere "
            "Contractanforderung."
        ),
    ),
    ContractTestTrace(
        contract_test_id="KB04-T-N33",
        contract_title=(
            "Bundlemodus und tatsaechlich sichtbarer Zustand weichen ab — "
            "PC-07, abgelehnt, der Bundlewert wird nicht automatisch "
            "akzeptiert (MT-9)"
        ),
        disposition=_REAL,
        coverage_note=(
            "Ausschliesslich real pruefbar: der Abgleich des Bundlewerts "
            "gegen den tatsaechlich sichtbaren Zustand verlangt eine reale "
            "Profil-A-Instanz. Der Fall wird niemals als bestanden "
            "ausgegeben."
        ),
        b2d_target=B2D_TARGET,
        real_scope=(
            "der tatsaechliche Abgleich zwischen zugesagtem Bundlemodus "
            "und sichtbarem Zustand nach §10.6 Pruefung 12"
        ),
        required_execution_origin=_OBSERVED,
    ),
)

#: Gemeinsame verbotene Aussagen aller sechs Vorbereitungen.
_COMMON_FORBIDDEN: Final[tuple[str, ...]] = (
    "dass ein Gate erfuellt ist",
    "dass eine Control hochgestuft werden darf",
    "dass KB-04 den Status DOCUMENTED ONLY verlaesst",
    "dass eine Vorbereitung ein Nachweis ist",
)

REAL_ONLY_PREPARATIONS: Final[tuple[RealOnlyPreparation, ...]] = (
    RealOnlyPreparation(
        contract_test_id="KB04-T-N07",
        contract_title=(
            "Retrieval kann Canonical schreiben — PC-01, Schreibversuch "
            "scheitert"
        ),
        b2d_target=B2D_TARGET,
        related_nt="NT-04",
        required_profile="PP-3a",
        real_scope=(
            "das tatsaechliche Scheitern des Schreibversuchs auf "
            "Betriebssystemebene, nicht erst in der Anwendung"
        ),
        success_condition=(
            "Der Schreibvorgang scheitert auf Betriebssystemebene. Ein "
            "Scheitern erst in der Anwendung erfuellt die Bedingung nicht."
        ),
        preconditions=(
            "eine reale Profil-A-Instanz nach Nachweisstufe 4",
            "PC-01 ist mit PP-3a und beidseitig read-only eingebunden",
            "die Rolle retrieval besitzt kein Canonical-Schreibrecht",
            "Vertragsregeln I-3 und I-4 sowie MT-3 bis MT-6 sind wirksam",
        ),
        execution_steps_summary=(
            "die Rolle ohne Canonical-Schreibrecht versucht zu schreiben",
            "das Ablehnungsverhalten des Betriebssystems wird beobachtet",
            "der beobachtete Zustand wird mit Herkunft OBSERVED erfasst",
        ),
        required_dimensions=(CONTRACT_DOES_NOT_SPECIFY,),
        expected_reason_codes=(
            "KB04-MODE-MISMATCH",
            "KB04-MOUNT-MODE-MISMATCH",
        ),
        forbidden_claims=_COMMON_FORBIDDEN
        + (
            "dass KB-03 vollstaendig ist",
            "dass andere Bereiche geschuetzt sind",
        ),
    ),
    RealOnlyPreparation(
        contract_test_id="KB04-T-N08",
        contract_title=(
            "Ingest schreibt Canonical unkontrolliert — PC-01, Schreibversuch "
            "scheitert"
        ),
        b2d_target=B2D_TARGET,
        related_nt="NT-04",
        required_profile="PP-3a",
        real_scope=(
            "das tatsaechliche Scheitern des unkontrollierten "
            "Ingest-Schreibvorgangs auf Betriebssystemebene"
        ),
        success_condition=(
            "Der unkontrollierte Schreibvorgang scheitert auf "
            "Betriebssystemebene."
        ),
        preconditions=(
            "eine reale Profil-A-Instanz nach Nachweisstufe 4",
            "PC-01 ist mit PP-3a und beidseitig read-only eingebunden",
            "die Rolle ingest schreibt Canonical nicht unkontrolliert",
            "Vertragsregeln I-3 und I-4 sowie MT-3 bis MT-6 sind wirksam",
        ),
        execution_steps_summary=(
            "die Ingest-Rolle versucht einen unkontrollierten Schreibvorgang",
            "das Ablehnungsverhalten des Betriebssystems wird beobachtet",
            "der beobachtete Zustand wird mit Herkunft OBSERVED erfasst",
        ),
        required_dimensions=(CONTRACT_DOES_NOT_SPECIFY,),
        expected_reason_codes=(
            "KB04-MODE-MISMATCH",
            "KB04-MOUNT-MODE-MISMATCH",
        ),
        forbidden_claims=_COMMON_FORBIDDEN
        + (
            "dass KB-03 vollstaendig ist",
            "dass andere Bereiche geschuetzt sind",
        ),
    ),
    RealOnlyPreparation(
        contract_test_id="KB04-T-N14",
        contract_title="Symlink-Escape — PC-02, blockiert",
        b2d_target=B2D_TARGET,
        related_nt="NT-05",
        required_profile="PP-1",
        real_scope=(
            "die tatsaechliche Blockade der Symlinkaufloesung — die "
            "Aufloesung wird verweigert, nicht gefolgt"
        ),
        success_condition=(
            "Die Aufloesung wird verweigert. Ein blosses Erkennen ohne "
            "Blockade erfuellt die Bedingung nicht."
        ),
        preconditions=(
            "eine reale Profil-A-Instanz nach Nachweisstufe 4",
            "ein Symlink innerhalb eines geschuetzten Bereichs zeigt nach "
            "aussen",
            "Vertragsregel I-5 sowie LP-1 bis LP-4 und LP-9 sind wirksam",
        ),
        execution_steps_summary=(
            "der bereichsverlassende Symlink wird angesprochen",
            "die Verweigerung der Aufloesung wird beobachtet",
            "der beobachtete Zustand wird mit Herkunft OBSERVED erfasst",
        ),
        required_dimensions=(CONTRACT_DOES_NOT_SPECIFY,),
        expected_reason_codes=("KB04-LINK-SYMLINK-ESCAPE",),
        forbidden_claims=_COMMON_FORBIDDEN
        + (
            "dass Hardlinks abgedeckt sind",
            "dass TOCTOU geloest ist",
        ),
    ),
    RealOnlyPreparation(
        contract_test_id="KB04-T-N31",
        contract_title="Runtime kann das Artefakt veraendern — PC-07, abgelehnt",
        b2d_target=B2D_TARGET,
        related_nt="CONTRACT_DECLARES_NO_NT_REFERENCE",
        required_profile="PP-3b",
        real_scope=(
            "der tatsaechliche Nachweis, dass die Runtime keine "
            "Schreibfaehigkeit auf das PP-3b-Artefakt besitzt"
        ),
        success_condition=(
            "Die Runtime besitzt keine Schreibfaehigkeit; dies ist nach "
            "§10.6 Pruefung 6 negativ zu belegen."
        ),
        preconditions=(
            "eine reale Profil-A-Instanz nach Nachweisstufe 4",
            "PC-07 ist mit PP-3b und read-only eingebunden",
            "das Artefakt ist als nicht geheim klassifiziert",
        ),
        execution_steps_summary=(
            "die Schreibfaehigkeit der Runtime auf PC-07 wird geprueft",
            "die Abwesenheit der Schreibfaehigkeit wird negativ belegt",
            "der beobachtete Zustand wird mit Herkunft OBSERVED erfasst",
        ),
        required_dimensions=("D-III",),
        expected_reason_codes=(
            "KB04-MODE-MISMATCH",
            "KB04-MOUNT-MODE-MISMATCH",
        ),
        forbidden_claims=_COMMON_FORBIDDEN
        + ("dass der Bundlemodus allein den Hostzustand belegt",),
    ),
    RealOnlyPreparation(
        contract_test_id="KB04-T-N33",
        contract_title=(
            "Bundlemodus und tatsaechlich sichtbarer Zustand weichen ab — "
            "PC-07, abgelehnt"
        ),
        b2d_target=B2D_TARGET,
        related_nt="CONTRACT_DECLARES_NO_NT_REFERENCE",
        required_profile="PP-3b",
        real_scope=(
            "der tatsaechliche Abgleich zwischen zugesagtem Bundlemodus und "
            "sichtbarem Zustand nach §10.6 Pruefung 12"
        ),
        success_condition=(
            "Bundlemodus und sichtbarer Zustand stimmen ueberein; der "
            "Bundlewert wird nach MT-9 nicht automatisch akzeptiert."
        ),
        preconditions=(
            "eine reale Profil-A-Instanz nach Nachweisstufe 4",
            "der Bundlemodus des Config-Bindmounts ist bekannt",
            "der runtime-sichtbare Zustand ist beobachtbar",
        ),
        execution_steps_summary=(
            "der zugesagte Bundlemodus wird erfasst",
            "der runtime-sichtbare Zustand wird erfasst",
            "beide Werte werden gegeneinander abgeglichen",
        ),
        required_dimensions=("D-II", "D-III"),
        expected_reason_codes=("KB04-MODE-MISMATCH",),
        forbidden_claims=_COMMON_FORBIDDEN
        + ("dass der Bundlemodus allein den sichtbaren Zustand belegt",),
    ),
    RealOnlyPreparation(
        contract_test_id="KB04-T-P12",
        contract_title=(
            "PP-3b ueber alle vier Dimensionen nach §10.6 — reale Dimension "
            "D-I verbleibend"
        ),
        b2d_target=B2D_TARGET,
        related_nt="CONTRACT_DECLARES_NO_NT_REFERENCE",
        required_profile="PP-3b",
        real_scope=(
            "die reale Dimension D-I — der Host-Quellzustand des "
            "PP-3b-Artefakts"
        ),
        success_condition=(
            "Der Host-Quellzustand ist nach §10.6 Pruefung 8 separat "
            "geprueft. Solange D-I nicht positiv validiert werden kann, ist "
            "er offen auszuweisen und darf nicht als erfuellt dargestellt "
            "werden."
        ),
        preconditions=(
            "eine reale Profil-A-Instanz nach Nachweisstufe 4",
            "D-II, D-III und D-IV sind synthetisch modelliert vorgeprueft",
            "das Artefakt ist als nicht geheim klassifiziert",
        ),
        execution_steps_summary=(
            "der Host-Quellzustand des Artefakts wird real erhoben",
            "er wird gegen die Profilzusage geprueft",
            "der beobachtete Zustand wird mit Herkunft OBSERVED erfasst",
        ),
        required_dimensions=("D-I",),
        expected_reason_codes=("KB04-STATE-INDETERMINATE",),
        forbidden_claims=_COMMON_FORBIDDEN
        + (
            "dass KB04-T-P12 bestanden ist",
            "dass D-III den Zustand von D-I belegt",
        ),
        synthetic_support_tests=(
            _a("TestOperationalVerification.test_synthetic_conform_is_not_verified"),
            _v("TestObservationDimensions.test_all_four_dimensions_present"),
            _v("TestPP3bBoundary.test_non_secret_runtime_config_is_conform"),
            _v("TestPP3bBoundary.test_world_write_stays_forbidden_under_pp3b"),
        ),
    ),
)


def _ids_with(disposition: TraceabilityDisposition) -> tuple[str, ...]:
    """Sortierte Kennungen einer Disposition."""
    return tuple(
        sorted(
            t.contract_test_id
            for t in CONTRACT_TEST_TRACEABILITY
            if t.disposition is disposition
        )
    )


SYNTHETIC_COVERED_CONTRACT_TEST_IDS: Final[tuple[str, ...]] = _ids_with(
    TraceabilityDisposition.SYNTHETIC_COVERED
)
SYNTHETIC_COVERAGE_GAP_CONTRACT_TEST_IDS: Final[tuple[str, ...]] = _ids_with(
    TraceabilityDisposition.SYNTHETIC_COVERAGE_GAP
)
B2D_REAL_ONLY_CONTRACT_TEST_IDS: Final[tuple[str, ...]] = _ids_with(
    TraceabilityDisposition.B2D_REAL_ONLY
)


def traceability_manifest_dict() -> dict[str, Any]:
    """Deterministische Gesamtabbildung der Matrix.

    Enthaelt keine absoluten Pfade, keine Laufzeiten, keine Angaben zur
    lokalen Testumgebung und keine realen Identitaetswerte. **Es wird keine
    Datei geschrieben**, und es entsteht **kein** Evidence-Artefakt.
    """
    entries = sorted(
        (t.to_dict() for t in CONTRACT_TEST_TRACEABILITY),
        key=lambda e: e["contract_test_id"],
    )
    preparations = sorted(
        (p.to_dict() for p in REAL_ONLY_PREPARATIONS),
        key=lambda p: p["contract_test_id"],
    )
    return {
        "counts": {
            "b2d_real_only": len(B2D_REAL_ONLY_CONTRACT_TEST_IDS),
            "real_only_preparations": len(preparations),
            "synthetic_coverage_gap": len(
                SYNTHETIC_COVERAGE_GAP_CONTRACT_TEST_IDS
            ),
            "synthetic_covered": len(SYNTHETIC_COVERED_CONTRACT_TEST_IDS),
            "total": len(entries),
        },
        "entries": entries,
        "gap_contract_section": GAP_CONTRACT_SECTION,
        "real_only_preparations": preparations,
    }


def traceability_manifest_sha256() -> str:
    """Byte-stabiler Hash ueber die kanonische Serialisierung der Matrix."""
    payload = json.dumps(
        traceability_manifest_dict(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
