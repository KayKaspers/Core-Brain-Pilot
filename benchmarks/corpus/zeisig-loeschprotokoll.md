---
source_id: ZEI-LOESCHPROTOKOLL
title: Zeisig Löschprotokoll
project: Zeisig
source_type: log
authority_class: A2
data_class: internal
revision: 1
reviewed_at: 2026-07-08
freshness_status: current
verification_status: verified
valid_from: 2026-07-08
valid_until: null
ai_transfer: allowed
conflict_refs: []
test_fixture: true
---

# Zeisig — Löschprotokoll

Tombstone-Einträge für entfernte Quellen. Die Einträge bleiben dauerhaft
bestehen, damit Löschungen nachvollziehbar sind.

## Tombstone ZEI-ALTBESTAND-2025

| Feld | Wert |
| --- | --- |
| `source_id` | `ZEI-ALTBESTAND-2025` |
| Titel | Zeisig Altbestand 2025 |
| Gelöscht am | 2026-07-08 |
| Grund | Bestand vollständig in `ZEI-STATUS-2026-07` überführt |
| Letzte Revision | 4 |
| Status | **gelöscht** |

Der Inhalt dieser Quelle existiert nicht mehr und ist nicht wiederherstellbar.
Eine Frage nach ihrem Inhalt ist **nicht beantwortbar**; korrekt ist der
Hinweis auf die Löschung.

## Erwartetes Verhalten nach Rebuild

Nach einem Rebuild darf `ZEI-ALTBESTAND-2025` in keinem Index, keinem
Embeddingbestand und keinem Context Pack mehr auffindbar sein.
