# Technical Security Foundation Plan — Kontrollbereiche für Phase 1

| Feld | Wert |
| --- | --- |
| **Status** | **PROPOSED** — Plan, keine Implementierung |
| Stream | F3 · Backlogpunkt P3 |
| Erfasst in | CBP-WP-008 |
| Autoritätsklasse | A3 |
| Grundlage | **ADR-0004**, [PERMISSION_MODEL.md](../security/PERMISSION_MODEL.md) |
| Betrifft | **R-25**, **R-27** (beide bleiben offen) |
| Stand | 2026-07-21 |

Dieses Dokument benennt **was** technisch durchgesetzt werden muss und **in
welcher Reihenfolge**. Es wählt **keine Software**, solange mehrere Adapter
möglich bleiben, und legt **keine Ports, Benutzer-IDs oder Hostpfade**
endgültig fest.

**F3 ist der breiteste Enabler von Phase 1.** F4 und F5 hängen daran.

---

## Verbindliche Durchsetzungsreihenfolge

```text
OS-Dateirechte
  → Container- beziehungsweise Prozessidentität
    → Mount-Modi
      → API-Autorisierung
        → Netzwerkgrenzen
          → Approval-Zustände
            → Promptregeln NUR ergänzend
```

Die Reihenfolge folgt der Angreifbarkeit: was weiter oben steht, gilt auch
dann noch, wenn alles darunter versagt.

| Rang | Ebene | Gilt noch, wenn … |
| --- | --- | --- |
| **1** | OS-Dateirechte | … die Anwendung kompromittiert ist |
| **2** | Container-/Prozessidentität | … der Anwendungsprozess übernommen wurde |
| **3** | Mount-Modi | … der Prozess schreiben will |
| **4** | API-Autorisierung | … ein Client mehr verlangt als vorgesehen |
| **5** | Netzwerkgrenzen | … ein Dienst versehentlich exponiert wird |
| **6** | Approval-Zustände | … eine Aktion technisch möglich wäre |
| **7** | Promptregeln | — **nur ergänzend** |

### Promptregeln sind keine technische Kontrolle

Sie beschreiben erwünschtes Verhalten eines Systems, das sich nicht an
Beschreibungen halten muss. Eine Regel, die nur im Prompt steht, ist eine
Bitte.

**Rang 7 darf nie die einzige Ebene einer Anforderung sein.** Wo eine
Anforderung ausschließlich auf Rang 7 ruht, ist sie **nicht durchgesetzt** —
und muss so berichtet werden. Das ist Abbruchbedingung **SB-03**.

---

## Zwölf Kontrollbereiche

### KB-01 — Nicht privilegierter Betrieb

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Kein Dienst läuft als Root oder direkt auf dem Hypervisor-Host |
| **Bedrohung** | Eine kompromittierte Komponente übernimmt Host oder Nachbardienste |
| **Geplante Kontrolle** | Nicht privilegierte Ausführung; Privilegienerweiterung unterbunden; keine Hostausführung |
| **Nachweis** | Auflistung der effektiven Identität je laufendem Prozess |
| **Negativtest** | **Eskalationsversuch scheitert**; Startversuch als Root wird abgelehnt |
| **Rollen** | Retrieval Service, Indexer, Web-UI, MCP/API, Backup Service |
| **Ressourcen** | alle |
| **Risiken** | **R-26**, R-25 |
| **Voraussetzung** | Laufzeitumgebung gewählt (Profil A) |
| **Rollback** | Dienste anhalten; Rechte zurücksetzen; kein Datenbestand betroffen |

### KB-02 — Getrennte Unix-Benutzer und Service-Identitäten

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Jede Komponente hat eine **eigene**, nicht geteilte Identität |
| **Bedrohung** | Eine übernommene Komponente erbt die Rechte aller anderen |
| **Geplante Kontrolle** | Je Rolle eine eigene Dienstidentität; keine gemeinsame Sammelkennung |
| **Nachweis** | Zuordnung Identität ↔ Rolle ↔ Komponente, vollständig |
| **Negativtest** | **Indexer greift mit seiner Identität nicht auf `backup storage` oder `secret store` zu** |
| **Rollen** | alle neun Rollen der Berechtigungsmatrix |
| **Ressourcen** | alle zwölf |
| **Risiken** | R-25, R-27 |
| **Voraussetzung** | KB-01 |
| **Rollback** | Identitäten deaktivieren; Dienste anhalten |

> **Konkrete UIDs und GIDs werden hier nicht festgelegt** — das ist eine
> Deploymententscheidung.

### KB-03 — read-only und read-write Mount-Grenzen

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Kanonische Bestände werden lesend eingebunden, wo immer möglich |
| **Bedrohung** | Ein Dienst überschreibt kanonisches Wissen |
| **Geplante Kontrolle** | `ro`-Einbindung als Vorgabe; `rw` nur mit benennbarer Begründung |
| **Nachweis** | Mountliste mit Modus je Komponente |
| **Negativtest** | **Schreibversuch auf ein `ro`-Volume schlägt fehl** |
| **Rollen** | Retrieval Service, Indexer, Web-UI, Mobile Client |
| **Ressourcen** | `canonical sources`, `ingest quarantine`, `derived index` |
| **Risiken** | R-06, R-07, R-25 |
| **Voraussetzung** | KB-01, KB-02 |
| **Rollback** | Mounts entfernen; Dienste anhalten |

### KB-04 — Dateisystemrechte

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Der kanonische Bestand ist für Dienstkonten nicht schreibbar |
| **Bedrohung** | Direktzugriff unter Umgehung der Anwendung |
| **Geplante Kontrolle** | Explizite Eigentümer, Gruppen und Modi; nichts wird geerbt |
| **Nachweis** | Rechteauflistung vor und nach dem Start |
| **Negativtest** | **Schreibversuch auf kanonisch unter Dienstidentität schlägt fehl** |
| **Rollen** | Indexer, Retrieval Service, Web-UI, Claude Agent |
| **Ressourcen** | `canonical sources`, `project decisions`, `handoffs` |
| **Risiken** | R-06, R-25 |
| **Voraussetzung** | KB-01, KB-02 |
| **Rollback** | Rechte auf den dokumentierten Ausgangszustand zurücksetzen |

**KB-04 ist die unterste tragende Ebene.** Versagt sie, sind KB-05 bis KB-07
wirkungslos.

### KB-05 — API-Autorisierung

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Jeder Endpunkt prüft **serverseitig** Rolle und Aktionsklasse |
| **Bedrohung** | Ein Client verlangt mehr, als seine Rolle erlaubt |
| **Geplante Kontrolle** | Default deny; Prüfung gegen die Matrix 9 Rollen × 12 Ressourcen |
| **Nachweis** | Prüfprotokoll je Rolle × Endpunkt |
| **Negativtest** | **Unbekannte Rolle erhält nichts** — nicht das Minimum; verbotene Zelle wird abgelehnt |
| **Rollen** | alle neun |
| **Ressourcen** | alle zwölf |
| **Risiken** | **R-25**, R-05 |
| **Voraussetzung** | KB-01 bis KB-04; erste API existiert |
| **Rollback** | Endpunkt deaktivieren — **nicht** Prüfung abschalten |

> **Framework und Tokenformat bleiben offen** (OD-20).

### KB-06 — Approval-Zustände

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Schreibende und veröffentlichende Wirkung erst nach dokumentierter Freigabe |
| **Bedrohung** | Unbeabsichtigte oder automatische Änderungen |
| **Geplante Kontrolle** | Maschinell geführter Freigabezustand; `draft` erzeugt nie Wirkung |
| **Nachweis** | Zustandsverlauf je Aktion |
| **Negativtest** | **Aktion ohne Freigabe bleibt wirkungslos**; der Versuch ist im Audit sichtbar |
| **Rollen** | Claude Agent, Web-UI, Mobile Client, Reviewer |
| **Ressourcen** | `canonical sources`, `project decisions`, `workspaces`, `git repository` |
| **Risiken** | R-12, R-25 |
| **Voraussetzung** | KB-05 |
| **Rollback** | Freigabezustände zurücksetzen; offene Anträge verwerfen |

### KB-07 — Git- und GitHub-Rechte

| Feld | Inhalt |
| --- | --- |
| **Ziel** | **Kein pauschaler Schreibzugriff** für den Implementation Agent |
| **Bedrohung** | Unkontrollierter Push; Änderung an Remote, Branches oder Releases |
| **Geplante Kontrolle** | Claude `forbidden` auf `github remote`, nur `draft` auf `git repository`; Push- und Release-Autorität ausschließlich beim Human Maintainer |
| **Nachweis** | Rechteauflistung der verwendeten Zugänge; kein Schreibtoken im Agentenkontext |
| **Negativtest** | **Pushversuch aus der Agentenidentität scheitert** |
| **Rollen** | Claude Agent, Human Maintainer, Reviewer |
| **Ressourcen** | `git repository`, `github remote` |
| **Risiken** | **R-27**, R-01 |
| **Voraussetzung** | KB-02 |
| **Rollback** | Zugang entziehen; Token widerrufen |

### KB-08 — Secret-Store-Grenze

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Secrets nie in Repository, Mapping, Index, Context Pack oder Modellkontext (**D-006**) |
| **Bedrohung** | Ein Secret gelangt in die Git-Historie und ist praktisch nicht entfernbar |
| **Geplante Kontrolle** | Konfiguration enthält ausschließlich **Verweise**; Zugriff auf den Store nur für ausdrücklich berechtigte Identitäten |
| **Nachweis** | Suche über Repository, Index und Context Packs **ohne Fund** |
| **Negativtest** | **Zugriffsversuch aus Claude-, Web-UI- und Indexer-Identität scheitert**; synthetisches Muster wird erkannt |
| **Rollen** | Human Maintainer (WA), Backup Service (R), alle übrigen **verboten** |
| **Ressourcen** | `secret store` |
| **Risiken** | **R-01**, R-02 |
| **Voraussetzung** | KB-01, KB-02, KB-04 |
| **Rollback** | Zugriff sperren; bei Fund [SECRET_INCIDENT_RESPONSE](../security/SECRET_INCIDENT_RESPONSE.md) — **Rotation vor History Cleanup** |

**KB-08 muss vor jedem Ingest stehen.** Ein Secret im Index ist nicht durch
spätere Kontrollen zu entfernen, nur durch Rotation und Rebuild.

> **Secret-Store-Technologie bleibt offen.**

### KB-09 — Audit-Logging

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Jede schreibende Aktion **und jeder abgelehnte Versuch** ist nachvollziehbar |
| **Bedrohung** | Ein Vorfall bleibt unentdeckt oder wird nachträglich verwischt |
| **Geplante Kontrolle** | Append-only für protokollierende Komponenten; kein Löschrecht auf eigene Einträge |
| **Nachweis** | Abgelehnter Zugriff erscheint im Protokoll |
| **Negativtest** | **Komponente kann den eigenen Eintrag nicht entfernen oder ändern** |
| **Rollen** | Indexer und Retrieval Service (append), Human Maintainer (R) |
| **Ressourcen** | `audit logs` |
| **Risiken** | R-25, R-16 |
| **Voraussetzung** | KB-02, KB-04 |
| **Rollback** | Protokollierung **nicht** abschalten; bei Fehlern Dienst anhalten |

> Auditdaten liegen in der Runtime Data Area, sind aber **nicht
> reproduzierbar**. Ihr Sicherungsbedarf ist gesondert zu klären.

### KB-10 — Netzwerk-Egress

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Ausgehender Verkehr ist **allowlist-basiert**; keine öffentliche Erreichbarkeit |
| **Bedrohung** | Datenabfluss an ein nicht vorgesehenes Ziel; Zugriff von außen |
| **Geplante Kontrolle** | Zugriff nur über privates Netz oder VPN (**D-023**); Egress-Allowlist statt Blocklist |
| **Nachweis** | Portauflistung von außen; wirksame Allowlist |
| **Negativtest** | **Verbindung zu einem nicht gelisteten Ziel scheitert**; Zugriff ohne VPN scheitert |
| **Rollen** | Retrieval Service, Web-UI, MCP/API, Mobile Client |
| **Ressourcen** | `context packs`, `derived index` |
| **Risiken** | R-05, R-02 |
| **Voraussetzung** | KB-01, KB-02 |
| **Rollback** | Egress vollständig sperren — der sichere Zustand ist **kein** Netz |

> **VPN-Technologie, Ports und Adressbereiche bleiben offen** (Deployment
> Required).

### KB-11 — `excluded-from-ai`-Ausgabesperre

| Feld | Inhalt |
| --- | --- |
| **Ziel** | So klassifizierte Inhalte erreichen **keinen** Modellkontext |
| **Bedrohung** | Leakage über Retrieval, Context Pack, Sammelanfrage oder Web-UI |
| **Geplante Kontrolle** | Sperre auf **mehreren** Ebenen: Dateirechte, Mount, Indexausschluss, API-Filter, Ausgabefilter — **nicht nur** im Retrieval |
| **Nachweis** | Negativtest mit **synthetischen** Daten (**D-021**), Zielwert **null Leaks** |
| **Negativtest** | Inhalt erscheint **weder** in Suchergebnis **noch** in Context Pack **noch** in einer Antwort; besonders über **weit gefasste Sammelanfragen** |
| **Rollen** | Retrieval Service, Indexer, Web-UI, Mobile Client, MCP/API |
| **Ressourcen** | `canonical sources`, `derived index`, `context packs` |
| **Risiken** | **R-31**, **R-30**, R-02, R-05 |
| **Voraussetzung** | KB-04, KB-05, KB-10; Fixtures aus Dataset 2.0.0 |
| **Rollback** | Retrieval-Pfad anhalten; betroffene Context Packs verwerfen |

**Dies ist der Nachweis, der R-31 schließt — kein anderer.** Er ist zugleich
die technische Durchsetzung, deren Fehlen **R-30** beschreibt.

### KB-12 — Backup-Storage-Isolation

| Feld | Inhalt |
| --- | --- |
| **Ziel** | Backup Storage ist für Web-UI, Suche und Claude **nicht beschreibbar** |
| **Bedrohung** | Eine kompromittierte Komponente überschreibt die Sicherung |
| **Geplante Kontrolle** | Schreibrecht ausschließlich für Backup Service und Human Maintainer |
| **Nachweis** | Rechteauflistung; **ein tatsächlich durchgeführter Restore** |
| **Negativtest** | **Schreibversuch aus Claude-, Web-UI-, Retrieval- und Indexer-Identität scheitert** |
| **Rollen** | Backup Service (WA), Human Maintainer (WA), alle übrigen **verboten** |
| **Ressourcen** | `backup storage` |
| **Risiken** | **R-20**, R-07 |
| **Voraussetzung** | KB-02, KB-04 |
| **Rollback** | Schreibrechte entziehen; Sicherung auf getrenntes Ziel |

**Wer die Sicherung überschreiben kann, hat keine Sicherung.** Eine ungetestete
Sicherung zählt nicht.

---

## Zuordnung Bereiche × Durchsetzungsebenen

| Bereich | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| KB-01 | | ● | | | | | |
| KB-02 | | ● | | | | | |
| KB-03 | | | ● | | | | |
| KB-04 | ● | | | | | | |
| KB-05 | | | | ● | | | |
| KB-06 | | | | | | ● | |
| KB-07 | | ● | | ● | | ● | ○ |
| KB-08 | ● | ● | | | | | ○ |
| KB-09 | ● | | | ● | | ● | |
| KB-10 | | | | | ● | | |
| KB-11 | ● | | ● | ● | ● | | ○ |
| KB-12 | ● | | | ● | | | |

● tragende Ebene · ○ ergänzend

**Kein Bereich ruht allein auf Rang 7.** Das ist die Prüfregel dieser Tabelle
und der Auslöser für SB-03.

## Umsetzungsreihenfolge

| Schritt | Bereiche | Begründung |
| --- | --- | --- |
| 1 | KB-01, KB-02, KB-04 | Fundament; alles Weitere setzt darauf auf |
| 2 | KB-03, KB-08 | Mount-Grenzen und Secret-Grenze **vor jedem Ingest** |
| 3 | KB-07, KB-10 | Git-Rechte und Netzgrenzen vor der ersten erreichbaren Komponente |
| 4 | KB-05, KB-06, KB-09 | mit der ersten API |
| 5 | KB-11 | mit dem ersten Retrieval-Pfad |
| 6 | KB-12 | mit dem ersten produktiven Bestand |

## Was dieser Plan nicht festlegt

| Gegenstand | Status |
| --- | --- |
| Container-Runtime, Basisimages | offen — mehrere Adapter möglich |
| Konkrete UIDs, GIDs, Dateimodi | offen — Deployment |
| Hostpfade, Volume-Namen | offen — OD-05, OD-26 |
| Ports und Adressbereiche | offen — Deployment |
| VPN-Technologie | offen — Deployment Required |
| Secret-Store-Technologie | offen — nicht registriert |
| Allowlist ausgehender Ziele | offen — OD-20 |
| API-Framework, Tokenformat | offen — OD-20 |
| Scanner und Suchdienst | offen — OD-25 |

## Status der Risiken

**R-25 und R-27 bleiben `offen`.** Dieses Dokument beschreibt Kontrollen, die
**nicht existieren**. Ein Plan ist keine Durchsetzung — genau das ist der
Inhalt beider Risiken. Sie schließen erst durch bestandene Negativtests.

**Implementierung erlaubt: nein.**
