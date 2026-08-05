# KB-04 Profile-A Integration Plan

**Architektur-, Ausführungs- und Freigabeplan der Teilphase B2D**

> **Ein Plan ist keine Ausführung.**
>
> Dieses Dokument beschreibt, **was** eine spätere reale Integration verlangen
> würde und **welche Freigaben** ihr vorausgehen müssen. Es führt nichts aus,
> stellt nichts bereit, misst nichts und belegt nichts.

---

## 1 — Dokumentstatus

| Feld | Wert |
| --- | --- |
| Work Package | **CBP-WP-022** — KB-04 Enforcement Stage 1 |
| Teilphase | **B2D-P** — Profile-A Integration Plan and Execution Authorization Gates |
| Status | **plan-only** |
| Reale Infrastruktur | **nicht autorisiert** |
| Ausführung | **nicht autorisiert** |
| Gate | **nicht autorisiert** — weder Eingabe noch Auswertung |
| OD-37-Schließung | **nicht autorisiert** |
| B2B-Apply | **nicht autorisiert** |
| Operative Sicherheitswirkung | **keine** |
| Vorgängerlauf | **B2D.0** — read-only Boundary- und Readiness-Audit, `PASS WITH NOTES` |

**Was dieses Dokument ist:** ein Architektur- und Ausführungsplan sowie eine
Sicherheits- und Freigabespezifikation.

**Was dieses Dokument nicht ist:** kein ausführbares Runbook · kein
Deploymentartefakt · kein Evidenzartefakt · keine Konfiguration · kein Harness
· keine technische Implementierung.

**KB-04 bleibt `DOCUMENTED ONLY`.** Beide Runtime-Gates bleiben
`NOT EVALUATED`. **NT-04 und NT-05 sind nicht ausgeführt.** **SB-S04 ist nicht
wirksam.** **OD-37 bleibt offen.** **RT-2 ist nicht implementiert.**

---

## 2 — Authority und Quellen

Die Autoritätsreihenfolge dieses Plans ist verbindlich und wird **nicht**
umgekehrt:

1. **Contract** — `docs/security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md`
2. **Angenommene Decisions** — D-060, D-061, D-062
3. **Angenommene ADRs** — ADR-0013, ADR-0014
4. **Implementierungsstand** — Enforcement-Paket, Gate- und Evidenzcode
5. **Tests und Fixtures** — die Traceability- und Vorbereitungsdateien
6. **Statusspiegel** — zuletzt und ausschließlich als Spiegel

> **Ein Statusspiegel steht niemals über einer normativen Quelle.** Wo ein
> Spiegel von Contract, Decision oder ADR abweicht, gilt die normative Quelle,
> und die Abweichung ist zu melden.

### Normative Stellen

| Quelle | Beitrag zu diesem Plan |
| --- | --- |
| **Contract §2** | Scope: Profil **A**, Plattform **Linux/POSIX**, Authority **Host-Dateisystem**, Runtimeanteil **read-only** |
| **Contract §3** | Non-Goals: **keine** reale Testausführung, **keine** realen UID-/GID-Werte, **keine** realen Benutzer- oder Gruppennamen, **keine** realen Hostpfade, **keine** RT-2-Implementierung |
| **Contract §7.1** | vier getrennte Prüfdimensionen **D-I** bis **D-IV**; **MT-9** bis **MT-14** — eine nicht prüfbare Dimension gilt als **nicht erfüllt** |
| **Contract §8** | Identitätsbindungsvertrag: elf Felder, `value_origin` ausschließlich `operator-workspace`, **keine sicheren Defaults**, **keine Fallback-Identität** |
| **Contract §9** | Initialisierungsvertrag: **nachweislich neue, leere** Zielstruktur; sechs gleichzeitige Voraussetzungen; Transaktionsgrenze; **keine Rollback-Zusage** |
| **Contract §12** | Migration und Reparatur: **ausführender Reparaturmodus gesperrt**, RT-2-Grenze |
| **Contract §16** | NT-04 und NT-05 wörtlich, einschließlich der Aussagegrenzen |
| **Contract §17** | SB-S04, OD-37 und die Gatepunkte; **keine Auswertung** |
| **Contract §18** | **die einzige normative B2D-Scopedefinition** sowie der gesperrte Scope |
| **Contract §19** | Aussagegrenzen: *„Ein implementierungsfähiger Vertrag ist keine Implementierung, und eine geplante Prüfung ist kein Nachweis."* |
| **ADR-0014** (A1) | Host-authoritative Enforcement; drei Schichten mit disjunkten Befugnissen; Durchsetzung **außerhalb der Runtime, außerhalb des Repositorys**; kategorisches Mutationsverbot für lang laufende Komponenten |
| **ADR-0013** (A1) | Evidence-Schema 3.0; Security-Control-Form ist **negative-evidence-only** und erfüllt **niemals** ein Gatekriterium |
| **D-060** (A0) | Annahme des Contracts |
| **D-061** (A0) | B2C-Lesart; **Teil O**: eine KB-04-Security-Control-Form- oder Gate-Evidence-Integration verlangt eine **eigenständige A0-Entscheidung** |
| **D-062** (A0) | kanonischer Abdeckungssplit **37 / 2 / 6**; **Teil J**: eine §10.3-Umsetzung verlangt eigene Scopefreigabe sowie erneute ADR- und Decision-Prüfung |

**Ergebnis des Quellenabgleichs: keine Konflikte.** Eine **Sequenzbedingung**
ist zu beachten — Contract §18 führt „Gate-Evidenz" im B2D-Scope, D-061 Teil O
bindet ihre Integration an eine eigene A0-Entscheidung.

---

## 3 — Verbindlicher B2D-Zweck

Contract §18 definiert B2D als **Profile-A Deployment Integration** mit genau
fünf Gegenständen:

| Gegenstand | Einordnung |
| --- | --- |
| **lokale Identitätsbindung** | Bestandteil |
| **reale Profil-A-Instanz** | Voraussetzung |
| **reale Nachweise** | Bestandteil und Ergebnis |
| **OD-37** | **nur Vorbereitung** — die Schließung ist nicht Ergebnis von B2D |
| **Gate-Evidenz** | **nur Vorbereitung und Optionsbildung** — Integration verlangt eigene A0-Entscheidung |

### Ausdrücklich außerhalb von B2D

**Gatefreigabe** · **Control-Uplift** · **SB-S04-Aktivierung** ·
**OD-37-Schließung** · **RT-2** · **produktive Reparatur** · **Migration
bestehender Daten** · **KB-04 Stage 2** · **Contract-§10.3-Implementierung**.

Der gesperrte Scope stammt wörtlich aus Contract §18: *„produktive Reparatur ·
Migration bestehender Daten · RT-2 · reale Gatefreigabe · Control-Uplift ·
Stage 2."*

### Rollentrennung

B2D ist **keine** Planungsphase im Kern, **keine** Implementierungsphase für
Enforcement-Produktionscode, **keine** Gate-Evaluationsphase und **keine**
Control-Uplift-Phase. B2D ist eine **reale Ausführungs- und
Nachweisphase innerhalb einer Deployment-Integration**.

**Nicht vermischbar:** reale Ausführung und Gateauswertung · Evidenzerzeugung
und Gate-Eingabe · Setup-Mutation und Runtime-Validierung · Planung und
Ausführung.

---

## 4 — B2D-Phasenmodell

| Phase | Zweck | Reale Infrastruktur | Repositoryänderung | Status |
| --- | --- | :---: | --- | --- |
| **B2D-P** | Planung und Freigabegates — dieses Dokument | **nein** | ein Plandokument, neun Statusspiegel | **dieser Stand, plan-only** |
| **B2D-H** | optionaler operator-geführter Harness | nein | offen, Verortung ungeklärt | **nicht autorisiert** |
| **B2D-E** | reale Ausführung in isolierter Referenzumgebung | **ja** | **keine** — nur lokale Ergebnisartefakte | **nicht autorisiert** |
| **B2D-V** | read-only Verifikation und Anonymisierung | nein | Statusspiegel, ggf. anonymisierte Zusammenfassung | **nicht autorisiert** |
| **B2D-G** | Gate- und OD-37-Reconciliation | nein | Gate-, Decision- und Registerdateien | **nicht autorisiert** |

### Verbindliche Sequenzregeln

| # | Regel |
| --- | --- |
| **S-1** | **B2D-P muss committed und durch Nova geprüft sein**, bevor eine weitere Phase überhaupt erwogen wird. |
| **S-2** | **B2D-E und B2D-G dürfen niemals im selben Lauf stattfinden.** Andernfalls würde eine Ausführung unmittelbar zur Freigabe. |
| **S-3** | **B2D-E löst keinen automatischen Übergang** zu B2D-V oder B2D-G aus. Jeder Übergang ist ein eigener, gesondert freigegebener Lauf. |
| **S-4** | Jede Phase nach B2D-P verlangt eine **eigene Freigabe**; eine Freigabe für B2D-P ist **keine** Freigabe für die Folgephasen. |
| **S-5** | **B2D-E erzeugt keine Repositorydateiänderung.** Ergebnisse entstehen ausschließlich lokal und unversioniert. |

---

## 5 — B2B-Apply-Unabhängigkeit

**B2D hängt nicht von einer Repository-Apply-Funktion ab.**

ADR-0014 trennt drei Schichten mit disjunkten Befugnissen und verortet die
**Durchsetzung** ausdrücklich **außerhalb der Runtime und außerhalb des
Repositorys**. Der **Setup-Akteur** ist dort als **hostseitig und
operatorgeführt** beschrieben; er darf Rollen an Identitäten binden sowie
Besitz und Rechte **initial herstellen**, und er darf **niemals als
Dauerprozess laufen**.

| Feststellung | Begründung |
| --- | --- |
| Der Setup-Akteur ist **hostseitig und operatorgeführt** | ADR-0014, Authority-Modell |
| Er liegt **außerhalb von Runtime und Repository** | ADR-0014, Schichtentabelle |
| Die Runtime bleibt **strikt read-only** | ADR-0014, kategorische Regel — Architekturaussage, keine Konfigurationsoption |
| Es existiert **keine Repository-Funktion `apply_plan`** | Contract §9.3: *„Keine Funktion wird implementiert."* |
| **Keine Umgehung durch einen versteckten Repo-Helper** | ein mutierender Helfer im Repository wäre dieselbe Grenzverletzung, unabhängig von seiner Benennung oder Ablage |
| **B2B-Apply bleibt unabhängig nicht autorisiert** | die dortige Frage — ob ein *Repository-Werkzeug* mutieren darf — stellt sich für B2D nicht |

**Konsequenz:** Die für B2D nötige Mutation liegt vollständig auf der
Deployment-Seite der von ADR-0014 gezogenen Grenze. Sie ist damit
**architektonisch verortet**, aber **operativ nicht freigegeben**.

---

## 6 — Profile-A-Referenzumgebung

Alle Angaben sind **abstrakt**. Es wird kein realer Wert festgelegt.

| Merkmal | Festlegung |
| --- | --- |
| Plattform | **Linux/POSIX** — normativ aus Contract §2 |
| Instanzart | **dedizierte, nicht produktive Referenzinstanz** in Gestalt einer virtuellen Maschine |
| Zielstruktur | **nachweislich neu und leer** nach Contract §9.1 |
| Produktive Daten | **ausgeschlossen** |
| Wiederverwendete Produktionsinstanz | **ausgeschlossen** |
| Reale Hostwerte | **niemals** im Repository |
| UID- und GID-Werte | **niemals** fest eingebettet |
| Benutzer- und Gruppennamen | **niemals** im Repository |
| Pfadklassen | **PC-01** bis **PC-11** nach Contract §4 |
| Rechteprofile | **PP-1**, **PP-2**, **PP-3a**, **PP-3b**, **PP-4** nach Contract §6 |
| Prüfdimensionen | **D-I** Host-Quellobjekt · **D-II** Mountvertrag · **D-III** Runtime-sichtbares Objekt · **D-IV** Runtimeidentität |
| Objektarten | Verzeichnis und reguläre Datei zulässig; Device, FIFO und Socket **unzulässig** (LP-6) |
| Root-Boundary | feste Bereichsgrenze je Pfadklasse; normalisierte Auflösung statt Zeichenkettenvergleich (LP-1, LP-2) |
| Link-Regeln | bereichsverlassende Symlinks **unzulässig**; interne Symlinks werden **abgelehnt, nicht aufgelöst**; Hardlinks in geschützten Bereichen **unzulässig** (LP-3 bis LP-5) |
| TOCTOU | **nicht gelöst** — LP-9 hält ausdrücklich fest, dass ein Prüfergebnis nicht über einen Schreibvorgang hinaus gilt |

### Container als Variante

**Ein Container wird ausdrücklich nicht als gleichwertiger Ersatz der
VM-Referenzvariante festgelegt.** Eine spätere Containeroption benötigte eine
**eigene Eignungs- und Autorisierungsprüfung**, weil die getrennte
Feststellbarkeit der vier Dimensionen — insbesondere **D-I gegenüber D-III** —
davon abhängt, welche Sicht auf Host und Einbindung überhaupt zur Verfügung
steht. Contract §7.1 hält diesen Punkt ausdrücklich als **offenen Punkt der
realen Deployment-Evidenz** fest.

**Für B2D-P wird ausschließlich die VM-Referenzvariante geplant.**

---

## 7 — Wiederherstellungsanforderung

Contract §9.3 hält fest: *„Es wird keine Rollback-Zusage gegeben. Ein
Rücksetzungsmechanismus existiert nicht."*

Deshalb legt **Nova** für jede spätere B2D-E-Ausführung zusätzlich fest:

| # | Anforderung |
| --- | --- |
| **R-1** | Ein **Snapshot oder gleichwertiger Wiederherstellungspunkt** existiert **vor** dem Lauf. |
| **R-2** | Die **Zielinstanz ist dokumentiert** und eindeutig bezeichnet. |
| **R-3** | Ein **dokumentierter Wiederherstellungstest** oder ein nachweislich verfügbarer Wiederherstellungsweg liegt vor. |
| **R-4** | **Kein Lauf ohne bestätigten Recovery-Punkt.** |

**Einordnung, verbindlich:**

- Dies ist eine **Ausführungsvoraussetzung von Nova**.
- Es ist **keine** bestehende Rollbackzusage des Contracts — der Contract gibt
  ausdrücklich keine.
- **In B2D-P wird kein Snapshot erzeugt** und keine Instanz berührt.

---

## 8 — Privilegien- und Identitätsgrenze

| Feststellung | Inhalt |
| --- | --- |
| Setup-Fähigkeiten | Das Setzen von Besitz und Gruppe **kann** privilegierte Fähigkeiten erfordern. Diese liegen **ausschließlich** beim hostseitigen, operatorgeführten Setup-Akteur. |
| Runtime | **Keine Runtime erhält Setup-Rechte** — weder beim Start noch im Betrieb noch zur Fehlerbehebung. |
| Neue Identitäten | Es wird **nicht behauptet**, dass zwingend neue Benutzer oder Gruppen angelegt werden müssen. |
| Vorhandene Identitäten | Bereits vorhandene, hinreichend isolierte Identitäten **könnten** verwendet werden. |
| Auswahl | Die konkrete Auswahl bleibt **lokal und in B2D-P unentschieden**. |
| Konkrete Werte | UID-, GID- und Namenswerte bleiben **außerhalb des Repositorys**. |
| Defaults | **Keine sicheren Defaults für lokale Identitäten** — Contract §8. |
| Fallback | **Keine automatische Fallback-Identität** — Contract §8. |
| Unvollständige Bindung | **fail-closed**; eine Bindung ist erst gültig, wenn sie **positiv** validiert wurde. |

Die Trennung zweier logischer Rollen — eine Control-Plane-Rolle und eine
Data-Worker-Rolle — bleibt Zweck der Bindung; eine Identitätskollision ist
nach Contract §8 **fail-closed**, weil die Trennung selbst der Schutzzweck ist.

---

## 9 — Lokaler Operator-Workspace

**Reale Identitätswerte gehören ausschließlich in den lokalen
Operator-Workspace.** Sie erscheinen **nicht** in versionierten Dateien,
**nicht** in Berichten, **nicht** in Commits und **nicht** in
Public-Neutrality-Artefakten.

### Speicheroptionen — bewertet, nicht ausgewählt

| Option | Bewertung |
| --- | --- |
| unversionierte lokale Datei | zulässig; entspricht der bereits dokumentierten Operator-Workspace-Praxis |
| Umgebungsvariablen | zulässig; flüchtig, hinterlässt kein Artefakt |
| Human-Maintainer-Eingabe | zulässig; nicht reproduzierbar |
| externes Deploymentprofil | zulässig; liegt außerhalb des Repositorys |
| temporäres lokales Artefakt | zulässig **nur lokal**, mit Löschpflicht |

**Verbindlich für B2D-P:**

- **B2D-P wählt keine neue Configsemantik.**
- **B2D-P erweitert keine öffentlichen Configschlüssel.**
- **B2D-P erzeugt kein Binding-Schema.**

Entstünde später ein **versioniertes** Bindungsschema, wäre das eine Frage der
öffentlichen Konfigurationssemantik mit eigenem Entscheidungsbedarf.

---

## 10 — Preconditions für B2D-E

Die folgende Checkliste ist **vollständig zu erfüllen**. Fehlt ein einziger
Punkt, **darf B2D-E nicht beginnen**.

| # | Voraussetzung | Nachweisform |
| ---: | --- | --- |
| 1 | **B2D-P ist committed und durch Nova geprüft** | Commit und Prüfvermerk |
| 2 | **Eigene A0-Ausführungsfreigabe** liegt vor | Human-Maintainer-Beschluss |
| 3 | **Genaue Ziel-Referenzinstanz bestätigt** | Operatorbestätigung |
| 4 | **Nicht produktiver Status bestätigt** | Operatorbestätigung |
| 5 | **Neue und leere Zielstruktur bestätigt** | Preflight nach Contract §9.1 |
| 6 | **Snapshot oder Recovery-Punkt bestätigt** | Operatorbestätigung |
| 7 | **Lokale Identitäten vollständig gebunden** | alle Pflichtfelder nach Contract §8, `validated` |
| 8 | **Mountplan lokal geprüft** | Abgleich gegen die Mounterwartung je Pfadklasse |
| 9 | **Keine realen Werte im Repository** | Neutralitätsprüfung |
| 10 | **Abbruch- und Cleanupplan bestätigt** | siehe Kapitel 13 und 19 |
| 11 | **Evidence-Form noch nicht mit einem Gate gekoppelt** | Kapitel 14 und 15 |
| 12 | **B2D-G ist nicht gleichzeitig autorisiert** | Sequenzregel S-2 |
| 13 | **Human Maintainer bestätigt den Startzeitpunkt** | ausdrückliche Freigabe |

> **Ohne vollständige Checkliste darf B2D-E nicht beginnen.**

---

## 11 — Die sechs B2D-real-only-Fälle

Alle Angaben sind abstrakt und **nicht ausführbar**. **Gatewirkung: keine** —
für jeden der sechs Fälle.

### KB04-T-N07 — Retrieval kann Canonical schreiben

**Contractquelle** §15, §16 (NT-04) · **Ziel** der Schreibversuch scheitert ·
**Umgebung** reale Referenzinstanz, Nachweisstufe 4 · **Identität** die
lesende Retrieval-Rolle ohne Canonical-Schreibrecht · **Pfadklasse** PC-01 ·
**Rechteprofil** PP-3a · **Dimensionen** vom Contract nicht ausdrücklich
festgelegt · **Beobachtete Aktion** ein Schreibvorgang gegen den
Canonical-Bereich · **Erwartetes Ergebnis** Ablehnung **auf
Betriebssystemebene**, nicht erst in der Anwendung · **Zulässige Aussage**
dieser eine Schreibversuch wurde real abgewiesen · **Verbotene Aussage** dass
KB-03 vollständig ist, dass andere Bereiche geschützt sind, dass ein Gate
erfüllt ist, dass eine Control hochgestuft werden darf · **Abbruchbedingung**
gelingt der Schreibvorgang, ist SB-S04 unmittelbar berührt — sofortiger
Abbruch · **Cleanup** im Normalfall keiner; gelingt der Vorgang wider
Erwarten, ist das der Störfall · **Evidenzherkunft** lokal, real beobachtet.

### KB04-T-N08 — Ingest schreibt Canonical unkontrolliert

Wie N07, jedoch mit der **schreibenden Ingest-Rolle** als Akteur.
**Zwei getrennte reale Fälle sind erforderlich**, weil der Contract in der
Akteursmatrix unterschiedliche Rollenzeilen führt und §15 zwei eigenständige
Kennungen definiert. **Ein einziger Schreibversuch belegt nicht beide.**
Aussagegrenzen, Abbruchbedingung und Cleanup entsprechen N07.

### KB04-T-N14 — Symlink-Escape

**Contractquelle** §15, §16 (NT-05) · **Ziel** die Auflösung wird verweigert ·
**Umgebung** isolierte, neue und leere Struktur · **Pfadklasse** PC-02 ·
**Rechteprofil** PP-1 · **Beobachtete Aktion** ein Verweis innerhalb des
geschützten Bereichs zeigt nach außen und wird angesprochen · **Erwartetes
Ergebnis** die Auflösung wird **verweigert, nicht gefolgt** · **Zulässige
Aussage** dieser eine Escape-Versuch wurde real blockiert · **Verbotene
Aussage** dass Hardlinks abgedeckt sind, dass TOCTOU gelöst ist, dass ein Gate
erfüllt ist · **Abbruchbedingung** wird die Auflösung gefolgt, ist die
Bereichsgrenze verletzt — sofortiger Abbruch · **Cleanup** **verpflichtend** —
das angelegte Verweisobjekt ist zu entfernen · **Evidenzherkunft** lokal, real
beobachtet.

### KB04-T-N31 — Runtime kann das Artefakt verändern

**Contractquelle** §15, §10.6 Prüfung 6 · **Ziel** die Runtime besitzt **keine
Schreibfähigkeit** · **Pfadklasse** PC-07 · **Rechteprofil** PP-3b ·
**Dimension** **D-III** · **Beobachtete Aktion** Feststellung der
Schreibfähigkeit auf das Konfigurationsartefakt · **Erwartetes Ergebnis** die
Abwesenheit der Schreibfähigkeit ist **negativ zu belegen** · **Verbotene
Aussage** dass der Bundlemodus allein den Hostzustand belegt · **Cleanup**
keiner · **Evidenzherkunft** lokal, real beobachtet.

### KB04-T-N33 — Bundlemodus weicht vom sichtbaren Zustand ab

**Contractquelle** §15, §10.6 Prüfung 12, **MT-9** · **Ziel** zugesagter
Bundlemodus und tatsächlich sichtbarer Zustand stimmen überein ·
**Pfadklasse** PC-07 · **Rechteprofil** PP-3b · **Dimensionen** **D-II gegen
D-III** · **Beobachtete Aktion** Abgleich beider Werte · **Erwartetes
Ergebnis** Übereinstimmung; der Bundlewert wird nach MT-9 **nicht automatisch
akzeptiert** · **Verbotene Aussage** dass der Bundlemodus allein den sichtbaren
Zustand belegt · **Cleanup** keiner · **Evidenzherkunft** lokal, real
beobachtet.

### KB04-T-P12 / D-I — reales Host-Quellobjekt

**Contractquelle** §15, §10.6 Prüfung 8 · **Ziel** der Host-Quellzustand des
PP-3b-Artefakts ist separat geprüft · **Pfadklasse** PC-07 · **Rechteprofil**
PP-3b · **Dimension** **D-I** · **Beobachtete Aktion** Erhebung von Besitz,
Gruppe, Modus, Objektart und Linkstatus auf dem Host · **Erwartetes Ergebnis**
positiver Nachweis; **solange D-I nicht positiv validiert werden kann, ist er
offen auszuweisen und darf nicht als erfüllt dargestellt werden** ·
**Verbotene Aussage** dass KB04-T-P12 bestanden ist, dass D-III den Zustand von
D-I belegt (MT-10) · **Cleanup** keiner · **Evidenzherkunft** lokal, real
beobachtet.

> Die synthetischen Vorprüfungen aus der bestehenden Testbasis decken D-II,
> D-III und D-IV **modellhaft** ab. Sie sind **kein** vollständiger Nachweis
> und geben P12 **nicht** als bestanden aus.

---

## 12 — NT-04-Plan

| Punkt | Festlegung |
| --- | --- |
| Fälle | **zwei getrennte** — **N07** (Retrieval) und **N08** (Ingest) |
| Umgebung | reale Profil-A-Referenzinstanz, Nachweisstufe **4** |
| Pfadklasse | **PC-01** |
| Rechteprofil | **PP-3a** |
| Identitäten | **unterschiedliche gebundene Rollen** je Fall |
| Erwartung | Scheitern **auf Betriebssystemebene** |
| Ersatz | **keine Applikationssimulation** — ein anwendungsseitiges Scheitern erfüllt die Bedingung **nicht** |
| Abbruch | bei unerwartet **erfolgreichem** Schreibvorgang **sofortiger Abbruch**; SB-S04 ist berührt |
| Gate- und Controlaussage | **keine** |
| Ausführung in B2D-P | **kein tatsächlicher Schreibversuch** |

**ReasonCodes**, soweit der Contract sie eindeutig trägt:
`KB04-MODE-MISMATCH` und `KB04-MOUNT-MODE-MISMATCH`.

**Aussagegrenze wörtlich aus Contract §16:** ein bestandener Test belegt
**nicht**, dass KB-03 vollständig ist, dass andere Bereiche geschützt sind,
dass ein Gate erfüllt ist oder dass eine Control hochgestuft werden darf.

---

## 13 — NT-05-Plan

| Punkt | Festlegung |
| --- | --- |
| Fall | **N14** |
| Umgebung | **isolierte, neue und leere** Struktur nach Contract §9.1 |
| Pfadklasse | **PC-02** |
| Rechteprofil | **PP-1** |
| Gegenstand | ein Verweis innerhalb des geschützten Bereichs zeigt nach außen |
| Erwartung | die Auflösung wird **verweigert, nicht gefolgt** |
| Cleanup | **verpflichtender Ausführungsschritt** — das angelegte Verweisobjekt ist zu entfernen |
| Nicht abgedeckt | **Hardlinks** und **TOCTOU** — Contract §16 sagt dies ausdrücklich |
| Gate- und Controlaussage | **keine** |
| Ausführung in B2D-P | **kein tatsächlicher Verweis wird angelegt** |

**ReasonCode**, soweit der Contract ihn eindeutig trägt:
`KB04-LINK-SYMLINK-ESCAPE`.

Anders als bei NT-04 entsteht hier **bewusst ein Artefakt**. Der Cleanup ist
deshalb Teil der Ausführungsdefinition, nicht ein nachgelagerter Wunsch.

---

## 14 — Evidence-Optionen

**Keine Option wird ausgewählt. Kein Producer wird definiert. Keine
Gate-Eingabe wird definiert.**

| Evidenzart | Zweck | lokal-only | versionierbar | reale Werte möglich | Anonymisierung nötig | negative-evidence-only | gate-relevant | neue A0 nötig | ADR-Neubewertung nötig | Status |
| --- | --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | --- |
| **Rohbeobachtung** | unveränderte Erhebung des Ist-Zustands | **ja** | nein | **ja** | — | nein | nein | nein | nein | `LOCAL_ONLY` |
| **Normalisierte Beobachtung** | Abbildung auf abstrakte Referenzen | nein | **ja** | nein | **ja** | nein | nein | nein | nein | `OPTION_ONLY` |
| **Lokales Testprotokoll** | Ablauf und Ergebnis eines Laufs | **ja** | nein | **ja** | — | nein | nein | nein | nein | `LOCAL_ONLY` |
| **Operatorbestätigung** | menschlicher Nachweis auf Stufe 4 | **ja** | nein | **ja** | **ja** | nein | nein | nein | nein | `LOCAL_ONLY` |
| **Anonymisierte Zusammenfassung** | veröffentlichbarer Ergebnisspiegel | nein | **ja** | nein | **ja** | nein | nein | nein | nein | `OPTION_ONLY` |
| **Security-Control-Form** | maschinenlesbarer Controlnachweis | nein | **ja** | nein | **ja** | **ja** | **ja** | **ja** | **ja** | `SEPARATE_DECISION_REQUIRED` |
| **Evidence-Schema 3.0** | bestehendes Trägerformat | nein | **ja** | nein | **ja** | **ja** | **ja** | **ja** | nein | `SEPARATE_DECISION_REQUIRED` |
| **Gate-Eingabe** | Zuführung an einen Gate-Evaluator | nein | **ja** | nein | **ja** | **ja** | **ja** | **ja** | **ja** | `NOT_AUTHORIZED` |
| **OD-37-Nachweis** | Nachweisbündel für die Ziel-Instanz | **ja** | teilweise | **ja** | **ja** | nein | mittelbar | **ja** | **ja** | `SEPARATE_DECISION_REQUIRED` |

### Erläuterung der Statuswerte

- **`OPTION_ONLY`** — technisch denkbar, in B2D-P weder gewählt noch spezifiziert.
- **`LOCAL_ONLY`** — darf entstehen, aber ausschließlich lokal und unversioniert.
- **`NOT_AUTHORIZED`** — darf in keiner B2D-Phase entstehen.
- **`SEPARATE_DECISION_REQUIRED`** — verlangt eine eigenständige A0-Entscheidung,
  vgl. **D-061 Teil O**.

**Warum die Sequenzbedingung besteht:** KB-04 ist im Readiness-Contract
runtime-scoped und mit den Mapping-Gate-Punkten **7**, **8** und **11**
verknüpft. Ein Security-Control-Form-Artefakt für KB-04 würde damit die
**Eingabefläche des Gate-Evaluators** berühren. Nach **ADR-0013** wäre ein
solches Artefakt zudem **negative-evidence-only** und könnte **niemals** ein
Gatekriterium erfüllen — es könnte ein Gate nur blockieren, nie freigeben.

---

## 15 — Gate- und OD-37-Trennung

| Aussage | Geltung |
| --- | --- |
| **B2D bereitet Nachweise vor.** | ja |
| **B2D wertet kein Gate aus.** | verbindlich |
| **B2D setzt kein Gate auf PASS.** | verbindlich |
| **B2D hebt keine Control hoch.** | verbindlich |
| **B2D setzt SB-S04 nicht wirksam.** | verbindlich |
| **B2D schließt OD-37 nicht.** | verbindlich |

Contract §17 hält für beide Gates ausdrücklich fest: **keine Auswertung**,
Status bleibt `NOT EVALUATED`. Contract §18 sperrt **reale Gatefreigabe** und
**Control-Uplift**.

### Zusätzlicher Bedarf für OD-37

OD-37 verlangt den **Nachweis auf der Ziel-Instanz**. Contract §17 nennt als
später benötigte Evidenz: **Rechteauflistung vor und nach dem Start** ·
**NT-04 und NT-05 bestanden** · **Mountliste je Identität** ·
**Auditeintrag**.

Darüber hinaus gilt:

| # | Zusätzlicher Bedarf |
| --- | --- |
| 1 | **KB-03-Anteil** — OD-37 nennt KB-03 gleichrangig neben KB-04; KB-03 ist **nicht** Gegenstand von CBP-WP-022 |
| 2 | **reale Ziel-Instanz-Nachweise** |
| 3 | **Auditeintrag** — dieser ist RT-2-nah, und **RT-2 ist nicht implementiert** |
| 4 | **separate Reconciliation** |
| 5 | **separate A0-Decision** |

**Ergebnis: OD-37 kann in B2D ausschließlich vorbereitet werden.**

---

## 16 — Contract-§10.3-Isolation

| Aussage | Geltung |
| --- | --- |
| **`KB04-T-P10` und `KB04-T-N25` bleiben Coverage Gaps.** | verbindlich, D-062 |
| **Beide blockieren B2D nicht.** | Contract §18 nennt Schreibzeitvalidierung nicht im B2D-Scope; §16 und §17 verlangen sie nicht |
| **Beide dürfen in keiner B2D-Phase als abgedeckt erscheinen.** | verbindlich |
| **Keine Schreibzeitvalidierung in B2D.** | verbindlich |
| **Keine atomare Ersetzungslogik in B2D.** | verbindlich |

Beide Lücken betreffen **Contract §10.3 Schreibzeitvalidierung**. Es existiert
keine Validierungsfunktion, keine Prüfung atomarer Ersetzung und keine Prüfung
des temporären Schreibkontexts; der zugehörige ReasonCode ist ausschließlich
deklariert und hat keinen produktiven Verwendungsort.

**Eine spätere §10.3-Phase benötigt eine eigene Scopefreigabe sowie eine
erneute ADR- und Decision-Erforderlichkeitsprüfung** — so bereits in **D-062
Teil J** festgelegt.

---

## 17 — Risikokandidaten

**Status aller sechs: `RISK_CANDIDATE_NOT_REGISTERED`.** Es wird **keine
Risiko-ID erzeugt** und **nichts im Risk Register registriert**.

### 1 — Falsche Zielinstanz

**Beschreibung** der Lauf trifft eine andere als die vorgesehene Instanz ·
**Auslöser** mehrdeutige Zielbezeichnung, Verwechslung beim Wechsel zwischen
Umgebungen · **Auswirkung** Rechteänderungen oder Schreibversuche außerhalb
der Referenzumgebung · **Prävention** dokumentierte, eindeutig bezeichnete
Zielinstanz; Bestätigung je Lauf · **Detektion** Abgleich der bestätigten
Zielbezeichnung unmittelbar vor Beginn · **Abbruch** bei jeder Unklarheit ·
**Restgrenze** die Zielwahl bleibt eine menschliche Handlung · **Phase**
B2D-E.

### 2 — Unzureichende Isolation

**Beschreibung** die Referenzumgebung ist nicht hinreichend von produktiven
Beständen getrennt · **Auslöser** geteilte Speicherbereiche, gemeinsame
Einbindungen · **Auswirkung** Nebenwirkungen außerhalb des Testbereichs ·
**Prävention** dedizierte, nicht produktive Instanz; nachweislich neue und
leere Zielstruktur · **Detektion** Preflight nach Contract §9.1; jede
unbekannte Bestandsdatei führt zur Einstufung als Migration · **Abbruch** bei
jedem Bestandsfund · **Restgrenze** der Isolationsnachweis bleibt
organisatorisch · **Phase** B2D-E.

### 3 — Umgehung der B2B-Apply-Grenze

**Beschreibung** ein mutierender Helfer entsteht faktisch doch im Repository ·
**Auslöser** Bequemlichkeit bei wiederholten Läufen · **Auswirkung** die von
ADR-0014 gezogene Architekturgrenze wird verletzt · **Prävention** Setup
bleibt hostseitig und operatorgeführt; kein `apply_plan`; keine mutierende
Funktion im Repository · **Detektion** Diff-Prüfung auf `core/**` und auf
mutierende Aufrufe · **Abbruch** bei jedem mutierenden Repositorycode ·
**Restgrenze** die Werkzeugform des Setups bleibt außerhalb des Repositorys
ungeregelt · **Phase** B2D-P und B2D-H.

### 4 — Fehlender Snapshot oder Recovery-Punkt

**Beschreibung** ein Lauf beginnt ohne Wiederherstellungsmöglichkeit ·
**Auslöser** Zeitdruck, Annahme der Harmlosigkeit · **Auswirkung** ein
Fehlzustand ist nicht rücksetzbar; der Contract gibt **keine Rollback-Zusage**
· **Prävention** Anforderungen R-1 bis R-4 · **Detektion** Checklistenpunkt 6
· **Abbruch** ohne bestätigten Recovery-Punkt kein Lauf · **Restgrenze** die
Gültigkeit des Snapshots wird nicht technisch erzwungen · **Phase** B2D-E.

### 5 — Ausführung auf dem falschen Host

**Beschreibung** der Lauf startet auf einem anderen System als der
Referenzinstanz · **Auslöser** parallele Sitzungen, verwechselte Kontexte ·
**Auswirkung** reale Rechte- oder Schreibwirkung außerhalb des Testbereichs ·
**Prävention** ausdrückliche Zielbestätigung durch den Human Maintainer
unmittelbar vor Beginn · **Detektion** Abgleich der bestätigten Umgebung ·
**Abbruch** bei jeder Abweichung · **Restgrenze** rein organisatorisch ·
**Phase** B2D-E.

### 6 — Beschädigung realer Daten

**Beschreibung** ein Testschritt verändert oder zerstört echte Bestände ·
**Auslöser** Kombination aus Risiko 1, 2, 4 und 5 · **Auswirkung** Datenverlust
· **Prävention** Isolation, leere Zielstruktur, Snapshot, erwartet
scheiternde statt erzwungene Schreibvorgänge · **Detektion** Post-Validation
nach Contract §9.3 · **Abbruch** bei jedem unerwarteten Erfolg eines
Schreibvorgangs · **Restgrenze** ein Restrisiko bleibt bestehen · **Phase**
B2D-E.

> **Verbindlich: Vor B2D-E muss entschieden werden, ob und wie diese
> Kandidaten als kanonische Risiken registriert werden.** Diese Entscheidung
> ist in B2D-P ausdrücklich **nicht** getroffen.

---

## 18 — Human-Maintainer-Autorisierungsmatrix

| Gegenstand | Nova-Freigabe ausreichend | A0 erforderlich | ADR-Prüfung erforderlich | Reale Infrastruktur | Repositoryänderung | Commitgrenze | Derzeitiger Status |
| --- | :-: | :-: | :-: | :-: | --- | --- | --- |
| **B2D-P** | **ja** | nein | nein | **nein** | ein Plandokument, neun Spiegel | eigener Commit | **autorisiert** |
| **B2D-H** | nein | **ja**, sobald CLI oder Config entstünde | **ja**, sobald öffentliche Semantik entstünde | nein | offen | eigener Commit | **nicht autorisiert** |
| **B2D-E** | nein | **ja, je Lauf** | nein bei reiner Beobachtung | **ja** | **keine** | **kein Commit** | **nicht autorisiert** |
| **B2D-V** | nein | **ja** | nein | nein | Statusspiegel | eigener Commit | **nicht autorisiert** |
| **B2D-G** | nein | **ja** | **ja** | nein | Gate-, Decision- und Registerdateien | eigener Commit | **nicht autorisiert** |
| **Evidence-Producer** | nein | **ja** | **ja** | nein | Produktionscode | eigener Commit | **nicht autorisiert** |
| **Gate-Eingabe** | nein | **ja** | **ja** | nein | Gatekopplung | eigener Commit | **nicht autorisiert** |
| **Gateauswertung** | nein | **ja** | **ja** | nein | Gatestatus | eigener Commit | **nicht autorisiert** |
| **OD-37-Schließung** | nein | **ja** | **ja** | **ja** mittelbar | Register und Gate | eigener Commit | **nicht autorisiert** |
| **Nutzung realer Infrastruktur** | nein | **ja, je Lauf** | nein | **ja** | keine | **kein Commit** | **nicht autorisiert** |

**B2D-P ist die einzige derzeit autorisierte Zeile.** Eine Freigabe für B2D-P
ist ausdrücklich **keine** Freigabe für irgendeine andere Zeile.

---

## 19 — Stop-Bedingungen

Bei **jeder** der folgenden Bedingungen gilt: **keine Fortsetzung.**

| # | Stop-Bedingung |
| ---: | --- |
| 1 | **Zielinstanz nicht eindeutig** bestimmt oder bestätigt |
| 2 | **Produktive Instanz erkannt** |
| 3 | **Snapshot oder Recovery-Punkt nicht bestätigt** |
| 4 | **Identitätsbindung unvollständig** oder nicht positiv validiert |
| 5 | **Reale Werte im Repository** gefunden |
| 6 | **Mountzustand nicht eindeutig** feststellbar |
| 7 | **Unerwarteter Schreibzugriff erfolgreich** — SB-S04 ist berührt |
| 8 | **Symlink-Auflösung nicht sicher blockiert** |
| 9 | **Cleanup nicht gesichert** |
| 10 | **Evidence-Form nicht entschieden**, aber Evidenz soll gekoppelt werden |
| 11 | **Gate- und Execution-Scope vermischt** |
| 12 | **B2B-Apply-Grenze verletzt** — mutierender Repositorycode |
| 13 | **Contract §10.3 fälschlich als geschlossen dargestellt** |

Zusätzlich gilt die Grundregel des Contracts: **nicht feststellbar ist nicht
erfüllt.** Eine Dimension, die nicht positiv validiert werden kann, gilt als
Verletzung, nicht als offen.

---

## 20 — Do-not-run

Dieses Dokument enthält **ausdrücklich**:

- **keine ausführbaren Befehle**,
- **keine Copy-and-paste-Kommandos**,
- **keine Kommandos mit erhöhten Rechten**,
- **keine Besitz- oder Rechteänderungsbefehle**,
- **keine Anlage von Benutzern oder Gruppen**,
- **keine Einbindungsbefehle**,
- **keine Schreibversuche**,
- **keine Erzeugung von Verweisobjekten**,
- **keine Cleanupbefehle**,
- **keine NT-Ausführung**.

Die Kapitel 11 bis 13 beschreiben **Anforderungen und Sicherheitsgrenzen**,
nicht Handlungsanweisungen. Wer aus diesem Dokument einen Ablauf ableitet,
benötigt dafür eine **eigene, ausdrückliche A0-Freigabe** und die vollständige
Erfüllung der Checkliste aus Kapitel 10.

---

## Nachtrag B2D-GOV — Kanonisierte Ausführungsvoraussetzungen

> **Ergänzt in Phase B2D-GOV.** Dieser Nachtrag **schwächt keine der
> vorstehenden Sicherheitsgrenzen ab**; er macht sie kanonisch verbindlich.
> **B2D-P ist `committed` (`b409d25`).**

### N.1 — Entscheidungsgrundlage

| Feld | Wert |
| --- | --- |
| Decision | **D-063**, `accepted`, **A0**, 2026-08-04, Teile A–O |
| Ergebnis | **`B2D_EXECUTION_PREREQUISITES_ESTABLISHED`** |
| ADR-Gate | **`ADR_NOT_REQUIRED`** — innerhalb ADR-0014, D-060, D-061 und D-062 |
| Vorlauf | **B2D.1** read-only Audit, `PASS WITH NOTES` |

### N.2 — Kanonisierte Risiken

| ID | Titel | Schwere | Status |
| --- | --- | --- | --- |
| **R-35** | Reale KB-04-Nachweisausführung trifft eine **falsche oder unzureichend isolierte Zielinstanz** | **hoch** | **offen** |
| **R-36** | Reale KB-04-Nachweisausführung beginnt **ohne bestätigten Wiederherstellungspunkt** | **hoch** | **offen** |

Von den **sechs** Kandidaten aus Kapitel 17 wurden damit **vier** in **R-35**
gebündelt — *falsche Zielinstanz*, *unzureichende Isolation*, *falscher Host*
und *Beschädigung realer Daten* als **Auswirkung**. **Kandidat 3 — Umgehung
der B2B-Apply-Grenze — ist durch R-12 abgedeckt** und erhielt **keine eigene
ID**. **R-20 wurde nicht erweitert**, **R-18 nicht wiederverwendet**.

### N.3 — Harnessentscheidung

> ### **`NO_HARNESS_REQUIRED`**

Die **reale Erhebung bleibt hostseitig und operatorgeführt**; der **vorhandene
Validator** verarbeitet injizierte Beobachtungen mit Herkunft **`OBSERVED`**.
**Es fehlt kein technischer Repositorybaustein.** Ein Repository-Harness
erzeugte zusätzliche Angriffs- und Governancefläche in genau der Zone, die
ADR-0014 freihält.

**Nicht umgesetzt:** **H1** (Testhelper) · **H2** (operatorgeführtes Script) ·
**H3** (Repository-CLI) · keine CLI · kein Script · **kein externes Werkzeug
durch das Repository definiert**. **Ein optionaler zukünftiger H1-Testhelper
benötigt eine eigene Freigabe.**

### N.4 — Maximaler späterer B2D-E-Scope

Ausschließlich die **sechs** B2D-real-only-Fälle: **`KB04-T-N07`** ·
**`KB04-T-N08`** · **`KB04-T-N14`** · **`KB04-T-N31`** · **`KB04-T-N33`** ·
**`KB04-T-P12` / Dimension D-I**.

**`KB04-T-P10` und `KB04-T-N25` bleiben Coverage Gaps** und sind **kein Teil
einer B2D-E-Erfolgsaussage**.

### N.5 — Producer-Unabhängigkeit

**B2D-E benötigt keinen neuen Evidence-Producer.** Zulässige spätere Formen
bleiben **lokal-only**: Rohbeobachtung · lokales Testprotokoll ·
Operatorbestätigung · normalisierte In-Memory-Beobachtung · lokale
Hashbindung. **Diese Formen sind keine Gate-Eingabe.** **In B2D-GOV wurde
nichts erzeugt.**

### N.6 — Freigabe je Lauf

**D-063 autorisiert keinen B2D-E-Lauf.** Jeder spätere Lauf verlangt zehn
Bestätigungen: ausdrückliche **Human-Maintainer-Ausführungsfreigabe** ·
Bindung an **genau eine lokal bezeichnete Zielinstanz** · **nicht produktiver**
Zustand · **neue und leere** Zielstruktur · **gültiger Recovery-Punkt** ·
**lokale Identitätsbindung** · **Stop- und Cleanupplan** · **Fallumfang** ·
**B2D-G nicht gleichzeitig freigegeben** · **konkreter Startzeitpunkt**.

Eine Ausführungsfreigabe gilt für **genau einen Lauf**, ist **nicht
übertragbar** und **nicht wiederverwendbar**. Sie verfällt bei anderer
Instanz, anderem Strukturzustand, geänderter Identitätsbindung, geändertem
Fallumfang, ausgelöster Stop-Bedingung sowie bei Änderung von Contract,
ADR-0014 oder D-063.

**Eine globale A0-Pauschalfreigabe ist unzulässig.** Die konkrete Form der
per-run Dokumentation wird **erst in einer separaten
B2D-E-Autorisierungsphase** festgelegt.

**Reale Werte bleiben außerhalb des Repositorys.**

### N.7 — Unverändert getrennte Gegenstände

**B2D-E und B2D-G bleiben getrennt** — nie im selben Lauf. **Nicht Bestandteil
von D-063:** anonymisierte versionierbare Zusammenfassung ·
Security-Control-Form · Evidence-Schema-3.0-Produktion · Evidence-Producer ·
Gate-Eingabe · Gateauswertung · Gatefreigabe · Control-Uplift ·
SB-S04-Aktivierung · **OD-37-Reconciliation und -Schließung** · KB-03-Nachweis
· Auditeintrag · RT-2 · **Contract §10.3**.

### N.8 — Status nach B2D-GOV

**B2D-H**, **B2D-E**, **B2D-V**, **B2D-G** und **reale Infrastruktur** bleiben
**nicht autorisiert**. Die Autorisierungsmatrix aus Kapitel 18 gilt
unverändert fort; **B2D-H** trägt nun zusätzlich das Ergebnis
**`NO_HARNESS_REQUIRED`**.

**Eine Voraussetzung ist keine Ausführung, und eine Ausführungsfreigabe ist
kein Nachweis.**

---

## Aussagegrenzen dieses Dokuments

| Nicht belegt | Tatsächlicher Stand |
| --- | --- |
| Eine Profil-A-Instanz existiere | **keine** |
| Ein Recht sei gesetzt | **keines** |
| NT-04 oder NT-05 seien ausgeführt | **nicht ausgeführt** |
| Eine der sechs real-only Kennungen sei bestanden | **keine** |
| Ein Gate sei ausgewertet | beide **`NOT EVALUATED`** |
| Eine Control sei hochgestuft | **12 `DOCUMENTED ONLY`**, KB-04 darunter |
| SB-S04 sei wirksam | **nicht wirksam** |
| OD-37 sei geschlossen | **offen** |
| Contract §10.3 sei umgesetzt | **technisch offen** |
| Ein Risiko sei registriert | **sechs Kandidaten, keine ID** |
| B2B-Apply sei freigegeben | **nicht autorisiert** |

**Ein Plan ist keine Ausführung, eine Freigabespezifikation ist keine
Freigabe, und eine beschriebene Prüfung ist kein Nachweis.**
