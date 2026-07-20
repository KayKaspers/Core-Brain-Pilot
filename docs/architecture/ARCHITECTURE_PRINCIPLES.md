# Architecture Principles — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Überarbeitet in | CBP-WP-002 |
| Autoritätsklasse | **A2** |
| Stand | 2026-07-20 |

Die folgenden 16 Prinzipien beschreiben, wie das System gebaut werden soll —
nicht, wie es heute ist. **Kein Prinzip ist implementiert.**

> **Zum Rang.** Die Prinzipien tragen **A2**. Der Quellenabgleich in
> CBP-WP-002 hat sie inhaltlich gegen die A5-Projektübergabe bestätigt; ihre
> formale Bindung durch einen ADR (A1) steht aus. Bis dahin sind sie
> Arbeitsgrundlage, nicht unveränderliche Festlegung. Siehe OD-03.

---

## 1. Kanonischer Markdown-Wissensbestand

Der Wissensbestand liegt als Markdown vor. Markdown ist das kanonische Format,
nicht ein Exportziel. Jedes andere Format ist Ableitung.

*Quelle: Bauanleitung, Seite 6; Projektübergabe §5.*

## 2. Git-Historie für kuratierte Inhalte

Kuratierte Inhalte stehen unter Git-Versionierung. Die Historie ist Teil der
Wahrheit: wer wann was geändert hat, ist nachvollziehbar.

## 3. Reproduzierbare abgeleitete Daten

Index, Cache, Embeddings, Graph und Web-UI-Zustand sind vollständig aus dem
kanonischen Bestand reproduzierbar. Sie werden nicht versioniert und sind nie
autoritativ.

## 4. Deterministischer Quellenindex

Gleicher Eingangszustand ergibt gleichen Index. Deterministische Verarbeitung
wird überall dort bevorzugt, wo kein Sprachverständnis nötig ist.

*Quelle: Bauanleitung, Seite 6.*

## 5. Lokale Hybrid-Suche — mit klarer Grenze

Volltext- und semantische Suche laufen **lokal**. Index und Suchmodelle werden
serverseitig und selbst gehostet betrieben.

> **Wichtige Klarstellung.** Das bedeutet **nicht**, dass keine Inhalte das
> System verlassen. Claude Code verwendet **keinen** vollständig lokalen
> Sprachmodellbetrieb. Ausgewählte Inhalte **werden** an das Claude-Modell
> übertragen.
>
> Lokal sind **Index und Suche**, nicht die Sprachverarbeitung.
>
> Genau daraus entsteht die Notwendigkeit der Datenklassifikation: weil
> Übertragung stattfindet, muss geregelt sein, **was** übertragen werden darf.

*Quelle: Bauanleitung, Seite 2; Projektübergabe §11. Korrigiert in CBP-WP-002
als Abschwächung Ü-01 — die vorherige Fassung behauptete fälschlich, es bestehe
keine Notwendigkeit, Wissensbestand an externe Dienste zu senden.*

## 6. Brain-First-Retrieval

Die Suche beginnt im kuratierten Projektgedächtnis, nicht im Rohbestand.

### Verbindliche Suchleiter

1. Projekt- oder Wissensindex lesen
2. Quellentyp und notwendige Autoritätsklasse bestimmen
3. Aktuellen Status prüfen, falls die Frage zeitabhängig ist
4. Wiki **nur als abgeleitete Orientierung** prüfen
5. Suche auf relevante Collection oder Projektgrenze beschränken
6. Kandidaten zunächst über Titel, Pfad, Metadaten und Trefferabschnitt prüfen
7. Nur die kleinste ausreichende Zahl von Quellen öffnen
8. Nur relevante Abschnitte lesen
9. Fakten, Ableitungen, Empfehlungen und Unsicherheit trennen
10. Quellen und Revisionen im Ergebnis nennen

**Keine blinden Vollscans** ganzer Repositories oder Wissensbestände.

### Quellenzahlregel

```text
Normalfall:        eine Quelle
erweiterter Fall:  höchstens drei Quellen
größerer Fall:     begründete Eskalation oder Aufteilung der Aufgabe
```

Die Bauanleitung (Seite 3) formuliert strenger — „genau eine beste Datei
öffnen". Projektübergabe §7 erweitert diese Regel ausdrücklich für Core Brain.

*Quelle: Projektübergabe §7; Bauanleitung, Seite 3. Ergänzt in CBP-WP-002 als
F-02.*

## 7. A0–A6-Autoritätsmodell

Jede Wissenseinheit trägt eine Autoritätsklasse.

| Klasse | Quelle |
| --- | --- |
| A0 | Ausdrücklicher Human-Maintainer-Beschluss |
| A1 | Release, Tag oder angenommener ADR |
| A2 | Formeller Projektstatus oder Work-Package-Queue |
| A3 | Freigegebene Roadmap oder Gate-Dokumentation |
| A4 | README und erläuternde Dokumentation |
| A5 | Freigegebene Projektchat-Übergabe |
| A6 | Automatisch abgeleitete Zusammenfassung oder Wiki-Inhalt |

**A6 darf A0 bis A5 niemals automatisch überschreiben.**

### Pflichtmetadaten abgeleiteter Aussagen

Jede abgeleitete Aussage führt mindestens:

1. Quellpfad
2. Quellentyp
3. Revision oder Prüfzeitpunkt
4. Autoritätsklasse
5. Aktualitätsstatus
6. Verifikationsstatus
7. Mögliche Konfliktreferenzen

*Quelle: Projektübergabe §6. Ergänzt in CBP-WP-002 als F-03.*

## 8. Datenklassen und technische Datenschutzregeln

Fünf Datenklassen steuern, was wohin fließen darf. Die Durchsetzung ist
technisch, nicht nur organisatorisch. Siehe
[../privacy/DATA_CLASSIFICATION.md](../privacy/DATA_CLASSIFICATION.md).

## 9. Context Budgets B0–B4

Retrieval liefert nicht „so viel wie möglich", sondern innerhalb eines
definierten Budgets. Das Budget ist ein Eingabeparameter, kein Nachgedanke.

Vollständig definiert in [CONTEXT_BUDGETS.md](CONTEXT_BUDGETS.md).

> **Abgrenzung:** B0–B4 sind ein **Core-Brain-Pilot-Produktkonzept** für
> Retrieval-Umfang und **nicht** identisch mit den NDF Prompt Modes
> (Full/Standard/Short). „Lean" ist ausschließlich der Name von B1.

## 10. Reproduzierbare Context Packs

Ein Context Pack ist bei gleichem Eingangszustand, gleicher Anfrage und
gleichem Budget reproduzierbar. Ohne Reproduzierbarkeit ist ein Agentenlauf
nicht nachvollziehbar.

## 11. Erklärbarer Retrieval-Trace

Zu jedem Ergebnis ist nachvollziehbar: welche Quellen betrachtet, welche Filter
angewandt, welche Treffer aus welchem Grund verworfen wurden.

**Jede Behauptung benötigt einen Prüfpunkt.**

*Quelle: Bauanleitung, Seite 6.*

## 12. Menschlich kontrollierte Konfliktauflösung

Widersprüche werden **nicht** automatisch aufgelöst. Sie landen in einer
Konflikt-Queue und warten auf eine menschliche Entscheidung.

### Widerspruchs-Workflow

1. Der Mensch entscheidet, was gilt:
   - alter Stand ist veraltet,
   - beide Aussagen stimmen in unterschiedlichem Kontext,
   - die neue Information ist falsch,
   - der Konflikt bleibt bewusst offen.
2. Die widersprüchliche Quelle wird **korrigiert**, nicht nur der Warnhinweis
   entfernt.
3. Danach wird das Wiki aktualisiert und die Entscheidung protokolliert.

Ein sichtbarer Widerspruch kann zu einem konkreten Arbeitsauftrag werden.

*Quelle: Bauanleitung, Seite 4.*

## 13. Private Mehrgeräte-Nutzung

Ein Human Maintainer, mehrere Geräte einschließlich mobil. Kein
Mehrmandantenbetrieb in Phase 0.

## 14. Deployment-neutrale Architektur

Proxmox und Docker Compose sind Betriebsentscheidungen, keine
Architekturbindungen. Kein Kernbestandteil darf eine Laufzeitumgebung
voraussetzen. Fünf Referenzprofile A bis E sind in
[PROJECT_DEFINITION.md](PROJECT_DEFINITION.md) beschrieben.

## 15. Austauschbare Suche und Web-UI

Suchmaschine und Web-UI sind ersetzbare Komponenten hinter stabilen Grenzen.
Ein Wechsel darf den kanonischen Bestand nicht berühren.

Keine Bindung an einen einzelnen Suchanbieter, eine einzelne Oberfläche oder
einen einzelnen VPN-Anbieter.

*Quelle: Projektübergabe §13.*

## 16. Backup-, Restore- und Rebuild-Fähigkeit

Drei unterscheidbare Fähigkeiten:

| Fähigkeit | Bedeutung |
| --- | --- |
| Backup | Kanonischen Bestand sichern |
| Restore | Kanonischen Bestand wiederherstellen |
| Rebuild | Abgeleitete Daten aus dem kanonischen Bestand neu erzeugen |

**Invariante:** Der Verlust von Index, Cache, Embeddings, Graph oder Web-UI
verursacht keinen Wissensverlust.

---

## Bauprozess für größere Bestandteile

Sechs Schritte, aus Bauanleitung, Seite 6:

```text
1. Datenbasis ordnen
2. Brainstorming
3. Spezifikation
4. Plan
5. Bauen in kleinen, prüfbaren Aufgaben
6. Praxistest gegen den bisherigen Ablauf
```

Kernlektionen derselben Seite: Der Mensch kuratiert, entscheidet und nimmt ab.
Referenzen sind besser als unklare Beschreibungen. Kleine Schritte mit
Zwischenabnahme. Erst entscheiden, dann bauen. Abgeleitete Ansichten müssen
ersetzbar sein.

*Ergänzt in CBP-WP-002 als F-15.*

## Prinzipienkonflikte

Prinzipien können in Spannung stehen — etwa 5 (lokale Suche) gegen
Antwortqualität, oder 9 (Budget) gegen 11 (Trace-Vollständigkeit). Solche
Konflikte werden **nicht** vom Agent entschieden, sondern als ADR in
[../decisions/](../decisions/README.md) vorgelegt.
