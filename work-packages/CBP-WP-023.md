# CBP-WP-023 — Repository Visibility Governance Reconciliation

| Feld | Wert |
| --- | --- |
| Titel | **Repository Visibility Governance Reconciliation** |
| Typ | **Documentation / Governance** |
| Priorität | **P0** |
| Prompt Mode | **Full** · Context Budget **B2 – Standard** (Maximum **B3**) |
| Status | **`active`** |
| Aktuelle Phase | **G3 – Maintainer Commit and Post-Commit Reconciliation** (Commit-Vorbereitung autorisiert durch Human-Maintainer-A0 vom 2026-10-17) |
| Registration Decision | **D-069**, Teil **P** (konsolidiert, A–P) — `accepted`, **A0**, 2026-10-17 — Ergebnis **`REPOSITORY_VISIBILITY_PUBLIC_CONFIRMED_PUBLICATION_NOT_AUTHORIZED`** |
| Human-Maintainer-Authority | **A0**, 2026-10-17 — **A0-1** (Sichtbarkeit), **WB-1 Option A** (eigenständiges Work Package), G1-Scopefreigabe mit **18-Dateien-Allowlist** · **G2-A0** vom 2026-10-17 (**A0-G2-1** bis **A0-G2-7**: Annahme des G1-Reviews, Annahme von ADR-0015, partielle Ablösung, Zählerziel, Work-Package-Status, Scope- und Git-Grenze) |
| ADR-Gate | **`ADR_REQUIRED`** |
| ADR | **ADR-0015** — *Repository-Sichtbarkeit, Entwicklungsstatus und Publikationsstatus* — **`accepted`**, **A1** (in G1 `proposed`; in G2 durch Human-Maintainer-A0 vom 2026-10-17 angenommen); ADR-0006 und ADR-0007 **partiell abgelöst**, im Übrigen `accepted` |
| Registrierungsdatum | **2026-10-17** |
| Parallele Work Packages | **CBP-WP-022** bleibt **`in-review`** (Closure-Grenze **D-068** unverändert) · zuletzt abgeschlossen bleibt **CBP-WP-021** |
| Commit | Commit und Push ausschließlich durch den Human Maintainer nach separatem GO (Phase G3); die Commit-Referenz wird erst nach dem Commit nachgeführt |
| KB-04-Status | **`DOCUMENTED ONLY`** — unverändert |
| Capabilities | **0 von 29** — unverändert |
| Gates | Mapping Activation `NOT EVALUATED` · Security Foundation Readiness `NOT EVALUATED` |

## Anlass

GitHub weist das Core-Repository als **öffentlich sichtbar** aus. Bisherige
Governance-Dokumente — darunter der Klarstellungsnachtrag von ADR-0006
(Verbindliche Folgerung 2), ADR-0007 und mehrere aktive Statusspiegel — führten
das Repository als **privat**; **OD-11** war offen. Wann die Sichtbarkeit
tatsächlich gewechselt hat, ist **nicht belegt**.

Der Human Maintainer hat am **2026-10-17** entschieden, das Repository als
öffentlich sichtbares Entwicklungsrepository zu führen (**A0-1**), und dieses
Work Package als **eigenständige Governance-Einheit** registriert (**WB-1,
Option A**). Ein vorheriger G1-Lauf endete mit `WORK_PACKAGE_BINDING_REQUIRED`,
ein weiterer mit `ALLOWLIST_INSUFFICIENT` — beide **vor** jeder Dateiänderung.

## Phasenmodell

Die Phasen sind **Governance-Schritte innerhalb desselben Work Packages**. Aus
G1 folgt **keine** Ausführungsfreigabe für G2 oder G3.

| Phase | Inhalt | Status |
| --- | --- | --- |
| **G1 — Governance Candidate Preparation** | Registrierung von CBP-WP-023 · Registrierung von **D-069** · **ADR-0015 `proposed`** · OD-11-Reconciliation · aktive Sichtbarkeitsspiegel · R-16-/R-01-Dokumentation · statische Prüfung · Nova-Review | **reviewt** — Nova-Review `GO WITH NOTES`, vom Human Maintainer angenommen (A0-G2-1) |
| **G2 — Human-Maintainer ADR Acceptance** | **ADR-0015 `accepted`** · definitive A1-Teilablösungsvermerke in ADR-0006 und ADR-0007 · abschließender Review | **abgeschlossen und reviewt** — autorisiert durch Human-Maintainer-A0 vom 2026-10-17; Nova-Review `GO WITH NOTES`, vom Human Maintainer angenommen (G3-A1) |
| **G3 — Maintainer Commit and Post-Commit Reconciliation** | Commit und Push **ausschließlich durch den Human Maintainer** · Post-Commit Truth Check | **Commit-Vorbereitung autorisiert** durch Human-Maintainer-A0 vom 2026-10-17 (G3-A1 bis G3-A5) — Commit und Push ausschließlich durch den Human Maintainer nach **separatem** GO |

## Autorisierter G1-Scope

1. Registrierung von CBP-WP-023.
2. Registrierung der bereits gefassten A0-Decision **D-069** im uncommitteten
   Review-Diff.
3. Erstellung von **ADR-0015 ausschließlich als `proposed`**.
4. Vorbereitung der **OD-11**-Reconciliation.
5. Notwendige Aktualisierung aktiver Sichtbarkeitsspiegel — einschließlich der
   ausdrücklich zusätzlich autorisierten Zeile 114 in `PROJECT_PROFILE.md`.
6. Dokumentarische **R-16**-Reconciliation (zählneutral).
7. Neubewertung von **R-01** ohne Schwere- oder Statusänderung.
8. Eng begrenzte Sperrlisten-Klarstellung.
9. Minimal notwendige Aktualisierung der Capability Matrix.
10. Validierung des vollständigen G1-Diffs.

**Allowlist (höchstens 18 Dateien):** ADR-0015 (neu), ADR-0006, ADR-0007,
`docs/decisions/README.md`, `DECISION_REGISTER.md`, `DO_NOT_START.md`,
`CAPABILITY_MATRIX.md`, `RISK_REGISTER.md`, `COMPLIANCE_CHECK.md`,
`PROJECT_MANIFEST.md`, `PROJECT_BRAIN.md`, `README.md`, `CLAUDE.md`,
`HEALTH_SCORE.md`, `WORK_PACKAGE_QUEUE.md`, dieses Work Package (neu),
`PHASE_1_WORK_PACKAGE_MAP.md` und `PROJECT_PROFILE.md` (nur Zeile 114).

## Abhängigkeiten

- **A0-1** des Human Maintainers vom 2026-10-17
- read-only Confidentiality Intake vom 2026-10-17 (keine kritischen Befunde;
  CF-01 und CF-02 als niedrige Hinweise akzeptiert)
- **WB-1, Option A**
- **D-068** als bestehende Closure-Grenze von CBP-WP-022 — **unverändert**
- bestehende CBP-/NDF-Governance (NDF v1.0.0, D-003)

## Non-Goals und Non-Claims

CBP-WP-023 autorisiert **nicht**:

| Ausgeschlossen |
| --- |
| GitHub-Transfer · Umbenennung · Remote-Wechsel (separat **A0-2**) |
| Lizenzwahl (OD-23 bleibt offen) |
| Branding · Logos · Wortmarken · Marketingtexte · Social Previews · README-Neugestaltung |
| Produktrelease oder Produktveröffentlichung |
| operative Security-Evidenz · Gate-Hochstufung · Control-Uplift |
| Closure von CBP-WP-022 · Ersatz der Closure-Grenze **D-068** |
| technische Implementierung · Änderungen an Code, Tests, Deployments oder Konfiguration |
| Annahme von ADR-0015 in G1 · eine **D-070** · einen weiteren ADR |
| einen R-33-Vorgang 41 · eine neue Risiko-ID · Bereinigung von D-1 bis D-10 |
| Commit, Push, Tag oder Release durch einen Implementation Agent |

## D-069 — Entscheidungsblock

| Feld | Wert |
| --- | --- |
| ID | **D-069** |
| Titel | **CONFIRM CORE REPOSITORY PUBLIC VISIBILITY AND SEPARATE IT FROM PUBLICATION STATE** |
| Status | `accepted` |
| Autorität | **A0** — Human Maintainer |
| Datum | **2026-10-17** |
| Work Package | **CBP-WP-023** |
| Ergebnis | **`REPOSITORY_VISIBILITY_PUBLIC_CONFIRMED_PUBLICATION_NOT_AUTHORIZED`** |
| ADR-Gate | **`ADR_REQUIRED`** — **ADR-0015** `proposed` |

| Teil | Inhalt |
| --- | --- |
| **A — Gegenstand** | Kanonische Festlegung der Sichtbarkeit des Core-Repositorys. |
| **B — Kontext** | GitHub weist das Repository als **öffentlich** aus, während bisherige Governance-Dokumente — darunter ADR-0006 (Klarstellungsnachtrag, Folgerung 2) und ADR-0007 — sowie aktive Statusspiegel private Sichtbarkeit behaupteten; OD-11 war offen. **Der Zeitpunkt des ursprünglichen Sichtbarkeitswechsels ist nicht belegt.** |
| **C — Authority** | Human-Maintainer-A0 vom **2026-10-17**. Die Entscheidung bestätigt den **künftigen Sollzustand**, **ohne** die frühere Abweichung zwischen Dokumentation und tatsächlicher Sichtbarkeit rückwirkend zu legitimieren. |
| **D — Repository Visibility** | **PUBLIC** |
| **E — Development State** | **PRIVATE DEVELOPMENT** — ein öffentlich sichtbares GitHub-Repository bleibt ein kontrolliertes Entwicklungsprojekt. |
| **F — Product Publication** | **NOT AUTHORIZED** |
| **G — Lizenz** | **UNDECIDED** — OD-23 bleibt offen. |
| **H — Branding** | DO_NOT_START **#11** und **#13** bleiben gesperrt, ebenso **#12** (öffentliche Produktveröffentlichung); **keine neue Markenproduktion**. |
| **I — Sicherheit und Vertraulichkeit** | Der read-only Audit vom 2026-10-17 fand **keine kritischen** Vertraulichkeitsbefunde; **CF-01** und **CF-02** wurden vom Human Maintainer als **niedrige Hinweise akzeptiert**. **Ein negativer Audit ist keine vollständige Sicherheitsgarantie.** Vor künftigen Pushes bleibt eine **Vertraulichkeitsprüfung des Diffs** erforderlich. |
| **J — ADR-Gate** | **`ADR_REQUIRED`.** ADR-0015 ist in G1 **ausschließlich `proposed`**; seine Annahme verlangt ein neues ausdrückliches Human-Maintainer-GO (G2). |
| **K — Architektur** | ADR-0006 und ADR-0007 bleiben im Übrigen gültig. Die **endgültige A1-Teilablösung** ihrer Sichtbarkeitsaussagen ist Gegenstand von **G2**. **D-069 ist als A0 bereits verbindlich für die Repository-Sichtbarkeit.** |
| **L — OD-11** | Inhaltlich **beantwortet**; formale Reconciliation durch D-069 und den nachfolgenden Human-Maintainer-Commit. |
| **M — Offen bleiben** | **OD-23** (Lizenz) und **OD-28** (öffentlicher Produktname). |
| **N — Operative Grenzen** | **0 von 29** Capabilities vollständig implementiert · keine produktive Retrieval-Plattform · keine produktive Quellenanbindung · KB-04 **`DOCUMENTED ONLY`** · Mapping Activation Gate und Security Foundation Readiness Gate **`NOT EVALUATED`**. |
| **O — Transfergrenze** | Ein späterer GitHub-Transfer, eine Umbenennung oder ein Remote-Wechsel verlangt eine **separate A0-Entscheidung (A0-2)**; D-069 autorisiert keinen Transfer. |
| **P — Work-Package-Registrierung** | **CBP-WP-023** — *Repository Visibility Governance Reconciliation* — wird als eigenständiges Governance-Work-Package registriert: Typ **Documentation/Governance**, Priorität **P0**, Status **`active`**. **CBP-WP-022 bleibt `in-review`**, **CBP-WP-021 bleibt zuletzt abgeschlossen**, **G2** und **G3** bleiben freigabepflichtig. **Keine zusätzliche Registrierungs-Decision.** Commit und Push verbleiben **ausschließlich beim Human Maintainer** (D-003). |

Dieser Block ist mit der Zeile **D-069** im
[Decision Register](../project-system/DECISION_REGISTER.md) **inhaltlich
identisch**. Registriert im **uncommitteten G1-Review-Diff**.

## Fünf Dimensionen

| Dimension | Zustand | Grundlage |
| --- | --- | --- |
| Repository Visibility | **PUBLIC** | D-069 (A0) |
| Development State | **PRIVATE DEVELOPMENT** | D-069 (A0) |
| Product Publication | **NOT AUTHORIZED** | D-069, DO_NOT_START #12 |
| License | **UNDECIDED** | OD-23 |
| Public Branding | **gesperrt** | DO_NOT_START #11, #13 |

Die architektonische Verankerung dieser Trennung ist
[ADR-0015](../docs/decisions/ADR-0015-repository-sichtbarkeit-und-publikationsstatus.md)
— **`accepted`** (A1, seit 2026-10-17; in G1 `proposed`).

## Stand G1

*Stand Phase G1 — als G1-Nachweis unverändert erhalten; fortgeschrieben durch
den Abschnitt* Stand G2 *unten.*

Der G1-Diff registriert D-069 und dieses Work Package, legt ADR-0015 als
`proposed` an, versieht ADR-0006 und ADR-0007 mit datierten
Governance-Vermerken (Entscheidungssubstanz unverändert), schließt OD-11 im
Register, ergänzt eine A0-Klarstellung in der Sperrliste, eine Klarstellung in
der Capability Matrix, eine R-01-Neubewertung und eine R-16-Notiz und führt die
aktiven Statusspiegel nach.

**Zähler im Review-Diff:** **69** Entscheidungen, davon **65** mit A0 ·
**14** angenommene ADRs · **1** vorgeschlagener ADR (ADR-0015) · offene
Entscheidungen **22**, davon **4** mit P0 · geschlossene offene Entscheidungen
**13** · Risiken **35** (Schwere **20/14/1**) · R-33 **40/22**.

**R-33-Abgrenzung:** Die Sichtbarkeitsabweichung ist gemäß
Human-Maintainer-Klassifikation ein **R-16**-Governance-Fall und **kein**
weiterer R-33-Vorgang. Die Nachführung der Aussage „CBP-WP-023 nicht
registriert" ist Teil der Registrierung selbst. **Kein Vorgang 41.**

## Stand G2

*Stand Phase G2 — als G2-Nachweis unverändert erhalten; fortgeschrieben durch
Kopf und Phasenmodell (Phase G3).*

**Authority:** Der Human Maintainer hat am **2026-10-17** den G1-Kandidaten nach
Nova-Review mit **`GO WITH NOTES`** angenommen (**A0-G2-1**), **ADR-0015** als
`accepted` mit Autoritätsklasse **A1** angenommen (**A0-G2-2**) und die
**partielle Ablösung** der widersprechenden Sichtbarkeitsaussagen in ADR-0006
und ADR-0007 beschlossen (**A0-G2-3**). Vor jeder G2-Änderung wurde der lokale
G1-Stand byte-genau gegen das freigegebene G1-Reviewpaket geprüft.

**Autorisierter G2-Scope:** ADR-0015 `proposed` → `accepted` (A3 → A1) ·
datierte Teilablösungsvermerke in ADR-0006 und ADR-0007 · ADR-Index ·
notwendige aktive ADR-Statusspiegel · dieser G2-Nachweis. Die Allowlist bleibt
auf dieselben **18 Dateien** beschränkt; **keine neue Datei**.

**Ergebnis im uncommitteten G2-Review-Diff:** ADR-0015 ist **`accepted`**
(A1); ADR-0006 und ADR-0007 bleiben **`accepted`** und sind **ausschließlich**
in ihren Sichtbarkeitsaussagen **partiell abgelöst** — *Superseded by* bleibt
**—**, der historische Wortlaut bleibt erhalten. Die fünf Dimensionen und
**D-069** sind unverändert; die Annahme ist **keine neue Decision** (keine
D-070).

**Zähler im Review-Diff:** **69** Entscheidungen, davon **65** mit A0 ·
**15** angenommene ADRs · **0** vorgeschlagene ADRs · offene Entscheidungen
**22**, davon **4** mit P0 · geschlossene offene Entscheidungen **13** · Risiken
**35** (Schwere **20/14/1**) · R-33 **40/22**.

**R-33-Abgrenzung:** Die Nachführung des ADR-Status von `proposed` auf
`accepted` ist Teil der G2-Annahme selbst und **kein** Konsistenzvorgang.
**Kein Vorgang 41**, keine neue Risiko-ID.

**Offen:** **G3** — Commit, Push und Post-Commit Truth Check ausschließlich
durch den Human Maintainer — ist **nicht autorisiert**. CBP-WP-023 bleibt
**`active`**; ein Abschluss verlangt eine **separate** Entscheidung.

## Aussageschutz

| Behauptung | Zutreffend? |
| --- | --- |
| Öffentliche Sichtbarkeit sei eine Produktveröffentlichung | **nein** — Product Publication bleibt **NOT AUTHORIZED** |
| Öffentliche Sichtbarkeit sei eine Open-Source-Lizenz | **nein** — Lizenz **UNDECIDED**, OD-23 offen |
| Öffentliche Sichtbarkeit sei eine Branding-Freigabe | **nein** — #11 und #13 bleiben gesperrt |
| ADR-0015 sei bereits in G1 angenommen worden | **nein** — in G1 **`proposed`**; angenommen erst in **G2** durch Human-Maintainer-A0 vom 2026-10-17 |
| ADR-0006 oder ADR-0007 seien vollständig abgelöst oder `superseded` | **nein** — seit G2 **ausschließlich** in ihren Sichtbarkeitsaussagen **partiell** abgelöst; beide bleiben `accepted` |
| Die Annahme von ADR-0015 sei eine neue Decision | **nein** — Human-Maintainer-Annahmeentscheidung **ohne** neue Decision-ID; D-069 unverändert |
| D-069 legitimiere die frühere Sichtbarkeitsabweichung rückwirkend | **nein** — sie bestätigt den künftigen Sollzustand |
| Die Registrierung ändere den Status von CBP-WP-022 | **nein** — CBP-WP-022 bleibt `in-review`, D-068 unverändert |
| G1 autorisiere G2, G3, einen Transfer oder einen Commit | **nein** |
| G2 autorisiere G3, einen Commit, einen Push, einen Transfer oder den Abschluss von CBP-WP-023 | **nein** |
| Ein negativer Vertraulichkeitsaudit sei eine Sicherheitsgarantie | **nein** |

**Die Registrierung eines Work Packages ist keine Implementierungsfreigabe.**
