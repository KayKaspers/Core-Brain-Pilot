# Profile-A Deployment Bundle

Offline deployment bundle for **Profile A** (Proxmox VM reference profile),
created in **CBP-WP-020** under **D-055**.

| Feld | Wert |
| --- | --- |
| Zielzustand | **Z1** — Artefakte plus lokale Offline-Validierung |
| Scope | **S2** — Deployment Bundle plus Offline Validation |
| RT-2-Grenze | **P1** — ausschließlich Pfad-, Mount- und Schnittstellenvertrag |
| Status | **offline-template** |

## Aussagegrenzen — verbindlich

Dieses Bundle ist eine **Vorlage**. Es ist **kein** Deployment.

| Nicht belegt | Stand |
| --- | --- |
| Eine Bereitstellung existiere | **keine** — `deployed: false`, `runtime_started: false` |
| Ein Container sei gestartet | **nein** — in CBP-WP-020 wird nichts gestartet |
| Eine Sicherheitskontrolle sei wirksam | **12 Controls `DOCUMENTED ONLY`** |
| Security-Negativtests seien gelaufen | **0 von 31 ausgeführt** |
| RT-2 existiere | **contract-only**, nicht implementiert |
| Ein Gate sei ausgewertet | Mapping Activation und Security Foundation Readiness: **`NOT EVALUATED`** |
| Eine Capability sei erreicht | **0 von 29** |
| R-20 sei geschlossen | **offen** |

**Kein Containerstart, keine Installation, keine Infrastrukturberührung durch
CBP-WP-020.**

## Dateien — exakt sieben

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

Jede weitere Datei unter `deployments/profile-a/` wird vom Validator
**fail-closed** abgewiesen.

## Warum `compose.yaml` JSON-formatiert ist

- **JSON ist eine gültige YAML-Teilmenge.** Jeder YAML-Parser liest gültiges
  JSON.
- **Docker Compose kann die Datei später unverändert als Compose-YAML lesen.**
- **Der Offline-Validator liest dieselbe Datei deterministisch als JSON** —
  mit `json.loads` aus der Standardbibliothek, ohne externe YAML-Abhängigkeit.
- Das ist eine **reversible Implementierungsentscheidung**, **keine neue
  Architekturbindung**. Wird später ein YAML-Parser eingeführt, kann die Datei
  ohne Vertragsänderung in idiomatisches YAML überführt werden.

## Validator

```bash
py.exe -3.13 deployments/profile-a/validate.py
```

Optional mit explizitem Bundle-Root:

```bash
py.exe -3.13 deployments/profile-a/validate.py <bundle-root>
```

**Exitcodes** (gelten nur für dieses Offline-Werkzeug):

| Code | Bedeutung |
| --- | --- |
| **0** | Bundle gültig |
| **1** | Bundle fachlich ungültig |
| **2** | ungültiger Aufruf oder unerwarteter Lesefehler |

**Gültige Ausgabe:**

```text
PROFILE-A-BUNDLE VALID
issues=0
```

**Ungültige Ausgabe:**

```text
PROFILE-A-BUNDLE INVALID
issues=<Anzahl>
<CODE> | <relativer Pfad> | <Meldung>
```

Die Ausgabe ist **deterministisch**: stabil sortiert nach Code, Pfad und
Meldung, ohne Zeitstempel, ohne absolute Pfade, ohne Farben. Gleiche Eingabe
erzeugt byte-identische Ausgabe.

Der Validator ruft **kein Docker** auf, verwendet **kein Netzwerk**, startet
**keine Prozesse**, liest **keine Hostbenutzer, UIDs oder GIDs**, löst **keine
Secrets** auf, folgt **keinen Symlinks** und liest **keine Datei außerhalb des
Bundle-Roots**. Er schreibt nichts.

### Stabile Issue-Code-Familien

| Familie | Gegenstand |
| --- | --- |
| `BND-FILE-*` | Dateisatz, Kodierung, Symlinks, unerwartete Pfade |
| `BND-COMPOSE-*` | Compose-Struktur, Härtung, Mounts, Netzwerk, Configs |
| `BND-CONTRACT-*` | `bundle.json` — Identität, Datenklassen, Egress, Secrets, Backup, RT-2, Controls, Gates |
| `BND-CONFIG-*` | TOML-Vorlagen und Rollenkonsistenz |
| `BND-ENV-*` | Operator-Environment-Vorlage |
| `BND-LEAK-*` | Public-Neutrality und Secret-Leakage |
| `BND-DETERMINISM-*` | kanonische Serialisierung |
| `BND-CLI-*` | reserviert für CLI-Vertragsverletzungen |

**Jeder fachliche Fehler trägt einen stabilen Code.** Es gibt keine
Fehlermeldung ohne Code.

`validate.py` ist von seiner **eigenen inhaltlichen** Leakage-Prüfung
ausgenommen, weil es die Erkennungsmuster enthält. Es bleibt Teil des
geprüften Dateisatzes.

## Operator-Pflichtvariablen

`operator.env.example` enthält ausschließlich **leere** Pflichtwerte:

```text
CBP_CONTROL_PLANE_IMAGE=
CBP_DATA_WORKER_IMAGE=
CBP_CONTROL_PLANE_UID=
CBP_CONTROL_PLANE_GID=
CBP_DATA_WORKER_UID=
CBP_DATA_WORKER_GID=
CBP_DEPLOYMENT_PROFILE=A
```

**Leere Pflichtwerte sind beabsichtigt fail-closed.** Die Vorlage ist **nicht
direkt lauffähig**: Compose bricht bei fehlender Auflösung ab (`:?`-Syntax).
Die Datei wird in den **lokalen Operator-Workspace außerhalb dieses
Repositorys** kopiert und **nur dort** befüllt. Eine befüllte Datei wird
**niemals** zurück ins Repository kopiert.

**Keine Secret-Werte. Keine privaten Infrastrukturwerte.** Weder Adressen noch
Hostnamen, Domains, URLs, NAS-Kennungen, Hostpfade noch konkrete UID- oder
GID-Werte gehören in dieses Bundle.

## Weiterführende Dokumente

| Dokument | Zweck |
| --- | --- |
| [PROFILE_A_DEPLOYMENT_BUNDLE.md](../../docs/runtime/PROFILE_A_DEPLOYMENT_BUNDLE.md) | vollständiger Runtime-Vertrag |
| [PROFILE_A_INSTALLATION_RUNBOOK.md](../../docs/operations/PROFILE_A_INSTALLATION_RUNBOOK.md) | spätere Bereitstellung |
| [PROFILE_A_VALIDATION_RUNBOOK.md](../../docs/operations/PROFILE_A_VALIDATION_RUNBOOK.md) | Validierung |
| [PROFILE_A_ROLLBACK_RUNBOOK.md](../../docs/operations/PROFILE_A_ROLLBACK_RUNBOOK.md) | Rollback |
