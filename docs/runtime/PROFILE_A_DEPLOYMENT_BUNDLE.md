# Profile-A Deployment Bundle — Runtime Contract

| Feld | Wert |
| --- | --- |
| **Vertragsstatus** | **repository artifact implemented** · **offline validation implemented** · **offline validation passed** |
| **Nicht** | deployed · operational · production-ready |
| Erfasst in | **CBP-WP-020** (D-055) |
| Autoritätsklasse | A2 |
| Zielzustand | **Z1** · Scope **S2** · RT-2-Grenze **P1** |
| Stand | 2026-07-29 |

> **Dieses Dokument beschreibt eine Vorlage, kein laufendes System.** Es wurde
> nichts installiert, gestartet, verbunden oder durchgesetzt.

---

## Dateibaum

**Bundle — exakt sieben Dateien:**

```text
deployments/profile-a/
├── README.md
├── bundle.json
├── compose.yaml
├── operator.env.example
├── validate.py
└── config/
    ├── control-plane.example.toml
    └── data-worker.example.toml
```

**Drei externe Runbooks** (bewusst **nicht** im Bundle):

```text
docs/operations/PROFILE_A_INSTALLATION_RUNBOOK.md
docs/operations/PROFILE_A_VALIDATION_RUNBOOK.md
docs/operations/PROFILE_A_ROLLBACK_RUNBOOK.md
```

## Compose-Vertrag

**JSON-kompatible YAML-Teilmenge.** JSON ist gültiges YAML; Docker Compose kann
`compose.yaml` unverändert lesen, und der Offline-Validator liest dieselbe Datei
deterministisch mit `json.loads`. Das ist eine **reversible
Implementierungsentscheidung**, **keine neue Architekturbindung**.

**Zwei getrennte Services** mit getrennten logischen Identitäten:

| Compose-Service | Logische Identität | Approval | Publish | Admin |
| --- | --- | --- | --- | --- |
| `control-plane` | `svc-control-plane` | ja | **nein** | **nein** |
| `data-worker` | `svc-data-worker` | **nein** | **nein** | **nein** |

**Härtungsvorlage je Service:** `read_only: true` · `cap_drop: [ALL]` ·
`security_opt: [no-new-privileges:true]` · `privileged: false` ·
`restart: "no"` · eigenes `tmpfs` · ausschließlich das interne Profil-A-Netz.

**Prozessidentität:** ausschließlich über **fail-closed Operatorvariablen**
(`${...:?...}`) für UID **und** GID. **Kein Root-Literal, keine numerische
Identität, kein Default.**

**Images:** ausschließlich fail-closed Operatorvariablen. **Keine Registry,
Domain, URL oder `latest`.**

### Mountmatrix

| Bereich | `control-plane` | `data-worker` |
| --- | --- | --- |
| `canonical-data` | **read-only** | **read-only** |
| `source-registry` | read-write | read-only |
| `mapping-registry` | read-write | read-only |
| `released-artifacts` | read-write | **nicht gemountet** |
| `quarantine` | **nicht gemountet** | read-write |
| `derived-indices` | **nicht gemountet** | read-write |
| `backup-storage` | **verboten** | **verboten** |
| RT-2 | **verboten (contract-only)** | **verboten (contract-only)** |

### Containerinterne Zielpfade

`/etc/cbp` · `/var/lib/cbp/canonical` · `/var/lib/cbp/source-registry` ·
`/var/lib/cbp/mapping-registry` · `/var/lib/cbp/quarantine` ·
`/var/lib/cbp/released` · `/var/lib/cbp/derived` · `/run/cbp` · `/tmp`

**Reale Hostpfade sind verboten.** Es werden ausschließlich **benannte Volumes**
verwendet — keine Bind-Mounts, kein Docker-Socket, keine Geräte.

### Netzwerk

**Genau ein internes Netz** (`internal: true`). **Keine Portpublikation**, kein
Host-Netzwerk, kein Host-PID, kein Host-IPC, keine Subnetzdefinition, kein
Gateway, kein externer Netzwerkname.

## Egress

**Deny-by-default.** Sechs abstrakte Zielklassen, **keine konkreten
Endpunkte**, **keine Wildcards**:

1. Betriebssystem-Paket- und Security-Repositories
2. erforderliche Container-Registries
3. DNS-Dienste
4. NTP-Dienste
5. Zertifikats-, Renewal- und Revocation-Dienste
6. ausdrücklich freigegebene Git-/Artefaktquellen

Änderungen ausschließlich durch den **Human Maintainer**. Die **tatsächliche
Durchsetzung** erfolgt später auf **Host- und Dienstebene** — aktuell besteht
**nur der Vertrag**.

## Secrets

**Referenz-, kein Wertmodell.** Providerklasse: OS-geschützter Datei-Provider;
Providertyp **`file`**; Syntax `cbp-secret:v1:file:<opaque-id>`.
Unbekannter Provider und fehlende Referenz **blockieren fail-closed**. Rotation:
kontrollierter manueller Austausch der Referenz. Widerruf: alte Referenz sperren
und ersetzen. **Niemals Secret-Werte im Bundle oder Log.**

## Backup und Restore

| Ebene | Wert |
| --- | --- |
| VM-Backup | **wöchentlich** |
| Kanonische Daten | **täglich** — trägt das RPO |
| Zielklasse | **physisch separate NAS** (abstrakt) |
| RPO / RTO | **24 h** / **8 h** |
| Backupjob | **nicht implementiert** |
| CBP-/RT-2-Restore-Nachweis | **nicht erbracht** — R-20 offen |

## RT-2-Grenze

**P1 — contract-only.** Kein Speicher, kein Ereignis, keine Hashverkettung,
keine Retention-Engine, kein Backup, kein Restore. Mindestaufbewahrung **365
Tage**, danach **dauerhaft**, **keine** automatische Löschung, **kein**
separates Archiv. Zugriff ausschließlich über die Evidence-Schnittstelle
(TB-C4) — **im Bundle nicht gemountet**.

## Offline-Validator

**API:** `validate_bundle(root: pathlib.Path) -> ValidationReport` mit den
unveränderlichen Strukturen `ValidationIssue(code, path, message)` und
`ValidationReport(valid, issues)`. Issues sind stabil sortiert nach **Code,
Pfad, Meldung**.

**CLI:** `py.exe -3.13 deployments/profile-a/validate.py [bundle-root]`

**Exitcodes:** `0` gültig · `1` fachlich ungültig · `2` ungültiger Aufruf oder
Lesefehler.

**Stabile Issue-Code-Familien:** `BND-FILE-*` · `BND-COMPOSE-*` ·
`BND-CONTRACT-*` · `BND-CONFIG-*` · `BND-ENV-*` · `BND-LEAK-*` ·
`BND-DETERMINISM-*` · `BND-CLI-*`.

**Determinismus:** keine Zeitstempel, keine Zufallswerte, keine absoluten Pfade,
keine Hostinformationen; gleiche Eingabe erzeugt byte-identische Ausgabe.

**Grenzen:** kein Docker, kein Netzwerk, keine Prozesse, keine Hostrechte,
keine UID-/GID-Ermittlung, keine Secret-Auflösung, keine Symlink-Verfolgung,
keine Datei außerhalb des Bundle-Roots, keine Schreibzugriffe, ausschließlich
Python-Standardbibliothek.

## Testgrenze

Die zugehörigen Unit Tests heißen und gelten ausschließlich als **Profile-A
Bundle Validation Tests**. Sie sind **keine** Security Foundation NT-01 bis
NT-33 und **kein** PT-01, **keine** realen Containerprüfungen, **keine**
Infrastruktur- oder Deploymenttests, **kein** Enforcement-Nachweis und **keine**
operative Evidenz.

## Verbindliche Aussagegrenzen

| Nicht belegt | Stand |
| --- | --- |
| reale Bereitstellung | **keine** |
| Security-Control-Hochstufung | **12 `DOCUMENTED ONLY`** |
| Security-Negativtests | **0 von 32 ausgeführt** (D-056; zusätzlich **0 von 1** Positivtest) |
| Capability-Hochstufung | **0 von 29** |
| Gateauswertung | Mapping Activation und Security Foundation Readiness **`NOT EVALUATED`** |
| RT-2 | **nicht implementiert** |
| R-20 | **offen** |

**Zulässige Statusformulierungen für dieses Artefakt:** *repository artifact
implemented*, *offline validation implemented*, *offline validation passed*.
**Unzulässig:** Security Control implemented/tested/enforced, deployed,
operational, production-ready.
