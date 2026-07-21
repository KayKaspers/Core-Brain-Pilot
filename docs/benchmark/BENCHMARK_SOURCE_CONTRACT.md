# Benchmark Source Contract

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-005 |
| Autoritätsklasse | A2 |
| Status | **Vertrag definiert, kein Retrieval implementiert** |
| Stand | 2026-07-21 (Korrekturlauf) |

---

## 1. Zweck

Der Benchmark-Korpus ist ein **kontrolliertes Testartefakt**. Er existiert, um
den späteren Retrieval-Pfad messbar zu machen: Findet er die richtige Quelle?
Beachtet er Autorität, Aktualität und Datenklasse? Erkennt er Widersprüche?
Schweigt er, wenn keine Evidenz vorliegt?

Ein Benchmark auf produktiven Daten wäre unbrauchbar, weil die Grundwahrheit
fehlt. Hier ist sie konstruiert und damit prüfbar.

## 2. Abgrenzung zum produktiven Wissensbestand

Der Korpus ist **nicht**:

| Nicht | Begründung |
| --- | --- |
| Produktiver Wissensbestand | Er enthält ausschließlich erfundene Inhalte |
| Beweis einer Suchimplementierung | Es existiert keine Suche |
| Ersatz für einen späteren Realbestandstest | Synthetik hat andere Verteilungen als echte Daten |
| Trainingsmaterial für ein Sprachmodell | Ausdrücklich ausgeschlossen |
| Freigabe für vertrauliche Daten | `confidential` und `excluded-from-ai` sind hier **Etiketten auf harmlosem Text** |

Der Korpus liegt unter `benchmarks/` und ist damit räumlich vom künftigen
kanonischen Bestand getrennt. Er wird **nie** in den produktiven Index
aufgenommen.

## 3. Zulässige Dateiformate

Im ersten Benchmark **ausschließlich Markdown**.

PDF, Office und andere Formate kommen erst in Frage, wenn die Ingest- und
Quarantäne-Pipeline existiert (D-019). Ein Benchmark über Formate, die das
System noch nicht sicher aufnehmen kann, misst nichts Sinnvolles.

## 4. Zulässige Daten

| Regel | Ausprägung |
| --- | --- |
| Synthetisch | Alle Inhalte sind erfunden |
| Unkritisch | Kein Inhalt wäre bei Offenlegung schädlich |
| Keine realen Secrets | Keine Schlüssel, Tokens, Passwörter — auch keine realistisch aussehenden Platzhalter |
| Keine realen personenbezogenen Daten | Keine echten Namen, Adressen, Kennungen |
| Keine realen Organisationen | Keine existierenden Firmen, Kunden, Produkte |

Die drei Projekte des Korpus — **Kastanie**, **Nordlicht**, **Zeisig** — sind
frei erfunden. Personen erscheinen nur als Rollen („die Projektleitung"), nie
als Namen.

## 5. Mindestmetadaten je Benchmarkquelle

Jede Quelldatei führt einen Frontmatterblock mit **allen** folgenden Feldern:

| Feld | Bedeutung |
| --- | --- |
| `source_id` | Stabile Kennung, überlebt Umbenennung |
| `title` | Titel |
| `project` | Zugehöriges fiktives Projekt |
| `source_type` | `adr`, `status`, `roadmap`, `readme`, `handoff`, `wiki`, `log` |
| `authority_class` | `A0` bis `A6` |
| `data_class` | `public`, `internal`, `confidential`, `excluded-from-ai` |
| `revision` | Fortlaufende Revisionsnummer |
| `reviewed_at` | Datum der letzten Prüfung |
| `freshness_status` | `current`, `stale`, `superseded` |
| `verification_status` | `verified`, `unverified`, `derived` |
| `valid_from` | Beginn der Gültigkeit |
| `valid_until` oder `superseded_by` | Ende der Gültigkeit oder ersetzende `source_id` |
| `ai_transfer` | `allowed`, `restricted`, `forbidden` |
| `conflict_refs` | `source_id`s widersprechender Quellen, oder `[]` |
| `test_fixture` | **immer `true`** |

`test_fixture: true` ist die technische Absicherung: eine Quelle ohne dieses
Feld gehört nicht in den Korpus, und eine Quelle mit diesem Feld gehört nie in
den produktiven Bestand.

**`data_class: secret` kommt im Korpus nicht vor.** Secrets sind unabhängig von
Synthetik verboten; ein synthetisches Secret bleibt ein Muster, das man nicht
üben sollte.

### Zusatzfeld für A0-Fixtures

| Feld | Bedeutung |
| --- | --- |
| `synthetic_authority` | **Pflicht bei `authority_class: A0`**, immer `true` |

## 5a. Autoritätsabdeckung und synthetische A0-Fixtures

*Ergänzt im Korrekturlauf zu CBP-WP-005.*

### A0 bis A6 müssen vertreten sein

> **Der Benchmark-Korpus muss alle sieben Autoritätsklassen A0 bis A6
> abbilden.** Eine fehlende Klasse bedeutet eine ungetestete Stufe des
> Autoritätsmodells.

Diese Anforderung war in der Erstausführung von CBP-WP-005 nicht erfüllt: der
Korpus enthielt nur A1 bis A6. A0 wurde mit der Begründung ausgelassen, ein
Human-Maintainer-Beschluss lasse sich nicht synthetisieren. **Das war eine
unzulässige Verengung der Anforderung** — die höchste Autoritätsstufe blieb
dadurch ungetestet. Korrigiert in Dataset-Version 2.0.0.

### Was ein synthetisches A0-Fixture ist

Ein A0-Fixture ist ein **fiktiver Human-Maintainer-Beschluss innerhalb eines
vollständig synthetischen Benchmarkprojekts**.

| Eigenschaft | Ausprägung |
| --- | --- |
| Zweck | **Simuliert nur eine Autoritätsstufe** |
| Kennzeichnung | `test_fixture: true` **und** `synthetic_authority: true` |
| `source_type` | `human-maintainer-decision` |
| Inhalt | offensichtlich fiktiv; keine realen Namen, Organisationen, Produkte oder Zugangsdaten |
| Datenklasse | niemals `secret`; keine personenbezogenen oder vertraulichen Echtdaten |

### Was ein A0-Fixture nicht ist

- **Keine reale A0-Entscheidung.** Es ist kein Beschluss des Human Maintainers
  für Core Brain Pilot.
- **Keine Autorität außerhalb des Benchmark-Korpus.** Die Wirkung endet an der
  Korpusgrenze.
- **Kein zulässiger Beleg für eine reale Projektentscheidung.** Ein A0-Fixture
  darf **niemals** in `DECISION_REGISTER.md`, einem ADR oder einem
  Statusdokument als Quelle zitiert werden.

> **Das Benchmarksystem prüft Autoritätsverhalten. Es verleiht selbst keine
> Autorität.**
>
> Die falsche Übertragung einer Fixture-Autorität auf das reale Projekt ist ein
> **kritischer Fehler** — siehe
> [EVALUATION_RUBRIC.md](EVALUATION_RUBRIC.md).

## 6. Versionierungsregeln

- Der Korpus wird als Ganzes versioniert (`benchmarks/README.md`, Feld
  Dataset-Version).
- Eine inhaltliche Änderung an einer Quelle erhöht deren `revision`.
- Eine Änderung, die eine erwartete Antwort verschiebt, ist eine
  **Dataset-Änderung** und folgt
  [DATASET_GOVERNANCE.md](DATASET_GOVERNANCE.md).
- Messergebnisse gelten nur für die Dataset-Version, unter der sie entstanden
  sind.

## 7. Regeln für absichtliche Konflikte

Konflikte sind **konstruiert und dokumentiert**, nicht zufällig.

1. Jede beteiligte Quelle nennt die Gegenseite in `conflict_refs`.
2. Der Konflikt ist im Korpus-Index als Paar geführt.
3. Die **erwartete Auflösung** steht in
   [EXPECTED_RESULTS.md](../../benchmarks/expected/EXPECTED_RESULTS.md), nicht
   in den Quellen selbst.
4. Das erwartete Systemverhalten ist **Konflikt melden**, nicht auflösen — die
   automatische Auflösung ist ein kritischer Fehler.
5. Wo Autoritätsklassen unterschiedlich sind, gewinnt die niedrigere Zahl. Das
   System soll das erkennen und **begründen**, nicht raten.

## 8. Regeln für veraltete Quellen

- `freshness_status: superseded` **erfordert** ein `superseded_by`.
- `freshness_status: stale` bedeutet: nicht ersetzt, aber überholt; erfordert
  ein `valid_until` in der Vergangenheit.
- Veraltete Quellen bleiben im Korpus. Sie zu löschen würde den Aktualitätstest
  entfernen.
- Erwartetes Verhalten: die aktuelle Quelle liefern, die veraltete allenfalls
  als Historie kennzeichnen.

## 9. Regeln für `excluded-from-ai`-Testfälle

> **Wichtig.** Eine als `excluded-from-ai` gekennzeichnete Testquelle enthält
> **nur synthetische, nicht sensible Testdaten**. Ihre Funktion ist
> ausschließlich zu prüfen, dass der spätere Retrieval-Layer ihren Inhalt
> **nicht an ein externes Modell überträgt**.
>
> **Das schwächt die Produktionsregel nicht ab.** Im produktiven Bestand
> bleibt `excluded-from-ai` eine Willensentscheidung über echte Inhalte, und
> die Sperrwirkung ist dieselbe.

Regeln:

1. Der Inhalt ist harmlos genug, dass ein Testfehler keinen Schaden anrichtet.
2. `ai_transfer: forbidden` ist gesetzt.
3. Erwartetes Verhalten: **Trefferexistenz oder Sperrhinweis melden, Inhalt
   zurückhalten.** Das ist kein Widerspruch — dass etwas existiert, ist keine
   Preisgabe dessen, was drinsteht.
4. Die Ausgabe des Inhalts an ein externes Modell ist ein **kritischer Fehler**
   (D-021, R-31).

## 10. Lösch- und Rebuild-Regeln

- Eine gelöschte Testquelle erhält einen **Tombstone-Eintrag** in einem
  Löschprotokoll, statt spurlos zu verschwinden.
- Ein Rebuild des Testindex folgt dem Rebuild-Vertrag aus
  [SYSTEM_ARCHITECTURE.md](../architecture/SYSTEM_ARCHITECTURE.md).
- Nach einem Rebuild darf keine gelöschte Quelle mehr auffindbar sein — das ist
  ein eigener Prüfpunkt.
- Der Korpus selbst wird **nie** aus einem Index rekonstruiert; er ist
  kanonisch für sich.

## 11. Beziehung zu D-1

G0-Kriterium **D-1** („Gewünschte Quellen") steht auf `answered`, nicht
`accepted`.

| Ebene | Stand |
| --- | --- |
| Quellen**arten** | entschieden (HDI A3): Markdown, Git-Repositories, Chat-Handoffs, Obsidian-Vault als Markdown |
| Benchmark-Korpus | **hier definiert** — kontrolliert, synthetisch, versioniert |
| Konkrete produktive Quellenpfade | **offen** — OD-05, OD-06 |

Dieser Vertrag ersetzt D-1 **nicht**. Er zeigt, dass das Quellenmodell
tragfähig ist, ohne den produktiven Bestand festzulegen. D-1 bleibt
`answered`, bis der reale Bestand benannt ist.

## 12. Beziehung zum späteren produktiven Ingest

| Aspekt | Benchmark | Produktiver Ingest |
| --- | --- | --- |
| Quelle der Inhalte | erfunden | real |
| Eingang | direkt als Fixture | **nur über Quarantäne** (TB-1, D-019) |
| Klassifikation | vorab gesetzt | an der Grenze zugewiesen |
| Freigabe | keine nötig | **menschlicher Kurationsschritt** (TB-2) |
| Secret-Prüfung | entfällt (keine Secrets vorhanden) | verpflichtend |

Der Benchmark **umgeht** die Ingest-Pipeline bewusst, weil er sie testen soll,
nicht durchlaufen. Diese Ausnahme gilt ausschließlich für `test_fixture: true`.

## Status

**Kein Retrieval implementiert, keine Suchsoftware ausgewählt, kein Index
gebaut.** Dieser Vertrag beschreibt, wie der Korpus beschaffen ist — nicht, wie
er verarbeitet wird.
