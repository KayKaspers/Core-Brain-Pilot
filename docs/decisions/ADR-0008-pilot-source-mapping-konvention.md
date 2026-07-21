# ADR-0008 — Pilot Source Mapping Konvention

| Feld | Wert |
| --- | --- |
| Status | **accepted** |
| Datum | 2026-07-21 |
| Entscheider | **Human Maintainer** |
| Angenommen am | **2026-07-21** |
| Autorität | **A0** — drei getrennte direkte Human-Maintainer-Entscheidungen |
| Supersedes | — |
| Superseded by | — |
| Entschieden in | **CBP-WP-010** |
| Belegt durch | ADR-0006 (A1), ADR-0007 (A1), PILOT_SOURCE_CONTRACT (A2), SOURCE_SLOT_MODEL (A2), D-006, D-019, D-021 |
| Betrifft | PS-02, PS-03, PS-04 |

> **Dieser ADR ist angenommen und bindend.** Er trägt Autoritätsklasse **A1**.
> Die zugrunde liegenden Human-Entscheidungen tragen **A0**.

---

## Kontext

**ADR-0006** trennt logische Source Slots von deploymentspezifischen Mappings.
**ADR-0007** legt fest, wo ein ausgefülltes Mapping liegt: im **privaten
Operator-Workspace**, außerhalb des Core-Repositorys.

Offen war, **wie** ein Mapping aussieht. Drei Fragen mussten getrennt
entschieden werden, weil sie unabhängig voneinander wirken:

| Frage | Wirkt auf |
| --- | --- |
| **Format** | Validierbarkeit, Determinismus, Werkzeugkette |
| **Collection-Strategie** | Retrieval, Berechtigungen, Provenienz |
| **Granularität** | Rechte, Revisionen, Löschung, Tombstones, Freigaben |

Der Planungsstand aus CBP-WP-008
([PILOT_SOURCE_MAPPING_PLAN.md](../roadmap/PILOT_SOURCE_MAPPING_PLAN.md))
beschrieb ein Feldschema, ließ aber alle drei Fragen offen.

---

## Teilentscheidung A — Kanonisches Mappingformat

**SELECT A1 — YAML 1.2 Strict Subset mit JSON-Schema-Validierung**

### Human Notes

*Wortlaut unverändert übernommen:*

> Das Mappingformat soll für Operatoren gut lesbar bleiben und zugleich
> deterministisch validierbar sein.
>
> Zulässig ist nur ein klar begrenzter YAML-1.2-Teilumfang. JSON Schema bildet
> die verbindliche maschinenprüfbare Vertragsgrenze.
>
> Nicht zulässig sind insbesondere mehrdeutige oder erweiterte YAML-Funktionen
> wie Anchors, Aliases, Merge Keys, benutzerdefinierte Tags, doppelte Schlüssel
> und mehrere Dokumente pro Datei.

## Teilentscheidung B — Collection-Strategie

**SELECT B3 — hybride Strategie: Projekt- oder Domänen-Collection mit
zusätzlicher Slot-Kennzeichnung**

### Human Notes

*Wortlaut unverändert übernommen:*

> Collections werden primär nach fachlichem Projekt oder fachlicher Domäne
> gebildet.
>
> Der Source Slot bleibt als verpflichtendes Metadatum erhalten, damit
> Provenienz, Ingest-Regeln, Berechtigungen, Löschung und Audit weiterhin nach
> Quellenart nachvollziehbar sind.
>
> Die Collection allein darf keine Autoritätsklasse, Datenklasse oder
> AI-Transfer-Freigabe verleihen.

## Teilentscheidung C — Mapping-Granularität

**SELECT C1 — genau eine Source Boundary je Mapping**

### Human Notes

*Wortlaut unverändert übernommen:*

> Jedes Mapping beschreibt genau eine eindeutig freigegebene Source Boundary:
>
> - bei PS-02 genau einen Markdown Root,
> - bei PS-03 genau ein Git Repository,
> - bei PS-04 genau einen Handoff Root.
>
> Dadurch bleiben Rechte, Datenklasse, Revision, Verifikation, Freigabe,
> Widerruf, Löschung und Tombstone-Verhalten unabhängig prüfbar.
>
> Mehrere Quellen dürfen nicht durch ein gemeinsames Mapping gekoppelt werden.

---

## Entscheidung

Ein Pilot Source Mapping ist ein **YAML-1.2-Strict-Subset-Dokument**, das
**genau eine Source Boundary** beschreibt, einer **fachlichen Collection**
zugeordnet ist und den **Source Slot** als verpflichtendes Metadatum führt.
**JSON Schema** ist die maschinenprüfbare Vertragsgrenze.

| Gegenstand | Festlegung |
| --- | --- |
| Format | YAML 1.2, eingeschränkter Teilumfang; genau ein Dokument je Datei; UTF-8 |
| Vertragsgrenze | JSON Schema — maschinenprüfbar, verbindlich |
| Collection | **fachlich** (Projekt oder Domäne), nicht nach Slot |
| Slot | **verpflichtendes Metadatum**, nicht Collection-Kriterium |
| Granularität | **eine** Source Boundary je Mapping |
| Ablage ausgefüllter Mappings | **privater Operator-Workspace** (ADR-0007) |
| Ablage von Schema und Regeln | **Core Repository** |

### Drei abgeleitete Grundsätze

| # | Grundsatz | Herkunft |
| --- | --- | --- |
| **M-A** | **Was mehrdeutig geparst werden kann, ist unzulässig.** Ein Mapping, das je nach Parser verschieden gelesen wird, ist keine Vertragsgrundlage | Teil A |
| **M-B** | **Eine Collection verleiht nichts.** Sie gruppiert. Autorität, Datenklasse und AI-Transfer stammen aus Slot, Mapping und Dokument — nie aus der Zugehörigkeit | Teil B |
| **M-C** | **Eine Quelle, ein Mapping.** Was gemeinsam gemappt ist, wird gemeinsam widerrufen — deshalb wird nichts gemeinsam gemappt | Teil C |

**M-B ist die schärfste der drei.** Sie verhindert, dass die Sortierordnung zur
Rechtequelle wird — dieselbe Fehlerklasse wie Slot-Regel 8, nach der die Ablage
keine Autorität verleiht.

---

## Scope

- Mappingformat, Collection-Strategie und Granularität für **PS-02, PS-03,
  PS-04**
- Feldschema, Zustandsmodell, Validierungsregeln, Freigabekette
- Lösch- und Tombstone-Verhalten
- Synthetische Beispiele im Core-Repository

## Non-Goals

| Nicht Gegenstand | Zuständig |
| --- | --- |
| Konkrete Mappings, reale Location References | **OD-05, OD-06** — offen |
| Ablageort des kanonischen Bestands | **OD-05** — offen |
| Secret-Store-Technologie, Credential-Reference-Format | **OD-34** — offen |
| PS-01, PS-05, PS-06, PS-07 | PS-06/PS-07 bleiben `deferred` bis zur Quarantäne |
| JSON-Schema-Datei, Parser, Validator | spätere Implementierung, CBP-WP-013 f. |
| Aktivierung einer Quelle, Ingest, Indexierung | **Aktivierungsgate**, `NOT EVALUATED` |
| Suchprovider, Retrieval | OD-25, P6 |

---

## Konsequenzen

| Gegenstand | Wirkung |
| --- | --- |
| Lesbarkeit | Operatoren bearbeiten Mappings ohne Werkzeug |
| Determinismus | Zwei Läufe über dasselbe Mapping ergeben dieselbe Normalform |
| Werkzeugkette | JSON Schema ist breit verfügbar; kein YAML-spezifischer Validator nötig |
| Betriebsaufwand | **höher** — je Quelle ein eigenes Mapping statt einer Sammeldatei |
| Fehlerfläche | **kleiner** — ein fehlerhaftes Mapping betrifft eine Quelle |
| Collection-Pflege | Zwei Achsen sind zu führen: fachliche Collection **und** Slot |
| Migration | Kein Bestand vorhanden — die Konvention ist heute kostenlos |

**Der höhere Betriebsaufwand aus C1 ist der bewusst gezahlte Preis.** Eine
Sammeldatei wäre bequemer und würde Widerruf, Löschung und Tombstone über
mehrere Quellen verschränken.

## Datenschutzwirkung

**Positiv, aber nicht durchgesetzt.**

| Aspekt | Wirkung |
| --- | --- |
| Trennung | Ausgefüllte Mappings verlassen das Core-Repository nie (ADR-0007) |
| Defaults | `enabled: false`, `read_only: true`, leere Allowlist, `data_class: unknown`, `ai_transfer_policy: forbidden`, `indexing_policy: none`, `mobile_visibility: forbidden` |
| Unbekanntes | **fail-closed** — `unknown` wird wie `excluded-from-ai` behandelt |
| `excluded-from-ai` | erzwingt `ai_transfer_policy: forbidden`; jede andere Kombination wird **abgelehnt**, nicht korrigiert |
| Secrets | **niemals** in einem Mapping; `credential_reference` ist opak und wertfrei |
| Granularität | Ein Widerruf trifft genau eine Quelle |

**Grenze:** Sämtliche Regeln sind **dokumentarisch**. Es existiert kein
Validator, kein Parser und keine technische Durchsetzung. **R-25, R-27, R-30
und R-31 bleiben offen.**

## Berechtigungswirkung

| Aspekt | Wirkung |
| --- | --- |
| Retrieval und Rechte | arbeiten auf der **fachlichen Collection** |
| Provenienz und Ingest-Regeln | folgen dem **Slot** |
| Collection als Rechtequelle | **ausgeschlossen** (M-B) |
| `read_only` | Vorgabe `true`; `false` erfordert eine benennbare A0-Entscheidung |
| Mapping gegen Slot | Das Mapping kann nur **einschränken**, nie erweitern |

Konsistent mit [PERMISSION_MODEL.md](../security/PERMISSION_MODEL.md): Rechte
werden serverseitig gegen Rolle und Ressource geprüft, nicht aus einer
Gruppierung abgeleitet.

## Portabilitätswirkung

| Aspekt | Wirkung |
| --- | --- |
| Deploymentprofile | Alle fünf Profile nutzen dasselbe Schema |
| Ortsbindung | Nur `location_reference` und `location_reference_type` sind ortsabhängig |
| Umzug | Eine Installation zieht um, indem sie ihre Mappings ersetzt |
| Zweite Installation | Braucht eigene Mappings, kein zweites Schema |
| Formatbindung | YAML-Subset plus JSON Schema, beides implementierungsneutral |

## Validierungswirkung

Das Schema ist **maschinenprüfbar**, nicht nur beschrieben. Vollständig in
[PILOT_SOURCE_MAPPING_VALIDATION.md](../sources/PILOT_SOURCE_MAPPING_VALIDATION.md)
— **24 Regeln V1 bis V24**, sämtlich fail-closed.

| Grundsatz | Regel |
| --- | --- |
| Unbekannter Zustand | **blockiert** |
| Konflikt | **blockiert** |
| Fehlende Evidenz | **blockiert** |
| Widerspruch | die **restriktivere** Regel gewinnt |
| Warnung | hebt **nie** automatisch eine Blockade auf |

**Kein Validator existiert.** Die Regeln beschreiben, was ein Validator prüfen
muss.

## Migrationswirkung

**Keine Migration erforderlich.** Es existiert kein Mapping, keine Quelle, kein
Index. Die Konvention greift ab dem ersten Mapping.

Eine spätere Schemaänderung erfolgt über `schema_version`; nicht unterstützte
Versionen blockieren die Aktivierung (V1). Ein Formatwechsel von A1 nach A2
wäre eine Serialisierungsänderung, keine Inhaltsänderung — das JSON Schema
bliebe tragend.

---

## Verworfene und vertagte Alternativen

| Option | Bewertung |
| --- | --- |
| **A2** — kanonisches JSON | **verworfen.** Maschinell eindeutiger, für Operatoren aber schlechter lesbar und ohne Kommentare. Das JSON Schema als Vertragsgrenze wird ohnehin übernommen |
| **DEFER A** | **verworfen.** Ohne Format ist kein Schema und keine Validierung spezifizierbar |
| **B1** — eine Collection je Slot | **verworfen.** Die Collection wäre eine Wiederholung des Slots; fachliches Retrieval hätte keine Achse |
| **B2** — ausschließlich fachlich | **verworfen.** Provenienz und Ingest-Regeln wären nicht mehr nach Quellenart nachvollziehbar |
| **DEFER B** | **verworfen.** Blockiert Retrieval- und Rechteplanung |
| **C2** — mehrere Boundaries je Mapping | **verworfen.** Verschränkt Widerruf, Löschung und Tombstones über Quellen hinweg |
| **DEFER C** | **verworfen.** Ohne Granularität sind Lösch- und Revisionsregeln nicht formulierbar |

## Offene Folgefragen

| Punkt | Register | Status |
| --- | --- | --- |
| Konkreter Ablageort, reale Location References | **OD-05** | **offen** |
| Konkrete Pilotquellen und Nicht-Quellen | **OD-06** | **offen** |
| Secret-Store-Technologie und Credential-Reference-Format | **OD-34** | **offen** |
| Repository-Sichtbarkeit | OD-11 | offen |
| Bildungsvorschrift der `mapping_id` | **neu** | offen — Eigenschaften festgelegt, Vorschrift nicht |
| Zulässige Collection-Namen und ihre Vergabe | **neu** | offen |
| Unterstützte `schema_version`-Werte über `1.0` hinaus | **neu** | offen |
| JSON-Schema-Datei | — | spätere Implementierung |
| RT-2: Aufbewahrung, Integritätsschutz, Backup-Nachweis | **OD-35** | offen |

**Keine dieser Fragen wird durch ADR-0008 beantwortet.** Die Konvention legt
Form und Regeln fest — nicht, welche Quellen es gibt und wo sie liegen.
