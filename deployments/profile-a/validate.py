"""Deterministic offline validator for the Profile-A deployment bundle.

CBP-WP-020 Phase B2 (D-055). This is a **repository and bundle tool only**:
it is not a product runtime module, not a service, not a daemon and not a
deployment agent.

It never calls Docker, never uses the network, never starts a process, never
reads host users, UIDs or GIDs, never resolves secrets and never reads a file
outside the bundle root. It only reads, never writes.

Python standard library only.
"""

from __future__ import annotations

import json
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

__all__ = ["ValidationIssue", "ValidationReport", "validate_bundle", "main"]

# --- contract constants ----------------------------------------------------

EXPECTED_FILES: tuple[str, ...] = (
    "README.md",
    "bundle.json",
    "compose.yaml",
    "config/control-plane.example.toml",
    "config/data-worker.example.toml",
    "operator.env.example",
    "validate.py",
)

#: ``validate.py`` carries the detection patterns below and is therefore
#: exempt from its own *content* leakage scan (it is still part of the file set).
LEAKAGE_EXEMPT: tuple[str, ...] = ("validate.py",)

SERVICES: tuple[str, ...] = ("control-plane", "data-worker")
IDENTITIES = {"control-plane": "svc-control-plane", "data-worker": "svc-data-worker"}
NETWORK_NAME = "cbp-profile-a-internal"
ALLOWED_TOP_LEVEL = frozenset({"name", "services", "networks", "volumes", "configs"})
ALLOWED_CONTAINER_PATHS = frozenset({
    "/etc/cbp",
    "/run/cbp",
    "/tmp",
    "/var/lib/cbp/canonical",
    "/var/lib/cbp/derived",
    "/var/lib/cbp/mapping-registry",
    "/var/lib/cbp/quarantine",
    "/var/lib/cbp/released",
    "/var/lib/cbp/source-registry",
})
FORBIDDEN_AREAS = frozenset({"backup-storage", "rt2-operational-evidence", "rt2"})

MOUNTS = {
    "control-plane": {
        "canonical-data": True,
        "source-registry": False,
        "mapping-registry": False,
        "released-artifacts": False,
    },
    "data-worker": {
        "canonical-data": True,
        "source-registry": True,
        "mapping-registry": True,
        "quarantine": False,
        "derived-indices": False,
    },
}

ENV_VARS: tuple[str, ...] = (
    "CBP_CONTROL_PLANE_IMAGE",
    "CBP_DATA_WORKER_IMAGE",
    "CBP_CONTROL_PLANE_UID",
    "CBP_CONTROL_PLANE_GID",
    "CBP_DATA_WORKER_UID",
    "CBP_DATA_WORKER_GID",
    "CBP_DEPLOYMENT_PROFILE",
)
ENV_EMPTY_REQUIRED = frozenset(ENV_VARS) - {"CBP_DEPLOYMENT_PROFILE"}

EGRESS_CLASSES: tuple[str, ...] = (
    "operating-system-package-and-security-repositories",
    "required-container-registries",
    "dns-services",
    "ntp-services",
    "certificate-renewal-and-revocation-services",
    "explicitly-approved-git-and-artifact-sources",
)

CONTROL_IDS: tuple[str, ...] = tuple(f"KB-{i:02d}" for i in range(1, 13))
FORBIDDEN_CONTROL_STATUS = ("implemented", "tested", "enforced")

SECRET_REF_RE = re.compile(r"\Acbp-secret:v1:file:<opaque-id>\Z")

# --- leakage detection patterns -------------------------------------------

_OCTET = r"(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])"
LEAK_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("ipv4", re.compile(r"(?<![\w.])" + _OCTET + r"(?:\." + _OCTET + r"){3}(?![\w.])")),
    ("ipv6", re.compile(r"(?<![\w:])(?:[0-9a-fA-F]{1,4}:){3,}[0-9a-fA-F]{1,4}(?![\w:])")),
    ("url", re.compile(r"[a-zA-Z][a-zA-Z0-9+.-]*://[^\s\"'<>]+")),
    ("mac", re.compile(r"(?<![\w:])(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}(?![\w:])")),
    ("uuid", re.compile(r"(?i)(?<![\w-])[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
                        r"[0-9a-f]{4}-[0-9a-f]{12}(?![\w-])")),
    ("windows-path", re.compile(r"(?<![\w])[A-Za-z]:[\\/]{1,2}[A-Za-z0-9_.$-]")),
    ("unc-path", re.compile(r"\\\\[A-Za-z0-9_.$-]+\\")),
    ("private-key", re.compile(r"BEGIN\s+(?:[A-Z]+\s+)?PRIVATE\s+KEY")),
    ("password-assignment", re.compile(r"(?i)\b(?:password|passwd|passphrase)\s*[:=]\s*\S")),
    ("token-assignment", re.compile(r"(?i)\b(?:token|api[_-]?key|apikey|access[_-]?key)"
                                    r"\s*[:=]\s*\S")),
    ("bearer", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._-]{4,}")),
    ("aws-key", re.compile(r"(?<![A-Z0-9])AKIA[0-9A-Z]{16}(?![A-Z0-9])")),
    ("numeric-identity", re.compile(r"(?i)\b(?:uid|gid)\s*[:=]\s*[0-9]+")),
)

#: Domain-like tokens are only reported when they are not part of an allowed
#: bundle filename or a documented abstract term.
_DOMAIN_RE = re.compile(r"(?<![\w.-])[a-zA-Z0-9-]{2,}\.(?:com|net|org|io|dev|local|lan|"
                        r"home|internal|de|eu|cloud)(?![\w-])")


@dataclass(frozen=True, slots=True, order=True)
class ValidationIssue:
    """One deterministic, stably sortable bundle finding."""

    code: str
    path: str
    message: str


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Result of a bundle validation run."""

    valid: bool
    issues: tuple[ValidationIssue, ...]


class _Ctx:
    """Collects issues during a run."""

    def __init__(self) -> None:
        self._issues: list[ValidationIssue] = []

    def add(self, code: str, path: str, message: str) -> None:
        self._issues.append(ValidationIssue(code, path, message))

    def sorted(self) -> tuple[ValidationIssue, ...]:
        return tuple(sorted(self._issues))


def _rel(root: Path, p: Path) -> str:
    try:
        return p.relative_to(root).as_posix()
    except ValueError:  # pragma: no cover - defensive
        return p.name


def _read_text(ctx: _Ctx, root: Path, rel: str) -> str | None:
    """Reads a bundle file fail-closed as UTF-8 without BOM."""
    p = root / rel
    try:
        raw = p.read_bytes()
    except OSError:
        ctx.add("BND-FILE-UNREADABLE", rel, "file is not readable")
        return None
    if raw.startswith(b"\xef\xbb\xbf"):
        ctx.add("BND-FILE-BOM", rel, "file starts with a UTF-8 BOM")
        return None
    if b"\x00" in raw:
        ctx.add("BND-FILE-NUL", rel, "file contains a NUL byte")
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        ctx.add("BND-FILE-ENCODING", rel, "file is not valid UTF-8")
        return None
    if not text.strip():
        ctx.add("BND-FILE-EMPTY", rel, "contract file is empty")
        return None
    return text


# --- file set --------------------------------------------------------------


def _check_files(ctx: _Ctx, root: Path) -> None:
    found: set[str] = set()
    for p in sorted(root.rglob("*")):
        rel = _rel(root, p)
        if p.is_symlink():
            ctx.add("BND-FILE-SYMLINK", rel, "symlinks are not allowed in the bundle")
            continue
        if p.is_dir():
            if rel != "config":
                ctx.add("BND-FILE-UNEXPECTED-DIR", rel, "unexpected directory in the bundle")
            continue
        found.add(rel)
    for rel in EXPECTED_FILES:
        if rel not in found:
            ctx.add("BND-FILE-MISSING", rel, "expected bundle file is missing")
    for rel in sorted(found - set(EXPECTED_FILES)):
        ctx.add("BND-FILE-UNEXPECTED", rel, "unexpected file in the bundle")


# --- compose ---------------------------------------------------------------


def _iter_strings(node: object):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield k
            yield from _iter_strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from _iter_strings(v)


def _check_compose(ctx: _Ctx, root: Path) -> None:
    rel = "compose.yaml"
    text = _read_text(ctx, root, rel)
    if text is None:
        return
    try:
        doc = json.loads(text)
    except ValueError:
        ctx.add("BND-COMPOSE-PARSE", rel, "compose file is not parsable as JSON")
        return
    if not isinstance(doc, dict):
        ctx.add("BND-COMPOSE-STRUCTURE", rel, "compose top level is not an object")
        return
    for key in sorted(set(doc) - ALLOWED_TOP_LEVEL):
        ctx.add("BND-COMPOSE-TOPLEVEL", rel, f"unknown top-level section: {key}")

    services = doc.get("services")
    if not isinstance(services, dict):
        ctx.add("BND-COMPOSE-SERVICES-MISSING", rel, "services section is missing")
        return
    for name in SERVICES:
        if name not in services:
            ctx.add("BND-COMPOSE-SERVICE-MISSING", rel, f"required service missing: {name}")
    for name in sorted(set(services) - set(SERVICES)):
        ctx.add("BND-COMPOSE-SERVICE-UNEXPECTED", rel, f"unexpected service: {name}")

    _check_network(ctx, rel, doc)
    _check_config_defs(ctx, rel, doc)

    for name in SERVICES:
        svc = services.get(name)
        if isinstance(svc, dict):
            _check_service(ctx, rel, name, svc)


def _check_network(ctx: _Ctx, rel: str, doc: dict) -> None:
    nets = doc.get("networks")
    if not isinstance(nets, dict) or len(nets) != 1:
        ctx.add("BND-COMPOSE-NETWORK-COUNT", rel, "exactly one network must be defined")
        return
    name, spec = next(iter(nets.items()))
    if name != NETWORK_NAME:
        ctx.add("BND-COMPOSE-NETWORK-NAME", rel, f"unexpected network name: {name}")
    if not isinstance(spec, dict):
        ctx.add("BND-COMPOSE-NETWORK-SPEC", rel, "network specification is not an object")
        return
    if spec.get("internal") is not True:
        ctx.add("BND-COMPOSE-NETWORK-NOT-INTERNAL", rel, "network is not internal")
    for key in ("ipam", "driver_opts", "external", "name"):
        if key in spec:
            ctx.add("BND-COMPOSE-NETWORK-FORBIDDEN", rel, f"forbidden network key: {key}")


def _check_config_defs(ctx: _Ctx, rel: str, doc: dict) -> None:
    cfgs = doc.get("configs")
    if not isinstance(cfgs, dict) or len(cfgs) != 2:
        ctx.add("BND-COMPOSE-CONFIG-COUNT", rel, "exactly two compose configs are required")
        return
    for key, want in (("control-plane-config", "./config/control-plane.example.toml"),
                      ("data-worker-config", "./config/data-worker.example.toml")):
        spec = cfgs.get(key)
        if not isinstance(spec, dict) or spec.get("file") != want:
            ctx.add("BND-COMPOSE-CONFIG-SOURCE", rel, f"config {key} does not reference {want}")


def _check_service(ctx: _Ctx, rel: str, name: str, svc: dict) -> None:
    image = svc.get("image")
    if not isinstance(image, str) or not image.startswith("${"):
        ctx.add("BND-COMPOSE-IMAGE-LITERAL", rel, f"{name}: image must be an operator variable")
    else:
        if ":?" not in image:
            ctx.add("BND-COMPOSE-IMAGE-NOT-REQUIRED", rel,
                    f"{name}: image variable is not fail-closed")
        if ":-" in image:
            ctx.add("BND-COMPOSE-IMAGE-DEFAULT", rel, f"{name}: image variable has a default")

    user = svc.get("user")
    if not isinstance(user, str):
        ctx.add("BND-COMPOSE-USER-MISSING", rel, f"{name}: process identity is missing")
    else:
        low = user.strip().lower()
        if low in {"root", "0", "0:0", '"0"', '"0:0"'}:
            ctx.add("BND-COMPOSE-USER-ROOT", rel, f"{name}: root process identity is forbidden")
        elif re.fullmatch(r"[0-9]+(?::[0-9]+)?", low):
            ctx.add("BND-COMPOSE-USER-NUMERIC", rel,
                    f"{name}: concrete numeric identity is forbidden")
        elif user.count(":?") < 2:
            ctx.add("BND-COMPOSE-USER-NOT-REQUIRED", rel,
                    f"{name}: identity is not fail-closed for UID and GID")
        if ":-" in user:
            ctx.add("BND-COMPOSE-USER-DEFAULT", rel, f"{name}: identity variable has a default")

    if svc.get("read_only") is not True:
        ctx.add("BND-COMPOSE-READONLY", rel, f"{name}: read_only must be true")
    if svc.get("privileged") is True:
        ctx.add("BND-COMPOSE-PRIVILEGED", rel, f"{name}: privileged is forbidden")
    if svc.get("restart") != "no":
        ctx.add("BND-COMPOSE-RESTART", rel, f"{name}: restart must be no")
    caps = svc.get("cap_drop")
    if not isinstance(caps, list) or "ALL" not in caps:
        ctx.add("BND-COMPOSE-CAPDROP", rel, f"{name}: cap_drop must contain ALL")
    opts = svc.get("security_opt")
    if not isinstance(opts, list) or "no-new-privileges:true" not in opts:
        ctx.add("BND-COMPOSE-NONEWPRIV", rel, f"{name}: no-new-privileges:true is required")

    for key, code in (("network_mode", "BND-COMPOSE-HOST-NETWORK"),
                      ("pid", "BND-COMPOSE-HOST-PID"),
                      ("ipc", "BND-COMPOSE-HOST-IPC")):
        val = svc.get(key)
        if isinstance(val, str) and val.startswith("host"):
            ctx.add(code, rel, f"{name}: host namespace {key} is forbidden")
        elif key == "network_mode" and val is not None:
            ctx.add(code, rel, f"{name}: network_mode is forbidden")
    if svc.get("ports"):
        ctx.add("BND-COMPOSE-PORTS", rel, f"{name}: publishing ports is forbidden")
    if svc.get("devices"):
        ctx.add("BND-COMPOSE-DEVICES", rel, f"{name}: device access is forbidden")

    tmpfs = svc.get("tmpfs")
    if not isinstance(tmpfs, list) or not tmpfs:
        ctx.add("BND-COMPOSE-TMPFS", rel, f"{name}: a tmpfs for transient data is required")

    nets = svc.get("networks")
    if nets != [NETWORK_NAME]:
        ctx.add("BND-COMPOSE-SERVICE-NETWORK", rel,
                f"{name}: only the internal Profile-A network is allowed")

    _check_volumes(ctx, rel, name, svc)
    _check_service_configs(ctx, rel, name, svc)


def _check_volumes(ctx: _Ctx, rel: str, name: str, svc: dict) -> None:
    vols = svc.get("volumes")
    if not isinstance(vols, list):
        ctx.add("BND-COMPOSE-VOLUMES", rel, f"{name}: volumes must be a list")
        return
    seen: dict[str, bool] = {}
    for entry in vols:
        if not isinstance(entry, dict):
            ctx.add("BND-COMPOSE-VOLUME-SYNTAX", rel,
                    f"{name}: only the long volume syntax is allowed")
            continue
        vtype = entry.get("type")
        src = entry.get("source")
        tgt = entry.get("target")
        if vtype != "volume":
            ctx.add("BND-COMPOSE-BIND-MOUNT", rel,
                    f"{name}: only named volumes are allowed, found type {vtype}")
            continue
        if not isinstance(src, str) or not isinstance(tgt, str):
            ctx.add("BND-COMPOSE-VOLUME-SYNTAX", rel, f"{name}: volume source or target missing")
            continue
        if src in FORBIDDEN_AREAS or "backup" in src or src.startswith("rt2"):
            ctx.add("BND-COMPOSE-FORBIDDEN-AREA", rel, f"{name}: forbidden area mounted: {src}")
            continue
        if src.startswith("/") or src.startswith(".") or ":" in src:
            ctx.add("BND-COMPOSE-HOST-PATH", rel, f"{name}: host paths are forbidden")
            continue
        if "docker.sock" in tgt or "docker.sock" in src:
            ctx.add("BND-COMPOSE-DOCKER-SOCKET", rel, f"{name}: the Docker socket is forbidden")
            continue
        if tgt not in ALLOWED_CONTAINER_PATHS:
            ctx.add("BND-COMPOSE-TARGET-PATH", rel, f"{name}: target path not allowed: {tgt}")
        seen[src] = bool(entry.get("read_only"))

    expected = MOUNTS[name]
    for src, want_ro in expected.items():
        if src not in seen:
            ctx.add("BND-COMPOSE-MOUNT-MISSING", rel, f"{name}: required area not mounted: {src}")
        elif seen[src] != want_ro:
            mode = "read-only" if want_ro else "read-write"
            ctx.add("BND-COMPOSE-MOUNT-MODE", rel, f"{name}: {src} must be {mode}")
    for src in sorted(set(seen) - set(expected)):
        ctx.add("BND-COMPOSE-MOUNT-UNEXPECTED", rel, f"{name}: area must not be mounted: {src}")


def _check_service_configs(ctx: _Ctx, rel: str, name: str, svc: dict) -> None:
    cfgs = svc.get("configs")
    want_src = f"{name}-config"
    want_tgt = f"/etc/cbp/{name}.toml"
    if not isinstance(cfgs, list) or len(cfgs) != 1 or not isinstance(cfgs[0], dict):
        ctx.add("BND-COMPOSE-CONFIG-MOUNT", rel, f"{name}: exactly one config must be mounted")
        return
    entry = cfgs[0]
    if entry.get("source") != want_src or entry.get("target") != want_tgt:
        ctx.add("BND-COMPOSE-CONFIG-TARGET", rel, f"{name}: config source or target is wrong")
    mode = entry.get("mode")
    if not isinstance(mode, int) or mode & 0o222:
        ctx.add("BND-COMPOSE-CONFIG-WRITABLE", rel, f"{name}: config must be mounted read-only")


# --- bundle.json -----------------------------------------------------------


def _check_contract(ctx: _Ctx, root: Path) -> None:
    rel = "bundle.json"
    text = _read_text(ctx, root, rel)
    if text is None:
        return
    try:
        doc = json.loads(text)
    except ValueError:
        ctx.add("BND-CONTRACT-PARSE", rel, "bundle contract is not valid JSON")
        return
    if not isinstance(doc, dict):
        ctx.add("BND-CONTRACT-STRUCTURE", rel, "bundle contract top level is not an object")
        return
    canonical = json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if text != canonical:
        ctx.add("BND-DETERMINISM-CANONICAL", rel, "bundle contract is not canonically formatted")

    for key, want in (("schema_id", "cbp-profile-a-deployment-bundle"),
                      ("deployment_profile", "A"),
                      ("target_state", "Z1"),
                      ("scope", "S2"),
                      ("rt2_boundary", "P1"),
                      ("status", "offline-template"),
                      ("deployed", False),
                      ("runtime_started", False)):
        if doc.get(key) != want:
            ctx.add("BND-CONTRACT-IDENTITY", rel, f"{key} must be {want!r}")
    if not isinstance(doc.get("contract_revision"), str) or not doc.get("contract_revision"):
        ctx.add("BND-CONTRACT-IDENTITY", rel, "contract_revision is missing")

    files = doc.get("files")
    if list(EXPECTED_FILES) != (sorted(files) if isinstance(files, list) else None):
        ctx.add("BND-CONTRACT-FILES", rel, "file list must contain exactly the seven bundle files")
    if isinstance(files, list):
        for f in files:
            if not isinstance(f, str) or f.startswith("/") or "\\" in f or ".." in f:
                ctx.add("BND-CONTRACT-FILES", rel, "file list must use relative POSIX paths")

    _check_contract_services(ctx, rel, doc)
    _check_contract_areas(ctx, rel, doc)
    _check_contract_egress(ctx, rel, doc)
    _check_contract_secret(ctx, rel, doc)
    _check_contract_backup(ctx, rel, doc)
    _check_contract_rt2(ctx, rel, doc)
    _check_contract_controls(ctx, rel, doc)
    _check_contract_gates(ctx, rel, doc)


def _check_contract_services(ctx: _Ctx, rel: str, doc: dict) -> None:
    services = doc.get("services")
    if not isinstance(services, dict) or set(services) != set(SERVICES):
        ctx.add("BND-CONTRACT-SERVICES", rel, "contract must describe exactly two services")
        return
    for name in SERVICES:
        svc = services[name]
        if not isinstance(svc, dict):
            ctx.add("BND-CONTRACT-SERVICES", rel, f"{name}: service entry is not an object")
            continue
        if svc.get("service_identity") != IDENTITIES[name]:
            ctx.add("BND-CONTRACT-IDENTITY-MISMATCH", rel,
                    f"{name}: logical service identity is wrong")
        for key in ("administrative_access", "publish_rights",
                    "backup_storage_access", "rt2_direct_access"):
            if svc.get(key) is not False:
                ctx.add("BND-CONTRACT-PRIVILEGE", rel, f"{name}: {key} must be false")
        allowed = svc.get("allowed_areas")
        if not isinstance(allowed, dict) or not allowed:
            ctx.add("BND-CONTRACT-AREAS", rel, f"{name}: allowed_areas is missing")
        elif {k: v == "read-only" for k, v in allowed.items()} != MOUNTS[name]:
            ctx.add("BND-CONTRACT-AREAS", rel, f"{name}: allowed_areas do not match the mounts")
        if not isinstance(svc.get("forbidden_areas"), list) or not svc.get("forbidden_areas"):
            ctx.add("BND-CONTRACT-AREAS", rel, f"{name}: forbidden_areas is missing")


def _check_contract_areas(ctx: _Ctx, rel: str, doc: dict) -> None:
    areas = doc.get("data_areas")
    required = {"canonical-data", "source-registry", "mapping-registry", "quarantine",
                "released-artifacts", "derived-indices", "runtime-transient",
                "rt2-operational-evidence"}
    if not isinstance(areas, dict) or not required <= set(areas):
        ctx.add("BND-CONTRACT-DATA-AREAS", rel, "data area contract is incomplete")
        return
    fields = ("owner", "consumer", "mode", "kind", "persisted", "backup_required",
              "restore_required", "rebuildable", "secret_risk")
    for name in sorted(required):
        spec = areas[name]
        if not isinstance(spec, dict):
            ctx.add("BND-CONTRACT-DATA-AREAS", rel, f"{name}: area entry is not an object")
            continue
        for f in fields:
            if f not in spec:
                ctx.add("BND-CONTRACT-DATA-AREAS", rel, f"{name}: missing field {f}")
    if areas.get("runtime-transient", {}).get("rt_class") != "RT-3":
        ctx.add("BND-CONTRACT-DATA-AREAS", rel, "runtime-transient must be RT-3")
    if areas.get("rt2-operational-evidence", {}).get("mode") != "contract-only":
        ctx.add("BND-CONTRACT-DATA-AREAS", rel, "RT-2 area must be contract-only")


def _check_contract_egress(ctx: _Ctx, rel: str, doc: dict) -> None:
    eg = doc.get("egress")
    if not isinstance(eg, dict):
        ctx.add("BND-CONTRACT-EGRESS", rel, "egress contract is missing")
        return
    if eg.get("default") != "deny":
        ctx.add("BND-CONTRACT-EGRESS-DEFAULT", rel, "egress default must be deny")
    if eg.get("wildcards_allowed") is not False:
        ctx.add("BND-CONTRACT-EGRESS-WILDCARD", rel, "egress wildcards must be forbidden")
    if eg.get("concrete_endpoints") is not False:
        ctx.add("BND-CONTRACT-EGRESS-ENDPOINT", rel, "concrete egress endpoints are forbidden")
    if eg.get("enforced") is not False:
        ctx.add("BND-CONTRACT-EGRESS", rel, "egress must not be declared as enforced")
    classes = eg.get("target_classes")
    if not isinstance(classes, list) or len(classes) != 6:
        ctx.add("BND-CONTRACT-EGRESS-COUNT", rel, "exactly six egress target classes are required")
    elif list(classes) != list(EGRESS_CLASSES):
        ctx.add("BND-CONTRACT-EGRESS-CLASSES", rel, "egress target classes do not match")
    if isinstance(classes, list):
        for c in classes:
            if isinstance(c, str) and "*" in c:
                ctx.add("BND-CONTRACT-EGRESS-WILDCARD", rel, "wildcard in egress class")
    if eg.get("change_authority") != "human-maintainer":
        ctx.add("BND-CONTRACT-EGRESS", rel, "egress change authority must be human-maintainer")


def _check_contract_secret(ctx: _Ctx, rel: str, doc: dict) -> None:
    sec = doc.get("secret_provider")
    if not isinstance(sec, dict):
        ctx.add("BND-CONTRACT-SECRET", rel, "secret provider contract is missing")
        return
    if sec.get("provider_type") != "file":
        ctx.add("BND-CONTRACT-SECRET-PROVIDER", rel, "secret provider type must be file")
    if not isinstance(sec.get("provider_class"), str) or not sec.get("provider_class"):
        ctx.add("BND-CONTRACT-SECRET", rel, "secret provider class is missing")
    ref = sec.get("reference_syntax")
    if not isinstance(ref, str) or not SECRET_REF_RE.match(ref):
        ctx.add("BND-CONTRACT-SECRET-SYNTAX", rel, "secret reference syntax is invalid")
    for key in ("unknown_provider_blocks", "missing_reference_blocks"):
        if sec.get(key) is not True:
            ctx.add("BND-CONTRACT-SECRET", rel, f"{key} must be true")
    for key in ("values_in_bundle", "values_in_logs"):
        if sec.get(key) is not False:
            ctx.add("BND-CONTRACT-SECRET", rel, f"{key} must be false")


def _check_contract_backup(ctx: _Ctx, rel: str, doc: dict) -> None:
    bk = doc.get("backup")
    if not isinstance(bk, dict):
        ctx.add("BND-CONTRACT-BACKUP", rel, "backup contract is missing")
        return
    for key, want in (("vm_backup_interval", "weekly"),
                      ("canonical_data_interval", "daily"),
                      ("rpo_hours", 24), ("rto_hours", 8),
                      ("job_implemented", False),
                      ("cbp_restore_evidence", False),
                      ("rt2_restore_evidence", False)):
        if bk.get(key) != want:
            ctx.add("BND-CONTRACT-BACKUP", rel, f"{key} must be {want!r}")
    if not isinstance(bk.get("target_class"), str) or not bk.get("target_class"):
        ctx.add("BND-CONTRACT-BACKUP", rel, "abstract backup target class is missing")


def _check_contract_rt2(ctx: _Ctx, rel: str, doc: dict) -> None:
    rt2 = doc.get("rt2")
    if not isinstance(rt2, dict):
        ctx.add("BND-CONTRACT-RT2", rel, "RT-2 contract is missing")
        return
    if rt2.get("boundary") != "P1" or rt2.get("mode") != "contract-only":
        ctx.add("BND-CONTRACT-RT2-BOUNDARY", rel, "RT-2 must be P1 and contract-only")
    for key in ("storage", "events", "hash_chaining", "retention_engine",
                "backup", "restore", "automatic_deletion", "separate_archive"):
        if rt2.get(key) is not False:
            ctx.add("BND-CONTRACT-RT2-IMPLEMENTED", rel, f"RT-2 {key} must be false")
    if rt2.get("minimum_retention_days") != 365:
        ctx.add("BND-CONTRACT-RT2", rel, "RT-2 minimum retention must be 365 days")
    if rt2.get("after_minimum") != "permanent":
        ctx.add("BND-CONTRACT-RT2", rel, "RT-2 retention after minimum must be permanent")


def _check_contract_controls(ctx: _Ctx, rel: str, doc: dict) -> None:
    controls = doc.get("security_controls")
    if not isinstance(controls, dict) or set(controls) != set(CONTROL_IDS):
        ctx.add("BND-CONTRACT-CONTROLS", rel, "exactly KB-01 to KB-12 must be listed")
        return
    for cid in CONTROL_IDS:
        spec = controls[cid]
        status = spec.get("status") if isinstance(spec, dict) else None
        if status != "DOCUMENTED ONLY":
            ctx.add("BND-CONTRACT-CONTROL-STATUS", rel,
                    f"{cid}: status must be DOCUMENTED ONLY")
        if isinstance(status, str) and status.strip().lower() in FORBIDDEN_CONTROL_STATUS:
            ctx.add("BND-CONTRACT-CONTROL-FORBIDDEN", rel,
                    f"{cid}: forbidden control status")


def _check_contract_gates(ctx: _Ctx, rel: str, doc: dict) -> None:
    caps = doc.get("capabilities")
    if not isinstance(caps, dict) or caps.get("implemented") != 0 or caps.get("total") != 29:
        ctx.add("BND-CONTRACT-CAPABILITIES", rel, "capabilities must be 0 of 29")
    gates = doc.get("gates")
    if not isinstance(gates, dict):
        ctx.add("BND-CONTRACT-GATES", rel, "gate contract is missing")
    else:
        for key in ("mapping_activation_gate", "security_foundation_readiness_gate"):
            if gates.get(key) != "NOT EVALUATED":
                ctx.add("BND-CONTRACT-GATE-STATUS", rel, f"{key} must be NOT EVALUATED")
    nt = doc.get("security_negative_tests")
    if not isinstance(nt, dict) or nt.get("executed") != 0 or nt.get("total") != 32:
        ctx.add("BND-CONTRACT-NEGATIVE-TESTS", rel, "security negative tests must be 0 of 32")
    risks = doc.get("risks")
    if not isinstance(risks, dict) or risks.get("R-20") != "open":
        ctx.add("BND-CONTRACT-RISK", rel, "R-20 must remain open")


# --- TOML ------------------------------------------------------------------


def _check_toml(ctx: _Ctx, root: Path) -> None:
    for name in SERVICES:
        rel = f"config/{name}.example.toml"
        text = _read_text(ctx, root, rel)
        if text is None:
            continue
        try:
            doc = tomllib.loads(text)
        except tomllib.TOMLDecodeError:
            ctx.add("BND-CONFIG-PARSE", rel, "configuration template is not valid TOML")
            continue
        allowed = {"contract_revision", "deployment_profile", "service_identity",
                   "compose_service", "mode", "egress", "secrets", "rt2",
                   "activation", "access", "privileges"}
        for key in sorted(set(doc) - allowed):
            ctx.add("BND-CONFIG-TOPLEVEL", rel, f"unknown contract section: {key}")
        if doc.get("deployment_profile") != "A":
            ctx.add("BND-CONFIG-PROFILE", rel, "deployment profile must be A")
        if doc.get("service_identity") != IDENTITIES[name]:
            ctx.add("BND-CONFIG-IDENTITY", rel, "logical service identity is wrong")
        if doc.get("compose_service") != name:
            ctx.add("BND-CONFIG-IDENTITY", rel, "compose service name is wrong")
        if doc.get("mode") != "offline-template":
            ctx.add("BND-CONFIG-MODE", rel, "mode must be offline-template")
        if not isinstance(doc.get("contract_revision"), str) or not doc.get("contract_revision"):
            ctx.add("BND-CONFIG-REVISION", rel, "contract revision is missing")

        eg = doc.get("egress", {})
        if eg.get("mode") != "deny-by-default":
            ctx.add("BND-CONFIG-EGRESS", rel, "egress mode must be deny-by-default")
        sec = doc.get("secrets", {})
        if sec.get("provider_type") != "file":
            ctx.add("BND-CONFIG-SECRET-PROVIDER", rel, "secret provider must be file")
        for key in ("reference_syntax", "example_reference"):
            val = sec.get(key)
            if not isinstance(val, str) or not SECRET_REF_RE.match(val):
                ctx.add("BND-CONFIG-SECRET-SYNTAX", rel, f"{key} is not the synthetic reference")
        if sec.get("values_in_bundle") is not False:
            ctx.add("BND-CONFIG-SECRET-VALUE", rel, "secret values must not be declared")

        rt2 = doc.get("rt2", {})
        if rt2.get("mode") != "contract-only":
            ctx.add("BND-CONFIG-RT2", rel, "RT-2 mode must be contract-only")
        if rt2.get("implemented") is not False:
            ctx.add("BND-CONFIG-RT2-IMPLEMENTED", rel, "RT-2 must not be marked implemented")

        act = doc.get("activation", {})
        for key in ("automatic_activation", "real_source_bound", "productive_mapping"):
            if act.get(key) is not False:
                ctx.add("BND-CONFIG-ACTIVATION", rel, f"{key} must be false")

        access = doc.get("access", {})
        # Area names use hyphens in the contract and underscores as TOML keys.
        expected = {a.replace("-", "_"): ("read-only" if ro else "read-write")
                    for a, ro in MOUNTS[name].items()}
        for a, want in expected.items():
            if access.get(a) != want:
                ctx.add("BND-CONFIG-ACCESS", rel, f"{a} must be {want}")
        for a in ("backup_storage", "rt2_direct"):
            if access.get(a) != "none":
                ctx.add("BND-CONFIG-ACCESS", rel, f"{a} must be none")
        priv = doc.get("privileges", {})
        for key in ("administrative_access", "publish_rights"):
            if priv.get(key) is not False:
                ctx.add("BND-CONFIG-PRIVILEGE", rel, f"{key} must be false")


# --- operator environment --------------------------------------------------


def _check_env(ctx: _Ctx, root: Path) -> None:
    rel = "operator.env.example"
    text = _read_text(ctx, root, rel)
    if text is None:
        return
    seen: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "=" not in s:
            ctx.add("BND-ENV-SYNTAX", rel, "line is not a variable assignment")
            continue
        key, _, value = s.partition("=")
        key = key.strip()
        seen.append(key)
        if key not in ENV_VARS:
            ctx.add("BND-ENV-UNEXPECTED", rel, f"unexpected variable: {key}")
            continue
        if key in ENV_EMPTY_REQUIRED and value.strip():
            ctx.add("BND-ENV-PREFILLED", rel, f"required value must stay empty: {key}")
        if key == "CBP_DEPLOYMENT_PROFILE" and value.strip() != "A":
            ctx.add("BND-ENV-PROFILE", rel, "deployment profile must be A")
        if key.endswith(("_UID", "_GID")) and value.strip():
            ctx.add("BND-ENV-NUMERIC-IDENTITY", rel, f"concrete identity is forbidden: {key}")
    for key in ENV_VARS:
        if key not in seen:
            ctx.add("BND-ENV-MISSING", rel, f"required variable missing: {key}")
        elif seen.count(key) > 1:
            ctx.add("BND-ENV-DUPLICATE", rel, f"variable defined more than once: {key}")


# --- leakage ---------------------------------------------------------------


def _check_leakage(ctx: _Ctx, root: Path) -> None:
    for rel in EXPECTED_FILES:
        if rel in LEAKAGE_EXEMPT:
            continue
        p = root / rel
        if not p.is_file() or p.is_symlink():
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for label, pattern in LEAK_PATTERNS:
            if pattern.search(text):
                ctx.add("BND-LEAK-" + label.upper().replace("-", "-"), rel,
                        f"forbidden {label} pattern found")
        for m in _DOMAIN_RE.finditer(text):
            token = m.group(0)
            if token in EXPECTED_FILES or token.endswith((".md", ".py", ".json",
                                                          ".toml", ".yaml", ".example")):
                continue
            ctx.add("BND-LEAK-DOMAIN", rel, "forbidden domain-like token found")


# --- public API ------------------------------------------------------------


def validate_bundle(root: Path) -> ValidationReport:
    """Validates the Profile-A bundle at ``root`` deterministically and offline."""
    ctx = _Ctx()
    if not root.exists():
        ctx.add("BND-FILE-ROOT-MISSING", ".", "bundle root does not exist")
        return ValidationReport(False, ctx.sorted())
    if not root.is_dir():
        ctx.add("BND-FILE-ROOT-NOT-DIR", ".", "bundle root is not a directory")
        return ValidationReport(False, ctx.sorted())

    _check_files(ctx, root)
    if (root / "compose.yaml").is_file():
        _check_compose(ctx, root)
    if (root / "bundle.json").is_file():
        _check_contract(ctx, root)
    _check_toml(ctx, root)
    if (root / "operator.env.example").is_file():
        _check_env(ctx, root)
    _check_leakage(ctx, root)

    issues = ctx.sorted()
    return ValidationReport(not issues, issues)


def main(argv: list[str]) -> int:
    """CLI entry point. Exit codes: 0 valid, 1 invalid, 2 invalid call."""
    if len(argv) > 1:
        sys.stderr.write("usage: validate.py [bundle-root]\n")
        return 2
    root = Path(argv[0]) if argv else Path(__file__).resolve().parent
    try:
        report = validate_bundle(root)
    except OSError:
        sys.stderr.write("error: bundle could not be read\n")
        return 2
    if report.valid:
        sys.stdout.write("PROFILE-A-BUNDLE VALID\nissues=0\n")
        return 0
    lines = [f"PROFILE-A-BUNDLE INVALID", f"issues={len(report.issues)}"]
    lines.extend(f"{i.code} | {i.path} | {i.message}" for i in report.issues)
    sys.stdout.write("\n".join(lines) + "\n")
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
