# Risk Register – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Überarbeitet in | CBP-WP-003 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

> **Ablageabweichung.** NDF v1.0.0 sieht `project-brain/RISKS.md` vor.
> Es existiert bewusst nur **eine** von beiden — AB-04.

## Bewertung

Schweregrad **hoch / mittel / niedrig** nach Schadenshöhe und Umkehrbarkeit.
Ein irreversibler Schaden ist mindestens **hoch**.

> **Grundsatz aus CBP-WP-003:** Kein Risiko wird geschlossen, weil eine
> **Absicht** genannt wurde. Eine technische Gegenmaßnahme gilt erst nach
> späterer Evidenz als umgesetzt.

## Sicherheit und Datenschutz

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-01 | Secret gelangt in die Git-Historie und ist praktisch nicht mehr entfernbar | **hoch** | `.gitignore`, keine Beispiel-Secrets, Secret-Prüfung beim Ingest. **Verfahren im Schadensfall weiterhin undefiniert** (OD-10, D-8) | teilweise gemindert |
| R-02 | `confidential` oder `excluded-from-ai` gelangt in den Modellkontext | **hoch** | Datenschutzfilter TB-4, fail-closed. **Standardwert 5:** Übertragung an externe KI standardmäßig verweigert | **konkretisiert** |
| R-03 | Datenklassen werden nie konsequent vergeben; Filter laufen ins Leere | **hoch** | Klassenvergabe verpflichtend an TB-1, Vault Doctor. Vergabeverfahren offen (OD-08) | offen |
| R-04 | Prompt Injection aus ingestiertem Material steuert einen Agenten | **hoch** | Ingest ist Daten, nie Anweisung; Quarantäne TB-1. **Durch D-019 verstärkt:** PDF/Office nur über kontrollierte Pipeline | **konkretisiert** |
| R-05 | Inhalte werden an das Claude-Modell übertragen, obwohl ihre Klasse das nicht erlaubt | **hoch** | Datenschutzmatrix; **Standardwert 5** macht Verweigerung zum Normalzustand | **konkretisiert** |
| R-25 | Berechtigungen bestehen nur als Promptregel und nicht technisch | **hoch** | Fünf Berechtigungsstufen dokumentiert. **Zuordnung je Bereich und Freigabeverfahren weiterhin offen** (OD-32, E-2 bis E-5) | **offen, kritisch** |
| R-26 | Betrieb als Root oder direkt auf dem Proxmox-Host | **hoch** | Ausdrückliches Verbot in TRUST_BOUNDARIES | offen |
| R-27 | Pauschale GitHub-Schreibrechte oder allgemeiner Repository-Schreibzugriff | **hoch** | Verbot dokumentiert. **Erlaubte Zugriffe nicht erhoben** (E-2, E-3) | **offen, kritisch** |
| **R-31** | **Die Sperrwirkung von `excluded-from-ai` wird nie mit Testdaten geprüft** | **hoch** | D-021 fordert die Prüfung ausdrücklich mit synthetischen oder unkritischen Testdaten | **neu, offen** |

## Wissensintegrität

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-06 | Abgeleitete Inhalte (A6) überschreiben kuratierte (A0–A5) | **hoch** | Autoritätsmodell, Einbahnregel TB-3 | offen |
| R-07 | Indexverlust bedeutet Wissensverlust | **hoch** | Trennung kanonisch/abgeleitet, Rebuild-Fähigkeit. **ADR fehlt** (F-3) | offen |
| R-08 | Widersprüche werden automatisch aufgelöst statt vorgelegt | mittel | Konflikt-Queue, menschliche Auflösung. **Standardwert 7** | gemindert |
| R-09 | Veraltetes Wissen wird als aktuell ausgeliefert | mittel | Aktualitätsfilter, Supersession | offen |
| R-10 | Nichtdeterministische Indexierung macht Ergebnisse unreproduzierbar | mittel | Determinismus als Akzeptanzkriterium | offen |
| R-11 | Paralleler Schreibzugriff mehrerer Geräte beschädigt den Bestand | mittel | Atomare Änderungen, Mehrschreiberschutz. **Durch D-018 entschärft:** Single-User im Pilot | **verändert** |
| R-22 | Source Drift — A6-Textfassung weicht von der A4-PDF ab | mittel | PDF bleibt Original; visuelle Prüfung nicht behauptet | dokumentiert |
| R-23 | Unvollständiger Quellenabgleich | mittel | Abgleich in SOURCE_RECONCILIATION nachvollziehbar | offen |
| **R-32** | **Nicht-Markdown-Quellen umgehen die Quarantäne und gelangen direkt in den kanonischen Bestand** | **hoch** | D-019 untersagt das ausdrücklich; Capability 5 wird Voraussetzung für PDF/Office | **neu, offen** |

## Projekt und Prozess

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-12 | Vorgezogene Implementierung präjudiziert offene Architekturentscheidungen | **hoch** | Sperrliste `DO_NOT_START.md`, Aufhebung nur per A0 | gemindert |
| R-13 | Scope Creep durch unpriorisierte Capabilities | **hoch** | Priorisierung P0/P1/P2/Deferred; **D-025 vertagt vier Funktionen ausdrücklich** | **gemindert** |
| R-14 | G0 ohne objektive Kriterien | mittel | 47 Kriterien, dreistufig klassifiziert | geschlossen |
| R-15 | Verbindliche Eingangsquellen liegen nicht vor | mittel | Beide Quellen abgeglichen | geschlossen |
| R-16 | Dokumentationsfundament driftet vom tatsächlichen Stand ab | mittel | Pflege in jedem Work Package | offen |
| R-17 | Abweichungen vom NDF wachsen unkontrolliert | niedrig | AB-03 bis AB-08 nur vorläufig akzeptiert | gemindert |
| R-24 | Verwechslung von NDF Prompt Mode und Context Budget | mittel | Ausdrückliche Abgrenzung; D-009 | gemindert |
| R-28 | Ein zweites Governance-System wird eingeführt | mittel | Superpowers nur als Referenz | gemindert |
| **R-33** | **Fehlerhafte Kennzahlen in Statusdokumenten führen zu falschen Gate-Einschätzungen** | mittel | Summen in CBP-WP-003 gegen die Einzeleinträge nachgezählt und korrigiert (47/45/38/56); künftig Auszählung statt Fortschreibung | **neu, gemindert** |
| **R-34** | **Deployment-Required-Kriterien werden vertagt und dann vergessen** | **hoch** | Alle 16 bleiben als `open` erfasst; separates Deployment-Readiness-Gate zu definieren (OD-33). **Fail-closed:** ohne die Angaben wird nicht installiert | **neu, offen** |

## Betrieb

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-19 | Bindung an Proxmox oder Compose sickert in die Architektur ein | mittel | **D-017 bestätigt Deployment-Neutralität ausdrücklich** | **gemindert** |
| R-20 | Fehlende Restore-Evidenz — Sicherung existiert, Wiederherstellung nie geprobt | **hoch** | **Standardwert 10:** Backup muss vor produktivem Betrieb eingerichtet **und getestet** sein. Zielwerte weiterhin offen (F-4) | offen |
| R-21 | Retrieval-Qualität verschlechtert sich unbemerkt | mittel | Benchmarks und Regressionstests; **keine der mindestens 30 Fragen formuliert** | **offen, kritisch** |
| R-29 | Produktive Synchronisation ohne Test-Vault führt zu Datenverlust | **hoch** | **D-025 vertagt native Obsidian-Nutzung**; Freigabe erst nach Test-Vault, Konflikt- und Restore-Prüfung | **gemindert** |
| R-30 | Datenschutzklassifikation ohne technische Durchsetzung | **hoch** | **D-021 macht daraus eine prüfbare Anforderung** — Sperrwirkung mit Testdaten nachzuweisen | **konkretisiert** |

## Zusammenfassung

| Schwere | Anzahl |
| --- | --- |
| hoch | 17 |
| mittel | 13 |
| niedrig | 2 |
| **Summe** | **32** |

| Status | Anzahl |
| --- | --- |
| geschlossen | 2 |
| gemindert | 9 |
| konkretisiert | 4 |
| dokumentiert | 1 |
| teilweise gemindert | 1 |
| offen | 15 |

**Neu in CBP-WP-003:** R-31 bis R-34.

**Verändert:** R-02, R-04, R-05, R-30 → `konkretisiert` durch A0-Entscheidungen;
R-11, R-13, R-19, R-29 → `gemindert`; R-25, R-27, R-21 als **kritisch offen**
hervorgehoben.

**Kein Risiko wurde geschlossen, weil eine Absicht genannt wurde.** D-021 etwa
verschärft R-30 zu einer prüfbaren Anforderung, schließt es aber nicht — der
Nachweis steht aus.

## Weiterhin kritisch

| ID | Warum |
| --- | --- |
| R-25 | Berechtigungen ohne technische Durchsetzung; Zuordnung nicht erhoben |
| R-27 | Erlaubte Repository- und GitHub-Zugriffe unbekannt |
| R-31 | Sperrwirkung von `excluded-from-ai` ungeprüft |
| R-32 | Quarantäne für Nicht-Markdown-Quellen existiert nicht |
| R-34 | 16 vertagte Deployment-Kriterien ohne zuständiges Gate |
| R-21 | Kein Benchmark, damit keine Qualitätsaussage möglich |

## Pflege

Ein Risiko wird nicht gelöscht, sondern auf `geschlossen` gesetzt und mit der
wirksamen Kontrolle verknüpft.
