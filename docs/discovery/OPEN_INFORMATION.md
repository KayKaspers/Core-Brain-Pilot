# Open Information — fehlende Eingangsinformation

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Überarbeitet in | CBP-WP-002 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

Während [DISCOVERY_QUESTIONS.md](DISCOVERY_QUESTIONS.md) offene
**Entscheidungen** sammelt und
[G0_SCOPE_LOCK_CRITERIA.md](G0_SCOPE_LOCK_CRITERIA.md) die **Gate-Kriterien**
führt, verzeichnet dieses Dokument fehlende oder nicht zugängliche
**Eingangsinformation**.

---

## OI-01 — Zwei verbindliche Quellen lagen zunächst nicht vor

**Schweregrad:** hoch · **Status:** **GESCHLOSSEN** (2026-07-20, CBP-WP-002)

### Ursprünglicher Befund

CBP-WP-001 nannte vier verbindliche Grundlagen. Zwei davon — die
Core-Brain-Übergabe und die Second-Brain-Bauanleitung — waren dem
Implementation Agent in der Ausführungssitzung nicht zugänglich. Das Fundament
wurde deshalb aus dem Wortlaut des Work Packages abgeleitet.

### Auflösung

| Bedingung aus CBP-WP-002 | Erfüllt |
| --- | --- |
| A5-Projektübergabe vollständig gelesen | **ja** — `docs/discovery/Core-Brain-Project-Handoff.md`, 20 Abschnitte, getrackt in Commit `03a29f5` |
| A6-Textrepräsentation vollständig gelesen | **ja** — `Second-Brain-Bauanleitung-Textfassung.md`, Seitenmarker 1 bis 6 |
| Provenienz zur PDF dokumentiert | **ja** — [SOURCE_RECONCILIATION.md](SOURCE_RECONCILIATION.md) Abschnitt 1 |
| Keine ungeklärte inhaltliche Abweichung | **ja** — fünf Widersprüche W-01 bis W-05 erfasst; vier aufgelöst, einer (W-05, Repository-Struktur) bewusst als offene Entscheidung OD-26 geführt, nicht ungeklärt |

Der vollständige Abgleich mit 20 bestätigten Übereinstimmungen, 16 Ergänzungen
und 5 Abschwächungen liegt in
[SOURCE_RECONCILIATION.md](SOURCE_RECONCILIATION.md).

### Verbleibende Einschränkung

Der Fließtext der PDF war im lokalen Werkzeug nicht zuverlässig extrahierbar.
Die Auswertung stützt sich auf die A6-Textfassung. Eine **visuelle
Detailprüfung der PDF wird nicht behauptet**. Sollte die Textfassung von der
PDF abweichen, gilt die PDF (A4) — die Textfassung beansprucht keine höhere
Autorität.

Diese Einschränkung ist als eigenständiges Risiko R-22 erfasst und schließt
OI-01 nicht wieder auf: die Freigabebedingungen aus CBP-WP-002 sind erfüllt.

---

## OI-02 — Herkunft und Rang der Kernprinzipien

**Schweregrad:** mittel · **Status:** **teilweise aufgelöst** · **Adressat:** Human Maintainer

Der Quellenabgleich hat die inhaltliche Herkunft geklärt: Die Kernprinzipien
und der Capability-Katalog sind durch die A5-Projektübergabe gedeckt — siehe
die 20 bestätigten Übereinstimmungen in
[SOURCE_RECONCILIATION.md](SOURCE_RECONCILIATION.md) Abschnitt 2.

**Offen bleibt der formale Rang.** Die Prinzipien tragen A2 und sind nicht als
ADR ausgefertigt. Die Bezeichnung „verbindlich" wurde entsprechend präzisiert
(Abschwächung Ü-04).

Eine Ausnahme: Capability 27 „read-only MCP/API" findet sich in **keiner** der
beiden Originalquellen. Ihre Provenienz ist CBP-WP-001 (A2). Vermerkt in der
Capability Matrix.

Weiterverfolgt als OD-03.

---

## OI-03 — Definition der Context Budgets B0–B4

**Schweregrad:** mittel · **Status:** **GESCHLOSSEN** (2026-07-20, CBP-WP-002)

B0 bis B4 sind in [../architecture/CONTEXT_BUDGETS.md](../architecture/CONTEXT_BUDGETS.md)
mit je sieben Attributen definiert: geeignete Aufgaben, maximaler
Quellenumfang, erlaubte Kontextarten, Zielgröße des Quellkontexts, erwartete
Rückmeldelänge, Reviewtiefe und Eskalationsbedingungen. Für B4 sind die sechs
Pflichtfragen und ein Eskalationsprotokoll festgelegt.

**Einschränkung:** Die Token-Zielgrößen sind gesetzte Richtwerte, keine
gemessenen Schwellen. Sie stammen nicht aus den Originalquellen und sind gegen
den Benchmark zu validieren. Die harte Grenze ist die Quellenzahl.

Verbleibende Kalibrierung als OD-02 geführt.

---

## OI-04 — Gate-Kriterien für G0

**Schweregrad:** mittel · **Status:** **GESCHLOSSEN** (2026-07-20, CBP-WP-002)

41 objektiv prüfbare Kriterien in sieben Bereichen liegen in
[G0_SCOPE_LOCK_CRITERIA.md](G0_SCOPE_LOCK_CRITERIA.md) vor, davon 39
blockierend. Jedes Kriterium führt Nachweis, Owner, Status, erforderliche
Autorität und Blockierungskennzeichen. Die Abschlussregel ist fünfteilig und
endet mit der ausdrücklichen Freigabe des Human Maintainers.

**Gate-Status weiterhin NOT PASSED** — kein Kriterium ist beantwortet.

---

## OI-05 — Zielumgebung nicht verifiziert

**Schweregrad:** niedrig · **Status:** offen · **Adressat:** Human Maintainer

Proxmox als Referenzplattform und die dedizierte Linux-VM sind dokumentiert,
aber nicht verifiziert. In Phase 0 wurde bewusst keine Umgebungsprüfung
durchgeführt — das wäre Betriebsarbeit vor dem Scope Lock.

Die Erhebung erfolgt über den Fragebogen, Abschnitt 1, und die G0-Kriterien
B-1 bis B-8.

---

## OI-06 — Benchmarkfragen noch nicht formuliert

**Schweregrad:** mittel · **Status:** offen · **Adressat:** Nova + Human Maintainer

Projektübergabe §16 nennt zehn Erfolgskriterien, Bauanleitung Seite 3
beschreibt das Baseline-Verfahren. Beides ist in die G0-Kriterien G-1 bis G-6
überführt.

Es existiert jedoch noch **keine einzige** der geforderten mindestens 30
Benchmarkfragen. Ohne sie ist Erfolgskriterium 2 („Baselinefragen werden
korrekt beantwortet") nicht prüfbar, und die Formulierungen „deutlich weniger
Dateien" und „deutlich weniger Kontext" bleiben unquantifiziert.

Die Fragen können erst sinnvoll entstehen, wenn der reale Wissensbestand
bekannt ist — also nach Beantwortung von D-1 bis D-3.

---

## OI-07 — Repository-Struktur nicht freigegeben

**Schweregrad:** mittel · **Status:** offen · **Adressat:** Nova + Human Maintainer

Drei Strukturvorstellungen stehen nebeneinander:

| Quelle | Struktur |
| --- | --- |
| Projektübergabe §13 (A5) | `core/`, `deployments/`, `docs/`, `examples/` — ausdrücklich noch nicht freigegeben |
| NDF v1.0.0 (A1) | `project-manifest.yaml`, `project-brain/DECISIONS.md`, `prompts/claude/work-packages/` |
| Repository (A2) | Struktur aus CBP-WP-001 |

Die Übergabe stellt selbst klar, dass die konkrete Struktur im Projekt geplant
werden muss. Deshalb sind die Abweichungen AB-03 bis AB-08 nur **vorläufig für
den Bootstrap** akzeptiert und vor G0 zu entscheiden.

Siehe Widerspruch W-05 und Entscheidung OD-26.

---

## Bearbeitung

Ein Eintrag wird nicht gelöscht, sondern auf `geschlossen` gesetzt und mit der
auflösenden Quelle oder Entscheidung verknüpft.
