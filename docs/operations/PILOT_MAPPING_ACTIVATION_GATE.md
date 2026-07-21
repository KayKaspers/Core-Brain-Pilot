# Pilot Mapping Activation Gate

| Feld | Wert |
| --- | --- |
| **Status** | **NOT EVALUATED** |
| Art | Prüfmodell, **kein NDF-Gate** |
| Grundlage | **ADR-0008** (A1), [Specification](../sources/PILOT_SOURCE_MAPPING_SPECIFICATION.md), [Validation](../sources/PILOT_SOURCE_MAPPING_VALIDATION.md) |
| Erfasst in | CBP-WP-010 |
| Autoritätsklasse | A3 |
| Gilt für | jedes einzelne Mapping der Slots **PS-02, PS-03, PS-04** |
| Stand | 2026-07-21 |

> **Dieses Gate wurde nicht ausgeführt.** Es existiert kein Mapping, keine
> angebundene Quelle und kein Prüfergebnis. Der Status `NOT EVALUATED` ist der
> korrekte Ausgangszustand — nicht ein offener Punkt.

---

## Zweck

Ein Mapping erreicht den Zustand **`enabled` ausschließlich über dieses Gate**.
Es beantwortet eine einzige Frage:

> Darf **dieses** Mapping **jetzt** wirksam werden?

**Das Gate wird je Mapping und je Revision durchlaufen**, nicht einmal für alle.
Eine sicherheitsrelevante Änderung setzt es zurück (Regel R4 der Spezifikation).

## Abgrenzung

| Gate | Gegenstand | Status |
| --- | --- | --- |
| **G0** | Produkt- und Architektur-Scope | PASSED WITH NOTES |
| **DRC** | Installationsreife eines Deployments | `NOT EVALUATED` |
| **dieses Gate** | Wirksamwerden **eines einzelnen Mappings** | **`NOT EVALUATED`** |

Dieses Gate ersetzt weder den DRC noch ein NDF Quality Gate. Es ist ein
Prüfmodell im Sinne von **ADR-0005**.

---

## Ergebniswerte

| Wert | Bedeutung | Wer stellt fest |
| --- | --- | --- |
| **`NOT EVALUATED`** | Nicht geprüft — **Ausgangszustand** | — |
| **`BLOCKED`** | Mindestens ein Punkt verletzt | Prüfung oder Mensch |
| **`READY FOR ACTIVATION DECISION`** | Alle 20 Punkte erfüllt, Entscheidung steht aus | Prüfung |
| **`APPROVED FOR ACTIVATION`** | Aktivierung freigegeben | **ausschließlich der Human Maintainer** |
| **`REVOKED`** | Freigabe zurückgenommen | Human Maintainer oder Vorfall |

| # | Regel |
| --- | --- |
| **E1** | **Nur der Human Maintainer darf `APPROVED FOR ACTIVATION` feststellen** |
| **E2** | `READY FOR ACTIVATION DECISION` ist **keine** Freigabe |
| **E3** | Ein einziger nicht erfüllter Punkt ergibt **`BLOCKED`** |
| **E4** | Ein **nicht geprüfter** Punkt zählt wie ein verletzter (fail-closed) |
| **E5** | `REVOKED` erzwingt Deaktivierung und **Derived Cleanup** |
| **E6** | Eine Warnung hebt **nie** ein `BLOCKED` auf |

**E2 ist die Stelle, an der ein Prüfergebnis mit einer Entscheidung verwechselt
werden könnte.** Dass alles geprüft ist, bedeutet nicht, dass jemand es will.

---

## Die 20 Gate-Punkte

| # | Punkt | Nachweis | Regel |
| --- | --- | --- | --- |
| **1** | **Mapping außerhalb des Core-Repositorys gespeichert** | Ablageort im privaten Operator-Workspace belegt | V7, MG-1 |
| **2** | **Schema validiert** | Validierung gegen JSON Schema bestanden | V1, V2 |
| **3** | **Keine unbekannten Felder** | Feldliste vollständig bekannt | V3 |
| **4** | **Secret-Prüfung bestanden** | Scan über alle Felder inklusive `notes` **ohne Fund** | V8, V23 |
| **5** | **Datenklasse bestätigt** | `data_class` ist **nicht** `unknown`, menschlich bestätigt | V9 |
| **6** | **AI-Transfer-Policy bestätigt** | Kombination mit `data_class` konsistent | V10 |
| **7** | **Minimale Rechte bestätigt** | Kein Schreibrecht über das Nötige hinaus | V20 |
| **8** | **Read-only technisch nachgewiesen** | **Schreibversuch scheitert tatsächlich** | V11, V20 |
| **9** | **Subpath-Allowlist bestätigt** | `allowed_subpaths` **nicht leer**, Umfang geprüft | V12 |
| **10** | **Ausschlüsse negativ getestet** | Ein ausgeschlossener Pfad wird nachweislich **nicht** aufgenommen | V13 |
| **11** | **Symlink-Verhalten geprüft** | Kein Ziel außerhalb der Source Boundary erreichbar | V14 |
| **12** | **Quelle erreichbar** | Source Boundary existiert und ist lesbar | V19 |
| **13** | **Revision erfassbar** | `revision_strategy` liefert einen stabilen Wert | V16 |
| **14** | **Tombstone-Konflikt ausgeschlossen** | `mapping_id` nie gelöscht, kein aktiver Vorgänger | V21, V22 |
| **15** | **Operator Review erfolgt** | Fachliche Prüfung dokumentiert | — |
| **16** | **Human Approval erfolgt** | `approval_status: approved` mit `approved_by`, `approved_at` | V17 |
| **17** | **Auditnachweis vorgesehen** | RT-2-Protokollierung für Freigabe und Aktivierung eingerichtet | AE-1…AE-4 |
| **18** | **Backupwirkung klassifiziert** | Zuordnung zu Operator-Workspace (kanonisch) und RT-2 dokumentiert | ADR-0007, RG-4 |
| **19** | **Rollback definiert** | Weg zurück nach `suspended` oder `revoked` inklusive Derived Cleanup benannt | Z7, Z8, D3 |
| **20** | **Aktivierung separat autorisiert** | Ausdrückliche Entscheidung des Human Maintainers, **getrennt** von Punkt 16 | E1, Z13 |

### Warum Punkt 16 und Punkt 20 getrennt sind

**Punkt 16 gibt das Mapping frei. Punkt 20 schaltet es ein.** Beides kann
zeitlich und inhaltlich auseinanderfallen: Ein Mapping darf korrekt und
freigegeben sein und trotzdem noch nicht wirksam werden sollen — etwa weil die
Sicherheitsgrundlage aus CBP-WP-012 fehlt.

Das entspricht Zustandsregel **Z5**: `approved` ist noch nicht `enabled`.

### Punkte mit Negativtest

Fünf Punkte gelten nur als erfüllt, wenn der **verbotene Fall tatsächlich
scheitert** — eine Warnung genügt nicht:

| Punkt | Negativtest |
| --- | --- |
| **8** | Schreibversuch bei `read_only: true` scheitert |
| **10** | Ausgeschlossener Pfad wird nicht aufgenommen |
| **11** | Symlink aus der Boundary heraus wird nicht verfolgt |
| **4** | Synthetisches Secret-Muster wird erkannt und blockiert |
| **6** | `excluded-from-ai` erreicht keinen Modellkontext |

Nachweisstufe **4 `negativ getestet`** nach
[PHASE_1_EVIDENCE_PLAN.md](../roadmap/PHASE_1_EVIDENCE_PLAN.md).

---

## Fail-closed-Verhalten

| Situation | Ergebnis |
| --- | --- |
| Ein Punkt verletzt | **`BLOCKED`** |
| Ein Punkt **nicht geprüft** | **`BLOCKED`** — nicht `READY` |
| Widersprüchliche Nachweise | **`BLOCKED`**, restriktivere Angabe gewinnt |
| Nachweis veraltet (Revision erhöht) | **`NOT EVALUATED`**, Gate neu durchlaufen |
| Secret gefunden | **`BLOCKED`** plus Incident-Verfahren, **SB-02** |
| Unbekannter Zustand | **`BLOCKED`** |

**Der Normalzustand ist Verweigerung.** Es gibt keinen Weg, das Gate durch
Zeitablauf, Wiederholung oder Quittierung zu passieren.

## Rücknahme

| Auslöser | Wirkung |
| --- | --- |
| Human Maintainer widerruft | `REVOKED`, Deaktivierung, **Derived Cleanup** |
| Sicherheitsrelevante Änderung | `NOT EVALUATED`, `enabled: false` (R4) |
| Stop-Bedingung eingetreten | `BLOCKED`, Verarbeitung anhalten |
| Quelle nicht mehr erreichbar | `suspended` — kein automatischer Widerruf |
| Tombstone gesetzt | `REVOKED`, Cleanup, `mapping_id` gesperrt |

## Verhältnis zu den Nachweisstufen

| Gate-Punkte | Erforderliche Stufe |
| --- | --- |
| 1, 2, 3, 13, 14, 18, 19 | **2** `implementiert` |
| 12, 15, 17 | **3** `lokal getestet` |
| **4, 5, 6, 7, 8, 9, 10, 11** | **4** `negativ getestet` |
| **16, 20** | **6** `vom Human Maintainer angenommen` |

**Acht der zwanzig Punkte verlangen Stufe 4.** Sie sind der Grund, warum dieses
Gate ohne CBP-WP-012 (Foundation Runtime Skeleton) nicht durchlaufen werden
kann: Ohne durchgesetzte Dateirechte und Mount-Grenzen ist kein
Read-only-Nachweis führbar.

## Abhängigkeiten

| Voraussetzung | Aus | Grund |
| --- | --- | --- |
| KB-01 bis KB-04 | CBP-WP-012 | Punkte 7, 8, 11 setzen durchgesetzte Rechte voraus |
| KB-08 | CBP-WP-012 | Punkt 4 setzt die Secret-Store-Grenze voraus |
| KB-09 | CBP-WP-012 | Punkt 17 setzt Audit-Logging voraus |
| KB-11 | CBP-WP-012 | Punkt 6 setzt die `excluded-from-ai`-Sperre voraus |
| Validator | spätere Implementierung | Punkte 2, 3 |
| **OD-05, OD-06** | Human Maintainer | Ohne konkrete Quellen gibt es nichts zu aktivieren |
| **OD-34** | Human Maintainer | Punkt 4, sofern `credential_reference` genutzt wird |

**Dieses Gate ist heute nicht durchlaufbar** — nicht, weil es zu streng wäre,
sondern weil die Voraussetzungen nicht existieren.

## Status

**NOT EVALUATED.**

**Es existiert kein Mapping**, keine angebundene Quelle, kein Prüfergebnis und
kein Auditnachweis. Kein Punkt wurde geprüft, keiner erfüllt.

**Dieses Work Package hat das Gate nicht ausgeführt und lässt es nicht
bestehen.** Eine Feststellung von `APPROVED FOR ACTIVATION` ist ausschließlich
dem Human Maintainer vorbehalten.

**Implementierung erlaubt: nein.**
