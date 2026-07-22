# Ingest Quarantine MVP — lokaler, fail-closed Prototyp

| Feld | Wert |
| --- | --- |
| Erfasst in | **CBP-WP-013** |
| Autoritätsklasse | A2 (technische Beschreibung) |
| Entscheidungen | D-038 bis D-041, [ADR-0010](../decisions/ADR-0010-ingest-quarantaene-mvp.md) |
| Grundlage | [INGEST_QUARANTINE_PLAN.md](../roadmap/INGEST_QUARANTINE_PLAN.md) (A3), ADR-0003, ADR-0007, ADR-0009 |
| Stand | 2026-07-22 |

> **Dies ist ein lokaler, synthetisch testbarer Prototyp.** Er ist **keine**
> produktive Quarantäne, **kein** vollständiger Secret-Scanner und **kein**
> PII-Klassifikationssystem. Keine reale Quelle, kein reales Mapping, kein
> produktiver Ingest, keine Indexierung.

---

## Trust Boundary

Der Prototyp bildet die **Pre-Ingest-Vertrauensgrenze (TB-1)** ab: ein Artefakt
wird strukturell geprüft, gescannt und isoliert, **bevor** irgendeine weitere
Verarbeitung möglich wäre. Es gibt **keinen** automatischen Pfad von einem
Artefakt in einen kanonischen Bestand, einen Index oder eine Collection.

Die Grenze wird durch die **Synthetic-only-Bedingung** technisch verstärkt.
Jede ausführbare Scan- und Stage-Operation verlangt gleichzeitig:

1. das Flag `--synthetic-test-only`,
2. eine opake Source Reference mit Präfix `synthetic:` (nur `[A-Za-z0-9._:-]`),
3. den Marker `<!-- synthetic-test-only -->` im Artefakt.

Fehlt eine Bedingung, **blockiert** die Operation mit einem stabilen Reason
Code und speichert **keinen** Payload.

## Komponenten

| Modul | Verantwortung |
| --- | --- |
| `quarantine/models.py` | Enums, Finding-Codes, Policy-, Scan- und Record-Modelle (unveränderlich) |
| `quarantine/policy.py` | Fail-closed Validierung der Policy |
| `quarantine/scanner.py` | Deterministische strukturelle, Kodierungs-, Credential- und PII-Indikatoren |
| `quarantine/store.py` | Content-addressed Store, atomare Schreibweise, Idempotenz, Kollision |
| `quarantine/pipeline.py` | Orchestrierung: Synthetic-Gate, Intake, einmaliges Lesen, Scan, Record |

## Policy

13 Pflichtfelder, fail-closed. Beispiel:
[config/quarantine_policy.example.toml](../../config/quarantine_policy.example.toml).

- Unbekanntes Feld, unbekannte Schema-Version, fehlendes Feld → **blockiert**.
- `max_bytes` muss positiv und konservativ begrenzt sein; leere Suffixliste → **blockiert**.
- `release_enabled = true` oder `network_enabled = true` → **blockiert**.
- Environment und CLI überschreiben **keine** Policy-Werte.
- **Keine** frei konfigurierbaren regulären Ausdrücke.

## Scanner — Befundcodes

| Code | Schwere | Bedeutung |
| --- | --- | --- |
| `QF-STRUCTURE-NOT-REGULAR` | blocking | keine reguläre Datei (Verzeichnis, Device, Pipe) |
| `QF-STRUCTURE-SYMLINK` | blocking | Symlink |
| `QF-STRUCTURE-SUFFIX` | blocking | Suffix nicht erlaubt |
| `QF-STRUCTURE-SIZE` | blocking | größer als `max_bytes` |
| `QF-STRUCTURE-EMPTY` | blocking | leere Datei |
| `QF-ENCODING-UTF8` | blocking | kein striktes UTF-8 oder unerlaubtes Steuerzeichen |
| `QF-CONTENT-NUL` | blocking | NUL-Byte |
| `QF-SYNTHETIC-MARKER-MISSING` | blocking | Pflichtmarker fehlt |
| `QF-CREDENTIAL-PRIVATE-KEY-MARKER` | blocking | Private-Key-Marker |
| `QF-CREDENTIAL-ASSIGNMENT` | blocking | Credential-Zuweisung |
| `QF-PII-EMAIL-INDICATOR` | review | E-Mail-Indikator |
| `QF-PII-PHONE-INDICATOR` | review | Telefonindikator |

Befunde enthalten **niemals** einen Inhaltsauszug, einen Pfad oder einen Wert —
höchstens Code, Schwere und eine normalisierte Zeilennummer. Die Erkennung ist
ein **Indikator**, keine Tatsachenbehauptung über ein echtes Secret oder eine
echte Person.

## Store

Logische Struktur unter einem expliziten Root **außerhalb** des Repositorys:

```text
objects/sha256/<prefix>/<digest>.blob   # unveränderlicher Payload
records/<quarantine-id>.json            # kanonisches Manifest, sortierte Schlüssel
```

- Objektpfade **nur** aus validiertem SHA-256.
- Atomare Schreibweise (exklusive Temp-Datei, `fsync`, `os.replace`).
- Identische Wiederholung idempotent; abweichende Kollision blockiert.
- Kein Schreiben außerhalb des Store-Roots; keine Hardlinks oder Symlinks.

## Record

14 Felder, minimiert. Enthält **keinen** Eingabepfad, **keinen** Inhalt,
**keinen** Secret-Wert. `source_reference` ist opak und beginnt mit
`synthetic:`. `quarantine_id` ist deterministisch aus `source_reference`,
`content_sha256` und `policy_sha256` abgeleitet. `created_at` ist
UTC-normalisiert und injizierbar.

## Zustände und Exitcodes

| Status | Bedeutung | Exitcode |
| --- | --- | ---: |
| `READY_FOR_HUMAN_REVIEW` | kein Indikator; **keine** Freigabe | **0** |
| `REVIEW_REQUIRED` | nicht blockierender Indikator; Human Review nötig | **5** |
| `BLOCKED` | strukturelle oder blockierende Regel verletzt | **6** |
| — | `quarantine release` verweigert immer | **7** |

Exitcode 0 bedeutet ausschließlich: die lokale Operation wurde technisch
abgeschlossen und kein Baseline-Indikator wurde gefunden. Er bedeutet **nicht**
`approved`, `released`, `enabled`, `indexed` oder „sicher für externe
Übertragung".

## Keine Promotion

`quarantine release` verweigert unabhängig vom Recordstatus (Exit 7) und
verändert keine Datei. Kein Zustand erzeugt automatisch Mapping Approval,
Mapping Activation, Source Registry Entry, Collection Entry, Index Entry,
Context Pack oder externen Transfer.

## Nicht implementierte Kontrollen

- Produktive Isolation auf OS-Ebene (KB-03/KB-04) — **OD-37**, Deployment Required.
- Vollständige Secret- oder PII-Erkennung — **OD-38**.
- Reale Quellenregistrierung, Datenklassifizierung, Autoritätsvergabe, Human
  Review, Freigabe, Indexierung, Auditkette (Schritte 1, 5–12 des Plans).
- RT-2 Operational Evidence, Secret-Auflösung, Netzwerkzugriff.

## Verhältnis zum Zwölf-Schritte-Plan

Der MVP setzt eine **Teilmenge** des
[INGEST_QUARANTINE_PLAN.md](../roadmap/INGEST_QUARANTINE_PLAN.md) um: die
strukturelle Aufnahme in einen isolierten Bereich (Schritt 2), die Formatprüfung
(Schritt 3) und einen **Baseline**-Scan (Schritt 4, ohne Anspruch auf
Vollständigkeit). Die Planschritte 1 und 5 bis 12 sowie die zehn Planzustände
bleiben unimplementiert. **R-32 bleibt offen.**
