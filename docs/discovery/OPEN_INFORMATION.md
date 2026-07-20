# Open Information — fehlende Eingangsinformation

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Überarbeitet in | CBP-WP-003 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

Dieses Dokument verzeichnet fehlende oder nicht zugängliche
**Eingangsinformation**.

---

## OI-01 — Zwei verbindliche Quellen lagen zunächst nicht vor

**Schweregrad:** hoch · **Status:** **GESCHLOSSEN** (2026-07-20, CBP-WP-002)

Beide Originalquellen wurden gelesen und abgeglichen, die Provenienz der
A6-Textfassung zur A4-PDF ist dokumentiert, keine ungeklärte inhaltliche
Abweichung. Vollständig in
[SOURCE_RECONCILIATION.md](SOURCE_RECONCILIATION.md).

**Verbleibende Einschränkung:** Der PDF-Fließtext war lokal nicht extrahierbar;
eine visuelle Detailprüfung wird nicht behauptet. Erfasst als R-22, R-23.

---

## OI-02 — Herkunft und Rang der Kernprinzipien

**Schweregrad:** mittel · **Status:** teilweise aufgelöst · **Adressat:** Human Maintainer

Inhaltliche Herkunft geklärt (20 bestätigte Übereinstimmungen). **Offen bleibt
der formale Rang** — die Prinzipien tragen A2 und sind nicht als ADR
ausgefertigt. Weiterverfolgt als OD-03 und G0-Kriterium F-3.

---

## OI-03 — Definition der Context Budgets B0–B4

**Schweregrad:** mittel · **Status:** **GESCHLOSSEN** (2026-07-20, CBP-WP-002)

Definiert in [../architecture/CONTEXT_BUDGETS.md](../architecture/CONTEXT_BUDGETS.md).
Kalibrierung der Token-Richtwerte als OD-02b offen.

---

## OI-04 — Gate-Kriterien für G0

**Schweregrad:** mittel · **Status:** **GESCHLOSSEN** (2026-07-20, CBP-WP-002),
**überarbeitet in CBP-WP-003**

47 Kriterien liegen vor, seit CBP-WP-003 dreistufig klassifiziert in Core
Required (25), Deployment Required (16) und Conditional (6).

**Gate-Status weiterhin NOT PASSED.**

---

## OI-05 — Zielumgebung nicht verifiziert

**Schweregrad:** niedrig · **Status:** **umklassifiziert** · **Adressat:** Human Maintainer

Das Betriebsprofil ist entschieden: Proxmox-VM mit dedizierter Linux-VM
(D-015). Die konkreten Werte — Version, CPU, RAM, Speicher, Storage — sind
**bewusst nicht erhoben** worden und nun **Deployment Required**.

Sie verhindern den allgemeinen Scope Lock nicht mehr, sondern die spätere
Installation. Zuständig ist ein noch zu definierendes
Deployment-Readiness-Gate (OD-33).

---

## OI-06 — Benchmarkfragen noch nicht formuliert

**Schweregrad:** **hoch** · **Status:** offen · **Adressat:** Nova + Human Maintainer

Es existiert **keine einzige** der geforderten mindestens 30 Benchmarkfragen.
Ohne sie ist Erfolgskriterium 2 der Projektübergabe §16 nicht prüfbar, und
„deutlich weniger Dateien" sowie „deutlich weniger Kontext" bleiben
unquantifiziert.

**Nach dem Intake ist dies der größte zusammenhängende G0-Blocker:** sechs der
25 Core-Required-Kriterien (G-1 bis G-6) hängen daran.

Der Intake hat die Voraussetzung teilweise geschaffen — die Quellenarten sind
bekannt (HDI A3). Die **Größenordnung** des Bestands (D-2) ist es nicht; sie
wurde bewusst nicht erhoben. Für die Fragenformulierung dürfte das genügen, für
die Kalibrierung der Metriken nicht.

Schweregrad von mittel auf **hoch** angehoben.

---

## OI-07 — Repository-Struktur nicht freigegeben

**Schweregrad:** mittel · **Status:** offen · **Adressat:** Nova + Human Maintainer

Drei Strukturvorstellungen stehen nebeneinander: Projektübergabe §13 (`core/`,
`deployments/`, `docs/`, `examples/`), NDF v1.0.0 und die aktuelle Struktur aus
CBP-WP-001.

Die Abweichungen AB-03 bis AB-08 bleiben nur **vorläufig für den Bootstrap**
akzeptiert. Siehe W-05, OD-26, OD-29.

---

## OI-08 — Berechtigungsmodell nicht erhoben

**Schweregrad:** **hoch** · **Status:** offen · **Adressat:** Human Maintainer

*Neu in CBP-WP-003.*

Vier Core-Required-Kriterien sind unbeantwortet: erlaubte Repository-Zugriffe
(E-2), GitHub-Zugriffe (E-3), Berechtigungsstufe je Bereich (E-4) und
Freigabeverfahren (E-5).

Der überarbeitete Minimal-Fragebogen hat diesen Block bewusst nicht erhoben —
er war auf Betriebs-, Nutzungs-, Quellen-, Datenschutz-, Zugriffs- und
Funktionsprofil beschränkt. Das ist eine **bewusste Lücke des Intakes**, kein
Versäumnis des Human Maintainers.

Projektübergabe §10 verlangt, Berechtigungen **technisch** umzusetzen, nicht
nur über Promptregeln. Ohne Zuordnung der fünf Stufen bleibt R-25 kritisch
offen.

Erfasst als OD-32.

---

## OI-09 — Verfahren bei Secret in der Git-Historie

**Schweregrad:** **hoch** · **Status:** offen · **Adressat:** Human Maintainer

*Neu in CBP-WP-003.*

Der Intake hat das **Verbot** bestätigt: Secrets sind immer verboten in
Wissensbestand, Repository, Index, Embeddings, Wiki und Context Packs (HDI A4).

Der **Ablauf im Schadensfall** ist nicht festgelegt — was geschieht, wenn ein
Secret trotzdem in die Historie gelangt: Rotation, History-Rewrite, Meldeweg,
Zuständigkeit.

Ein Verbot ohne Schadensverfahren ist unvollständig: R-01 bleibt deshalb
„teilweise gemindert" statt geschlossen.

Kriterium D-8, Frage 4.8, Entscheidung OD-10.

---

## Bearbeitung

Ein Eintrag wird nicht gelöscht, sondern auf `geschlossen` gesetzt und mit der
auflösenden Quelle oder Entscheidung verknüpft.
