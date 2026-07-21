# Security Foundation Readiness Gate

| Feld | Wert |
| --- | --- |
| **Status** | **NOT EVALUATED** |
| Art | Prüfmodell, **kein NDF-Gate** |
| Grundlage | **ADR-0009** (A1), [Specification](../security/TECHNICAL_SECURITY_FOUNDATION_SPECIFICATION.md), [Acceptance Matrix](../security/SECURITY_CONTROL_ACCEPTANCE_MATRIX.md) |
| Erfasst in | CBP-WP-011 |
| Autoritätsklasse | A3 |
| Gate-Punkte | **24** |
| Stand | 2026-07-21 |

> **Dieses Gate wurde nicht ausgeführt.** Es existiert keine Foundation
> Runtime, keine Kontrolle und kein Prüfergebnis. `NOT EVALUATED` ist der
> korrekte Ausgangszustand — kein offener Punkt.

---

## Zweck

Das Gate beantwortet eine Frage:

> Ist die technische Sicherheitsgrundlage **nachweislich** wirksam — nicht
> beschrieben, sondern geprüft?

Es steht **vor** dem produktiven Betrieb und **vor** dem Mapping Activation
Gate. Ohne bestandene Sicherheitsgrundlage ist ein Mapping nicht aktivierbar:
Acht der zwanzig Punkte jenes Gates verlangen Nachweisstufe 4, die ohne KB-01
bis KB-04 nicht erreichbar ist.

## Abgrenzung

| Gate | Gegenstand | Status |
| --- | --- | --- |
| **G0** | Produkt- und Architektur-Scope | PASSED WITH NOTES |
| **DRC** | Installationsreife eines Deployments | `NOT EVALUATED` |
| **Mapping Activation Gate** | Wirksamwerden **eines Mappings** | `NOT EVALUATED` |
| **dieses Gate** | Wirksamkeit der **Sicherheitsgrundlage** | **`NOT EVALUATED`** |

**Die vier Gates bleiben getrennt.** Keines ersetzt ein anderes.

## Ergebniswerte

| Wert | Bedeutung | Wer stellt fest |
| --- | --- | --- |
| **`NOT EVALUATED`** | Nicht geprüft — **Ausgangszustand** | — |
| **`BLOCKED`** | Mindestens ein Punkt verletzt oder ungeprüft | Prüfung oder Mensch |
| **`READY FOR HUMAN SECURITY DECISION`** | Alle 24 Punkte erfüllt, Entscheidung steht aus | Prüfung |
| **`ACCEPTED BY HUMAN MAINTAINER`** | Sicherheitsgrundlage angenommen | **ausschließlich der Human Maintainer** |
| **`REVOKED`** | Annahme zurückgenommen | Human Maintainer oder Vorfall |

| # | Regel |
| --- | --- |
| **E1** | **Nur der Human Maintainer darf `ACCEPTED BY HUMAN MAINTAINER` feststellen** |
| **E2** | `READY FOR HUMAN SECURITY DECISION` ist **keine Annahme** |
| **E3** | Ein einziger nicht erfüllter Punkt ergibt **`BLOCKED`** |
| **E4** | Ein **nicht geprüfter** Punkt zählt wie ein verletzter (fail-closed) |
| **E5** | `REVOKED` erzwingt Anhalten des Betriebs |
| **E6** | Eine Warnung hebt **nie** ein `BLOCKED` auf |
| **E7** | Eine sicherheitsrelevante Änderung setzt das Gate auf **`NOT EVALUATED`** zurück |

---

## Die 24 Gate-Punkte

| # | Punkt | Nachweis | KB | Stufe |
| --- | --- | --- | --- | --- |
| **1** | **Nicht privilegierte Identität definiert** | Identitätsauflistung, keine root | KB-01 | 2 |
| **2** | **Service-Identity-Trennung definiert** | Control Plane und Data Worker getrennt belegt | KB-02 | 2 |
| **3** | **OS-Rechte umgesetzt** | Rechteauflistung, keine world-writable | KB-04 | 2 |
| **4** | **Mount-Matrix umgesetzt** | Mountliste mit Modus je Identität | KB-03 | 2 |
| **5** | **Canonical read-only nachgewiesen** | **NT-04 bestanden** | KB-03, KB-04 | **4** |
| **6** | **Runtime-Schreibgrenzen nachgewiesen** | RT-1 beschreibbar, RT-2 nur über Writer, RT-3 begrenzt | KB-03 | **4** |
| **7** | **API-Authentisierung umgesetzt** | Identitätsprüfung je Endpunkt | KB-05 | 2 |
| **8** | **API-Autorisierung negativ getestet** | **NT-06, NT-07 bestanden** | KB-05 | **4** |
| **9** | **Approval-Bypass negativ getestet** | **NT-08 bestanden** | KB-06 | **4** |
| **10** | **Git-/GitHub-Rechte minimal** | **NT-09 bestanden**, kein breites Token | KB-07 | **4** |
| **11** | **Secret Resolver umgesetzt** | Resolver mit Versions- und Providerprüfung | KB-08 | 2 |
| **12** | **Secret-Werte nicht in Logs** | **NT-10, NT-11, NT-28 bestanden** | KB-08, KB-09 | **4** |
| **13** | **Secret-Rotation getestet** | Rotation ohne Referenzänderung; Widerruf blockiert | KB-08 | 3 |
| **14** | **Egress deny-by-default umgesetzt** | Wirksame Allowlist, vierfach gebunden | KB-10 | 2 |
| **15** | **Redirect-Bypass negativ getestet** | **NT-15, NT-23 bestanden** | KB-10 | **4** |
| **16** | **`excluded-from-ai` negativ getestet** | **NT-16, NT-17 bestanden — null Leaks** | KB-11 | **4** |
| **17** | **RT-2-Integritätsschutz umgesetzt** | Verkettung wirksam, **NT-19, NT-20 bestanden** | KB-09 | **4** |
| **18** | **RT-2-Backup nachgewiesen** | Sicherung erfolgt, Ziel nicht überschreibbar | KB-12 | 3 |
| **19** | **Restore nachgewiesen** | **Durchgeführter Restore mit Integritätsprüfung** | KB-12 | **5** |
| **20** | **Sichere Abschaltung nachgewiesen** | Dienst hält an statt zu degradieren | alle | 3 |
| **21** | **Rollback definiert** | Je Kontrolle ein Weg zurück, erprobt | alle | 3 |
| **22** | **DRC-Werte vollständig** | Alle Deployment-Required-Werte erhoben | — | 2 |
| **23** | **Mapping Activation Gate weiterhin getrennt** | Keine Vermischung der beiden Gates | — | 1 |
| **24** | **Human-Abnahme** | Ausdrückliche Entscheidung des Human Maintainers | — | **6** |

### Verteilung der Nachweisstufen

**Jeder Gate-Punkt trägt genau eine primäre Mindeststufe.** Die Zahlen sind aus
der Gate-Tabelle oben zeilenweise ausgezählt.

| Nachweisstufe | Gate-IDs | Anzahl |
| --- | --- | ---: |
| **1** `dokumentiert` | 23 | 1 |
| **2** `implementiert` | 1, 2, 3, 4, 7, 11, 14, 22 | 8 |
| **3** `lokal getestet` | 13, 18, 20, 21 | 4 |
| **4** `negativ getestet` | 5, 6, 8, 9, 10, 12, 15, 16, 17 | **9** |
| **5** `wiederhergestellt` | 19 | 1 |
| **6** `angenommen` | 24 | 1 |
| **Summe** | | **24** |

**Konsistenzprüfung:** Summe der Stufenanzahlen = **24** · eindeutige Gate-IDs
= **24** · dokumentierte Gesamtzahl = **24**. Keine doppelte ID, keine fehlende
ID, keine ID mit zwei Stufen.

**Neun Punkte verlangen Stufe 4, einer Stufe 5.** Das ist der Grund, warum
dieses Gate ohne CBP-WP-012 nicht durchlaufbar ist.

> **Korrektur im Nova-REWORK-Lauf (2026-07-21):** Die Anzahlspalte führte für
> Stufe 4 zuvor **10** bei neun aufgezählten IDs; die Summe ergab damit 25
> statt 24. Die **ID-Liste war korrekt**, nur die Zahl nicht.

### Warum Punkt 23 im Gate steht

Punkt 23 prüft nicht die Runtime, sondern die **Governance**: Dass jemand
versucht sein könnte, das Mapping Activation Gate mit diesem hier zu
verrechnen, ist absehbar — beide betreffen dieselbe Runtime. **Sie bleiben
getrennt**, weil sie verschiedene Fragen beantworten: *Ist die Grundlage
sicher?* gegen *Darf diese eine Quelle wirksam werden?*

---

## Fail-closed-Verhalten

| Situation | Ergebnis |
| --- | --- |
| Ein Punkt verletzt | **`BLOCKED`** |
| Ein Punkt **nicht geprüft** | **`BLOCKED`** — nicht `READY` |
| Widersprüchliche Nachweise | **`BLOCKED`**, restriktivere Angabe gewinnt |
| Nachweis veraltet | **`NOT EVALUATED`**, Gate neu durchlaufen |
| Secret gefunden | **`BLOCKED`** plus Incident-Verfahren, SB-S05 |
| Kontrolle ruht allein auf Promptregeln | **`BLOCKED`**, SB-S15 |
| Unbekannter Zustand | **`BLOCKED`** |

**Der Normalzustand ist Verweigerung.** Es gibt keinen Weg durch Zeitablauf,
Wiederholung oder Quittierung.

## Rücknahme

| Auslöser | Wirkung |
| --- | --- |
| Human Maintainer widerruft | `REVOKED`, Betrieb anhalten |
| Sicherheitsrelevante Änderung | `NOT EVALUATED` (E7) |
| Stop-Bedingung eingetreten | `BLOCKED`, Verarbeitung anhalten |
| Nachweis nicht mehr gültig | `NOT EVALUATED` |

## Abhängigkeiten

| Voraussetzung | Aus | Grund |
| --- | --- | --- |
| KB-01 bis KB-04 umgesetzt | **CBP-WP-012** | Punkte 1–6 |
| KB-05, KB-06 umgesetzt | CBP-WP-012 | Punkte 7–9 |
| KB-08 umgesetzt | CBP-WP-012 | Punkte 11–13 |
| KB-09 umgesetzt | CBP-WP-012 | Punkte 17, 18 |
| KB-10, KB-11 umgesetzt | CBP-WP-012 | Punkte 14–16 |
| KB-12 umgesetzt | CBP-WP-012 | Punkte 18, 19 |
| Deployment-Werte erhoben | **DRC** | Punkt 22 |
| **OD-05, OD-06** | Human Maintainer | mittelbar — ohne Quellen kein Betrieb |

**CBP-WP-012 ist nicht autorisiert.** Dieses Gate ist deshalb heute nicht
durchlaufbar — nicht, weil es zu streng wäre, sondern weil die Voraussetzungen
nicht existieren.

## Status

**NOT EVALUATED.**

**Kein Punkt wurde geprüft, keiner erfüllt.** Es existiert keine Foundation
Runtime, keine Service-Identität, kein Secret Resolver, keine Egress-Regel,
kein RT-2-Speicher und kein Backup.

**Dieses Work Package hat das Gate nicht ausgeführt.** Eine Feststellung von
`ACCEPTED BY HUMAN MAINTAINER` ist ausschließlich dem Human Maintainer
vorbehalten.

**Implementierung erlaubt: nein.**
