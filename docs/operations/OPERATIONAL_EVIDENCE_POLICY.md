# Operational Evidence Policy — RT-2

| Feld | Wert |
| --- | --- |
| **Status** | **ACCEPTED FOR IMPLEMENTATION PLANNING** |
| **Nicht** | IMPLEMENTED · DEPLOYED · TESTED |
| Grundlage | **ADR-0009** (A1), **D-037** (A0), ADR-0007 (RT-1/RT-2/RT-3) |
| Erfasst in | CBP-WP-011 |
| Autoritätsklasse | A2 |
| Schließt | **OD-35** — mit Ausnahme der Aufbewahrungsdauer |
| Stand | 2026-07-21 |

> **Es wurde keine Logging-, Datenbank- oder Speichertechnologie ausgewählt.**
> Es existiert kein RT-2-Speicher und kein Ereignis.

---

## Einordnung

**D-037:** RT-2 Operational Evidence wird **logisch append-only** geführt.

| RT-2 ist | RT-2 ist **nicht** |
| --- | --- |
| Nachweis über Entscheidungen und Ereignisse | **kein Cache** |
| Getrennt von RT-1 und RT-3 | **keine kanonische Wissensbasis** |
| Aufbewahrungs- und sicherungspflichtig | **nicht zuverlässig rekonstruierbar** |

> **Grundsatz S-D: Ein Nachweis, der überschrieben werden kann, ist kein
> Nachweis.**

**Der Verlust von RT-2 kann einen Nachweisverlust darstellen.** Kein Rebuild
stellt ein Auditereignis wieder her — anders als bei RT-1, wo genau das der
Vertrag ist.

## Append-only-Semantik

| # | Regel |
| --- | --- |
| **AO-1** | **Ereignisse werden angefügt, nie geändert** |
| **AO-2** | **Korrekturen erfolgen durch nachvollziehbare Folgeereignisse** |
| **AO-3** | **Kein stillschweigendes Überschreiben** bestehender Nachweise |
| **AO-4** | Ein Löschversuch ist selbst ein Ereignis |
| **AO-5** | Die protokollierende Komponente kann **eigene Einträge nicht entfernen** |

**Zu AO-2:** Ein falsch protokolliertes Ereignis wird nicht repariert, sondern
**richtiggestellt**. Beide Fassungen bleiben sichtbar — die Korrektur ist Teil
des Nachweises, nicht sein Ersatz.

---

## Ereignismodell

| # | Feld | Bedeutung |
| --- | --- | --- |
| 1 | `event_schema_version` | Version des Ereignisschemas; unbekannt blockiert |
| 2 | `event_id` | **Stabile, eindeutige** Ereignisidentität |
| 3 | `event_type` | Eine der 17 Ereignisarten |
| 4 | `occurred_at` | **Eindeutig normalisierter** Zeitstempel |
| 5 | `actor_reference` | Rollenkennung — **nie aus freiem Clienttext** |
| 6 | `service_identity` | Control Plane oder Data Worker |
| 7 | `action` | Aktionsklasse |
| 8 | `resource_reference` | Kennung der betroffenen Ressource |
| 9 | `policy_revision` | Fassung der wirksamen Regel |
| 10 | `mapping_revision` | Fassung des betroffenen Mappings |
| 11 | `correlation_id` | Verkettung zusammengehöriger Ereignisse |
| 12 | `result` | `allowed`, `blocked`, `failed`, `completed` |
| 13 | `reason_code` | Strukturierter Grund — keine Freitextfehlermeldung |
| 14 | `data_class` | Datenklasse des betroffenen Gegenstands |
| 15 | `previous_event_hash` | **Verkettung zum Vorgänger** |
| 16 | `event_hash` | Hash dieses Ereignisses |
| 17 | `retention_class` | Aufbewahrungsklasse |
| 18 | `backup_status` | Sicherungsstand |

### Feldregeln

| # | Regel |
| --- | --- |
| **F-1** | **`event_id` ist stabil und eindeutig** |
| **F-2** | **`occurred_at` ist eindeutig normalisiert** — eine Zeitzone, ein Format |
| **F-3** | **`actor_reference` wird nie aus freiem Clienttext übernommen** — serverseitig bestimmt |
| **F-4** | **Kein Secret im Event** — auch nicht gekürzt, maskiert oder gehasht |
| **F-5** | **Keine vollständigen Quellinhalte im Event** — Kennungen statt Inhalt |
| **F-6** | `reason_code` ist **strukturiert**, damit Fehlermeldungen nichts preisgeben |
| **F-7** | `previous_event_hash` bildet eine **lückenlose Kette** |

**F-4 und F-5 zusammen:** Ein Auditereignis beschreibt, **dass** etwas geschah
und **worauf** es sich bezog — nie **was** darin stand. Sonst wird das
Auditprotokoll selbst zur Datenschutzlücke.

## Integritätsschutz

| # | Regel |
| --- | --- |
| **INT-1** | **Hashverkettung oder gleichwertiger Manipulationsschutz** |
| **INT-2** | **Eine fehlende oder gebrochene Verkettung wird sichtbar** — sie wird nicht stillschweigend repariert |
| **INT-3** | Ein Kettenbruch ist ein **Vorfall** (SB-S11), kein Fehler |
| **INT-4** | Der Manipulationsschutz gilt **auch gegenüber der schreibenden Komponente** |
| **INT-5** | **Keine Technologiewahl in diesem Work Package** |

**Zu INT-2:** Ein System, das eine gebrochene Kette selbsttätig neu aufbaut,
hat keinen Integritätsschutz, sondern eine Reparaturfunktion. Der Bruch **muss**
stehenbleiben und sichtbar sein.

## Aufbewahrung

| # | Regel |
| --- | --- |
| **RET-1** | **Aufbewahrung ist verpflichtend** |
| **RET-2** | Die **Dauer ist deploymentspezifisch** und **Deployment Required** |
| **RET-3** | **Der Ablauf einer Frist darf keine aktive Incident-, Legal- oder Restore-Sperre übergehen** |
| **RET-4** | `retention_class` wird je Ereignis gesetzt |
| **RET-5** | Ein Ablauf ohne Sperre erzeugt selbst ein Ereignis |

**RET-3 ist die wichtigste Regel dieses Abschnitts.** Eine automatische
Löschung, die während eines laufenden Vorfalls greift, vernichtet genau die
Nachweise, die gebraucht werden.

## Backup und Restore

| # | Regel |
| --- | --- |
| **BR-1** | **RT-2 ist sicherungspflichtig** |
| **BR-2** | **Wiederherstellung nur aus Backup** — Rebuild leistet nichts |
| **BR-3** | Das Backupziel ist **vom Anwendungsprozess nicht überschreibbar** |
| **BR-4** | **Restore in eine getrennte Zielumgebung** |
| **BR-5** | **Kein Überschreiben des letzten bekannten guten Backups** |
| **BR-6** | **Restore mit Integritätsnachweis** — die Kette wird geprüft |
| **BR-7** | Backup und Restore erzeugen selbst Ereignisse |
| **BR-8** | RPO und RTO sind **Deployment Required** |

## Ereignisarten

| # | Art | Auslöser |
| --- | --- | --- |
| 1 | `authentication` | Identitätsfeststellung, auch fehlgeschlagene |
| 2 | `authorization` | Rechteentscheidung, auch abgelehnte |
| 3 | `approval` | Menschliche Freigabe |
| 4 | `activation` | Wirksamwerden eines Mappings |
| 5 | `suspension` | Aussetzung |
| 6 | `revocation` | Widerruf |
| 7 | `mapping-change` | Revisionswechsel |
| 8 | `ingest-decision` | Aufnahme oder Ablehnung |
| 9 | `secret-resolution-failure` | Resolver blockiert |
| 10 | `egress-decision` | Netzentscheidung, erlaubt **und** blockiert |
| 11 | `excluded-from-ai-block` | Sperre gegriffen |
| 12 | `deletion` | Löschung |
| 13 | `tombstone` | Tombstone gesetzt |
| 14 | `rebuild` | Derived Data neu erzeugt |
| 15 | `backup` | Sicherung |
| 16 | `restore` | Wiederherstellung |
| 17 | `incident` | Stop-Bedingung eingetreten |

**Bemerkenswert bei 2, 10 und 11:** Auch **abgelehnte** Vorgänge erzeugen
Ereignisse. Ein Protokoll, das nur Erfolge verzeichnet, ist für die Aufklärung
eines Vorfalls wertlos.

## Ausgeschlossene Inhalte

| Ausgeschlossen | Grund |
| --- | --- |
| **Secret-Werte** | F-4 — auch nicht gekürzt oder gehasht |
| **Vollständige Quellinhalte** | F-5 |
| `excluded-from-ai`-Inhalte | Datenklassengrenze |
| Personennamen, E-Mail-Adressen | Rollenkennungen statt Klarnamen |
| Vollständige Adressen mit Parametern | Zielkennung genügt |
| Freitext aus Clientangaben | F-3, F-6 |

## Negativtests

| # | Test | Erwartung |
| --- | --- | --- |
| **NT-18** | Ereignis ohne `actor_reference` | **abgelehnt** |
| **NT-19** | Kettenbruch | **sichtbar**, nicht repariert |
| **NT-20** | Nachträgliche Manipulation eines Ereignisses | **erkannt und abgelehnt** |
| **NT-28** | Secret-Wert in einem Ereignisfeld | **abgelehnt**, SB-S05 |
| **NT-29** | Actor aus freiem Clienttext | **abgelehnt** |
| **NT-30** | Aufbewahrungsablauf bei aktiver Incident-Sperre | **Löschung unterbleibt** |
| **NT-31** | Schreibende Komponente löscht eigenen Eintrag | **scheitert** |
| **NT-22** | Restore ohne Integritätsnachweis | **abgelehnt** |

## Verhältnis zu OD-35

**OD-35 ist geschlossen.** Die offenen Punkte waren **Aufbewahrungsfrist,
Integritätsschutz und Backup-/Restore-Nachweis**:

| Punkt | Stand |
| --- | --- |
| **Integritätsschutz** | **entschieden** — Verkettung oder gleichwertig, Bruch sichtbar (INT-1…INT-5) |
| **Backup- und Restore-Nachweis** | **entschieden** — verpflichtend, mit Integritätsprüfung (BR-1…BR-8) |
| **Aufbewahrungspflicht** | **entschieden** — verpflichtend (RET-1) |
| **Konkrete Aufbewahrungsdauer** | **bleibt Deployment Required** — im DRC zu prüfen |

**Die Dauer wird nicht als allgemeine Architekturentscheidung erfunden.** Sie
hängt von rechtlichen und betrieblichen Rahmenbedingungen ab, die der Human
Maintainer je Installation setzt.

## Offene Deploymentwerte

| Wert | Status |
| --- | --- |
| **Aufbewahrungsdauer je `retention_class`** | **Deployment Required** |
| Speichertechnologie | spätere Work Packages |
| Hashverfahren | CBP-WP-012 |
| Backupziel, RPO, RTO | **Deployment Required** |
| Ablageort von RT-2 | **Deployment Required** |

## Status

**Es existiert kein RT-2-Speicher, kein Ereignis, kein Integritätsschutz und
kein Backup.** Keine Technologie wurde ausgewählt.

**R-20 bleibt offen** — es wurde kein Restore durchgeführt.

**Implementierung erlaubt: nein.**
