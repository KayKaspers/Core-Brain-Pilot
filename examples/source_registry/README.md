# Beispiele — Source Registry (CBP-WP-014)

**synthetic · non-operational · test-only**

Dieses Verzeichnis dokumentiert, wie der lokale, **deaktivierte** und
fail-closed Source-Registry-Prototyp mit **ausschließlich synthetischen**
Metadaten aufgerufen wird. Es enthält **keine** realen Quellen, **keine**
Pfade oder URLs, **keinen** Source-Inhalt und **keine** produktive Registry.

## Grenzen

- Jede schreibende Operation verlangt die Synthetic-only-Grenze:
  1. das Flag `--synthetic-test-only`,
  2. `synthetic_test_only = true` in der Definition,
  3. `source_reference` mit Präfix `synthetic:`,
  4. `activation_enabled = false`, `content_access_enabled = false`,
     `network_enabled = false`.
- Der Registry-Root liegt **außerhalb** des Core-Repositorys und wird nur in
  einem **temporären** Verzeichnis verwendet.
- Jede Registrierung erzeugt ausschließlich den Zustand `REGISTERED_DISABLED`.
- Retirement ist ein **append-only** Event; es gibt **keine** Reaktivierung und
  **keine** Record-Löschung.
- `source-registry activate` verweigert **immer** fail-closed.
- Kein Zustand bedeutet `approved`, `mapped`, `activated`, `ingestible`,
  `indexed` oder `retrievable`.

## Synthetische Beispiel-Definition

Eine gültige synthetische Definition enthält ausschließlich normalisierte
Metadaten — keinen Pfad, keine URL, keinen Inhalt:

```toml
schema_version = "1.0"
namespace = "synthetic-demo"
source_key = "notes-alpha"
display_name = "Synthetische Notizsammlung Alpha"
collection_key = "demo-collection"
domain_key = "demo-domain"
source_kind = "markdown"
data_class = "internal"
ai_eligibility = "restricted"
owner_role = "operator"
source_reference = "synthetic:demo-notes-alpha"
synthetic_test_only = true
activation_enabled = false
content_access_enabled = false
network_enabled = false
```

Reproduzierbare PowerShell-Beispiele (temporäre Daten, vollständiges Cleanup)
stehen im Runbook:
[docs/runtime/SOURCE_REGISTRY_RUNBOOK.md](../../docs/runtime/SOURCE_REGISTRY_RUNBOOK.md).

## Zustände und Exitcodes

| Kommando | Bedeutung | Exitcode |
| --- | --- | ---: |
| `register` (gültig) | Record im Zustand `REGISTERED_DISABLED` | 0 |
| `validate-definition` (gültig) | Definition strukturell gültig | 0 |
| Synthetic-Grenze verletzt / ungültige Definition | blockiert | 8 |
| abweichende Definition derselben Identität | Konflikt | 9 |
| unbekannte Source ID | nicht gefunden | 10 |
| `activate` | verweigert immer | 11 |

Ein erfolgreicher `register` ist ausschließlich eine technische Registrierung
synthetischer Metadaten — **keine** Freigabe, **kein** Mapping, **keine**
Aktivierung.
