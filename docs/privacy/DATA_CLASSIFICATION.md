# Data Classification — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Status | Verbindliches Regelwerk, technisch noch nicht durchgesetzt |
| Autoritaetsklasse | A2 |
| Stand | 2026-07-20 |

Jede Wissenseinheit traegt **genau eine** Datenklasse. Die Klasse entscheidet,
ob der Inhalt in Repository, Index, Context Pack, Modellkontext oder Web-UI
gelangen darf.

## Die fuenf Klassen

### `public`

Fuer Veroeffentlichung geeignet. Keine personenbezogenen Daten, keine internen
Details.

*Beispiele:* oeffentliche Dokumentation, Lizenztexte, veroeffentlichte Releases.

### `internal`

Projektinterne Arbeitsinformation ohne besondere Schutzbeduerftigkeit.
Standardklasse fuer kuratiertes Projektwissen.

*Beispiele:* Architekturnotizen, Work Packages, Entscheidungsregister.

### `confidential`

Erhoehter Schutzbedarf. Offenlegung waere schaedlich. Enthaelt haeufig
personenbezogene Daten.

*Beispiele:* interne Betriebsdetails, personenbezogene Notizen,
Sicherheitsanalysen.

### `secret`

Zugangsdaten und Geheimnisse jeder Art.

*Beispiele:* Passwoerter, API-Keys, Tokens, private Schluessel, Zertifikate mit
privatem Teil, Verbindungszeichenfolgen mit Zugangsdaten.

### `excluded-from-ai`

Inhalte, die aus rechtlichen oder persoenlichen Gruenden **nicht** in einen
KI-Kontext gelangen duerfen — unabhaengig von ihrer sonstigen
Schutzbeduerftigkeit.

Diese Klasse ist eine **Willensentscheidung**, keine Risikoeinstufung. Ein
harmloser Inhalt kann hier stehen, weil der Maintainer es so will.

## Flussmatrix

| Klasse | Repository | Index | Context Pack | Modellkontext | Web-UI |
| --- | --- | --- | --- | --- | --- |
| `public` | ja | ja | ja | ja | ja |
| `internal` | ja | ja | ja | ja | ja |
| `confidential` | ja, mit Vorsicht | ja | nur bei Bedarf | nur bei Bedarf | ja, autorisiert |
| `secret` | **nie** | **nie** | **nie** | **nie** | **nie** |
| `excluded-from-ai` | **nie** | **nie** | **nie** | **nie** | nur lokal, ausserhalb des Systems |

## Absolute Regel

> **Secrets duerfen nicht in Repository, Wissensbestand, Index, Context Pack
> oder Modellkontext gelangen.**

Diese Regel kennt keine Ausnahme, keinen Debug-Modus und keinen Testfall.

Folgerungen:

- Keine Beispiel-Secrets, keine Platzhalter-Keys, keine `.env.example` mit
  realistisch aussehenden Werten.
- Ein Implementation Agent erzeugt, liest, speichert und indexiert keine
  Secrets.
- Wird ein Secret entdeckt, ist das ein **Blocker**: Arbeit anhalten, melden,
  nicht selbstaendig bereinigen.

## Fail-closed

Ist die Datenklasse eines Inhalts **unbekannt**, gilt er als nicht
freigegeben. Unbekannt bedeutet niemals "vermutlich unbedenklich".

## Durchsetzungsebenen

| Ebene | Mechanismus | Status |
| --- | --- | --- |
| 1 | `.gitignore` | angelegt |
| 2 | Secret- und PII-Pruefung beim Ingest | not-started |
| 3 | Datenschutzfilter vor dem Modellkontext | not-started |
| 4 | Quellen- und Collection-Berechtigungen | not-started |
| 5 | Vault Doctor als periodische Pruefung | not-started |

Ebene 1 ist eine Vorsichtsmassnahme, keine Garantie.

## Offene Fragen

Klassifikationsschema und Rechtsgrundlagen sind noch nicht gelockt. Siehe
[docs/discovery/DISCOVERY_QUESTIONS.md](../discovery/DISCOVERY_QUESTIONS.md).
