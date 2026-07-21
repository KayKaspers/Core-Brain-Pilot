# Service Identity and Privilege Model

| Feld | Wert |
| --- | --- |
| **Status** | **ACCEPTED FOR IMPLEMENTATION PLANNING** |
| **Nicht** | IMPLEMENTED · DEPLOYED · TESTED |
| Grundlage | **ADR-0009** (A1), **D-034** (A0), ADR-0004, PERMISSION_MODEL |
| Erfasst in | CBP-WP-011 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

Dieses Dokument definiert **logische** Service-Identitäten. Es enthält **keine
Unix-Benutzer, keine Gruppen, keine UID- oder GID-Werte und keine Hostpfade**.

---

## Zwei logische Identitäten

**D-034:** Control Plane und Data Worker werden als getrennte logische
Service-Identitäten mit **minimalen, voneinander unabhängigen Rechten**
geführt.

| Identität | Kennung | Aufgabe |
| --- | --- | --- |
| **Control Plane** | `svc-control-plane` *(logisch)* | Konfiguration, Status, Review- und Freigabevorgänge |
| **Data Worker** | `svc-data-worker` *(logisch)* | Verarbeitung freigegebener und aktivierter Source Boundaries |

> Die Kennungen sind **logische Bezeichner**, keine Betriebssystemnamen. Die
> Abbildung auf konkrete Identitäten erfolgt im Deployment Mapping.

### Control Plane

| Darf | Darf **nicht** |
| --- | --- |
| Allgemeine und private Konfiguration **im erforderlichen Umfang** lesen | **Canonical Sources verändern** |
| Status- und Approval-Vorgänge verwalten | **Secret-Werte anzeigen** |
| Freigabezustände setzen und dokumentieren | **automatisch publizieren** |
| RT-2-Ereignisse über die Evidence-Schnittstelle erzeugen | **Worker-Rechte voraussetzen oder erben** |

### Data Worker

| Darf | Darf **nicht** |
| --- | --- |
| **Ausschließlich `approved` und `enabled`** Source Boundaries lesen | **Approval-Rechte** besitzen |
| Nur benötigte Secret-Bereitstellungen lesen | **Administrationsrechte** besitzen |
| **Nur definierte RT-1- und RT-3-Bereiche** beschreiben | **Publish-Rechte** besitzen |
| RT-2-Ereignisse **ausschließlich über die Evidence-Schnittstelle** erzeugen | **allgemeine GitHub-Schreibrechte** besitzen |
| | Canonical Sources verändern |
| | RT-2 direkt beschreiben |

> **Grundsatz S-A:** **Verarbeitung erteilt keine Freigabe.** Wer Daten liest,
> darf sie nicht freigeben.

---

## Trust Boundaries

| # | Grenze | Bedeutung |
| --- | --- | --- |
| **TB-C1** | Control Plane ↔ Data Worker | **Keine gemeinsame administrative Identität**; kein Rechteübergang in beide Richtungen |
| **TB-C2** | Beide ↔ Canonical | Lesend, nie schreibend ohne dokumentierte Freigabe |
| **TB-C3** | Beide ↔ Secret Store | Nur die berechtigte Identität, nur read-only, nur zweckgebunden |
| **TB-C4** | Data Worker ↔ RT-2 | **Nur über die Evidence-Schnittstelle**, nie direkt |
| **TB-C5** | Beide ↔ externes Netz | Deny-by-default; Egress an Identität gebunden |

---

## Ressourcenmatrix

Aktionsklassen: `R` read · `D` draft · `WA` write with approval ·
`PA` publish with approval · `✗` forbidden · `append` nur anfügen

| Ressource | Control Plane | Data Worker |
| --- | --- | --- |
| `canonical sources` | **R** | **R** — nur `approved` + `enabled` |
| `operator configuration` | **R** | **R** — read-only |
| `source registry` | **WA** | **R** |
| `mapping definitions` | **WA** | **R** |
| `approval state` | **WA** | **✗** |
| `secret store` | **✗** — auch keine Werteanzeige | **R** — nur benötigte Bereitstellungen |
| `rt1 derived data` | **R** | **WA** — nur definierte Bereiche |
| `rt2 operational evidence` | **append** — nur über Evidence-Schnittstelle | **append** — nur über Evidence-Schnittstelle |
| `rt3 transient state` | **R** | **WA** — begrenzt |
| `git repository` | **D** | **✗** |
| `github remote` | **✗** | **✗** |
| `backup storage` | **✗** | **✗** |
| `network egress` | **R** — zweckgebunden | **R** — zweckgebunden |
| `model context` | **✗** ohne Datenklassen- und Transfergate | **✗** ohne Datenklassen- und Transfergate |

**Bemerkenswert:** Die Control Plane hat **kein** Leserecht auf Secret-Werte,
obwohl sie Konfiguration verwaltet. Sie sieht **Referenzen**, nie Werte
(Grundsatz S-B). Und **keine** der beiden Identitäten darf `backup storage`
beschreiben — das bleibt dem Backup Service und dem Human Maintainer
vorbehalten (KB-12).

---

## Erlaubte Aktionen

| # | Regel |
| --- | --- |
| **E-1** | Jede Aktion wird gegen **Rolle, Ressource, Aktion und Approval-Zustand** geprüft |
| **E-2** | Nur ausdrücklich zugewiesene Aktionen sind erlaubt (**deny-by-default**) |
| **E-3** | Rechte werden **je Identität** vergeben, nie je Prozess oder Container |
| **E-4** | Eine Identität darf **nur ihre eigenen** Ressourcen berühren |

## Verbotene Aktionen

| # | Verbot | Gilt für |
| --- | --- | --- |
| **V-1** | **Ausführung als root** | beide |
| **V-2** | **Direkte Proxmox-Hostausführung** | beide |
| **V-3** | **Privilegierter Container** | beide |
| **V-4** | **Host-Administrationsrechte** | beide |
| **V-5** | **Schreiben auf Canonical ohne dokumentierte Freigabe** | beide |
| **V-6** | **Automatischer Commit oder Push** | beide |
| **V-7** | **Publish ohne separate Human-Freigabe** | beide |
| **V-8** | **Approval durch den Data Worker** | Data Worker |
| **V-9** | **Direktes Beschreiben von RT-2** | beide |
| **V-10** | **Anzeige oder Protokollierung von Secret-Werten** | beide |
| **V-11** | **Beschreiben von `backup storage`** | beide |
| **V-12** | **Impersonation** — Wechsel in eine andere Identität | beide |

## Mount-Matrix

| Bereich | Control Plane | Data Worker |
| --- | --- | --- |
| `canonical sources` | **ro** | **ro** |
| `operator configuration` | **ro** | **ro** |
| `source registry` | **rw** *(mit Freigabe)* | **ro** |
| Secret-Bereitstellung | **nicht eingebunden** | **ro**, zweckgebunden |
| RT-1 | **ro** | **rw** — nur definierte Pfade |
| RT-2 | **nicht direkt eingebunden** | **nicht direkt eingebunden** |
| RT-3 | **ro** | **rw** — begrenzt |
| `backup storage` | **nicht eingebunden** | **nicht eingebunden** |
| Hostpfade außerhalb der Allowlist | **nicht eingebunden** | **nicht eingebunden** |

| # | Regel |
| --- | --- |
| **M-1** | **Keine unkontrollierten Host-Mounts** |
| **M-2** | **RT-2 wird von keiner der beiden Identitäten direkt eingebunden** — Zugriff nur über die Evidence-Schnittstelle |
| **M-3** | Ein nicht benötigter Bereich wird **nicht eingebunden**, nicht nur `ro` |
| **M-4** | **Symlink-Escapes blockieren** — Ziele außerhalb des Bereichs sind unzulässig |

**M-3 ist strenger als es aussieht:** Ein `ro`-Mount ist immer noch ein Mount.
Was nicht gebraucht wird, ist nicht sichtbar.

## Secret-Zugriff

| Identität | Zugriff |
| --- | --- |
| **Control Plane** | **keine Secret-Werte.** Sie sieht ausschließlich **Referenzen** |
| **Data Worker** | **nur die benötigte Bereitstellung**, read-only, zweckgebunden, für die notwendige Dauer |

| # | Regel |
| --- | --- |
| **SEC-1** | Bereitstellung **nie** über Umgebungsvariablen oder Kommandozeilen |
| **SEC-2** | **Keine Verzeichnisfreigabe** an nicht berechtigte Prozesse |
| **SEC-3** | Fehlende oder ungültige Referenz **blockiert** |
| **SEC-4** | Ein Resolverfehler **blockiert** — kein Fallback, kein Leerwert |

Vollständig im
[Secret Reference and Provider Contract](SECRET_REFERENCE_AND_PROVIDER_CONTRACT.md).

## Egress-Zugriff

| Identität | Egress |
| --- | --- |
| **Control Plane** | nur zweckgebunden, nur an freigegebene Ziele |
| **Data Worker** | nur zweckgebunden, nur an freigegebene Ziele |

**Die Allowlist bindet an Ziel, Provider, Zweck und Identität.** Eine für die
Control Plane freigegebene Verbindung ist für den Data Worker **nicht**
automatisch erlaubt.

Vollständig in der [Network Egress Policy](NETWORK_EGRESS_POLICY.md).

## Impersonation-Verbot

| # | Regel |
| --- | --- |
| **IMP-1** | **Keine Identität darf in die Rolle einer anderen wechseln** |
| **IMP-2** | **Kein Client darf seine Rolle selbst festlegen** |
| **IMP-3** | Die Identität wird **serverseitig** bestimmt, nie aus Clientangaben übernommen |
| **IMP-4** | **Der Actor in einem RT-2-Ereignis stammt nie aus freiem Clienttext** |
| **IMP-5** | Ein Impersonationsversuch ist ein **Vorfall**, kein Fehler — er erzeugt ein `incident`-Ereignis |

## Fehlerverhalten

| Situation | Verhalten |
| --- | --- |
| Identität nicht bestimmbar | **Verweigerung** |
| Recht nicht zugewiesen | **Verweigerung** (deny-by-default) |
| Widersprüchliche Rechte | **restriktivere Angabe gewinnt** |
| Mount fehlt | **Verweigerung**, kein Ersatzpfad |
| Secret nicht auflösbar | **Verweigerung**, kein Leerwert |
| Privileggrenze verletzt | **Start verweigern** — kein Degraded Mode |
| Evidence-Schnittstelle nicht erreichbar | **Verarbeitung anhalten** — nicht ohne Protokoll weiterlaufen |

**Die letzte Zeile ist die unbequemste.** Ein System, das ohne Protokoll
weiterläuft, erzeugt genau die Lücke, die später niemand rekonstruieren kann.

## Spätere technische Nachweise

Zu erbringen in **CBP-WP-012**. **Keiner existiert.**

| # | Nachweis | Art | Zielstufe |
| --- | --- | --- | --- |
| 1 | Effektive Identität je Prozess, keine root | NW-IMP | 2 |
| 2 | Getrennte Identitäten belegt | NW-IMP | 2 |
| 3 | Mount-Matrix je Identität belegt | NW-CFG | 2 |
| 4 | **Schreibversuch auf Canonical scheitert** | **NW-NEG** | **4** |
| 5 | **Data Worker erreicht Approval-Pfad nicht** | **NW-NEG** | **4** |
| 6 | **Control Plane erhält keinen Secret-Wert** | **NW-NEG** | **4** |
| 7 | **Impersonationsversuch scheitert und wird protokolliert** | **NW-NEG** | **4** |
| 8 | **Keine Identität beschreibt `backup storage`** | **NW-NEG** | **4** |
| 9 | Start als root wird verweigert | NW-NEG | 4 |
| 10 | Human-Abnahme des Identitätsmodells | NW-HUM | 6 |

## Offene Deploymentwerte

| Wert | Status |
| --- | --- |
| Konkrete Unix-Benutzer und Gruppen | **Deployment Required** |
| UID- und GID-Werte | **Deployment Required** |
| Container-Identitäten und Runtime | **Deployment Required** |
| Hostpfade und Volume-Namen | **Deployment Required** |
| Dateimodi | **Deployment Required** |

**Keiner dieser Werte wird hier festgelegt.**

## Status

**Es existiert keine Service-Identität.** Kein Benutzer angelegt, kein Recht
gesetzt, kein Mount konfiguriert, kein Nachweis erbracht.

**Implementierung erlaubt: nein.**
