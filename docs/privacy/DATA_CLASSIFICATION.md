# Data Classification — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Status | Verbindliches Regelwerk, **technisch nicht durchgesetzt** |
| Überarbeitet in | CBP-WP-002 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

Jede Wissenseinheit trägt **genau eine** Datenklasse.

## Warum Klassifikation überhaupt nötig ist

Index und Suchmodelle laufen lokal und selbst gehostet. **Claude Code
verwendet jedoch keinen vollständig lokalen Sprachmodellbetrieb** — nur
ausgewählte Inhalte dürfen an das verwendete Claude-Modell übertragen werden.

Weil Übertragung stattfindet, muss geregelt sein, was übertragen werden darf.
Genau dafür existieren die Datenklassen.

*Quelle: Projektübergabe §11.*

## Die fünf Klassen

### `public`
Für Veröffentlichung geeignet. Keine personenbezogenen Daten, keine internen
Details.

### `internal`
Projektinterne Arbeitsinformation ohne besondere Schutzbedürftigkeit.
Standardklasse für kuratiertes Projektwissen.

### `confidential`
Erhöhter Schutzbedarf. Offenlegung wäre schädlich. Enthält häufig
personenbezogene Daten.

### `secret`
Zugangsdaten und Geheimnisse jeder Art: Passwörter, API-Keys, Tokens, private
Schlüssel, Zertifikate mit privatem Teil, Verbindungszeichenfolgen mit
Zugangsdaten.

### `excluded-from-ai`
Inhalte, die aus rechtlichen oder persönlichen Gründen **nicht** in einen
KI-Kontext gelangen dürfen — unabhängig von ihrer sonstigen
Schutzbedürftigkeit.

Diese Klasse ist eine **Willensentscheidung**, keine Risikoeinstufung. Ein
harmloser Inhalt kann hier stehen, weil der Maintainer es so will.

## Flussmatrix

Die fünf Dimensionen entsprechen der Vorgabe aus Projektübergabe §11.
*Umgestellt in CBP-WP-002 als Korrektur F-06 — die vorherige Fassung verwendete
abweichende Dimensionen.*

| Klasse | darf indexiert werden | darf lokal durchsucht werden | **darf an Claude übertragen werden** | darf im Wiki zusammengefasst werden | darf mobil angezeigt werden |
| --- | --- | --- | --- | --- | --- |
| `public` | ja | ja | ja | ja | ja |
| `internal` | ja | ja | ja | ja | ja |
| `confidential` | ja | ja | **nur bei Bedarf und mit Begründung** | nur als Verweis, ohne Inhalt | ja, autorisiert |
| `secret` | **nie** | **nie** | **nie** | **nie** | **nie** |
| `excluded-from-ai` | **nie** | nur lokal, außerhalb des KI-Pfads | **nie** | **nie** | **nie** |

Die dritte Spalte ist die kritische: sie beschreibt die Vertrauensgrenze TB-4,
an der Daten das System tatsächlich verlassen.

## Absolute Regel

> **Secrets dürfen nicht in Repository, Wissensbestand, Index, Context Pack
> oder Modellkontext gelangen.**

Keine Ausnahme, kein Debug-Modus, kein Testfall.

Folgerungen:

- Keine Beispiel-Secrets, keine Platzhalter-Keys, keine `.env.example` mit
  realistisch aussehenden Werten
- Ein Implementation Agent erzeugt, liest, speichert und indexiert keine
  Secrets
- Wird ein Secret entdeckt, ist das ein **Blocker**: Arbeit anhalten, melden,
  nicht selbstständig bereinigen

Das Verfahren für den Fall eines Secrets in der Git-Historie ist offen — OD-10.

## Fail-closed

Ist die Datenklasse eines Inhalts **unbekannt**, gilt er als nicht freigegeben.
Unbekannt bedeutet niemals „vermutlich unbedenklich".

## Durchsetzungsebenen

| Ebene | Mechanismus | Status |
| --- | --- | --- |
| 1 | `.gitignore` | **wirksam** |
| 2 | Secret- und PII-Prüfung beim Ingest | not-started |
| 3 | Datenschutzfilter vor dem Modellkontext | not-started |
| 4 | Quellen- und Collection-Berechtigungen | not-started |
| 5 | Vault Doctor als periodische Prüfung | not-started |

> **Warnung.** Nur Ebene 1 ist wirksam, und sie ist eine Vorsichtsmaßnahme,
> keine Garantie. Die Klassifikation existiert derzeit **dokumentarisch, ohne
> technische Durchsetzung** — erfasst als Risiko R-30.

## Offene Fragen

| Frage | Bezug |
| --- | --- |
| Wer vergibt Datenklassen, und wann? | OD-08, G0-Kriterium D-4 |
| Rechtsgrundlage für personenbezogene Daten | OD-09, D-6 |
| Verfahren bei Secret in der Historie | OD-10, D-8 |
| Welche Daten sind `excluded-from-ai`? | D-5, Fragebogen 4.5 |
| Erfolgt PII-Erkennung automatisch, manuell oder beides? | Fragebogen 4.6 |
