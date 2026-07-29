# CBP-WP-020 — Controlled Profile-A Deployment Foundation

| Feld | Wert |
| --- | --- |
| Titel | **Controlled Profile-A Deployment Foundation** |
| Typ | **implementation** (Deployment-Artefakte, offline validiert) |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Status | **`in-review`** |
| Aktuelle Phase | **Phase B0 – Registration and Additive Deployment-Root Authority** |
| A0-Entscheidung | **D-055** (konsolidiert, A–J) |
| ADR | **not required** (`ADR_NOT_REQUIRED`) |
| Zielzustand | **Z1** — Deployment-Artefakte plus lokale Offline-Validierung |
| Scope | **S2** — Deployment Bundle plus Offline Validation |
| RT-2-Grenze | **P1** — ausschließlich Pfad-, Mount- und Schnittstellenvertrag |
| Capabilities | **0 von 29** — unverändert |
| Gates | Mapping Activation `NOT EVALUATED` · Security Foundation Readiness `NOT EVALUATED` |
| Security Controls | **12 `DOCUMENTED ONLY`** |
| R-20 | **offen** |
| R-33 | **16 Konsistenzvorgänge in 19 Work Packages** — in diesem Lauf unverändert |
| Tests | **558 – OK**, compileall Exit 0 (B0 ist docs-only) |
| Commit | **nicht ausgeführt** — Commit-Autorität beim Human Maintainer |

---

## Phasenmodell

| Phase | Stand |
| --- | --- |
| **A** — Architektur und Scope (read-only) | **abgeschlossen** |
| **B0** — Registration and Additive Deployment-Root Authority | **aktiv (dieser Stand)** |
| **B1** — Deployment Bundle | **nicht begonnen** |
| **B2** — Offline Validation | **nicht begonnen** |
| **B3** — reale Bereitstellung | **ausgeschlossen** — nicht Bestandteil von CBP-WP-020 |
| **C** — Post-Commit-Reconciliation | **nicht begonnen** |

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

**In Phase B0 wurde dieses Verzeichnis nicht angelegt.** Die Autorisierung gilt
ausschließlich für **Phase B1**.

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
die reale Durchsetzung auf Profil A. **0 von 31 Negativtests** werden ausgeführt.

## Capability- und Gate-Grenze (D-055 H)

Capabilities bleiben **0/29** · Mapping Activation Gate **`NOT EVALUATED`** ·
Security Foundation Readiness Gate **`NOT EVALUATED`** · **R-20 bleibt offen**.

---

## Geplantes B1-Zielbild — noch nicht erzeugt

Geplanter kanonischer Root: `deployments/profile-a/`

Geplante Artefaktklassen: Compose-Struktur für zwei getrennte Dienste · sichere
Konfigurationsvorlagen · Mount- und Datenklassenbeschreibung ·
Service-Identitätsabbildung · Secret-Referenzkonfiguration · Egress-Policy ·
Installationsrunbook · Validierungsrunbook · Rollbackrunbook.

> **Keines dieser Artefakte existiert.** Sie sind autorisierter späterer Scope,
> kein aktueller Stand.

## Geplantes B2-Zielbild — noch nicht erzeugt

Geplante Prüfungen: Artefakt- und Schemakonsistenz · zwei getrennte Services ·
non-root-Konfiguration · `no-new-privileges` · Capability-Drop ·
schreibgeschütztes Root-Filesystem · RT-3 als tmpfs · Canonical-Mounts
read-only · Backup-Storage **nicht** gemountet · Egress deny-by-default · keine
Wildcard-Allowlist · keine konkreten Endpunkte · Secret-Referenzsyntax ·
unbekannter Provider blockiert · fehlende Referenz blockiert · keine
Secret-Werte · keine privaten Infrastrukturkennungen · deterministische
Negativkonfigurationen.

> **Kein Validator und kein Test wurde implementiert oder verändert.** Die
> Testzahl bleibt in B0 unverändert bei **558**.

---

## Human Gates

| Gate | Gegenstand | Stand |
| --- | --- | --- |
| **1** | WP-020-Registrierung | **ausgeführt** — mit **D-055** |
| **2** | B1-/B2-Implementierung | **nicht ausgeführt** — erfordert nach Abschluss und Review von B0 einen **separaten Nova-Prompt** |
| **3** | Commit | **ausstehend** — ausschließlich Human Maintainer |
| **4** | **Reale Profil-A-Bereitstellung** | **nicht Bestandteil von CBP-WP-020** — erfordert abgeschlossenes und committetes WP-020, ein **separates Folge-Work-Package**, eine eigene Human-Maintainer-Autorisierung sowie einen eigenen Infrastruktur- und Sicherheitsplan |

**Keine reale Bereitstellung wird vorweggenommen.**

---

## Aussageschutz

Dieses Work Package belegt **nicht**:

| Nicht belegt | Tatsächlicher Stand |
| --- | --- |
| Ein Deployment existiere | **keines** — keine VM, kein Host, keine Runtime |
| Eine Kontrolle sei implementiert, getestet oder enforced | **12 `DOCUMENTED ONLY`**, 0 von 31 Negativtests |
| RT-2 existiere | **nicht implementiert** — nur Vertrag geplant |
| Ein Gate sei ausgewertet | beide **`NOT EVALUATED`** |
| Eine Capability sei erreicht | **0 von 29** |
| R-20 sei geschlossen | **offen** |

**Es wurde keine reale Infrastruktur berührt.** Kein Hypervisor-, NAS-, UniFi-,
Netz- oder Zielsystemzugriff; keine Port-, Prozess- oder Rechteprüfung; keine
Secret-Auflösung.

---

## Do-not-start-Scope

Nicht durchgeführt und nicht autorisiert: `deployments/` anlegen ·
Deployment-Artefakte, Konfigurationsvorlagen oder Compose-Dateien erzeugen ·
Validatoren implementieren · Tests oder Runtime-Code ändern · Datei verschieben,
umbenennen oder löschen · bestehende Struktur migrieren · VM-Erstellung ·
Installation · Deployment · Containerstart · Infrastruktur- oder Netzwerkzugriff ·
Secret-Auflösung oder Secret-Werte · konkrete UID/GID, IP-Adressen oder lokale
Pfade · RT-2-Erzeugung · Persistenz · Backupausführung · Restore-Test ·
Security-Evaluation · Enforcement · Gateauswertung oder -freigabe ·
Capability-Änderung · Source- oder Mapping-Aktivierung · zusätzliche Decision ·
ADR · neue Risiko-ID · Commit · Push · Tag · Release · CBP-WP-021.

**R-33 bleibt in diesem uncommitteten B0-Lauf unverändert bei 16
Konsistenzvorgängen in 19 Work Packages.** `RISK_REGISTER.md` und
`COMPLIANCE_CHECK.md` wurden **nicht** verändert.

**CBP-WP-021 ist nicht registriert und nicht autorisiert.**
