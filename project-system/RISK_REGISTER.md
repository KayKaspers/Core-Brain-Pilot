# Risk Register – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Überarbeitet in | CBP-WP-007 |
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
| R-01 | Secret gelangt in die Git-Historie und ist praktisch nicht mehr entfernbar | **hoch** | `.gitignore`; **Schadensverfahren jetzt definiert** (SECRET_INCIDENT_RESPONSE, 14 Schritte, Rotation vor Cleanup). Erkennung und Automatik fehlen | **verändert, teilweise gemindert** |
| R-02 | `confidential` oder `excluded-from-ai` gelangt in den Modellkontext | **hoch** | Datenschutzfilter TB-4, fail-closed. **Standardwert 5:** Übertragung an externe KI standardmäßig verweigert | **konkretisiert** |
| R-03 | Datenklassen werden nie konsequent vergeben; Filter laufen ins Leere | **hoch** | Klassenvergabe verpflichtend an TB-1, Vault Doctor. Vergabeverfahren offen (OD-08) | offen |
| R-04 | Prompt Injection aus ingestiertem Material steuert einen Agenten | **hoch** | Ingest ist Daten, nie Anweisung; Quarantäne TB-1. **Durch D-019 verstärkt:** PDF/Office nur über kontrollierte Pipeline | **konkretisiert** |
| R-05 | Inhalte werden an das Claude-Modell übertragen, obwohl ihre Klasse das nicht erlaubt | **hoch** | Datenschutzmatrix; **Standardwert 5** macht Verweigerung zum Normalzustand | **konkretisiert** |
| R-25 | Berechtigungen bestehen nur als Promptregel und nicht technisch | **hoch** | **Modell vollständig dokumentiert** (PERMISSION_MODEL, ADR-0004): 5 Aktionsklassen, 5 Durchsetzungsebenen, Default deny. **Technische Umsetzung existiert nicht** | **verändert, offen** |
| R-26 | Betrieb als Root oder direkt auf dem Proxmox-Host | **hoch** | Ausdrückliches Verbot in TRUST_BOUNDARIES | offen |
| R-27 | Pauschale GitHub-Schreibrechte oder allgemeiner Repository-Schreibzugriff | **hoch** | **Regel gesetzt:** Claude `forbidden` auf `github remote`, nur `draft` auf `git repository`; Push ausschließlich Human Maintainer. Technisch nicht durchgesetzt | **verändert, offen** |
| R-31 | Die Sperrwirkung von `excluded-from-ai` wird nie mit Testdaten geprüft | **hoch** | **Zwei synthetische Fixtures und 6 Datenschutzfragen angelegt**; Leakage ist als kritischer Fehler mit Zielwert 0 definiert. **Prüfung noch nicht durchgeführt** | **gemindert** |

## Wissensintegrität

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-06 | Abgeleitete Inhalte (A6) überschreiben kuratierte (A0–A5) | **hoch** | **ADR-0003:** Einbahnregel TB-3; nur ein autorisierter Schreibpfad nach kanonisch (COMPONENT_MODEL) | **gemindert** |
| R-07 | Indexverlust bedeutet Wissensverlust | **hoch** | **ADR-0003 angenommen**; Rebuild-Vertrag mit Inputs, Versionen, Verifikation und Tombstone-Weg in SYSTEM_ARCHITECTURE | **gemindert** |
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
| R-33 | Fehlerhafte Kennzahlen in Statusdokumenten führen zu falschen Gate-Einschätzungen | mittel | Fünfteilige **Zähl- und Statusregel** in COMPLIANCE_CHECK (CBP-WP-007); Summen gelten als `derived status data`. **Dokumentregel, keine technische Kontrolle** — der dritte Zählfehler trat in CBP-WP-006 auf und wurde erst in der Prüfphase gefunden | **gemindert, nicht geschlossen** |
| **R-34** | **Deployment-Required-Kriterien werden vertagt und dann vergessen** | **hoch** | Alle 16 bleiben als `open` erfasst; separates Deployment-Readiness-Gate zu definieren (OD-33). **Fail-closed:** ohne die Angaben wird nicht installiert | **neu, offen** |

## Betrieb

| ID | Risiko | Schwere | Gegenmaßnahme | Status |
| --- | --- | --- | --- | --- |
| R-19 | Bindung an Proxmox oder Compose sickert in die Architektur ein | mittel | **ADR-0001 angenommen**; fünf Profile beschrieben; Profil B ist der laufende Neutralitätsnachweis | **gemindert** |
| R-20 | Fehlende Restore-Evidenz — Sicherung existiert, Wiederherstellung nie geprobt | **hoch** | **Standardwert 10:** Backup muss vor produktivem Betrieb eingerichtet **und getestet** sein. Zielwerte weiterhin offen (F-4) | offen |
| R-21 | Retrieval-Qualität verschlechtert sich unbemerkt | mittel | **Benchmark entworfen** (Dataset **2.0.0**): 36 Fragen, 4 Metrikgruppen, Regressionsregeln bei 7 Systemänderungen. **Kein Lauf durchgeführt.** Auflage 3 der G0-Entscheidung; Backlogpunkt P7 | **gemindert, nicht geschlossen** |
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
| gemindert | **14** |
| konkretisiert | 4 |
| dokumentiert | 1 |
| teilweise gemindert | 1 |
| offen | **10** |

**Neu in CBP-WP-005:** keine.

**Verändert in CBP-WP-005:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| **R-21** | Benchmark entworfen → `gemindert, nicht geschlossen` | Dataset 1.0.0, 36 Fragen, Metrikrubrik, Regressionsregeln |
| **R-31** | Zwei `excluded-from-ai`-Fixtures und 6 Datenschutzfragen angelegt → `gemindert` | Benchmark-Korpus, Leakage als kritischer Fehler mit Zielwert 0 |
| R-33 | Kennzahlen erneut skriptgestützt ausgezählt | Prüfungen in CBP-WP-005 |

> **R-21 ist ausdrücklich nicht geschlossen.** Ein entworfener Benchmark misst
> nichts. Ohne durchgeführten Lauf bleibt jede Qualitätsaussage unbelegt.
>
> **R-31 ist gemindert, nicht geschlossen.** Die Fixtures existieren, die
> Prüfung der Sperrwirkung steht aus.

**Verändert in CBP-WP-004:**

| ID | Änderung | Auslöser |
| --- | --- | --- |
| R-01 | Schadensverfahren definiert → `teilweise gemindert` | SECRET_INCIDENT_RESPONSE |
| R-06 | Einbahnregel und einziger Schreibpfad festgeschrieben → `gemindert` | ADR-0003, COMPONENT_MODEL |
| R-07 | Rebuild-Vertrag definiert → `gemindert` | ADR-0003, SYSTEM_ARCHITECTURE |
| R-19 | Deployment-Neutralität als ADR → `gemindert` | ADR-0001, DEPLOYMENT_PROFILES |
| R-25 | Berechtigungsmodell dokumentiert; **technisch weiterhin nicht durchgesetzt** | ADR-0004, PERMISSION_MODEL |
| R-27 | Zugriffsregeln gesetzt; **technisch weiterhin nicht durchgesetzt** | PERMISSION_MODEL |
| R-34 | DRC eingeführt → `gemindert` | ADR-0005, DEPLOYMENT_READINESS_CHECK |

**Kein Risiko wurde geschlossen, weil ein Dokument entstanden ist.** R-25 und
R-27 bleiben ausdrücklich **offen**: ein Berechtigungsmodell auf Papier ist
keine Zugriffskontrolle. R-01 bleibt `teilweise gemindert`, weil Erkennung und
technische Unterstützung fehlen. Der Nachweis der Wirksamkeit gehört in spätere
Gates.

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
