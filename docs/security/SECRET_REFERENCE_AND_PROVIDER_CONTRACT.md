# Secret Reference and Provider Contract

| Feld | Wert |
| --- | --- |
| **Status** | **ACCEPTED FOR IMPLEMENTATION PLANNING** |
| **Nicht** | IMPLEMENTED · DEPLOYED · TESTED |
| Grundlage | **ADR-0009** (A1), **D-035** (A0), D-006, SECRET_INCIDENT_RESPONSE |
| Erfasst in | CBP-WP-011 |
| Autoritätsklasse | A2 |
| Vertragsversion | **`v1`** |
| Schließt | **OD-34** |
| Stand | 2026-07-21 |

> **Dieses Dokument enthält kein Secret, keine reale Referenz, keinen realen
> Provider und keinen Hostpfad.** Alle Beispiele sind synthetisch.

---

## Grundsatz

> **S-B: Eine Referenz ist kein Secret.** Sie verweist, ohne zu verraten.

Der Core kennt ausschließlich **Referenzen**. Werte existieren nur im Secret
Store und werden der berechtigten Service-Identität für die notwendige Dauer
bereitgestellt.

## Referenzformat

```text
cbp-secret:v1:<provider>:<opaque-id>
```

| Bestandteil | Bedeutung | Regel |
| --- | --- | --- |
| `cbp-secret` | Feste Kennung | unveränderlich |
| `v1` | **Vertragsversion** | unbekannte Version **blockiert** |
| `<provider>` | Registrierter **Resolver-Typ** | unbekannter Provider **blockiert** |
| `<opaque-id>` | Undurchsichtige Kennung | **enthält keinen Secret-Wert** |

### Was eine Referenz nicht enthält

| Verboten | Grund |
| --- | --- |
| **Secret-Wert oder Fragment** | die Referenz wäre selbst ein Secret |
| **Hostpfad** | verrät die Ablage und bindet an ein Deployment |
| **Zugangsdaten** | dasselbe Problem in anderer Form |
| Benutzername, Organisationsname | Personenbezug und Provenienzleck |
| Rateable Klartextbedeutung | eine „sprechende" ID verrät den Zweck |

## Vertragsregeln

| # | Regel | Verhalten bei Verletzung |
| --- | --- | --- |
| **SR-1** | **Die Referenz ist kein Secret** | Fund eines Werts → **Blocker**, SB-S05 |
| **SR-2** | **Unbekannte Version blockiert** | kein Fallback auf `v1` oder eine ältere Fassung |
| **SR-3** | **Unbekannter Provider blockiert** | kein Standardresolver |
| **SR-4** | **Fehlende Referenz blockiert** | kein Leerwert, kein Weiterlaufen |
| **SR-5** | **Resolverfehler blockiert** | **kein Retry-Durchlauf ohne Secret** |
| **SR-6** | **Secret-Werte werden nicht geloggt** | auch nicht gekürzt, maskiert oder gehasht in RT-2 |
| **SR-7** | **Secret-Werte erscheinen nicht in Fehlermeldungen** | Fehler nennt die **Referenz**, nie den Wert |
| **SR-8** | **Keine Übergabe über Umgebungsvariablen** | auf einem Linux-System für andere Prozesse lesbar |
| **SR-9** | **Keine Übergabe über Kommandozeilen** | dito, zusätzlich in der Prozessliste sichtbar |
| **SR-10** | Bereitstellung **nur für die notwendige Dauer und Identität** | zweckgebunden |
| **SR-11** | **Rotation ändert nicht zwingend die Referenz** | die Referenz ist stabil, der Wert nicht |
| **SR-12** | **Widerruf blockiert weitere Verwendung** | sofort, nicht nach Ablauf |

**SR-8 und SR-9 sind die wirksamsten Einzelregeln.** Umgebungsvariablen und
Kommandozeilen sind die beiden Kanäle, über die Secrets auf einem
Mehrbenutzersystem am häufigsten unbeabsichtigt sichtbar werden.

### Verbotene Ablageorte

Secret-**Werte** erscheinen **niemals** in:

| Ort | |
| --- | --- |
| Git | Core-Repository und jedes andere |
| Mapping- oder Konfigurationsdateien | auch nicht im Operator-Workspace |
| **Umgebungsvariablen** | SR-8 |
| **Kommandozeilen** | SR-9 |
| Logs oder **Operational Evidence (RT-2)** | SR-6 |
| Context Packs | Modellkontextgrenze |
| Fehlermeldungen | SR-7 |
| **Implementation Reports** | auch nicht auszugsweise |

---

## Pilot-Provider — OS-protected file provider

**D-035:** Für den ersten lokalen Pilot wird ein durch Betriebssystemrechte
geschützter Secret-Dateibereich verwendet.

| Eigenschaft | Regel |
| --- | --- |
| **Speicherbereich** | **außerhalb** von Core-Repository, Operator-Workspace **und** Runtime-Datenbereich |
| **Konkrete Position** | **deploymentspezifisch** — hier nicht festgelegt |
| **Provisionierung** | **außerhalb des Anwendungsprozesses** — die Anwendung legt keine Secrets an |
| **Leserechte** | **nur die erforderliche Service-Identität** |
| **Bereitstellung** | **read-only** |
| **Verzeichnisfreigabe** | **keine** an nicht berechtigte Prozesse |
| **Sicherung** | **nie zusammen mit veröffentlichbarem Core-Inhalt** |
| **Git** | **keine Secret-Werte** in Git oder Backlogdokumenten |
| **Rotation und Widerruf** | **müssen möglich sein** |

**Der vierte Bereich.** ADR-0007 definierte drei Datenbereiche — Core,
Operator-Workspace, Runtime. Der Secret Store liegt außerhalb **aller drei**.
Er ist kein vierter Wissensbereich, sondern ein gesonderter Schutzbereich mit
eigenem Sicherungsvertrag (KB-12).

### Warum kein externer Secret Manager im Pilot

Ein externer Manager setzt eine Technologiewahl, eine Betriebsinfrastruktur und
eigene Zugangsdaten voraus — die es alle nicht gibt. **Der Vertrag hält den Weg
offen:** Ein späterer Wechsel ist ein **Resolver-Wechsel**, kein
Vertragswechsel. Die Referenzform bleibt, die Mappingkonvention aus ADR-0008
bleibt unberührt.

## Resolver-Vertrag

| Schritt | Verhalten |
| --- | --- |
| 1 | Referenz **parsen** — Formatverstoß blockiert |
| 2 | **Version prüfen** — unbekannt blockiert (SR-2) |
| 3 | **Provider prüfen** — unbekannt blockiert (SR-3) |
| 4 | **Identität prüfen** — nicht berechtigt blockiert |
| 5 | **Zweck prüfen** — nicht zugeordnet blockiert |
| 6 | Wert **read-only bereitstellen**, für die notwendige Dauer |
| 7 | **Nutzung protokollieren** — als Ereignis, **ohne Wert** |

**Bei jedem Fehler in Schritt 1 bis 5:** Verweigerung plus
`secret-resolution-failure` in RT-2 — mit **Referenz**, nie mit Wert.

## Rotation und Widerruf

| Vorgang | Wirkung |
| --- | --- |
| **Rotation** | Der Wert ändert sich, **die Referenz bleibt**. Keine Änderung an Mapping oder `mapping_id` |
| **Widerruf** | Die Referenz wird ungültig; **weitere Verwendung blockiert sofort** |
| **Kompromittierung** | **Rotation vor History Cleanup** — verbindliche Reihenfolge aus [SECRET_INCIDENT_RESPONSE.md](SECRET_INCIDENT_RESPONSE.md) |

**Zur Reihenfolge:** Ein bereinigtes Repository mit einem weiterhin gültigen
Secret ist gefährlicher als ein unbereinigtes mit einem rotierten — im ersten
Fall glaubt man, fertig zu sein.

---

## Synthetische Beispiele

**synthetic · non-operational · test-only**

```text
# GÜLTIGE FORM — synthetisch, nicht auflösbar
cbp-secret:v1:example-file-provider:placeholder-reference-0001
cbp-secret:v1:example-file-provider:placeholder-reference-0002
```

```text
# UNGÜLTIG — verletzt SR-2, unbekannte Version
cbp-secret:v0:example-file-provider:placeholder-reference-0003
cbp-secret:v9:example-file-provider:placeholder-reference-0004
```

```text
# UNGÜLTIG — verletzt SR-3, unbekannter Provider
cbp-secret:v1:example-unregistered-provider:placeholder-reference-0005
```

```text
# UNGÜLTIG — verletzt SR-1, enthält einen Pfad
cbp-secret:v1:example-file-provider:placeholder-with-path-segment
```

> Alle Kennungen sind **Platzhalter ohne Bedeutung**. `example-file-provider`
> ist **kein registrierter Providername** — die Registrierung erfolgt in
> CBP-WP-012. Kein Beispiel ist auflösbar, keines enthält einen Wert.

## Fehlerverhalten

| Situation | Ergebnis | Ereignis |
| --- | --- | --- |
| Formatverstoß | **blockiert** | `secret-resolution-failure` |
| Unbekannte Version | **blockiert** | `secret-resolution-failure` |
| Unbekannter Provider | **blockiert** | `secret-resolution-failure` |
| Referenz fehlt | **blockiert** | `secret-resolution-failure` |
| Identität nicht berechtigt | **blockiert** | `authorization` |
| Zweck nicht zugeordnet | **blockiert** | `authorization` |
| Resolver nicht erreichbar | **blockiert** — kein Weiterlaufen | `secret-resolution-failure` |
| **Wert in einem Feld gefunden** | **Blocker** | `incident`, **SB-S05** |

## Spätere technische Nachweise

Zu erbringen in **CBP-WP-012**. **Keiner existiert.**

| # | Nachweis | Art | Zielstufe |
| --- | --- | --- | --- |
| 1 | Resolver umgesetzt | NW-IMP | 2 |
| 2 | **Kein Secret-Wert in Repository, Konfiguration, Logs, RT-2, Context Packs** | **NW-SEC** | **4** |
| 3 | **Unbekannte Version blockiert** | **NW-NEG** | **4** |
| 4 | **Unbekannter Provider blockiert** | **NW-NEG** | **4** |
| 5 | **Nicht berechtigte Identität erhält keinen Wert** | **NW-NEG** | **4** |
| 6 | **Keine Übergabe über Umgebungsvariablen oder Kommandozeile** | **NW-NEG** | **4** |
| 7 | **Rotation ohne Referenzänderung** | NW-RUN | 3 |
| 8 | **Widerruf blockiert sofort** | NW-NEG | 4 |
| 9 | Secret Store nicht mit Core-Inhalt gesichert | NW-CFG | 2 |
| 10 | Human-Abnahme | NW-HUM | 6 |

## Offene Deploymentwerte

| Wert | Status |
| --- | --- |
| Konkreter Speicherort des Secret-Bereichs | **Deployment Required** |
| Dateimodi und berechtigte Identität | **Deployment Required** |
| Registrierte Providernamen | CBP-WP-012 |
| Externer Secret Manager | später, ohne Vertragswechsel |
| Bereitstellungsmechanismus im Detail | CBP-WP-012 |

## Verhältnis zu OD-34

**OD-34 ist geschlossen.** Die offene Frage lautete: *Secret-Store-Technologie
und Credential-Reference-Format.* Beides ist entschieden — ein versionierter,
providerneutraler Referenzvertrag und ein OS-geschützter Dateiprovider für den
Pilot.

**Nicht entschieden und bewusst offen:** der konkrete Ablageort, die
Dateimodi, die registrierten Providernamen und ein späterer externer Manager.
Diese Werte sind **Deployment Required**, keine Architekturfragen.

## Status

**Es existiert kein Secret Store, kein Resolver und keine Referenz.** Kein
Secret wurde erzeugt, gespeichert oder bereitgestellt.

**R-01 bleibt offen** — der Vertrag verhindert, dass eine Referenz zum Secret
wird. Er ersetzt keine Erkennung.

**Implementierung erlaubt: nein.**
