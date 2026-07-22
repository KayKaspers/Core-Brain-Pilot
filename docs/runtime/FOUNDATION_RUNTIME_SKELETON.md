# Foundation Runtime Skeleton

| Feld | Wert |
| --- | --- |
| **Status** | **IMPLEMENTED LOCALLY** — lokal, fail-closed, **nicht produktionsbereit** |
| **Nicht** | DEPLOYED · PRODUCTION READY · SECURITY FOUNDATION IMPLEMENTED |
| Grundlage | **ADR-0009** (A1), ADR-0007, ADR-0008; TECHNICAL_SECURITY_FOUNDATION_SPECIFICATION |
| Erfasst in | CBP-WP-012 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

> **Dieser Skeleton führt keine operative Verarbeitung aus.** Er bindet keine
> Quelle an, löst kein Secret auf, öffnet keine Verbindung und schreibt keinen
> RT-2-Nachweis. Das Kommando `run` verweigert deterministisch.
>
> **CBP-WP-013** ergänzt auf diesem Skeleton die Kommandogruppe `quarantine`
> (`scan`, `stage`, `inspect`, `release`) — ein lokaler, synthetisch testbarer
> Quarantäneprototyp. Siehe [INGEST_QUARANTINE_MVP.md](INGEST_QUARANTINE_MVP.md).

---

## Zweck

Der Skeleton ist das **erste Artefakt mit technischer Wirkung** im Projekt. Er
belegt lokal und reproduzierbar, dass die fail-closed Grundsätze aus ADR-0009
als ausführbarer, getesteter Code existieren — **ohne** eine Kontrolle KB-01
bis KB-12 als durchgesetzt zu behaupten.

## Struktur

Additiv begonnen (D-029, ADR-0007). **Keine bestehende Datei wurde
verschoben.**

```text
pyproject.toml                     # Projektmetadaten, requires-python >=3.13
core/
  __init__.py                      # Namensraum, ohne Nebenwirkung
  core_brain/
    __init__.py                    # Version, Modus, production_ready = False
    __main__.py                    # py -3.13 -m core.core_brain
    cli.py                         # version · validate-config · doctor · run
    config.py                      # strikte, fail-closed Validierung
    models.py                      # unveränderliche Datenmodelle
    policies.py                    # reine Policy-Funktionen
    ports.py                       # Protokolle + verweigernde Defaults
    errors.py                      # Fehler, Exit- und Reason-Codes
config/
  runtime.example.toml             # synthetisch, non-operational, test-only
examples/
  README.md                        # Kennzeichnung der Beispiele
tests/
  __init__.py
  test_config.py · test_policies.py · test_ports.py · test_cli.py
docs/runtime/
  FOUNDATION_RUNTIME_SKELETON.md   # dieses Dokument
  FOUNDATION_RUNTIME_EVIDENCE.md   # Testlauf und Smoke-Tests
  DEVELOPER_RUNBOOK.md             # PowerShell-Befehle
```

## Komponenten

| Modul | Verantwortung | Grenze |
| --- | --- | --- |
| `errors` | Exit- und Reason-Codes, Fehlertypen | keine Logik |
| `models` | unveränderliche Konfiguration und Berichte | keine I/O |
| `config` | strikte Validierung, fail-closed | liest **nur** die angegebene Datei; **nie** Environment oder `sys.argv` |
| `policies` | reine Prüfungen KB-01…KB-10 + Runtime-Start | seiteneffektfrei |
| `ports` | vier Protokolle, verweigernde Defaults | kein Netzwerk, kein Secret, kein RT-2 |
| `cli` | vier Kommandos, deterministische Ausgabe | keine HTTP-API |

## Trust Boundaries

Der Skeleton realisiert **nur logische** Grenzen aus ADR-0009:

| Grenze | Im Skeleton |
| --- | --- |
| **TB-C** Control Plane / Data Worker | zwei **logische** Identitäten in der Konfiguration; getrennt geprüft (KB-02). **Keine OS-Identität angelegt** |
| **TB-F** Secret Store / übrige | `SecretResolver`-Port; Default **verweigert** jede Auflösung |
| **TB-G** intern / extern | `EgressDecisionPort`; Default **verweigert** jeden Egress |
| RT-2-Grenze | `OperationalEvidenceWriter`-Port; Default **verweigert** jedes Anfügen |

## Implementierte Skeleton-Grenzen

| Grenze | Umsetzung | Testbeleg |
| --- | --- | --- |
| Strikte Konfigurationsvalidierung | `config.parse_config_mapping` | `test_config.py` |
| Fail-closed Defaults | restriktive Werte erzwungen | `test_config.py` |
| Getrennte Identitäten | `policies.check_identity_separation` | `test_policies.py` |
| Root-Guard | `policies.check_not_privileged` | `test_policies.py` |
| Canonical Write verboten | `policies.check_canonical_write_blocked` | `test_policies.py` |
| Source-Aktivierung blockiert | `policies.check_source_activation_blocked` | `test_policies.py` |
| Egress deny-by-default | `policies.check_egress_deny_by_default` | `test_policies.py` |
| Verweigernde Ports | vier Default-Ports | `test_ports.py` |
| Fail-closed CLI-Start | `run` verweigert | `test_cli.py` |
| **Netzwerkfreiheit der CLI-Pfade** | ausführbarer Netzwerk-Guard | `test_cli.py::TestNetworkGuard` |

### Netzwerk-Guard

`TestNetworkGuard` ersetzt `socket.create_connection`, `socket.socket.connect`,
`socket.socket.connect_ex` und `socket.getaddrinfo` durch verweigernde
Funktionen und führt darunter alle fünf CLI-Pfade aus. Ein Verbindungs- oder
DNS-Versuch würde den Test scheitern lassen; eine Gegenprobe belegt, dass der
Guard wirksam ist.

> **Aussagegrenze:** Der Guard belegt Netzwerkfreiheit **dieser lokalen
> CLI-Pfade in-process** — **nicht** Deployment-Isolation, Firewallwirkung,
> Container-Netzgrenzen, VM-Egress-Kontrolle oder allgemeine
> Systemnetzwerkfreiheit.

## Ausdrücklich NICHT implementierte Kontrollen

**Keine Kontrolle KB-01 bis KB-12 aus ADR-0009 ist durchgesetzt.** Sie bleiben
**DOCUMENTED ONLY**. Der Skeleton implementiert **nicht**:

- Source Mapping, Ingest, Retrieval, Indexierung,
- Secret-Auflösung (der Resolver verweigert),
- Netzwerkzugriff oder eine Egress-Allowlist,
- RT-2-Speicherung (der Writer verweigert),
- API, Webserver oder Web UI,
- OS-Identitäten, UID/GID, Mount-Modi, Dateisystemrechte,
- Container- oder VM-Deployment,
- die Ausführung eines Gates.

> **Ein `PASS` im Doctor ist ein Skeleton-Ergebnis, kein Deploymentnachweis.**
> KB-01 wird auf Windows als `NOT APPLICABLE` gemeldet — der reale Nachweis
> entsteht auf der Ziel-Linux-VM.

## Exitcodes

| Name | Wert | Bedeutung |
| --- | --- | --- |
| `OK` | **0** | Kommando erfolgreich |
| `CONFIG_INVALID` | **2** | Konfiguration ungültig |
| `POLICY_BLOCKED` | **3** | Doctor meldet mindestens ein `BLOCKED` |
| `RUNTIME_START_BLOCKED` | **4** | `run` verweigert fail-closed |
| `USAGE_ERROR` | **64** | Falsche Kommandozeile |
| `INTERNAL_ERROR` | **70** | Unerwarteter Fehler |

Die Werte sind stabil und werden nach dieser Dokumentation nicht verändert.

## Konfigurationsmodell

TOML, **eine** Schema-Version (`1.0`). Elf Pflichtfelder, keine optionalen.

| Feld | Vorgabe im Skeleton | Regel |
| --- | --- | --- |
| `schema_version` | `"1.0"` | andere Version blockiert |
| `runtime_mode` | `"skeleton"` | nur dieser Wert |
| `control_plane_identity` | `"control-plane"` | nicht `root`/`administrator`/`system` |
| `data_worker_identity` | `"data-worker"` | ≠ Control Plane |
| `egress_default` | `"deny"` | nur `deny` |
| `canonical_write_allowed` | `false` | `true` blockiert |
| `source_activation_enabled` | `false` | `true` blockiert |
| `mapping_gate_status` | `"NOT EVALUATED"` | Statuswert |
| `security_gate_status` | `"NOT EVALUATED"` | Statuswert |
| `secret_provider_status` | `"unconfigured"` | Statuswert |
| `evidence_writer_status` | `"unconfigured"` | Statuswert |

**Fail-closed:** unbekanntes Feld → blockiert · unbekannte Version → blockiert ·
fehlendes Pflichtfeld → blockiert · unzulässiger Wert → blockiert.
**Environment und CLI überschreiben keinen Sicherheitswert.**

## Ports

| Port | Default | Verhalten |
| --- | --- | --- |
| `SecretResolver` | `DenyingSecretResolver` | verweigert; nennt die Referenz **nicht** |
| `OperationalEvidenceWriter` | `DenyingEvidenceWriter` | verweigert jedes Anfügen |
| `EgressDecisionPort` | `DenyingEgressPort` | verweigert jeden Egress |
| `RuntimeStatusProvider` | `SkeletonRuntimeStatusProvider` | meldet dauerhaft `production_ready = False` |

## Stop-Bedingungen

Die Stop-Bedingungen aus
[PHASE_1_STOP_CONDITIONS.md](../roadmap/PHASE_1_STOP_CONDITIONS.md) und der
Sicherheitsspezifikation gelten fort. Für den Skeleton besonders relevant:

| Auslöser | Verhalten |
| --- | --- |
| Konfiguration verlangt Canonical Write oder Source-Aktivierung | **blockiert** (SB-01, SB-06-Nähe) |
| Egress ungleich `deny` | **blockiert** |
| Secret-Wert in einem Feld | Validierung blockiert; kein Wert im Log |
| Versuch, `run` produktiv zu starten | **verweigert** (SB-S15-Nähe: Skeleton statt Kontrolle) |
| Prozess als root (POSIX) | **blockiert** |

## Status

**IMPLEMENTED LOCALLY.** Ausführbar, getestet, fail-closed. **Nicht
produktionsbereit.** Security Foundation Readiness Gate, Mapping Activation
Gate und DRC bleiben `NOT EVALUATED`.
