# Source Registry MVP — lokaler, deaktivierter Prototyp

| Feld | Wert |
| --- | --- |
| Erfasst in | **CBP-WP-014** |
| Autoritätsklasse | A2 (technische Beschreibung) |
| Entscheidungen | D-042 bis D-045, [ADR-0011](../decisions/ADR-0011-deterministische-source-registry.md) |
| Grundlage | ADR-0007, ADR-0008, ADR-0009, ADR-0010 |
| Stand | 2026-07-22 |

> **Dies ist ein lokaler, synthetisch testbarer, deaktivierter Prototyp.** Er
> ist **keine** produktive Registry, **kein** Source Mapping, **keine**
> Aktivierung, **kein** Ingest, **kein** Index und **kein** Retrieval.

---

## Trust Boundary

Die Registry sitzt **vor** jeder Aktivierung und jedem Mapping. Sie
katalogisiert Identität, Klassifikation und einen minimalen Lifecycle, ohne
eine Source Boundary oder einen Zugriffsweg zu definieren. Es gibt **keinen**
Pfad von einem Registry-Record zu Source-Inhalt, Mapping, Collection oder Index.

Die **Synthetic-only-Grenze** ist technisch durchgesetzt. Jede schreibende
Operation verlangt gleichzeitig:

1. das Flag `--synthetic-test-only`,
2. `synthetic_test_only = true` in der Definition,
3. `source_reference` mit Präfix `synthetic:`,
4. `activation_enabled = false`, `content_access_enabled = false`,
   `network_enabled = false`.

Fehlt eine Bedingung, **blockiert** die Operation mit stabilem Reason Code und
schreibt **keinen** Record und **kein** Event.

## Identitätsmodell (D-042)

Die logische Identität besteht ausschließlich aus Identitätsschema-Version,
`namespace` und `source_key`. Die Source ID ist `src-` + die ersten 24
Hex-Zeichen des SHA-256 dieser Identität — **kein** Display Name, **kein**
Pfad, **keine** URL, **kein** Inhalt. Dieselbe Identität ergibt dieselbe ID;
eine abweichende Identität oder Definition unter bestehender ID blockiert.

## Definition

Genau 15 Felder, fail-closed validiert. `namespace`, `source_key`,
`collection_key`, `domain_key`, `owner_role` sind normalisierte ASCII-Slugs
(`[a-z0-9]` mit Bindestrichen). Pfadseparatoren, `..`, URL-Indikatoren
(`://`, `http:`, `www.`) und Steuerzeichen blockieren. `source_reference`
beginnt mit `synthetic:`. Keine freien Metadatenfelder, keine Mapping- oder
Secret-Referenz.

## Policy

14 Pflichtfelder, fail-closed:
[config/source_registry_policy.example.toml](../../config/source_registry_policy.example.toml).
`allow_activation`, `allow_content_access`, `allow_network`, `allow_updates`,
`allow_deletion` gleich `true` blockieren; `allow_retirement` gleich `false`
blockiert. Leere Allowlists und unzulässige Maximalwerte blockieren.
Environment und CLI überschreiben nichts.

## Record

17 Felder, unveränderlich, kanonisches sortiertes JSON. Enthält **keinen**
Pfad, **keine** URL, **keinen** Inhalt, **keinen** Mapping-Locator, **keinen**
Secret-Wert. Initialzustand `REGISTERED_DISABLED`. `registered_at` ist
UTC-normalisiert und injizierbar.

## Retirement-Event (D-044)

Append-only, unveränderlich, 9 Felder. `event_type = RETIRED`,
`reason_code = HUMAN_REQUESTED_SYNTHETIC_RETIREMENT`,
`previous_state = REGISTERED_DISABLED`, `resulting_state = RETIRED`. Die
Event-ID (`evt-` + 24 Hex) ist deterministisch aus nicht geheimen Eventdaten
abgeleitet und schließt `occurred_at` aus, damit ein idempotentes Retirement
dieselbe ID ergibt. Keine Freitextbegründung, keine Pfade, keine Reaktivierung,
keine Record-Löschung.

## Storage (D-043)

Root außerhalb des Core-Repositorys, kein Symlink. Struktur:

```text
records/<source-id>.json           # unveränderlicher Record
events/<source-id>/<event-id>.json # append-only Retirement-Event
catalog/catalog.json               # atomar ersetzter, abgeleiteter Katalog
```

Pfade ausschließlich aus validierten IDs. Atomare Schreibweise (Temp-Datei,
`fsync`, `os.replace`). Records und Events werden nicht überschrieben; der
Katalog wird atomar ersetzt. Kein Schreiben außerhalb des Roots.

## Catalog (D-045)

Deterministisch nach `source_id` sortiert, ausschließlich aus Records und
Events abgeleitet. Kopf: `catalog_schema_version`, `generated_at`,
`record_count`, `registered_disabled_count`, `retired_count`. Jeder Eintrag
enthält **nur** 10 minimierte Felder — **keine** `source_reference`, keinen
Definition Hash, keinen Owner-Freitext, keinen Pfad, keine URL. Ein
beschädigter Record blockiert die **gesamte** Katalogerzeugung; es entsteht
**kein** Teilkatalog.

## Zustände und Exitcodes

| Zustand / Ergebnis | Bedeutung | Exitcode |
| --- | --- | ---: |
| `REGISTERED_DISABLED` | registriert, deaktiviert | `register` 0 |
| Definition gültig | strukturell valide | `validate-definition` 0 |
| Synthetic-Grenze verletzt / ungültige Definition / Storage-Verstoß | blockiert | **8** `SOURCE_REGISTRY_BLOCKED` |
| abweichende Definition/Identität | Konflikt | **9** `SOURCE_REGISTRY_CONFLICT` |
| unbekannte Source ID | nicht gefunden | **10** `SOURCE_REGISTRY_NOT_FOUND` |
| `activate` | verweigert immer | **11** `SOURCE_REGISTRY_ACTIVATION_BLOCKED` |

Exitcode 0 bei `register` bedeutet ausschließlich: ein synthetischer
Metadatenrecord wurde technisch registriert und ist `REGISTERED_DISABLED`. Er
bedeutet **nicht** `approved`, `mapped`, `activated`, `ingestible`, `indexed`
oder `retrievable`.

## Keine Aktivierung

`source-registry activate` verweigert unabhängig von Record- und
Lifecycle-Zustand (Exit 11) und öffnet den Speicher nicht. Kein Zustand erzeugt
Mapping Approval, Mapping Activation, Source Boundary, Source-Zugriff,
Quarantäne-Promotion, Collection-Eintrag, Index-Eintrag, Context Pack oder
externen Transfer.

## Nicht implementierte Kontrollen

- Reale Quellenanbindung, Source Mapping, Aktivierung, Ingest, Indexierung, Retrieval.
- Produktive Isolation auf OS-Ebene — **OD-37**, Deployment Required.
- Produktive Secret-/PII-Erkennung — **OD-38**.
- RT-2 Operational Evidence, Secret-Auflösung, Netzwerkzugriff.
