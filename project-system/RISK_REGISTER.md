# Risk Register – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Autoritaetsklasse | A2 |
| Stand | 2026-07-20 |

> **Ablageabweichung.** NDF v1.0.0 sieht `project-brain/RISKS.md` vor.
> CBP-WP-001 fordert diese Datei. Es existiert bewusst nur **eine** von beiden
> — siehe AB-04 in
> [../docs/ndf/ADOPTION_NOTES.md](../docs/ndf/ADOPTION_NOTES.md).

## Bewertung

Schweregrad **hoch / mittel / niedrig** nach Schadenshoehe und Umkehrbarkeit.
Ein irreversibler Schaden ist mindestens **hoch**, auch bei geringer
Eintrittswahrscheinlichkeit.

## Sicherheit und Datenschutz

| ID | Risiko | Schwere | Gegenmassnahme | Status |
| --- | --- | --- | --- | --- |
| R-01 | Secret gelangt in die Git-Historie und ist praktisch nicht mehr entfernbar | **hoch** | `.gitignore`, keine Beispiel-Secrets, Secret-Pruefung beim Ingest (Cap. 6), Verfahren OD-10 | teilweise gemindert |
| R-02 | `confidential` oder `excluded-from-ai` gelangt in den Modellkontext | **hoch** | Datenschutzfilter TB-4, fail-closed bei unbekannter Klasse | offen |
| R-03 | Datenklassen werden nie konsequent vergeben; Filter laufen ins Leere | **hoch** | Klassenvergabe verpflichtend an TB-1, Vault Doctor | offen |
| R-04 | Prompt Injection aus ingestiertem Material steuert einen Agenten | **hoch** | Ingest ist Daten, nie Anweisung; Quarantaene TB-1 | offen |
| R-05 | Externer Dienst erhaelt Wissensbestand entgegen der Absicht | mittel | Prinzip lokale Hybrid-Suche | offen |

## Wissensintegritaet

| ID | Risiko | Schwere | Gegenmassnahme | Status |
| --- | --- | --- | --- | --- |
| R-06 | Abgeleitete Inhalte (A6) ueberschreiben kuratierte (A0–A5) | **hoch** | Autoritaetsmodell, Einbahnregel TB-3 | offen |
| R-07 | Indexverlust bedeutet Wissensverlust, weil Kanonisches nur im Index lag | **hoch** | Trennung kanonisch/abgeleitet, Rebuild-Faehigkeit (Cap. 28) | offen |
| R-08 | Widersprueche werden automatisch aufgeloest statt vorgelegt | mittel | Konflikt-Queue, menschliche Aufloesung (Cap. 18) | offen |
| R-09 | Veraltetes Wissen wird als aktuell ausgeliefert | mittel | Aktualitaetsfilter, Supersession (Cap. 13, 14) | offen |
| R-10 | Nichtdeterministische Indexierung macht Ergebnisse unreproduzierbar | mittel | Determinismus als Akzeptanzkriterium (Cap. 7) | offen |
| R-11 | Paralleler Schreibzugriff von mehreren Geraeten beschaedigt den Bestand | mittel | Atomare Aenderungen, Mehrschreiberschutz (Cap. 23) | offen |

## Projekt und Prozess

| ID | Risiko | Schwere | Gegenmassnahme | Status |
| --- | --- | --- | --- | --- |
| R-12 | Vorgezogene Implementierung praejudiziert offene Architekturentscheidungen | **hoch** | Sperrliste `DO_NOT_START.md`, Aufhebung nur per A0 | gemindert |
| R-13 | 29 Capabilities ohne Priorisierung fuehren zu Scope-Ueberdehnung | **hoch** | Scope Lock an G0, minimal nuetzlicher Umfang OD-04 | offen |
| R-14 | Gate G0 ohne definierte Kriterien ist nicht abschliessbar | mittel | OD-01 | offen |
| R-15 | Zwei verbindliche Eingangsquellen lagen nicht vor | mittel | Dokumentiert als OI-01; nichts erfunden, Luecke als offene Frage gefuehrt | dokumentiert |
| R-16 | Dokumentationsfundament driftet vom tatsaechlichen Stand ab | mittel | Pflege im Rahmen jedes Work Packages, `project-brain` als Einstiegspunkt | offen |
| R-17 | Abweichungen vom NDF wachsen unkontrolliert | niedrig | `ADOPTION_NOTES.md`, jede Abweichung nummeriert und begruendet | gemindert |
| R-18 | Fehlende Lizenz blockiert spaetere Nutzung oder Veroeffentlichung | niedrig | OD-23; bis dahin bewusst offen | offen |

## Betrieb

| ID | Risiko | Schwere | Gegenmassnahme | Status |
| --- | --- | --- | --- | --- |
| R-19 | Bindung an Proxmox oder Compose sickert in die Architektur ein | mittel | Prinzip Deployment-Neutralitaet (Cap. 29) | offen |
| R-20 | Sicherung existiert, Wiederherstellung wurde nie geprobt | mittel | Backup, Restore und Rebuild als drei getrennte Faehigkeiten (Cap. 28) | offen |
| R-21 | Retrieval-Qualitaet verschlechtert sich unbemerkt | mittel | Benchmarks und Regressionstests (Cap. 22) | offen |

## Zusammenfassung

| Schwere | Anzahl |
| --- | --- |
| hoch | 8 |
| mittel | 11 |
| niedrig | 2 |
| **Summe** | **21** |

Kein Risiko ist vollstaendig geschlossen. Das entspricht Phase 0: die
Gegenmassnahmen sind ueberwiegend geplante Capabilities, keine wirksamen
Kontrollen.

## Pflege

Ein Risiko wird nicht geloescht, sondern auf `geschlossen` gesetzt und mit der
wirksamen Kontrolle verknuepft.
