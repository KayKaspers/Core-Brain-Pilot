# Component Model — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-004 |
| Autoritätsklasse | A2 |
| Status | **Logisches Modell, nicht implementiert** |
| Stand | 2026-07-20 |

Logische Komponenten mit ihren Vertrauensgrenzen. Keine Implementierung, keine
Produktnamen.

---

## Grundregel

> **Nur ein ausdrücklich autorisierter Schreibpfad darf kanonische Inhalte
> verändern:** die Freigabe im Review- und Approval-Workflow, ausgelöst durch
> eine menschliche Entscheidung.
>
> **Suchdienst, Web-UI, Indexer und externe Agenten dürfen kanonische Quellen
> nicht direkt verändern** — unter keinen Umständen, auch nicht „nur zum
> Korrigieren".

Alles andere schreibt entweder in die Quarantäne oder in die abgeleitete
Schicht.

## Übersicht der Schreibrechte

```text
                    darf canonical schreiben?
Review/Approval ─────────── JA (einziger Pfad, nach Human Approval)
Source Registry ─────────── JA, aber nur über Review/Approval
Ingest Quarantine ───────── NEIN  (schreibt nur Quarantäne)
Security Scanner ────────── NEIN  (nur Befunde)
Indexer ─────────────────── NEIN  (nur derived)
Search Provider Adapter ─── NEIN  (liest derived)
Retrieval Policy Gateway ── NEIN  (liest, filtert, protokolliert)
Context Pack Compiler ───── NEIN  (nur derived)
Review Queue ────────────── NEIN  (nur eigener Zustand)
Audit Service ───────────── NEIN  (nur derived, append-only)
Web-UI Adapter ──────────── NEIN  (stellt Anträge)
Read-only MCP/API Adapter ─ NEIN  (liest ausschließlich)
Backup/Restore Adapter ──── nur bei Restore, ausdrücklich freigegeben
Evaluation Runner ───────── NEIN  (nur derived)
```

---

## 1 — Canonical Store

| Feld | Wert |
| --- | --- |
| **Zweck** | Hält die einzige Wahrheitsquelle: freigegebene Markdown-Quellen, Entscheidungen, Handoffs, bestätigte Statusinformationen, Konfigurationen und Regeln |
| **Dateneigentum** | Kanonische Inhalte |
| Darf canonical lesen | **ja** |
| Darf canonical schreiben | **ja**, aber ausschließlich auf Anweisung des Review-/Approval-Workflows |
| Darf derived schreiben | nein |
| Darf externe KI aufrufen | **nein** |
| Benötigt Human Approval | **ja**, für jede Änderung |
| **Ausfallauswirkung** | **Kritisch.** Ohne Canonical Store gibt es kein Wissen |
| **Wiederherstellungsweg** | Restore aus Backup; Git-Historie als zusätzliche Sicherung |

## 2 — Source Registry

| Feld | Wert |
| --- | --- |
| **Zweck** | Verzeichnis aller Quellen mit stabiler Source-ID, Content Hash, Datenklasse, Autoritätsklasse, Owner, Revision, Aktualitäts- und Verifikationsstatus |
| **Dateneigentum** | Quellenmetadaten (kanonisch) |
| Darf canonical lesen | ja |
| Darf canonical schreiben | ja, **nur über den Freigabepfad** |
| Darf derived schreiben | nein |
| Darf externe KI aufrufen | nein |
| Benötigt Human Approval | **ja**, bei Aufnahme und Klassenänderung |
| **Ausfallauswirkung** | Hoch. Ohne Registry ist keine Filterung möglich — fail-closed bedeutet: es wird nichts ausgeliefert |
| **Wiederherstellungsweg** | Restore; Registry ist kanonisch und damit gesichert |

## 3 — Ingest Quarantine

| Feld | Wert |
| --- | --- |
| **Zweck** | Nimmt externes Material auf, bevor es geprüft ist (TB-1). Einziger Eingang für Nicht-Markdown-Quellen (D-019) |
| **Dateneigentum** | Quarantänebestand, **nicht kanonisch** |
| Darf canonical lesen | nur Metadaten für Abgleich |
| Darf canonical schreiben | **nein** |
| Darf derived schreiben | nein |
| Darf externe KI aufrufen | **nein** — Quarantänematerial ist unvertrauenswürdig |
| Benötigt Human Approval | **ja**, für die Promotion nach kanonisch |
| **Ausfallauswirkung** | Mittel. Kein Neueingang; Bestand bleibt nutzbar |
| **Wiederherstellungsweg** | Erneuter Ingest aus der Ursprungsquelle |

**Prompt-Injection-Regel:** Inhalte in der Quarantäne sind **Daten, niemals
Anweisungen**. Kein Agent befolgt Instruktionen aus ingestiertem Material.

## 4 — Security Scanner

| Feld | Wert |
| --- | --- |
| **Zweck** | Secret- und PII-Prüfung an der Quarantänegrenze; Befunde melden |
| **Dateneigentum** | Prüfbefunde (derived) |
| Darf canonical lesen | ja, für periodische Nachprüfung |
| Darf canonical schreiben | **nein** |
| Darf derived schreiben | ja (Befunde) |
| Darf externe KI aufrufen | **nein** — ein Scanner, der Verdachtsmaterial an ein externes Modell schickt, wäre der Fehler, den er verhindern soll |
| Benötigt Human Approval | nein für Prüfung, **ja** für jede Folgemaßnahme |
| **Ausfallauswirkung** | **Hoch.** Ohne Scanner darf nichts promoviert werden — fail-closed |
| **Wiederherstellungsweg** | Neustart; erneute Prüfung des Quarantänebestands |

Ein Fund ist ein **Blocker**, kein Automatismus. Siehe
[../security/SECRET_INCIDENT_RESPONSE.md](../security/SECRET_INCIDENT_RESPONSE.md).

## 5 — Indexer

| Feld | Wert |
| --- | --- |
| **Zweck** | Deterministischer Aufbau des Quellenindex; inkrementelle Aktualisierung mit Tombstones |
| **Dateneigentum** | Index (derived) |
| Darf canonical lesen | **ja** |
| Darf canonical schreiben | **nein** |
| Darf derived schreiben | **ja** |
| Darf externe KI aufrufen | nein (lokale Modelle für Embeddings sind kein externer Aufruf) |
| Benötigt Human Approval | nein |
| **Ausfallauswirkung** | Mittel. Suche veraltet; **kein Wissensverlust** |
| **Wiederherstellungsweg** | **Rebuild** nach dem Rebuild-Vertrag |

Der Indexer schließt `secret` und `excluded-from-ai` **vor** der Verarbeitung
aus, nicht danach.

## 6 — Search Provider Adapter

| Feld | Wert |
| --- | --- |
| **Zweck** | Bindet eine konkrete Suchtechnologie an eine stabile interne Schnittstelle: Volltext, semantisch, hybrid, Reranking |
| **Dateneigentum** | keines |
| Darf canonical lesen | **nein** — liest ausschließlich den Index |
| Darf canonical schreiben | **nein** |
| Darf derived schreiben | nein (nur lesen) |
| Darf externe KI aufrufen | **nein** — Suche läuft lokal |
| Benötigt Human Approval | nein |
| **Ausfallauswirkung** | Mittel. Retrieval fällt aus; Bestand unberührt |
| **Wiederherstellungsweg** | Neustart oder **Austausch des Adapters** |
| **Austauschbarkeit** | **Hoch** — ausdrücklich vorgesehen. Keine Bindung an qmd (OD-25) |

## 7 — Retrieval Policy Gateway

| Feld | Wert |
| --- | --- |
| **Zweck** | Setzt TB-4 durch: Datenklasse, Quellenberechtigung, Autorität, Aktualität, Verifikation, Context Budget, externe KI-Übertragungsregel. Erzeugt den Retrieval Trace |
| **Dateneigentum** | Trace (derived) |
| Darf canonical lesen | ja, gefiltert |
| Darf canonical schreiben | **nein** |
| Darf derived schreiben | ja (Trace) |
| Darf externe KI aufrufen | **entscheidet darüber**, ruft aber nicht selbst auf |
| Benötigt Human Approval | nein für Filterung; **ja** für Ausnahmen — die es nicht gibt |
| **Ausfallauswirkung** | **Kritisch, aber sicher.** Fällt das Gateway aus, wird **nichts** ausgeliefert |
| **Wiederherstellungsweg** | Neustart; Zustand ist ableitbar |

**Fail-closed ohne Ausnahme.** Bei unbekannter Einstufung wird verweigert.
`secret` und `excluded-from-ai` passieren nie.

## 8 — Context Pack Compiler

| Feld | Wert |
| --- | --- |
| **Zweck** | Baut reproduzierbare Context Packs mit Quellenmanifest, Abschnittsreferenzen, Pack Hash, Ablaufzeit und Ausschlussgründen |
| **Dateneigentum** | Context Packs (derived, mit Nutzdaten) |
| Darf canonical lesen | ja, **nur was das Gateway freigegeben hat** |
| Darf canonical schreiben | **nein** |
| Darf derived schreiben | ja |
| Darf externe KI aufrufen | nein |
| Benötigt Human Approval | nein |
| **Ausfallauswirkung** | Mittel. Agentenarbeit stockt; Bestand unberührt |
| **Wiederherstellungsweg** | Neu erzeugen; Packs sind flüchtig |

Context Packs gehören **nicht** ins Repository.

## 9 — Review Queue

| Feld | Wert |
| --- | --- |
| **Zweck** | Führt Konflikte, Freigabekandidaten und Verifikationsaufgaben zur menschlichen Entscheidung |
| **Dateneigentum** | Queue-Zustand |
| Darf canonical lesen | ja |
| Darf canonical schreiben | **nein** — löst die Freigabe nur aus |
| Darf derived schreiben | ja (eigener Zustand) |
| Darf externe KI aufrufen | nein |
| Benötigt Human Approval | **ja** — das ist ihr Zweck |
| **Ausfallauswirkung** | Mittel. Keine Freigaben möglich; Lesebetrieb läuft weiter |
| **Wiederherstellungsweg** | Restore; offene Konflikte bleiben offen |

**Keine automatische Konfliktentscheidung** (D-022 des Sicherheitsmodells,
Projektübergabe §10). Ein Konflikt wartet, bis ein Mensch entscheidet.

## 10 — Audit Service

| Feld | Wert |
| --- | --- |
| **Zweck** | Protokolliert Freigaben, Klassenänderungen, Rebuilds, Retrieval-Entscheidungen und Vorfälle |
| **Dateneigentum** | Audit Log (derived, append-only) |
| Darf canonical lesen | ja, Metadaten |
| Darf canonical schreiben | **nein** |
| Darf derived schreiben | ja, **nur anhängend** |
| Darf externe KI aufrufen | nein |
| Benötigt Human Approval | nein |
| **Ausfallauswirkung** | Mittel. Nachvollziehbarkeit leidet; kein Wissensverlust |
| **Wiederherstellungsweg** | Restore; verlorene Einträge sind nicht rekonstruierbar |

Audit-Einträge dürfen **keine Secrets und keine Inhalte der Klassen
`confidential` oder `excluded-from-ai`** enthalten — nur Referenzen.

## 11 — Web-UI Adapter

| Feld | Wert |
| --- | --- |
| **Zweck** | Bindet eine austauschbare Oberfläche an die Core API |
| **Dateneigentum** | keines |
| Darf canonical lesen | ja, **über die Core API und das Gateway** |
| Darf canonical schreiben | **nein** |
| Darf derived schreiben | nein |
| Darf externe KI aufrufen | nein |
| Benötigt Human Approval | für jede schreibende Aktion, die sie beantragt |
| **Ausfallauswirkung** | **Niedrig.** CLI und API bleiben nutzbar |
| **Wiederherstellungsweg** | Neustart oder **Austausch** |
| **Austauschbarkeit** | **Hoch** — ausdrücklich vorgesehen |

Die Web-UI erhält **keine administrativen Hostrechte** und beginnt erst nach
funktionierendem Retrieval und Benchmark (D-024).

## 12 — Read-only MCP/API Adapter

| Feld | Wert |
| --- | --- |
| **Zweck** | Programmatischer **Lesezugriff** für spätere Clients |
| **Dateneigentum** | keines |
| Darf canonical lesen | ja, über das Gateway |
| Darf canonical schreiben | **nein — konstruktiv ausgeschlossen** |
| Darf derived schreiben | nein |
| Darf externe KI aufrufen | nein |
| Benötigt Human Approval | für die Freischaltung des Adapters |
| **Ausfallauswirkung** | Niedrig |
| **Wiederherstellungsweg** | Neustart |

> **Provenienzhinweis:** Diese Komponente stammt aus CBP-WP-001 (A2) und ist in
> keiner Originalquelle belegt (Ü-05). Projektübergabe §10 fordert lediglich
> „keine unkontrollierten MCP-Server". Sie bleibt **nicht Pilotumfang**.

## 13 — Backup and Restore Adapter

| Feld | Wert |
| --- | --- |
| **Zweck** | Sichert den kanonischen Bestand, stellt ihn wieder her, prüft Wiederherstellbarkeit |
| **Dateneigentum** | Backupbestand |
| Darf canonical lesen | **ja**, vollständig |
| Darf canonical schreiben | **nur beim Restore**, und nur nach ausdrücklicher Freigabe |
| Darf derived schreiben | optional |
| Darf externe KI aufrufen | **nein** |
| Benötigt Human Approval | **ja**, für jeden Restore |
| **Ausfallauswirkung** | **Hoch, aber verzögert.** Man merkt es erst, wenn man es braucht — R-20 |
| **Wiederherstellungsweg** | Sekundäres Backupziel; externe Kopie außerhalb des Hosts |

**Backup Storage ist für Web-UI, Suche und Agenten nicht beschreibbar.** Ein
Angreifer oder ein Fehler in diesen Komponenten darf die Sicherung nicht
erreichen.

## 14 — Evaluation Runner

| Feld | Wert |
| --- | --- |
| **Zweck** | Führt Benchmark und Regressionstests gegen den Retrieval-Pfad aus |
| **Dateneigentum** | Messergebnisse (derived) |
| Darf canonical lesen | ja, über das Gateway |
| Darf canonical schreiben | **nein** |
| Darf derived schreiben | ja |
| Darf externe KI aufrufen | **ja, kontrolliert** — für Baseline-Vergleiche, unter denselben Regeln wie jeder Retrieval-Pfad |
| Benötigt Human Approval | für Läufe mit externer Übertragung |
| **Ausfallauswirkung** | Niedrig im Betrieb, **hoch für die Qualitätsaussage** |
| **Wiederherstellungsweg** | Neustart; Ergebnisse neu erzeugen |

Der Benchmark existiert noch nicht (G-1 bis G-6 offen).

---

## Zusammenfassung Schreibrechte auf kanonisch

| Komponente | canonical schreiben |
| --- | --- |
| Review- und Approval-Workflow | **ja** — einziger Pfad, nach Human Approval |
| Source Registry | ja, ausschließlich über diesen Pfad |
| Backup/Restore Adapter | nur beim freigegebenen Restore |
| **Alle übrigen 11 Komponenten** | **nein** |

Diese Tabelle ist die praktische Fassung der Grundregel. Wird sie verletzt,
verliert die Trennung von kanonisch und abgeleitet ihren Sinn.

## Austauschbare Adapter

| Adapter | Austauschbarkeit | Bindung vermeiden an |
| --- | --- | --- |
| Search Provider | **hoch** | einen Suchanbieter |
| Web-UI | **hoch** | eine Oberflächentechnologie |
| Backup/Restore | mittel | eine Backupsoftware |
| MCP/API | hoch | ein Protokoll |
| Embedding-Modell | mittel | ein Modell — Wechsel erfordert Rebuild |

Ein Adapterwechsel darf den kanonischen Bestand **nicht berühren**.

## Status

**Nicht implementiert.** Keine dieser Komponenten existiert.
