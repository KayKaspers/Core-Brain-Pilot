# Beispiele — Ingest-Quarantäne (CBP-WP-013)

**synthetic · non-operational · test-only**

Dieses Verzeichnis dokumentiert, wie der lokale, fail-closed
Quarantäneprototyp mit **ausschließlich synthetischen** Testdaten aufgerufen
wird. Es enthält **keine** realen Quellen, **keine** Secrets, **keine**
personenbezogenen Daten und **keinen** produktiven Quarantänespeicher.

## Grenzen

- Genau **eine** ausdrücklich angegebene Markdown-Datei je Intake.
- Jede Scan- und Stage-Operation verlangt die Synthetic-only-Grenze:
  1. das Flag `--synthetic-test-only`,
  2. eine opake Source Reference mit Präfix `synthetic:`,
  3. den Marker `<!-- synthetic-test-only -->` im Artefakt.
- Der Quarantänestore liegt **außerhalb** des Core-Repositorys und wird nur
  in einem **temporären** Verzeichnis verwendet.
- Kein Ergebnisstatus bedeutet `approved`, `released`, `enabled` oder
  `indexed`.
- `quarantine release` verweigert **immer** fail-closed.

## Synthetisches Beispielartefakt

Ein gültiges synthetisches Markdown-Artefakt beginnt mit dem Pflichtmarker:

```markdown
<!-- synthetic-test-only -->
# Synthetische Notiz

Dies ist ein synthetischer Testinhalt ohne Secrets und ohne
personenbezogene Daten.
```

Reproduzierbare PowerShell-Beispiele (temporäre Daten, vollständiges Cleanup)
stehen im Runbook:
[docs/runtime/INGEST_QUARANTINE_RUNBOOK.md](../../docs/runtime/INGEST_QUARANTINE_RUNBOOK.md).

## Zustände

| Status | Bedeutung | Exitcode |
| --- | --- | ---: |
| `READY_FOR_HUMAN_REVIEW` | kein Baseline-Indikator gefunden; **keine** Freigabe | 0 |
| `REVIEW_REQUIRED` | nicht blockierender Indikator; menschliche Prüfung nötig | 5 |
| `BLOCKED` | strukturelle oder blockierende Regel verletzt | 6 |

Ein erfolgreicher Scan ist eine **Voraussetzung**, keine fachliche,
datenschutzrechtliche oder sicherheitstechnische Freigabe.
