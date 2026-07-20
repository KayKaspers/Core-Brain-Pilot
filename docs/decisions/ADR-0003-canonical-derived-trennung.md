# ADR-0003 — Strikte Trennung von kanonischen und abgeleiteten Daten

| Feld | Wert |
| --- | --- |
| Status | **accepted** |
| Datum | 2026-07-20 |
| Entscheider | Human Maintainer |
| Supersedes | — |
| Superseded by | — |
| Belegt durch | Projektübergabe §5 (A5), Bauanleitung Seite 6 (A4), D-005 |

## Kontext

Ein Wissenssystem, das Index, Embeddings, Cache, Graph und Oberfläche einsetzt,
erzeugt große Mengen abgeleiteter Daten. Ohne klare Trennung entsteht zwei
Gefahren: abgeleitete Inhalte werden als autoritativ behandelt (Risiko R-06),
und der Verlust einer Ableitung wird zum Wissensverlust (Risiko R-07).

Projektübergabe §5 formuliert die Invariante wörtlich: der Verlust eines
Indexes oder einer Oberfläche darf nicht zum Verlust des Wissens führen.

## Entscheidung

Kanonische und abgeleitete Daten werden **strikt getrennt**.

**Kanonisch:** freigegebene Markdown-Quellen, Projektentscheidungen, Handoffs,
bestätigte Statusinformationen, Konfigurationen und Regeln, manuell bestätigte
Wiki-Inhalte.

**Abgeleitet:** Kataloge, Suchindex, Embeddings, Cache, Graphdaten, automatisch
erzeugte Wiki-Entwürfe, Retrieval-Traces, temporäre Context Packs,
Visualisierungen.

Daraus folgen vier bindende Regeln:

1. **Einbahnstraße.** Kanonisch speist abgeleitet. Rückfluss ist ausgeschlossen
   (TB-3). Eine automatisch erzeugte Zusammenfassung (A6) überschreibt niemals
   kuratierte Inhalte (A0–A5).
2. **Abgeleitete Daten werden nicht versioniert.** Sie gehören nicht ins
   Repository und sind über `.gitignore` ausgeschlossen.
3. **Vollständige Reproduzierbarkeit.** Jede Ableitung ist aus dem kanonischen
   Bestand neu erzeugbar. Der Rebuild-Vertrag benennt Inputs, festzuhaltende
   Versionen, Verifikationsschritte und den Weg, gelöschte oder gesperrte
   Quellen zu entfernen.
4. **Nur ein autorisierter Schreibpfad** verändert kanonische Inhalte: die
   Freigabe im Review- und Approval-Workflow nach menschlicher Entscheidung.
   Suchdienst, Web-UI, Indexer und externe Agenten dürfen kanonische Quellen
   nicht direkt verändern.

## Alternativen

**Index als Primärspeicher.** Verworfen: verletzt die Invariante unmittelbar
und macht das System von einer Suchtechnologie abhängig.

**Abgeleitete Daten mitversionieren.** Verworfen: bläht die Historie, erzeugt
Konflikte ohne Erkenntniswert und verwischt genau die Grenze, um die es geht.

**Schreibrechte für den Indexer auf Metadaten.** Verworfen: „nur Metadaten" ist
der erste Schritt zur Aufweichung. Metadaten sind kanonisch.

## Konsequenzen

**Leichter:** Verlust der abgeleiteten Schicht ist folgenlos. Adapter und
Suchtechnologien sind austauschbar. Backup konzentriert sich auf einen klar
umrissenen Bestand.

**Schwerer:** Jede Ableitung braucht einen belastbaren Rebuild-Weg. Löschungen
müssen über Tombstones bis in Index, Embeddings, Cache und Context Packs
durchgereicht werden — eine Löschung an der Quelle allein genügt nicht.

**Geschlossene Türen:** Kein Feature darf Zustand ausschließlich in der
abgeleiteten Schicht halten.

## Bezug

Prinzipien 1, 3, 16 · G0-Kriterium **F-3** · Risiken R-06, R-07 · TB-3 ·
Rebuild-Vertrag in
[../architecture/SYSTEM_ARCHITECTURE.md](../architecture/SYSTEM_ARCHITECTURE.md)
