# CBP-WP-020 — Controlled Profile-A Deployment Foundation

| Feld | Wert |
| --- | --- |
| Titel | **Controlled Profile-A Deployment Foundation** |
| Typ | **implementation** (Deployment-Artefakte, offline validiert) |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Status | **`committed`** · **`complete`** |
| Aktuelle Phase | **Phase C – Post-Commit Reconciliation** (abgeschlossen) |
| A0-Entscheidung | **D-055** (konsolidiert, A–J) |
| ADR | **not required** (`ADR_NOT_REQUIRED`) |
| Zielzustand | **Z1** — Deployment-Artefakte plus lokale Offline-Validierung |
| Scope | **S2** — Deployment Bundle plus Offline Validation |
| RT-2-Grenze | **P1** — ausschließlich Pfad-, Mount- und Schnittstellenvertrag |
| Capabilities | **0 von 29** — unverändert |
| Gates | Mapping Activation `NOT EVALUATED` · Security Foundation Readiness `NOT EVALUATED` |
| Security Controls | **12 `DOCUMENTED ONLY`** |
| R-20 | **offen** |
| R-33 | **17 Konsistenzvorgänge in 20 Work Packages** (`17/20`) — fortgeschrieben durch diese Post-Commit-Reconciliation |
| Tests | **724 – OK**, **0 übersprungen**; `compileall .` Exit 0, Offline-Validator Exit 0 |
| Commit | **B0 `committed` `17057e2`** · **B1/B2 `committed` `9c6c0fb`** — Phase C uncommitted, Commit-Autorität beim Human Maintainer |

---

## Phasenmodell

| Phase | Stand |
| --- | --- |
| **A** — Architektur und Scope (read-only) | **abgeschlossen** |
| **B0** — Registration and Additive Deployment-Root Authority | **complete** — `committed` `17057e2` |
| **B1** — Deployment Bundle | **complete** — `committed` `9c6c0fb` |
| **B2** — Offline Validation | **complete** — `committed` `9c6c0fb` |
| **B3** — reale Bereitstellung | **nicht Bestandteil von CBP-WP-020** — **nicht begonnen**, **nicht autorisiert** |
| **C** — Post-Commit-Reconciliation | **abgeschlossen (dieser Stand, uncommitted)** |

---

## Phase-A-Ergebnis

Die read-only Architekturphase hat vier Zielzustände (Z0–Z3) und vier
Scope-Varianten (S1–S4) bewertet.

| Ergebnis | Begründung |
| --- | --- |
| **Zielzustand Z1** | Artefakte **plus** Offline-Validierung. Z0 allein bliebe unbelegt — genau der Fehler, der bei den Security-Kontrollen bereits zu `DOCUMENTED ONLY` geführt hat. Z2 und Z3 verlangen realen Infrastrukturzugriff und sind eigene Pakete. |
| **Scope S2** (46/50) | S1 (38) wäre dokumentarischer Leerlauf; S3 (21) und S4 (17) wären ein Deployment-/Security-Megapaket mit realem Zugriff, den der Implementation Agent weder darf noch kann. |
| **RT-2-Grenze P1** | Nur Vertrag. P0 erzeugte spätere Nachrüstschulden; P2 löste sofort BR-1…BR-8, INT-1…INT-5 und vier Negativtests aus und wäre ein eigenes Paket. |
| **`ADR_NOT_REQUIRED`** | Keiner der sechs ADR-Auslöser trifft zu. |

Zentraler Befund: Die Deployment-**Werte** für Profil A sind vollständig und
genehmigt (DRC **APPROVED BY HUMAN MAINTAINER**, 19 `ready`); die
Deployment-**Artefakte** fehlen vollständig.

---

## Verbindliche Strukturentscheidung (D-055 A)

Autorisierter kanonischer Repository-Ort für spätere Profil-A-Artefakte:

```text
deployments/profile-a/
```

**In Phase B0 wurde dieses Verzeichnis nicht angelegt; in Phase B1 wurde es
angelegt** — mit **genau sieben Dateien** und ohne jede Berührung bestehender
Inhalte.

### Verhältnis zu ADR-0007

ADR-0007 führt `deployments/` bereits als Zielstruktur mit der Zweckbestimmung
„**Profilspezifische Vorlagen ohne private Werte**". D-055 setzt diesen
**bereits angenommenen** Zielstrukturteil kontrolliert um. **Es wird keine neue
Architektur erfunden und ADR-0007 nicht verändert.**

### Verhältnis zu D-029

D-029 friert das bestehende Layout ein: „Autorisiert **keine** Verschiebung; das
aktuelle Layout bleibt bis zu einem separaten, ausdrücklich freigegebenen
Migrations-Work-Package."

Die Autorisierung ist **ausschließlich additiv**. Verboten bleiben:

| Verboten |
| --- |
| Verschieben bestehender Dateien |
| Umbenennen bestehender Dateien |
| Löschen bestehender Dateien |
| Umsortieren bestehender Verzeichnisse |
| vollständige Migration auf die ADR-0007-Zielstruktur |
| Verlust oder Umschreiben von Git-Historie |

**Das Anlegen eines neuen, bislang nicht vorhandenen Artefaktpfads ist keine
Migration bestehender Inhalte. D-029 bleibt vollständig wirksam.**

---

## In Scope (Phasen B1 und B2)

- Profil-A-Deployment-Bundle unter `deployments/profile-a/`
- Compose-Struktur für **zwei getrennte Dienste**
- sichere Konfigurationsvorlagen (ausschließlich Platzhalter)
- Mount- und Datenklassenbeschreibung
- Service-Identitätsabbildung (`svc-control-plane`, `svc-data-worker`) — abstrakt
- Secret-Referenzkonfiguration (Providertyp `file`, read-only)
- Egress-Policy, deny-by-default
- **Installationsrunbook**, **Validierungsrunbook**, **Rollbackrunbook**
- deterministische **Offline-Validatoren**
- **synthetische Negativkonfigurationstests**

## Out of Scope

| Ausgeschlossen |
| --- |
| reale VM · Installation · Containerstart |
| Proxmox-, NAS-, UniFi- und Netzwerkzugriff |
| lokale UID-/GID-Festlegung |
| konkrete IP-Adressen, Hostnamen, lokale Pfade |
| Secret-Werte |
| **RT-2-Implementation** |
| reale Persistenz · Backupausführung · Restore-Test |
| Security-Enforcement · Gateauswertung · Gatefreigabe |
| Capability-Freigabe · Source- oder Mapping-Aktivierung |

---

## RT-2-Grenze (D-055 F)

**P1 ist verbindlich.** WP-020 definiert ausschließlich den **abstrakten Pfad-,
Mount- und Schnittstellenvertrag** für ein späteres RT-2.

**WP-020 darf nicht erzeugen:** RT-2-Speicher · RT-2-Ereignisse ·
Hashverkettung · append-only Runtime · Retention-Engine · RT-2-Backup ·
RT-2-Restore.

## Security-Grenze (D-055 G)

Alle **zwölf Security Controls bleiben `DOCUMENTED ONLY`**. **Kein** Control
darf durch WP-020 auf `implemented`, `tested` oder `enforced` gesetzt werden.
Die Offline-Validatoren prüfen **ausschließlich Artefakte und Verträge**, nicht
die reale Durchsetzung auf Profil A. **0 von 32 Negativtests** werden ausgeführt.

## Capability- und Gate-Grenze (D-055 H)

Capabilities bleiben **0/29** · Mapping Activation Gate **`NOT EVALUATED`** ·
Security Foundation Readiness Gate **`NOT EVALUATED`** · **R-20 bleibt offen**.

---

## B1-Ergebnis — Profil-A-Bundle

Kanonischer Root: `deployments/profile-a/` — **genau sieben Dateien**:

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

**Drei Runbooks** und **ein Runtime-Vertrag** liegen bewusst **außerhalb** des
Bundles:

```text
docs/operations/PROFILE_A_INSTALLATION_RUNBOOK.md
docs/operations/PROFILE_A_VALIDATION_RUNBOOK.md
docs/operations/PROFILE_A_ROLLBACK_RUNBOOK.md
docs/runtime/PROFILE_A_DEPLOYMENT_BUNDLE.md
```

| Gegenstand | Umsetzung |
| --- | --- |
| Zwei getrennte Dienste | `control-plane` / `data-worker` mit den logischen Identitäten `svc-control-plane` / `svc-data-worker` |
| Prozessidentität | ausschließlich **fail-closed Operatorvariablen** (`${...:?...}`) für UID **und** GID — **kein Root-Literal, keine numerische Identität, kein Default** |
| Images | ausschließlich fail-closed Operatorvariablen — **keine Registry, Domain, URL oder `latest`** |
| Härtung | `read_only: true` · `cap_drop: [ALL]` · `no-new-privileges:true` · `privileged: false` · `restart: "no"` · eigenes `tmpfs` |
| Mounts | ausschließlich **benannte Volumes**; `canonical-data` beidseitig **read-only**; `backup-storage` und RT-2 **verboten**; **keine Bind-Mounts, kein Docker-Socket, keine Geräte** |
| Netzwerk | **genau ein** internes Netz (`internal: true`), **keine Portpublikation**, kein Host-Netz/-PID/-IPC |
| Egress | **deny-by-default**, sechs **abstrakte** Zielklassen, keine Wildcards, keine konkreten Endpunkte |
| Secrets | **Referenz-, kein Wertmodell** — `cbp-secret:v1:file:<opaque-id>`; unbekannter Provider und fehlende Referenz **blockieren** |
| RT-2 | **P1 contract-only** — kein Speicher, kein Ereignis, keine Hashverkettung, keine Retention-Engine, kein Backup, kein Restore |
| Compose-Format | **JSON-kompatible YAML-Teilmenge** — erlaubt stdlib-only Validierung; **reversible Implementierungsentscheidung, keine neue Architekturbindung** |

## B2-Ergebnis — deterministische Offline-Validierung

`deployments/profile-a/validate.py` — Python-Standardbibliothek, read-only.

**API:** `validate_bundle(root: pathlib.Path) -> ValidationReport` mit
`ValidationIssue(code, path, message)`; Issues stabil sortiert nach Code, Pfad,
Meldung.

**Exitcodes:** `0` gültig · `1` fachlich ungültig · `2` ungültiger Aufruf.

**Ergebnis:**

```text
PROFILE-A-BUNDLE VALID
issues=0
```

Zwei Läufe erzeugten **byte-identische** Ausgabe (SHA-256 gleich), Exit **0**.

Geprüft: Dateisatz, Kodierung, BOM, NUL, Symlinks · Compose-Struktur und
Härtungsvorlagen · Mountmatrix und Zielpfade · Netzwerk- und Egress-Vertrag ·
Secret-Referenzsyntax · Vertragskonsistenz zwischen `compose.yaml`, beiden TOML-
Vorlagen und `bundle.json` · Public-Neutrality und Leakage · kanonische
JSON-Formatierung.

**Nicht geprüft** (und nicht prüfbar): reale Hostrechte, reale UID-/GID-Werte,
tatsächlich gemountete Volumes, echte Netzwerkdurchsetzung, aufgelöste Secrets,
laufende Container, Security-Foundation-Wirksamkeit.

**166 neue Tests** in `tests/test_profile_a_deployment_bundle.py` (25 positive,
81 negative Konfigurationen, plus Determinismus-, CLI-, Literal- und
Scope-Prüfungen). Gesamtstand **724 Tests OK**, **0 übersprungen**.

Der **Symlink-Negativfall** wird deterministisch ausgeführt: Da die
Ausführungsumgebung keine echten Symlinks anlegen darf, meldet genau ein
Bundle-Eintrag über `Path.is_symlink` einen Symlink, während die vollständige
`validate_bundle`-Pipeline unverändert läuft. Eine vorgeschaltete
Kontrollzusicherung belegt, dass ohne die Simulation **kein**
`BND-FILE-SYMLINK` entsteht — die Simulation kippt also genau den geprüften
Zweig. Ein zweiter Test zeigt, dass ein als Symlink erkannter **erwarteter**
Eintrag fail-closed übersprungen wird und zusätzlich `BND-FILE-MISSING`
auslöst.

> **Diese Tests sind Profile-A Bundle Validation Tests.** Sie sind
> ausdrücklich **keine** Security Foundation NT-01 bis NT-33 und **kein**
> PT-01, **keine** realen Containerprüfungen, **kein** Enforcement-Nachweis und
> **keine** operative Evidenz. **Kanonische Kennzahl (D-056): 0 von 32
> Negativtests, 0 von 1 Positivtest.**

## Zulässige Statusaussagen

**Zulässig:** *repository artifact implemented* · *offline validation
implemented* · *offline validation passed*.

**Unzulässig:** Security Control implemented/tested/enforced · deployed ·
operational · production-ready.

---

## Human Gates

| Gate | Gegenstand | Stand |
| --- | --- | --- |
| **1** | WP-020-Registrierung | **ausgeführt** — mit **D-055** |
| **2** | B1-/B2-Implementierung | **ausgeführt** — auf separaten Nova-Prompt nach Commit von B0 (`17057e2`) |
| **3** | Commit | **ausgeführt** — B0 `17057e2`, B1/B2 `9c6c0fb`; Phase C bleibt uncommitted |
| **4** | **Reale Profil-A-Bereitstellung** | **nicht Bestandteil von CBP-WP-020** — erfordert abgeschlossenes und committetes WP-020, ein **separates Folge-Work-Package**, eine eigene Human-Maintainer-Autorisierung sowie einen eigenen Infrastruktur- und Sicherheitsplan |

**Keine reale Bereitstellung wird vorweggenommen.**

---

## Aussageschutz

Dieses Work Package belegt **nicht**:

| Nicht belegt | Tatsächlicher Stand |
| --- | --- |
| Ein Deployment existiere | **keines** — keine VM, kein Host, keine Runtime |
| Eine Kontrolle sei implementiert, getestet oder enforced | **12 `DOCUMENTED ONLY`**, 0 von 32 Negativtests |
| RT-2 existiere | **nicht implementiert** — nur Vertrag geplant |
| Ein Gate sei ausgewertet | beide **`NOT EVALUATED`** |
| Eine Capability sei erreicht | **0 von 29** |
| R-20 sei geschlossen | **offen** |

**Es wurde keine reale Infrastruktur berührt.** Kein Hypervisor-, NAS-, UniFi-,
Netz- oder Zielsystemzugriff; keine Port-, Prozess- oder Rechteprüfung; keine
Secret-Auflösung.

---

## Do-not-start-Scope

Nicht durchgeführt und nicht autorisiert: Datei verschieben, umbenennen oder
löschen · bestehende Struktur migrieren · Runtime-Code unter `core/` ändern ·
VM-Erstellung · Installation · Deployment · Containerstart · Docker- oder
Compose-Kommando · Infrastruktur- oder Netzwerkzugriff · DNS-, Port-, Prozess-
oder Hostrechteprüfung · reale UID-/GID-Ermittlung · Secret-Auflösung oder
Secret-Werte · konkrete IP-Adressen, Domains, URLs, Hostnamen oder lokale
Pfade · RT-2-Erzeugung · Persistenz · Backupausführung · Restore-Test ·
Security-Evaluation · Enforcement · Gateauswertung oder -freigabe ·
Capability-Änderung · Source- oder Mapping-Aktivierung · zusätzliche Decision ·
ADR · neue Risiko-ID · Commit · Push · Tag · Release · CBP-WP-021.

**In B1/B2 wurden ausschließlich neue Dateien angelegt und zehn bestehende
Statusspiegel nachgeführt.** **In Phase C wurden ausschließlich Statusspiegel
und die R-33-Fortschreibung nachgeführt** — kein Bundle, kein Validator, kein
Test, kein Runbook, kein Runtime-Vertrag und kein Runtime-Code berührt.

---

## Phase C — Post-Commit Reconciliation

| Feld | Wert |
| --- | --- |
| Implementation Commit | **`9c6c0fb`** — „CBP-WP-020: add validated profile A deployment bundle" |
| Parent | `17057e2` (Phase B0) |
| Commitinhalt | **22 Pfade**, **3467 Einfügungen**, **87 Löschungen**, **12 neue** und **10 modifizierte** Dateien, **0 gelöscht**, **0 umbenannt** |
| Commitzahl | **29**, `origin/main` synchron |
| Bundle | **exakt sieben Dateien** unter `deployments/profile-a/` |
| Tests | **724 – OK**, **0 übersprungen**, davon **166** Profile-A Bundle Validation Tests |
| Validator | `PROFILE-A-BUNDLE VALID`, `issues=0`, Exit 0, byte-identisch wiederholbar |
| `compileall .` | Exit 0 |
| R-33 | **16/19 → 17/20** |

**Zielzustand Z1 erreicht · Scope S2 abgeschlossen · RT-2-Grenze P1 eingehalten.**

**CBP-WP-020 ist `committed` und `complete`.** Es ist **kein Work Package
aktiv** und **kein Folge-Work-Package autorisiert**. **CBP-WP-021 ist nicht
registriert und nicht autorisiert.** Der nächste Schritt wird durch den Human
Maintainer und Nova separat bestimmt.

**Phase C ändert keine Sachaussage:** Deployment Foundation bleibt *repository
artifact implemented* und *offline validation passed* — **nicht deployed, nicht
operational, nicht production-ready**. Capabilities **0/29**, beide Gates
`NOT EVALUATED`, zwölf Controls `DOCUMENTED ONLY`, Security-Foundation-NT-Tests
**0/32** (D-056), **R-20 offen**.
