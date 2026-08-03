# CBP-WP-021 — Canonical Security Test Inventory Reconciliation

| Feld | Wert |
| --- | --- |
| Titel | **Canonical Security Test Inventory Reconciliation** |
| Typ | **governance-and-validation reconciliation** |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Status | **`in-review`** |
| Aktuelle Phase | **Phase B0 – Registration and Canonical Authority** |
| A0-Entscheidung | **D-056** (konsolidiert, A–U) |
| ADR | **not required** (`ADR_NOT_REQUIRED`) |
| Kanonische Authority | **32** Negativtests · **1** Positivtest · **33** Testfälle |
| Ausgeführt | **0 von 32** Negativtests · **0 von 1** Positivtest |
| Capabilities | **0 von 29** — unverändert |
| Gates | Mapping Activation `NOT EVALUATED` · Security Foundation Readiness `NOT EVALUATED` |
| Security Controls | **12 `DOCUMENTED ONLY`** |
| R-20 | **offen** |
| R-33 | **17/20** — in B0 unverändert, Fortschreibung erst in Phase C |
| Commit | **nicht ausgeführt** — Commit-Autorität beim Human Maintainer |

---

## Zweck

Alle kanonischen, abgeleiteten **und ausführbaren** Referenzen auf die
Security-Foundation-Testzahl auf den durch die authoritative A2-Acceptance-Matrix
belegten Stand reconciliieren:

| Kennzahl | Kanonischer Wert |
| --- | ---: |
| Security-Foundation-**Negativtests** | **32** |
| Security-Foundation-**Positivtests** | **1** |
| **Testfälle gesamt** | **33** |

**Dies ist keine Testausführung und keine Gateauswertung.** Ausgeführt sind
weiterhin **0 von 32** Negativtests und **0 von 1** Positivtest.

---

## Neuordnung gegenüber dem bisherigen Vorschlag

Die ID CBP-WP-021 war zuvor für **Enforcement Stage 1 – Filesystem Permission
Contract (KB-04)** vorgeschlagen. Dieser Vorschlag ist **zurückgestellt**.

**Grund:** Die read-only Phase-A-Analyse hat eine bereits **committete und
ausführbare** Kennzahl-Inkonsistenz festgestellt. Betroffen sind unter anderem
`deployments/profile-a/bundle.json`, `deployments/profile-a/validate.py` und
`tests/test_profile_a_deployment_bundle.py`. Damit ist die Abweichung **keine
rein redaktionelle**, sondern berührt validierte, ausführbare Artefakte.

**Verbindliche Reihenfolge:**

1. **CBP-WP-021** korrigiert das Security-Testinventar.
2. Danach darf das KB-04-Paket als **CBP-WP-022** vorbereitet werden.
3. Der abgeschlossene **KB-04-Phase-A-Bericht bleibt als vorbereitende
   Architekturgrundlage erhalten**.
4. **CBP-WP-022 ist weder registriert noch autorisiert.**

---

## Kanonisches Testinventar (D-056)

### Aktive Negativtests

| Bereich | IDs | Anzahl |
| --- | --- | ---: |
| erste Reihe | **NT-01 bis NT-24** | **24** |
| zweite Reihe | **NT-26 bis NT-33** | **8** |
| **Summe** | | **32** |

### Positivtest

**PT-01** — ein aktiver Security-Foundation-Positivtest.

### Gesamtinventar

**32 Negativtests + 1 Positivtest = 33 Security-Foundation-Testfälle.**

### NT-25

**Nicht aktiv.** Der frühere Fall war inhaltlich ein Positivtest und ist korrekt
als **PT-01** klassifiziert. Nach Regel **TT-5** wird eine umbenannte ID **nicht
neu vergeben** — **NT-25 bleibt bewusst frei**.

### NT-32 und NT-33

**Gültig, aktiv und aktuell.** Sie ersetzen die früheren Egress-Verwendungen der
dokumentübergreifend doppelt vergebenen IDs NT-23 und NT-24. Die **ursprünglichen
NT-23- und NT-24-Fälle der Acceptance Matrix bleiben aktiv und unverändert**.

### Die Zahl 31

**Ein überholter, falsch etikettierter Ableitungswert.** Er entspricht dem von
CBP-WP-011 auf **33** korrigierten **Gesamtwert** (30 NT + 1 PT) und wurde in
einer nicht nachgeführten Zusammenfassungszeile fälschlich als „Negativtests"
geführt; von dort ist er über die Roadmap in spätere Dokumente und in
ausführbare Artefakte gewandert.

> **31 ist keine konkurrierende Zählung**, sondern eine überholte Zahl in
> falscher Kategorie.

---

## In Scope (gesamtes Work Package)

- authoritative Feststellung über **D-056**
- Korrektur der fehlerhaften **Ursprungs- und Ableitungsstellen**
- Korrektur der **Roadmap**
- Korrektur der **Profil-A-Runbooks**
- Korrektur des **Profil-A-Runtime-Vertrags**
- Korrektur des **WP-020-Dokuments**
- Korrektur der **Statusspiegel**
- Korrektur von **`deployments/profile-a/bundle.json`**
- Korrektur von **`deployments/profile-a/validate.py`**
- Korrektur der zugehörigen **Bundle-Tests**
- vollständige Validierung
- Post-Commit-Reconciliation

## Out of Scope

| Ausgeschlossen |
| --- |
| neue Security-Foundation-Test-ID |
| Änderung des Inhalts bestehender NT-Fälle |
| tatsächliche Ausführung von NT-01 bis NT-33 |
| Änderung von PT-01 |
| KB-04-Vertrag · KB-04-Prüfmodul · neues Security-Unterpaket |
| Shellskript · neuer Repository-Root |
| Control-Hochstufung · Gateauswertung · Capability-Änderung |
| reale Infrastruktur · Docker · VM · Netzwerk · Secrets |
| RT-2 · Persistenz · Backup · Restore |
| Source- oder Mapping-Aktivierung |
| Commitzähler-Governance C3 |
| CBP-WP-022-Registrierung |

---

## Phasenmodell

| Phase | Gegenstand | Stand |
| --- | --- | --- |
| **A** | Authority- und Scope-Analyse (read-only) | **abgeschlossen** |
| **B0** | Registrierung und D-056 | **aktiv (dieser Stand, uncommitted)** |
| **B1** | Dokumentarische und ausführbare Reconciliation | **nicht begonnen** |
| **B2** | Vollständige Tests, Validator- und Konsistenzprüfung | **nicht begonnen** |
| **C** | Post-Commit-Reconciliation | **nicht begonnen** |

**Keine reale Infrastrukturphase.**

---

## Übergangszustand nach B0

**D-056 stellt 32 verbindlich fest. Die Durchführung erfolgt erst in B1/B2.**

Bis dahin besteht eine **bekannte, ausdrücklich eingegrenzte
Übergangsabweichung**:

| Feststellung |
| --- |
| Einige committete Dokumente und ausführbare Profil-A-Artefakte führen weiterhin **31** |
| Die Abweichung ist **bekannt** und **aktiv in CBP-WP-021 eingegrenzt** |
| Sie wird in **B1/B2** korrigiert |
| Das bestehende Profil-A-Bundle bleibt bis zur koordinierten Änderung **unverändert und gegen seinen bisherigen Vertrag gültig** |
| Es darf bis zur B1/B2-Korrektur **nicht als kanonisch hinsichtlich der Security-Test-Gesamtzahl** bezeichnet werden |

> **Der Bundlevertrag ist fail-closed.** Eine Änderung von `bundle.json` ohne die
> gleichzeitige Anpassung von Validator und Testsuite bricht die Validierung
> sofort. Deshalb erfolgt die Korrektur **koordiniert in einem Schritt** und
> **nicht** in B0.

### In B0 nicht verändert

`deployments/**` · `tests/**` · `core/**` · `docs/operations/**` ·
`docs/runtime/**` · `docs/security/**` · `docs/decisions/**` ·
`project-system/RISK_REGISTER.md` · `project-system/COMPLIANCE_CHECK.md` ·
`project-system/CAPABILITY_MATRIX.md` · `work-packages/CBP-WP-011.md` ·
`work-packages/CBP-WP-020.md` · `docs/roadmap/PHASE_1_FOUNDATION_PLAN.md`.

---

## Aussageschutz

Dieses Work Package belegt **nicht**:

| Nicht belegt | Tatsächlicher Stand |
| --- | --- |
| Ein Security-Foundation-Test sei ausgeführt | **0 von 32** NT, **0 von 1** PT |
| Eine Kontrolle sei implementiert, getestet oder enforced | **12 `DOCUMENTED ONLY`** |
| Ein Gate sei ausgewertet | beide **`NOT EVALUATED`** |
| Eine Capability sei erreicht | **0 von 29** |
| R-20 sei geschlossen | **offen** |
| Ein Deployment existiere | **keines** |
| RT-2 existiere | **nicht implementiert** |

**Die Feststellung eines Inventarwerts ist keine Testausführung.**

---

## Human Gates

| Gate | Gegenstand | Stand |
| --- | --- | --- |
| **1** | WP-021-Registrierung mit **D-056** | **ausgeführt** (dieser Stand) |
| **2** | B1-/B2-Reconciliation | **nicht ausgeführt** — erfordert separaten Nova-Prompt |
| **3** | Commit | **ausstehend** — ausschließlich Human Maintainer |
| **4** | **CBP-WP-022 (KB-04)** | **nicht registriert, nicht autorisiert** |

---

## Do-not-start-Scope

Nicht durchgeführt und nicht autorisiert: vollständige 31→32-Korrektur ·
Bundle · Validator · Tests · Runbooks · Runtime-Vertrag · WP-011 · WP-020 ·
Acceptance Matrix · KB-04-Implementierung · Security-Unterpaket · Shellskript ·
neuer Repository-Root · Control-Hochstufung · Meldung eines
Security-Foundation-Tests als ausgeführt · Gateauswertung · Capability-Änderung ·
Risikoänderung · neue Risiko-ID · ADR · reale Infrastruktur · Docker · VM ·
Netzwerk · Secret-Auflösung · RT-2 · Persistenz · Backup · Restore · Source- oder
Mapping-Aktivierung · Commitzähler-Governance · CBP-WP-022 · Commit · Push · Tag ·
Release.

**In B0 wurden ausschließlich eine neue Work-Package-Datei angelegt und
Authority- sowie Statusspiegel nachgeführt.**

**R-33 bleibt in diesem uncommitteten B0-Lauf unverändert bei 17
Konsistenzvorgängen in 20 Work Packages.** `RISK_REGISTER.md` und
`COMPLIANCE_CHECK.md` wurden **nicht** verändert.

**Die Commitzähler-Governance C3 ist fachlich zur Kenntnis genommen, aber
ausdrücklich nicht Bestandteil von D-056 oder CBP-WP-021.**

**CBP-WP-022 ist nicht registriert und nicht autorisiert.**
