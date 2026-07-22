# ADR-0010 — Ingest-Quarantäne MVP

| Feld | Wert |
| --- | --- |
| Status | **accepted** |
| Datum | 2026-07-22 |
| Entscheider | **Human Maintainer** |
| Angenommen am | **2026-07-22** |
| Autorität | **A0** — vier getrennte direkte Human-Maintainer-Entscheidungen |
| Supersedes | — |
| Superseded by | — |
| Entschieden in | **CBP-WP-013** |
| Belegt durch | ADR-0003 (A1), ADR-0007, ADR-0009, INGEST_QUARANTINE_PLAN (A3), D-019, D-021 |
| Schließt | **keine** offene Entscheidung — OD-05 und OD-06 bleiben offen |

> **Dieser ADR ist angenommen und bindend.** Er trägt Autoritätsklasse **A1**.
> Die zugrunde liegenden Human-Entscheidungen (D-038 bis D-041) tragen **A0**.
>
> **Er beschreibt einen lokalen, synthetisch testbaren Prototyp.** Er ist
> **keine** produktive Quarantäne, **kein** vollständiger Secret-Scanner und
> **kein** PII-Klassifikationssystem. Keine reale Quelle, kein reales Mapping
> und kein produktiver Ingest wird durch diesen ADR autorisiert.

---

## Kontext

Der [INGEST_QUARANTINE_PLAN.md](../roadmap/INGEST_QUARANTINE_PLAN.md) (A3,
CBP-WP-008) beschreibt die Zielpipeline mit **zwölf Schritten** und **zehn
Statuswerten**. Er ist ein Plan — er implementiert nichts. **R-32**
(Nicht-Markdown-Quellen umgehen die Quarantäne) bleibt offen und schließt erst
durch bestandene Negativtests, nicht durch ein Dokument.

CBP-WP-012 hat einen lokalen, fail-closed Runtime Skeleton erstellt. CBP-WP-013
setzt darauf ein **Minimum Viable** der Quarantäne auf: eine eng umrissene,
**synthetisch testbare** Vertrauensgrenze vor jeder Aufnahme. Vier Fragen
mussten entschieden werden, die sich nicht aus der Architektur ableiten lassen:

| Frage | Wirkt auf |
| --- | --- |
| **Wie viel je Intake?** | Hash-, Befund-, Widerruf- und Prüfeindeutigkeit |
| **Wie wird gespeichert?** | Reproduzierbarkeit, Idempotenz, Trennung der Review-Artefakte |
| **Wie tief prüft der Scanner?** | Blockade offensichtlicher Credentials, PII-Kennzeichnung |
| **Was bedeutet ein Ergebnis?** | Verhinderung automatischer Freigabe oder Promotion |

## Entscheidung

### D-038 — Intake-Granularität (Teil A)

**Genau eine ausdrücklich angegebene Markdown-Datei je Intake.**
Keine Verzeichnisrekursion, keine Mehrfachdateien, keine Archive, keine
Symlink-Folgen, keine implizite Dateisuche, kein Zugriff auf
Canonical-Source-Roots.

### D-039 — Quarantänespeicher (Teil B)

**Lokaler content-addressed Dateispeicher** mit unveränderlichem Payload und
atomarem JSON-Manifest. Der Store-Root wird **explizit** angegeben, liegt
**außerhalb** des Core-Repositorys und wird in diesem Work Package
**ausschließlich** in temporären Testverzeichnissen mit synthetischen Daten
verwendet. Objektpfade werden **nur** aus einem validierten SHA-256 abgeleitet.
Der Store ist **weder Canonical Source noch RT-2** und **keine** produktive
Sicherheitsgrenze.

### D-040 — Baseline-Scanner (Teil C)

**Strukturelle Prüfungen plus deterministische Credential- und
PII-Indikatoren.** Blockierende Befunde: Struktur, Symlink, Suffix, Größe,
Leere, UTF-8, NUL, fehlender Synthetic-Marker, Private-Key-Marker,
Credential-Assignment. Nicht blockierende Review-Indikatoren: E-Mail, Telefon.
Die Regeln sind **fest verdrahtet** (keine frei konfigurierbaren regulären
Ausdrücke) und **Indikatoren, keine Tatsachenbehauptung** über ein echtes
Secret oder eine echte Person.

### D-041 — Freigabemodell (Teil D)

**Drei Zustände: `READY_FOR_HUMAN_REVIEW`, `REVIEW_REQUIRED`, `BLOCKED`.**
**Keine automatische Promotion.** Kein Zustand bedeutet `approved`, `released`,
`enabled` oder `indexed`. Ein technischer Scan ersetzt keine fachliche,
datenschutzrechtliche oder sicherheitstechnische Human-Freigabe.

## Trust Boundary

Der Prototyp bildet die Vertrauensgrenze **TB-1** (Pre-Ingest) ab: ein Artefakt
wird geprüft und isoliert, **bevor** irgendeine weitere Verarbeitung möglich
wäre. Die Grenze wird durch die **Synthetic-only-Bedingung** verstärkt: jede
ausführbare Scan- und Stage-Operation verlangt (1) das Flag
`--synthetic-test-only`, (2) eine opake Source Reference mit Präfix
`synthetic:`, (3) den Marker `<!-- synthetic-test-only -->` im Artefakt. Fehlt
eine Bedingung, blockiert die Operation und speichert keinen Payload.

## Konsequenzen

| Wirkung | Beschreibung |
| --- | --- |
| **Datenschutz** | E-Mail- und Telefonindikatoren erzwingen Human Review; **keine** vollständige PII-Erkennung wird behauptet. Records enthalten keine personenbezogenen Inhalte |
| **Secret** | Private-Key- und Credential-Marker blockieren; **keine** vollständige Secret-Erkennung wird behauptet. Es wird **kein** Secret aufgelöst |
| **Portabilität** | Reine Standardbibliothek, kein Netzwerk, kein Dienst. Der Store ist ein lokales Dateilayout ohne Datenbank |
| **Aufbewahrung** | Der Prototyp erzeugt **keine** RT-2 Operational Evidence. Records sind reproduzierbar aus synthetischen Eingaben |
| **Idempotenz** | Identische Wiederholung ist idempotent; abweichender Inhalt unter derselben Identität blockiert |

## Verworfene Alternativen

- **A2 (Verzeichnisbaum je Intake):** vergrößert Fehlerfläche, Symlink- und
  Teilzustandsrisiken; verworfen zugunsten eindeutiger Datei-Granularität.
- **B2 (nur flüchtiger Scan):** kein reproduzierbares Review-Artefakt; verworfen.
- **C2 (nur strukturell):** ließe offensichtliche Credential-Marker passieren;
  verworfen.
- **D2 (automatische Promotion):** verletzt Q2/S3 des Quarantäneplans; verworfen.

## Aussagegrenzen

- Kein produktiver Ingest, keine Aktivierung eines Mappings, keine Indexierung.
- `.gitignore` und OS-Rechte sind **keine** durchgesetzte Sicherheitsgrenze.
- Der Netzwerk-Guard belegt Netzwerkfreiheit der getesteten CLI-Pfade, **nicht**
  Deployment-Isolation, Firewall oder VM-Egress.
- Der Scanner ist ein **Baseline-Indikator**, kein vollständiges Secret- oder
  PII-Klassifikationssystem.

## Offene Folgefragen

| ID | Frage |
| --- | --- |
| **OD-37** | Produktive Quarantäne-Isolation auf der Ziel-VM (KB-03, KB-04): OS-Rechte, getrennte Identität, Unzugänglichkeit für den Indexer — **Deployment Required** |
| **OD-38** | Produktive Secret- und PII-Erkennung: Werkzeugauswahl, Erkennungsgüte, Verfahren nach D-019 — offen |

**OD-05 und OD-06 bleiben offen.** Dieser ADR entscheidet die vier
MVP-Teilfragen, nicht den Ablageort des kanonischen Bestands oder den konkreten
Quellenbestand.

## Verhältnis zum Autoritätsmodell

Ein angenommener ADR (A1) schlägt README (A4), abgeleitete Zusammenfassungen
(A6) und Projektchat-Übergaben (A5). Er wird nur durch einen ausdrücklichen
Human-Maintainer-Beschluss (A0) oder einen späteren ADR verdrängt.
