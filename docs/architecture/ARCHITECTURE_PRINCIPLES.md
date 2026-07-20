# Architecture Principles — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Status | Verbindliche Kernprinzipien, noch nicht implementiert |
| Autoritaetsklasse | A2 |
| Stand | 2026-07-20 |

Die folgenden 16 Prinzipien sind **verbindlich**. Sie beschreiben, wie das
System gebaut werden soll — nicht, wie es heute ist. Kein Prinzip ist
implementiert.

---

## 1. Kanonischer Markdown-Wissensbestand

Der Wissensbestand liegt als Markdown vor. Markdown ist das kanonische Format,
nicht ein Exportziel. Jedes andere Format ist Ableitung.

## 2. Git-Historie fuer kuratierte Inhalte

Kuratierte Inhalte stehen unter Git-Versionierung. Die Historie ist Teil der
Wahrheit: wer wann was geaendert hat, ist nachvollziehbar.

## 3. Reproduzierbare abgeleitete Daten

Index, Cache, Embeddings, Graph und Web-UI-Zustand sind vollstaendig aus dem
kanonischen Bestand reproduzierbar. Sie werden nicht versioniert und sind nie
autoritativ.

## 4. Deterministischer Quellenindex

Gleicher Eingangszustand ergibt gleichen Index. Die Indexierung enthaelt keine
nichtdeterministischen Bestandteile, die das Ergebnis verschieben.

## 5. Lokale Hybrid-Suche

Volltext- und semantische Suche laufen **lokal**. Es besteht keine
Notwendigkeit, Wissensbestand an externe Dienste zu senden.

## 6. Brain-First-Retrieval

Die Suche beginnt im kuratierten Projektgedaechtnis, nicht im Rohbestand.
Kuratiertes, verdichtetes Wissen hat Vorrang vor unverarbeitetem Material.

## 7. A0–A6-Autoritaetsmodell

Jede Wissenseinheit traegt eine Autoritaetsklasse.

| Klasse | Quelle |
| --- | --- |
| A0 | Ausdruecklicher Human-Maintainer-Beschluss |
| A1 | Release, Tag oder angenommener ADR |
| A2 | Formeller Projektstatus oder Work-Package-Queue |
| A3 | Freigegebene Roadmap oder Gate-Dokumentation |
| A4 | README und erlaeuternde Dokumentation |
| A5 | Freigegebene Projektchat-Uebergabe |
| A6 | Automatisch abgeleitete Zusammenfassung oder Wiki-Inhalt |

**A6 darf A0 bis A5 niemals automatisch ueberschreiben.**

## 8. Datenklassen und technische Datenschutzregeln

Fuenf Datenklassen steuern, was wohin fliessen darf. Die Durchsetzung ist
technisch, nicht nur organisatorisch. Siehe
[docs/privacy/DATA_CLASSIFICATION.md](../privacy/DATA_CLASSIFICATION.md).

## 9. Context Budgets B0–B4

Retrieval liefert nicht "so viel wie moeglich", sondern innerhalb eines
definierten Budgets. Das Budget ist ein Eingabeparameter, kein Nachgedanke.

> **Abgrenzung:** B0–B4 sind ein **Core-Brain-Pilot-Produktkonzept** fuer
> Retrieval-Umfang. Sie sind **nicht** identisch mit der NDF Context Economy
> (fuenf Kontextschichten, Prompt Modes Full/Standard/Short). Siehe
> [docs/ndf/ADOPTION_NOTES.md](../ndf/ADOPTION_NOTES.md).

## 10. Reproduzierbare Context Packs

Ein Context Pack ist bei gleichem Eingangszustand, gleicher Anfrage und
gleichem Budget reproduzierbar. Ohne Reproduzierbarkeit ist ein Agentenlauf
nicht nachvollziehbar.

## 11. Erklaerbarer Retrieval-Trace

Zu jedem Ergebnis ist nachvollziehbar: welche Quellen betrachtet, welche
Filter angewandt, welche Treffer aus welchem Grund verworfen wurden.

## 12. Menschlich kontrollierte Konfliktaufloesung

Widersprueche zwischen Quellen werden **nicht** automatisch aufgeloest. Sie
landen in einer Konflikt-Queue und warten auf eine menschliche Entscheidung.

## 13. Private Mehrgeraete-Nutzung

Ein Human Maintainer, mehrere Geraete einschliesslich mobil. Kein
Mehrmandantenbetrieb in Phase 0.

## 14. Deployment-neutrale Architektur

Proxmox und Docker Compose sind Betriebsentscheidungen, keine
Architekturbindungen. Kein Kernbestandteil darf eine Laufzeitumgebung
voraussetzen.

## 15. Austauschbare Suche und Web-UI

Suchmaschine und Web-UI sind ersetzbare Komponenten hinter stabilen Grenzen.
Ein Wechsel darf den kanonischen Bestand nicht beruehren.

## 16. Backup-, Restore- und Rebuild-Faehigkeit

Drei unterscheidbare Faehigkeiten:

| Faehigkeit | Bedeutung |
| --- | --- |
| Backup | Kanonischen Bestand sichern |
| Restore | Kanonischen Bestand wiederherstellen |
| Rebuild | Abgeleitete Daten aus dem kanonischen Bestand neu erzeugen |

**Invariante:** Der Verlust von Index, Cache, Embeddings, Graph oder Web-UI
verursacht keinen Wissensverlust.

---

## Prinzipienkonflikte

Prinzipien koennen in Spannung stehen — etwa 5 (lokale Suche) gegen
Antwortqualitaet, oder 9 (Budget) gegen 11 (Trace-Vollstaendigkeit). Solche
Konflikte werden **nicht** vom Agent entschieden, sondern als ADR in
[docs/decisions/](../decisions/README.md) vorgelegt.
