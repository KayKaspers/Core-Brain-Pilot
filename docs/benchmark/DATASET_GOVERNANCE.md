# Dataset Governance — Pflege des Benchmark-Datasets

| Feld | Wert |
| --- | --- |
| **Dataset-Version** | **2.0.0** |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-005 |
| Owner | **Human Maintainer** |
| Reviewstatus | **in-review** (CBP-WP-005, Korrekturlauf) |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

---

## Der Grundsatz

> **Eine Benchmarkfrage darf nicht stillschweigend so verändert werden, dass
> eine zuvor fehlerhafte Implementierung nachträglich als korrekt gilt.**

Das ist die einzige Regel, die dieses Dokument wirklich braucht. Alles Weitere
sind Verfahren, die sie durchsetzbar machen.

Ein Benchmark, dessen Erwartungen sich an das System anpassen, misst nichts
mehr. Er bestätigt nur noch.

## Dataset-Version

Format `MAJOR.MINOR.PATCH`.

| Änderung | Stufe |
| --- | --- |
| Frage hinzugefügt oder entfernt | **MAJOR** |
| Erwartete Quelle oder Antwortform geändert | **MAJOR** |
| Korpusquelle hinzugefügt, entfernt oder inhaltlich geändert | **MAJOR** |
| Kategorie- oder Set-Zuordnung geändert | **MAJOR** |
| Formulierung präzisiert, ohne die Erwartung zu verschieben | MINOR |
| Tippfehler, Formatierung, Verweise | PATCH |

**MAJOR-Änderungen machen frühere Messwerte nicht falsch, aber nicht mehr
vergleichbar.** Sie werden in Auswertungen nie über Versionsgrenzen hinweg
zusammengefasst.

## Änderungshistorie

| Version | Datum | Änderung | Work Package |
| --- | --- | --- | --- |
| 1.0.0 | 2026-07-21 | Erstanlage: 24 Korpusquellen (A1–A6), 36 Fragen, erwartete Ergebnisse | CBP-WP-005 |
| **2.0.0** | 2026-07-21 | **Korrekturlauf nach Nova-REWORK:** A0-Fixture ergänzt (`ZEI-A0-BESCHLUSS-WEBOBERFLAECHE`), `NOR-README` entfernt, B-03 und F-03 auf den A0-Vorrang umgestellt, Konfliktpaar K5, kritische Fehler 8 und 9 ergänzt | CBP-WP-005 (REWORK) |

## Owner und Reviewstatus

| Rolle | Zuständigkeit |
| --- | --- |
| **Human Maintainer** | Owner. Gibt jede Dataset-Änderung frei |
| **Nova** | Schlägt Änderungen vor, prüft fachlich |
| **Implementation Agent** | Setzt freigegebene Änderungen um, **entscheidet nichts** |

| Reviewstatus | Bedeutung |
| --- | --- |
| `draft` | In Arbeit, nicht für Messungen verwendbar |
| `in-review` | Vollständig, wartet auf Freigabe |
| `released` | Freigegeben, für Messungen verwendbar |
| `archived` | Durch neuere Version ersetzt |

**Version 2.0.0 steht auf `in-review`.** Sie ist erst nach Freigabe durch den
Human Maintainer für Messungen verwendbar.

**Zur Versionsstufe:** Der Korrekturlauf entfernt und ergänzt Korpusquellen und
verschiebt erwartete Quellen bei zwei Fragen — nach den Regeln oben ist das
**MAJOR**. Version 1.0.0 hat nie den Status `released` erreicht und es
existiert keine Messung auf ihrer Grundlage; die Stufe wird dennoch strikt
angewendet, weil eine Ausnahme genau die Aufweichung wäre, gegen die diese
Governance geschrieben ist.

## Freigabeprozess

```text
1. Antrag        Änderungsvorschlag mit Begründung und betroffenen question_ids
2. Prüfung       Verschiebt die Änderung eine Erwartung? Wenn ja: MAJOR
3. Zielprüfung   Würde die Änderung ein bekanntes Fehlverhalten legitimieren?
                 Wenn ja: ABLEHNEN
4. Freigabe      Human Maintainer entscheidet
5. Versionierung Neue Dataset-Version, Historieneintrag, alte Version archivieren
6. Regression    Betroffene Messreihen als nicht mehr vergleichbar kennzeichnen
```

Schritt 3 ist der wichtigste und derjenige, den man am leichtesten überspringt.

## Regeln für neue Fragen

1. Jede neue Frage nennt Kategorie, Set, alle Pflichtfelder und eine
   `rationale`.
2. Die Kategorieverteilung bleibt ausgeglichen — sechs Kategorien.
3. Eine neue Frage darf **keine** Information verlangen, die nicht im Korpus
   belegt ist. Ausnahme: ausdrückliche Negativfälle.
4. Neue Fragen gehen **zuerst ins Development-Set**. Ein direkter Zugang zum
   Holdout ist ausgeschlossen — eine Frage, die man gerade erfunden hat, ist
   kein unabhängiger Test.
5. Das Verhältnis 2:1 zwischen Development und Holdout wird beibehalten.

## Regeln für Änderungen erwarteter Quellen

Eine Änderung an `expected_source_ids` oder an der erwarteten Antwortform ist
**immer** MAJOR und **immer** begründungspflichtig.

Zulässige Gründe:

| Grund | Beispiel |
| --- | --- |
| Der Korpus hat sich geändert | Neue Quelle beantwortet die Frage besser |
| Die Erwartung war sachlich falsch | Zwei Quellen wären nötig, nicht eine |
| Eine Regel hat sich geändert | Neue A0-Entscheidung ändert die Autoritätslage |

**Unzulässiger Grund:** „Das System hat eine andere Quelle gefunden, die auch
plausibel ist." Das ist genau die stille Zielverschiebung, die dieser
Grundsatz verhindert.

## Vermeidung stiller Zielverschiebung

Vier Mechanismen:

1. **Begründungspflicht.** Jede Erwartungsänderung nennt einen der drei
   zulässigen Gründe.
2. **Zeitliche Trennung.** Eine Erwartungsänderung, die unmittelbar nach einem
   fehlgeschlagenen Lauf beantragt wird, ist besonders zu prüfen.
3. **Historie.** Alte Erwartungen bleiben in der archivierten Dataset-Version
   nachlesbar.
4. **Vier-Augen-Prinzip.** Der Implementation Agent, der das System kalibriert,
   entscheidet nicht über Erwartungen.

## Umgang mit fehlerhaften Fragen

Eine Frage ist fehlerhaft, wenn sie mehrdeutig ist, die erwartete Antwort im
Korpus nicht belegt ist, ihre Pflichtfelder widersprüchlich sind oder mehrere
Antworten gleichermaßen korrekt wären.

| Schritt | Vorgehen |
| --- | --- |
| 1 | Frage als `defective` markieren, **nicht löschen** |
| 2 | Aus laufenden Auswertungen nehmen und den Ausschluss ausweisen |
| 3 | Korrigierte Fassung als **neue** `question_id` aufnehmen |
| 4 | Die fehlerhafte Fassung bleibt archiviert |

Eine stillschweigend korrigierte Frage ist von einer nachträglich passend
gemachten Frage nicht mehr unterscheidbar.

## Holdout-Schutz

| Regel | Ausprägung |
| --- | --- |
| Nicht zur Kalibrierung | Weder Gewichte, Prompts, Filterreihenfolge noch Budgets |
| Nicht zur Fehlersuche | Ein Fehler wird am Development-Set reproduziert |
| Auswertung | Erst bei der formalen Abschlussprüfung, vollständig |
| Versionierung | Wie alle Fragen — offen im Repository |
| **Kein Sicherheitsgeheimnis** | Der Schutz ist Disziplin, nicht Verschluss |
| Bei versehentlicher Nutzung | Frage als `burned` markieren und aus der Abschlussprüfung nehmen |

Wird der Holdout zu klein — unter acht Fragen —, werden neue Fragen ergänzt und
die Dataset-Version erhöht.

## Archivierung alter Dataset-Versionen

- Ältere Versionen bleiben vollständig erhalten, einschließlich Korpus, Fragen
  und Erwartungen.
- Eine archivierte Version wird **nie** verändert.
- Messergebnisse tragen die Dataset-Version, unter der sie entstanden sind.
- Ein Ergebnis ohne Versionsangabe ist wertlos.

## A0-Fixtures

*Ergänzt im Korrekturlauf zu CBP-WP-005.*

### Abdeckungspflicht

**A0 bis A6 müssen im Benchmark-Korpus vertreten sein.** Fehlt eine Klasse,
bleibt eine Stufe des Autoritätsmodells ungetestet. Diese Regel ist Gegenstand
jeder Dataset-Prüfung.

### Gleiche Governance wie erwartete Ergebnisse

Änderungen an einem A0-Fixture — Anlage, Entfernung, Inhaltsänderung,
Änderung der beteiligten Konfliktquellen — folgen **denselben versionierten
Regeln** wie Änderungen an erwarteten Ergebnissen:

| Änderung | Stufe | Begründungspflicht |
| --- | --- | --- |
| A0-Fixture angelegt oder entfernt | **MAJOR** | ja |
| Inhalt oder Konfliktbezug geändert | **MAJOR** | ja |
| Formulierung ohne Erwartungsverschiebung | MINOR | nein |

Es gibt **keine erleichterte Behandlung**, weil ein Fixture „nur ein Test" ist.
Ein A0-Fixture steuert die höchste Autoritätsstufe des Benchmarks; eine stille
Änderung daran verschiebt die Messlatte am wirksamsten.

### Grenze der Fixture-Autorität

> **Das Benchmarksystem prüft Autoritätsverhalten, verleiht aber selbst keine
> reale Autorität.**

| Ein A0-Fixture | |
| --- | --- |
| simuliert | eine Autoritätsstufe innerhalb des synthetischen Korpus |
| ist **nicht** | eine reale A0-Entscheidung für Core Brain Pilot |
| darf **nicht** | in reale Projektentscheidungen übernommen werden |
| darf **nicht** | in `DECISION_REGISTER.md`, einem ADR oder einem Statusdokument zitiert werden |

Die Übertragung einer Fixture-Autorität auf das reale Projekt ist ein
**kritischer Fehler** (Fehler 9 in
[EXPECTED_RESULTS.md](../../benchmarks/expected/EXPECTED_RESULTS.md)).

Technische Absicherung: `test_fixture: true` **und**
`synthetic_authority: true` in jedem A0-Fixture.

## Verknüpfung mit Source IDs und Revisionen

Jede Frage verweist über `expected_source_ids` auf stabile `source_id`s, nicht
auf Dateipfade. Eine Umbenennung im Korpus lässt die Verknüpfung intakt.

`expected_current_revision` bindet die Erwartung zusätzlich an einen
Revisionsstand. Erhöht sich die Revision einer Quelle inhaltlich, ist zu
prüfen, ob die Erwartung noch gilt — **automatisch gilt sie nicht**.

## Regression bei Systemänderungen

Nach jeder dieser Änderungen ist eine **vollständige Regression auf dem
Development-Set** erforderlich, bevor weitergearbeitet wird:

| Änderung | Warum kritisch |
| --- | --- |
| **Chunking** | Verschiebt Trefferpositionen und Abschnittsgrenzen |
| **Metadaten** | Ändert die Filterwirkung unmittelbar |
| **Autoritätsgewicht** | Kann Konfliktfälle in beide Richtungen kippen |
| **Embeddings** | Modellwechsel ändert den gesamten semantischen Raum; erfordert Rebuild |
| **Reranking** | Ändert die Rangfolge und damit alle Recall-Metriken |
| **Prompt** | Ändert Antwortform und Abstentionsverhalten |
| **Context Budget** | Ändert unmittelbar, wie viel gelesen wird |

Die Abschlussprüfung am Holdout erfolgt **erst danach** und nur einmal je
Konfiguration.

## Was dieses Dokument nicht regelt

- Die Auswahl des Suchproviders — offen (OD-25)
- Die Kalibrierung der Context Budgets — **OD-02b bleibt offen**
- Den konkreten produktiven Wissensbestand — offen (OD-05, OD-06)
- Die Durchführung von Läufen — siehe [BASELINE_PROTOCOL.md](BASELINE_PROTOCOL.md)

## Status

**Dataset-Version 1.0.0, Reviewstatus `in-review`.** Kein Lauf durchgeführt,
keine Messung erhoben, keine Erwartung jemals angepasst.
