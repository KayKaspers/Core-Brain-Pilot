# Network Egress Policy

| Feld | Wert |
| --- | --- |
| **Status** | **ACCEPTED FOR IMPLEMENTATION PLANNING** |
| **Nicht** | IMPLEMENTED · DEPLOYED · TESTED |
| Grundlage | **ADR-0009** (A1), **D-036** (A0), D-023, DATA_CLASSIFICATION |
| Erfasst in | CBP-WP-011 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

> **Dieses Dokument enthält keine produktiven Hosts, Ports, IP-Bereiche oder
> Provider.** Es wurde keine Netzwerkregel verändert.

---

## Grundsatz — deny-by-default

**D-036:** Der Default für Netzwerk-Egress ist **deny**.

| # | Regel |
| --- | --- |
| **EG-1** | **Default ist deny** |
| **EG-2** | **Jede Erlaubnis ist explizit** |
| **EG-3** | **Unbekannte Ziele sind blockiert** |
| **EG-4** | **Redirect auf ein nicht erlaubtes Ziel ist blockiert** |
| **EG-5** | **DNS-Auflösung hebt die Zielbindung nicht auf** |
| **EG-6** | **Private Netzwerkzugehörigkeit ist keine automatische Erlaubnis** |
| **EG-7** | **Lokale Suche muss ohne externen Egress möglich sein** |
| **EG-8** | Externe AI-Übertragung benötigt **zusätzlich** kompatible Datenklasse und `ai_transfer_policy` |
| **EG-9** | **`excluded-from-ai` bleibt unabhängig vom Ziel blockiert** |

> **Grundsatz S-C: Eine Netzwerkerlaubnis ist keine Datenfreigabe.**
> Erreichbarkeit und Übertragbarkeit sind **getrennte Prüfungen**.

**Warum deny-by-default und nicht Blocklisting:** Eine Blockliste ist per
Konstruktion unvollständig. Jedes neue Ziel wäre erlaubt, bis jemand es
bemerkt — und Datenabfluss bemerkt man selten rechtzeitig.

---

## Zielklassen

| Klasse | Beispiele | Default |
| --- | --- | --- |
| **Lokal** | Prozesse innerhalb derselben VM, Loopback | **erlaubt** für definierte Dienstpaare |
| **Privat** | Ziele im privaten Netz oder VPN (D-023) | **deny** — Zugehörigkeit genügt nicht (EG-6) |
| **Extern** | Alles jenseits von TB-G, insbesondere Modellgrenzen | **deny** |

**Lokal ≠ frei:** Auch lokale Verbindungen folgen der Identitäts- und
Zweckbindung. Ein lokal erreichbarer Dienst ist nicht automatisch ein
autorisierter Dienst (DD-6).

## Bindung jeder Erlaubnis

Eine Egress-Erlaubnis ist **immer vierfach gebunden**:

| Bindung | Bedeutung |
| --- | --- |
| **Ziel** | Konkretes, benanntes Ziel — keine Wildcards, keine Domänenbäume |
| **Provider** | Registrierter Anbietertyp |
| **Zweck** | Wofür — Retrieval, Modellanfrage, Aktualisierung |
| **Service-Identität** | Control Plane **oder** Data Worker, nie beide implizit |

**Eine für die Control Plane freigegebene Verbindung ist für den Data Worker
nicht automatisch erlaubt.**

## Die fünf Gates vor einer externen Übertragung

Alle fünf müssen erfüllt sein. **Ein einziges nicht erfülltes Gate blockiert.**

| # | Gate | Prüft |
| --- | --- | --- |
| **G-1** | **Zielgate** | Ist das Ziel freigegeben — für diese Identität, diesen Provider, diesen Zweck? |
| **G-2** | **Datenklassengate** | Erlaubt die Datenklasse eine externe Übertragung? |
| **G-3** | **AI-Transfer-Gate** | Ist `ai_transfer_policy` kompatibel? |
| **G-4** | **Approval-Gate** | Ist der Mapping- und Freigabezustand `approved` und `enabled`? |
| **G-5** | **Zweckgate** | Entspricht die Übertragung dem freigegebenen Zweck? |

### Datenklassengate im Einzelnen

| Datenklasse | Externe Übertragung |
| --- | --- |
| `public` | zulässig, wenn G-1, G-4, G-5 erfüllt |
| `internal` | nur bei `ai_transfer_policy: allowed` oder `restricted` mit dokumentierter Einschränkung |
| `confidential` | **nicht im Pilot** (D-020) |
| **`excluded-from-ai`** | **niemals** — unabhängig von jeder Netzfreigabe (EG-9) |
| `unknown` | **niemals** — fail-closed wie `excluded-from-ai` |
| `secret` | **existiert nicht** in einem Mapping |

**Die letzten drei Zeilen sind der Kern.** Sie machen G-2 und G-3 unabhängig
von G-1: Selbst ein vollständig freigegebenes Ziel nimmt gesperrten Inhalt
nicht entgegen.

## DNS- und Redirect-Verhalten

| Situation | Verhalten |
| --- | --- |
| DNS löst auf ein nicht erlaubtes Ziel auf | **blockiert** — die Bindung gilt dem Ziel, nicht dem Namen (EG-5) |
| Ziel antwortet mit Redirect auf ein erlaubtes Ziel | zulässig, **erneute Prüfung aller fünf Gates** |
| Ziel antwortet mit Redirect auf ein **nicht** erlaubtes Ziel | **blockiert** (EG-4) |
| DNS nicht auflösbar | **blockiert** — kein Fallback |
| Ziel wechselt die Adresse | **erneute Prüfung**, keine Übernahme |

**Ein Redirect ist eine neue Verbindung, keine Fortsetzung.** Wer das anders
behandelt, hat eine Allowlist, die sich vom Ziel selbst erweitern lässt.

## Timeout- und Fehlerverhalten

| Situation | Verhalten |
| --- | --- |
| Zeitüberlauf | **Abbruch**, kein Wiederholungslauf ohne erneute Gate-Prüfung |
| Verbindungsfehler | **Abbruch**, Ereignis `egress-decision` mit Ergebnis |
| Gate nicht prüfbar | **blockiert** (DD-4 — fehlende Evidenz blockiert) |
| Allowlist nicht lesbar | **blockiert** — kein Betrieb ohne Regelwerk |
| Teilübertragung abgebrochen | als **erfolgt** behandeln — was raus ist, ist raus |

**Die letzte Zeile ist unbequem und richtig.** Eine abgebrochene Übertragung
ist keine nicht stattgefundene Übertragung.

## Auditpflicht

**Jede Egress-Entscheidung erzeugt ein `egress-decision`-Ereignis in RT-2** —
erlaubte **und** blockierte.

| Feld im Ereignis | Enthalten |
| --- | --- |
| Service-Identität | ja |
| Zielkennung | ja — **als Kennung, nicht als vollständige Adresse mit Parametern** |
| Zweck | ja |
| Ergebnis | `allowed` oder `blocked` |
| Grund bei Blockade | Gate-ID (G-1 bis G-5) |
| Datenklasse | ja |
| **Übertragener Inhalt** | **nein** |
| **Secret-Werte** | **nein** |

## Widerruf

| Auslöser | Wirkung |
| --- | --- |
| Human Maintainer widerruft eine Erlaubnis | sofort wirksam, laufende Verbindungen werden beendet |
| Mapping wird `revoked` | zugehöriger Egress blockiert |
| Datenklasse verschärft | betroffene Übertragungen blockiert |
| Vorfall nach SB-S07 oder SB-S08 | **Egress vollständig sperren** |

## Offline-Modus

| # | Regel |
| --- | --- |
| **OFF-1** | **Lokale Suche und lokales Retrieval funktionieren ohne externen Netzwerkzugriff** |
| **OFF-2** | Der Ausfall externer Ziele **degradiert** das System, er legt es nicht lahm |
| **OFF-3** | Ein fehlender Egress ist **kein Fehlerzustand**, sondern der Normalfall |
| **OFF-4** | **Der sichere Zustand ist kein Netz** |

**OFF-1 ist eine Architekturanforderung, keine Betriebsoption.** Ein System,
das für die lokale Suche das Internet braucht, hat die Trennung zwischen
lokalem Index und externer Sprachverarbeitung nicht umgesetzt.

## Tests

**Sieben Negativtests und ein Positivtest.** Kanonische Zuordnung in der
[Acceptance Matrix](SECURITY_CONTROL_ACCEPTANCE_MATRIX.md).

### Negativtests

| # | Test | Erwartung | Regel |
| --- | --- | --- | --- |
| **NT-14** | Egress zu einem nicht erlaubten Ziel | **blockiert** | EG-3 |
| **NT-15** | Redirect auf ein nicht erlaubtes Ziel | **blockiert** | EG-4 |
| **NT-16** | Externe Übertragung von `excluded-from-ai` | **blockiert** | EG-9, G-2 |
| **NT-26** | Erlaubnis der Control Plane vom Data Worker genutzt | **blockiert** | Identitätsbindung |
| **NT-27** | `data_class: unknown` bei externer Übertragung | **blockiert** | G-2 |
| **NT-32** | DNS löst auf ein nicht erlaubtes Ziel auf | **blockiert** | EG-5 |
| **NT-33** | Ziel im privaten Netz ohne Freigabe | **blockiert** | EG-6 |

### Positivtest

| # | Test | Erwartung | Regel |
| --- | --- | --- | --- |
| **PT-01** | Lokale Suche bei vollständig gesperrtem Egress | **funktioniert** | OFF-1 |

**PT-01 ist ein Positivtest, kein Negativtest.** Er prüft, dass die Sperre das
System nicht funktionsunfähig macht — die zulässige Funktion bei erfüllten
Voraussetzungen. Er wird **nicht** zur Negativtestzahl gerechnet.

> **Korrektur im Nova-REWORK-Lauf (2026-07-21):** Dieser Abschnitt trug zuvor
> die Überschrift „Negativtests" und enthielt acht Einträge, von denen einer
> ein Positivtest war — mit einer **NT-ID**. Zusätzlich waren **NT-23 und
> NT-24 doppelt vergeben**: In der Acceptance Matrix bezeichnen sie
> RT-1- und RT-3-Tests des Bereichs KB-03. Die beiden hiesigen Egress-Tests
> haben deshalb die neuen, eindeutigen IDs **NT-32** und **NT-33** erhalten.

## Offene Deploymentwerte

| Wert | Status |
| --- | --- |
| Konkrete Egress-Ziele | **Deployment Required** |
| Ports und IP-Bereiche | **Deployment Required** |
| Registrierte Provider | CBP-WP-012 |
| VPN-Technologie | **Deployment Required** |
| Firewall- oder Proxy-Mechanismus | **Deployment Required** |
| Timeoutwerte | **Deployment Required** |

**Keiner dieser Werte wird hier festgelegt. Keine Netzwerkregel wurde
verändert, kein Port geöffnet.**

## Status

**Es existiert keine Egress-Allowlist, keine Durchsetzung und kein Test.**

**R-05 und R-02 bleiben offen.**

**Implementierung erlaubt: nein.**
