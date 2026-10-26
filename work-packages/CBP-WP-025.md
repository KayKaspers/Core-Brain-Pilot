# CBP-WP-025 — GitHub Repository Ownership Transfer & Rename Governance

## 1. Identität und Metadaten

| Feld | Wert |
| --- | --- |
| Titel | **GitHub Repository Ownership Transfer & Rename Governance** |
| Typ | **Mehrphasiges Governance-/Repository-Operations-Work-Package** |
| Priorität | **P0** — kontrollierte Repository-Governance vor weiteren geplanten Implementierungsschritten |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** (begründet **B3**) |
| Status | **`in-review`** — Phase **X1** ausgeführt, wartet auf Nova-Review und Human-Maintainer-Entscheidung |
| Aktuelle Phase | **X1 – Governance, D-071 und Work-Package-Registrierung** |
| Registration Decision | **D-071** — `accepted`, **A0**, 2026-10-26 — Ergebnis **`CBP_TRANSFER_GOVERNANCE_MODEL_SELECTED_EXECUTION_NOT_AUTHORIZED`** |
| Human-Maintainer-Authority | **A0** vom **2026-10-26**: „GO CBP-TRANSFER-X1 – GOVERNANCE AND WORK PACKAGE REGISTRATION ONLY“; TR-G1 bis TR-G8 ausdrücklich angenommen |
| Review Authority | **Nova** |
| ADR-Gate | **`ADR_NOT_REQUIRED`** — ausschließlich innerhalb der unveränderten Architektur-, Sichtbarkeits- und Publikationsgrenzen (D-071 Teil K) |
| ADR | **keiner** |
| Registrierungsdatum | **2026-10-26** |
| Planungsgrundlage | read-only Intake **CBP-TRANSFER-PRE** vom 2026-10-26 (`DECISION_REQUIRED`); **kein** registriertes Work Package, **keine** Authority |
| Commit | **X1 nicht committed** — Commit und Push ausschließlich durch den Human Maintainer (D-003); keine Selbstreferenz auf einen künftigen Commit |
| Transferstatus | **kein Transfer, keine Umbenennung, kein Remote-Wechsel ausgeführt** |
| CBP-WP-024 | **unabhängig `in-review`** (Phase B0 `committed` `dd72c3f`; B1, B2, B3 und C nicht autorisiert) |
| KB-04-Status | **`DOCUMENTED ONLY`** — unverändert |
| Capabilities | **0 von 29** — unverändert |
| Gates | Mapping Activation `NOT EVALUATED` · Security Foundation Readiness `NOT EVALUATED` |
| R-33 | **`42/24`** — unverändert; kein neuer Vorgang |

## 2. Ausgangslage

Das Core-Repository liegt als persönliches Repository unter
`KayKaspers/Core-Brain-Pilot`. Es soll als **bestehendes** Repository in die
Organisation `blackhole-dynamics` übertragen und anschließend in `Core-Brain`
umbenannt werden — nicht durch Neuanlage und Kopie ersetzt. Erhalt der
Git-Historie, der Repository-Identität, der Zugriffsberechtigungen und der
Governance ist verbindliches Ziel.

Der read-only Intake **CBP-TRANSFER-PRE** (2026-10-26) ergab:

- Quellrepository sauber und synchron, metadatenarm: 1 Branch (`main`),
  0 Tags, 0 Releases, 0 Issues und Pull Requests, 0 Forks, 0 Workflows,
  0 Webhooks, 0 Deploy Keys, 0 Secret-Namen; kein Git LFS, keine Submodule.
- Der Human Maintainer ist **Owner** von `blackhole-dynamics` und darf dort
  Repositories anlegen; ein Repository `Core-Brain` existiert dort nicht.
- Organisations-Rulesets, Actions-Policy, Security-Konfigurationen,
  Org-Webhooks und Org-Secrets waren ohne Admin-Scope **nicht lesbar**.
- Ein vollständiges Git-Backup war **nicht nachgewiesen**.
- **D-069 Teil O** verlangt für Transfer, Umbenennung und Remote-Wechsel eine
  **separate A0-Entscheidung (A0-2)**.

## 3. Autorität und Governance

| Quelle | Klasse | Bindung für CBP-WP-025 |
| --- | --- | --- |
| Human-Maintainer-A0 vom 2026-10-26 (X1, TR-G1 bis TR-G8) | **A0** | Grundlage von D-071 und dieser Registrierung |
| **D-071** | **A0** | konsolidierte Transfer-Governance-Entscheidung (Abschnitt 4) |
| **D-003** | A0 | Commit-, Push- und Release-Autorität ausschließlich beim Human Maintainer |
| **D-029** / ADR-0007 | A0 / A1 | Repository-Zielstruktur und Workspace-Grenze — **keine** Strukturmigration; ein Eigentümerwechsel ist davon getrennt |
| **D-066** | A0 | unverändert; `KB04-T-N07` bleibt zurückgestellt |
| **D-069 Teil O** | A0 | Transfer, Umbenennung und Remote-Wechsel verlangen je eine **separate A0 (A0-2)**; **nicht umgedeutet** |
| ADR-0015 | A1 | Sichtbarkeit PUBLIC, Development State PRIVATE DEVELOPMENT, Product Publication NOT AUTHORIZED — **unverändert** |
| **D-070** | A0 | CBP-WP-024 bleibt unverändert und unabhängig `in-review` |
| NDF v1.0.0 | A1 | normative Baseline |
| CBP-TRANSFER-PRE | — | Planungsgrundlage, **keine** Authority |

## 4. D-071 — Entscheidungsblock

| Feld | Wert |
| --- | --- |
| ID | **D-071** |
| Titel | **CBP REPOSITORY TRANSFER GOVERNANCE AND EXECUTION BOUNDARY** |
| Status | `accepted` |
| Autorität | **A0** — Human Maintainer |
| Datum | **2026-10-26** |
| Work Package | **CBP-WP-025** |
| Ergebnis | **`CBP_TRANSFER_GOVERNANCE_MODEL_SELECTED_EXECUTION_NOT_AUTHORIZED`** |
| ADR-Gate | **`ADR_NOT_REQUIRED`** — ausschließlich innerhalb der unveränderten Architektur-, Sichtbarkeits- und Publikationsgrenzen |

| Teil | Inhalt |
| --- | --- |
| **A — Gegenstand** | Kontrollierte Planung einer GitHub-Eigentümerübertragung und anschließenden Repository-Umbenennung. |
| **B — Quelle** | `KayKaspers/Core-Brain-Pilot`. |
| **C — Ziel** | `blackhole-dynamics/Core-Brain`. |
| **D — TR-G1: Transfermodell** | **Variante B** angenommen: zuerst Ownership-Transfer nach `blackhole-dynamics/Core-Brain-Pilot`, danach gesonderte Umbenennung zu `blackhole-dynamics/Core-Brain`. Zwischen beiden Operationen ist eine **unabhängige Verifikation** erforderlich. |
| **E — TR-G2: Repository-Name** | `Core-Brain` wird **ausschließlich als geplanter Repository-Name** bestätigt. **Keine** Entscheidung über einen öffentlichen Produktnamen; **OD-28 bleibt offen**. Keine neue Branding- oder Produktreifeaussage. |
| **F — TR-G3: Berechtigungen** | Organisationsberechtigungen und relevante Policies werden vor X3 in **X2** erneut geprüft. Bereits vorliegende Nachweise ersetzen diese Prüfung **nicht**. |
| **G — TR-G4: Sichtbarkeit** | Unverändert: Repository Visibility **`PUBLIC`** · Development State **`PRIVATE DEVELOPMENT`** · Product Publication **`NOT AUTHORIZED`** · Lizenz **`UNDECIDED`**. **OD-23 bleibt offen.** |
| **H — TR-G5: Dokumentationsgrenze** | Historische Governance-, Commit- und Architekturbelege bleiben **unverändert**. Aktive operative Referenzen werden erst in einem **separat autorisierten Nachlauf** nachgeführt. **Keine** globale Suche-und-Ersetzen-Aktion. |
| **I — TR-G6: Sicherheit und Integrationen** | Vor und nach dem tatsächlichen Transfer sind zu prüfen: GitHub-Apps · Tokens und repositoryspezifische Berechtigungen · Organisationsrichtlinien · Rulesets und Branch Protection · Security-Konfigurationen · Secrets und Secret-Scanning-Einstellungen · Webhooks · Actions · Teams und Collaborators · externe Integrationen. **Keine** automatische Zugriffserweiterung. **Keine** Secret-Werte erfassen. |
| **J — TR-G7: Backup und Recovery** | Vor X3 sind **verbindlich** nachzuweisen: vollständiges verifiziertes Git-Backup · Git-Referenzinventar · Metadatensnapshot · Organisations-Policy-Snapshot · Wiederherstellungs- und STOP-Plan. Eine vollständige technische Rückabwicklung wird **nicht** garantiert. |
| **K — TR-G8: ADR-Gate** | **`ADR_NOT_REQUIRED`** für den reinen Eigentümer- und Repository-Namenswechsel. Bedingungen: keine Architekturänderung · keine Änderung an ADR-0007 · keine Änderung an ADR-0015 · keine Veränderung des Publikationsstatus · keine Lizenzentscheidung · keine Produktbrandingentscheidung · keine technische Implementierung. Bei Abweichung ist die ADR-Erforderlichkeit **vor** Ausführung erneut zu prüfen. |
| **L — A0-2-Ausführungsgrenze** | Diese A0 autorisiert die Governance-Planung und deren Aufzeichnung. Sie autorisiert **ausdrücklich keine** tatsächliche GitHub-Transfer-, Rename- oder Remote-Operation. Für jede solche Operation bleibt eine **eigenständige, konkrete Human-Maintainer-A0** erforderlich. **D-069 Teil O wird nicht umgedeutet.** |
| **M — Work-Package-Registrierung** | **CBP-WP-025** wird als eigenständiges, mehrphasiges Governance-/Repository-Operations-Work-Package registriert. Priorität **P0**. **CBP-WP-024 bleibt unabhängig `in-review`.** |
| **N — Ausführungsreihenfolge** | **X1 bis X6** mit gesondertem Umbenennungsschritt **X4b**. **Keine** Folgephase durch implizite Freigabe. |
| **O — Governance- und Kennzahlenschutz** | Nach D-071: Decisions **71** · davon A0 **67** · höchste Decision **D-071** · angenommene ADRs **15** · Risiken **35** · R-33 **`42/24`** · Capabilities **0 von 29** · KB-04 **`DOCUMENTED ONLY`** · beide Gates **`NOT EVALUATED`**. |
| **P — Commit-Autorität** | **Exklusiv beim Human Maintainer.** X1 enthält **keine** Freigabe für Staging, Commit oder Push. |

Dieser Block ist mit der Zeile **D-071** im
[Decision Register](../project-system/DECISION_REGISTER.md) **inhaltlich
identisch**. TR-G1 bis TR-G8 sind **Teile** von D-071, keine eigenen
Decision-IDs.

## 5. Ziel und Non-Goals

**Ziel:** Das Core-Repository wird unter Erhalt von Repository-ID, Git-Historie,
Commit-Hashes, Zugriff und Governance von `KayKaspers/Core-Brain-Pilot` über den
Zwischenzustand `blackhole-dynamics/Core-Brain-Pilot` nach
`blackhole-dynamics/Core-Brain` überführt — jeder ausführende Schritt einzeln
freigegeben und unabhängig verifiziert.

**Non-Goals:**

- Kein Produktrelease.
- Keine Lizenz (OD-23 offen).
- Kein Branding (OD-28 offen; DO_NOT_START #11, #12, #13 unverändert).
- Keine Implementierung.
- Keine Deploymentänderung.
- Kein GitHub-Transfer während X1.
- Keine Umbenennung während X1.
- Keine Änderung am lokalen Projektordner `D:\Projects\Core-Brain-Pilot`.
- Keine Änderung an NDF, CDS oder BGRS.
- Keine B1-Freigabe von CBP-WP-024.
- Keine Repository-Strukturmigration nach D-029 / ADR-0007.

## 6. Phasenmodell X1–X6 einschließlich X4b

| Phase | Gegenstand | Autorität | Status |
| --- | --- | --- | --- |
| **X1** | Governance, D-071 und WP-Registrierung | **autorisiert** — Human-Maintainer-A0 vom 2026-10-26 | ausgeführt, **`in-review`**, **nicht committed** |
| **X2** | Berechtigungen, Policies, Vollbackup und Readiness | **nicht autorisiert** | — |
| **X3** | Ownership-Transfer zum Org-Zwischennamen `blackhole-dynamics/Core-Brain-Pilot` | **nicht autorisiert** — eigene A0 (A0-2) | — |
| **X4** | Unabhängige Verifikation des Eigentümerwechsels (Zwischenzustand) | erst nach X3, **gesonderte Freigabe** | — |
| **X4b** | Rename von `Core-Brain-Pilot` zu `Core-Brain`, danach erneute Verifikation des Endzustands | **nicht autorisiert** — eigene A0 (A0-2) | — |
| **X5** | Lokale Remote- und Dokumentations-Reconciliation | **nicht autorisiert** — eigene A0 | — |
| **X6** | Review und Closure | **nicht autorisiert** — eigene A0 | — |

X4 prüft nach erfolgreichem X3 zunächst den **Zwischenzustand**; nach X4b ist
der **endgültige Zielzustand** erneut zu prüfen. Eine allgemeine Freigabe für
die gesamte Sequenz ist **nicht zulässig**. Jede Phase verlangt eine eigene
Human-Maintainer-A0 und endet mit einem Bericht an Nova.

## 7. Abhängigkeiten

| Abhängigkeit | Art |
| --- | --- |
| D-069 Teil O (A0-2) | jede ausführende Operation (X3, X4b, X5-Remote-Wechsel) braucht eine eigene konkrete A0 |
| D-003 | Commit, Push und GitHub-Operationen ausschließlich durch den Human Maintainer |
| ADR-0015 / D-069 | Sichtbarkeit und Publikationsstatus bleiben unverändert |
| D-029 / ADR-0007 | Strukturmigration bleibt ein **eigenes**, nicht autorisiertes Vorhaben |
| CBP-WP-024 | bleibt unabhängig `in-review`; keine gegenseitige Blockade, keine gemeinsame Freigabe |
| Organisation `blackhole-dynamics` | Owner-Rolle des Human Maintainers und Policies sind in X2 erneut zu prüfen |
| Präzedenz | `KayKaspers/Nova-Development-Framework` leitet auf `blackhole-dynamics/Nova-Development-Framework` weiter (CBP-TRANSFER-PRE) — Präzedenz, **keine** Freigabe |

## 8. Pre-Transfer Readiness Contract (X2, nicht autorisiert)

X3 darf erst vorgeschlagen werden, wenn **alle** Punkte in X2 nachgewiesen und
an Nova berichtet sind:

| Nr. | Nachweis | Quelle |
| --- | --- | --- |
| R-1 | Baseline neu gebunden: Branch, HEAD, Parent, `origin/main`, Remote-HEAD, sauberer Index und Worktree | Git, read-only |
| R-2 | Quellrepository: Repository-ID, Owner, Sichtbarkeit, Default Branch, Admin-Recht des Human Maintainers | GitHub, read-only |
| R-3 | Zielorganisation: Owner-Rolle des Human Maintainers, Recht zur Repository-Erstellung, Name `Core-Brain-Pilot` und `Core-Brain` in der Organisation frei | GitHub, read-only |
| R-4 | Organisations-Policies: Rulesets, Actions-Policy, Security-Konfigurationen, Webhooks, Secrets-Sichtbarkeit, Default Permissions — durch den Human Maintainer bestätigt | Organization Settings |
| R-5 | Vollständiges verifiziertes Git-Backup (Abschnitt 11) | Human Maintainer |
| R-6 | Git-Referenzinventar, Metadatensnapshot, Organisations-Policy-Snapshot | X2-Bericht |
| R-7 | Wiederherstellungs- und STOP-Plan für X3 | X2-Bericht |
| R-8 | Security- und Integrationsprüfung „vorher“ (Abschnitt 9) | X2-Bericht |

## 9. Security & Integration Checks

Vor X3 und nach X3 beziehungsweise X4b jeweils zu prüfen (D-071 Teil I).
**Keine Secret-Werte erfassen, nur Existenz und Konfiguration.**

| Bereich | Vorher (X2) | Nachher (X4 / X4b) |
| --- | --- | --- |
| GitHub-Apps (Organisation und persönliches Konto) | Installationen und Repository-Auswahl | keine automatische Zugriffserweiterung auf das übertragene Repository |
| Tokens und repositoryspezifische Berechtigungen | betroffene Tokens benennen | Zugriff erneut prüfen |
| Organisationsrichtlinien | Default Permissions, Repository-Erstellung, 2FA | wirksam auf dem übertragenen Repository |
| Rulesets und Branch Protection | Org-Rulesets mit Zielwirkung | Wirkung auf `main` |
| Security-Konfigurationen | Org-Defaults | Dependabot, Code Scanning, Secret Scanning, Push Protection |
| Secrets und Secret-Scanning-Einstellungen | Anzahl und Sichtbarkeit (keine Werte) | unverändert oder bewusst entschieden |
| Webhooks | Repository und Organisation | keine unerwartete Ereignisweitergabe |
| Actions | Repository- und Org-Policy | Rechte und Default-Workflow-Permissions |
| Teams und Collaborators | Bestand | Rollen nach dem Transfer |
| Externe Integrationen | Nova- und weitere Konnektoren, Werkzeuge mit festem Pfad | Erreichbarkeit unter dem neuen Pfad |

## 10. Repository-Identität und Git-Historie

| Konstante | Wert | Charakter |
| --- | --- | --- |
| Source Repository-ID | `1306799607` | Baseline-Fingerprint |
| Source HEAD | `b3100efcc124915597cc43bd10386de34ea0e7d7` | Baseline-Fingerprint |
| Quelle | `KayKaspers/Core-Brain-Pilot` | Ausgangszustand |
| Zwischenzustand | `blackhole-dynamics/Core-Brain-Pilot` | nach X3 |
| Endzustand | `blackhole-dynamics/Core-Brain` | nach X4b |

Diese Werte sind **Baseline-Fingerprints**, keine Behauptung über den
zukünftigen Ausführungszeitpunkt. Vor jeder ausführenden Phase muss die dann
tatsächlich gültige Baseline **erneut gebunden** werden. Erwartet wird, dass
Repository-ID, Git-Historie und Commit-Hashes durch Transfer und Umbenennung
**unverändert** bleiben; dies ist in X4 und nach X4b **nachzuweisen**, nicht
vorauszusetzen.

## 11. Backup- und Recovery-Voraussetzungen

Vor X3 verbindlich (D-071 Teil J):

1. **Vollständiges verifiziertes Git-Backup** — zum Beispiel Mirror und Bundle
   mit Prüfung und Hash; Ort und Verfahren bestimmt der Human Maintainer in X2.
2. **Git-Referenzinventar** — alle Branches und Tags mit Objekt-IDs.
3. **Metadatensnapshot** — Repository-ID, Beschreibung, Features, Sichtbarkeit,
   Default Branch, Actions-Rechte, Security-Einstellungen, Collaborators.
4. **Organisations-Policy-Snapshot** — durch den Human Maintainer bestätigt.
5. **Wiederherstellungs- und STOP-Plan.**

Ein Git-Backup sichert **nicht** alle GitHub-Metadaten. Ein Rücktransfer ist
möglich, aber **nicht garantiert**; eine vollständige technische Rückabwicklung
wird **nicht** zugesagt. Unter dem alten Pfad darf kein neues Repository
angelegt werden, solange Weiterleitungen benötigt werden.

## 12. Owner-/Rename-Entscheidungsgrenzen

- Der **Owner-Wechsel** (X3) und die **Umbenennung** (X4b) sind **getrennte**
  Operationen mit **je eigener** A0 (D-071 Teil D und L).
- `Core-Brain` ist ein **Repository-Name**, kein Produktname, keine Marke und
  keine Reifeaussage (Teil E); OD-28 bleibt offen.
- Die Einbettung in eine Organisation ist **keine** Produktveröffentlichung
  (Teil G); Product Publication bleibt `NOT AUTHORIZED`.
- Eine Änderung der Sichtbarkeit, eine Lizenz oder eine Aufnahme in das
  Organisationsprofil ist **nicht** Teil dieses Work Packages.

## 13. Post-Transfer-Verifikationsmatrix (X4 und nach X4b)

| Prüfpunkt | Nach X3 (Zwischenzustand) | Nach X4b (Endzustand) |
| --- | --- | --- |
| Repository-ID | `1306799607` | `1306799607` |
| `owner/name` | `blackhole-dynamics/Core-Brain-Pilot` | `blackhole-dynamics/Core-Brain` |
| HEAD `main` | gleich der neu gebundenen Baseline | gleich |
| Branches und Tags | vollständig | vollständig |
| Git-Historie | identisch | identisch |
| Sichtbarkeit | `PUBLIC` | `PUBLIC` |
| Repository-Einstellungen | gegen Metadatensnapshot | gegen Metadatensnapshot |
| Zugriff | Human Maintainer Admin; keine unerwarteten Teams oder Collaborators | gleich |
| Integrationen | Abschnitt 9 „nachher“ | Abschnitt 9 „nachher“ |
| Weiterleitungen | alter Pfad → Zwischenpfad | alter Pfad und Zwischenpfad → Endpfad |
| Governance-Bindungen | D-069, ADR-0015, D-071 unverändert wirksam | gleich |

## 14. Lokale Remote-Reconciliation (X5, nicht autorisiert)

Erst nach erfolgreicher Verifikation des Endzustands und mit eigener
Scope-A0:

- Die lokale Remote-URL wird **durch den Human Maintainer** umgestellt.
- Aktive operative Referenzen werden kontrolliert nachgeführt, insbesondere die
  Remote-Angabe in `project-system/PROJECT_MANIFEST.md`.
- Der lokale Projektordner `D:\Projects\Core-Brain-Pilot` bleibt unverändert;
  eine Umbenennung wäre ein eigenes Vorhaben.
- Verweise auf `KayKaspers/Nova-Development-Framework` sind ein **getrennter**
  Befund aus CBP-TRANSFER-PRE und nur mit eigener Freigabe zu ändern.

## 15. Historischer Aussage- und Dokumentationsschutz

- Historische Governance-, Commit- und Architekturbelege bleiben unverändert
  (D-071 Teil H) — darunter abgeschlossene Work Packages, D-069 Teil O,
  ADR-0007, ADR-0015 und frühere Commit-Statusberichte.
- Lokale Pfadangaben in abgeschlossenen Berichten sind historisch, keine
  aktive Referenz.
- Keine globale Suche-und-Ersetzen-Aktion; jede Änderung ist einzeln
  begründet und an Nova berichtet.

## 16. Abnahmekriterien

**X1:**

- D-071 genau einmal registriert, `accepted`, A0, mit Teilen A bis P;
  Entscheidungsblock und Register-Zeile inhaltlich identisch.
- CBP-WP-025 registriert; X1 `in-review`, nicht committed; X2 bis X6 und X4b
  nicht autorisiert.
- Kennzahlen: Decisions **71**, A0 **67**, höchste **D-071**; ADRs **15**;
  Risiken **35**; R-33 **`42/24`**.
- CBP-WP-024 unverändert `in-review`; kein Work Package `active`.
- Nur Dateien der X1-Allowlist geändert; kein Transfer, keine Umbenennung,
  kein Remote-Wechsel, kein Backup, kein Commit, kein Push.

**Gesamtpaket (Closure in X6):** Endzustand `blackhole-dynamics/Core-Brain` mit
unveränderter Repository-ID, Historie und Governance nachgewiesen; aktive
Referenzen nachgeführt; historische Aussagen unverändert.

## 17. STOP-Bedingungen

- Baseline-Abweichung vor einer ausführenden Phase.
- Fehlende eigene A0 für die jeweilige Phase.
- Nicht verifizierte Organisations-Policy oder Berechtigung.
- Fehlendes oder nicht verifiziertes Vollbackup vor X3.
- Namenskonflikt oder Warnung im Transfer- oder Umbenennungsdialog.
- Abweichende Repository-ID, Historie oder Sichtbarkeit nach X3 oder X4b.
- Unerwartete Zugriffs- oder Integrationsänderung.
- Jede Abweichung von den Bedingungen aus D-071 Teil K (ADR-Gate neu prüfen).
- Jede unerwartete Sicherheitsblockierung.

## 18. Risiken und offene Nachweise (ohne neue Risiko-ID)

| Thema | Bezug | Stand |
| --- | --- | --- |
| Secret im öffentlichen Repository; Secret Scanning und Push Protection laut CBP-TRANSFER-PRE deaktiviert | **R-01** | offen — Prüfung in X2 und X4 |
| Dokumentationsdrift nach Transfer und Umbenennung | **R-16** | offen — X5 |
| Kennzahlen- und Statusspiegel | **R-33** | `42/24`, unverändert |
| Fehlende Restore-Evidenz | **R-20** | Backup in X2 nachzuweisen; Restore nicht geprobt |
| Implizites Veröffentlichungs- oder Open-Source-Signal durch die Organisationseinbettung bei offener Lizenz | Hinweis ohne Registrierung | durch D-071 Teil G und E begrenzt |
| Organisations-Policies nicht lesbar (Rulesets, Actions, Security-Konfigurationen, Webhooks, Secrets) | offener Nachweis | X2 |
| Projects v2, Packages, Apps am persönlichen Konto, externe Referenzen | offener Nachweis | X2 |

Es wird **keine** neue Risiko-ID registriert.

## 19. Status und Next-Gate

| Feld | Wert |
| --- | --- |
| Gesamtstatus | **`in-review`** |
| Phase X1 | ausgeführt, **`in-review`**, **nicht committed** |
| X2 bis X6, X4b | **nicht autorisiert** |
| Next-Gate | Nova-Review von X1, danach Human-Maintainer-Entscheidung über Commit und Push von X1 sowie — gesondert — über eine X2-Freigabe |

## 20. Aussageschutz

| Behauptung | Zutreffend? |
| --- | --- |
| Das Repository sei übertragen oder umbenannt | **nein** — weder Transfer noch Umbenennung ausgeführt |
| D-071 autorisiere einen Transfer, eine Umbenennung oder einen Remote-Wechsel | **nein** — Teil L; jede Operation braucht eine eigene A0 (A0-2) |
| D-069 Teil O sei umgedeutet oder erfüllt | **nein** — unverändert; D-071 ist Governance-Planung |
| `Core-Brain` sei ein Produkt- oder Markenname | **nein** — nur Repository-Name; OD-28 offen |
| Die Organisationseinbettung sei eine Produktveröffentlichung | **nein** — Product Publication `NOT AUTHORIZED` |
| Eine Lizenz sei entschieden | **nein** — OD-23 offen |
| Ein ADR sei angelegt | **nein** — `ADR_NOT_REQUIRED` innerhalb der Bedingungen aus Teil K |
| Ein Backup sei erstellt | **nein** — Voraussetzung für X2/X3 |
| CBP-WP-025 sei `committed` oder `complete` | **nein** — `in-review`; X1 nicht committed |
| CBP-WP-024 sei verändert oder B1 freigegeben | **nein** — unabhängig `in-review`, B1 bis C nicht autorisiert |
| Ein R-33-Vorgang oder eine neue Risiko-ID sei registriert | **nein** — R-33 `42/24`, Risiken 35 |

**Die Registrierung dieses Work Packages ist keine Transferfreigabe.**
