# Risk Register – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Überarbeitet in | **CBP-WP-014** |
| Autoritätsklasse | A2 |
| Stand | 2026-07-22 |

> **Ablageabweichung.** NDF v1.0.0 sieht `project-brain/RISKS.md` vor.
> Es existiert bewusst nur **eine** von beiden — AB-04.

## Bewertung

Schweregrad **hoch / mittel / niedrig** nach Schadenshöhe und Umkehrbarkeit.
Ein irreversibler Schaden ist mindestens **hoch**.

> **Grundsatz aus CBP-WP-003:** Kein Risiko wird geschlossen, weil eine
> **Absicht** genannt wurde. Eine technische Gegenmaßnahme gilt erst nach
> späterer Evidenz als umgesetzt.

## Sicherheit und Datenschutz

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-01 | Secret gelangt in die Git-Historie und ist praktisch nicht mehr entfernbar | **hoch** | Schadensverfahren definiert (SECRET_INCIDENT_RESPONSE, 14 Schritte, Rotation vor Cleanup). **W-3 mindert genau einen Pfad:** private Information → versehentlich in Core → Core-Push → unbeabsichtigte Veröffentlichung. **W-3 implementiert weder Secret-Erkennung noch Rotation, Secret Store, Scanning oder Zugriffskontrolle.** `.gitignore` ist ausdrücklich keine Sicherheitsgrenze | **offen — nur hinsichtlich des Veröffentlichungspfads teilweise gemindert** |
| R-02 | `confidential` oder `excluded-from-ai` gelangt in den Modellkontext | **hoch** | Datenschutzfilter TB-4, fail-closed. **Standardwert 5:** Übertragung an externe KI standardmäßig verweigert | **konkretisiert** |
| R-03 | Datenklassen werden nie konsequent vergeben; Filter laufen ins Leere | **hoch** | Klassenvergabe verpflichtend an TB-1, Vault Doctor. Vergabeverfahren offen (OD-08) | offen |
| R-04 | Prompt Injection aus ingestiertem Material steuert einen Agenten | **hoch** | Ingest ist Daten, nie Anweisung; Quarantäne TB-1. **Durch D-019 verstärkt:** PDF/Office nur über kontrollierte Pipeline | **konkretisiert** |
| R-05 | Inhalte werden an das Claude-Modell übertragen, obwohl ihre Klasse das nicht erlaubt | **hoch** | Datenschutzmatrix; **Standardwert 5** macht Verweigerung zum Normalzustand | **konkretisiert** |
| R-25 | Berechtigungen bestehen nur als Promptregel und nicht technisch | **hoch** | **Modell vollständig dokumentiert** (PERMISSION_MODEL, ADR-0004): 5 Aktionsklassen, 5 Durchsetzungsebenen, Default deny. **Technische Umsetzung existiert nicht** | **verändert, offen** |
| R-26 | Betrieb als Root oder direkt auf dem Proxmox-Host | **hoch** | Ausdrückliches Verbot in TRUST_BOUNDARIES | offen |
| R-27 | Pauschale GitHub-Schreibrechte oder allgemeiner Repository-Schreibzugriff | **hoch** | **Regel gesetzt:** Claude `forbidden` auf `github remote`, nur `draft` auf `git repository`; Push ausschließlich Human Maintainer. Technisch nicht durchgesetzt | **verändert, offen** |
| R-31 | Die Sperrwirkung von `excluded-from-ai` wird nie mit Testdaten geprüft | **hoch** | **Zwei synthetische Fixtures und 6 Datenschutzfragen angelegt**; Leakage ist als kritischer Fehler mit Zielwert 0 definiert. **Prüfung noch nicht durchgeführt** | **gemindert** |

## Wissensintegrität

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-06 | Abgeleitete Inhalte (A6) überschreiben kuratierte (A0–A5) | **hoch** | **ADR-0003:** Einbahnregel TB-3; nur ein autorisierter Schreibpfad nach kanonisch (COMPONENT_MODEL) | **gemindert** |
| R-07 | Indexverlust bedeutet Wissensverlust | **hoch** | **ADR-0003 angenommen**; Rebuild-Vertrag mit Inputs, Versionen, Verifikation und Tombstone-Weg in SYSTEM_ARCHITECTURE | **gemindert** |
| R-08 | Widersprüche werden automatisch aufgelöst statt vorgelegt | mittel | Konflikt-Queue, menschliche Auflösung. **Standardwert 7** | gemindert |
| R-09 | Veraltetes Wissen wird als aktuell ausgeliefert | mittel | Aktualitätsfilter, Supersession | offen |
| R-10 | Nichtdeterministische Indexierung macht Ergebnisse unreproduzierbar | mittel | Determinismus als Akzeptanzkriterium | offen |
| R-11 | Paralleler Schreibzugriff mehrerer Geräte beschädigt den Bestand | mittel | Atomare Änderungen, Mehrschreiberschutz. **Durch D-018 entschärft:** Single-User im Pilot | **verändert** |
| R-22 | Source Drift — A6-Textfassung weicht von der A4-PDF ab | mittel | PDF bleibt Original; visuelle Prüfung nicht behauptet | dokumentiert |
| R-23 | Unvollständiger Quellenabgleich | mittel | Abgleich in SOURCE_RECONCILIATION nachvollziehbar | offen |
| **R-32** | **Nicht-Markdown-Quellen umgehen die Quarantäne und gelangen direkt in den kanonischen Bestand** | **hoch** | D-019 untersagt das ausdrücklich; Capability 5 wird Voraussetzung für PDF/Office | **neu, offen** |

## Projekt und Prozess

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-12 | Vorgezogene Implementierung präjudiziert offene Architekturentscheidungen | **hoch** | Sperrliste `DO_NOT_START.md`, Aufhebung nur per A0 | gemindert |
| R-13 | Scope Creep durch unpriorisierte Capabilities | **hoch** | Priorisierung P0/P1/P2/Deferred; **D-025 vertagt vier Funktionen ausdrücklich** | **gemindert** |
| R-14 | G0 ohne objektive Kriterien | mittel | 47 Kriterien, dreistufig klassifiziert | geschlossen |
| R-15 | Verbindliche Eingangsquellen liegen nicht vor | mittel | Beide Quellen abgeglichen | geschlossen |
| R-16 | Dokumentationsfundament driftet vom tatsächlichen Stand ab | mittel | Pflege in jedem Work Package | offen |
| R-17 | Abweichungen vom NDF wachsen unkontrolliert | niedrig | AB-03 bis AB-08 nur vorläufig akzeptiert | gemindert |
| R-24 | Verwechslung von NDF Prompt Mode und Context Budget | mittel | Ausdrückliche Abgrenzung; D-009 | gemindert |
| R-28 | Ein zweites Governance-System wird eingeführt | mittel | Superpowers nur als Referenz | gemindert |
| R-33 | Fehlerhafte Kennzahlen in Statusdokumenten führen zu falschen Gate-Einschätzungen | mittel | Fünfteilige **Zähl- und Statusregel** in COMPLIANCE_CHECK (CBP-WP-007); Summen gelten als `derived status data`. **Dokumentregel, keine technische Kontrolle.** Der **vierte** Zählfehler entstand in CBP-WP-007 und wurde in CBP-WP-008 gefunden; der **fünfte** in CBP-WP-010 — „neun Blocker" bei acht IDs; der **sechste** in CBP-WP-011 — Gate-Stufenverteilung 25 statt 24, ein Positivtest mit NT-ID, und **doppelt vergebene Test-IDs über Dokumentgrenzen hinweg**. Alle im jeweiligen REWORK-Lauf korrigiert. **Sechs Zählvorgänge in elf Work Packages; jeder durch Auszählung gefunden, keiner durch die Regel verhindert** — diese Aufzählung endet beim **sechsten** Vorgang (CBP-WP-011) und wird nicht rückwirkend umgeschrieben. **Aktueller Stand: 43 Konsistenzvorgänge in 25 Work Packages (`43/25`)** — der Zähler zählt Vorgänge, der Nenner Work Packages mit mindestens einem Vorgang; **kein Erfüllungsgrad**; die vollständige Chronologie steht unten | **gemindert, nicht geschlossen** |
| **R-34** | **Deployment-Required-Kriterien werden vertagt und dann vergessen** | **hoch** | Alle 16 bleiben als `open` erfasst; separates Deployment-Readiness-Gate zu definieren (OD-33). **Fail-closed:** ohne die Angaben wird nicht installiert | **neu, offen** |

## Betrieb

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-19 | Bindung an Proxmox oder Compose sickert in die Architektur ein | mittel | **ADR-0001 angenommen**; fünf Profile beschrieben; Profil B ist der laufende Neutralitätsnachweis | **gemindert** |
| R-20 | Fehlende Restore-Evidenz — Sicherung existiert, Wiederherstellung nie geprobt | **hoch** | **Standardwert 10:** Backup muss vor produktivem Betrieb eingerichtet **und getestet** sein. **Seit ADR-0007 erweitert sich der Umfang:** Der private Operator-Workspace enthält **nicht reproduzierbare kanonische Registry-Metadaten**, und **RT-2 Operational Evidence** (Audit-, Approval-, Incident- und Restore-Nachweise) ist ebenfalls **nicht vollständig rekonstruierbar**. Beide müssen in Backup-, Restore- und Aufbewahrungsregeln einbezogen werden (RG-4). Zielwerte weiterhin offen (F-4) | **verändert, offen** |
| R-21 | Retrieval-Qualität verschlechtert sich unbemerkt | mittel | **Benchmark entworfen** (Dataset **2.0.0**): 36 Fragen, 4 Metrikgruppen, Regressionsregeln bei 7 Systemänderungen. **Kein Lauf durchgeführt.** Auflage 3 der G0-Entscheidung; Backlogpunkt P7 | **gemindert, nicht geschlossen** |
| R-29 | Produktive Synchronisation ohne Test-Vault führt zu Datenverlust | **hoch** | **D-025 vertagt native Obsidian-Nutzung**; Freigabe erst nach Test-Vault, Konflikt- und Restore-Prüfung | **gemindert** |
| R-30 | Datenschutzklassifikation ohne technische Durchsetzung | **hoch** | **D-021 macht daraus eine prüfbare Anforderung** — Sperrwirkung mit Testdaten nachzuweisen | **konkretisiert** |
| **R-35** | **Reale KB-04-Nachweisausführung trifft eine falsche oder unzureichend isolierte Zielinstanz** | **hoch** | **Auslöser:** falsche Zielinstanz · falscher Host · nicht ausreichend isolierte Referenzumgebung · produktive oder wiederverwendete Datenstruktur · Übertragung einer alten Freigabe auf einen anderen Lauf. **Auswirkung:** Beschädigung realer Daten · Veränderung einer nicht autorisierten Instanz · ungültige oder falsch zugeordnete Nachweise · Verletzung der Public- und Operational-Boundary. **Gegenmaßnahmen (D-063):** dedizierte, nicht produktive VM · lokal eindeutig bezeichnete Zielinstanz · **nachweislich neue und leere** Zielstruktur (Contract §9.1) · **einmalige, nicht übertragbare Freigabe je Lauf** · unmittelbare Zielbestätigung vor dem Start · **Stop bei jeder Abweichung**. **Restgrenze:** eine organisatorische Fehlbindung bleibt möglich; **das Repository kennt die reale Zielinstanz nicht**. **Betroffene Phase: B2D-E.** Integriert die B2D-P-Kandidaten *falsche Zielinstanz*, *unzureichende Isolation*, *Ausführung auf dem falschen Host* sowie *Beschädigung realer Daten* als **Auswirkung**. **Ersetzt weder R-26 noch R-29 noch R-32**; macht **keine** produktive Ausführung zulässig; **B2D-E bleibt nicht autorisiert** | **neu, offen** |
| **R-36** | **Reale KB-04-Nachweisausführung beginnt ohne bestätigten Wiederherstellungspunkt** | **hoch** | **Auslöser:** kein Snapshot · kein gleichwertiger Recovery-Punkt · Recovery-Punkt nicht bestätigt · Recovery-Punkt nicht mehr gültig · Wiederherstellungsweg nicht nachweislich verfügbar. **Auswirkung:** unerwartete Änderungen können nicht zuverlässig zurückgeführt werden · Daten- oder Zustandsbeschädigung bleibt bestehen · die Ausführung kann nicht sicher abgebrochen und zurückgesetzt werden. **Gegenmaßnahmen (D-063):** **Recovery-Gate R-1 bis R-4** der Profile-A-Plandatei · **kein Start ohne bestätigten Recovery-Punkt** · Bestätigung des Recovery-Status unmittelbar vor dem Lauf · **Freigabe bei jeder Änderung verwerfen**. **Restgrenze:** ein vorhandener Recovery-Punkt garantiert **nicht** automatisch eine erfolgreiche Wiederherstellung. **Betroffene Phase: B2D-E.** Der **Contract enthält keine Rollbackzusage** (§9.3) — das Recovery-Gate ist eine **Nova-Ausführungsvoraussetzung**. **R-20 wird weder geschlossen noch ersetzt noch erweitert**; **in diesem Lauf wurde kein Snapshot erzeugt** | **neu, offen** |

## Zusammenfassung

| Schwere | Anzahl |
| --- | --- |
| hoch | **20** |
| mittel | **14** |
| niedrig | **1** |
| **Summe** | **35** |

| Status | Anzahl |
| --- | --- |
| geschlossen | 2 |
| gemindert | **14** |
| konkretisiert | 4 |
| dokumentiert | 1 |
| teilweise gemindert | 1 |
| offen | **13** |

> **Aggregatreconciliation in CBP-WP-022 Phase B2D-GOV (D-063).** Die zuvor
> ausgewiesenen Werte **hoch 17 · mittel 13 · niedrig 2 · Summe 32** waren
> **nicht konsistent** mit den damals **33** kanonischen Risikodatensätzen.
> Die Reconciliation beruht auf einer **vollständigen Neuauszählung aller
> kanonischen Risikozeilen**, nicht auf einer Fortschreibung.
>
> **Die Abweichung ließ sich nicht allein R-34 zuschreiben.** Sie zerfiel in
> **zwei voneinander unabhängige Fehler**: erstens war **R-34** in beiden
> Aggregattabellen **nicht mitgezählt** — das erklärt `hoch` und die Summe;
> zweitens war der **`mittel`/`niedrig`-Schnitt falsch** — ausgewiesen
> **13/2**, kanonisch **14/1**, wobei **R-17** die einzige Zeile mit Schwere
> `niedrig` ist. Der zweite Fehler betrifft **ausschließlich die
> Schweretabelle**; die Statustabelle war allein durch die R-34-Auslassung
> verschoben (`offen` **10** statt **11**).
>
> **Auszählung vor den neuen Risiken:** hoch **18** · mittel **14** · niedrig
> **1** · gesamt **33**. **Nach Aufnahme von R-35 und R-36** — beide **hoch**
> und **offen** —: hoch **20** · mittel **14** · niedrig **1** · gesamt
> **35**; `offen` **13** (11 + 2).
>
> **R-33 bleibt unverändert in seinem bisherigen Status. Diese Reconciliation
> schließt R-33 nicht** — sie ist ein weiterer belegter Vorgang seiner
> Fehlerklasse, keine Behebung ihrer Ursache. **R-01 bis R-34 sind
> inhaltlich unverändert**, **R-18 bleibt eine nicht wiederverwendete
> Nummernlücke**, und es wurde **keine R-37** vergeben.

**Neu in CBP-WP-025 (Phase X1-C3 — R-33-Vorgang 43):** keine.

**Verändert in CBP-WP-025 Phase X1-C3 — rein dokumentarisch, ohne Schwere- oder
Statusänderung:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| **R-33** | **Dreiundvierzigster Konsistenzvorgang** — **CBP-WP-025 Active X1 Commit-status Mirrors Staleness** (`X1-PCR-F01`) (siehe Chronologie unten); Zuordnung **CBP-WP-025**, erstes R-33-Erfassen; **`42/24 → 43/25`**; Status `gemindert, nicht geschlossen` und Kritikalität **mittel** unverändert | Human-Maintainer-A0 vom 2026-10-26 („GO CBP-WP-025 X1-C3 – POST-COMMIT STATUS RECONCILIATION") |

**Kein Risiko wurde in CBP-WP-025 Phase X1-C3 geschlossen**, keine Schwere und
kein Status geändert, **keine neue Risiko-ID** vergeben: Risiken **35**, Severity
**20/14/1**.

**Neu in CBP-WP-024 (Phase B0-R2 — R-33-Vorgang 42):** keine.

**Verändert in CBP-WP-024 Phase B0-R2 — rein dokumentarisch, ohne Schwere- oder
Statusänderung:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| **R-33** | **Zweiundvierzigster Konsistenzvorgang** — **Active A0 Counter Mirror Staleness** (`B0-R1-F01`) (siehe Chronologie unten); Zuordnung **CBP-WP-024**, erstes R-33-Erfassen; **`41/23 → 42/24`**; Status `gemindert, nicht geschlossen` und Kritikalität **mittel** unverändert | Human-Maintainer-A0 vom 2026-10-22 (HD-8, Klassifikation **Z-1**) |

**Kein Risiko wurde in CBP-WP-024 Phase B0-R2 geschlossen**, keine Schwere und
kein Status verändert, **keine neue Risiko-ID** vergeben. Risiken **35** (hoch
**20** · mittel **14** · niedrig **1**), `offen` **13**, gemindert **14** —
unverändert. Der Driftkandidat **DK-3** (DRC-Gatestatus, Umfeld Vorgang **39**)
bleibt **gesondert** und ohne Zählwirkung.

**Neu in CBP-WP-022 (Phase C — dokumentarische Closure):** keine.

**Verändert in CBP-WP-022 Phase C — rein dokumentarisch, ohne Schwere- oder
Statusänderung:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| **R-33** | **Einundvierzigster Konsistenzvorgang** — **Residual WP-023 Registration Lifecycle Statement Staleness** (siehe Chronologie unten); Zuordnung **CBP-WP-023**, erstes R-33-Erfassen; **`40/22 → 41/23`**; Status `gemindert, nicht geschlossen` und Kritikalität **mittel** unverändert | Human-Maintainer-A0 vom 2026-10-19 (E-1, Klassifikation K-3) |

**Kein Risiko wurde in CBP-WP-022 Phase C geschlossen**, keine Schwere und kein
Status verändert, **keine neue Risiko-ID** vergeben. Risiken **35** (hoch
**20** · mittel **14** · niedrig **1**), `offen` **13**, gemindert **14** —
unverändert. **R-01**, **R-16**, **R-20**, **R-35** und **R-36** bleiben
unverändert; die reale KB-04-Ausführung, auf die sich **R-35** und **R-36**
beziehen, bleibt nach **D-068** herausgenommen und nicht autorisiert.

**Neu in CBP-WP-023 (Phase G1, uncommitted Review-Diff):** keine.

**Verändert in CBP-WP-023 (Phase G1) — rein dokumentarisch, ohne Schwere- oder
Statusänderung:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| **R-01** | **Neubewertung des öffentlichen Repositorybetriebs (2026-10-17).** Das Repository ist **öffentlich sichtbar** (D-069); jeder Push des Human Maintainers macht Commits samt Historie **unmittelbar öffentlich einsehbar**. Der in der Gegenmaßnahme genannte Pfad *Core-Push → unbeabsichtigte Veröffentlichung* ist damit **tatsächlich aktiv** und kein hypothetischer Folgeschritt mehr; W-3 mindert weiterhin nur den **Eintrittspfad** (privater Bestand gelangt nicht in das Core-Repository), nicht die Folge eines Fehlers. Zu berücksichtigen sind insbesondere: **versehentliche Commits** sensibler Inhalte · **automatisiert erzeugte oder importierte Dateien** im Worktree · **GitHub-Schutzfunktionen** (etwa Secret Scanning, Push Protection), die **nicht als aktiviert nachgewiesen** sind · die **verpflichtende Vertraulichkeitsprüfung des Diffs vor jedem Human-Maintainer-Push** (D-069 Teil I). Diese Prüfung ist eine **dokumentierte Anforderung, keine implementierte Kontrolle**; **keine Schutzmaßnahme wird als umgesetzt behauptet**. Der read-only Audit vom 2026-10-17 fand keine kritischen Befunde (CF-01, CF-02 als niedrige Hinweise akzeptiert) — **ein negativer Audit ist keine Sicherheitsgarantie**. Schwere **hoch** und Status-Wortlaut **unverändert** (`offen — nur hinsichtlich des Veröffentlichungspfads teilweise gemindert`; in der Statusauszählung unverändert unter `teilweise gemindert`) | D-069, ADR-0015 (`proposed`) |
| **R-16** | **Zählneutrale Notiz zur Sichtbarkeits-Governance-Abweichung.** Zu unterscheiden sind: (1) der **historische Governance-Stand** — ADR-0006 (Klarstellungsnachtrag, Folgerung 2), ADR-0007 und aktive Statusspiegel führten das Repository als „privat", OD-11 war offen; (2) der **frühere faktische Zustand** — GitHub wies das Repository als öffentlich aus, der **Zeitpunkt des Wechsels ist nicht belegt**; (3) die **Human-Maintainer-A0 vom 2026-10-17** (A0-1); (4) **D-069**, die PUBLIC als künftigen Sollzustand bestätigt, **ohne** die frühere Abweichung rückwirkend zu legitimieren; (5) **ADR-0015 `proposed`** (Annahme erst in G2); (6) die **Nachführung der aktiven Statusspiegel** im G1-Review-Diff. Historische Aussagen bleiben unverändert. Gemäß Human-Maintainer-Klassifikation ist dies ein **R-16-Fall** und **kein R-33-Vorgang**; Schwere **mittel** und Status **offen** unverändert | D-069 |

**Kein Risiko wurde in CBP-WP-023 G1 geschlossen**, keine Schwere und kein
Status verändert, **keine neue Risiko-ID** vergeben. Risiken **35** (hoch
**20** · mittel **14** · niedrig **1**), `offen` **13**, gemindert **14** —
unverändert. **R-33 bleibt `40/22`**; ein Vorgang 41 ist **nicht**
registriert. Der Altdrift-Prüfbestand **D-1 bis D-10** bleibt unverändert
**ungelöst**.

**Fortschreibung in CBP-WP-023 Phase G2 (uncommitted Review-Diff) — keine
Risikoänderung:** **ADR-0015** ist durch ausdrückliche Human-Maintainer-A0 vom
2026-10-17 **`accepted`** (A1); die Sichtbarkeitsaussagen in ADR-0006 und
ADR-0007 sind **partiell abgelöst**, beide bleiben im Übrigen `accepted`. Die
Angaben „ADR-0015 (`proposed`)" in der Zeile **R-01** (*Auslöser*) und
„ADR-0015 `proposed` (Annahme erst in G2)" in der Zeile **R-16** (Punkt 5) geben
den **Stand G1** wieder und bleiben als G1-Nachweis unverändert. **R-01** bleibt
**hoch**, Status-Wortlaut unverändert (`offen — nur hinsichtlich des
Veröffentlichungspfads teilweise gemindert`; in der Statusauszählung unter
`teilweise gemindert`); **R-16** bleibt **mittel** und **offen**; die
R-16-Fallnotiz gilt unverändert. Risiken
**35**, **keine neue Risiko-ID**, **R-33 bleibt `40/22`**, **kein Vorgang 41**:
die Nachführung des ADR-Status ist Teil der G2-Annahme selbst und **kein**
Konsistenzvorgang.

**Neu in CBP-WP-012:** keine.

**Neu in CBP-WP-015:** keine.

**Verändert in CBP-WP-015:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| **R-33** | **Ein neuer, datierter Konsistenzvorgang (der neunte):** die aktuellen A3-Planungsangaben nannten **19** Mapping-Felder, während der angenommene A1/A2-Vertrag **31 Felddefinitionen** (29 Pflicht + 2 optional, 24 Regeln) umfasst. Betroffen: `docs/roadmap/PILOT_SOURCE_MAPPING_PLAN.md`, `docs/roadmap/PHASE_1_EVIDENCE_PLAN.md`. Korrigiert durch transparente Korrekturhinweise (keine Umschreibung der Entscheidungshistorie). Test- (**315**), Git-, Entscheidungs- (D-046…D-049) und ADR-Zahlen aus den tatsächlichen Ausgaben ausgezählt. **Dokumentregel, keine Kontrolle** | CBP-WP-015 |

**Kein Risiko wurde in CBP-WP-015 geschlossen.** Ein synthetisch testbarer,
read-only Mapping-Draft-Validator ist keine reale Source Governance und keine
Gate-Ausführung. **R-33 bleibt offen.**

**Neu in CBP-WP-014:** keine.

**Verändert in CBP-WP-014:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| **R-33** | Test- (**212**), Git-, Entscheidungs- (D-042…D-045) und ADR-Zahlen aus den tatsächlichen Ausgaben bzw. Quelltabellen ausgezählt; Risikomengen A (6) / B (5) / C (11) kanonisch getrennt geführt. **Dokumentregel, keine Kontrolle** | CBP-WP-014 |

**Kein Risiko wurde in CBP-WP-014 geschlossen.** Ein synthetisch testbarer,
**deaktivierter** Registry-Prototyp ist keine reale Source Governance: er
berührt keine reale Quelle, erzeugt kein Mapping und aktiviert nichts
(`activate` verweigert immer). **R-33 bleibt offen.**

**Neu in CBP-WP-013:** keine.

**Verändert in CBP-WP-013:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| **R-32** | Ein lokaler, synthetisch testbarer Quarantäne**prototyp** existiert (getestete Pre-Ingest-Grenze, fail-closed, keine Promotion). **Lokal teilweise gemindert, nicht geschlossen** — die produktive Quarantäne, die OS-Isolation (OD-37) und die Nicht-Markdown-Quarantäne existieren nicht. Status unverändert `offen` | CBP-WP-013, D-038…D-041 |
| **R-01** | Deterministische Baseline-Indikatoren blockieren offensichtliche Credential-/Private-Key-Marker in **synthetischen** Testdaten. **Lokal teilweise berührt, nicht geschlossen** — keine vollständige Secret-Erkennung, keine reale Quelle, keine technische Erkennung im Bestand (OD-38). Status unverändert `offen` | CBP-WP-013, D-040 |
| **R-33** | Testzahl **137** und Git-Inventar aus dem tatsächlichen Lauf bzw. `git status --porcelain=v1 -uall` ausgezählt; zwei Testdefekte vor dem grünen Lauf gefunden (beide in Tests). **Dokumentregel, keine Kontrolle** | CBP-WP-013 |

**Kein Risiko wurde in CBP-WP-013 geschlossen.** Ein synthetisch testbarer
Prototyp ist keine durchgesetzte Kontrolle: er berührt keine reale Quelle,
erzwingt keine OS-Isolation und behauptet keine vollständige Secret- oder
PII-Erkennung. **R-01, R-32 und R-33 bleiben offen.**

**R-33-Chronologie — achter Konsistenzvorgang (CBP-WP-013, 2026-07-22):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-013** |
| Fehlerklasse | **dokumentübergreifender Mengen- und Terminologiekonsistenzfehler** (kein arithmetischer Zählfehler) |
| Betroffene Repository-Artefakte | `work-packages/CBP-WP-013.md`, `docs/runtime/INGEST_QUARANTINE_EVIDENCE.md` |
| Tatsächlicher Fehler | Die Mengen A (6), B (5) und C (11) waren **numerisch korrekt**. Die Vereinigungsmenge **C** wurde jedoch fälschlich als „vollständige kritische Liste" bezeichnet; die Gruppe **B** wurde als „offen/hoch" bezeichnet, obwohl **R-33** die Kritikalität **mittel** besitzt |
| Korrektur | A bleibt die kuratierte Registerliste „Weiterhin kritisch" (6 IDs); B bleibt „Zusätzliche offene Beobachtungsrisiken" (5 IDs); C bleibt „Gesamte beobachtete Risikomenge" (11 IDs) und wird **nicht** als kritische Liste bezeichnet; kein mittel-Risiko wird als hoch bezeichnet |
| Aussagegrenze | **Keine** Risikokritikalität verändert; **kein** Risiko geschlossen; die technische Quarantäneimplementierung **unverändert** |

Damit sind **acht Konsistenzvorgänge in dreizehn Work Packages** dokumentiert;
jeder durch Auszählung bzw. Terminologieprüfung gefunden, keiner durch die Regel
verhindert. **R-33 bleibt `gemindert, nicht geschlossen`** — dieser Eintrag
ändert den Status nicht. Die kanonische Chronologietabelle steht in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md); frühere Einträge sind unverändert.

**R-33-Chronologie — neunter Konsistenzvorgang (CBP-WP-015, 2026-07-27):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-015** |
| Fehlerklasse | **veraltete Feldzahlangabe in A3-Planungsartefakten** — die aktuellen Angaben nannten **19** Felder, während der angenommene A1/A2-Vertrag **31 Felddefinitionen** umfasst |
| Betroffene aktuelle Repository-Artefakte | `docs/roadmap/PILOT_SOURCE_MAPPING_PLAN.md`, `docs/roadmap/PHASE_1_EVIDENCE_PLAN.md` |
| Tatsächlicher Fehler | Beide A3-Dokumente führten „19 Felder" (bzw. „M1–M14") als Planungsannahme aus CBP-WP-008 fort. Der angenommene Vertrag (ADR-0008, CBP-WP-010) hat **31 Felddefinitionen** — **29 Pflichtfelder** und **zwei optionale Felder** — sowie **24 Validierungsregeln** (V1–V24) |
| Korrektur | Transparente 19/31-Korrekturhinweise in beiden Dokumenten; die historischen 19-Feld-/M1–M14-Angaben bleiben als **abgelöste Planungsannahme** erhalten und werden **nicht** rückwirkend umgeschrieben. Die historische Queue-Aussage zu CBP-WP-008 wird separat als historisch gekennzeichnet |
| Aussagegrenze | **Der akzeptierte 31-Feld-Vertrag wurde nicht verändert**; **kein** Feld hinzugefügt/entfernt/umbenannt; **keine** Risikokritikalität verändert; **kein** Risiko geschlossen |

Damit waren **neun Konsistenzvorgänge in fünfzehn Work Packages** dokumentiert
(*Stand nach dem neunten Vorgang; durch den zehnten Vorgang unten auf **zehn**
aktualisiert*); jeder durch Auszählung bzw. Quellenabgleich gefunden, keiner
durch die Regel verhindert. **R-33 bleibt `gemindert, nicht geschlossen`** —
dieser Eintrag ändert den Status und die Kritikalität (**mittel**) nicht.
Derselbe Vorgang ist in [COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und
zählt **nur einmal**.

**R-33-Chronologie — zehnter Konsistenzvorgang (CBP-WP-015 Post-Commit Status Reconciliation, 2026-07-27):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-015** (Post-Commit-Status-Reconciliation; kein neues Work Package) |
| Fehlerklasse | **Git-/Register-Statusabweichung** — nach Commit und Push von CBP-WP-015 (`645ccb1`) blieb der formale A2-Status in mehreren Statusdokumenten auf `in-review`, obwohl Git CBP-WP-015 bereits als `committed` und mit origin/main synchron auswies |
| Betroffene aktuelle Repository-Artefakte | `README.md`, `CLAUDE.md`, `project-system/WORK_PACKAGE_QUEUE.md`, `project-system/PROJECT_MANIFEST.md`, `project-brain/PROJECT_BRAIN.md` |
| Ursache | Der Implementation Commit trug den korrekten **Vor-Commit-Reviewstatus** `in-review`; es fehlte anschließend eine **Post-Commit-Status-Reconciliation** |
| Korrektur | Die kanonischen Statusdokumente wurden auf den durch Git belegten `committed`-Zustand von CBP-WP-015 synchronisiert; CBP-WP-016 bleibt `proposed`, kein Work Package ist `active` |
| Aussagegrenze | **Kein Funktionsfehler, keine Runtimeänderung, keine Gatefreigabe, keine Aktivierung, keine Capability-Änderung**; keine neue Decision-ID, kein neues ADR, kein neues/geschlossenes Risiko; **keine** Risikokritikalität verändert |

Damit waren **zehn Konsistenzvorgänge in fünfzehn Work Packages** dokumentiert
(*Stand nach dem zehnten Vorgang; durch den elften Vorgang unten auf **elf**
aktualisiert*; löst die vorige Angabe „neun" ab). Die Zahl der Work Packages
bleibt **fünfzehn**, weil dieser Vorgang erneut **CBP-WP-015** betrifft und
**kein** neues Work Package hinzukommt. **R-33 bleibt `gemindert, nicht
geschlossen`**, Kritikalität unverändert **mittel**. Derselbe Vorgang ist in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und zählt **nur einmal**.

**R-33-Chronologie — elfter Konsistenzvorgang (CBP-WP-014/015 Queue Detail Block Reconciliation, 2026-07-27):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-014 und CBP-WP-015** (Queue-Detailblock-Nachführung; kein neues Work Package) |
| Fehlerklasse | **Git-/Register-Statusabweichung in Detailblöcken** — in `project-system/WORK_PACKAGE_QUEUE.md` blieben die Detailblöcke von CBP-WP-014 (`Status in-review`, „Commit nicht ausgeführt") und CBP-WP-015 (`vorgeschlagen, nicht freigegeben`, `proposed`) auf Vor-Commit- bzw. Vor-Autorisierungsständen, obwohl Git, Queue-Übersicht und zentrale Statusfelder beide bereits als `committed` belegten |
| Betroffene aktuelle Repository-Artefakte | `project-system/WORK_PACKAGE_QUEUE.md` (Detailblöcke CBP-WP-014 und CBP-WP-015) |
| Ursache | Frühere Status-Reconciliations prüften Header, Übersicht und zentrale Statusfelder, erfassten jedoch nicht sämtliche **Detailblöcke** der Queue |
| Korrektur | Detailblock CBP-WP-014 auf `committed` + `Git-Beleg d0c0531` synchronisiert; Detailblock CBP-WP-015 auf `committed`, `645ccb1` und Reconciliation `8d715e7` synchronisiert; frühere Planungs-/Freigabestände nur noch ausdrücklich historisch gekennzeichnet |
| Aussagegrenze | **Keine Codeänderung, keine Runtimeänderung, keine Gatefreigabe, keine Aktivierung, keine Capability-Änderung**; keine neue Decision-ID, kein neues ADR, kein neues/geschlossenes Risiko; **keine** Risikokritikalität verändert; CBP-WP-016 bleibt `proposed` |

Damit waren **elf Konsistenzvorgänge in fünfzehn Work Packages** dokumentiert
(*Stand nach dem elften Vorgang; durch den zwölften Vorgang unten auf **zwölf**
aktualisiert*; löst die vorige Angabe „zehn" ab). Die Zahl der
Work Packages blieb zu diesem Zeitpunkt **fünfzehn**, weil dieser Vorgang
**CBP-WP-014** und **CBP-WP-015** betrifft, die bereits Teil der bisherigen Menge
sind, und **kein** neues Work Package hinzukommt. **R-33 bleibt `gemindert, nicht
geschlossen`**, Kritikalität unverändert **mittel**. Derselbe Vorgang ist in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und zählt **nur einmal**.

**R-33-Chronologie — zwölfter Konsistenzvorgang (CBP-WP-016 Post-Commit Status Reconciliation, 2026-07-28):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-016** (Post-Commit-Status-Reconciliation; kein neues Work Package im Sinne einer neuen Ausführung, aber **erstes** R-33-Erfassen von CBP-WP-016) |
| Fehlerklasse | **Git-/Register-Statusabweichung** — nach Commit und Push von CBP-WP-016 (`04c427c`) führten mehrere Statusdokumente CBP-WP-016 weiterhin als `in-review` bzw. „nicht committet", obwohl Git CBP-WP-016 als `committed` und mit origin/main synchron auswies |
| Betroffene aktuelle Repository-Artefakte | `README.md`, `CLAUDE.md`, `project-system/WORK_PACKAGE_QUEUE.md` (Header, Übersicht, Detailblock), `project-system/PROJECT_MANIFEST.md`, `project-system/PROJECT_PROFILE.md`, `project-system/HEALTH_SCORE.md`, `project-brain/PROJECT_BRAIN.md` |
| Ursache | Der Implementation Commit trug den korrekten **Vor-Commit-Reviewstatus** `in-review`; es fehlte anschließend eine **Post-Commit-Status-Reconciliation** (dieselbe Klasse wie der zehnte Vorgang für CBP-WP-015) |
| Korrektur | Die kanonischen Statusdokumente wurden auf den durch Git belegten `committed`-Zustand von CBP-WP-016 (`04c427c`) synchronisiert; „aktuelles Work Package" auf **keines aktiv, zuletzt abgeschlossen CBP-WP-016** gesetzt; kein Work Package ist `active`/`in-review`; **CBP-WP-017 nicht autorisiert** |
| Aussagegrenze | **Kein Funktionsfehler, keine Runtimeänderung, keine Gatefreigabe, keine Aktivierung, keine Capability-Änderung**; keine neue Decision-ID, kein neues ADR, kein neues/geschlossenes Risiko; **keine** Risikokritikalität verändert; Mapping Activation Gate/Security Foundation Readiness Gate/DRC bleiben `NOT EVALUATED`; Capabilities **0 von 29** |

Damit waren **zwölf Konsistenzvorgänge in sechzehn Work Packages** dokumentiert
(*Stand nach dem zwölften Vorgang; durch den dreizehnten Vorgang unten auf
**dreizehn** aktualisiert*; löst die vorige Angabe „elf" ab). Die Zahl der
Work Packages stieg auf **sechzehn**, weil dieser Vorgang **erstmals
CBP-WP-016** betraf, das durch den Commit `04c427c` Teil der committeten Menge
wurde. **R-33 bleibt `gemindert, nicht geschlossen`**, Kritikalität unverändert
**mittel**. Derselbe Vorgang ist in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und zählt **nur einmal**.

**R-33-Chronologie — dreizehnter Konsistenzvorgang (CBP-WP-017 Post-Commit Status Reconciliation, 2026-07-28):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-017** (Post-Commit-Status-Reconciliation; **erstes** R-33-Erfassen von CBP-WP-017) |
| Fehlerklasse | **Git-/Register-Statusabweichung** — nach Commit und Push von CBP-WP-017 (`d3168c4`) führten mehrere Statusdokumente CBP-WP-017 weiterhin als `in-review` bzw. „nicht committet", obwohl Git CBP-WP-017 als `committed` und mit origin/main synchron auswies |
| Betroffene aktuelle Repository-Artefakte | `README.md`, `CLAUDE.md`, `project-system/WORK_PACKAGE_QUEUE.md` (Header, Übersicht, Detailblock), `project-system/PROJECT_MANIFEST.md`, `project-system/PROJECT_PROFILE.md`, `project-system/HEALTH_SCORE.md`, `project-brain/PROJECT_BRAIN.md` |
| Ursache | Der Implementation Commit trug den korrekten **Vor-Commit-Reviewstatus** `in-review`; es fehlte anschließend eine **Post-Commit-Status-Reconciliation** (dieselbe Klasse wie der zehnte/zwölfte Vorgang) |
| Korrektur | Die kanonischen Statusdokumente wurden auf den durch Git belegten `committed`-Zustand von CBP-WP-017 (`d3168c4`) synchronisiert; „aktuelles Work Package" auf **keines aktiv, zuletzt abgeschlossen CBP-WP-017** gesetzt; kein Work Package ist `active`/`in-review`; **CBP-WP-018 nicht autorisiert** |
| Aussagegrenze | **Kein Funktionsfehler, keine Runtimeänderung, keine Gatefreigabe, keine Aktivierung, keine Capability-Änderung**; keine neue Decision-ID, kein neues ADR, kein neues/geschlossenes Risiko; **keine** Risikokritikalität verändert; Mapping Activation Gate/Security Foundation Readiness Gate/DRC bleiben `NOT EVALUATED`; Capabilities **0 von 29** |

Damit waren **dreizehn Konsistenzvorgänge in siebzehn Work Packages** dokumentiert
(*Stand nach dem dreizehnten Vorgang; durch den vierzehnten Vorgang unten auf
**vierzehn** aktualisiert*; löst die vorige Angabe „zwölf" ab). Die Zahl der
Work Packages stieg auf **siebzehn**, weil dieser Vorgang **erstmals
CBP-WP-017** betraf, das durch den Commit `d3168c4` Teil der committeten Menge
wurde. **R-33 bleibt `gemindert, nicht geschlossen`**, Kritikalität unverändert
**mittel**. Derselbe Vorgang ist in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und zählt **nur einmal**.

**R-33-Chronologie — vierzehnter Konsistenzvorgang (CBP-WP-018 Phase B0 — ADR-Index-Zählkorrektur, 2026-07-28):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-018** (Governance Foundation, Phase B0; **erstes** R-33-Erfassen von CBP-WP-018) |
| Fehlerklasse | **Vorbestehender Zählfehler in einem kanonischen Statusartefakt** (kein Post-Commit-Vorgang, kein arithmetischer Summenfehler im Register) — der kanonische ADR-Index `docs/decisions/README.md` wies im Kopf-Feld „Angenommene ADRs" **elf** aus, obwohl ADR-0001 bis ADR-0012 **bereits existierten** (der korrekte Wert vor CBP-WP-018 war **zwölf**) |
| Betroffene aktuelle Repository-Artefakte | `docs/decisions/README.md` (ADR-Index-Kopf, Prosa, Tabelle) |
| Ursache | Der ADR-Index wurde nach der Aufnahme von **ADR-0012** (CBP-WP-015) nicht auf zwölf nachgeführt; der Zähler blieb auf dem älteren Stand elf stehen. Der Fehler wurde erst im Governance-Diff von CBP-WP-018 sichtbar. |
| Korrektur | Der ADR-Index wurde beim Hinzufügen von **ADR-0013** auf den durch Auszählung belegten Gesamtwert **13** gesetzt (11 → 13, davon der vorbestehende Fehler 11 → 12 plus die Ergänzung 12 → 13). Kein ADR wurde inhaltlich umgeschrieben. |
| Aussagegrenze | **Kein Funktionsfehler, keine Runtimeänderung, keine Gatefreigabe, keine Aktivierung, keine Capability-Änderung**; keine neue Decision-ID, kein neues ADR **über ADR-0013 hinaus**, kein neues/geschlossenes Risiko; **keine** Risikokritikalität verändert; D-052/ADR-0013 unverändert; Gates `NOT EVALUATED`; Capabilities **0 von 29** |

Damit waren **vierzehn Konsistenzvorgänge in achtzehn Work Packages** dokumentiert
(*Stand nach dem vierzehnten Vorgang; durch den fünfzehnten Vorgang unten auf
**fünfzehn** aktualisiert*; löst die vorige Angabe „dreizehn" ab). Die Zahl der
Work Packages stieg auf **achtzehn**, weil dieser Vorgang **erstmals
CBP-WP-018** betraf. R-33 zählt eigenständige Korrekturen kanonischer Status-,
Zähl- oder Konsistenzabweichungen — **nicht** ausschließlich
Post-Commit-Reconciliations; die Korrektur eines vorbestehend falschen
ADR-Zählers ist ein solcher Vorgang. **R-33 bleibt `gemindert, nicht
geschlossen`**, Kritikalität unverändert **mittel**. Derselbe Vorgang ist in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und zählt **nur einmal**.

**R-33-Chronologie — fünfzehnter Konsistenzvorgang (CBP-WP-018 Post-Commit Status Reconciliation, 2026-07-29):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-018** (Post-Commit-Status-Reconciliation; CBP-WP-018 war **bereits** durch den vierzehnten Vorgang Teil der betroffenen Work-Package-Menge) |
| Fehlerklasse | **Git-/Register-Statusabweichung** — nach Commit und Push der technischen Implementation von CBP-WP-018 (`5ee2e83`) führten die Statusdokumente CBP-WP-018 weiterhin als `in-review` / „Phase B1, uncommitted", obwohl Git CBP-WP-018 als `committed` und mit origin/main synchron auswies |
| Betroffene aktuelle Repository-Artefakte | `README.md`, `CLAUDE.md`, `project-system/WORK_PACKAGE_QUEUE.md` (Header, Übersicht, Detailblock), `project-system/PROJECT_MANIFEST.md`, `project-system/PROJECT_PROFILE.md`, `project-system/HEALTH_SCORE.md`, `project-brain/PROJECT_BRAIN.md` |
| Ursache | Der Implementation Commit trug den korrekten **Vor-Commit-Reviewstatus** `in-review`; es fehlte anschließend die **Post-Commit-Status-Reconciliation** (dieselbe Klasse wie der zehnte/zwölfte/dreizehnte Vorgang) |
| Korrektur | Die kanonischen Statusdokumente wurden auf den durch Git belegten `committed`-Zustand von CBP-WP-018 (Governance `4dec921`, Implementation `5ee2e83`) synchronisiert; „aktuelles Work Package" auf **keines aktiv, zuletzt abgeschlossen CBP-WP-018** gesetzt; kein Work Package ist `active`/`in-review`; **kein nächstes Work Package autorisiert**, **CBP-WP-019 nicht registriert, nicht begonnen, nicht autorisiert** |
| Aussagegrenze | **Kein Funktionsfehler, keine Runtimeänderung, keine Gatefreigabe, keine Aktivierung, keine Capability-Änderung**; keine neue Decision-ID, kein neues ADR, kein neues/geschlossenes Risiko; **keine** Risikokritikalität verändert; D-053/ADR-0013 unverändert; Mapping Activation Gate/Security Foundation Readiness Gate/DRC bleiben `NOT EVALUATED`; Capabilities **0 von 29**; die zwölf KB-Kontrollen bleiben `DOCUMENTED ONLY` |

Damit waren **fünfzehn Konsistenzvorgänge in achtzehn Work Packages** dokumentiert
(*Stand nach dem fünfzehnten Vorgang; durch den sechzehnten Vorgang unten auf
**sechzehn** aktualisiert*; löst die vorige Angabe „vierzehn" ab). Die Zahl der
Work Packages blieb **achtzehn**, weil CBP-WP-018 durch den vierzehnten Vorgang
**bereits** Teil der betroffenen Menge war; ein weiterer Vorgang im selben,
bereits erfassten Work Package erhöht **nur** den Vorgangszähler
(**14/18 → 15/18**). **R-33 bleibt `gemindert, nicht geschlossen`**,
Kritikalität unverändert **mittel**. Derselbe Vorgang ist in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und zählt **nur einmal**.

**R-33-Chronologie — sechzehnter Konsistenzvorgang (CBP-WP-019 Post-Commit Status Reconciliation, 2026-07-29):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-019** (Post-Commit-Status-Reconciliation; **erstes** R-33-Erfassen von CBP-WP-019) |
| Fehlerklasse | **Git-/Register-Statusabweichung** — nach Commit und Push von CBP-WP-019 (`3c437f2`) führten die Statusdokumente CBP-WP-019 weiterhin als `in-review` und als **aktives** Work Package ohne Commitbeleg, obwohl Git es als `committed` und mit origin/main synchron auswies |
| Betroffene aktuelle Repository-Artefakte | `README.md`, `CLAUDE.md`, `project-system/WORK_PACKAGE_QUEUE.md` (Header, Übersicht, Detailblock), `project-system/PROJECT_MANIFEST.md`, `project-system/PROJECT_PROFILE.md`, `project-system/HEALTH_SCORE.md`, `project-brain/PROJECT_BRAIN.md`, `docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`, `work-packages/CBP-WP-019.md` |
| Ursache | Der Implementation Commit trug den korrekten **Vor-Commit-Reviewstatus** `in-review`; es fehlte anschließend die **Post-Commit-Status-Reconciliation** (dieselbe Klasse wie der zehnte/zwölfte/dreizehnte/fünfzehnte Vorgang) |
| Korrektur | Die kanonischen Statusdokumente wurden auf den durch Git belegten `committed`-Zustand von CBP-WP-019 (`3c437f2`) synchronisiert; **Commitbeleg eingetragen**; „aktuelles Work Package" auf **keines aktiv, zuletzt abgeschlossen CBP-WP-019** gesetzt; kein Work Package ist `active`/`in-review`; **kein nächstes Work Package autorisiert**, **CBP-WP-020 nicht registriert, nicht begonnen, nicht autorisiert** |
| Aussagegrenze | **Kein Funktionsfehler, keine Runtimeänderung, keine Installation, keine Bereitstellung, keine Gatefreigabe, keine Aktivierung, keine Capability-Änderung**; keine neue Decision-ID, kein neues ADR, kein neues/geschlossenes Risiko; **keine** Risikokritikalität verändert; **D-054 und der DRC-Vertrag unverändert**; der DRC-Gesamtstatus **APPROVED BY HUMAN MAINTAINER** (Profil A, 2026-07-29) bleibt **rein dokumentarisch**; Mapping Activation Gate und Security Foundation Readiness Gate bleiben `NOT EVALUATED`; Capabilities **0 von 29**; die zwölf KB-Kontrollen bleiben `DOCUMENTED ONLY`; **R-20 bleibt offen** |

Damit waren **sechzehn Konsistenzvorgänge in neunzehn Work Packages** dokumentiert
(*Stand nach dem sechzehnten Vorgang; durch den siebzehnten Vorgang unten auf
**siebzehn/zwanzig** aktualisiert*; löst die vorige Angabe „fünfzehn" ab). Die
Zahl der Work Packages stieg auf **neunzehn**, weil dieser Vorgang **erstmals
CBP-WP-019** betraf, das durch den Commit `3c437f2` Teil der committeten Menge
wurde (**15/18 → 16/19**). **R-33 bleibt `gemindert, nicht geschlossen`**,
Kritikalität unverändert **mittel**. Derselbe Vorgang ist in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und zählt **nur einmal**.

**R-33-Chronologie — siebzehnter Konsistenzvorgang (CBP-WP-020 Post-Commit Status Reconciliation, 2026-07-29):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-020** (Post-Commit-Status-Reconciliation; **erstes** R-33-Erfassen von CBP-WP-020) |
| Fehlerklasse | **Git-/Register-Statusabweichung** — nach Commit und Push der B1/B2-Implementation von CBP-WP-020 (`9c6c0fb`, Parent `17057e2`) führten die Statusdokumente CBP-WP-020 weiterhin als `in-review` in „Phase B1/B2, uncommitted" und als **aktives** Work Package, obwohl Git es als `committed` und mit origin/main synchron auswies |
| Betroffene aktuelle Repository-Artefakte | `README.md`, `CLAUDE.md`, `project-system/WORK_PACKAGE_QUEUE.md` (Header, Übersicht, Detailblock), `project-system/PROJECT_MANIFEST.md`, `project-system/PROJECT_PROFILE.md`, `project-system/HEALTH_SCORE.md`, `project-brain/PROJECT_BRAIN.md`, `docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`, `work-packages/CBP-WP-020.md` |
| Ursache | Der Implementation Commit trug den korrekten **Vor-Commit-Reviewstatus** `in-review`; es fehlte anschließend die **Post-Commit-Status-Reconciliation** (dieselbe Klasse wie der zehnte/zwölfte/dreizehnte/fünfzehnte/sechzehnte Vorgang) |
| Zusätzlich bereinigte Zählabweichungen | `project-brain/PROJECT_BRAIN.md` führte **45/41** statt der kanonischen **55/51** getroffenen bzw. A0-Entscheidungen; `project-system/HEALTH_SCORE.md` führte in der Zeile „Entscheidungslage" **54** statt **55**; die Commitzähler in `PROJECT_MANIFEST.md`, `PROJECT_BRAIN.md` und `HEALTH_SCORE.md` standen auf **28** statt **29**. Kanonische Quelle ist `DECISION_REGISTER.md` (**55**, davon **51** mit A0) beziehungsweise Git |
| Korrektur | Die kanonischen Statusdokumente wurden auf den durch Git belegten `committed`-Zustand von CBP-WP-020 (B0 `17057e2`, B1/B2 `9c6c0fb`) synchronisiert; **Commitbelege eingetragen**; CBP-WP-020 auf **`committed` und `complete`** gesetzt; „aktuelles Work Package" auf **keines aktiv, zuletzt abgeschlossen CBP-WP-020**; kein Work Package ist `active`/`in-review`; **kein nächstes Work Package autorisiert**, **CBP-WP-021 nicht registriert, nicht begonnen, nicht autorisiert**; Decisions/A0/ADRs auf **55 / 51 / 13** und Commitzahl auf **29** vereinheitlicht |
| Aussagegrenze | **Kein Funktionsfehler, keine Runtimeänderung, keine Installation, keine Bereitstellung, kein Containerstart, keine Gatefreigabe, keine Aktivierung, keine Capability-Änderung**; keine neue Decision-ID, kein neues ADR, kein neues/geschlossenes Risiko; **keine** Risikokritikalität verändert; **D-055 unverändert**; das Profil-A-Bundle bleibt *repository artifact implemented* und *offline validation passed* — **nicht deployed, nicht operational, nicht production-ready**; die **166 Profile-A Bundle Validation Tests sind keine** Security Foundation NT-01 bis NT-31 (**damals als 0 von 31 geführt** — siehe Nachtrag unten); Mapping Activation Gate und Security Foundation Readiness Gate bleiben `NOT EVALUATED`; Capabilities **0 von 29**; die zwölf KB-Kontrollen bleiben `DOCUMENTED ONLY`; **R-20 bleibt offen** |

> **Nachtrag aus CBP-WP-021 (D-056, 2026-08-03).** Die im siebzehnten Vorgang
> genannte Kennzahl „**0 von 31**" gibt den **damaligen** Stand wieder. Sie war
> bereits zu diesem Zeitpunkt fehlerhaft: der kanonische Wert lautet
> **32 Negativtests, 1 Positivtest, 33 Testfälle** — ausgeführt **0 von 32** und
> **0 von 1**. Genau diese Abweichung ist Gegenstand des **achtzehnten**
> Konsistenzvorgangs unten. **Der historische Eintrag wird nicht umgeschrieben**;
> er dokumentiert weiterhin, was damals geführt wurde.

Damit waren **siebzehn Konsistenzvorgänge in zwanzig Work Packages** dokumentiert
(*Stand nach dem siebzehnten Vorgang; durch den achtzehnten Vorgang unten auf
**18/21** aktualisiert*; löste die vorige Angabe „sechzehn" ab). Die Zahl der
Work Packages stieg auf **zwanzig**, weil jener Vorgang **erstmals
CBP-WP-020** betraf, das durch den Commit `9c6c0fb` Teil der committeten Menge
wurde (**16/19 → 17/20**). **R-33 bleibt `gemindert, nicht geschlossen`**,
Kritikalität unverändert **mittel**. Derselbe Vorgang ist in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und zählt **nur einmal**.

**R-33-Chronologie — achtzehnter Konsistenzvorgang (CBP-WP-021 Canonical Security Test Inventory Reconciliation, 2026-08-03):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-021** (**erstes** R-33-Erfassen von CBP-WP-021) |
| Fehlerklasse | **Fortgeschriebene, falsch etikettierte Kennzahl** — der überholte Wert **31** wurde als **aktive Security-Foundation-Negativtest-Gesamtzahl** geführt, obwohl die authoritative A2-Acceptance-Matrix **32** Negativtests auszählt |
| Herkunft des Fehlers | **31** war der von CBP-WP-011 auf **33** korrigierte **Gesamtwert** (30 NT + 1 PT). Die Zusammenfassungszeile jenes Work Packages wurde beim Audit nicht mitgeführt und etikettierte den Gesamtwert zusätzlich als „Negativtests". Von dort wanderte die Zahl über die Roadmap in spätere Dokumente **und in ausführbare Artefakte** |
| Betroffene Repository-Artefakte | Status- und Roadmapdokumente (`CLAUDE.md`, `README.md`, `project-brain/PROJECT_BRAIN.md`, `project-system/HEALTH_SCORE.md`, `project-system/PROJECT_MANIFEST.md`, `project-system/PROJECT_PROFILE.md`, `project-system/WORK_PACKAGE_QUEUE.md`, `docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`, `docs/roadmap/PHASE_1_FOUNDATION_PLAN.md`), Profil-A-Dokumentation (`docs/operations/PROFILE_A_INSTALLATION_RUNBOOK.md`, `docs/operations/PROFILE_A_VALIDATION_RUNBOOK.md`, `docs/runtime/PROFILE_A_DEPLOYMENT_BUNDLE.md`), Work Packages (`work-packages/CBP-WP-011.md`, `work-packages/CBP-WP-020.md`, `work-packages/CBP-WP-021.md`) sowie die **ausführbaren Artefakte** `deployments/profile-a/bundle.json`, `deployments/profile-a/validate.py`, `deployments/profile-a/README.md` und `tests/test_profile_a_deployment_bundle.py` |
| Besonderheit | **Erstmals war ein Konsistenzfehler nicht rein redaktionell**, sondern in **committetem, ausführbarem Code** verankert: Bundlevertrag, fail-closed Validator und Bundle-Test erzwangen den falschen Wert. Die Korrektur musste deshalb **atomar** erfolgen — eine Teiländerung hätte die Bundlevalidierung sofort gebrochen |
| Autorität | **D-056** (`accepted`, **A0**, 2026-08-03) stellt fest: **32** aktive Negativtests (NT-01…NT-24, NT-26…NT-33), **1** Positivtest (**PT-01**), **33** Testfälle; **NT-25** bleibt nach Regel **TT-5** frei; **NT-32** und **NT-33** sind gültig; **31** ist ein überholter, falsch etikettierter Ableitungswert |
| Korrektur | Vollständige Reconciliation in CBP-WP-021: **B0** (`0cb4ea9`) Registrierung und Authority; **B1/B2** (`271acc7`) dokumentarische **und** ausführbare Angleichung auf **32 / 1 / 33** — `bundle.json` `"total": 32`, `validate.py` erzwingt 32 fail-closed unter unverändertem Issue-Code `BND-CONTRACT-NEGATIVE-TESTS`, Bundle-Test erwartet `(0, 32)`; **B1/B2.1** Schließung der Restfundstelle in `deployments/profile-a/README.md`; **B1/B2.2** Bereinigung des erzeugten Repository-Bytecodes. Die vier Teilschritte gehören zu **genau einem** Konsistenzvorgang |
| Aussagegrenze | **Kein Funktionsfehler, keine Runtimeänderung, keine Installation, keine Bereitstellung, kein Containerstart, keine Gatefreigabe, keine Aktivierung, keine Capability-Änderung**; keine neue Decision-ID, kein neues ADR, kein neues/geschlossenes Risiko; **keine** Risikokritikalität verändert; **D-056 unverändert**; **die Reconciliation einer Inventarzahl ist keine Testausführung** — ausgeführt bleiben **0 von 32** Negativtests und **0 von 1** Positivtest; das Bundleschema enthält **keinen** eigenen Positivtestzähler und wurde **nicht** erweitert; Mapping Activation Gate und Security Foundation Readiness Gate bleiben `NOT EVALUATED`; Capabilities **0 von 29**; die zwölf KB-Kontrollen bleiben `DOCUMENTED ONLY`; **R-20 bleibt offen** |

Damit waren **achtzehn Konsistenzvorgänge in einundzwanzig Work Packages**
dokumentiert (*Stand nach dem achtzehnten Vorgang; durch den neunzehnten
Vorgang unten auf **19/22** und durch die Vorgänge zwanzig bis
zweiundzwanzig fortlaufend auf **22/22** aktualisiert*; löste die vorige
Angabe „siebzehn" ab). Die Zahl der Work
Packages steigt auf **einundzwanzig**, weil dieser
Vorgang **erstmals CBP-WP-021** betrifft, das durch den Commit `271acc7` Teil
der committeten Menge wurde (**17/20 → 18/21**). **R-33 bleibt `gemindert,
nicht geschlossen`**, Kritikalität unverändert **mittel**, kein Risiko
geschlossen, **keine neue Risiko-ID**; **das projektweite Konsistenzrisiko ist
nicht beseitigt**. Derselbe Vorgang ist in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und zählt **nur einmal**.

---

**R-33-Chronologie — neunzehnter Konsistenzvorgang (CBP-WP-022 D-066-Zählerspiegel-Reconciliation, 2026-08-05):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** (**erstes** R-33-Erfassen von CBP-WP-022) |
| Phase und Anlass | **B2D-E-N07-GOV** / **D-066** — die Zählerprüfung des D-066-Registrierungslaufs deckte den Befund auf |
| Fehlerklasse | **Unterbliebene Fortschreibung eines aktiven Zählerspiegels** — zwei allgemeine Statusspiegel führten veraltete Decision- und A0-Zähler, während das kanonische Register bereits fortgeschrieben war |
| Kanonischer Sollstand vor D-066 | **65** Decisions · **61** mit **A0** · **14** ADRs |
| Fehlerhafter Spiegelstand | **61** Decisions · **57** mit **A0** — die ADR-Zahl **14** war korrekt |
| Abweichung | **je vier fehlende Fortschreibungen** bei Decisions und A0 |
| Herkunft des Fehlers | Stand aus Commit **`38eb33f`**; die Fortschreibung unterblieb bei **D-062**, **D-063**, **D-064** und **D-065**. Die betroffenen Zeilen liegen in allgemeinen Zustandstabellen, nicht in den phasendatierten Momentaufnahmen — deren jüngste wies korrekt **65/61/14** aus |
| Betroffene Repository-Artefakte | **`CLAUDE.md`** und **`project-brain/PROJECT_BRAIN.md`** — je genau eine Zeile des allgemeinen Projektzustands |
| Besonderheit | **Rein dokumentarisch** — im Gegensatz zum achtzehnten Vorgang war **kein ausführbares Artefakt** betroffen, weder Bundlevertrag noch Validator noch Test. Der Fehler wurde **innerhalb** des D-066-Laufs durch die vorgeschriebene Zählerprüfung gefunden, **nicht** durch die fünfteilige Zähl- und Statusregel verhindert |
| Autorität | **D-066** (`accepted`, **A0**, 2026-08-05, `PROFILE_A_RETRIEVAL_NOT_INSTANTIATED_N07_DEFERRED`, `ADR_NOT_REQUIRED`) — die Registrierung erfolgt im selben Kandidaten; **D-062 bis D-065 bleiben unverändert** |
| Korrektur | Im D-066-Arbeitsbaum wurden beide Spiegel auf den Kandidatenstand **66** Decisions · **62** mit **A0** · **14** ADRs gebracht — innerhalb des autorisierten D-066-Dateiscopes und im D-066-Ausführungsbericht offengelegt, dessen Result deshalb **`COUNTER_INCONSISTENCY`** lautete. Die Registrierung dieses Vorgangs erfolgte im Retry **B2D-E-N07-GOV-N1-R1**, nachdem der erste Versuch mit **`ALLOWLIST_INSUFFICIENT`** angehalten hatte, weil [COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) außerhalb des damaligen Dateiscopes lag |
| Closure | Die **aktiven** Decision- und A0-Spiegel stimmen im aktuellen Arbeitsbaum wieder mit dem kanonischen Decision Register überein; der Vorgang ist im Kandidaten **behoben** |
| Aussagegrenze | **Keine Decision vor D-066 geändert**, **keine ADR geändert**, **keine Risiko-ID ergänzt**, **keine Severity geändert**, **keine Tests geändert**, **keine Traceability geändert**, **keine technische Reifeaussage**; die **D-066-Semantik ist unverändert**; **KB-04 bleibt `DOCUMENTED ONLY`**, beide Gates `NOT EVALUATED`, Capabilities **0 von 29**, **NT-04 und NT-05 nicht ausgeführt**, **OD-37 offen**, **Contract §10.3 offen**, **`KB04-T-N07` zurückgestellt**, **`KB04-T-N14` nicht autorisiert**, **R-20 bleibt offen** |

Damit waren **neunzehn Konsistenzvorgänge in zweiundzwanzig Work Packages**
dokumentiert (*Stand nach dem neunzehnten Vorgang; durch die Vorgänge zwanzig
bis zweiundzwanzig unten fortlaufend auf **20/22**, **21/22** und **22/22**
aktualisiert*; löste die vorige Angabe „achtzehn" ab). Die Zahl der Work
Packages steigt auf **zweiundzwanzig**, weil dieser
Vorgang **erstmals CBP-WP-022** betrifft, das durch die Commits `e4caa14` bis
`0cd21f5` Teil der committeten Menge ist (**18/21 → 19/22**). **R-33 bleibt
`gemindert, nicht geschlossen`**, Kritikalität unverändert **mittel**, kein
Risiko geschlossen, **keine neue Risiko-ID**; **das projektweite
Konsistenzrisiko ist nicht beseitigt** — dieser Vorgang belegt es erneut.
Derselbe Vorgang ist in [COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt
und zählt **nur einmal**. Die dortige Darstellung folgt der **Prosaform** jenes
Dokuments, während hier die **Tabellenform** des Risk Registers verwendet wird;
**Fakten, Zahlen, Closure-Grenze und R-33-Wirkung sind identisch**.

---

**R-33-Chronologie — zwanzigster Konsistenzvorgang (CBP-WP-022 B2D-ENV-GOV Active Phase-status Mirrors Staleness, 2026-08-06):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert**, weil CBP-WP-022 durch den neunzehnten Vorgang **bereits** Teil der erfassten Menge ist. Nennerkonstanz ist **kein Erstfall**: sie trat schon beim **fünfzehnten** Vorgang auf (`14/18 → 15/18`) |
| Phase und Anlass | Gefunden im read-only Bericht **B2D-E-N14-HM-AUTH-PREP**, registriert in **B2D-E-N14-HM-AUTH-PREP-R33-N1** |
| Fehlerklasse | **Unterbliebene Fortschreibung aktiver Phasenstatusspiegel** — **mehrere Fundstellen derselben Fehlerursache** führten den Commitstatus **einer** Phase falsch; in `CLAUDE.md` stand die falsche Angabe sogar zweimal widersprüchlich in **einer** Zelle |
| Betroffene aktive Repository-Artefakte | **drei** — **`CLAUDE.md`** (Zeile des aktiven Work Packages im Abschnitt *Aktueller Zustand*), **`project-system/WORK_PACKAGE_QUEUE.md`** (Kopfzeile *Aktuelles Work Package*, Feld *Stand*, Queue-Tabellenzeile CBP-WP-022, Detailfelder *Aktuelle Phase* und *Commit*) und **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** (aktive Fortschrittsaussage) |
| Falsche aktive Aussagen | **`B2D-ENV-GOV uncommitted`** (`CLAUDE.md`, `WORK_PACKAGE_QUEUE.md` Queue-Tabelle), **`B2D-ENV-GOV nicht committed`** (`WORK_PACKAGE_QUEUE.md` Commit-Feld), **„Phase B2D-ENV-GOV abgeschlossen und uncommitted"** (`PHASE_1_WORK_PACKAGE_MAP.md`) sowie **B2D-ENV-GOV als aktuelle Phase** in Kopf-, Stand- und Detailfeldern von `WORK_PACKAGE_QUEUE.md`, obwohl die Phase längst abgeschlossen und committet ist |
| Einmalzählung trotz mehrerer Fundstellen | **eine** Phase · **ein** korrekter Commitstatus · **ein** gemeinsamer Root Cause — die unterbliebene Post-Commit-Fortschreibung derselben Angabe · **eine** gemeinsame Reconciliation. Deshalb **genau ein** Konsistenzvorgang; für einzelne B2D-ENV-GOV-Zeilen wird **kein** zusätzlicher Vorgang angelegt |
| Korrekter Zustand | **B2D-ENV-GOV ist `committed`**, Commit **`0cd21f5`** — wenige Sätze später in derselben Zelle bereits korrekt ausgewiesen |
| Herkunft des Fehlers | Alle Fundstellen entstanden im B2D-ENV-GOV-Lauf, als die Phase tatsächlich noch nicht committet war; die Post-Commit-Fortschreibung unterblieb, während spätere Läufe an anderer Stelle derselben Dokumente den korrekten Zustand ergänzten — daher der Widerspruch |
| Abgrenzung | **Keine zitierte historische Momentaufnahme**, **keine bewusst markierte Darstellung eines früheren Zustands** — beide Aussagen stehen unmarkiert in der aktiven Statusdarstellung und erzeugten am committeten HEAD **`c662452`** eine tatsächliche aktive Statusinkonsistenz |
| Erstmalige Registrierung | Dieser Sachverhalt war in den bisherigen **neunzehn** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Alle bestätigten aktiven Fundstellen wurden auf **B2D-ENV-GOV `committed` (`0cd21f5`)** und auf die tatsächliche aktuelle Phase **B2D-E-N14-GOV** gebracht; **keine phasendatierte historische Momentaufnahme überschrieben** |
| Zählwirkung | Zähler **19 → 20**, Nenner **22 unverändert** (**`19/22 → 20/22`**). Die Doppelabbildung in Risk Register und Compliance Check **zählt als genau ein Konsistenzvorgang** |
| Aussagegrenze | **Keine technische Implementierungsänderung**, **keine Decisionänderung**, **keine ADR-Änderung**, **keine Risikoänderung**, **keine neue Risiko-ID**, **keine Teständerung**, **keine Traceabilityänderung**, **keine Capabilityänderung**; **D-067 unverändert**; **KB-04 bleibt `DOCUMENTED ONLY`**; beide Gates bleiben `NOT EVALUATED`; **`KB04-T-N14` nicht ausgeführt und nicht lokal autorisiert**; **NT-04 und NT-05 nicht ausgeführt**; **OD-37 offen**; **Contract §10.3 offen**; **R-20 bleibt offen** |

Damit waren **zwanzig Konsistenzvorgänge in zweiundzwanzig Work Packages**
dokumentiert (*Stand nach dem zwanzigsten Vorgang; durch den einundzwanzigsten
Vorgang unten auf **21/22** und durch den zweiundzwanzigsten auf **22/22**
aktualisiert*; löste die vorige Angabe „neunzehn" ab). Die Zahl der Work
Packages bleibt **zweiundzwanzig**, weil CBP-WP-022 durch den neunzehnten
Vorgang **bereits** Teil der erfassten Menge war; ein weiterer Vorgang im
selben, bereits erfassten Work Package erhöht **nur** den Vorgangszähler
(**19/22 → 20/22**). **R-33 bleibt `gemindert, nicht geschlossen`**,
Kritikalität unverändert **mittel**, kein Risiko geschlossen, **keine neue
Risiko-ID**; **das projektweite Konsistenzrisiko ist nicht beseitigt** — der
zwanzigste Vorgang belegt es unmittelbar nach dem neunzehnten. Derselbe Vorgang
ist in [COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und **zählt nur
einmal**. Die dortige Darstellung folgt der **Prosaform** jenes Dokuments,
während hier die **Tabellenform** des Risk Registers verwendet wird; **Fakten,
Zahlen, Closure-Grenze und R-33-Wirkung sind identisch**.

---

**R-33-Chronologie — einundzwanzigster Konsistenzvorgang (CBP-WP-022 B2B-P Active Commit-status Mirror Staleness, 2026-08-06):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert**, weil CBP-WP-022 seit dem neunzehnten Vorgang **bereits** Teil der erfassten Menge ist |
| Phase und Anlass | Gefunden im read-only Bericht **B2D-E-N14-HM-AUTH-PREP**, dort als unregistrierte Nebenbeobachtung ausgewiesen; registriert in **B2D-E-N14-HM-AUTH-PREP-R33-N2** |
| Fehlerklasse | **Unterbliebene Fortschreibung eines aktiven Commitstatusspiegels** — dieselbe Klasse wie der zwanzigste Vorgang, jedoch **andere Phase**, **anderer Commit** und **anderes Artefakt** |
| Betroffene aktive Repository-Artefakte | **zwei** — **`README.md`** (Zeile des aktiven Work Packages im Abschnitt *Aktueller Stand*) und **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** (aktive Fortschrittsaussage im Fließtext). Die zweite Fundstelle wurde in **B2D-E-N14-HM-AUTH-PREP-R33-N3** nachgetragen; **mehrere Fundstellen derselben Fehlerursache bleiben genau ein Vorgang** und erhöhen den Zähler **nicht** erneut. Im **R-33 Active-Status Closure Fix** um **`project-brain/PROJECT_BRAIN.md`** erweitert — siehe *Erweiterung* |
| Falsche aktive Aussagen | **`B2B-P uncommitted`** (`README.md`, Phasen-Commit-Aufzählung) und **„Phase B2B-P ist abgeschlossen und uncommitted"** (`PHASE_1_WORK_PACKAGE_MAP.md`) |
| Korrekter Zustand | **B2B-P ist `committed`**, Commit **`fff8227`** — *„CBP-WP-022: add KB-04 initialization planning and safety guards"* |
| Abgrenzung | **Keine zitierte historische Momentaufnahme**, **keine bewusst markierte frühere Phase** — die Aussage steht unmarkiert in der aktiven Statusdarstellung; im Gegensatz zum zwanzigsten Vorgang enthält `README.md` **keine** gegenläufige korrekte Angabe, der Fehler ist eine **reine Fortschreibungslücke** |
| Erstmalige Registrierung | In den bisherigen **zwanzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Beide Fundstellen wurden auf **B2B-P `committed` `fff8227`** gebracht; **keine weitere Angabe dieser Dateien verändert**, insbesondere **keine** historische Darstellung und **keine** ausdrücklich markierte Momentaufnahme |
| Zählwirkung | Zähler **20 → 21**, Nenner **22 unverändert** (**`20/22 → 21/22`**) |
| Einmalzählung | Die Doppelabbildung in Risk Register und Compliance Check **zählt als genau ein Konsistenzvorgang** |
| Erweiterung (R-33 Active-Status Closure Fix, 2026-09-21) | Der repositoryweite read-only Vollständigkeitsaudit bestätigte **zwei weitere Fundstellen derselben Fehlerursache** in **`project-brain/PROJECT_BRAIN.md`**: die Phasen-Commit-Aufzählung der Zeile *Aktuelles Work Package* und die Zeile *Geplante Work Packages* führten jeweils **`B2B-P uncommitted`**. Beide wurden auf **B2B-P `committed` `fff8227`** gebracht. **Zählneutral** — dieselbe Phase, derselbe Commit, dieselbe Fehlerursache; **kein neuer Vorgang**, Zähler und Nenner unverändert |
| Aussagegrenze | **Keine technische Implementierungsänderung**, **keine Decisionänderung**, **keine ADR-Änderung**, **keine Risikoänderung**, **keine neue Risiko-ID**, **keine Teständerung**, **keine Traceabilityänderung**, **keine Capabilityänderung**; **R-33 bleibt offen und `gemindert, nicht geschlossen`** |

Damit waren **einundzwanzig Konsistenzvorgänge in zweiundzwanzig Work
Packages** dokumentiert (*Stand nach dem einundzwanzigsten Vorgang; durch den
zweiundzwanzigsten Vorgang unten auf **22/22** aktualisiert*; löste die vorige
Angabe „zwanzig" ab). Der Nenner bleibt **zweiundzwanzig** (**20/22 → 21/22**).
Derselbe Vorgang ist in [COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt
und **zählt nur einmal**; **Fakten, Zahlen, Closure-Grenze und R-33-Wirkung
sind identisch**.

---

**R-33-Chronologie — zweiundzwanzigster Konsistenzvorgang (CBP-WP-022 B2D-E-N07-GOV Active Commit-status Mirror Staleness, 2026-08-06):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert**, weil CBP-WP-022 seit dem neunzehnten Vorgang **bereits** Teil der erfassten Menge ist |
| Phase und Anlass | Gefunden im read-only Bericht **B2D-E-N14-HM-AUTH-PREP**, dort als unregistrierte Nebenbeobachtung ausgewiesen; registriert in **B2D-E-N14-HM-AUTH-PREP-R33-N2** |
| Fehlerklasse | **Unterbliebene Fortschreibung eines aktiven Commitstatusspiegels** — dieselbe Klasse wie der zwanzigste und einundzwanzigste Vorgang, jedoch **andere Phase**, **anderer Commit** und **anderes Artefakt** |
| Betroffenes aktives Repository-Artefakt | **`project-system/PROJECT_MANIFEST.md`** — Zeile des aktiven Work Packages im Abschnitt *Status* |
| Falsche aktive Aussage | Die Phasen-Commit-Aufzählung führte **`B2D-E-N07-GOV uncommitted`** |
| Korrekter Zustand | **B2D-E-N07-GOV ist `committed`**, Commit **`c4b0426`** — *„CBP-WP-022: defer N07 retrieval and reconcile R-33"* |
| Abgrenzung | **Keine zitierte historische Momentaufnahme**, **keine bewusst markierte frühere Phase**; die Zeile weist die aktuelle Phase **B2D-E-N14-GOV** korrekt aus, führte den unmittelbar davorliegenden Phasencommit aber weiter als offen. Der Commit **`c4b0426`** war in dieser Datei **an keiner Stelle** genannt — eine **reine Fortschreibungslücke** |
| Erstmalige Registrierung | In den bisherigen **einundzwanzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | **`B2D-E-N07-GOV uncommitted`** wurde durch **B2D-E-N07-GOV `committed` `c4b0426`** ersetzt; **keine weitere Angabe dieser Datei verändert** |
| Zählwirkung | Zähler **21 → 22**, Nenner **22 unverändert** (**`21/22 → 22/22`**) |
| Einmalzählung | Die Doppelabbildung in Risk Register und Compliance Check **zählt als genau ein Konsistenzvorgang** |
| Aussagegrenze | **Keine technische Implementierungsänderung**, **keine Decisionänderung**, **keine ADR-Änderung**, **keine Risikoänderung**, **keine neue Risiko-ID**, **keine Teständerung**, **keine Traceabilityänderung**, **keine Capabilityänderung**; **D-067 unverändert**; **KB-04 bleibt `DOCUMENTED ONLY`**; beide Gates bleiben `NOT EVALUATED`; **`KB04-T-N14` nicht ausgeführt und nicht lokal autorisiert**; **NT-04 und NT-05 nicht ausgeführt**; **OD-37 offen**; **Contract §10.3 offen**; **R-20 bleibt offen** |

Damit waren **zweiundzwanzig Konsistenzvorgänge in zweiundzwanzig Work
Packages** dokumentiert (*Stand nach dem zweiundzwanzigsten Vorgang; durch den
dreiundzwanzigsten Vorgang unten auf **23/22** aktualisiert*; löste die vorige
Angabe „einundzwanzig" ab). Die Zahl der Work Packages bleibt
**zweiundzwanzig**, weil alle drei Vorgänge **20**, **21** und **22** dasselbe,
seit dem neunzehnten Vorgang bereits erfasste Work Package CBP-WP-022
betreffen; sie erhöhen **ausschließlich** den Vorgangszähler
(**19/22 → 20/22 → 21/22 → 22/22**). Nennerkonstanz ist **kein Erstfall** — sie
trat bereits beim **fünfzehnten** Vorgang auf (`14/18 → 15/18`). **R-33 bleibt
`gemindert, nicht geschlossen`**, Kritikalität unverändert **mittel**, kein
Risiko geschlossen, **keine neue Risiko-ID**; **das projektweite
Konsistenzrisiko ist nicht beseitigt** — drei Vorgänge derselben Klasse an
einem Tag belegen es unmittelbar. Derselbe Vorgang ist in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und **zählt nur einmal**.
Die dortige Darstellung folgt der **Prosaform** jenes Dokuments, während hier
die **Tabellenform** des Risk Registers verwendet wird; **Fakten, Zahlen,
Closure-Grenze und R-33-Wirkung sind identisch**.

---

**R-33-Chronologie — dreiundzwanzigster Konsistenzvorgang (CBP-WP-022 Active Current-phase Mirrors Staleness, 2026-08-06):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert**, weil CBP-WP-022 seit dem neunzehnten Vorgang **bereits** Teil der erfassten Menge ist |
| Phase und Anlass | Im Bericht **B2D-E-N14-HM-AUTH-PREP-R33-N2** als verbleibende, **nicht registrierte** Beobachtung ausgewiesen; registriert in **B2D-E-N14-HM-AUTH-PREP-R33-N3** |
| Fehlerklasse | **Unterbliebene Fortschreibung aktiver Current-Phase-Spiegel** — anders als bei den Vorgängen 20 bis 22 betrifft der Fehler nicht den **Commitstatus** einer einzelnen Phase, sondern die Angabe, **welche Phase gegenwärtig aktuell ist** |
| Betroffene aktive Repository-Artefakte | **zwei** — **`README.md`** (Zeile *Aktuelles Work Package* im Abschnitt *Aktueller Stand*) und **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** (Kopffeld *Stand* und Work-Package-Tabellenzeile CBP-WP-022). Im **R-33 Active-Status Closure Fix** um **vier** weitere aktive Current-Phase-Spiegel erweitert — siehe *Erweiterung* |
| Falsche aktive Current-Phase-Werte | **`B2B-P`** in `README.md` und im Kopffeld *Stand* der Roadmapkarte · **`B2D-P`** in der Work-Package-Tabellenzeile der Roadmapkarte |
| Korrekter gemeinsamer Zustand | **Phase `B2D-E-N14-GOV`** — *N14 Ephemeral Observation Bridge Classification*; zugehörige Decision **D-067** (`accepted`, **A0**); zugehöriger Commit **`c662452`** |
| Aktiv, nicht historisch | Beide Fundstellen sind **Top-Level-Current-Phase-Spiegel** ihrer Dokumente, stehen **unmarkiert**, tragen **keine** Zitatform und **keinen** Hinweis auf einen früheren Zustand. Beide Dateien nennen **an anderer Stelle** bereits korrekt **B2D-E-N14-GOV** und **D-067** — der Widerspruch ist damit dateiintern belegt |
| Herkunft des Fehlers | Beide Spiegel wurden über **mehrere** Phasen hinweg nicht fortgeschrieben: `README.md` blieb auf **B2B-P**, die Roadmapkarte auf **B2B-P** (Kopf) beziehungsweise **B2D-P** (Tabelle) stehen, während die Phasenkette bis **B2D-E-N14-GOV** fortschritt |
| Erstmalige Registrierung | In den bisherigen **zweiundzwanzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Beide aktiven Current-Phase-Spiegel wurden auf **Phase `B2D-E-N14-GOV` – D-067, `committed` `c662452`** gebracht. **Keine historische Phasenangabe ersetzt** — insbesondere bleiben die Aussagen **B2D-P ist `committed` (`b409d25`)** und **B2B-P `committed` `fff8227`** unverändert, ebenso alle früheren Work-Package-Planungen und accepted Governancegrenzen |
| Einmalzählung trotz zweier Artefakte | **derselbe Spiegeltyp** — aktiver Current-Phase-Spiegel · **derselbe Zielzustand** — `B2D-E-N14-GOV` / D-067 / `c662452` · **dieselbe Fortschreibungsfehlerklasse** · **eine** gemeinsame Reconciliation. Deshalb **genau ein** Konsistenzvorgang und **keine** eigene Ereignisnummer je Datei |
| Erweiterung (R-33 Active-Status Closure Fix, 2026-09-21) | Der repositoryweite read-only Vollständigkeitsaudit bestätigte **vier weitere aktive Current-Phase-Spiegel desselben Spiegeltyps** mit **demselben Zielzustand**: **`project-brain/PROJECT_BRAIN.md`** (Zeile *Geplante Work Packages*: **`B2B-P`**) · **`project-system/HEALTH_SCORE.md`** (Zeile *Vorgeschlagene Work Packages*: **`B2C.2`**) · **`project-system/PROJECT_PROFILE.md`** (Zeile *Phase 1*: **`B2C.1 – Synthetic Evidence Scope Decision`**) · **`project-system/WORK_PACKAGE_QUEUE.md`** (Übersichtsabsatz CBP-WP-022: **`Phase B0 – Registration and Authority Baseline`**). Alle wurden auf **Phase `B2D-E-N14-GOV` – D-067**, `committed` **`c662452`**, gebracht; im Queue-Absatz blieb die Registrierungsangabe als **Phase B0 `committed` `e4caa14`** erhalten. **Aussagen zum Autorisierungsstand in denselben Zeilen blieben wörtlich unverändert.** **Zählneutral** — derselbe Spiegeltyp, derselbe Zielzustand, dieselbe Fortschreibungsfehlerklasse; **kein neuer Vorgang**, Zähler und Nenner unverändert |
| Zählwirkung | Zähler **22 → 23**, Nenner **22 unverändert** (**`22/22 → 23/22`**) |
| Verhältnisgrenze | **`23/22` ist kein Erfüllungsgrad und keine Prozentkennzahl.** Der Zähler zählt **dokumentierte Konsistenzvorgänge**, der Nenner **Work Packages mit mindestens einem Vorgang**; der Zähler **darf** den Nenner überschreiten, sobald ein Work Package mehrere Vorgänge trägt. **`23/23` ist unzulässig** |
| Doppelabbildung | Die Registrierung in Risk Register und Compliance Check **zählt als genau ein Konsistenzvorgang** |
| Aussagegrenze | **Keine technische Implementierungsänderung**, **keine neue Decision**, **keine ADR**, **keine Risikoänderung**, **keine neue Risiko-ID**, **keine Teständerung**, **keine Traceabilityänderung**, **keine Capabilityänderung**; **D-067 unverändert**; **KB-04 bleibt `DOCUMENTED ONLY`**; beide Gates bleiben `NOT EVALUATED`; **`KB04-T-N14` nicht ausgeführt und nicht lokal autorisiert**; **NT-04 und NT-05 nicht ausgeführt**; **OD-37 offen**; **Contract §10.3 offen**; **R-20 bleibt offen**; **R-33 bleibt offen und `gemindert, nicht geschlossen`** |

Damit waren **dreiundzwanzig Konsistenzvorgänge in zweiundzwanzig Work
Packages** dokumentiert (*Stand nach dem dreiundzwanzigsten Vorgang; durch die
Vorgänge vierundzwanzig bis dreißig unten fortlaufend auf **30/22**
aktualisiert, die Erweiterung dieses Vorgangs ist zählneutral*; löste die
vorige Angabe „zweiundzwanzig" ab). Die Zahl der Work Packages bleibt **zweiundzwanzig**;
Vorgang **23** betrifft — wie die Vorgänge 20 bis 22 — das seit dem
neunzehnten Vorgang bereits erfasste Work Package CBP-WP-022 und erhöht
**ausschließlich** den Vorgangszähler. Vollständige Progression:
**19/22 → 20/22 → 21/22 → 22/22 → 23/22**. **R-33 bleibt `gemindert, nicht
geschlossen`**, Kritikalität unverändert **mittel**, kein Risiko geschlossen,
**keine neue Risiko-ID**; **das projektweite Konsistenzrisiko ist nicht
beseitigt** — vier Vorgänge derselben Grundklasse an einem Tag belegen es
unmittelbar. Derselbe Vorgang ist in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und **zählt nur einmal**.
Die dortige Darstellung folgt der **Prosaform** jenes Dokuments, während hier
die **Tabellenform** des Risk Registers verwendet wird; **Fakten, Zahlen,
Closure-Grenze und R-33-Wirkung sind identisch**.

---

**R-33-Chronologie — Vorgänge vierundzwanzig bis dreißig (CBP-WP-022 R-33 Active-Status Closure Fix, 2026-09-21):**

Nach mehreren read-only Reviews bestätigte ein **repositoryweiter read-only
Vollständigkeitsaudit** am committeten HEAD **`c662452`** weitere aktive
Statusinkonsistenzen. Der abschließende Lauf **R-33 Active-Status Closure Fix**
erweitert die Vorgänge **21** und **23** zählneutral (siehe dort) und
registriert **genau sieben** neue Vorgänge. Für alle sieben gilt dieselbe
**Aussagegrenze**: **keine technische Implementierungsänderung**, **keine neue
Decision**, **keine ADR**, **keine Risikoänderung**, **keine neue Risiko-ID**,
**keine Teständerung**, **keine Traceabilityänderung**, **keine
Capabilityänderung**, **keine Änderung einer Aussage zum Autorisierungsstand**;
**D-056** und **D-067** unverändert; **KB-04 bleibt `DOCUMENTED ONLY`**; beide
Gates bleiben `NOT EVALUATED`; **`KB04-T-N14`**, **NT-04** und **NT-05** nicht
ausgeführt; **OD-37**, **Contract §10.3** und **R-20** bleiben offen.

**R-33-Chronologie — vierundzwanzigster Konsistenzvorgang (CBP-WP-022 B2D-E-N14-GOV Active Commit-status Mirrors Staleness, 2026-09-21):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert**, weil CBP-WP-022 seit dem neunzehnten Vorgang **bereits** Teil der erfassten Menge ist |
| Phase und Anlass | Im repositoryweiten read-only Vollständigkeitsaudit bestätigt; registriert im **R-33 Active-Status Closure Fix** |
| Fehlerklasse | **Unterbliebene Fortschreibung aktiver Commitstatusspiegel** — dieselbe Grundklasse wie die Vorgänge 20 bis 22, jedoch **andere Phase** und **anderer Commit** |
| Betroffene aktive Repository-Artefakte | **vier** — **`project-system/HEALTH_SCORE.md`** (Zeile *Vorgeschlagene Work Packages*), **`project-system/PROJECT_PROFILE.md`** (Zeile *Phase 1*), **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** (Work-Package-Tabellenzeile CBP-WP-022) und **`work-packages/CBP-WP-022.md`** (Zeile B2D-E-N14-GOV der Phasenmodelltabelle) |
| Falsche aktive Aussagen | **`B2D-E-N14-GOV uncommitted`** (`HEALTH_SCORE.md`, `PROJECT_PROFILE.md`) · **„B2D-E-N14-GOV registriert D-067 (…), uncommitted"** (`PHASE_1_WORK_PACKAGE_MAP.md`) · **„complete (dieser Stand, uncommitted)"** (`CBP-WP-022.md`, Phasenmodellzeile) |
| Korrekter Zustand | **B2D-E-N14-GOV ist `committed`**, Commit **`c662452`** — *„CBP-WP-022: classify N14 observation bridge"* |
| Herkunft des Fehlers | Alle vier Fundstellen entstanden im B2D-E-N14-GOV-Lauf **vor** dem Commit `c662452`, als die Phase tatsächlich noch nicht committet war; die Post-Commit-Fortschreibung unterblieb |
| Aktiv, nicht historisch | Alle Fundstellen stehen in **aktiven** Statuszeilen beziehungsweise in der **aktiven Phasenmodelltabelle**. Der Vermerk „(dieser Stand, uncommitted)" macht die Zeile einer Live-Statustabelle **nicht** zu einer historischen Momentaufnahme — die Nachbarzeilen **B2D-ENV-GOV** und **B2D-E-N07-GOV** derselben Tabelle waren bereits auf `committed` fortgeschrieben |
| Erstmalige Registrierung | In den bisherigen **dreiundzwanzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Alle vier Fundstellen wurden auf **B2D-E-N14-GOV `committed` `c662452`** gebracht; die Phasenmodellzeile folgt der Form ihrer Nachbarzeilen (**`committed` (`c662452`)** — **D-067**) |
| Einmalzählung | **eine** Phase · **ein** Commit · **eine** Fehlerursache · **eine** gemeinsame Reconciliation — **genau ein** Vorgang trotz vier Fundstellen; die Doppelabbildung in Risk Register und Compliance Check **zählt nur einmal** |
| Zählwirkung | Zähler **23 → 24**, Nenner **22 unverändert** (**`23/22 → 24/22`**) |

---

**R-33-Chronologie — fünfundzwanzigster Konsistenzvorgang (CBP-WP-022 Active Commit-field Sequence Staleness, 2026-09-21):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert** |
| Phase und Anlass | Im repositoryweiten read-only Vollständigkeitsaudit bestätigt; registriert im **R-33 Active-Status Closure Fix** |
| Fehlerklasse | **Unterbliebene Fortschreibung eines aktiven Commitfelds** — das Kopffeld *Commit* der Work-Package-Datei wurde über **neun** Phasencommits hinweg nicht fortgeschrieben |
| Betroffenes aktives Repository-Artefakt | **`work-packages/CBP-WP-022.md`** — Kopffeld *Commit* |
| Falsche aktive Aussage | Die Commitfolge endete bei **B2B-P `committed` `fff8227`** und führte **„B2C.1 nicht committed"**; sämtliche Commits ab B2C.1 fehlten |
| Korrekter Zustand | **B2C.1 `38eb33f`** · **B2C.2 `117647f`** · **B2C-T-R `9cde9de`** · **B2D-P `b409d25`** · **B2D-GOV `7e8328a`** · **B2D-AUTH `1222ec0`** · **B2D-ENV-GOV `0cd21f5`** · **B2D-E-N07-GOV `c4b0426`** · **B2D-E-N14-GOV `c662452`** — sämtlich `committed` |
| Herkunft des Fehlers | Der Eintrag **„B2C.1 nicht committed"** entstand im B2C.1-Lauf **vor** dessen Commit `38eb33f`; keiner der folgenden Läufe schrieb das Feld fort, obwohl die Phasenmodelltabelle derselben Datei die Commits zeilenweise auswies |
| Aktiv, nicht historisch | Ein **aktives Kopffeld**; die Abschnitte *Stand nach …* derselben Datei sind echte phasendatierte Momentaufnahmen und bleiben unverändert |
| Erstmalige Registrierung | In den bisherigen **vierundzwanzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Die Commitfolge wurde ab **B2C.1** bis **B2D-E-N14-GOV `c662452`** vervollständigt; die Angaben **B0** bis **B2B-P** und der Vermerk zur Commit-Autorität blieben unverändert |
| Einmalzählung | **ein** Feld · **eine** Fehlerursache · **eine** Reconciliation — **genau ein** Vorgang, obwohl neun Commits fehlten |
| Zählwirkung | Zähler **24 → 25**, Nenner **22 unverändert** (**`24/22 → 25/22`**) |

---

**R-33-Chronologie — sechsundzwanzigster Konsistenzvorgang (CBP-WP-022 B2C-T-R Active Commit-status Mirrors Staleness, 2026-09-21):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert** |
| Phase und Anlass | Im repositoryweiten read-only Vollständigkeitsaudit bestätigt; registriert im **R-33 Active-Status Closure Fix** |
| Fehlerklasse | **Unterbliebene Fortschreibung aktiver Commitstatusspiegel** — dieselbe Grundklasse wie der vierundzwanzigste Vorgang, jedoch **andere Phase** und **anderer Commit** |
| Betroffene aktive Repository-Artefakte | **zwei** — **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** (aktive Fortschrittsaussage im Fließtext) und **`project-system/WORK_PACKAGE_QUEUE.md`** (Kopfzeile *Aktuelles Work Package*) |
| Falsche aktive Aussagen | **„Phase B2C-T-R ist abgeschlossen und uncommitted"** (Roadmapkarte) · **`B2C-T-R uncommitted`** (Queue-Kopfzeile, zusätzlich mit unausgeglichener Fettmarkierung) |
| Korrekter Zustand | **B2C-T-R ist `committed`**, Commit **`9cde9de`** — *„CBP-WP-022: add KB-04 contract traceability and NT preparation"* |
| Herkunft des Fehlers | Beide Aussagen entstanden im B2C-T-R-Lauf **vor** dem Commit `9cde9de`; die Post-Commit-Fortschreibung unterblieb. Beide Dateien weisen **an anderer Stelle** bereits korrekt **B2C-T-R `committed` `9cde9de`** aus — der Widerspruch ist dateiintern belegt |
| Erstmalige Registrierung | In den bisherigen **fünfundzwanzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Beide Fundstellen wurden auf **B2C-T-R `committed` (`9cde9de`)** gebracht; die Fettmarkierung der Queue-Aufzählung ist dabei ausgeglichen. Die Aussage zum Autorisierungsstand am Ende derselben Queue-Zeile blieb **wörtlich unverändert** |
| Einmalzählung | **eine** Phase · **ein** Commit · **eine** Fehlerursache — **genau ein** Vorgang trotz zweier Artefakte |
| Zählwirkung | Zähler **25 → 26**, Nenner **22 unverändert** (**`25/22 → 26/22`**) |

---

**R-33-Chronologie — siebenundzwanzigster Konsistenzvorgang (CBP-WP-022 B1C Active Commit-status Mirror Staleness, 2026-09-21):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert** |
| Phase und Anlass | Im repositoryweiten read-only Vollständigkeitsaudit bestätigt; registriert im **R-33 Active-Status Closure Fix** |
| Fehlerklasse | **Unterbliebene Fortschreibung eines aktiven Commitstatusspiegels** — dieselbe Grundklasse, jedoch **andere Phase** und **anderer Commit** |
| Betroffenes aktives Repository-Artefakt | **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** — aktive Fortschrittsaussage im Absatz zu CBP-WP-022 |
| Falsche aktive Aussage | **„Phase B1C ist abgeschlossen und uncommitted"** |
| Korrekter Zustand | **B1C ist `committed`**, Commit **`24de07e`** — *„CBP-WP-022: define KB-04 enforcement contract and validation plan"* |
| Herkunft des Fehlers | Die Aussage entstand im B1C-Lauf **vor** dessen Commit `24de07e`; spätere Läufe ergänzten wenige Absätze darunter **„Phase B1C ist `committed` (`24de07e`)"**, schrieben die ursprüngliche Aussage aber nicht fort — der Widerspruch ist dateiintern belegt |
| Erstmalige Registrierung | In den bisherigen **sechsundzwanzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Auf **„Phase B1C ist abgeschlossen und `committed` (`24de07e`)"** gebracht; keine weitere Angabe verändert |
| Einmalzählung | Die Doppelabbildung in Risk Register und Compliance Check **zählt als genau ein Konsistenzvorgang** |
| Zählwirkung | Zähler **26 → 27**, Nenner **22 unverändert** (**`26/22 → 27/22`**) |

---

**R-33-Chronologie — achtundzwanzigster Konsistenzvorgang (CBP-WP-021 Queue Detail Block Staleness, 2026-09-21):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-021** — **der Nenner bleibt unverändert**, weil CBP-WP-021 seit dem achtzehnten Vorgang **bereits** Teil der erfassten Menge ist; registriert im Rahmen von CBP-WP-022 |
| Phase und Anlass | Im repositoryweiten read-only Vollständigkeitsaudit bestätigt; registriert im **R-33 Active-Status Closure Fix** |
| Fehlerklasse | **Git-/Register-Statusabweichung in einem Detailblock** — dieselbe Klasse wie der **elfte** Vorgang (*CBP-WP-014/015 Queue Detail Block Reconciliation*) |
| Betroffenes aktives Repository-Artefakt | **`project-system/WORK_PACKAGE_QUEUE.md`** — Detailblock CBP-WP-021, Felder *Status*, *Aktuelle Phase* und *Commit* |
| Falsche aktive Aussagen | *Status* **`in-review`** · *Aktuelle Phase* **„Phase C – Post-Commit Reconciliation (vorbereitet)"** · *Commit* **„nicht ausgeführt"** |
| Korrekter Zustand | **CBP-WP-021 ist `committed` und `complete`**; Phase C abgeschlossen; **B0 `0cb4ea9`** · **B1/B2 `271acc7`** · **C `0344774`** |
| Herkunft des Fehlers | *Status* und *Commit* stammen aus der Registrierung (`0cb4ea9`) und aus B1/B2 (`271acc7`); der Phase-C-Lauf (`0344774`) setzte die Phase auf „vorbereitet", schrieb die drei Felder nach dem Commit aber nicht fort. Queue-Tabelle, Kopfzeile und Übersichtsabsatz führten CBP-WP-021 bereits korrekt als `committed` |
| Abgrenzung | Die Phasenabsätze **„Phase B1/B2 (dieser Stand, uncommitted)"** und **„Phase C (dieser Stand, uncommitted)"** desselben Detailblocks sind echte phasendatierte Momentaufnahmen und bleiben unverändert |
| Erstmalige Registrierung | In den bisherigen **siebenundzwanzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | *Status* auf **`committed` · `complete`**, *Aktuelle Phase* auf **„Phase C – Post-Commit Reconciliation (abgeschlossen)"**, *Commit* auf **B0 `committed` `0cb4ea9` · B1/B2 `committed` `271acc7` · C `committed` `0344774`** — in der etablierten Form der Detailblöcke CBP-WP-020 und CBP-WP-022 |
| Einmalzählung | **ein** Detailblock · **eine** Fehlerursache · **eine** Reconciliation — **genau ein** Vorgang trotz dreier Felder |
| Zählwirkung | Zähler **27 → 28**, Nenner **22 unverändert** (**`27/22 → 28/22`**) |

---

**R-33-Chronologie — neunundzwanzigster Konsistenzvorgang (CBP-WP-019 Residual Queue Summary Status Staleness, 2026-09-21):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-019** — **der Nenner bleibt unverändert**, weil CBP-WP-019 seit dem sechzehnten Vorgang **bereits** Teil der erfassten Menge ist; registriert im Rahmen von CBP-WP-022 |
| Phase und Anlass | Im repositoryweiten read-only Vollständigkeitsaudit bestätigt; für diesen Lauf **verbindlich als eigener Vorgang** festgelegt und im **R-33 Active-Status Closure Fix** registriert |
| Fehlerklasse | **Residuum einer unvollständigen früheren Reconciliation** — eine aktive Statusaussage wurde nur teilweise ersetzt |
| Betroffenes aktives Repository-Artefakt | **`project-system/WORK_PACKAGE_QUEUE.md`** — Übersichtsabsatz unter der Queue-Tabelle |
| Falsche aktive Aussage | **„CBP-WP-019 (…) steht auf `in-review` in `committed` (`3c437f2`, …)"** — eine widersprüchliche Kombination aus `in-review` und `committed` |
| Korrekter Zustand | **CBP-WP-019 ist `committed`**, Commit **`3c437f2`** |
| Herkunft des Fehlers | Vor dem Commit lautete der Satz **„steht auf `in-review` in Phase B1.2 – Human DRC Approval Reconciliation"**; die Post-Commit-Reconciliation `387416b` ersetzte nur die Phasenangabe durch **`committed`** und ließ **„steht auf `in-review` in"** stehen |
| Abgrenzung zum sechzehnten Vorgang | Der **sechzehnte** Vorgang bleibt unverändert, wird **nicht wiedereröffnet** und **nicht rückwirkend neu gezählt** |
| Erstmalige Registrierung | In den bisherigen **achtundzwanzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | **„steht auf `in-review` in"** durch **„ist"** ersetzt; alle weiteren Angaben des Absatzes unverändert |
| Einmalzählung | Die Doppelabbildung in Risk Register und Compliance Check **zählt als genau ein Konsistenzvorgang** |
| Zählwirkung | Zähler **28 → 29**, Nenner **22 unverändert** (**`28/22 → 29/22`**) |

---

**R-33-Chronologie — dreißigster Konsistenzvorgang (CBP-WP-022 Registration Lifecycle-state Mirrors Staleness, 2026-09-21):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert** |
| Phase und Anlass | Im repositoryweiten read-only Vollständigkeitsaudit bestätigt; registriert im **R-33 Active-Status Closure Fix** |
| Fehlerklasse | **Unterbliebene Fortschreibung von Lebenszyklusaussagen bei der Registrierung eines Work Packages** — Aussagen, die nur bis zur Registrierung von CBP-WP-022 zutrafen, wurden mit dem Registrierungscommit **`e4caa14`** nicht fortgeschrieben |
| Betroffene aktive Repository-Artefakte | **zwei** — **`docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md`** (Absatz zu CBP-WP-021 im Übersichtsteil und Block *Aktueller Stand* im Abschnitt *Status*) und **`project-brain/PROJECT_BRAIN.md`** (Zeile *Geplante Work Packages*) |
| Falsche aktive Aussagen | **„Kein Work Package ist aktiv, kein Folge-Work-Package autorisiert."** (Roadmapkarte, Absatz CBP-WP-021) · **„Aktueller Stand (nachgeführt in CBP-WP-020 Phase C …)"** mit **„Kein Work Package ist aktiv; kein Folge-Work-Package über CBP-WP-020 hinaus ist autorisiert."**, ohne CBP-WP-021 und CBP-WP-022 (Roadmapkarte, Abschnitt *Status*) · **„das KB-04-Paket ist lediglich als möglicher Kandidat vorgemerkt"** (`PROJECT_BRAIN.md`) |
| Korrekter Zustand | **CBP-WP-022 ist registriert** (D-057, Registrierungscommit **`e4caa14`**) und das **aktuelle Work Package**, `in-review`, Phase **B2D-E-N14-GOV – D-067**, `committed` **`c662452`**; **CBP-WP-021 ist `committed` und `complete`** |
| Herkunft des Fehlers | Der Absatz entstand im Phase-C-Lauf von CBP-WP-021 (`0344774`), der Statusblock im Phase-C-Lauf von CBP-WP-020 (`d6a1a3c`); beide trafen zu ihrem Zeitpunkt zu. In `PROJECT_BRAIN.md` ersetzte der Registrierungslauf `e4caa14` in derselben Zeile **„CBP-WP-022 nicht registriert …"** durch **„CBP-WP-023 nicht registriert …"**, ließ den anschließenden Kandidatenhinweis auf das KB-04-Paket aber stehen |
| Aktiv, nicht historisch | Alle Fundstellen stehen **unmarkiert** in aktiven Statusdarstellungen; der Statusblock bezeichnet sich selbst als **Aktueller Stand** |
| Erstmalige Registrierung | In den bisherigen **neunundzwanzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Roadmapkarte: Absatz CBP-WP-021 und Statusblock auf den aktuellen Lebenszyklus gebracht (**CBP-WP-021 `committed`**, **CBP-WP-022 registriert und aktuell `in-review`**); die früheren Aussagen zum Aktivitäts- und Autorisierungsstand blieben **inhaltlich erhalten** und sind ausdrücklich auf ihren Abschlusszeitpunkt bezogen („Zum Abschluss von CBP-WP-020" bzw. „… von CBP-WP-021"). `PROJECT_BRAIN.md`: Kandidatenhinweis durch die Registrierung als **CBP-WP-022** (D-057, `e4caa14`) und den Status `in-review` ersetzt; **„CBP-WP-023 nicht registriert, nicht begonnen, nicht autorisiert"** blieb **wörtlich** erhalten |
| Einmalzählung | **ein** Ereignis — die Registrierung von CBP-WP-022 — · **ein** korrekter Lebenszyklusstand · **eine** Fehlerursache — **genau ein** Vorgang trotz dreier Fundstellen in zwei Dateien |
| Zählwirkung | Zähler **29 → 30**, Nenner **22 unverändert** (**`29/22 → 30/22`**) |

Damit waren **dreißig Konsistenzvorgänge in zweiundzwanzig Work Packages**
dokumentiert (*Stand nach dem dreißigsten Vorgang; durch den
einunddreißigsten Vorgang unten auf **31/22** aktualisiert*; löste die vorige
Angabe „dreiundzwanzig" ab). Die Zahl der Work Packages bleibt **zweiundzwanzig**: Die
Vorgänge 24 bis 27 und 30 betreffen das seit dem neunzehnten Vorgang erfasste
CBP-WP-022, Vorgang 28 das seit dem achtzehnten Vorgang erfasste CBP-WP-021 und
Vorgang 29 das seit dem sechzehnten Vorgang erfasste CBP-WP-019; sie erhöhen
**ausschließlich** den Vorgangszähler. Vollständige Progression seit dem
neunzehnten Vorgang: **19/22 → 20/22 → 21/22 → 22/22 → 23/22 → 24/22 → 25/22 →
26/22 → 27/22 → 28/22 → 29/22 → 30/22**. Die **Erweiterungen der Vorgänge 21
und 23 sind zählneutral**. **`30/22` ist kein Erfüllungsgrad und keine
Prozentkennzahl**; **`30/23` und `31/22` sind unzulässig**.

**Bekannter, zurückgestellter Befund AF-6 — kein Konsistenzvorgang dieser
Chronologie:** Die Angaben zum Git-Gesamtzähler und zum HEAD in
`project-brain/PROJECT_BRAIN.md`, `project-system/HEALTH_SCORE.md` und
`project-system/PROJECT_MANIFEST.md` (**Commits 29**, HEAD **`9c6c0fb`**) sind
veraltet. **D-056 Teil T** nimmt die Commitzähler-Governance aus und verweist
sie in eine separate Governance-Note; CBP-WP-022 schließt sie ausdrücklich aus
(Non-Goal *keine Commitzähler-Governance*). Gemäß **A0-Festlegung** für diesen
Lauf (**keine neue Decision-ID**) ist AF-6 **bekannt und zurückgestellt**, **kein
einunddreißigster Vorgang** und **ohne Zählwirkung**; die drei Felder bleiben
**unverändert**.

**R-33 bleibt `gemindert, nicht geschlossen`**, Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**; **das
projektweite Konsistenzrisiko ist nicht beseitigt** — sieben weitere Vorgänge
derselben Grundklasse, gefunden erst durch einen repositoryweiten
Vollständigkeitsaudit, belegen es unmittelbar. Dieselben Vorgänge sind in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und **zählen je nur
einmal**. Die dortige Darstellung folgt der **Prosaform** jenes Dokuments,
während hier die **Tabellenform** des Risk Registers verwendet wird; **Fakten,
Zahlen, Closure-Grenze und R-33-Wirkung sind identisch**.

---

**R-33-Chronologie — einunddreißigster Konsistenzvorgang (CBP-WP-022 Active B2 Authorization Umbrella Staleness, 2026-10-15):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert**, weil CBP-WP-022 seit dem neunzehnten Vorgang **bereits** Teil der erfassten Menge ist |
| Phase und Anlass | Im abgeschlossenen read-only **Finding-A/B Classification Review** als **Finding B** klassifiziert (`VALID_ACTIVE_STALENESS`, Primärklasse **R-33**); gemäß **A0-Festlegung** des Human Maintainers für diesen Lauf (2026-10-15, **keine neue Decision-ID**) als eigener Vorgang registriert in der **Finding-A/B-Reconciliation** |
| Fehlerklasse | **Unterbliebene Fortschreibung einer aktiven Autorisierungs-Sammelaussage** — eine pauschale Aussage über die Gesamtphase B2 blieb stehen, nachdem B2 in granulare Teilphasen zerlegt und mehrere davon autorisiert, abgeschlossen und committet worden waren |
| Betroffenes aktives Repository-Artefakt | **`work-packages/CBP-WP-022.md`** — Abschlussvermerk unmittelbar unter der Phasenmodelltabelle im Abschnitt *Phasenmodell* |
| Falsche aktive Aussage | **„B2 bleibt nicht autorisiert."** |
| Korrekter Zustand | Der Autorisierungsstand ist **je Teilphase** im Phasenmodell geführt: mehrere B2-Teilphasen — **B2A `929d10b`** bis **B2D-E-N14-GOV `c662452`** — sind abgeschlossen und `committed`; **B2D-H**, **B2D-E**, **B2D-V**, **B2D-G**, **B2B-Apply** sowie die Aggregatzeilen **B2C** und **B2D** bleiben **nicht autorisiert** |
| Herkunft des Fehlers | Die Aussage entstand im **B1C**-Lauf (Commit **`24de07e`**, 2026-08-04), als B2 noch als **ungeteilte** Phase geführt wurde und tatsächlich nicht autorisiert war. Mit der Zerlegung in granulare Teilphasen ab **B2A** (`929d10b`) wurde sie **nicht fortgeschrieben** und widersprach seitdem der unmittelbar darüberstehenden Phasenmodelltabelle — der Widerspruch ist dateiintern belegt |
| Aktiv, nicht historisch | Der Vermerk steht **unmarkiert** im aktiven Abschnitt *Phasenmodell* direkt unter der Live-Statustabelle, nicht in einem phasendatierten Abschnitt *Stand nach …*. Die phasengebundenen Aussagen **„B2-Kandidat — nicht autorisiert"** und **„B2 nicht autorisiert"** im Abschnitt *Phase B1C* (einschließlich *Stand nach B1C*) sind echte Momentaufnahmen und bleiben **unverändert** |
| Erstmalige Registrierung | In den bisherigen **dreißig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Die Sammelaussage wurde durch einen **nicht duplizierenden Verweis** ersetzt: **„Maßgeblich für den Autorisierungsstand der B2-Teilphasen ist ausschließlich das Phasenmodell; die dort als `nicht autorisiert` geführten Teilphasen und Aggregate bleiben nicht autorisiert."** Es entsteht **kein** weiterer manuell zu pflegender Sammelspiegel; **kein Phasenstatus verändert**, **keine neue Autorisierung** |
| Abgrenzung | **Kein AF-6-Fall** und **keine zählneutrale Erweiterung** der Vorgänge 20 bis 30. Die Fortschreibung der Zählerspiegel auf `31/22` in weiteren Dateien ist **kein** eigener Befund und erzeugt **keinen** weiteren Vorgang. Der im selben Lauf behobene **Finding A** — der veraltete feste ADR-Bereich in der Quellentabelle von `CLAUDE.md` — ist ein **R-16**-Dokumentationspflegefall, **zählt nicht** zu R-33 und ist **nicht** Teil dieses Vorgangs; R-16 bleibt **offen** |
| Einmalzählung | **eine** Aussage · **eine** Fehlerursache · **eine** Reconciliation — **genau ein** Vorgang; die Doppelabbildung in Risk Register und Compliance Check **zählt nur einmal** |
| Zählwirkung | Zähler **30 → 31**, Nenner **22 unverändert** (**`30/22 → 31/22`**) |
| Aussagegrenze | **Keine technische Implementierungsänderung**, **keine neue Decision**, **keine ADR**, **keine Risikoänderung**, **keine neue Risiko-ID**, **keine Teständerung**, **keine Traceabilityänderung**, **keine Capabilityänderung**, **kein Phasenstatus und keine Autorisierung verändert**; **D-067** unverändert; **KB-04 bleibt `DOCUMENTED ONLY`**; beide Gates bleiben `NOT EVALUATED`; **`KB04-T-N14`**, **NT-04** und **NT-05** nicht ausgeführt; **B2D-E**, **B2D-V**, **B2D-G** und **B2B-Apply** nicht autorisiert; **OD-37**, **Contract §10.3** und **R-20** bleiben offen; **CBP-WP-023** nicht registriert |

Damit waren **einunddreißig Konsistenzvorgänge in zweiundzwanzig Work
Packages** dokumentiert (*Stand nach dem einunddreißigsten Vorgang: `31/22`;
durch die Vorgänge zweiunddreißig bis vierzig unten auf **40/22**
aktualisiert*; löste die vorige Angabe „dreißig" ab). Die Zahl der Work Packages bleibt **zweiundzwanzig**: Vorgang
**31** betrifft das seit dem neunzehnten Vorgang erfasste CBP-WP-022 und erhöht
**ausschließlich** den Vorgangszähler. Vollständige Progression seit dem
neunzehnten Vorgang: **19/22 → 20/22 → 21/22 → 22/22 → 23/22 → 24/22 → 25/22 →
26/22 → 27/22 → 28/22 → 29/22 → 30/22 → 31/22**. **`31/22` ist kein
Erfüllungsgrad und keine Prozentkennzahl**; **`31/23` und `32/22` sind
unzulässig**.

**R-33 bleibt `gemindert, nicht geschlossen`**, Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**; **das
projektweite Konsistenzrisiko ist nicht beseitigt** — eine seit B2A
stehengebliebene Sammelaussage, die im R-33 Active-Status Closure Fix nicht
registriert wurde, belegt es unmittelbar. Derselbe Vorgang ist in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und **zählt nur einmal**.
Die dortige Darstellung folgt der **Prosaform** jenes Dokuments, während hier
die **Tabellenform** des Risk Registers verwendet wird; **Fakten, Zahlen,
Closure-Grenze und R-33-Wirkung sind identisch**.

---

**R-33-Chronologie — Vorgänge zweiunddreißig bis vierzig (CBP-WP-022 Pre-Closure Governance Reconciliation R4, 2026-10-15/16):**

Vor einer späteren Closure von CBP-WP-022 stellte eine Pre-Closure-Diagnose am
**2026-10-15** weitere veraltete aktive Spiegel fest; ein **vollständiger
read-only Audit aller aktiven Statusspiegel** am **2026-10-16** ergänzte weitere
Fundstellen. Gemäß **Human-Maintainer A0, 2026-10-16** (R4-Scopefreigabe)
registriert die **CBP-WP-022 Pre-Closure Governance Reconciliation R4** genau
**neun** neue Vorgänge. Für alle neun gilt dieselbe **Aussagegrenze**: **keine
technische Implementierungsänderung**, **keine ADR**, **keine Änderung von
Risikodatensätzen, Severity oder Risikostatus**, **keine neue Risiko-ID**, **keine
Teständerung und keine neue Testausführung**, **keine Traceabilityänderung**,
**keine Capabilityänderung**, **kein Phasenstatus und keine Autorisierung
verändert**; die einzige neue Decision ist **D-068** (Closure-Grenze, `accepted`,
**A0**, 2026-10-15), die **keine Closure ausführt**; **D-001 bis D-067**
unverändert; **CBP-WP-022 bleibt `in-review`**; **KB-04 bleibt `DOCUMENTED
ONLY`**; beide Gates bleiben `NOT EVALUATED`; **`KB04-T-N14`**, **NT-04** und
**NT-05** nicht ausgeführt; **B2D-H**, **B2D-E**, **B2D-V**, **B2D-G** und
**B2B-Apply** nicht autorisiert; **OD-37**, **Contract §10.3** und **R-20** bleiben
offen; **CBP-WP-023** nicht registriert. Der gesondert erfasste
**Altdrift-Prüfbestand D-1 bis D-10** ([COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md),
*R4 Deferred Legacy-Drift Inventory*) ist **kein** Vorgang dieser Chronologie,
**nicht klassifiziert**, **nicht bereinigt** und **ohne Zählwirkung**.

**R-33-Chronologie — zweiunddreißigster Konsistenzvorgang (CBP-WP-022 Active Authorization and Implementation Mirrors Staleness, 2026-10-15; erweitert 2026-10-16):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert**, weil CBP-WP-022 seit dem neunzehnten Vorgang **bereits** Teil der erfassten Menge ist |
| Phase und Anlass | Sechs Befundgruppen in der Pre-Closure-Diagnose vom **2026-10-15**, fünf weitere (**Z-1**, **Z-3**, **Z-4**, **Z-7**, **Z-8**) im vollständigen read-only Audit vom **2026-10-16**; registriert gemäß **Human-Maintainer A0, 2026-10-16** |
| Fehlerklasse | **Unterbliebene Fortschreibung grober aktiver Autorisierungs- und Implementierungsspiegel** — pauschale Aussagen über B1, B2, B2C-T oder die „technische Implementierung" blieben stehen, nachdem B1A bis B1C, B2A, B2B-P und B2C-T-R **granular autorisiert, ausgeführt und committet** waren; dieselbe Grundklasse wie der einunddreißigste Vorgang, jedoch **andere Fundstellen** |
| Betroffene aktive Repository-Artefakte | **elf Befundgruppen in sieben Dateien** — **32-A** `project-system/WORK_PACKAGE_QUEUE.md` (Kopfzeile *Aktuelles Work Package*) · **32-B** dieselbe Datei (Übersichtsabsatz CBP-WP-022) · **32-C** dieselbe Datei (Detailblock CBP-WP-022, Feld *Technische Implementierung*) · **N-1a** `project-system/PROJECT_MANIFEST.md` (*Aktuelles Work Package*) · **N-2** `project-brain/PROJECT_BRAIN.md` (*Geplante Work Packages*) · **N-3** `project-system/HEALTH_SCORE.md` (*Vorgeschlagene Work Packages*) · **Z-1** `README.md` (*Nächster Schritt*) · **Z-3** `project-system/PROJECT_PROFILE.md` (Roadmapzeile *Phase 1*) · **Z-4** `work-packages/CBP-WP-022.md` (*Aussageschutz*) · **Z-7** dieselbe Datei (*Voraussetzungen*) · **Z-8** `project-brain/PROJECT_BRAIN.md` (Phase-C-/Registrierungsnachtrag CBP-WP-021) |
| Falsche aktive Aussagen | **32-A** „B2C-T-Resume, B2B-Apply und B2D nicht autorisiert" · **32-B** „B1 und B2 sind nicht autorisiert" · **32-C** „Technische Implementierung: nicht autorisiert" · **N-1a** „technische B2C-T-Implementierung noch nicht begonnen und nicht autorisiert" · **N-2** „B2 nicht autorisiert" · **N-3** „B2C-T/B2B-Apply/B2D nicht autorisiert" · **Z-1** „Die technische Umsetzung von KB-04 ist nicht autorisiert; B1 und B2 sind nicht freigegeben" · **Z-3** „B2B-Apply/B2C-T/B2D nicht autorisiert" · **Z-4** „B2C-T ist nicht autorisiert, es entstand kein Test-, Fixture- oder Produktionscode" als Gesamtaussage · **Z-7** „Separate Human-Freigabe für B1/B2 — nicht erteilt" als Dauerzustand · **Z-8** „die technische Umsetzung bleibt nicht autorisiert" |
| Korrekter Zustand | Die Autorisierung ist **je Teilphase** im Phasenmodell von CBP-WP-022 geführt; B1A `1a7696d`, B1B `b86a35f`, B1C `24de07e`, B2A `929d10b`, B2B-P `fff8227`, B2C.1 `38eb33f`, B2C.2 `117647f` und **B2C-T-R `9cde9de`** sind autorisiert, abgeschlossen und `committed`; der **erste B2C-T-Lauf** endete `BLOCKED` ohne Dateiänderung; B2C-T-R lieferte **drei Testdateien** und **152 Tests**; **internes read-only Modell und Validator, plan-only Initialisierung und synthetische Traceability existieren**; **keine operative KB-04-Durchsetzung**, **keine B2D-E-Ausführung**; **B2B-Apply**, **B2D-H/E/V/G** sowie die Aggregate **B2C** und **B2D** bleiben **nicht autorisiert** — **keine pauschale B2-Freigabe** |
| Herkunft des Fehlers | Die Aussagen entstanden zwischen der Registrierung **`e4caa14`** (32-B, 32-C, Z-1, Z-7, Z-8) und B2C.2 **`117647f`** (32-A, Z-3), dazwischen **`24de07e`** (N-2) und **`38eb33f`** (N-1a, N-3, Z-4); jede traf zu ihrem Zeitpunkt zu und wurde mit den folgenden Teilphasen **nicht fortgeschrieben** |
| Aktiv, nicht historisch | Alle Fundstellen stehen in **aktiven** Statusfeldern, Detailblockfeldern, der Voraussetzungstabelle beziehungsweise im aktiven *Aussageschutz*. **Historische Abgrenzung:** die phasengebundenen Abschnitte *Stand nach …*, die Entscheidungsnotizen zu D-057 bis D-062 und die phasengebundenen Teststände **930** und **1050** bleiben unverändert; die Aussage über **D-061** (Z-4) sowie die Registrierungsbedingung (Z-7, Z-8) bleiben **inhaltlich erhalten** und sind **zeitlich gekennzeichnet**. **N-4** und **N-5** („B2B-Apply und B2D nicht autorisiert" in `CLAUDE.md` und `PROJECT_BRAIN.md`) sind kanonisch korrekt, weil B2D dort das nicht autorisierte Aggregat bezeichnet, und **nicht** Teil dieses Vorgangs |
| Erstmalige Registrierung | In den bisherigen **einunddreißig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | 32-A, N-3 und Z-3: **erster B2C-T-Lauf `BLOCKED`, B2C-T-R `committed` (`9cde9de`), B2B-Apply und Aggregat B2D nicht autorisiert** · 32-B, N-2: **granularer Phasenstatus maßgeblich, keine pauschale B2-Freigabe** · 32-C: **internes read-only Modell und Validator, plan-only Initialisierung und synthetische Traceability implementiert, keine operative KB-04-Durchsetzung** · N-1a: **B2C-T-R abgeschlossen, drei Testdateien, 152 zusätzliche Tests** · Z-1: abgeschlossene B1-/B2-Teilphasen anerkannt, **reale KB-04-Enforcement- und B2D-E-Ausführung weiterhin nicht autorisiert** · Z-4: D-061 als Scopeentscheidung ohne Code, **B2C-T-R später autorisiert und abgeschlossen**, kein neues Produktionsmodul, keine operative Evidenz · Z-7, Z-8: Registrierungsstand als zeitbezogen gekennzeichnet, spätere Teilphasen **granular autorisiert und ausgeführt**, keine B2D-E-Ausführung |
| Einmalzählung | **eine** Fehlerursache · **eine** gemeinsame Reconciliation — **genau ein** Vorgang trotz **elf** Befundgruppen in sieben Dateien; die Doppelabbildung in Risk Register und Compliance Check **zählt nur einmal** |
| Zählwirkung | Zähler **31 → 32**, Nenner **22 unverändert** (**`31/22 → 32/22`**) |

---

**R-33-Chronologie — dreiunddreißigster Konsistenzvorgang (CBP-WP-022 Active Decision/A0 Counter Mirrors Staleness, 2026-10-15):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert** |
| Phase und Anlass | Pre-Closure-Diagnose vom **2026-10-15**; registriert gemäß **Human-Maintainer A0, 2026-10-16** |
| Fehlerklasse | **Unterbliebene Fortschreibung aktiver Decision-, A0- und ADR-Zählerspiegel** bei neuen Decisions |
| Betroffene aktive Repository-Artefakte | **drei Befundgruppen** — **A** `project-system/HEALTH_SCORE.md` (*Dimensionen*, Zeile *Entscheidungslage*) · **B** dieselbe Datei (*Kennzahlen*, Zeilen *Getroffene Entscheidungen* und *davon A0*) · **C** `project-system/PROJECT_MANIFEST.md` (*Aktuelles Work Package*, Schlussklausel **N-1c**) |
| Falsche aktive Aussagen | **A** „56 Entscheidungen (52 mit A0), 13 angenommene ADRs" · **B** „61" und „57" · **C** „Zähler unverändert 60/56/14" — im selben Feld widersprochen durch den aktuelleren Zähler 67/63/14 |
| Korrekter Zustand | Vor D-068 **67/63/14**; nach D-068 **68 Decisions, 64 mit A0, 14 angenommene ADRs** |
| Herkunft des Fehlers | **A** entstand in **`0cb4ea9`** (D-056) und ist seit D-057 veraltet · **B** wurde zuletzt in **`38eb33f`** (D-061) fortgeschrieben · **C** entstand in **`929d10b`** (B2A) |
| Abgrenzung zum neunzehnten Vorgang | Der **neunzehnte** Vorgang korrigierte denselben Rückstand nur in `CLAUDE.md` und `PROJECT_BRAIN.md`; er bleibt **byte-identisch**, wird **weder wiedereröffnet noch erweitert** |
| Erstmalige Registrierung | In den bisherigen **zweiunddreißig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | **A** auf **„68 Entscheidungen (64 mit A0), 14 angenommene ADRs"** · **B** auf **68** und **64** · **C** redundante Schlussklausel entfernt; die Zähler stehen kanonisch in den Feldern *Getroffene Entscheidungen* und *Angenommene ADRs* desselben Dokuments, der D-067-Stand 67/63/14 ist dort als phasengebunden gekennzeichnet |
| Einmalzählung | **ein** Spiegeltyp · **eine** Fehlerursache — **genau ein** Vorgang trotz dreier Befundgruppen in zwei Dateien |
| Zählwirkung | Zähler **32 → 33**, Nenner **22 unverändert** (**`32/22 → 33/22`**) |

---

**R-33-Chronologie — vierunddreißigster Konsistenzvorgang (CBP-WP-022 Active Risk Aggregate Mirrors Staleness, 2026-10-15; erweitert 2026-10-16):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert** |
| Phase und Anlass | Zwei Befunde in `HEALTH_SCORE.md` in der Pre-Closure-Diagnose vom **2026-10-15**; **Z-9** und **Z-10** desselben Spiegeltyps im vollständigen Audit vom **2026-10-16**; registriert gemäß **Human-Maintainer A0, 2026-10-16** |
| Fehlerklasse | **Unterbliebene Fortschreibung aktiver Risikoaggregatspiegel** nach einer kanonischen Aggregatreconciliation |
| Betroffene aktive Repository-Artefakte | **vier falsche aktive Spiegel** — `project-system/HEALTH_SCORE.md` (*Kennzahlen*, Zeilen *Erfasste Risiken* und *davon hoch*) · `project-brain/PROJECT_BRAIN.md` (Abschnitt *Risiken*, **Z-9**) · `project-system/PROJECT_PROFILE.md` (Abschnitt *Risiken*, **Z-10**) |
| Falsche aktive Aussagen | **32** erfasste Risiken und **17** hoch (alle vier Spiegel) |
| Korrekter Zustand | Kanonisch **35** Risiken · hoch **20** · mittel **14** · niedrig **1** · gemindert **14** · offen **13**; die HEALTH_SCORE-Zeile *davon gemindert* **14** war bereits korrekt und bleibt unverändert |
| Herkunft des Fehlers | Die Werte stammen aus **`b1a6c2f`** (CBP-WP-003) und spiegelten die kanonische Zusammenfassung, bis **B2D-GOV** (**`7e8328a`**, D-063) diese vollständig neu auszählte und auf **35/20** reconciliierte; die Spiegel wurden dabei **nicht** nachgeführt |
| Abgrenzung | Die **kanonische Aggregatreconciliation aus B2D-GOV/D-063 bleibt unangetastet**; **keine Änderung an Risikodatensätzen**; die Listen *Weiterhin kritisch* gehören zum zurückgestellten Prüfbestand **D-3** und bleiben unverändert |
| Erstmalige Registrierung | In den bisherigen **dreiunddreißig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Alle vier Spiegel auf **35** beziehungsweise **20 hoch** gebracht |
| Einmalzählung | **ein** Spiegeltyp · **eine** Fehlerursache — **genau ein** Vorgang trotz vier Spiegeln in drei Dateien |
| Zählwirkung | Zähler **33 → 34**, Nenner **22 unverändert** (**`33/22 → 34/22`**) |

---

**R-33-Chronologie — fünfunddreißigster Konsistenzvorgang (CBP-WP-022 PROJECT_MANIFEST Active Test Count Mirror Staleness, 2026-10-16):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert** |
| Phase und Anlass | Befund **N-1b**; registriert gemäß **Human-Maintainer A0, 2026-10-16** |
| Fehlerklasse | **Unterbliebene Fortschreibung eines aktiven Testzählerspiegels** |
| Betroffenes aktives Repository-Artefakt | **`project-system/PROJECT_MANIFEST.md`** — Feld *Aktuelles Work Package*, Schlussklausel zum Implementierungspfad |
| Falsche aktive Aussage | **„Gesamtsuite 1050"** |
| Korrekter Zustand | Zuletzt dokumentierte bestandene Gesamtsuite **1202** (seit **B2C-T-R**, `9cde9de`); **1050** war der Stand nach **B2B-P** (`fff8227`) |
| Herkunft des Fehlers | Die Klausel entstand in **`fff8227`** (B2B-P) und wurde mit B2C-T-R nicht fortgeschrieben; dasselbe Feld führt an anderer Stelle bereits **1202** — der Widerspruch ist dateiintern belegt |
| Abgrenzung | Historische, eindeutig phasengebundene Teststände — **724** im WP-020-Eintrag (**Z-16**), **930** nach B2A, **1050** nach B2B-P in phasengebundenen Sätzen — bleiben erhalten. **R4 hat keine Tests ausgeführt**; die 1202 sind der **zuletzt dokumentierte** Stand, **keine neue Messung**; **keine Testdatei verändert** |
| Erstmalige Registrierung | In den bisherigen **vierunddreißig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Die Klausel ist als **B2B-P-Stand** gekennzeichnet und nennt die **zuletzt dokumentierte Gesamtsuite 1202** |
| Einmalzählung | **eine** Fundstelle · **eine** Fehlerursache — **genau ein** Vorgang |
| Zählwirkung | Zähler **34 → 35**, Nenner **22 unverändert** (**`34/22 → 35/22`**) |

---

**R-33-Chronologie — sechsunddreißigster Konsistenzvorgang (CBP-WP-022 Residual Registration Lifecycle-state Mirror Staleness, 2026-10-16):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert** |
| Phase und Anlass | Befund **Z-5** im vollständigen Audit vom **2026-10-16**; registriert gemäß **Human-Maintainer A0, 2026-10-16** |
| Fehlerklasse | **Unterbliebene zeitliche Abgrenzung einer Lebenszyklusaussage bei der Registrierung eines Work Packages** — dieselbe Grundklasse wie der dreißigste Vorgang, jedoch eine dort **nicht erfasste** Fundstelle |
| Betroffenes aktives Repository-Artefakt | **`project-system/PROJECT_MANIFEST.md`** — Feld *Zuletzt abgeschlossen* |
| Falsche aktive Aussage | **„Kein Folge-Work-Package autorisiert."** |
| Korrekter Zustand | **CBP-WP-021** ist zuletzt abgeschlossen; **CBP-WP-022** ist registriert (D-057, `e4caa14`) und aktuell **`in-review`**; **CBP-WP-023** ist nicht registriert und nicht autorisiert |
| Herkunft des Fehlers | Der Satz entstand im Phase-C-Lauf von CBP-WP-021 (**`0344774`**) und traf zu diesem Zeitpunkt zu; mit der Registrierung **`e4caa14`** wurde er **nicht zeitlich abgegrenzt** |
| Abgrenzung zum dreißigsten Vorgang | Der **dreißigste** Vorgang wird **nicht rückwirkend erweitert**; die Restfundstelle ist nach der Präzedenz des neunundzwanzigsten Vorgangs ein **eigener** Vorgang. **Keine neue Work-Package-Registrierung** |
| Erstmalige Registrierung | In den bisherigen **fünfunddreißig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | **„Zum Abschluss von CBP-WP-021 war kein Folge-Work-Package autorisiert; seitdem ist CBP-WP-022 registriert (D-057, `e4caa14`) und aktuell `in-review`."** |
| Einmalzählung | Die Doppelabbildung in Risk Register und Compliance Check **zählt als genau ein Konsistenzvorgang** |
| Zählwirkung | Zähler **35 → 36**, Nenner **22 unverändert** (**`35/22 → 36/22`**) |

---

**R-33-Chronologie — siebenunddreißigster Konsistenzvorgang (CBP-WP-022 Decision Register ADR-Gate Summary Count Error, 2026-10-16):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert** |
| Phase und Anlass | Befund **Z-6** im vollständigen Audit vom **2026-10-16**; registriert gemäß **Human-Maintainer A0, 2026-10-16** |
| Fehlerklasse | **Fortgeschriebene relative Zählformel in einer kanonischen Zusammenfassung** — die Formel „die letzten N" wurde je Decision um eins erhöht, statt gegen die Einzelzeilen ausgezählt zu werden (Zähl- und Statusregel 1 bis 3) |
| Betroffenes aktives Repository-Artefakt | **`project-system/DECISION_REGISTER.md`** — *Zusammenfassung*, Zeile *Neu in CBP-WP-022* |
| Falsche aktive Aussage | **„die letzten neun je `ADR_NOT_REQUIRED` innerhalb ADR-0014"** (Stand D-067) |
| Korrekter Zustand | **D-057** `ADR_NOT_REQUIRED` **ausschließlich für die Registrierung** · **D-058** `ADR_REQUIRED` · **D-059** `ADR-0014_ACCEPTED` · **D-060 bis D-067**: **acht** Entscheidungen `ADR_NOT_REQUIRED` innerhalb ADR-0014. **Nach D-068: neun** (**D-060 bis D-068**) |
| Herkunft des Fehlers | Die Formel entstand in **`38eb33f`** (D-061) mit „drei" statt korrekt **zwei** und wurde mit jeder folgenden Decision um eins fortgeschrieben — „vier" (`117647f`), „fünf" (`7e8328a`), „sechs" (`1222ec0`), „sieben" (`0cd21f5`), „acht" (`c4b0426`), „neun" (`c662452`); **D-059** wurde dabei stets mitgezählt. **Der Fehler bestand vor D-068** |
| Abgrenzung | Die **alte Summenbehauptung wird nicht als nun zufällig zutreffend weitergeführt**: nach D-068 wären „die letzten neun" zwar arithmetisch neun, die Formel bliebe aber eine unbelegte Fortschreibung. **Die einzelnen Decisions D-057 bis D-067 bleiben unverändert**; **keine ADR** |
| Erstmalige Registrierung | In den bisherigen **sechsunddreißig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Die relative Formel ist durch den **expliziten Bereich** ersetzt: **„D-060 bis D-068 je `ADR_NOT_REQUIRED`, innerhalb ADR-0014"**, mit Hinweis auf die frühere Abweichung |
| Einmalzählung | **eine** Zeile · **eine** Fehlerursache — **genau ein** Vorgang, obwohl die Formel über sieben Commits fortgeschrieben wurde |
| Zählwirkung | Zähler **36 → 37**, Nenner **22 unverändert** (**`36/22 → 37/22`**) |

---

**R-33-Chronologie — achtunddreißigster Konsistenzvorgang (CBP-WP-022 ADR Index Count and Entry Staleness, 2026-10-16):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-022** — **der Nenner bleibt unverändert** |
| Phase und Anlass | Befund **Z-11** im vollständigen Audit vom **2026-10-16**; registriert gemäß **Human-Maintainer A0, 2026-10-16** |
| Fehlerklasse | **Unterbliebene Fortschreibung eines kanonischen Indexartefakts** bei der Annahme eines ADR — dieselbe Fehlerklasse wie der **vierzehnte** Vorgang (*CBP-WP-018 ADR-Index-Zählkorrektur*) |
| Betroffenes aktives Repository-Artefakt | **`docs/decisions/README.md`** — Kopffeld *Angenommene ADRs*, Abschnitt *Aktueller Stand* und ADR-Tabelle |
| Falsche aktive Aussagen | Kopffeld **13** · „**Dreizehn** angenommene ADRs." · „Alle **dreizehn** tragen A1" · Tabelle endet bei **ADR-0013** |
| Korrekter Zustand | **14** angenommene ADRs; **ADR-0014** *KB-04 Stage 1 Filesystem Enforcement Architecture*, `accepted`, **A1**, 2026-08-03, belegt durch **D-059** (A0) |
| Herkunft des Fehlers | ADR-0014 wurde in **B1B** (**`b86a35f`**, 2026-08-03) angelegt und angenommen; der Index (zuletzt **`4dec921`**, CBP-WP-018 Phase B0) wurde dabei **nicht** nachgeführt |
| Abgrenzung zum vierzehnten Vorgang | Der **vierzehnte** Vorgang bleibt unverändert und wird **nicht wiedereröffnet**; die ältere Herkunft des Indexfehlers bleibt dort nachvollziehbar. **Keine ADR-Datei verändert**, **keine weitere ADR** |
| Erstmalige Registrierung | In den bisherigen **siebenunddreißig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Kopffeld auf **14**, Fließtext auf **vierzehn** einschließlich ADR-0014, Tabelleneintrag **ADR-0014** ergänzt; die Indexmetadaten *Überarbeitet in* und *Stand* sind auf diesen Lauf nachgeführt |
| Einmalzählung | **ein** Artefakt · **eine** Fehlerursache — **genau ein** Vorgang trotz vier Fundstellen |
| Zählwirkung | Zähler **37 → 38**, Nenner **22 unverändert** (**`37/22 → 38/22`**) |

---

**R-33-Chronologie — neununddreißigster Konsistenzvorgang (CBP-WP-019 Residual DRC Gate-status Mirror Staleness, 2026-10-16):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-019** — **der Nenner bleibt unverändert**, weil CBP-WP-019 seit dem sechzehnten Vorgang **bereits** Teil der erfassten Menge ist; registriert im Rahmen von CBP-WP-022 |
| Phase und Anlass | Befund **Z-12** im vollständigen Audit vom **2026-10-16**; registriert gemäß **Human-Maintainer A0, 2026-10-16** |
| Fehlerklasse | **Residuum einer unvollständigen früheren Statusfortschreibung** — ein aktiver Gate-Statusspiegel wurde mit der DRC-Genehmigung nicht nachgeführt |
| Betroffenes aktives Repository-Artefakt | **`project-system/COMPLIANCE_CHECK.md`** — Tabelle *Offene Punkte* |
| Falsche aktive Aussage | **„DRC definiert, aber NOT EVALUATED"** |
| Korrekter Zustand | Der Deployment Readiness Check ist für **Profil A** bewertet und **`APPROVED BY HUMAN MAINTAINER`** (CBP-WP-019, **D-054**, 2026-07-29) — **19 Prüfpunkte, 19 `ready`, 0 `blocked`** |
| Herkunft des Fehlers | Die Zeile entstand in **`4cddc28`** (CBP-WP-004) und traf bis CBP-WP-019 zu; mit **`3c437f2`** (D-054) wurde sie **nicht** fortgeschrieben |
| Abgrenzung | **Die DRC-Genehmigung ist rein dokumentarisch** — **keine** Installations-, Betriebs- oder produktive Sicherheitsfreigabe, **keine** Mapping-Activation-Gate- und **keine** Security-Foundation-Readiness-Gate-Evaluation; **beide Gates bleiben `NOT EVALUATED`**, **R-34 bleibt offen**, **kein Deployment**. Der **sechzehnte** und der **neunundzwanzigste** Vorgang bleiben unverändert und werden nicht wiedereröffnet |
| Erstmalige Registrierung | In den bisherigen **achtunddreißig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Die Zeile gibt den genehmigten DRC-Stand mit der verbindlichen Abgrenzung wieder |
| Einmalzählung | **eine** Zeile · **eine** Fehlerursache — **genau ein** Vorgang |
| Zählwirkung | Zähler **38 → 39**, Nenner **22 unverändert** (**`38/22 → 39/22`**) |

---

**R-33-Chronologie — vierzigster Konsistenzvorgang (CBP-WP-020/021 Residual Closure Header Commit-status Staleness, 2026-10-16):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-020** und **CBP-WP-021** — **der Nenner bleibt unverändert**, weil CBP-WP-020 seit dem siebzehnten und CBP-WP-021 seit dem achtzehnten Vorgang **bereits** Teil der erfassten Menge sind; registriert im Rahmen von CBP-WP-022 |
| Phase und Anlass | Befund **Z-13** im vollständigen Audit vom **2026-10-16**; registriert gemäß **Human-Maintainer A0, 2026-10-16** |
| Fehlerklasse | **Unterbliebene Post-Commit-Fortschreibung der Phase-C-Kopf- und Commitstatusspiegel** in den Work-Package-Dateien |
| Betroffene aktive Repository-Artefakte | **`work-packages/CBP-WP-020.md`** — Kopffeld *Commit* · **`work-packages/CBP-WP-021.md`** — Kopffelder *Aktuelle Phase* und *Commit* |
| Falsche aktive Aussagen | WP-020: „— Phase C uncommitted" · WP-021: „Phase C – Post-Commit Reconciliation (vorbereitet)" · „— Phase C uncommitted" |
| Korrekter Zustand | **CBP-WP-020** `committed` · `complete`, Phase C **`committed` `d6a1a3c`** · **CBP-WP-021** `committed` · `complete`, Phase C abgeschlossen und **`committed` `0344774`** |
| Herkunft des Fehlers | Die Fundstellen entstanden in den Phase-C-Läufen **vor** den Commits **`d6a1a3c`** (2026-07-29) beziehungsweise **`0344774`** (2026-08-03); die Post-Commit-Fortschreibung unterblieb, obwohl die Kopffelder *Status* bereits `committed` · `complete` führten |
| Aktiv, nicht historisch | Die Kopffelder *Aktuelle Phase* und *Commit* sind **aktive** Statusspiegel. **Historische Abgrenzung:** Die Phasenmodellzeilen **C** — WP-020 „abgeschlossen (dieser Stand, uncommitted)" und WP-021 „vorbereitet (dieser Stand, uncommitted)" — sind gemäß **Human-Maintainer A0, 2026-10-16** **historische Phase-C-Momentaufnahmen**, keine aktiven Falschaussagen; sie beschreiben einen anderen Zeitpunkt als die Kopffelder und bleiben im Wortlaut **unverändert**. Die Präzedenz des **vierundzwanzigsten** Vorgangs (Live-Phasenmodelltabelle des laufenden CBP-WP-022) wird auf diese Zeilen **nicht** übertragen; der vierundzwanzigste Vorgang bleibt unverändert. Ebenso bleiben phasengebundene Vor-Commit-Berichte derselben Dateien — darunter die Abschnitte *Human Gates* — **unverändert** |
| Abgrenzung zum achtundzwanzigsten Vorgang | Der **achtundzwanzigste** Vorgang betraf den Queue-Detailblock CBP-WP-021, bleibt unverändert und wird **nicht wiedereröffnet**. **Kein neues Work Package, keine neue Phase** |
| Erstmalige Registrierung | In den bisherigen **neununddreißig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | WP-020: Commitfolge um **C `committed` `d6a1a3c`** ergänzt · WP-021: *Aktuelle Phase* auf **(abgeschlossen)**, Commitfolge um **C `committed` `0344774`** ergänzt; die Statuswerte **`complete`** bleiben erhalten, die historischen Phasenmodellzeilen **C** beider Dateien bleiben **unverändert** |
| Einmalzählung | **eine** Fehlerursache · **eine** gemeinsame Reconciliation — **genau ein** Vorgang trotz drei Fundstellen in zwei Dateien |
| Zählwirkung | Zähler **39 → 40**, Nenner **22 unverändert** (**`39/22 → 40/22`**) |

Damit waren **vierzig Konsistenzvorgänge in zweiundzwanzig Work Packages**
dokumentiert (*Stand nach dem vierzigsten Vorgang: `40/22`; durch den
einundvierzigsten Vorgang unten auf **41/23** aktualisiert*; löste die vorige
Angabe „einunddreißig" ab). Die Zahl der Work Packages bleibt **zweiundzwanzig**: Die
Vorgänge 32 bis 38 betreffen das seit dem neunzehnten Vorgang erfasste
CBP-WP-022, Vorgang 39 das seit dem sechzehnten Vorgang erfasste CBP-WP-019 und
Vorgang 40 die seit dem siebzehnten beziehungsweise achtzehnten Vorgang
erfassten CBP-WP-020 und CBP-WP-021; sie erhöhen **ausschließlich** den
Vorgangszähler. Vollständige Progression seit dem neunzehnten Vorgang:
**19/22 → 20/22 → 21/22 → 22/22 → 23/22 → 24/22 → 25/22 → 26/22 → 27/22 → 28/22
→ 29/22 → 30/22 → 31/22 → 32/22 → 33/22 → 34/22 → 35/22 → 36/22 → 37/22 → 38/22
→ 39/22 → 40/22**. **`40/22` ist kein Erfüllungsgrad und keine
Prozentkennzahl**; **`40/23`** ist unzulässig, ebenso **`41/22`** ohne einen
zusätzlich registrierten Vorgang.

**R-33 bleibt `gemindert, nicht geschlossen`**, Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**; **das
projektweite Konsistenzrisiko ist nicht beseitigt** — neun weitere Vorgänge
derselben Grundklasse, gefunden erst durch eine Pre-Closure-Diagnose und einen
vollständigen Audit, belegen es unmittelbar. **Die Registrierung bedeutet
nicht, dass sämtliche aktiven Spiegel konsistent sind:** der gesondert erfasste
Altdrift-Prüfbestand **D-1 bis D-10** ist **nicht klassifiziert und nicht
bereinigt**, und **AF-6** bleibt **zurückgestellt**. Dieselben Vorgänge sind in
[COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und **zählen je nur
einmal**. Die dortige Darstellung folgt der **Prosaform** jenes Dokuments,
während hier die **Tabellenform** des Risk Registers verwendet wird; **Fakten,
Zahlen, Closure-Grenze und R-33-Wirkung sind identisch**.

---

**R-33-Chronologie — einundvierzigster Konsistenzvorgang (CBP-WP-023 Residual WP-023 Registration Lifecycle Statement Staleness, 2026-10-19):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-023** — **erstes** R-33-Erfassen; **der Nenner steigt von 22 auf 23**; registriert im Rahmen der dokumentarischen Closure von CBP-WP-022 (Phase C) |
| Phase und Anlass | Befund **E-1** des Pre-Closure Readiness Audit von CBP-WP-022, klassifiziert im E-1/R-33 Classification Audit (beide 2026-10-19); registriert gemäß **Human-Maintainer-A0 vom 2026-10-19** (Klassifikation **K-3**) |
| Fehlerklasse | **Residual WP-023 Registration Lifecycle Statement Staleness** — eine Lebenszyklusaussage wurde bei der Registrierung von CBP-WP-023 **nicht zeitlich abgegrenzt** (Grundklasse der Vorgänge **30** und **36**) |
| Auslöser | Registrierung von **CBP-WP-023** durch **D-069 Teil P** (A0, 2026-10-17) |
| Betroffenes aktives Repository-Artefakt | **`work-packages/CBP-WP-022.md`** — Schlusszeile des fortlaufend gepflegten Abschnitts *Aussageschutz* |
| Falsche aktive Aussage | „CBP-WP-023 ist nicht registriert und nicht autorisiert." |
| Korrekter Zustand | CBP-WP-023 ist seit **D-069 Teil P** (2026-10-17) registriert und seit **2026-10-19** `committed` und `complete` |
| Herkunft des Fehlers | Historischer Ursprung **`e4caa14`** (B0 von CBP-WP-022, 2026-08-03; damals zutreffend) · kanonische Zustandsänderung **`ca63b0a`** (Registrierung von CBP-WP-023 im Repository, ohne Änderung von `CBP-WP-022.md`) · abschließender WP-023-Commit **`1dad9a8`** |
| Aktiv, nicht historisch | Der Abschnitt *Aussageschutz* wurde in jeder Phase fortgeschrieben und in R4 als **aktiv** eingestuft (Befund **Z-4** des zweiunddreißigsten Vorgangs); die Schlusszeile stand **ohne** zeitliche Rahmung. Die Abschnitte *Stand nach …*, die B0-*Non-Goals* und die Entscheidungstexte (D-068 Teil H) bleiben **historisch** und unverändert |
| Abgrenzung | Der **zweiunddreißigste** Vorgang wird **nicht** rückwirkend erweitert — andere Fehlerursache, und die Aussage war am 2026-10-15/16 zutreffend; die Vorgänge **30** und **36** bleiben unverändert. Die frühere WP-023-Feststellung „kein Vorgang 41" beschreibt den **damaligen Abschlussstand** und ist **kein** fortgeltendes Zählverbot |
| Erstmalige Registrierung | In den bisherigen **vierzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | Die Schlusszeile ist **datiert qualifiziert**: „Zum Zeitpunkt von B0 (2026-08-03) war CBP-WP-023 nicht registriert und nicht autorisiert; seit D-069 Teil P (2026-10-17) ist CBP-WP-023 registriert und seit 2026-10-19 `committed` und `complete`." — die historische Aussage bleibt erhalten |
| Einmalzählung | **eine** Aussage · **eine** Fehlerursache — **genau ein** Vorgang; die Doppelabbildung in Risk Register und Compliance Check **zählt nur einmal** |
| Zählwirkung | Zähler **40 → 41**, Nenner **22 → 23** (**`40/22 → 41/23`**) |
| Aussagegrenze | **Keine neue Risiko-ID**, keine Schwere- oder Statusänderung, **keine neue Decision**, **keine ADR**; **D-068** und **D-069** unverändert; **KB-04 bleibt `DOCUMENTED ONLY`**; beide Gates bleiben `NOT EVALUATED` |

Damit waren **einundvierzig Konsistenzvorgänge in dreiundzwanzig Work Packages**
dokumentiert (*Stand nach dem einundvierzigsten Vorgang: `41/23`; durch den
zweiundvierzigsten Vorgang unten auf **42/24** aktualisiert*; löste die vorige
Angabe „vierzig" ab). Die Zahl der Work Packages steigt auf **dreiundzwanzig**, weil der
einundvierzigste Vorgang **erstmals CBP-WP-023** erfasst. Vollständige
Progression seit dem neunzehnten Vorgang: **19/22 → 20/22 → 21/22 → 22/22 → 23/22 → 24/22 → 25/22 → 26/22 → 27/22 → 28/22 → 29/22 → 30/22 → 31/22 → 32/22 → 33/22 → 34/22 → 35/22 → 36/22 → 37/22 → 38/22 → 39/22 → 40/22 → 41/23**.
**`41/23` ist kein Erfüllungsgrad und keine Prozentkennzahl**; **`41/24`** ist
unzulässig, ebenso **`42/23`** ohne einen zusätzlich registrierten Vorgang.
**R-33 bleibt `gemindert, nicht geschlossen`**, Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**. Derselbe Vorgang
ist in [COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und **zählt nur
einmal**; Fakten, Zahlen und R-33-Wirkung sind identisch.

---

**R-33-Chronologie — zweiundvierzigster Konsistenzvorgang (CBP-WP-024 Active A0 Counter Mirror Staleness, 2026-10-22):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-024** — **erstes** R-33-Erfassen; **der Nenner steigt von 23 auf 24**; registriert in **Phase B0-R2** |
| Kennung | **`B0-R1-F01`** |
| Phase und Anlass | Befund der unabhängigen Nova-Prüfung des B0-Reviewarchivs (Reviewentscheidung **REWORK**); korrigiert in **B0-R1**; klassifiziert durch **Human-Maintainer-A0 vom 2026-10-22 (HD-8, Klassifikation **Z-1**)** |
| Fehlerklasse | **Active A0 Counter Mirror Staleness** (`B0-R1-F01`) — unvollständige Aktualisierung **getrennter Kennzahlentabellenzeilen** (Decisions und A0-Decisions) |
| Auslöser | Registrierung von **D-070** (`accepted`, A0) in CBP-WP-024 Phase B0 |
| Betroffenes aktives Repository-Artefakt | **`project-system/HEALTH_SCORE.md`** — Tabelle *Kennzahlen*, Zeile *davon A0* |
| Falsche aktive Aussage | `\| davon A0 \| 8 \| **65** \|` neben der bereits auf **70** fortgeschriebenen Zeile *Getroffene Entscheidungen* |
| Korrekter Zustand | **66** A0-Decisions nach Registrierung von D-070 — **70** Decisions, davon **66** mit A0 |
| Herkunft des Fehlers | Am Ausgangscommit **`61e2f3a`** war **65** korrekt (69/65). Das B0-Fragment schrieb die Zeile *Getroffene Entscheidungen* auf **70** fort, nicht aber die unmittelbar benachbarte Zeile *davon A0*; die B0-Prüfung arbeitete mit einer Liste bekannter Formulierungen und erfasste die Tabellenform nicht. Der Fehler bestand **ausschließlich im uncommitteten B0-Review-Diff** |
| Aktiv, nicht historisch | Die Tabelle *Kennzahlen* ist ein **aktiver** Kennzahlenspiegel; die Nachbarzeile war in derselben Phase bereits fortgeschrieben |
| Abgrenzung | **Kein Bestandteil von Vorgang 39** und **keine zählneutrale Erweiterung** eines früheren Vorgangs — auch nicht von Vorgang **33** (gleiche Fehlerart, aber andere Ursache, anderer Zeitpunkt, anderes Work Package). Der Driftkandidat **DK-3** (`SECURITY_FOUNDATION_READINESS_GATE.md`, DRC-Gatestatus) bleibt **getrennt**, ohne Zählwirkung; Vorgang 39 wird **nicht** umklassifiziert. Dasselbe gilt für die übrigen Driftkandidaten aus B0 |
| Präzedenz | Gezählt werden auch im Nova-REWORK gefundene und vor dem Commit korrigierte Fehler: **CBP-WP-012** („Nova-REWORK-Korrekturlauf"), ebenso Korrekturen „im selben Lauf" (**CBP-WP-003**, **CBP-WP-006**) — Historie der Zählfehler in [COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) |
| Erstmalige Registrierung | In den bisherigen **einundvierzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | **B0-R1**: `\| davon A0 \| 8 \| **65** \|` → `\| davon A0 \| 8 \| **66** \|` (genau ein Byte); anschließend repositoryweiter wertbasierter Scan aller A0- und Decision-Zähler ohne weiteren Befund |
| Einmalzählung | **eine** Zeile · **eine** Fehlerursache — **genau ein** Vorgang; die Doppelabbildung in Risk Register und Compliance Check **zählt nur einmal** |
| Zählwirkung | Zähler **41 → 42**, Nenner **23 → 24** (**`41/23 → 42/24`**) — CBP-WP-024 wird **erstmals** erfasst |
| Aussagegrenze | **Keine neue Risiko-ID**, keine Schwere- oder Statusänderung, **keine neue Decision-ID** (HD-8 ist eine Klassifikationsentscheidung), **keine ADR**; **D-070** unverändert; **KB-04 bleibt `DOCUMENTED ONLY`**; beide Gates bleiben `NOT EVALUATED` |

Damit waren **zweiundvierzig Konsistenzvorgänge in vierundzwanzig Work Packages**
dokumentiert (*Stand nach dem zweiundvierzigsten Vorgang: `42/24`; durch den
dreiundvierzigsten Vorgang unten auf **43/25** aktualisiert*; löste die vorige
Angabe „einundvierzig" ab). Die Zahl der Work Packages steigt auf **vierundzwanzig**,
weil der zweiundvierzigste Vorgang **erstmals CBP-WP-024** erfasst. Vollständige
Progression seit dem neunzehnten Vorgang: **19/22 → 20/22 → 21/22 → 22/22 → 23/22 → 24/22 → 25/22 → 26/22 → 27/22 → 28/22 → 29/22 → 30/22 → 31/22 → 32/22 → 33/22 → 34/22 → 35/22 → 36/22 → 37/22 → 38/22 → 39/22 → 40/22 → 41/23 → 42/24**.
**`42/24` ist kein Erfüllungsgrad und keine Prozentkennzahl**; **`42/25`** ist
unzulässig, ebenso **`43/24`** ohne einen zusätzlich registrierten Vorgang.
**R-33 bleibt `gemindert, nicht geschlossen`**, Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**. Derselbe Vorgang
ist in [COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und **zählt nur
einmal**; Fakten, Zahlen und R-33-Wirkung sind identisch.

---

**R-33-Chronologie — dreiundvierzigster Konsistenzvorgang (CBP-WP-025 Active X1 Commit-status Mirrors Staleness, 2026-10-26):**

| Feld | Inhalt |
| --- | --- |
| Work Package | **CBP-WP-025** — **erstes** R-33-Erfassen; **der Nenner steigt von 24 auf 25**; registriert in **Phase X1-C3** |
| Kennung | **`X1-PCR-F01`** · `R33_EVENT_43_WP025_X1_POST_COMMIT_MIRROR_STALENESS` |
| Phase und Anlass | Post-Commit-Prüfung nach Human-Commit und Human-Push von Phase X1; klassifiziert und zur Korrektur freigegeben durch **Human-Maintainer-A0 vom 2026-10-26** („GO CBP-WP-025 X1-C3 – POST-COMMIT STATUS RECONCILIATION") |
| Fehlerklasse | **Git-/Register-Statusabweichung nach Commit und Push** — **CBP-WP-025 Active X1 Commit-status Mirrors Staleness** |
| Auslöser | Human-Commit und Human-Push von Phase X1: **`97cc85fe1531f49a5ad407ee30a1102a7d8bd446`** (Parent `b3100ef`, 2026-10-26) |
| Betroffene aktive Repository-Artefakte | `work-packages/CBP-WP-025.md` · `project-system/WORK_PACKAGE_QUEUE.md` · `project-brain/PROJECT_BRAIN.md` · `project-system/PROJECT_MANIFEST.md` · `project-system/HEALTH_SCORE.md` · `README.md` · `CLAUDE.md` · `docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md` |
| Falsche aktive Aussage | „Phase X1 `in-review` / **nicht committed**" |
| Korrekter Zustand | „Phase X1 **`committed`** (`97cc85f`)"; **CBP-WP-025 insgesamt weiterhin `in-review`**; X2 bis X6 und X4b nicht autorisiert |
| Abgrenzung zu historischen Aussagen | D-071 Teil O (`42/24`), die X1-Abnahmekriterien (datiert qualifiziert), der Satz „Zähler im X1-Review-Diff" in der Queue und die Registrierungsnotiz „uncommitteter X1-Review-Diff" im Decision Register beschreiben den **Stand vor dem Commit** und bleiben unverändert |
| Ursache | Ein Commit kann seinen eigenen Hash nicht vorwegnehmen; die X1-Statusspiegel beschrieben korrekt den Vor-Commit-Stand und wurden nach Commit und Push nicht unmittelbar nachgeführt |
| Abgrenzung zu früheren Vorgängen | **Keine zählneutrale Erweiterung** eines früheren Vorgangs — auch nicht von **30**, **36**, **40**, **41** oder **42** (andere Ursache, anderer Zeitpunkt, anderes Work Package). Die Post-Commit-Reconciliation von CBP-WP-024 B0 (B0-C6) wurde nach dortiger Human-Maintainer-A0 (R-1 Option N) **nicht** gezählt; dieser Befund ist durch eigene A0 ausdrücklich als Vorgang angenommen. **N-1a**, **N-1b**, **DK-3**, **AF-6** und **D-1 bis D-10** bleiben getrennt und ohne Zählwirkung |
| Erstmalige Registrierung | In den bisherigen **zweiundvierzig** Vorgängen **nicht** als eigener Vorgang registriert |
| Korrektur | **X1-C3**: aktive Statusfelder in den acht Dateien minimal nachgeführt („X1 `committed` `97cc85f`", Gesamt-Work-Package `in-review`); historische Aussagen erhalten oder datiert qualifiziert; keine globale Ersetzung |
| Einmalzählung | **acht** Spiegel · **eine** Fehlerursache · **eine** Zustandsänderung — **genau ein** Vorgang; die Doppelabbildung in Risk Register und Compliance Check **zählt nur einmal** |
| Zählwirkung | Zähler **42 → 43**, Nenner **24 → 25** (**`42/24 → 43/25`**) — CBP-WP-025 wird **erstmals** erfasst |
| Aussagegrenze | **Keine neue Risiko-ID**, keine Schwere- oder Statusänderung, **keine neue Decision**, **keine ADR**; **D-071**, **D-069** und **ADR-0015** unverändert; **KB-04 bleibt `DOCUMENTED ONLY`**; beide Gates bleiben `NOT EVALUATED`; **keine technische, operative oder Publikationswirkung**; kein Transfer |

Damit sind **dreiundvierzig Konsistenzvorgänge in fünfundzwanzig Work Packages**
dokumentiert (**neue aktuelle Basislinie**; löst die vorige Angabe
„zweiundvierzig" ab). Die Zahl der Work Packages steigt auf **fünfundzwanzig**,
weil der dreiundvierzigste Vorgang **erstmals CBP-WP-025** erfasst. Vollständige
Progression seit dem neunzehnten Vorgang: **19/22 → 20/22 → 21/22 → 22/22 → 23/22 → 24/22 → 25/22 → 26/22 → 27/22 → 28/22 → 29/22 → 30/22 → 31/22 → 32/22 → 33/22 → 34/22 → 35/22 → 36/22 → 37/22 → 38/22 → 39/22 → 40/22 → 41/23 → 42/24 → 43/25**.
**`43/25` ist kein Erfüllungsgrad und keine Prozentkennzahl**; **`43/26`** ist
unzulässig, ebenso **`44/25`** ohne einen zusätzlich registrierten Vorgang.
**R-33 bleibt `gemindert, nicht geschlossen`**, Kritikalität unverändert
**mittel**, kein Risiko geschlossen, **keine neue Risiko-ID**. Derselbe Vorgang
ist in [COMPLIANCE_CHECK.md](COMPLIANCE_CHECK.md) gespiegelt und **zählt nur
einmal**; Fakten, Zahlen und R-33-Wirkung sind identisch.

---

**Verändert in CBP-WP-012:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| **R-26** | Root-/Hostbetrieb: Der Skeleton **prüft** auf POSIX-root (`check_not_privileged`) und blockiert; auf Windows `NOT APPLICABLE`. **Kein Deploymentnachweis** — die Prüfung existiert lokal, die Durchsetzung auf der Ziel-VM fehlt. Status unverändert `offen` | CBP-WP-012 |
| **R-33** | Testzahl (67 im Erstlauf, **69** nach Netzwerk-Guard) und Commitzahl aus dem tatsächlichen Lauf bzw. Git ausgezählt; zwei Testdefekte vor dem grünen Lauf gefunden. **Dokumentregel, keine Kontrolle** | CBP-WP-012 |

**Kein Risiko wurde in CBP-WP-012 geschlossen oder gemindert.** Ein Skeleton
mit fail-closed Policies ist **keine durchgesetzte Kontrolle**: `check_*`-
Funktionen prüfen eine lokale Konfiguration, sie erzwingen keine OS-Rechte,
keine Mount-Grenzen und keinen Netzwerkfilter. R-25, R-26, R-27, R-30, R-31,
R-32 und R-20 bleiben **offen** und schließen erst durch bestandene
Negativtests auf der Ziel-VM (Nachweisstufe 4 bzw. 5).

**Neu in CBP-WP-010:** keine.

**Verändert in CBP-WP-010:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| **R-03** | Datenklassenvergabe **präzisiert**: `data_class: unknown` ist Vorgabe und wird fail-closed wie `excluded-from-ai` behandelt; Aktivierung blockiert (V9). **Vergabeverfahren bleibt offen** (OD-08) — Status unverändert `offen` | D-031…D-033, ADR-0008 |
| **R-27** | Zugriffsregeln für PS-03 **konkretisiert**: kein automatischer Commit, kein Push, kein pauschaler GitHub-Schreibzugriff, Standardzugriff `read_only`. **Technisch weiterhin nicht durchgesetzt** — Status unverändter `offen` | Slot-Regeln PS-03 |
| **R-32** | Mappingebene der Quarantäne **spezifiziert** (Zustandsmodell, Freigabekette). Die Quarantäne selbst existiert **nicht** — Status unverändert `offen` | Mapping-Spezifikation |

**Kein Risiko wurde in CBP-WP-010 geschlossen oder gemindert.** Sämtliche
Regeln der Mappingkonvention sind **dokumentarisch**: Es existiert kein
Validator, kein Parser, kein Mapping und keine angebundene Quelle. Nach
[PHASE_1_EVIDENCE_PLAN.md](../docs/roadmap/PHASE_1_EVIDENCE_PLAN.md) stehen
alle Nachweise auf **Stufe 1 `dokumentiert`** — und Stufe 1 schließt
definitionsgemäß kein Risiko.

**Neu in CBP-WP-009:** keine.

**Verändert in CBP-WP-009:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| **R-01** | Wirkung von W-3 **präzisiert**: mindert ausschließlich den Pfad private Information → versehentlich in Core → Core-Push → unbeabsichtigte Veröffentlichung. **Bleibt `offen`** | D-030, ADR-0007 · Nova-REWORK |
| **R-17** | NDF-Abweichungen: Zielstruktur nun entschieden, **AB-03…AB-08 bleiben offen** (OD-29). Status unverändert `gemindert` | D-029, ADR-0007 |
| **R-20** | Umfang **erweitert**: nicht nur Systemsicherung, sondern auch **kanonische Registry-Metadaten** im Operator-Workspace und **RT-2 Operational Evidence** — beide nicht rekonstruierbar. Bleibt `offen` | ADR-0007, G5, RG-4 · Nova-REWORK |

**Kein Risiko wurde in CBP-WP-009 geschlossen.** Eine Strukturentscheidung ist
kein technischer Nachweis.

> **Korrektur im Nova-REWORK-Lauf.** Die Erstausführung hatte R-01 als
> „strukturell gemindert" beschrieben, ohne den Wirkungsbereich zu begrenzen.
> Das war zu weit gefasst: W-3 verhindert einen **Veröffentlichungspfad**, kein
> Secret. Erkennung, Rotation, Ablage, Scanning und Zugriffskontrolle fehlen
> unverändert. R-20 war zudem zu eng beschrieben — **zwei** nicht
> rekonstruierbare Bestände sind betroffen, nicht einer.

**Neu in CBP-WP-008:** keine.

**Verändert in CBP-WP-008:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| R-33 | Vierter Zählfehler dokumentiert — **nach** Einführung der Regel entstanden | Auszählung des DECISION_REGISTER |

**Kein Risiko wurde in CBP-WP-008 geschlossen oder gemindert.** Das Work
Package erzeugt ausschließlich Planungsdokumente. Nach
[PHASE_1_EVIDENCE_PLAN.md](../docs/roadmap/PHASE_1_EVIDENCE_PLAN.md) stehen
damit **alle Nachweise auf Stufe 1 `dokumentiert`** — und Stufe 1 schließt
definitionsgemäß kein Risiko.

**Geplante Schließungswege** (keiner beschritten):

| Risiko | Schließt durch | Erforderliche Stufe |
| --- | --- | --- |
| R-25, R-27, R-26 | CBP-WP-012 | **4** — negativ getestet |
| R-32, R-31, R-30 | CBP-WP-013 | **4** — negativ getestet |
| R-10 | CBP-WP-014 | **4** |
| R-07 | CBP-WP-014 | **5** — Rebuild durchgeführt |
| R-20 | P9 | **5** — Restore durchgeführt |
| R-21 | P7 | **3** — gemessen |

**Neu in CBP-WP-005:** keine.

**Verändert in CBP-WP-005:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| **R-21** | Benchmark entworfen → `gemindert, nicht geschlossen` | Dataset 1.0.0, 36 Fragen, Metrikrubrik, Regressionsregeln |
| **R-31** | Zwei `excluded-from-ai`-Fixtures und 6 Datenschutzfragen angelegt → `gemindert` | Benchmark-Korpus, Leakage als kritischer Fehler mit Zielwert 0 |
| R-33 | Kennzahlen erneut skriptgestützt ausgezählt | Prüfungen in CBP-WP-005 |

> **R-21 ist ausdrücklich nicht geschlossen.** Ein entworfener Benchmark misst
> nichts. Ohne durchgeführten Lauf bleibt jede Qualitätsaussage unbelegt.
>
> **R-31 ist gemindert, nicht geschlossen.** Die Fixtures existieren, die
> Prüfung der Sperrwirkung steht aus.

**Verändert in CBP-WP-004:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| R-01 | Schadensverfahren definiert → `teilweise gemindert` | SECRET_INCIDENT_RESPONSE |
| R-06 | Einbahnregel und einziger Schreibpfad festgeschrieben → `gemindert` | ADR-0003, COMPONENT_MODEL |
| R-07 | Rebuild-Vertrag definiert → `gemindert` | ADR-0003, SYSTEM_ARCHITECTURE |
| R-19 | Deployment-Neutralität als ADR → `gemindert` | ADR-0001, DEPLOYMENT_PROFILES |
| R-25 | Berechtigungsmodell dokumentiert; **technisch weiterhin nicht durchgesetzt** | ADR-0004, PERMISSION_MODEL |
| R-27 | Zugriffsregeln gesetzt; **technisch weiterhin nicht durchgesetzt** | PERMISSION_MODEL |
| R-34 | DRC eingeführt → `gemindert` | ADR-0005, DEPLOYMENT_READINESS_CHECK |

**Kein Risiko wurde geschlossen, weil ein Dokument entstanden ist.** R-25 und
R-27 bleiben ausdrücklich **offen**: ein Berechtigungsmodell auf Papier ist
keine Zugriffskontrolle. R-01 bleibt `teilweise gemindert`, weil Erkennung und
technische Unterstützung fehlen. Der Nachweis der Wirksamkeit gehört in spätere
Gates.

## Weiterhin kritisch

| ID | Warum |
| --- | --- |
| R-25 | Berechtigungen ohne technische Durchsetzung; Zuordnung nicht erhoben |
| R-27 | Erlaubte Repository- und GitHub-Zugriffe unbekannt |
| R-31 | Sperrwirkung von `excluded-from-ai` ungeprüft |
| R-32 | Quarantäne für Nicht-Markdown-Quellen existiert nicht |
| R-34 | 16 vertagte Deployment-Kriterien ohne zuständiges Gate |
| R-21 | Kein Benchmark, damit keine Qualitätsaussage möglich |

## Pflege

Ein Risiko wird nicht gelöscht, sondern auf `geschlossen` gesetzt und mit der
wirksamen Kontrolle verknüpft.
