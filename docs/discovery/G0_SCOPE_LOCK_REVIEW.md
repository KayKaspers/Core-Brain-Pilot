# G0 Scope-Lock Review — Entscheidungsunterlage

| Feld | Wert |
| --- | --- |
| **Status** | **READY FOR HUMAN DECISION** |
| **Gate-Status** | **NOT PASSED** |
| Gate | G0 – Discovery and Scope Lock |
| Erfasst in | CBP-WP-006 |
| Autoritätsklasse | A3 |
| Adressat | **Human Maintainer** |
| Stand | 2026-07-21 |

Diese Unterlage fasst zusammen, worüber entschieden wird. Sie entscheidet
nichts.

---

## 1. Gegenstand des Scope Locks

G0 sperrt den **allgemeinen Produkt- und Architektur-Scope** von Core Brain
Pilot: was das System ist, welche Quellen es aufnimmt, welche Regeln für
Autorität, Datenschutz und Berechtigungen gelten, wie es betrieben und
gemessen wird.

**G0 sperrt nicht** die Details einer konkreten Installation. Diese liegen im
[Deployment Readiness Check](../operations/DEPLOYMENT_READINESS_CHECK.md).

| Kennzahl | Wert |
| --- | --- |
| Kriterien gesamt | 47 |
| **Core Required — G0-relevant** | **25**, alle `accepted` |
| Deployment Required — DRC | 16, alle `not-evaluated` |
| Conditional — nur bei aktivierter Funktion | 6, keine aktiv |

## 2. Bestätigte Projektdefinition

Ein **serverzentriertes und portables KI-Wissens- und Arbeitssystem**, das
Implementation Agents die kleinste ausreichende Menge relevanter, aktueller,
autoritativer und datenschutzrechtlich erlaubter Informationen bereitstellt.

**Anlass:** zu hoher Token- und Kontextverbrauch. Das System soll Limits nicht
umgehen, sondern Kontext effizienter nutzen.

**Leitprinzip:** Proxmox ist die erste Referenzplattform, nicht die
Produktgrenze. Der Wissensbestand bleibt portabel, der Index reproduzierbar,
Claude liest nur das Nötige, und der Mensch entscheidet, was gilt.

## 3. Pilotumfang

| Dimension | Festlegung | Beleg |
| --- | --- | --- |
| Betriebsprofil | Proxmox-VM mit dedizierter Linux-VM | D-015, ADR-0002 |
| Anwendungslaufzeit | Docker Compose bevorzugt **innerhalb** der VM | D-016 |
| Nutzung | Einzelperson, 1 Nutzer; Multi-User kein Pflichtumfang | D-018 |
| Quellen | Markdown, Git-Repositories, Chat-Handoffs, Obsidian-Vault als Markdown | HDI A3, PS-01…PS-04 |
| Datenklassen | `public`, `internal` | HDI A4 |
| Zugriff | privates VPN oder privates Netz, keine öffentliche Freigabe | D-023 |
| Im Pilot | Web-UI (erst nach funktionierendem Retrieval), mobile Nutzung | D-024 |

## 4. Nicht-Ziele

25 gesperrte Gegenstände in
[DO_NOT_START.md](../product/DO_NOT_START.md), davon 11 ausdrücklich auf A-8
gemappt: kein Kubernetes · kein Multi-Tenant-SaaS · keine öffentliche
Cloudinstanz · keine Proxmox-API-Integration · kein vollständiger Wiki-Ingest ·
kein Knowledge Graph im Pilot · keine automatische Konfliktentscheidung · keine
automatischen Commits und Pushes · keine breite Connector-Integration · keine
produktive Obsidian-Synchronisation ohne Test · kein öffentliches Branding.

**Vertagt:** native Obsidian-Nutzung, Wiki-Pilot, externe Connectoren (D-025).

## 5. Quellenvertrag

[PILOT_SOURCE_CONTRACT.md](../sources/PILOT_SOURCE_CONTRACT.md) — sieben
logische Source Slots:

| Slot | Status | Mapping nötig |
| --- | --- | --- |
| PS-01 Core Project Control | `active` | nein |
| PS-02 Operator Markdown Knowledge Root | `active` | **ja** |
| PS-03 Selected Git Repositories | `active` | **ja** |
| PS-04 Approved Chat Handoffs | `active` | ja |
| PS-05 Synthetic Benchmark Fixtures | `test-only` | nein |
| PS-06 PDF and Office Documents | `deferred` | — |
| PS-07 External Connectors | `deferred` | — |

**Kern der Entscheidung:** Der allgemeine Kern enthält **keinen privaten
Wissensbestand**. Quellen werden über logische Slots definiert und erst im
Deployment Mapping konkret zugeordnet (ADR-0006, `proposed`).

## 6. Autoritätsmodell

A0 bis A6; **A6 überschreibt A0–A5 niemals automatisch**. Konflikte werden
gemeldet, nicht entschieden. Ein Source Slot verleiht keine Autorität
(Slot-Regel 8); A0 muss auf eine konkrete menschliche Entscheidung
zurückführbar sein (Regel 9).

## 7. Datenschutzmodell

Fünf Datenklassen mit Flussmatrix. **Standardwert: Übertragung an externe KI
wird verweigert, bis eine Datenklasse sie erlaubt.** `secret` und
`excluded-from-ai` erreichen nie ein externes Modell; `excluded-from-ai`
erzwingt `ai_transfer: forbidden`. Fail-closed bei unbekannter Klasse.

Secret-Schadensverfahren: 14 Schritte, **Rotation vor History Cleanup**.

## 8. Berechtigungsmodell

[PERMISSION_MODEL.md](../security/PERMISSION_MODEL.md) — 9 Rollen × 12
Ressourcen, fünf Aktionsklassen, fünf technische Durchsetzungsebenen, Default
deny. Claude: `forbidden` auf `github remote`, `backup storage` und
`secret store`; nur `draft` auf kanonische Quellen. Nur **ein** autorisierter
Schreibpfad verändert Kanonisches (ADR-0004).

## 9. Deploymentprofile

Fünf Profile A–E, alle mit identischem Kern (ADR-0001). Referenz ist Profil A;
Profil B ist der laufende Nachweis der Neutralität. Keine
Proxmox-API-Abhängigkeit, kein Root, kein Betrieb auf dem Host.

## 10. Context Budgets

B0 Micro · B1 Lean · B2 Standard · B3 Extended · B4 Exceptional. Quellenregel:
Normalfall 1, erweitert höchstens 3, darüber begründete Eskalation. **Nicht zu
verwechseln mit den NDF Prompt Modes** (D-009).

**Die Token-Richtwerte sind ungemessene Setzungen** — OD-02b bleibt offen.

## 11. Benchmarkdesign

Dataset **2.0.0**: 24 synthetische Quellen, A0 bis A6, 5 Konfliktpaare, 4
Datenschutzfixtures, 36 Fragen in 6 Kategorien (24 Development / 12 Holdout),
9 kritische Fehler, V0/V1/V2 provider-neutral.

> **Entworfen, nicht ausgeführt.** Kein Lauf, keine Messung, kein Index, keine
> Suchsoftware.

---

## 12. Verbleibende technische Risiken

| Risiko | Gegenstand | Warum es zählt |
| --- | --- | --- |
| **R-25** | Berechtigungen nicht technisch durchgesetzt | Ein Modell auf Papier ist keine Zugriffskontrolle |
| **R-27** | Repository- und GitHub-Zugriffe nicht durchgesetzt | Dasselbe, mit unmittelbarer Wirkung auf fremde Repositories |
| **R-31** | `excluded-from-ai` ungeprüft | Die Sperrwirkung ist behauptet, nicht nachgewiesen |
| **R-32** | Keine Quarantäne für Nicht-Markdown | PS-06 und PS-07 bleiben deshalb `deferred` |
| **R-21** | Benchmark nicht ausgeführt | Keine Qualitätsaussage möglich |
| **R-20** | Restore nie geprobt | Eine ungeprüfte Sicherung ist keine Sicherung |
| **R-01** | Secret-Erkennung fehlt | Verfahren definiert, Erkennung nicht |

**Alle sieben bleiben offen.** Keines blockiert G0 — alle blockieren die
Umsetzung.

## 13. Verbleibende Deploymententscheidungen

16 Deployment-Required-Kriterien im DRC, Status **NOT EVALUATED**: Plattform­
version, CPU, RAM, Speicher, Storage-Technologie, VPN-Technologie, ausgehende
Verbindungen, Geräte, Backupziel und -frequenz, externe Kopie, RPO, RTO,
Restore-Test, Secret-Verwaltung, Betriebsverantwortung.

**Fail-closed:** Fehlt eine Angabe, wird nicht installiert.

## 14. Conditional-Themen

Sechs bedingte Kriterien, **keines aktiviert**: Offlineanforderungen (A-6),
native Obsidian-Nutzung (A-7, vertagt), DNS (C-3), Reverse Proxy (C-4),
personenbezogene Daten (D-6, `not-applicable`), `confidential`-Daten (D-7,
`not-applicable`).

Wird eine dieser Funktionen später aktiviert, **lebt das zugehörige Kriterium
auf** und ist zu beantworten.

## 15. DRC-Status

**NOT EVALUATED.** 18 Prüfpunkte, 0 auf `ready`. Je Deploymentprofil separat
auszuführen (ADR-0005). Nicht Gegenstand dieser Entscheidung.

## 16. Bedingungen für Phase 1

Phase 1 (Proxmox-Referenzumgebung) setzt voraus:

1. **G0 ausdrücklich freigegeben** — diese Entscheidung
2. **DRC für Profil A durchgeführt** und auf `ready`
3. Deployment Mappings für PS-02, PS-03 und PS-04 festgelegt (OD-05, OD-06)
4. Backup **eingerichtet und getestet** vor produktivem Betrieb (Standardwert 10)
5. Berechtigungen technisch umgesetzt, nicht nur dokumentiert

## 17. Was G0 nicht abdeckt

> Damit die Entscheidung nicht mehr trägt, als sie soll:

| Nicht abgedeckt | Zuständig |
| --- | --- |
| Funktionsfähigkeit irgendeiner Komponente | Phase 1 ff. |
| Technische Durchsetzung der Berechtigungen | Phase 1 ff., R-25/R-27 |
| Nachweis der `excluded-from-ai`-Sperrwirkung | Benchmarklauf, R-31 |
| Retrieval-Qualität | Benchmarklauf, R-21 |
| Wiederherstellbarkeit | Restore-Test, R-20 |
| Konkrete Infrastruktur | DRC |
| Konkreter produktiver Quellenbestand | OD-05, OD-06 |
| Repository-Layout | OD-26 |
| Repository-Sichtbarkeit | OD-11 |
| Lizenzwahl | OD-23 |
| Annahme von ADR-0006 | eigener Beschluss |

**G0 sperrt den Scope. Es bestätigt keine Reife.**

---

## 18. Entscheidungsoptionen

| Option | Bedeutung | Folge |
| --- | --- | --- |
| **APPROVE G0** | Scope Lock erteilt, ohne Auflagen | CBP-WP-007 zeichnet die Entscheidung auf; Phase-1-Backlog entsteht |
| **APPROVE G0 WITH NOTES** | Scope Lock erteilt, mit festgehaltenen Auflagen | wie oben, Auflagen werden Bestandteil des Phase-1-Backlogs |
| **REWORK** | Unterlage unvollständig oder fehlerhaft | benannte Kriterien zurück auf `answered` oder `open` |
| **SPLIT** | Teil des Scopes freigeben, Rest vertagen | Kriterien getrennt führen; G0 bleibt teilweise offen |
| **STOP** | Projekt anhalten | keine weitere Arbeit bis zu einem neuen Beschluss |

## 19. Empfehlung des Implementation Agent

**Empfehlung: APPROVE G0 WITH NOTES.**

Dies ist eine **Empfehlung, keine Freigabe.** Der Implementation Agent hat
keine Gate-Autorität.

**Begründung:** Alle 25 Core-Kriterien sind nachweisbasiert belegt. Jede
`accepted`-Markierung verweist auf ein konkretes Dokument, 18 davon auf eine
ausdrückliche A0-Entscheidung. Die Unterlage ist entscheidungsreif.

**Warum „with notes" und nicht schlicht „approve":** Sechzehn der 25 Kriterien
beschreiben Kontrollen, die **nicht existieren**. Das ist für einen Scope Lock
korrekt — G0 sperrt den Scope, nicht die Implementierung — aber es sollte in
der Entscheidung sichtbar werden. Ich schlage drei Auflagen vor:

1. **Vor produktivem Ingest:** technische Durchsetzung der Berechtigungen
   (R-25, R-27) und Nachweis der `excluded-from-ai`-Sperrwirkung (R-31).
2. **Vor dem Retrieval-Pilot:** ein vollständiger V0/V1-Benchmarklauf; erst
   danach sind die Pilotziele belastbar und OD-02b entscheidbar.
3. **Vor produktivem Betrieb:** geprüfter Restore (R-20) und ein DRC auf
   `ready` für Profil A.

**Drei Punkte, die ich ausdrücklich nicht als erledigt darstelle:**

- **D-1 `accepted` bedeutet nicht, dass eine Quelle angebunden ist.** Es
  bedeutet, dass der zulässige Quellenraum definiert und begrenzt ist. OD-05
  und OD-06 bleiben offen.
- **ADR-0006 ist `proposed`**, nicht `accepted`. Die darin vorgeschlagene
  Trennung von Kern und privatem Bestand braucht einen eigenen Beschluss.
- **Der Benchmark ist entworfen, nicht gemessen.** Sechs `accepted`-Marken im
  G-Block bedeuten einen prüfbaren Plan.

---

# BEGIN G0 HUMAN DECISION

Decision:
<vom Human Maintainer auszufüllen>

Notes:
<optional>

Authority:
A0

# END G0 HUMAN DECISION

---

> **Dieser Block ist bewusst leer.** Der Implementation Agent darf ihn nicht
> ausfüllen. Bis er ausgefüllt ist, gilt: **G0 NOT PASSED**.
>
> Die Aufzeichnung der Entscheidung erfolgt im vorgeschlagenen Work Package
> CBP-WP-007 — nach und nicht vor dem Beschluss.
