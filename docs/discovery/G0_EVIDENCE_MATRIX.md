# G0 Evidence Matrix — Nachweislage aller Core-Required-Kriterien

| Feld | Wert |
| --- | --- |
| Gate | G0 – Discovery and Scope Lock |
| **Gate-Status** | **PASSED WITH NOTES** — 2026-07-21, A0 |
| **Kriterienstand** | 25 von 25 `accepted` |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Erfasst in | CBP-WP-006, Status nachgeführt in CBP-WP-008 |
| Autoritätsklasse | A3 |
| Stand | 2026-07-21 |

Diese Matrix führt **alle 25 Core-Required-Kriterien** mit ihrer vollständigen
Nachweislage. Sie ist die Prüfgrundlage für die G0-Entscheidung.

> **Criteria complete ≠ Technical implementation ≠ Deployment ready.**
> Diese Matrix zeigt, dass die Kriterien belegt sind. Das Gate wurde am
> 2026-07-21 gesondert freigegeben — **16 der 25 Kriterien beschreiben
> weiterhin Kontrollen, die nicht existieren.**

## Legende

**Technisch erforderlich:** ob die Regel zusätzlich technisch umgesetzt werden
muss. `ja` = jetzt fehlend und kritisch · `später` = nach G0 · `nein` = rein
dokumentarisch ausreichend.

**Human-Entscheidung:** ob die Annahme eine ausdrückliche
Human-Maintainer-Entscheidung war.

---

## A — Nutzer und Scope

| ID | Kurzbeschreibung | Status | Autorität | Primärer Nachweis | Ergänzend | Verbleibende Einschränkung | Technisch erf. | Human-E. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **A-1** | Primärer Nutzer benannt | `accepted` | A0 | HDI A2 — Human Maintainer | D-018 | keine | nein | **ja** |
| **A-2** | Erwartete Nutzerzahl | `accepted` | A0 | HDI A2 — 1 im ersten Pilot | D-018 | Multi-User später nicht verhindert, aber ungetestet | später | **ja** |
| **A-4** | Desktop-Anforderungen | `accepted` | A0 | HDI A6 — Web-UI im Pilot | D-024 | Web-UI erst nach funktionierendem Retrieval | später | **ja** |
| **A-5** | Mobile-Anforderungen | `accepted` | A0 | HDI A6 — Suche, Lesen, Status, Handoffs | D-024 | Plattform (Android/iOS) offen — Deployment | später | **ja** |
| **A-8** | Explizite Nicht-Ziele | `accepted` | A0 | `DO_NOT_START.md`, 25 Punkte | 11 Nicht-Ziele auf A-8 gemappt | Repository-Sichtbarkeit separat als OD-11 offen | nein | **ja** |

## D — Datenbestand

| ID | Kurzbeschreibung | Status | Autorität | Primärer Nachweis | Ergänzend | Verbleibende Einschränkung | Technisch erf. | Human-E. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **D-1** | Gewünschte Quellen | `accepted` | A0 | `PILOT_SOURCE_CONTRACT.md` — 7 Slots | `SOURCE_SLOT_MODEL.md`, ADR-0006 (`proposed`), HDI A3 | **Keine produktive Quelle angebunden.** Konkrete Mappings offen (OD-05, OD-06) | **ja** | **ja** |
| **D-3** | Dateiformate | `accepted` | A0 | HDI A3 — Markdown zuerst | D-019 | PDF/Office erst nach Quarantäne (R-32) | **ja** | **ja** |
| **D-4** | Datenklassen zugeordnet | `accepted` | A0 | HDI A4 — Profilebene | `DATA_CLASSIFICATION.md` | Vergabeverfahren je Quelle offen (OD-08) | **ja** | **ja** |
| **D-5** | Ausgeschlossene Daten | `accepted` | A0 | HDI A4 — `excluded-from-ai` von Anfang an | D-021, Slot-Regel 5 | **Sperrwirkung technisch ungeprüft** (R-31) | **ja** | **ja** |
| **D-8** | Secret-Verfahren im Schadensfall | `accepted` | A0 | `SECRET_INCIDENT_RESPONSE.md`, 14 Schritte | Rotation vor Cleanup; Bereinigung vor Rebuild | **Keine Erkennung, keine technische Unterstützung** (R-01) | **ja** | **ja** |

## E — Claude und Repositories

| ID | Kurzbeschreibung | Status | Autorität | Primärer Nachweis | Ergänzend | Verbleibende Einschränkung | Technisch erf. | Human-E. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **E-2** | Erlaubte Repository-Zugriffe | `accepted` | A0 | `PERMISSION_MODEL.md`, Zeile `git repository` | ADR-0004, PS-03 Allowlist | **Nicht durchgesetzt** (R-27) | **ja** | **ja** |
| **E-3** | GitHub-Zugriffe | `accepted` | A0 | `PERMISSION_MODEL.md`, Zeile `github remote` | Claude `forbidden`; Push nur Human Maintainer | **Nicht durchgesetzt** (R-27) | **ja** | **ja** |
| **E-4** | Berechtigungsstufen je Bereich | `accepted` | A0 | Matrix 9 Rollen × 12 Ressourcen | 5 Aktionsklassen, Default deny | **Nicht durchgesetzt** (R-25) | **ja** | **ja** |
| **E-5** | Freigabeverfahren | `accepted` | A0 | Sechsstufiger Ablauf Antrag → Wirkung → Protokoll | ADR-0004 | **Kein Approval-Zustand implementiert** (R-25) | **ja** | **ja** |

## F — Architektur

| ID | Kurzbeschreibung | Status | Autorität | Primärer Nachweis | Ergänzend | Verbleibende Einschränkung | Technisch erf. | Human-E. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **F-1** | VM als Referenzbetrieb | `accepted` | A0 | HDI A1 — dedizierte Linux-VM (D-015) | ADR-0002, Profil A | Konkrete Werte im DRC, `not-evaluated` | später | **ja** |
| **F-2** | Docker Compose als Pilotlaufzeit | `accepted` | A0 | HDI A1 — bevorzugt (D-016) | ADR-0002 | Keine Compose-Datei, keine Installation | später | **ja** |
| **F-3** | Trennung canonical / derived | `accepted` | **A1** | **ADR-0003** (`accepted`) | Rebuild-Vertrag in `SYSTEM_ARCHITECTURE.md` | Kein Rebuild je ausgeführt | **ja** | **ja** |
| **F-5** | Deployment-Neutralität | `accepted` | A0 | HDI A1 (D-017) | **ADR-0001**, 5 Profile A–E | Profil B nie erprobt | später | **ja** |
| **F-6** | UI- und Wiki-Gates | `accepted` | A0 | HDI A6 (D-024, D-025) | Bedingungen aus Übergabe §9 | Gate-Bedingungen nicht messbar bis zum Benchmarklauf | später | **ja** |

## G — Benchmark

| ID | Kurzbeschreibung | Status | Autorität | Primärer Nachweis | Ergänzend | Verbleibende Einschränkung | Technisch erf. | Human-E. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **G-1** | Mindestens 30 Benchmarkfragen | `accepted` | A2 | `BENCHMARK_QUESTIONS.md` — **36** Fragen, Dataset 2.0.0 | 14 Pflichtfelder je Frage | **Nicht ausgeführt** (R-21) | **ja** | nein |
| **G-2** | Kategorien definiert | `accepted` | A2 | 6 Kategorien A–F zu je 6 | 24 Development / 12 Holdout | Holdout nie ausgewertet | **ja** | nein |
| **G-3** | Erfolgsmetriken definiert | `accepted` | A2 | `EVALUATION_RUBRIC.md` — 4 Metrikgruppen | Rubrik 0/1/2, **9** kritische Fehler | **Pilotziele sind ungemessene Setzungen** (OD-02b) | **ja** | nein |
| **G-4** | Baseline-Verfahren definiert | `accepted` | A2 | `BENCHMARK_PLAN.md` V0/V1/V2 | `BASELINE_PROTOCOL.md`, 13 Erfassungsregeln | Kein Lauf; Token-Schätzmethode offen | **ja** | nein |
| **G-5** | Datenschutzfälle enthalten | `accepted` | A2 | 6 Fragen D-01…D-06 | 4 Korpusfixtures, davon 2 `excluded-from-ai` | Sperrwirkung ungeprüft (R-31) | **ja** | nein |
| **G-6** | Konfliktfälle enthalten | `accepted` | A2 | 5 Konfliktpaare K1–K5 | 9 Konfliktfragen; A0/A1/A2/A6-Ketten | Konflikterkennung nie gemessen | **ja** | nein |

---

## Prüfung der Matrix

| Prüfung | Ergebnis |
| --- | --- |
| **Keine `accepted`-Markierung ohne Nachweis** | **erfüllt** — jedes der 25 Kriterien nennt einen primären Nachweis mit Dokumentverweis |
| **Keine dokumentarische Regel als technische Umsetzung dargestellt** | **erfüllt** — 16 Kriterien tragen „technisch erforderlich: ja"; die Einschränkungsspalte nennt jeweils das offene Risiko |
| **Benchmarkerstellung nicht als Benchmarkausführung dargestellt** | **erfüllt** — alle sechs G-Kriterien tragen „nicht ausgeführt" oder eine gleichwertige Einschränkung |
| **Permission Model nicht als realisierte Zugriffskontrolle dargestellt** | **erfüllt** — E-2 bis E-5 tragen ausdrücklich „nicht durchgesetzt" mit R-25/R-27 |
| **DRC nicht als durchgeführt dargestellt** | **erfüllt** — DRC ist kein Core-Kriterium; F-1 und F-2 verweisen auf `not-evaluated` |

## Summenzeile

*Reproduzierbar aus `G0_SCOPE_LOCK_CRITERIA.md` durch Auszählen der
Core-Required-Zeilen.*

| Kennzahl | Wert |
| --- | --- |
| **Core Required** | **25** |
| **`accepted`** | **25** |
| **`answered`** | **0** |
| **`open`** | **0** |
| **`blocked`** | **0** |

### Nach Autorität

| Autorität der Annahme | Anzahl |
| --- | --- |
| A0 — ausdrückliche Human-Maintainer-Entscheidung | 18 |
| A1 — angenommener ADR | 1 (F-3) |
| A2 — Projektstatus, ohne gesonderte Human-Entscheidung | 6 (Benchmarkblock) |

### Nach technischem Umsetzungsbedarf

*Spaltengenau aus den 25 Kriterienzeilen ausgezählt.*

| Technisch erforderlich | Anzahl | Kriterien |
| --- | --- | --- |
| **`ja`** | **16** | D-1, D-3, D-4, D-5, D-8, E-2, E-3, E-4, E-5, F-3, G-1…G-6 |
| `später` | **7** | A-2, A-4, A-5, F-1, F-2, F-5, F-6 |
| `nein` | **2** | A-1, A-8 |

> **16 von 25 Kriterien beschreiben Kontrollen, die nicht existieren.** Das ist
> kein Mangel der Nachweislage — es ist der ehrliche Zustand eines Projekts,
> das Phase 0 abschließt. G0 sperrt den Scope, nicht die Implementierung.

## Verbleibende Einschränkungen — gesammelt

| Risiko | Betrifft | Status |
| --- | --- | --- |
| **R-20** | Restore nie geprobt | offen |
| **R-21** | Benchmark entworfen, nicht ausgeführt | offen |
| **R-25** | Berechtigungen nicht technisch durchgesetzt | offen |
| **R-27** | Repository- und GitHub-Zugriffe nicht durchgesetzt | offen |
| **R-31** | `excluded-from-ai` ungeprüft | offen |
| **R-32** | Keine Quarantäne für Nicht-Markdown | offen |
| **DRC** | 16 Deployment-Kriterien | `NOT EVALUATED` |
| **OD-05, OD-06** | Konkreter Quellenbestand | offen |
| **OD-26** | Repository-Layout | offen |
| **OD-02b** | Kalibrierung der Budget-Richtwerte | offen |

Keiner dieser Punkte blockiert G0 — alle blockieren die **Umsetzung**.

**Stand nach CBP-WP-008:** Für jeden dieser Punkte ist nun ein Weg und eine
erforderliche Nachweisstufe benannt —
[PHASE_1_EVIDENCE_PLAN.md](../roadmap/PHASE_1_EVIDENCE_PLAN.md). **Kein Punkt
wurde dadurch geschlossen.** Alle Nachweise stehen auf Stufe 1 `dokumentiert`;
die 16 technisch erforderlichen Kriterien beschreiben weiterhin Kontrollen, die
nicht existieren.

## Status

**G0 PASSED WITH NOTES** — entschieden am 2026-07-21 durch den Human
Maintainer (A0). Wortlaut und Auflagen im Entscheidungsblock in
[G0_SCOPE_LOCK_REVIEW.md](G0_SCOPE_LOCK_REVIEW.md).

**Phase 0 COMPLETE · Phase 1 AUTHORIZED FOR PLANNING.**

Die Freigabe bestätigt den Scope, **nicht** die technische Umsetzung: DRC
`NOT EVALUATED`, Benchmark nicht ausgeführt, Berechtigungen nicht durchgesetzt,
keine Capability `implemented`.
