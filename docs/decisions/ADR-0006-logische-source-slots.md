# ADR-0006 — Logische Source Slots statt eingebetteter Wissensbestände

| Feld | Wert |
| --- | --- |
| Status | **accepted** |
| Datum | 2026-07-21 |
| Entscheider | **Human Maintainer** |
| Angenommen am | **2026-07-21** |
| Autorität | **A0** — direkte Human-Maintainer-Entscheidung |
| Supersedes | — |
| Superseded by | — |
| Teilweise abgelöst durch | [ADR-0015](ADR-0015-repository-sichtbarkeit-und-publikationsstatus.md) (`accepted`, **A1**, 2026-10-17) — **ausschließlich** Klarstellungsnachtrag, Verbindliche Folgerung 2 (Repository-Sichtbarkeit); **keine vollständige Ablösung**, siehe *Teilablösungsvermerk 2026-10-17* |
| Vorgeschlagen in | CBP-WP-006 · angenommen in CBP-WP-007 |
| Belegt durch | Übergabe §13 (A5), D-019, D-025 (A0), ADR-0001, ADR-0003 |

> **Dieser ADR ist angenommen und bindend.** Er trägt Autoritätsklasse **A1**.

## Entscheidung des Human Maintainers

*Wortlaut aus dem Entscheidungsblock in
[G0_SCOPE_LOCK_REVIEW.md](../discovery/G0_SCOPE_LOCK_REVIEW.md), unverändert
übernommen:*

> Produktive und private Wissensbestände bleiben außerhalb des allgemeinen
> Core-Repositorys.
>
> Sie werden über logische Source Slots und deploymentspezifische, fail-closed
> Mappings angebunden.
>
> Die Entscheidung legt keine konkreten Pfade, Repository-URLs oder
> Produktionsbestände fest.
>
> OD-05 und OD-06 bleiben für konkrete Quellen und Mappings offen.
> OD-26 bleibt für die spätere Repository-Layout-Entscheidung offen.

### Konsequenz für Source Slots und Repository-Grenze

| Gegenstand | Wirkung |
| --- | --- |
| Repository-Grenze | **Bindend:** kein privater oder produktiver Wissensbestand im allgemeinen Core-Repository |
| Source Slots | PS-01 bis PS-07 aus [PILOT_SOURCE_CONTRACT.md](../sources/PILOT_SOURCE_CONTRACT.md) sind die verbindliche Anbindungsform |
| Mappings | **fail-closed** — ohne Mapping bleibt ein Slot `enabled: false` (Slot-Regel 7) |
| Konkrete Pfade und URLs | **nicht festgelegt** und ausdrücklich nicht Gegenstand dieser Entscheidung |
| **OD-05, OD-06** | bleiben **offen** — konkrete Quellen und Mappings |
| **OD-26** | bleibt **offen** — Repository-Layout |

## Kontext

G0-Kriterium **D-1** verlangt, die gewünschten Quellen zu benennen. Der Intake
hat die Quellen**arten** entschieden (HDI A3), aber nicht den konkreten
Bestand. D-1 blieb deshalb als einziger Core-Blocker auf `answered`.

Zwei Wege wären möglich gewesen: den privaten Wissensbestand in das
Projektrepository aufnehmen und damit D-1 konkret beantworten — oder die
Anbindung so beschreiben, dass sie ohne Kenntnis des konkreten Bestands
prüfbar wird.

Der erste Weg kollidiert mit drei bestehenden Festlegungen:

- Projektübergabe §13 verlangt, dass die Architektur **von Anfang an öffentlich
  dokumentierbar** bleibt und keine privaten Pfade oder Namen im öffentlichen
  Kern erscheinen.
- ADR-0001 verlangt Deployment-Neutralität: nichts Installationsspezifisches
  im Kern.
- Die Repository-Sichtbarkeit ist offen (OD-11), der Ablageort des kanonischen
  Bestands ebenfalls (OD-05).

Ein Repository, das einen privaten Bestand voraussetzt, ist weder portabel noch
veröffentlichbar — und die Entscheidung darüber wäre stillschweigend gefallen.

## Entscheidungsvorschlag

**Produktive Wissensquellen werden über logische Source Slots und
deploymentspezifische Mappings angebunden — nicht durch Einbettung in das
Core-Repository.**

Im Einzelnen:

1. **Das allgemeine Core-Repository enthält** Projektsteuerung, Architektur,
   Sicherheits- und Betriebsdokumentation, Tests und synthetische Beispiele.
2. **Private oder installationsspezifische Wissensbestände werden nicht als
   Voraussetzung aufgenommen.** Kein konkreter Pfad, keine Repository-URL, kein
   Fremdsystem ist Bestandteil des allgemeinen Repositorys.
3. **Anbindung über zwei Ebenen:** ein **Logical Source Slot** definiert
   produktunabhängig, welche Art von Quelle zulässig ist und welche Regeln
   gelten; ein **Deployment Mapping** ordnet den Slot in einer konkreten
   Installation einem Ort zu.
4. **Der erste Retrieval-Pilot unterstützt** primär Markdown (PS-02),
   ausgewählte Git-Repositories (PS-03) und freigegebene Chat-Handoffs (PS-04),
   dazu die Projektsteuerung selbst (PS-01) und den synthetischen
   Benchmark-Korpus als Testartefakt (PS-05).
5. **PDF/Office (PS-06) und externe Connectoren (PS-07) bleiben `deferred`**,
   bis Quarantäne, Parser und Freigabepipeline existieren.

**G0 benötigt die Slot-Ebene. Ein Deployment benötigt zusätzlich das Mapping.**

## Alternativen

**Privaten Wissensbestand in das Core-Repository aufnehmen.** Verworfen:
verletzt Übergabe §13 und ADR-0001, präjudiziert OD-11 und OD-05, und macht
eine spätere Veröffentlichung praktisch unmöglich — was einmal in der Historie
steht, bleibt dort.

**D-1 auf konkrete Pfade festlegen.** Verworfen: Pfade sind
installationsspezifisch. Ein Scope Lock, der an einem Windows- oder Linux-Pfad
hängt, ist beim ersten Umzug ungültig. Genau diese Vermischung hat schon einmal
zum REWORK geführt (CBP-WP-003, dreistufiges Kriterienmodell).

**D-1 offen lassen und G0 blockieren.** Verworfen: der Blocker ist
dokumentarisch auflösbar, ohne etwas vorwegzunehmen. Ein Gate, das auf eine
Angabe wartet, die es gar nicht braucht, hält das Projekt ohne Erkenntnisgewinn
auf.

**Alle Quellenarten sofort unterstützen.** Verworfen: PDF und Office ohne
Quarantäne verletzen D-019 und TB-1. Ein Connector ohne Löschprozess erzeugt
einen Bestand, der Gelöschtes weiterführt.

## Konsequenzen

**Leichter:** Das Repository bleibt veröffentlichbar, ohne dass ein privater
Bestand herausgelöst werden müsste. Ein Betreiberwechsel oder ein Umzug
verändert nur das Mapping. Der Scope Lock wird unabhängig von der Installation
prüfbar. Neue Quellenarten entstehen als neue Slots, nicht als Sonderfälle.

**Schwerer:** Zwei Ebenen sind zu pflegen. Jede Aktivierung braucht ein
zusätzliches Mapping. Vor dem ersten Deployment ist das System vollständig
beschrieben, aber leer — man sieht ihm nicht an, ob die Beschreibung trägt.

**Geschlossene Türen:** Der Weg, „einfach das Vault-Verzeichnis einzuchecken",
ist ausgeschlossen. Das ist beabsichtigt.

## Datenschutzwirkung

**Stark positiv.** Der private Wissensbestand gerät konstruktiv nicht in die
Git-Historie des Core-Repositorys — der wirksamste Schutz gegen R-01, weil er
nicht auf Disziplin beruht. Datenklassen und AI-Transfer-Regeln werden je Slot
gesetzt, `excluded-from-ai` erzwingt `forbidden` (Regel 5), und Unbekanntes
läuft fail-closed (Regel 6).

**Grenze:** Die Trennung ist eine **Architekturentscheidung, keine technische
Kontrolle**. Es existiert kein Mechanismus, der das Einchecken eines privaten
Bestands verhindert — nur `.gitignore` als erste, unvollständige Stufe.

## Portabilitätswirkung

Der Kern bleibt frei von Installationsannahmen. Alle fünf Deploymentprofile
A–E nutzen dieselben Slots mit unterschiedlichen Mappings. Ein Wechsel von
Profil A auf B berührt keine Slot-Definition.

## Open-Source-Wirkung

Das Core-Repository wird veröffentlichbar, **ohne** dass eine Trennung
nachträglich durchgeführt werden müsste. Die synthetischen Benchmark-Fixtures
liefern Beispieldaten, die gefahrlos mitgeliefert werden können.

Die Entscheidung **erzwingt keine Veröffentlichung** — OD-11 bleibt offen. Sie
hält die Option offen.

## Migrationswirkung

**Gering, weil nichts existiert.** Es sind keine Quellen angebunden, kein Index
gebaut, keine Datei zu verschieben. Diese Entscheidung ist heute am billigsten;
nach dem ersten Ingest wäre sie eine Datenmigration.

Zum Repository-Layout ist sie **neutral**: Option A, B und C aus
[REPOSITORY_LAYOUT_OPTIONS.md](../architecture/REPOSITORY_LAYOUT_OPTIONS.md)
sind alle mit Source Slots vereinbar. **OD-26 bleibt offen.**

## Offene Punkte

| Punkt | Register | Status |
| --- | --- | --- |
| Ablageort des kanonischen Bestands | **OD-05** | **offen** — dieser ADR legt die Art fest, nicht den Ort |
| Konkrete Quellen und Nicht-Quellen | **OD-06** | **offen** |
| Repository-Layout | **OD-26** | **offen** |
| Repository-Sichtbarkeit | OD-11 | offen |
| Konkrete Deployment Mappings | DRC | `not-evaluated` |
| Technische Durchsetzung der Slot-Regeln | R-25, R-27 | offen |

---

## Klarstellungsnachtrag — 2026-07-21

| Feld | Wert |
| --- | --- |
| Art | **Non-substantive clarification** |
| Datum | 2026-07-21 |
| Ergänzt in | **CBP-WP-010** |
| Autorität | **A1** — abgeleitet aus [ADR-0007](ADR-0007-repository-und-workspace-grenze.md) und den unveränderten A0-Entscheidungen **D-029** und **D-030** |
| Wirkung auf Entscheidung und Status | **keine** |

**Entscheidung und Status dieses ADR bleiben unverändert.** Er bleibt
`accepted` und trägt weiterhin A1. Der Wortlaut oben wurde **nicht**
umgeschrieben.

### Gegenstand der Klarstellung

Dieser ADR verwendet an mehreren Stellen die Begriffe „veröffentlichbar" und
„Open-Source-Wirkung" — unter anderem in **Konsequenzen**, **Open-Source-Wirkung**
und in der Begründung der Alternativen. Diese Formulierungen beschreiben eine
**Architekturabsicht**, gleichbedeutend mit dem in ADR-0007 eingeführten Begriff
**`publication-capable by design`**.

| Die Begriffe bedeuten | Die Begriffe bedeuten **nicht** |
| --- | --- |
| Privater und produktiver Bestand ist konstruktiv ausgeschlossen | öffentliche Freigabe |
| Eine nachträgliche Trennung wäre nicht erforderlich | Open-Source-Freigabe |
| Synthetische Fixtures dürfen mitgeliefert werden | Lizenzentscheidung |
| Die Option bleibt offen | Branding-Freigabe |
| | Release-Autorisierung |

### Verbindliche Folgerungen

| # | Feststellung |
| --- | --- |
| 1 | **Aus diesem ADR folgt keine öffentliche Freigabe.** |
| 2 | **Die Repository-Sichtbarkeit bleibt privat.** |
| 3 | **Veröffentlichung, Lizenz, Branding und Release benötigen jeweils eine separate A0-Entscheidung** — OD-11, OD-23, OD-28. |
| 4 | **Es besteht keine pauschale Zusicherung**, dass der jeweils aktuelle Gesamtinhalt des Repositorys ohne erneute Prüfung veröffentlicht werden darf. |
| 5 | Die Sperrlisteneinträge zu öffentlichem Branding, Release und Veröffentlichung in [DO_NOT_START.md](../product/DO_NOT_START.md) bleiben bestehen. |

**Zu Punkt 4:** Die Bauweise sichert zu, dass **strukturell** kein privater
Bestand enthalten ist. Sie sagt nichts darüber aus, ob einzelne Dokumente —
etwa interne Statusberichte, Risikoeinschätzungen oder Betriebsdetails — im
Einzelfall für eine Veröffentlichung geeignet sind. Diese Prüfung wäre
Gegenstand einer eigenen Entscheidung.

Vollständige Ausformulierung des Begriffs in
[ADR-0007](ADR-0007-repository-und-workspace-grenze.md), Abschnitt „Core
Repository — Zielstruktur".

**Dieser ADR schließt OD-05, OD-06 und OD-26 nicht** und darf das nicht.

## Governance-Vermerk 2026-10-17 — Repository-Sichtbarkeit

*Stand Phase G1 — als G1-Nachweis unverändert erhalten; durch den
Teilablösungsvermerk unten (Phase G2) fortgeschrieben.*

| Feld | Wert |
| --- | --- |
| Art | **Datierter Governance-Vermerk** — keine Änderung von Entscheidung, Status oder Wortlaut |
| Datum | 2026-10-17 |
| Ergänzt in | **CBP-WP-023**, Phase G1 (uncommitted Review-Diff) |
| Bezug | **D-069** (A0) · [ADR-0015](ADR-0015-repository-sichtbarkeit-und-publikationsstatus.md) (`proposed`) |
| Wirkung auf Entscheidung und Status | **keine** |

Die **Verbindliche Folgerung 2** des Klarstellungsnachtrags — *„Die
Repository-Sichtbarkeit bleibt privat."* — gibt den **Governance-Stand vom
2026-07-21** wieder und bleibt **im Wortlaut unverändert**.

- **D-069** (`accepted`, **A0**, 2026-10-17) hat die Repository-Sichtbarkeit
  **PUBLIC** bestätigt: Development State **PRIVATE DEVELOPMENT**, Product
  Publication **NOT AUTHORIZED**, Lizenz offen (OD-23), Branding gesperrt. Für
  die Repository-Sichtbarkeit ist D-069 als A0 **bereits verbindlich**.
- **ADR-0015** ist zur Architekturpräzisierung **`proposed`**. Er soll nach
  seiner Annahme **ausschließlich** die Sichtbarkeitsaussage der Folgerung 2
  teilweise ablösen.
- **Die formale A1-Teilablösung ist nicht erfolgt.** Sie verlangt die Annahme
  von ADR-0015 in Phase **G2** nach erneutem ausdrücklichem
  Human-Maintainer-GO; bis dahin bleibt *Superseded by* unverändert.
- **Unverändert gültig** bleiben das Source-Slot-Modell sowie die Folgerungen
  1, 3, 4 und 5 — eine **Produktveröffentlichung**, eine Lizenz, ein Branding
  und ein Release benötigen weiterhin je eine separate A0-Entscheidung.
- D-069 legitimiert die frühere, zeitlich nicht belegte Abweichung zwischen
  Dokumentation und tatsächlicher Sichtbarkeit **nicht rückwirkend**.

## Teilablösungsvermerk 2026-10-17 — ADR-0015 (Phase G2)

| Feld | Wert |
| --- | --- |
| Art | **Datierter Teilablösungsvermerk** — partielle Ablösung durch einen späteren ADR, **keine** vollständige Ablösung |
| Datum | 2026-10-17 |
| Ergänzt in | **CBP-WP-023**, Phase G2 (uncommitted Review-Diff) |
| Grundlage | **Human-Maintainer-A0** vom 2026-10-17 — Annahme von ADR-0015 (A0-G2-2) und partielle Ablösung (A0-G2-3) |
| Abgelöst durch | [ADR-0015](ADR-0015-repository-sichtbarkeit-und-publikationsstatus.md) — `accepted`, **A1** |
| Abgelöster Umfang | **ausschließlich** Klarstellungsnachtrag, Verbindliche Folgerung 2: *„Die Repository-Sichtbarkeit bleibt privat."* |
| Status dieses ADR | **`accepted`** — unverändert; *Superseded by* bleibt **—** |

- Für die **Repository-Sichtbarkeit** gilt seit dem 2026-10-17 ADR-0015 (A1)
  auf Grundlage von **D-069** (A0): Repository Visibility **PUBLIC** ·
  Development State **PRIVATE DEVELOPMENT** · Product Publication **NOT
  AUTHORIZED** · License **UNDECIDED** · Public Branding **gesperrt**.
- Die Folgerung 2 bleibt **im Wortlaut erhalten** und dokumentiert den
  Governance-Stand vom 2026-07-21; für die Repository-Sichtbarkeit ist sie
  **nicht mehr maßgeblich**.
- **Nicht abgelöst** und unverändert bindend sind Entscheidung und Status
  dieses ADR, das Source-Slot-Modell sowie die Folgerungen 1, 3, 4 und 5 — eine
  **Produktveröffentlichung**, eine Lizenz, ein Branding und ein Release
  benötigen weiterhin je eine separate A0-Entscheidung.

## Bezug

G0-Kriterium **D-1** ·
[PILOT_SOURCE_CONTRACT.md](../sources/PILOT_SOURCE_CONTRACT.md) ·
[SOURCE_SLOT_MODEL.md](../sources/SOURCE_SLOT_MODEL.md) ·
[ADR-0001](ADR-0001-deployment-neutraler-core.md) ·
[ADR-0003](ADR-0003-canonical-derived-trennung.md) ·
Risiken R-01, R-32 · Übergabe §13
