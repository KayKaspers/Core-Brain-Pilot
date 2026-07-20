# Open Information — fehlende Eingangsinformation

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-001 |
| Stand | 2026-07-20 |

Waehrend [DISCOVERY_QUESTIONS.md](DISCOVERY_QUESTIONS.md) offene
**Entscheidungen** sammelt, verzeichnet dieses Dokument fehlende oder nicht
zugaengliche **Eingangsinformation**.

---

## OI-01 — Zwei verbindliche Quellen lagen nicht vor

**Schweregrad:** hoch · **Status:** offen · **Adressat:** Human Maintainer

CBP-WP-001 nennt vier verbindliche Grundlagen:

| # | Quelle | Verfuegbar |
| --- | --- | --- |
| 1 | Projektanweisungen dieses Claude-Projekts | **ja** |
| 2 | Projektwissen: Core-Brain-Uebergabe | **nein** |
| 3 | Projektwissen: Second-Brain-Bauanleitung | **nein** |
| 4 | Nova Development Framework v1.0.0 | **ja** (oeffentlich abgerufen) |

Die Quellen 2 und 3 waren dem Implementation Agent in der Ausfuehrungssitzung
**nicht zugaenglich**. Als Projektwissen hinterlegte Dateien wurden nicht in
den Sitzungskontext gereicht, und das Arbeitsverzeichnis enthielt sie nicht.

**Wie damit umgegangen wurde:** Das dokumentarische Fundament wurde aus dem
Wortlaut von CBP-WP-001 abgeleitet. Das Work Package traegt Projektdefinition,
Kernprinzipien, Datenklassen und den vollstaendigen Capability-Katalog
ausformuliert in sich; diese Substanz war ausreichend, um die geforderten
Dokumente widerspruchsfrei zu erzeugen.

**Was daraus folgt:** Detailwissen aus den Quellen 2 und 3, das ueber den
Wortlaut des Work Packages hinausgeht, ist **nicht** eingeflossen. Es wurde
nichts erfunden, um die Luecke zu fuellen — fehlende Information steht als
offene Frage in [DISCOVERY_QUESTIONS.md](DISCOVERY_QUESTIONS.md).

**Empfohlene Aufloesung:** Vor Gate G0 die beiden Dokumente entweder in das
Repository aufnehmen oder einem Folge-Work-Package als Kontext beilegen, und
das hier erzeugte Fundament gegen sie abgleichen.

---

## OI-02 — Herkunft und Rang der Kernprinzipien

**Schweregrad:** mittel · **Status:** offen · **Adressat:** Nova

Die 16 Kernprinzipien und die 29 Capabilities stammen aus dem Wortlaut von
CBP-WP-001. Ob sie dort eine bereits getroffene A0-Entscheidung wiedergeben
oder einen Vorschlag zur Pruefung an G0 darstellen, ist nicht ausgewiesen.

Sie wurden vorlaeufig als **A2** gefuehrt. Sollen sie bindend sein, ist ein ADR
erforderlich (A1) oder ein ausdruecklicher Beschluss (A0).

---

## OI-03 — Definition der Context Budgets B0–B4

**Schweregrad:** mittel · **Status:** offen · **Adressat:** Nova

B0–B4 sind als Kernprinzip gesetzt, aber inhaltlich nicht definiert. Unbekannt
sind Masseinheit, Schwellenwerte und Zuordnung zu Anwendungsfaellen.

Abgrenzung dokumentiert in [../ndf/ADOPTION_NOTES.md](../ndf/ADOPTION_NOTES.md).
Siehe auch Q-18.

---

## OI-04 — Gate-Kriterien fuer G0 nicht definiert

**Schweregrad:** mittel · **Status:** offen · **Adressat:** Nova

Das naechste Gate ist als **G0 – Discovery and Scope Lock** benannt. Es
existiert keine Kriterienliste, anhand derer G0 als bestanden gilt.

Ohne Kriterien ist der Scope Lock nicht pruefbar. Siehe Q-31.

---

## OI-05 — Zielumgebung nicht verifiziert

**Schweregrad:** niedrig · **Status:** offen · **Adressat:** Human Maintainer

Proxmox als Referenzplattform und eine dedizierte Linux-VM als spaetere
Laufzeit sind dokumentiert, aber nicht verifiziert. In Phase 0 wurde
bewusst **keine** Umgebungspruefung durchgefuehrt: das haette Betriebsarbeit
vor dem Scope Lock bedeutet.

---

## Bearbeitung

Ein Eintrag wird nicht geloescht, sondern auf `geschlossen` gesetzt und mit der
aufloesenden Quelle oder Entscheidung verknuepft.
