# Beispiele — synthetisch und nicht operational

| Feld | Wert |
| --- | --- |
| **Klassifikation** | **synthetic · non-operational · test-only** |
| Erfasst in | CBP-WP-012 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

---

## Was hier gilt

| # | Regel |
| --- | --- |
| 1 | **Alle Beispiele sind synthetisch.** Sie beschreiben keine reale Installation |
| 2 | **Sie sind nicht operational.** Kein Beispiel startet, verbindet oder verarbeitet etwas |
| 3 | **Keine privaten Werte** — keine Hostpfade, keine Repository-URLs, keine Benutzer- oder Organisationsnamen |
| 4 | **Keine Source-Aktivierung** — kein Beispiel aktiviert ein Mapping |
| 5 | **Keine Secret-Referenzen** und erst recht keine Secret-Werte |
| 6 | **Keine produktiven Mappings** |

## Vorhandene Beispiele

| Datei | Zweck |
| --- | --- |
| [`../config/runtime.example.toml`](../config/runtime.example.toml) | Beispielkonfiguration des Runtime Skeletons |

**Weitere Beispieldaten wurden bewusst nicht erzeugt.** Der Skeleton braucht
keine, und jede zusätzliche Datei wäre ein Ort, an dem versehentlich ein realer
Wert landet.

## Was ein gültiges Beispiel nicht bedeutet

Die Beispielkonfiguration validiert erfolgreich. Das bedeutet **strukturelle
Gültigkeit** — nicht:

- dass eine Runtime läuft,
- dass eine Kontrolle durchgesetzt ist,
- dass ein Gate bestanden wurde,
- dass eine Quelle angebunden ist.

`run` verweigert auch mit dieser Konfiguration deterministisch.

## Verwendung

```powershell
py -3.13 -m core.core_brain validate-config --config config/runtime.example.toml
py -3.13 -m core.core_brain doctor --config config/runtime.example.toml
```

Siehe [DEVELOPER_RUNBOOK.md](../docs/runtime/DEVELOPER_RUNBOOK.md).
