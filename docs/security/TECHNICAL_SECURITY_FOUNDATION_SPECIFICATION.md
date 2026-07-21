# Technical Security Foundation Specification

| Feld | Wert |
| --- | --- |
| **Status** | **ACCEPTED FOR IMPLEMENTATION PLANNING** |
| **Nicht** | IMPLEMENTED · DEPLOYED · TESTED · PRODUCTION READY |
| Grundlage | **ADR-0009** (A1), ADR-0004, ADR-0006, ADR-0007, ADR-0008 |
| Entschieden in | **CBP-WP-011** — D-034, D-035, D-036, D-037 (A0) |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

> **Keine Kontrolle dieser Spezifikation existiert technisch.** Kein Test wurde
> ausgeführt. Sämtliche Nachweise stehen auf **Stufe 1 `dokumentiert`**.

---

## 1 — Zweck

Diese Spezifikation überführt die zwölf Kontrollbereiche **KB-01 bis KB-12** in
technisch abnehmbare Anforderungen mit Negativtests, Nachweisen,
Stop-Bedingungen und sicheren Rücksetzwegen.

Sie beantwortet: **Was muss die Foundation Runtime technisch durchsetzen, und
woran erkennt man, dass sie es tut?**

## 2 — Scope

| Gegenstand | Enthalten |
| --- | --- |
| Zwölf Kontrollbereiche | ja |
| Neunstufige Durchsetzungsreihenfolge | ja |
| Identitäten, Ressourcen, Aktionen | ja — Detail im [Identity Model](SERVICE_IDENTITY_AND_PRIVILEGE_MODEL.md) |
| Secret-Vertrag | Verweis — [Secret Contract](SECRET_REFERENCE_AND_PROVIDER_CONTRACT.md) |
| Egress-Grundsatz | Verweis — [Egress Policy](NETWORK_EGRESS_POLICY.md) |
| Operational Evidence | Verweis — [Evidence Policy](../operations/OPERATIONAL_EVIDENCE_POLICY.md) |
| Negativtests und Abnahme | Verweis — [Acceptance Matrix](SECURITY_CONTROL_ACCEPTANCE_MATRIX.md) |
| Readiness Gate | Verweis — [Readiness Gate](../operations/SECURITY_FOUNDATION_READINESS_GATE.md), `NOT EVALUATED` |

## 3 — Non-Goals

| Nicht Gegenstand | Zuständig |
| --- | --- |
| Implementierung, Bereitstellung, Betrieb | **CBP-WP-012** — nicht autorisiert |
| Konkrete Unix-/Container-Identitäten, UID, GID | Deployment, DRC |
| Hostpfade, Ports, IP-Bereiche, Firewallregeln | Deployment, DRC |
| Logging-, Datenbank-, Backup-, Secret-Manager-Technologie | spätere Work Packages |
| Konkrete Aufbewahrungsdauer | **Deployment Required** |
| Testausführung | CBP-WP-012 ff. |

## 4 — System- und Trust Boundaries

| # | Grenze | Verläuft zwischen |
| --- | --- | --- |
| **TB-A** | **Host / VM** | Proxmox-Host und dedizierter Linux-VM — **die Anwendung läuft nie auf dem Host** |
| **TB-B** | **VM / Anwendungsprozess** | Betriebssystem und nicht privilegierten Diensten |
| **TB-C** | **Control Plane / Data Worker** | den beiden logischen Service-Identitäten |
| **TB-D** | **Canonical / Derived** | kanonischem Bestand und RT-1/RT-2/RT-3 |
| **TB-E** | **Core / Operator-Workspace / Runtime** | den drei Datenbereichen aus ADR-0007 |
| **TB-F** | **Secret Store / alles Übrige** | Secret-Bereich und allen drei Datenbereichen |
| **TB-G** | **intern / extern** | privatem Netz und externen Zielen, insbesondere Modellgrenzen |

**TB-G ist die Grenze mit der größten Schadenswirkung.** Ein Fehler dort ist
nicht rückholbar: Was übertragen wurde, ist übertragen.

## 5 — Bedrohungsannahmen

| # | Annahme |
| --- | --- |
| **BA-1** | Ein Anwendungsprozess **kann** kompromittiert werden |
| **BA-2** | Ingestierter Inhalt **kann** Anweisungen enthalten — Prompt Injection ist zu erwarten (R-04) |
| **BA-3** | Eine Fehlkonfiguration ist wahrscheinlicher als ein gezielter Angriff |
| **BA-4** | Der Betreiber ist eine Einzelperson ohne Sicherheitsteam (D-018) |
| **BA-5** | Ein Secret, das einmal abgeflossen ist, gilt als kompromittiert |
| **BA-6** | Promptregeln werden nicht zuverlässig befolgt |
| **BA-7** | Ein Nachweis, der überschrieben werden kann, wird irgendwann überschrieben |

**Aus BA-6 folgt die wichtigste Strukturregel dieser Spezifikation:**
Promptregeln stehen auf Stufe 9 und dürfen **nie** die einzige Ebene einer
Anforderung sein.

## 6 — Identitäten

| Identität | Aufgabe | Erhält **nicht** |
| --- | --- | --- |
| **Control Plane** | Konfiguration, Status, Review- und Freigabevorgänge | Schreibrecht auf Canonical · automatische Publish-Rechte · Secret-**Werte** |
| **Data Worker** | Verarbeitung freigegebener und aktivierter Source Boundaries | Approval-, Administrations- und Publish-Rechte · allgemeine GitHub-Schreibrechte |

**Weitere Rollen** aus `PERMISSION_MODEL.md` (Retrieval Service, Indexer,
Web-UI, MCP/API, Backup Service, Mobile Client, Reviewer, Human Maintainer)
bleiben gültig und werden auf diese beiden Laufzeitidentitäten abgebildet.

**Konkrete Unix- oder Container-Identitäten werden hier nicht festgelegt.**

## 7 — Ressourcen

| Ressource | Klasse | Bereich |
| --- | --- | --- |
| `canonical sources` | kanonisch | Operator-Workspace |
| `operator configuration` | kanonisch | Operator-Workspace |
| `source registry` | kanonisch | Operator-Workspace |
| `secret store` | **gesondert** | außerhalb aller drei Bereiche |
| `rt1 derived data` | abgeleitet | Runtime |
| `rt2 operational evidence` | **Nachweis** | Runtime, getrennt |
| `rt3 transient state` | flüchtig | Runtime |
| `git repository` | kanonisch | Core |
| `github remote` | extern | — |
| `backup storage` | Sicherung | getrennt |
| `network egress` | Kanal | — |
| `model context` | **externe Grenze** | jenseits TB-G |

## 8 — Aktionen

Fünf Aktionsklassen aus `PERMISSION_MODEL.md`, unverändert:

`read` · `draft` · `write with approval` · `publish with approval` ·
`forbidden`

| # | Regel |
| --- | --- |
| **AK-1** | Jede Aktion wird gegen **Rolle, Ressource, Aktion und Approval-Zustand** geprüft |
| **AK-2** | Eine Aktion ohne zugeordnete Klasse ist **`forbidden`** |
| **AK-3** | `draft` erzeugt **keine** Wirkung außerhalb des Entwurfsbereichs |
| **AK-4** | `write with approval` und `publish with approval` benötigen einen **dokumentierten Freigabezustand** |

## 9 — Deny-by-default-Grundsatz

| # | Regel |
| --- | --- |
| **DD-1** | Was nicht ausdrücklich erlaubt ist, ist **verboten** |
| **DD-2** | Ein **unbekannter** Zustand, Wert oder Bezeichner blockiert |
| **DD-3** | Bei Widerspruch gewinnt die **restriktivere** Regel |
| **DD-4** | **Fehlende Evidenz blockiert** |
| **DD-5** | Eine **Warnung hebt nie automatisch eine Blockade auf** |
| **DD-6** | **Erreichbarkeit ist keine Autorisierung** |
| **DD-7** | **Eine Netzwerkerlaubnis ist keine Datenfreigabe** |
| **DD-8** | Ein Fehler in einer Kontrolle führt zu **Verweigerung**, nicht zu Durchlass |

---

## 10 — Die zwölf Kontrollbereiche

### KB-01 — Nicht privilegierter Betrieb

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Keine Anwendungsausführung als root, keine direkte Proxmox-Hostausführung, kein privilegierter Container, keine Host-Administrationsrechte |
| **Bedrohung** | Eine kompromittierte Komponente übernimmt Host oder Nachbardienste (BA-1) |
| **Anforderung** | Der **Start wird verweigert**, wenn eine Privileggrenze verletzt ist — kein Warnstart, kein Degraded Mode |
| **Nachweis** | Effektive Identität je laufendem Prozess; Privilegienflags |
| **Negativtest** | **NT-01** Start als root scheitert · **NT-02** privilegierter Container scheitert |
| **Evidence-Ereignis** | `authentication`, `incident` bei Verstoß |
| **Stop-Bedingung** | **SB-S01** |
| **Rücksetzung** | Dienst anhalten; **nicht** im laufenden Betrieb umkonfigurieren |

### KB-02 — Getrennte Service-Identitäten

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Control Plane und Data Worker als getrennte logische Identitäten mit minimalen, unabhängigen Rechten (**D-034**) |
| **Bedrohung** | Ein übernommener Worker erbt Freigabe- oder Administrationsrechte |
| **Anforderung** | **Keine gemeinsame administrative Identität** · **kein impliziter Rechteübergang** · **Impersonation verboten** |
| **Nachweis** | Zuordnung Identität ↔ Rolle ↔ Ressource, vollständig |
| **Negativtest** | **NT-07** Rollen-Selbstzuweisung scheitert · **NT-08** Approval-Bypass scheitert |
| **Evidence-Ereignis** | `authorization` |
| **Stop-Bedingung** | SB-S09 |
| **Rücksetzung** | Identität deaktivieren; Dienst anhalten |
| **Offen** | Konkrete OS-Identitäten erst im Deployment Mapping |

### KB-03 — Mount- und Speichergrenzen

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Jeder Bereich wird mit dem geringstmöglichen Modus eingebunden |
| **Bedrohung** | Ein Dienst überschreibt kanonisches Wissen oder verlässt seinen Bereich |
| **Anforderung** | `canonical sources` **read-only** · `operator configuration` **read-only für Worker** · RT-1 **gezielt read-write** · **RT-2 nur über den Evidence Writer** · RT-3 **begrenzt read-write** · Secret-Bereitstellung **read-only** · **keine unkontrollierten Host-Mounts** |
| **Nachweis** | Mountliste mit Modus je Identität |
| **Negativtest** | **NT-03** Host-Mount außerhalb Allowlist scheitert · **NT-04** Canonical Write scheitert |
| **Evidence-Ereignis** | `incident` bei Verstoß |
| **Stop-Bedingung** | **SB-S04** |
| **Rücksetzung** | Mounts entfernen; Dienst anhalten |

### KB-04 — Dateisystemrechte

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Deny-by-default auf Dateiebene |
| **Bedrohung** | Direktzugriff unter Umgehung der Anwendung |
| **Anforderung** | Explizite Owner- und Gruppenregeln · **keine world-writable Dateien** · **kein Schreibrecht auf Canonical durch Retrieval oder Ingest** · **Symlink-Escapes blockieren** · sichere Dateierstellung und **atomare Writes** |
| **Nachweis** | Rechteauflistung vor und nach dem Start |
| **Negativtest** | **NT-05** Symlink Escape scheitert · **NT-04** Canonical Write scheitert |
| **Evidence-Ereignis** | `incident` |
| **Stop-Bedingung** | **SB-S04** |
| **Rücksetzung** | Rechte auf den dokumentierten Ausgangszustand |

**KB-04 ist die unterste tragende Ebene.** Versagt sie, sind KB-05 bis KB-07
wirkungslos.

### KB-05 — API-Authentisierung und Autorisierung

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Serverseitige Autorisierung, deny-by-default |
| **Bedrohung** | Ein Client verlangt mehr, als seine Rolle erlaubt |
| **Anforderung** | **Lokale oder private Erreichbarkeit ist keine Autorisierung** (DD-6) · Prüfung von **Rolle, Ressource, Aktion und Approval-Zustand** · **kein Client darf seine Rolle selbst festlegen** · **Fehlerantworten dürfen keine Secrets offenlegen** |
| **Nachweis** | Prüfprotokoll je Rolle × Endpunkt gegen die Matrix 9×12 |
| **Negativtest** | **NT-06** Aufruf ohne Identität scheitert · **NT-07** Rollen-Selbstzuweisung scheitert |
| **Evidence-Ereignis** | `authentication`, `authorization` |
| **Stop-Bedingung** | SB-S09 |
| **Rücksetzung** | Endpunkt deaktivieren — **nicht** die Prüfung abschalten |

### KB-06 — Approval-Zustände

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Wirkung erst nach dokumentierter Freigabe |
| **Bedrohung** | Unbeabsichtigte oder automatische Änderungen |
| **Anforderung** | **Validierung ist keine Freigabe** · **Security Check ist keine Freigabe** · **Human Approval ist keine automatische Aktivierung** · Aktivierung als **getrennter kontrollierter Vorgang** · **Widerruf blockiert Folgeverarbeitung** |
| **Nachweis** | Je Entscheidung **Actor, Zeitpunkt, Grund und Revision** |
| **Negativtest** | **NT-08** Approval-Bypass scheitert |
| **Evidence-Ereignis** | `approval`, `activation`, `suspension`, `revocation` |
| **Stop-Bedingung** | SB-S09 |
| **Rücksetzung** | Freigabezustände zurücksetzen; offene Anträge verwerfen |

Deckungsgleich mit den Validitätsstufen aus ADR-0008.

### KB-07 — Git- und GitHub-Rechte

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Kein pauschaler Schreibzugriff |
| **Bedrohung** | Unkontrollierter Push; Veröffentlichung privaten Bestands |
| **Anforderung** | **Read-only standardmäßig** · **keine automatischen Commits** · **keine automatischen Pushes** · **keine breit berechtigten Tokens** · Draft-Writes nur in **getrennten, ausdrücklich erlaubten** Arbeitsbereichen · **Publish nur nach separater Human-Freigabe** |
| **Nachweis** | Rechteauflistung der verwendeten Zugänge |
| **Negativtest** | **NT-09** automatischer Git-Push scheitert |
| **Evidence-Ereignis** | `authorization`, `incident` |
| **Stop-Bedingung** | **SB-S10** |
| **Rücksetzung** | Zugang entziehen; Token widerrufen |

### KB-08 — Secret-Grenze

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Secret-Werte verlassen den Secret Store nur zur berechtigten Identität |
| **Bedrohung** | Ein Secret gelangt in Git, Log, Report oder Modellkontext (BA-5) |
| **Anforderung** | **Versionierter Referenzvertrag** (**D-035**) · **keine Secret-Werte in Konfiguration, Git, Logs, RT-2 oder Reports** · **fehlende oder ungültige Referenz blockiert** · Bereitstellung nur an die berechtigte Identität · **Rotation ohne Änderung der kanonischen Mapping-ID** · **Widerruf und Rotation vor History Cleanup** |
| **Nachweis** | Scan über Repository, Konfiguration, Logs, RT-2, Context Packs **ohne Fund** |
| **Negativtest** | **NT-10** Secret in Konfiguration · **NT-11** Secret in Log · **NT-12** unbekannte Referenzversion · **NT-13** unbekannter Provider |
| **Evidence-Ereignis** | `secret-resolution-failure`, `incident` |
| **Stop-Bedingung** | **SB-S05**, **SB-S06** |
| **Rücksetzung** | Zugriff sperren; [SECRET_INCIDENT_RESPONSE](SECRET_INCIDENT_RESPONSE.md) — **Rotation vor History Cleanup** |
| **Offen** | Keine Technologie außerhalb der Human-Entscheidung festgelegt |

### KB-09 — Audit und Operational Evidence

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Jede sicherheitsrelevante Entscheidung ist nachweisbar (**D-037**) |
| **Bedrohung** | Ein Vorfall bleibt unentdeckt oder wird nachträglich verwischt (BA-7) |
| **Anforderung** | **RT-2 getrennt von RT-1 und RT-3** · definiertes Ereignismodell · **Actor-, Aktion-, Ressourcen- und Ergebnisnachweis** · **keine geheimen oder vollständigen Quellinhalte im Event** · Manipulationsschutz durch Verkettung · **Aufbewahrung und Backup erforderlich** · **Restore-Nachweis später verpflichtend** |
| **Nachweis** | Abgelehnter Zugriff erscheint im Protokoll; Kette prüfbar |
| **Negativtest** | **NT-18** Event ohne Actor · **NT-19** Kettenbruch wird sichtbar · **NT-20** nachträgliche Manipulation scheitert |
| **Evidence-Ereignis** | alle 17 Ereignisarten |
| **Stop-Bedingung** | **SB-S11**, **SB-S12** |
| **Rücksetzung** | Protokollierung **nicht** abschalten; bei Fehlern Dienst anhalten |

### KB-10 — Netzwerk-Egress

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Deny-by-default mit expliziter Allowlist (**D-036**) |
| **Bedrohung** | Datenabfluss an ein nicht vorgesehenes Ziel |
| **Anforderung** | Explizite **Ziel-, Provider- und Zweckbindung** · zusätzlich **Datenklasse und AI-Transfer-Policy prüfen** · **DNS- oder Netzwerkfreigabe ist keine Inhaltsfreigabe** (DD-7) · Verbindungsversuche zu nicht erlaubten Zielen **blockieren und nachweisen** |
| **Nachweis** | Portauflistung von außen; wirksame Allowlist; Auditeintrag je Entscheidung |
| **Negativtest** | **NT-14** Egress zu nicht erlaubtem Ziel · **NT-15** Redirect zu nicht erlaubtem Ziel |
| **Evidence-Ereignis** | `egress-decision` |
| **Stop-Bedingung** | **SB-S07** |
| **Rücksetzung** | Egress **vollständig sperren** — der sichere Zustand ist kein Netz |
| **Offen** | Keine endgültigen IPs, Ports oder Provider |

### KB-11 — `excluded-from-ai`-Ausgabesperre

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Kein so klassifizierter Inhalt überschreitet eine externe Modellgrenze |
| **Bedrohung** | Leakage über Retrieval, Context Pack, Sammelanfrage oder Web-UI |
| **Anforderung** | **Vor Context-Pack-Erstellung filtern** · **vor externer Übertragung erneut prüfen** · **Sammelanfragen berücksichtigen** · **indirekte und gemischte Treffer blockieren** · **Zielwert null externe Leaks** · **Promptregeln nicht als alleinige Sperre** |
| **Nachweis** | Negativtest mit **synthetischen** Fixtures (D-021) |
| **Negativtest** | **NT-16** externe Übertragung scheitert · **NT-17** gemischtes Context Pack blockiert |
| **Evidence-Ereignis** | `excluded-from-ai-block` |
| **Stop-Bedingung** | **SB-S08** |
| **Rücksetzung** | Retrieval-Pfad anhalten; betroffene Context Packs verwerfen |

**Die zweifache Prüfung ist Absicht.** Ein einziger Filterpunkt fällt mit dem
Code aus, der ihn enthält.

### KB-12 — Backup-Storage-Isolation

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Die Sicherung überlebt eine Kompromittierung der Anwendung |
| **Bedrohung** | Eine übernommene Komponente überschreibt oder löscht Sicherungen |
| **Anforderung** | **Core, Operator-Workspace, RT-2 und Secret Store getrennt klassifizieren** · **RT-1 per Rebuild** · **RT-3 nicht regulär sichern** · **Backupziel nicht vom Anwendungsprozess überschreibbar** · **Restore in getrennte Zielumgebung** · **kein Überschreiben des letzten bekannten guten Backups** |
| **Nachweis** | Rechteauflistung; **durchgeführter Restore** |
| **Negativtest** | **NT-21** Backup durch Anwendungsprozess überschrieben scheitert · **NT-22** Restore ohne Integritätsnachweis scheitert |
| **Evidence-Ereignis** | `backup`, `restore` |
| **Stop-Bedingung** | **SB-S13**, **SB-S14** |
| **Rücksetzung** | Schreibrechte entziehen; Sicherung auf getrenntes Ziel |
| **Offen** | RPO und RTO bleiben **Deployment Required** |

---

## 11 — Technische Durchsetzungsreihenfolge

**Verbindlich, neun Stufen.** Eine spätere Stufe darf eine frühere technische
Kontrolle **nicht ersetzen**.

| Stufe | Ebene | Gilt noch, wenn … |
| --- | --- | --- |
| **1** | **OS-Dateirechte** | … die Anwendung kompromittiert ist |
| **2** | **Prozess- oder Containeridentität** | … der Anwendungsprozess übernommen wurde |
| **3** | **Mount-Modi und Speichergrenzen** | … der Prozess schreiben will |
| **4** | **Secret-Bereitstellung** | … ein Prozess ein Secret anfordert |
| **5** | **API-Authentisierung und Autorisierung** | … ein Client mehr verlangt als vorgesehen |
| **6** | **Netzwerkgrenzen** | … ein Dienst versehentlich exponiert wird |
| **7** | **Approval-Zustände** | … eine Aktion technisch möglich wäre |
| **8** | **Audit und Operational Evidence** | … alles Vorige versagt hat — dann bleibt die Spur |
| **9** | **Promptregeln** | — **nur ergänzend** |

### Zu Stufe 9

**Promptregeln sind keine technische Sicherheitskontrolle.** Sie beschreiben
erwünschtes Verhalten eines Systems, das sich nicht daran halten muss (BA-6).

**Stufe 9 darf nie die einzige Ebene einer Anforderung sein.** Wo eine
Anforderung ausschließlich dort ruht, ist sie **nicht durchgesetzt** — und muss
so berichtet werden. Das ist Stop-Bedingung **SB-S15**.

### Zuordnung Bereiche × Stufen

| Bereich | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KB-01 | | ● | | | | | | | |
| KB-02 | | ● | | | | | | | |
| KB-03 | | | ● | | | | | | |
| KB-04 | ● | | | | | | | | |
| KB-05 | | | | | ● | | | | |
| KB-06 | | | | | | | ● | | |
| KB-07 | | ● | | | ● | | ● | | ○ |
| KB-08 | ● | ● | | ● | | | | | ○ |
| KB-09 | ● | | ● | | | | | ● | |
| KB-10 | | | | | | ● | | | |
| KB-11 | ● | | ● | | ● | ● | | | ○ |
| KB-12 | ● | | | | ● | | | | |

● tragende Stufe · ○ ergänzend

**Kein Bereich ruht allein auf Stufe 9.** Das ist die Prüfregel dieser Tabelle.

## 12 — Tests

Vollständiges Inventar in der
[Acceptance Matrix](SECURITY_CONTROL_ACCEPTANCE_MATRIX.md).

| Typ | Präfix | Anzahl |
| --- | --- | ---: |
| **Negativtests** | `NT-*` | **32** |
| **Positivtests** | `PT-*` | **1** |
| **Gesamt** | | **33** |

**Die geforderte Mindestzahl von 24 echten Negativtests ist erfüllt.**

| # | Regel |
| --- | --- |
| **NTR-1** | Ein Negativtest gilt nur als bestanden, wenn der verbotene Fall **tatsächlich scheitert** |
| **NTR-2** | Eine Warnung genügt **nicht** |
| **NTR-3** | Tests verwenden **synthetische** Daten; **kein reales Secret wird erzeugt** |
| **NTR-4** | Nachweisstufe **4 `negativ getestet`** |
| **NTR-5** | **Ein Positivtest wird nie zur Negativtestzahl gerechnet** |
| **NTR-6** | **Kein Test wurde ausgeführt** — alle 33 stehen auf `PLANNED / NOT EXECUTED` |

## 13 — Operational Evidence

**RT-2**, getrennt von RT-1 und RT-3. Vollständig in der
[Evidence Policy](../operations/OPERATIONAL_EVIDENCE_POLICY.md).

| # | Regel |
| --- | --- |
| **OE-1** | **Logisch append-only**; Korrekturen als Folgeereignis |
| **OE-2** | **Kein Secret, kein vollständiger Quellinhalt** im Event |
| **OE-3** | **Actor nie aus freiem Clienttext** |
| **OE-4** | Verkettung; **Bruch wird sichtbar** |
| **OE-5** | **RT-2 ist kein Cache und keine kanonische Wissensbasis** |
| **OE-6** | Verlust von RT-2 kann **Nachweisverlust** sein |

## 14 — Backup und Restore

| Bereich | Sicherung | Wiederherstellung |
| --- | --- | --- |
| Core Repository | ja | Git plus Backup |
| Operator-Workspace | **ja — kanonisch** | nur aus Backup |
| **Secret Store** | **ja — getrennt** | **nie mit veröffentlichbarem Core-Inhalt** |
| RT-1 | nein | **Rebuild** |
| **RT-2** | **ja** | nur aus Backup |
| RT-3 | nein | gar nicht |

**Backupziel nicht vom Anwendungsprozess überschreibbar** · **Restore in
getrennte Zielumgebung** · **kein Überschreiben des letzten bekannten guten
Backups** · RPO und RTO **Deployment Required**.

## 15 — Stop-Bedingungen

| ID | Auslöser | Autorität |
| --- | --- | --- |
| **SB-S01** | Ausführung als root | **A0** |
| **SB-S02** | Privilegierter Container | **A0** |
| **SB-S03** | Unerwarteter Hostzugriff | **A0** |
| **SB-S04** | Schreibzugriff auf Canonical | **A0** |
| **SB-S05** | Secret in Git, Log oder Context Pack | **A0** |
| **SB-S06** | Unbekannte Secret Reference | A2 |
| **SB-S07** | Nicht erlaubter Egress | **A0** |
| **SB-S08** | `excluded-from-ai`-Leak | **A0** |
| **SB-S09** | Approval-Bypass | **A0** |
| **SB-S10** | Unkontrollierter Git-Push | **A0** |
| **SB-S11** | RT-2-Manipulation | **A0** |
| **SB-S12** | Fehlender Actor im Audit | A2 |
| **SB-S13** | Backupverlust | **A0** |
| **SB-S14** | Restore ohne Integritätsnachweis | A2 |
| **SB-S15** | Kontrolle ruht allein auf Promptregeln | A2 |
| **SB-S16** | Änderung außerhalb des Work-Package-Scopes | **A0** |

Detail je Bedingung — Erkennung, Sofortmaßnahme, Evidenz, Incident-Prozess,
sichere Abschaltung, Wiederaufnahme, Autorität — in der
[Acceptance Matrix](SECURITY_CONTROL_ACCEPTANCE_MATRIX.md).

## 16 — Sichere Abschaltung

| # | Regel |
| --- | --- |
| **SA-1** | **Restriktiver werden ist immer erlaubt**; permissiver nur mit Freigabe |
| **SA-2** | Der sichere Zustand ist **kein Netz, kein Schreibrecht, kein Egress** |
| **SA-3** | Eine Kontrolle wird **nie abgeschaltet, um einen Fehler zu umgehen** — der Dienst wird angehalten |
| **SA-4** | **Protokollierung wird nie abgeschaltet** |
| **SA-5** | Abschaltung erzeugt selbst ein **RT-2-Ereignis** |

## 17 — Spätere Implementierungsnachweise

Zu erbringen in **CBP-WP-012** und folgenden. **Keiner existiert.**

| Bereich | Nachweisart | Zielstufe |
| --- | --- | --- |
| KB-01, KB-02 | Identitätsauflistung + Negativtest | **4** |
| KB-03, KB-04 | Mount- und Rechteauflistung + Negativtest | **4** |
| KB-05, KB-06 | Prüfprotokoll + Negativtest | **4** |
| KB-07 | Rechteauflistung + Negativtest | **4** |
| KB-08 | Scan ohne Fund + Rotationstest | **4** |
| KB-09 | Kettennachweis + Manipulationstest | **4** |
| KB-10 | Allowlist + Redirect-Negativtest | **4** |
| KB-11 | Leaktest mit synthetischen Fixtures | **4** |
| KB-12 | **durchgeführter Restore** | **5** |

Stufen nach
[PHASE_1_EVIDENCE_PLAN.md](../roadmap/PHASE_1_EVIDENCE_PLAN.md).

## 18 — Offene Deploymentwerte

| Wert | Status |
| --- | --- |
| Unix-/Container-Identitäten, UID, GID | **Deployment Required** |
| Dateimodi, Owner, Gruppen | **Deployment Required** |
| Hostpfade, Volume-Namen, Secret-Bereich | **Deployment Required** |
| Ports, IP-Bereiche, VPN-Technologie | **Deployment Required** |
| Egress-Ziele und Provider | **Deployment Required** |
| **Aufbewahrungsdauer für RT-2** | **Deployment Required** |
| RPO, RTO, Backupziel | **Deployment Required** |
| Logging-, Datenbank-, Backuptechnologie | spätere Work Packages |

**Alle im DRC zu prüfen** — Status `NOT EVALUATED`.

## Status

**ACCEPTED FOR IMPLEMENTATION PLANNING.**

**Keine Kontrolle existiert.** Keine Identität angelegt, kein Recht gesetzt,
kein Mount konfiguriert, kein Secret bereitgestellt, keine Egress-Regel
wirksam, kein RT-2-Speicher vorhanden, kein Test ausgeführt.

**R-25, R-27, R-26, R-30, R-31, R-32 und R-20 bleiben offen.**

**Implementierung erlaubt: nein.**
