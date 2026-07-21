# Baseline Protocol — Durchführung und Erfassung eines Laufs

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-005 |
| Autoritätsklasse | A2 |
| Status | **Protokoll definiert, kein Lauf durchgeführt** |
| Stand | 2026-07-21 |

Belegt G0-Kriterium **G-4** gemeinsam mit
[BENCHMARK_PLAN.md](BENCHMARK_PLAN.md).

**Keine Messsoftware implementiert.** Dieses Protokoll beschreibt ein manuell
durchführbares Verfahren.

---

## 1. Vorbereitung einer frischen Session

| Schritt | Anforderung |
| --- | --- |
| Neue Sitzung | Kein Kontext aus vorherigen Läufen |
| Kein Vorwissen | Weder Fragen noch erwartete Quellen vorab im Kontext |
| Korpusstand prüfen | Dataset-Version notieren |
| Modell notieren | Name und Version |
| Regeln laden | Datenschutz- und Berechtigungsregeln, in **allen** Varianten |

Eine Sitzung, die bereits eine Benchmarkfrage gesehen hat, ist für diesen Lauf
verbraucht.

## 2. Auswahl der Benchmarkvariante

V0, V1 oder V2 wird **vor** dem Lauf festgelegt und im Protokollkopf notiert.
Ein Wechsel mitten im Lauf macht ihn ungültig.

## 3. Umgang mit Development und Holdout

| Set | Verwendung |
| --- | --- |
| **Development** (24) | Kalibrierung, Iteration, Fehlersuche — beliebig oft |
| **Holdout** (12) | **Nur zur Abschlussprüfung.** Nicht zur Kalibrierung, nicht zur Fehlersuche |

Wird eine Holdout-Frage versehentlich zur Kalibrierung verwendet, ist sie
**verbrannt**: sie wird als solche markiert und aus der Abschlussprüfung
genommen. Sie wird nicht stillschweigend weiterverwendet.

## 4. Start- und Endzeit

Je Frage: Startzeit bei Stellung, Endzeit bei vollständiger Antwort.
Unterbrechungen werden gesondert notiert und **nicht** aus der Laufzeit
herausgerechnet — die Verzögerung ist real.

## 5. Erfassung geöffneter Dateien

Jede geöffnete Quelle wird mit `source_id` und Reihenfolge notiert.

„Geöffnet" bedeutet: Inhalt wurde gelesen. Ein Treffer in einer Ergebnisliste,
der nicht geöffnet wurde, zählt nicht als geöffnete Datei — wohl aber für die
Rangfolge.

## 6. Erfassung gelesener Abschnitte

Je geöffneter Quelle: welche Abschnitte gelesen wurden. Bei vollständigem Lesen
wird das ausdrücklich vermerkt — der Unterschied zwischen „ein Abschnitt" und
„ganze Datei" ist der Kern der Effizienzmessung.

## 7. Erfassung des Quellkontexts

Umfang der tatsächlich an das Modell übergebenen Quellinhalte, je Frage.

**Nicht erfasst wird der Inhalt gesperrter Quellen.** Bei
`excluded-from-ai` wird ausschließlich die Entscheidung protokolliert
(„gesperrt, nicht übertragen"), niemals der Text.

## 8. Tokenmessung oder reproduzierbare Schätzung

**Bevorzugt:** exakte Tokenzahlen aus dem Client.

**Falls der Client keine exakten Tokenzahlen liefert:**

1. Eine **dokumentierte deterministische Schätzung** verwenden. Deterministisch
   heißt: dieselbe Eingabe ergibt immer denselben Wert.
2. Schätzwerte **eindeutig kennzeichnen** — im Protokoll und in jeder
   Auswertung.
3. **Nur Werte vergleichen, die mit derselben Methode entstanden sind.** Ein
   gemessener Wert und ein geschätzter Wert gehören nicht in dieselbe Spalte.
4. Ein Wechsel der Schätzmethode macht frühere Werte nicht ungültig, aber
   **nicht mehr vergleichbar** — er wird wie ein Modellwechsel behandelt.

Die konkrete Schätzmethode ist noch nicht festgelegt und wird beim ersten Lauf
dokumentiert.

## 9. Erfassung der Quellenrangfolge

Die Reihenfolge, in der Quellen als Kandidaten erschienen — Grundlage für
Recall@1, @3, @5 und MRR.

V0 liefert in der Regel **keine** Rangfolge. Das ist kein Mangel des Protokolls,
sondern ein Merkmal der Baseline: rangabhängige Metriken werden für V0 als
**nicht anwendbar** ausgewiesen, nicht als null.

## 10. Erfassung von Fehlern

Je Frage: Qualitätspunktzahl (0/1/2), festgestellte kritische Fehler,
Abweichungen vom erwarteten Verhalten.

**Kritische Fehler werden gesondert gelistet**, nicht in die Punktzahl
eingerechnet.

## 11. Keine Nachbesserung während eines Laufs

> Fällt ein Fehler auf, wird er **notiert, nicht behoben**.

Keine Prompt-Anpassung, keine Gewichtsänderung, kein Nachfassen bei einer
bereits beantworteten Frage. Eine Korrektur mitten im Lauf erzeugt eine
Mischung aus zwei Konfigurationen, die nichts mehr misst.

Verbesserungen gehören in den **nächsten** Lauf.

## 12. Wiederholung bei technischem Abbruch

| Situation | Umgang |
| --- | --- |
| Technischer Abbruch (Verbindung, Zeitüberschreitung, Werkzeugfehler) | Lauf **vollständig** wiederholen, nicht ab der Abbruchstelle fortsetzen |
| Abbruch nach mehr als der Hälfte der Fragen | Teilergebnis archivieren, als unvollständig kennzeichnen, nicht in die Auswertung nehmen |
| Wiederholter Abbruch an derselben Frage | Als Befund dokumentieren — das ist ein Ergebnis, kein Störfall |

Ein fortgesetzter Lauf hat einen anderen Sitzungszustand als ein durchgehender
und ist damit ein anderer Lauf.

## 13. Umgang mit Modell- oder Tooländerungen

| Änderung | Folge |
| --- | --- |
| Modellwechsel | Messreihe endet; neue Reihe beginnt. Werte sind **nicht** vergleichbar |
| Modellversionswechsel | Wie Modellwechsel, sofern nicht ausdrücklich als äquivalent belegt |
| Wechsel des Suchproviders | Neue Variante, nicht neue Version derselben |
| Änderung der Token-Schätzmethode | Wie Modellwechsel |
| Änderung des Korpus | **Neue Dataset-Version**; alle früheren Werte gelten nur für die alte Version |

In allen Fällen: **dokumentieren, nicht stillschweigend fortführen.** Eine
unbemerkte Änderung ist der einzige Fehler, der eine ganze Messreihe wertlos
macht.

---

## Protokollkopf je Lauf

```text
Lauf-ID
Variante:              V0 | V1 | V2
Dataset-Version
Set:                   development | holdout
Modell und Version
Datum, Start, Ende
Token-Erfassung:       gemessen | geschätzt (Methode)
Suchprovider:          (bei V2)
Abweichungen vom Protokoll
```

## Protokoll je Frage

```text
question_id
Startzeit, Endzeit
Geöffnete Quellen (source_id, Reihenfolge)
Gelesene Abschnitte je Quelle
Rangfolge der Kandidaten
Übertragener Quellkontext
Tokens (gemessen oder geschätzt)
Zahl der Suchoperationen
Antwortform:           answer | qualified answer | abstain | escalate
Qualitätspunktzahl:    0 | 1 | 2
Kritische Fehler
Bemerkungen
```

## Status

**Kein Lauf durchgeführt, keine Messsoftware implementiert.** Dieses Protokoll
ist manuell ausführbar und setzt keine Werkzeuge voraus, die noch nicht
existieren.
