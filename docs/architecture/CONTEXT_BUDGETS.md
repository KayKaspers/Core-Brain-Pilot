# Context Budgets B0–B4 — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-002 |
| Autoritätsklasse | A2 |
| Quelle | Projektübergabe §8 (A5), Übergabe §7 (Suchleiter) |
| Stand | 2026-07-20 |

Ein Context Budget begrenzt, **wie viel Quellkontext** in eine Bearbeitung
fließen darf. Es ist ein Eingabeparameter der Aufgabe, kein Nachgedanke und
keine Obergrenze, die man ausschöpfen sollte.

---

## Abgrenzung: NDF Prompt Mode ≠ Core-Brain Context Budget

Das sind zwei verschiedene Dinge. Sie werden regelmäßig verwechselt; die
Verwechslung ist als Risiko R-24 erfasst.

| | **NDF Prompt Mode** | **Core-Brain Context Budget** |
| --- | --- | --- |
| Herkunft | Nova Development Framework v1.0.0 (A1) | Core Brain Pilot, Übergabe §8 (A5) |
| Regelt | Umfang des **Agentenauftrags** — wie viel Governance, Regeln und Phasenkontext ein Work Package mitführt | Umfang des **Quellkontexts** — wie viele Wissensquellen für eine Frage geladen werden dürfen |
| Werte | **Full**, **Standard**, **Short** | **B0** bis **B4** |
| Gilt für | Work Packages | Retrieval und Beantwortung |
| Festgelegt durch | Nova | Fragestellung und Budgetvorgabe |

Ein Work Package kann Prompt Mode `Full` und Context Budget `B1` haben: der
Auftrag führt vollständige Governance mit, die inhaltliche Recherche bleibt
trotzdem eng begrenzt. CBP-WP-002 selbst ist ein Beispiel — Prompt Mode `Full`,
Context Budget `B2`.

> **„Lean" ist ausschließlich der Name von B1.**
> Es ist **kein** NDF Prompt Mode. Die Formulierung „Lean Mode bevorzugen" in
> Projektübergabe §14 bezieht sich auf sparsamen Kontext, nicht auf einen
> NDF-Modus dieses Namens. Siehe Widerspruch W-01 in
> [../discovery/SOURCE_RECONCILIATION.md](../discovery/SOURCE_RECONCILIATION.md)
> und Entscheidung OD-12.

---

## Quellenzahlregel

Grundlage aller Budgets, aus Projektübergabe §7:

```text
Normalfall:        eine Quelle
erweiterter Fall:  höchstens drei Quellen
größerer Fall:     begründete Eskalation oder Aufteilung der Aufgabe
```

Die Bauanleitung (Seite 3) formuliert strenger — „genau eine beste Datei
öffnen". Die Übergabe erweitert diese Regel ausdrücklich für Core Brain.

**Eine Quelle** meint ein kanonisches Dokument, nicht eine Datei beliebiger
Größe. Der Index selbst zählt nicht als Quelle: ihn zu lesen ist Schritt 1 der
Suchleiter und in jedem Budget enthalten.

---

## Die fünf Budgets

### B0 — Micro

| Attribut | Festlegung |
| --- | --- |
| Geeignete Aufgaben | Genau eine einfache Faktenfrage mit eindeutiger Antwort |
| Maximaler Quellenumfang | **1 Quelle**, in der Regel **1 Abschnitt** |
| Erlaubte Kontextarten | Index, ein Quellabschnitt |
| Zielgröße Quellkontext | ≤ 2.000 Token |
| Erwartete Rückmeldelänge | 1–5 Sätze |
| Reviewtiefe | Keine — Antwort mit Quellenangabe genügt |
| Eskalation | Wenn zwei Quellen nötig werden oder die Antwort strittig ist → B1 |

*Beispiel:* „Welche Autoritätsklasse hat ein angenommener ADR?"

### B1 — Lean

| Attribut | Festlegung |
| --- | --- |
| Geeignete Aufgaben | Kleine, klar begrenzte Arbeitsfrage; Statusabfrage; kleine Dokumentkorrektur |
| Maximaler Quellenumfang | **1 Quelle**, mehrere Abschnitte zulässig |
| Erlaubte Kontextarten | Index, eine Quelle, aktueller Projektstatus |
| Zielgröße Quellkontext | ≤ 8.000 Token |
| Erwartete Rückmeldelänge | 1–3 Absätze |
| Reviewtiefe | Sichtprüfung durch den Anfragenden |
| Eskalation | Wenn eine zweite Quelle erforderlich wird → B2 |

*Beispiel:* „Welche offenen Entscheidungen blockieren derzeit G0?"

### B2 — Standard

| Attribut | Festlegung |
| --- | --- |
| Geeignete Aufgaben | Normales Work Package; Architekturteilfrage; Dokumentationsreview |
| Maximaler Quellenumfang | **höchstens 3 Quellen** |
| Erlaubte Kontextarten | Index, bis zu drei Quellen, Projektstatus, betroffene Register |
| Zielgröße Quellkontext | ≤ 25.000 Token |
| Erwartete Rückmeldelänge | Strukturierter Bericht |
| Reviewtiefe | Prüfungen mit Evidenz, Bericht an Nova |
| Eskalation | Wenn eine vierte Quelle nötig wird → B3 mit Begründung |

**Standardfall für Work Packages.** CBP-WP-002 läuft in B2.

### B3 — Extended

| Attribut | Festlegung |
| --- | --- |
| Geeignete Aufgaben | Komplexe Entscheidung innerhalb eines begrenzten Scopes; Quellenabgleich; Gate-Vorbereitung |
| Maximaler Quellenumfang | Weiterhin möglichst **höchstens 3 Hauptquellen**; ergänzende Quellen nur belegt |
| Erlaubte Kontextarten | Wie B2, zusätzlich externe Referenzdokumentation und Evidenz aus Git |
| Zielgröße Quellkontext | ≤ 60.000 Token |
| Erwartete Rückmeldelänge | Strukturierter Bericht mit Entscheidungsvorlage |
| Reviewtiefe | Vollständige Prüfmatrix; Human-Maintainer-Review |
| Eskalation | Nur nach Prüfung der B4-Pflichtfragen |

**B3 verlangt eine ausdrückliche Begründung** im Work Package: warum drei
Hauptquellen nicht genügen.

### B4 — Exceptional

| Attribut | Festlegung |
| --- | --- |
| Geeignete Aufgaben | Ausnahmefall. Migration, vollständige Bestandsprüfung, Gate-Entscheidung mit breiter Evidenz |
| Maximaler Quellenumfang | Nicht pauschal begrenzt, aber einzeln zu begründen |
| Erlaubte Kontextarten | Alle, jeweils benannt |
| Zielgröße Quellkontext | Keine Zielgröße — Umfang ist zu rechtfertigen, nicht auszuschöpfen |
| Erwartete Rückmeldelänge | Vollständiger Bericht mit Eskalationsprotokoll |
| Reviewtiefe | Human-Maintainer-Freigabe **vor** Ausführung |
| Eskalation | Entfällt — B4 ist die Endstufe |

> **B4 ist nie Standardmodus.** Projektübergabe §8 hält das ausdrücklich fest.

#### Pflichtfragen vor jeder B4-Nutzung

Alle sechs Fragen sind schriftlich zu beantworten und dem Work Package
beizulegen. Ein einziges „ja" bei den ersten fünf spricht gegen B4:

1. **Ist der Scope zu groß?**
2. **Muss das Work Package geteilt werden?**
3. **Ist der Index unzureichend?**
4. **Sind Quellen zu monolithisch?**
5. **Wird unnötiger Kontext geladen?**
6. **Kann ein eigenes Analyseartefakt erstellt werden**, das die Frage künftig
   in einem kleineren Budget beantwortbar macht?

Frage 6 ist die konstruktive: wiederholter B4-Bedarf ist ein Symptom
fehlender Verdichtung, kein Kapazitätsproblem.

#### Eskalationsprotokoll

Jede B4-Nutzung wird protokolliert mit Datum, Anlass, den sechs Antworten,
tatsächlich geladenem Umfang und der Freigabe des Human Maintainers. Häufen
sich Einträge, ist das ein Befund über die Architektur des Wissensbestands.

---

## Übersicht

| Budget | Name | Quellen | Zielgröße | Freigabe |
| --- | --- | --- | --- | --- |
| B0 | Micro | 1 Abschnitt | ≤ 2.000 Token | keine |
| B1 | Lean | 1 Quelle | ≤ 8.000 Token | keine |
| B2 | Standard | ≤ 3 Quellen | ≤ 25.000 Token | keine |
| B3 | Extended | ≤ 3 Hauptquellen, begründet | ≤ 60.000 Token | Begründung im WP |
| B4 | Exceptional | begründet | keine Zielgröße | **vorab durch Human Maintainer** |

---

## Status der Zahlenwerte

Die Token-Zielgrößen sind **Richtwerte zur Kalibrierung**, keine gemessenen
Schwellen. Sie stammen nicht aus den Originalquellen — die Übergabe fordert
Budgets, ohne Zahlen zu nennen — sondern sind in CBP-WP-002 als erster
prüfbarer Ansatz gesetzt worden.

Sie sind gegen den Benchmark (G0 Bereich G) zu validieren und danach
anzupassen. Bis dahin gilt: die **Quellenzahl** ist die harte Grenze, die
Tokenzahl die weiche.

Erfasst als offene Entscheidung OD-02 in
[../../project-system/DECISION_REGISTER.md](../../project-system/DECISION_REGISTER.md).

## Verhältnis zur Suchleiter

Ein Budget begrenzt, **wie viel** geladen wird. Die Brain-First-Suchleiter in
[ARCHITECTURE_PRINCIPLES.md](ARCHITECTURE_PRINCIPLES.md) legt fest, **in
welcher Reihenfolge** gesucht wird. Beide zusammen ergeben das
Retrieval-Verhalten; keines ersetzt das andere.
