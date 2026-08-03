# CBP-WP-021 — Canonical Security Test Inventory Reconciliation

| Feld | Wert |
| --- | --- |
| Titel | **Canonical Security Test Inventory Reconciliation** |
| Typ | **governance-and-validation reconciliation** |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** |
| Status | **`in-review`** |
| Aktuelle Phase | **Phase B1/B2 – Coordinated Reconciliation and Validation** |
| A0-Entscheidung | **D-056** (konsolidiert, A–U) |
| ADR | **not required** (`ADR_NOT_REQUIRED`) |
| Kanonische Authority | **32** Negativtests · **1** Positivtest · **33** Testfälle |
| Ausgeführt | **0 von 32** Negativtests · **0 von 1** Positivtest |
| Capabilities | **0 von 29** — unverändert |
| Gates | Mapping Activation `NOT EVALUATED` · Security Foundation Readiness `NOT EVALUATED` |
| Security Controls | **12 `DOCUMENTED ONLY`** |
| R-20 | **offen** |
| R-33 | **17/20** — unverändert, Fortschreibung erst in Phase C |
| Commit | **B0 `committed` `0cb4ea9`** · **B1/B2 nicht committed** — Commit-Autorität beim Human Maintainer |

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
| **B0** | Registrierung und D-056 | **abgeschlossen** — `committed` `0cb4ea9` |
| **B1** | Dokumentarische und ausführbare Reconciliation | **implemented, uncommitted** |
| **B2** | Vollständige Tests, Validator- und Konsistenzprüfung | **validated, uncommitted** |
| **C** | Post-Commit-Reconciliation | **nicht begonnen** |

**Keine reale Infrastrukturphase.**

---

## Stand nach B1/B2

**Die Übergangsabweichung ist aufgelöst.** Die Reconciliation auf **32 / 1 / 33**
ist durchgeführt.

### Koordinierte Änderung der ausführbaren Artefakte

Die drei Artefakte wurden **atomar in einem Lauf** geändert:

| Artefakt | vorher | nachher |
| --- | --- | --- |
| `deployments/profile-a/bundle.json` | `"total": 31` | **`"total": 32`** |
| `deployments/profile-a/validate.py` | erzwingt `total == 31` | **erzwingt `total == 32`** |
| `tests/test_profile_a_deployment_bundle.py` | `…are_zero_of_31`, erwartet `(0, 31)` | **`…are_zero_of_32`, erwartet `(0, 32)`** |

Schema, Issue-Codes, Exitcodes und Ausgabeformat sind **unverändert**. Der
Validator meldet weiterhin bei **jedem** anderen Wert als 32 fail-closed
`BND-CONTRACT-NEGATIVE-TESTS`. Die Testzahl ist **unverändert 166**.

### Dokumentarische Reconciliation

Korrigiert: `work-packages/CBP-WP-011.md` (falsch etikettierte
Zusammenfassungszeile, mit Erläuterung), `docs/roadmap/PHASE_1_FOUNDATION_PLAN.md`,
`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`, die drei Profil-A-Runbooks
beziehungsweise der Runtime-Vertrag, `work-packages/CBP-WP-020.md` sowie die
Statusspiegel.

**Historische Darstellungen bleiben erhalten:** die Befundbeschreibung in
CBP-WP-011 („Ursprünglich: 31 Tests, davon 30 Negativtests…"), die dortige
Korrekturtabelle (Vorher 31 → 33) und die R-33-Chronologieeinträge dokumentieren
weiterhin unverändert, dass **31 der frühere fehlerhafte Wert** war.

### Phase B1/B2.1 — Restfundstelle geschlossen

`deployments/profile-a/README.md` führte weiterhin „0 von 31 ausgeführt". Der
Pfad wurde für einen eng begrenzten Nachlauf zusätzlich autorisiert und auf
**0 von 32** korrigiert (mit Ergänzung **0 von 1** Positivtest). **Das
Profil-A-Bundle ist damit intern konsistent.**

**Bundle-Abhängigkeitsprüfung:** Die README ist in `bundle.json` **namentlich**
geführt und Teil der Exakt-sieben-Dateien-Regel. Es existiert **kein** SHA-256,
**keine** Dateigröße, **kein** aggregierter Bundle-Hash und **kein**
manifestierter Inhaltswert für sie; weder `validate.py` noch die Bundle-Tests
prüfen ihren Inhalt. **Es waren daher keine abhängigen Metadaten anzupassen** —
die Korrektur blieb auf die eine Textzeile beschränkt.

### Verbleibende Fundstellen — Phase C

| Datei | Fundstelle | Charakter |
| --- | --- | --- |
| `project-system/RISK_REGISTER.md` | R-33-Chronologie, siebzehnter Vorgang | dokumentiert den damaligen Stand — Datei bisher nicht im Scope |
| `project-system/COMPLIANCE_CHECK.md` | R-33-Chronologie, siebzehnter Vorgang | dokumentiert den damaligen Stand — Datei bisher nicht im Scope |

Beide sind **Chronologieeinträge** und werden sachgerecht in **Phase C**
behandelt. **Es verbleibt keine sachlich fehlerhafte aktuelle Fundstelle.**

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
Authority- sowie Statusspiegel nachgeführt. In B1/B2 wurden ausschließlich die
kanonische Testinventarzahl reconciliiert und die zugehörige Validierung
ausgeführt** — keine neue Test-ID, kein geänderter NT- oder PT-Testinhalt, keine
Testausführung der Security Foundation.

**R-33 bleibt unverändert bei 17 Konsistenzvorgängen in 20 Work Packages.**
`RISK_REGISTER.md` und `COMPLIANCE_CHECK.md` wurden **nicht** verändert;
die Fortschreibung erfolgt erst in Phase C.

**Die Commitzähler-Governance C3 ist fachlich zur Kenntnis genommen, aber
ausdrücklich nicht Bestandteil von D-056 oder CBP-WP-021.**

**CBP-WP-022 ist nicht registriert und nicht autorisiert.**
