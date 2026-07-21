# Source Registry Plan — deterministischer Quellenkatalog

| Feld | Wert |
| --- | --- |
| **Status** | **PROPOSED** — Modell, keine Implementierung |
| Stream | F5 · Backlogpunkt P5 |
| Erfasst in | CBP-WP-008 |
| Autoritätsklasse | A3 |
| Grundlage | **ADR-0003**, ADR-0006 |
| Abhängig von | **F2**, **F4** |
| Stand | 2026-07-21 |

Das Registry beantwortet: **Was gehört zum Bestand, woher stammt es, welche
Fassung ist gültig?** Es beantwortet **nicht**: *Was passt zu dieser Frage?*

---

## Registry ist kein Suchindex

Diese Trennung ist der Kern des Dokuments.

| | **Source Registry** | **Suchindex** |
| --- | --- | --- |
| Zweck | Bestandsverzeichnis | Auffindbarkeit |
| Klasse | **kanonisch** | **abgeleitet** |
| Enthält | Metadaten und Verweise | Chunks, Embeddings, Terme |
| Verlust bedeutet | **Wissensverlust** | nur Rechenzeit |
| Wiederherstellung | aus Backup | durch **Rebuild** |
| Versioniert | ja | **nie** |
| Autoritativ | **ja** | nie |
| Ablage | Operator Workspace | Runtime Data Area |

**Der Rebuild-Vertrag (ADR-0003) lautet:** Index, Cache, Embeddings und Context
Packs lassen sich aus kanonischem Bestand **plus Registry** vollständig neu
erzeugen. Das Registry gehört auf die kanonische Seite dieser Grenze — sonst
ist der Vertrag nicht erfüllbar.

**Regel R0:** Ein Feld, das aus dem Index rekonstruierbar wäre, gehört nicht
ins Registry. Ein Feld, ohne das ein Rebuild scheitert, gehört hinein.

## Canonical und Derived

| Seite | Gegenstand |
| --- | --- |
| **Canonical** | Quelle selbst, Registry-Eintrag, Tombstone, Freigabevermerk |
| **Derived** | Suchindex, Embeddings, Context Packs, Cache, `indexed_revision`, `last_indexed_at` |

Zwei Registry-Felder sind die begründete Ausnahme: `indexed_revision` und
`last_indexed_at` beschreiben abgeleiteten Zustand. Sie dienen ausschließlich
der Rebuild-Steuerung und dürfen **nie** als Beleg für Bestand oder Gültigkeit
herangezogen werden. Gehen sie verloren, ist die Folge ein vollständiger
Rebuild — kein Wissensverlust.

---

## Feldmodell — 24 Felder

| # | Feld | Typ | Bedeutung |
| --- | --- | --- | --- |
| 1 | `source_id` | Kennung | **Stabile ID der Wissenseinheit**, deploymentübergreifend |
| 2 | `mapping_id` | Kennung | Mapping, über das der Eintrag entstand |
| 3 | `slot_id` | Kennung | Zugehöriger Source Slot |
| 4 | `title` | Text | Sprechender Titel |
| 5 | `source_type` | Aufzählung | Entspricht `source_kind` des Slots |
| 6 | `owner` | Rolle | **Pflicht.** Verantwortung für Inhalt und Freigabe |
| 7 | `project` | Kennung | Fachliche Zuordnung |
| 8 | `collection` | Kennung | Logische Sammlung für Berechtigungen und Suche |
| 9 | `canonical_reference` | Referenz | **Verweis** auf den kanonischen Ort — nie ein Klartextpfad im Core Repository |
| 10 | `revision` | Kennung | Fassungsbezeichner |
| 11 | `content_hash` | Hash | Inhaltshash der aktuellen Fassung |
| 12 | `authority_class` | `A0`–`A6` | Wirksame Autorität |
| 13 | `data_class` | Aufzählung | `public`, `internal`, `confidential`, `excluded-from-ai`; **nie `secret`** |
| 14 | `ai_transfer_policy` | Aufzählung | `allowed`, `restricted`, `forbidden` |
| 15 | `verification_status` | Aufzählung | `unverified`, `verified`, `rejected` |
| 16 | `freshness_status` | Aufzählung | `current`, `aging`, `stale`, `unknown` |
| 17 | `valid_from` | Zeitpunkt | Beginn der Gültigkeit |
| 18 | `valid_until` | Zeitpunkt | Ende der Gültigkeit, sofern bekannt |
| 19 | `superseded_by` | Kennung | Nachfolgefassung, falls vorhanden |
| 20 | `tombstone_status` | Aufzählung | `none`, `tombstoned`; mit Pflichtbegründung |
| 21 | `indexed_revision` | Kennung | **Abgeleitet** — welche Revision im Index steht |
| 22 | `last_indexed_at` | Zeitpunkt | **Abgeleitet** — Zeitpunkt der letzten Indexierung |
| 23 | `approved_by` | Rolle | **Nur ein Mensch** |
| 24 | `approved_at` | Zeitpunkt | Zeitpunkt der Freigabe |

---

## Stabile Source-ID-Regeln

| # | Regel |
| --- | --- |
| **ID-1** | `source_id` ist **stabil über Ort und Zeit**. Verschieben ändert sie nicht |
| **ID-2** | `source_id` wird aus stabilen Merkmalen gebildet, **nie aus einem Dateipfad** |
| **ID-3** | Umbenennen erzeugt **keine** neue `source_id` |
| **ID-4** | Inhaltliche Ersetzung erzeugt eine **neue Revision**, keine neue `source_id` |
| **ID-5** | Eine `source_id` wird **nie wiederverwendet**, auch nach einem Tombstone nicht |
| **ID-6** | `source_id` ist deploymentübergreifend eindeutig |

> Die konkrete Bildungsvorschrift ist **OD-16** und bleibt offen. Hier steht,
> welche Eigenschaften sie erfüllen muss — nicht, wie sie lautet.

## Hash- und Revisionsregeln

| # | Regel |
| --- | --- |
| **H-1** | Der Hash bezieht sich auf den **kanonischen Inhalt**, nicht auf die Datei mit Metadaten |
| **H-2** | Gleicher Hash bedeutet gleiche Fassung — unabhängig vom Zeitstempel |
| **H-3** | Ein geänderter Hash **erzwingt** eine neue `revision` |
| **H-4** | Ein nicht bestimmbarer Hash verhindert die Aufnahme |
| **H-5** | Der Hash ist **kein** Vertraulichkeitsmerkmal und ersetzt keine Zugriffskontrolle |
| **REV-1** | Genau **eine** Revision je `source_id` ist gültig |
| **REV-2** | Die Vorgängerfassung wird über `superseded_by` verkettet, **nicht gelöscht** |
| **REV-3** | Die Revisionsstrategie folgt dem Slot (`revision_strategy`), nicht der Bequemlichkeit |

## Tombstone-Verhalten

| # | Regel |
| --- | --- |
| **T-1** | Entfernen erzeugt einen **Tombstone**, nie eine leere Lücke |
| **T-2** | Ein Tombstone trägt eine **Pflichtbegründung** |
| **T-3** | Ein Tombstone **erzwingt Derived Cleanup** — alle abgeleiteten Daten zu dieser `source_id` werden entfernt |
| **T-4** | **Ein Rebuild belebt einen getombsteinten Eintrag nie wieder** |
| **T-5** | Ein Tombstone ist selbst kanonisch und wird gesichert |
| **T-6** | Ein Secret-Fund führt zu Tombstone **plus** Incident-Verfahren — der Tombstone allein genügt nicht |

**T-4 ist der Punkt, an dem stille Wiederauferstehung entsteht:** Ein Rebuild,
der die Quelle erneut liest und den Tombstone ignoriert, macht die Löschung
rückgängig. **Das Registry, nicht die Quelle, entscheidet über Zugehörigkeit.**

## Änderungs- und Löschereignisse

| Ereignis | Registry | Derived |
| --- | --- | --- |
| Neue Quelle freigegeben | Eintrag angelegt, `approved_by`/`approved_at` gesetzt | Indexierung zulässig |
| Inhalt geändert | neue `revision`, neuer `content_hash` | **Reindex erforderlich** |
| Fassung ersetzt | `superseded_by` gesetzt | alte Fassung aus dem Index entfernt |
| Quelle widerrufen | `verification_status: rejected` | **Derived Cleanup** |
| Quelle gelöscht | `tombstone_status: tombstoned` | **Derived Cleanup** |
| Datenklasse verschärft | `data_class` aktualisiert | betroffene Context Packs verworfen |

**Jedes Lösch- oder Widerrufsereignis zieht Derived Cleanup nach sich.** Es
gibt keinen Zustand, in dem eine gelöschte Quelle im Index verbleibt — das ist
Abbruchbedingung **SB-08**.

## Index-Synchronisation und Rebuild-Vertrag

| # | Regel |
| --- | --- |
| **RB-1** | Der Index wird **ausschließlich** aus kanonischem Bestand **plus Registry** erzeugt |
| **RB-2** | Zwei Läufe bei unverändertem Input ergeben **denselben Indexzustand** |
| **RB-3** | Nur Einträge mit `approved` und ohne Tombstone werden indexiert |
| **RB-4** | Der Index ist jederzeit vollständig verwerfbar |
| **RB-5** | `indexed_revision` ungleich `revision` bedeutet **stale**, nicht ungültig |
| **RB-6** | Ein Rebuild erzeugt **keinen** neuen Registry-Eintrag |

**Reproduzierbarer INDEX:** Der Nachweis ist ein zweifacher Lauf mit
identischem Ergebnis — nicht die Aussage, dass er reproduzierbar sei.

## Auditnachweis

Protokolliert werden Anlage, Revisionswechsel, Freigabe, Widerruf, Tombstone,
Derived Cleanup und jeder abgelehnte Schreibversuch (KB-09). Auditeinträge sind
für die protokollierte Komponente **nicht löschbar**.

---

## Grenzen des Registry-Eintrags

Der Registry-Eintrag ist **Metadatenbestand**. Er darf:

| Verbot | Begründung |
| --- | --- |
| **Keine Quelle automatisch umschreiben** | Das Registry beschreibt, es verändert nicht |
| **Keine Autoritätsklasse aus einem Dateipfad ableiten** | Sonst würde Verschieben zur Beförderung — Slot-Regel 8 |
| **Keine Datenklasse aus Inhalt allein endgültig entscheiden** | Maschinelle Einschätzung ist ein Vorschlag; die Bestätigung ist menschlich |
| **Keine gelöschte Quelle im Index belassen** | T-3, SB-08 |

## Konsistenzregeln

| # | Regel | Verhalten bei Verletzung |
| --- | --- | --- |
| **C-1** | Kein Eintrag ohne `slot_id` und `mapping_id` | ungültig |
| **C-2** | Kein Eintrag ohne `owner`, `data_class`, `ai_transfer_policy` | ungültig |
| **C-3** | `excluded-from-ai` erzwingt `ai_transfer_policy: forbidden` | ungültig, **keine stille Korrektur** |
| **C-4** | `authority_class: A0` erfordert eine benennbare menschliche Entscheidung | ungültig |
| **C-5** | Registry-Autorität überschreibt nie die Dokumentautorität | Slot-Regel 8 gilt fort |
| **C-6** | Nur `approved` ohne Tombstone darf indexiert sein | Index wird verweigert |
| **C-7** | Unbekannter Wert | **Verweigerung**, keine Vorgabe |
| **C-8** | Registry-Verlust ist ein **Datenverlust**, kein Cache-Verlust | Wiederherstellung aus Backup, nicht durch Rebuild |

## Was offen bleibt

| Punkt | Register |
| --- | --- |
| Bildungsvorschrift der `source_id` | **OD-16** |
| Schnitt einer Wissenseinheit | **OD-15** |
| Verpflichtende Frontmatter-Felder | **OD-17** |
| Kriterien für `freshness_status` | offen |
| Speicherform des Registrys | offen — Deployment |

## Status

**PROPOSED.** Es existiert **kein Registry**, kein Eintrag, kein Index.

**R-10** (nichtdeterministische Indexierung) bleibt `offen`, **R-07**
(Indexverlust bedeutet Wissensverlust) bleibt `gemindert`: Der Rebuild-Vertrag
ist beschrieben, aber nie ausgeführt worden. Ein Vertrag ohne Durchlauf ist
eine Behauptung.

**Implementierung erlaubt: nein.**
