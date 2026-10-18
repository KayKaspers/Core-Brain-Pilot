# ADR-0015 — Repository-Sichtbarkeit, Entwicklungsstatus und Publikationsstatus

*Trennung von Repository-Sichtbarkeit, Entwicklungsstatus und Produktveröffentlichung*

| Feld | Wert |
| --- | --- |
| **Status** | **accepted** |
| Datum | 2026-10-17 |
| Entscheider | **Human Maintainer** |
| Angenommen am | **2026-10-17** — Phase **G2** von CBP-WP-023 |
| **Autorität** | **A1** — angenommen und bindend |
| Annahmegrundlage | **A0** — ausdrückliche Human-Maintainer-Annahmeentscheidung vom 2026-10-17 (**A0-G2-2** Annahme, **A0-G2-3** partielle Ablösung) |
| Vorheriger Status | `proposed` (A3, nicht bindend) — Phase G1 |
| Grundlage der Entscheidungen | **A0** — Human Maintainer, **D-069** (2026-10-17) |
| Erfasst in | **CBP-WP-023** — vorgeschlagen in Phase G1 (Governance Candidate Preparation), angenommen in Phase **G2** (Human-Maintainer ADR Acceptance) |
| Vorgeschaltetes Gate | **D-069**, Teil J — Ergebnis **`ADR_REQUIRED`** |
| Supersedes | — (**keine vollständige Ablösung**; siehe *Teilablösung*) |
| **Teilablösung** | **wirksam seit 2026-10-17** — **ausschließlich** die Sichtbarkeitsaussagen in **ADR-0006** (Klarstellungsnachtrag, Verbindliche Folgerung 2) und **ADR-0007** (siehe Abschnitt *Supersession Boundary*); beide bleiben **`accepted`** |
| Superseded by | — |
| Schließt | **OD-11** inhaltlich durch **D-069** (A0), nicht durch diesen ADR |

> **Dieser ADR ist angenommen und bindend.** Er trägt Autoritätsklasse **A1**.
> Der Human Maintainer hat ihn am **2026-10-17** in Phase **G2** von CBP-WP-023
> ausdrücklich angenommen (A0). Die **A0-Entscheidung D-069** bleibt die
> Grundlage der fünf Dimensionen; dieser ADR verankert ihre Trennung
> architektonisch und löst die widersprechenden Sichtbarkeitsaussagen in
> ADR-0006 und ADR-0007 **partiell** ab. Beide bleiben im Übrigen `accepted`.

---

## Kontext

ADR-0007 führte am 2026-07-21 den Begriff **`publication-capable by design`**
ein: Das Core-Repository ist so gebaut, dass privater Bestand, produktive
Mappings und Secrets konstruktiv ausgeschlossen sind. Zugleich hielt ADR-0007
fest, das Repository bleibe **zunächst privat**, und führte die Sichtbarkeit als
offene Entscheidung **OD-11**. Der Klarstellungsnachtrag von ADR-0006 übernahm
dies als Verbindliche Folgerung 2: *„Die Repository-Sichtbarkeit bleibt
privat."*

GitHub weist das Repository als **öffentlich** aus. Wann die Sichtbarkeit
gewechselt hat, ist **nicht belegt**. Der Human Maintainer hat am 2026-10-17
entschieden (**D-069**, A0), das Repository als öffentlich sichtbares
Entwicklungsrepository zu führen — **ohne** die Produktveröffentlichung, eine
Lizenz oder ein Branding freizugeben.

## Problem

Die bisherige Dokumentation verwendet „privat", „veröffentlicht" und
„veröffentlichbar" so, dass **drei verschiedene Sachverhalte** ineinander
übergehen:

1. ob Quellcode und Git-Historie **öffentlich einsehbar** sind,
2. ob das Projekt sich in einem **kontrollierten Entwicklungszustand** befindet,
3. ob ein **Produkt veröffentlicht**, lizenziert oder öffentlich positioniert
   ist.

Ohne eine dauerhafte Trennung droht jede künftige Statusaussage eine dieser
Dimensionen stillschweigend aus einer anderen abzuleiten — etwa „öffentlich
sichtbar, also freigegeben" oder „nicht veröffentlicht, also privat".

## Bindende Authority

| Quelle | Klasse | Inhalt |
| --- | --- | --- |
| **D-069** | **A0** | Repository Visibility **PUBLIC** · Development State **PRIVATE DEVELOPMENT** · Product Publication **NOT AUTHORIZED** · Lizenz **UNDECIDED** · Branding gesperrt · `ADR_REQUIRED` |
| [DO_NOT_START.md](../product/DO_NOT_START.md) | **A0** | #11 Öffentliches Branding, #12 Öffentliche Produktveröffentlichung, #13 Endgültiges Branding — **gesperrt** |
| **D-003** | **A0** | Commit-, Push- und Release-Autorität ausschließlich beim Human Maintainer |
| **Human-Maintainer-Annahme** (2026-10-17, Phase G2) | **A0** | Annahme dieses ADR (`accepted`, A1) und partielle Ablösung der Sichtbarkeitsaussagen in ADR-0006 und ADR-0007 — **keine neue Decision**, D-069 unverändert |
| [ADR-0006](ADR-0006-logische-source-slots.md), [ADR-0007](ADR-0007-repository-und-workspace-grenze.md) | **A1** | `accepted`; Sichtbarkeitsaussagen durch diesen ADR **partiell abgelöst** (siehe *Supersession Boundary*), im Übrigen unverändert gültig |

## Entscheidung

Das Core-Repository wird über **fünf voneinander unabhängige Dimensionen**
beschrieben. Keine Dimension wird aus einer anderen abgeleitet.

| Dimension | Zustand | Grundlage |
| --- | --- | --- |
| **Repository Visibility** | **PUBLIC** | D-069 (A0) |
| **Development State** | **PRIVATE DEVELOPMENT** | D-069 (A0) |
| **Product Publication** | **NOT AUTHORIZED** | D-069 (A0), DO_NOT_START #12 |
| **License** | **UNDECIDED** | OD-23 |
| **Public Branding** | **gesperrt** | DO_NOT_START #11, #13 |

### Normative Trennung

| PUBLIC bedeutet | PUBLIC bedeutet **nicht** |
| --- | --- |
| Quellcode und Git-Historie können öffentlich eingesehen werden | eine Open-Source-Lizenz |
| Jeder künftige Push macht die betreffenden Inhalte öffentlich verfügbar | eine Produktfreigabe |
| | produktive Einsatzbereitschaft |
| | bestandene Security Gates |
| | eine Freigabe von Datenquellen |
| | eine Freigabe von Branding |
| | eine Freigabe externer Beiträge als Governance-Authority |

**PRIVATE DEVELOPMENT** bedeutet: Das Projekt bleibt ein kontrolliertes
Entwicklungsprojekt unter dem Rollenmodell Nova → Implementation Agent → Human
Maintainer. Öffentliche Einsehbarkeit ändert weder Autoritätsmodell noch
Lifecycle noch Commit-Autorität.

**`publication-capable by design`** bleibt eine **Bauweise** im Sinne von
ADR-0007 — keine Aussage über den Zustand einer der fünf Dimensionen.

### Architekturpräzisierung

ADR-0015 präzisiert **ausschließlich** die Sichtbarkeitsaussagen in ADR-0006
und ADR-0007. **Nicht** abgelöst oder verändert werden:

- das Source-Slot-Modell aus ADR-0006,
- die W-3-Workspace-Grenze und die Bereichsgliederung RT-1/RT-2/RT-3,
- die Repository- und Monorepo-Zielstruktur aus ADR-0007,
- die Grenzen **G1 bis G10** aus ADR-0007,
- bestehende Sicherheitsgrenzen und operative Contracts,
- bestehende Rollen und Autoritäten.

## Supersession Boundary

**Seit der Annahme in G2 (2026-10-17) gilt:**

- Die unten genannten Sichtbarkeitsaussagen sind durch diesen ADR (**A1**)
  **partiell abgelöst**. Sie bleiben in ADR-0006 und ADR-0007 **im Wortlaut
  erhalten** und dokumentieren den Governance-Stand vom 2026-07-21.
- ADR-0006 und ADR-0007 bleiben **`accepted`**. Ihr Feld *Superseded by* bleibt
  **—**, weil **keine vollständige Ablösung** stattfindet; beide tragen einen
  datierten **Teilablösungsvermerk** mit Verweis auf diesen ADR.
- Die **A0-Wirkung von D-069** bleibt die Grundlage der Sichtbarkeitsfestlegung.

*Bis zur Annahme (Phase G1) galt:* Keine A1-Teilablösung war erfolgt; die
A0-Wirkung von D-069 bestand unabhängig von diesem ADR und hatte nach dem
Autoritätsmodell Vorrang vor widersprechenden A1-Formulierungen; ADR-0006 und
ADR-0007 trugen nur einen datierten Governance-Vermerk.

**Abgelöster Bereich (wirksam seit 2026-10-17):**

| ADR | Stelle | Aussage |
| --- | --- | --- |
| ADR-0006 | Klarstellungsnachtrag, Verbindliche Folgerung 2 | „Die Repository-Sichtbarkeit bleibt privat." |
| ADR-0007 | Abschnitt *Core Repository — Zielstruktur* | „Das Repository bleibt zunächst privat." sowie „OD-11 ist offen" |
| ADR-0007 | *Git- und Veröffentlichungswirkung* | *Aktuelle Sichtbarkeit*: privat · *OD-11*: bleibt offen |
| ADR-0007 | *Offene Folgefragen* | Zeilen zu OD-11 (Repository-Sichtbarkeit) |

**Ausdrücklich nicht abgelöst:** die Anforderung, dass eine
**Produktveröffentlichung**, eine **Lizenz**, ein **Branding** und ein
**Release** je eine separate A0-Entscheidung benötigen (ADR-0006, Folgerungen 3
bis 5; ADR-0007, Abschnitt *Core Repository — Zielstruktur*).

## Alternativen

| # | Alternative | Bewertung |
| --- | --- | --- |
| 1 | **D-069 ohne ADR** | **Verworfen.** D-069 bindet als A0 die Sichtbarkeit, aber die widersprechenden A1-Formulierungen in ADR-0006 und ADR-0007 blieben ohne A1-Anker stehen. Die dauerhafte Trennung dreier Begriffe ist eine Architekturregel für alle künftigen Statusaussagen; D-069 Teil J hat **`ADR_REQUIRED`** festgestellt. |
| 2 | **Vollständige Ablösung von ADR-0007** | **Verworfen.** Monorepo-Zielstruktur, W-3, RT-Gliederung und die Grenzen G1 bis G10 sind von der Sichtbarkeitsfrage nicht betroffen. Eine Vollablösung würde bindende Architektur ohne Anlass destabilisieren. |
| 3 | **Rückwirkende Umschreibung der alten ADRs** | **Verworfen.** Ein ADR wird nie rückwirkend umgeschrieben; die Nachvollziehbarkeit des früheren Governance-Stands ginge verloren. |
| 4 | **Rückkehr zu GitHub Private** | **Verworfen** durch den Human Maintainer (A0-1, D-069). Sie würde zudem eine bereits erfolgte öffentliche Einsehbarkeit nicht ungeschehen machen. |

**Begründung der gewählten Lösung:** Eine dauerhafte Trennung von
Sichtbarkeit, Entwicklungsstatus und Produktveröffentlichung braucht einen
eigenständigen, nachvollziehbaren **A1-Anker**, der die älteren ADRs nur dort
präzisiert, wo sie der A0-Entscheidung widersprechen.

## Konsequenzen

### Positiv

- Statusaussagen können jede der fünf Dimensionen einzeln und widerspruchsfrei
  benennen.
- Der Widerspruch zwischen A0-Entscheidung und A1-Formulierungen ist mit der
  Annahme kanonisch aufgelöst, ohne historischen Wortlaut zu verändern.
- Die Sperrliste bleibt unverändert wirksam; Branding und Release werden nicht
  implizit mitentschieden.

### Negativ

- **Jeder Push ist öffentlich.** Versehentlich committete sensible Inhalte,
  automatisiert erzeugte Dateien oder lokale Betriebsangaben werden mit dem Push
  unmittelbar einsehbar (**R-01**).
- Bis zur Annahme in G2 bestanden A0-Entscheidung und unveränderte
  A1-Formulierungen nebeneinander. Seit der Annahme bleiben die abgelösten
  Formulierungen im Wortlaut sichtbar und sind nur zusammen mit den datierten
  Teilablösungsvermerken in ADR-0006 und ADR-0007 richtig zu lesen.
- Ein negativer Vertraulichkeitsaudit ist **keine** Sicherheitsgarantie.

## Risiken und Gegenmaßnahmen

| Risiko | Gegenmaßnahme | Stand |
| --- | --- | --- |
| **R-01** — Secret oder sensibler Inhalt gelangt in die öffentliche Git-Historie | Vertraulichkeitsprüfung des Diffs vor jedem Human-Maintainer-Push (D-069 Teil I); Schadensverfahren SECRET_INCIDENT_RESPONSE | **dokumentierte Anforderung, keine implementierte Kontrolle**; GitHub-Schutzfunktionen **nicht als aktiviert nachgewiesen** |
| **R-16** — Dokumentation driftet vom tatsächlichen Stand ab | Nachführung der aktiven Sichtbarkeitsspiegel in CBP-WP-023; datierte Vermerke statt Umschreibung | offen |

## Non-Goals

Dieser ADR autorisiert **nicht**: eine Lizenzwahl · eine Produktveröffentlichung
· Branding, Logos, Wortmarken, Marketingtexte oder Social Previews · ein
Release · einen GitHub-Transfer, eine Umbenennung oder einen Remote-Wechsel
(A0-2) · eine Gate-Hochstufung · operative Security-Evidenz · die Closure von
CBP-WP-022.

## Do-not-start-Grenzen

DO_NOT_START **#11**, **#12** und **#13** bleiben **gesperrt**. Da kein
Sperrpunkt aufgehoben wird, ist das Aufhebungsverfahren der Sperrliste **nicht**
ausgelöst.

## Security Impact

Keine Kontrolle wird umgesetzt oder hochgestuft. **12 Kontrollen bleiben
`DOCUMENTED ONLY`**, KB-04 bleibt **`DOCUMENTED ONLY`**, Mapping Activation Gate
und Security Foundation Readiness Gate bleiben **`NOT EVALUATED`**. Die
öffentliche Sichtbarkeit erhöht die Bedeutung der Grenzen **G1**, **G2** und
**G6** aus ADR-0007.

## Acceptance Criteria für G2

1. Ausdrückliches Human-Maintainer-GO zur Annahme von ADR-0015 — **erfüllt**
   (Human-Maintainer-A0 vom 2026-10-17, A0-G2-2).
2. Nova-Review des G1-Diffs abgeschlossen — **erfüllt** (`GO WITH NOTES`, vom
   Human Maintainer angenommen, A0-G2-1).
3. Ablösungsbereich unverändert auf die Sichtbarkeitsaussagen begrenzt —
   **erfüllt** (siehe *Supersession Boundary*).
4. Definitive Teilablösungsvermerke in ADR-0006 und ADR-0007 nachgeführt —
   **erfüllt** im uncommitteten G2-Review-Diff.
5. Zähler nachgeführt: angenommene ADRs **15**, vorgeschlagene ADRs **0** —
   **erfüllt** im uncommitteten G2-Review-Diff.

Der G2-Diff wurde von Nova mit `GO WITH NOTES` geprüft und vom Human Maintainer am 17.10.2026 angenommen.
Commit und Push erfolgen in Phase G3 ausschließlich nach gesonderter Freigabe durch den Human Maintainer.

## Autoritätsgrenzen

Ein Implementation Agent kann diesen ADR als `proposed` verfassen; **die
Annahme bleibt dem Human Maintainer vorbehalten**. Der Human Maintainer hat sie
am 2026-10-17 ausdrücklich erteilt (A0); der Implementation Agent hat sie in G2
ausschließlich nachgeführt. Nova besitzt keine A0-Autorität. Commit und Push
erfolgen ausschließlich durch den Human Maintainer (D-003).

## Bezug

**D-069** · **OD-11** (beantwortet), **OD-23**, **OD-28** (offen) ·
[ADR-0006](ADR-0006-logische-source-slots.md) ·
[ADR-0007](ADR-0007-repository-und-workspace-grenze.md) ·
[DO_NOT_START.md](../product/DO_NOT_START.md) #11, #12, #13 · Risiken **R-01**,
**R-16** · [CBP-WP-023](../../work-packages/CBP-WP-023.md)
