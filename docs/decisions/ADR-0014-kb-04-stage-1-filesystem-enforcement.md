# ADR-0014 — KB-04 Stage 1 Filesystem Enforcement Architecture

*Durchsetzungsarchitektur der Dateisystemrechte, Stufe 1*

| Feld | Wert |
| --- | --- |
| **Status** | **accepted** |
| Datum | 2026-08-03 |
| Entscheider | **Human Maintainer** |
| Angenommen am | **2026-08-03** |
| **Autorität nach Annahme** | **A1** |
| Grundlage der Entscheidungen | **A0** — Human Maintainer, **D-059** |
| Erfasst in | **CBP-WP-022** (Phase B1B — ADR Authoring and Design Decision) |
| Vorgeschaltetes Gate | **D-058** (A0) — Ergebnis **`ADR_REQUIRED`** |
| Verhältnis | konkretisiert **ADR-0009** (Technische Sicherheitsgrundlage) für **KB-04**; übernimmt die Schreibsemantik aus **ADR-0010** und **ADR-0011** unverändert; respektiert die Bereichsgrenze aus **ADR-0007** |
| Entscheidungen | **D-059** (A0) |
| Supersedes | — |
| Amends | — (**ADR-0009 wird konkretisiert, nicht abgelöst**) |
| Superseded by | — |
| Schließt | **keine** offene Entscheidung — **OD-37 bleibt offen** |

> **Dieser ADR ist angenommen und bindend.** Er trägt Autoritätsklasse **A1**.
> Die zugrunde liegende Human-Maintainer-Entscheidung **D-059** trägt **A0**.
>
> **Er entscheidet eine Architektur, er implementiert nichts.** KB-04 bleibt
> **`DOCUMENTED ONLY`**. Es wird kein Recht gesetzt, kein Besitz zugewiesen,
> kein Test ausgeführt, kein Gate ausgewertet und nichts bereitgestellt.

---

## Kontext

**KB-04 — Dateisystemrechte** ist **Stufe 1** der neunstufigen technischen
Durchsetzungsreihenfolge und laut
[Spezifikation](../security/TECHNICAL_SECURITY_FOUNDATION_SPECIFICATION.md)
§KB-04 die **unterste tragende Ebene**: *versagt sie, sind KB-05 bis KB-07
wirkungslos*. Die Anforderung ist dort vollständig formuliert — explizite Owner-
und Gruppenregeln, keine world-writable Dateien, kein Schreibrecht auf Canonical
durch Retrieval oder Ingest, blockierte Symlink-Escapes, sichere Dateierstellung
und atomare Writes.

**Die Lösung ist dort nicht formuliert.** Phase B1A hat achtzehn Quellen
geprüft und **keinen Konflikt**, aber eine systematische Lücke gefunden: die
Spezifikation führt *Dateimodi, Owner, Gruppen* als **Deployment Required**
(§469), das
[Identity Model](../security/SERVICE_IDENTITY_AND_PRIVILEGE_MODEL.md) enthält
ausdrücklich *keine Unix-Benutzer, keine Gruppen, keine UID- oder GID-Werte und
keine Hostpfade* und listet dieselben Werte unter *Offene Deploymentwerte* mit
dem Nachsatz **„Keiner dieser Werte wird hier festgelegt."** Der
[Foundation Plan](../roadmap/PHASE_1_FOUNDATION_PLAN.md) führt *konkrete UIDs,
GIDs, Dateimodi* als **offen — Deployment**.

Damit war **sechs von zehn Designachsen** keine Authority zugeordnet:
Besitz- und Gruppenmodell, UID-/GID-Abbildung samt Host-/Container-Grenze,
konkrete Datei- und Verzeichnismodi, Durchsetzungsakteur, Verifikations- gegen
Korrektursemantik sowie Migrations- und Reparaturverhalten. **D-058** hat daraus
verbindlich **`ADR_REQUIRED`** abgeleitet.

Dieser ADR schließt diese Lücke — **nicht durch das Festlegen konkreter Werte**,
was der Spezifikation widerspräche, sondern durch die Entscheidung, **wo** die
Werte entstehen, **wer** sie durchsetzt, **wer** sie niemals verändern darf und
**wie** ihre Einhaltung nachgewiesen wird.

## Problem

| Frage | Zustand vor diesem ADR |
| --- | --- |
| Wer besitzt die Authority über Besitz und Rechte? | nirgends festgelegt |
| Welches Besitz- und Gruppenmodell gilt? | ausdrücklich nicht festgelegt |
| Wer darf Rechte initialisieren? | nirgends festgelegt |
| Wer darf Rechte reparieren? | nirgends festgelegt |
| Darf ein Langläufer Rechte selbst ändern? | nirgends festgelegt |
| Wird geprüft oder korrigiert? | nirgends festgelegt |
| Wann wird geprüft? | nirgends festgelegt |
| Wie bleiben Host- und Containeridentität deckungsgleich? | nirgends festgelegt |
| Welche Plattformgrenze gilt für die Durchsetzung? | nur implizit über Profil A |
| Wie werden Bestandsdaten mit falschen Rechten behandelt? | nirgends festgelegt |

**Ohne diese Entscheidungen ist KB-04 nicht implementierbar** — und jede
Implementierung würde die Antworten stillschweigend und unbelegt selbst treffen.

## Bindende Authority

| Quelle | Klasse | Bindende Aussage |
| --- | :---: | --- |
| Spezifikation §KB-04 | A2 | Ziel, Bedrohung, Anforderung, **Nachweis: Rechteauflistung vor und nach dem Start**, NT-04/NT-05, Evidence-Ereignis `incident`, **SB-S04**, **Rücksetzung auf den dokumentierten Ausgangszustand** |
| Spezifikation §11 | A2 | KB-04 = **Stufe 1**; *eine spätere Stufe darf eine frühere technische Kontrolle nicht ersetzen* |
| Spezifikation §469 | A2 | **Dateimodi, Owner, Gruppen — Deployment Required** |
| **ADR-0009** | **A1** | Technische Sicherheitsgrundlage; KB-04 als Control |
| **ADR-0010**, **ADR-0011** | **A1** | atomare Schreibweise: exklusive Temp-Datei, `fsync`, `os.replace`, kein Schreiben außerhalb des Roots, keine Hard- oder Symlinks — **implementiert** |
| **ADR-0007** | **A1** | Repository- und Workspace-Grenze; RT-1/RT-2/RT-3 |
| Acceptance Matrix §KB-04 | A2 | Status **`DOCUMENTED ONLY`**, Negativtests **NT-04**, **NT-05**, Nachweisstufe **4**, Stop-Bedingung **SB-S04** |
| Identity Model | A2 | zwei logische Identitäten; **V-1** kein root · **V-3** kein privilegierter Container · **V-5** kein Canonical-Schreiben ohne dokumentierte Freigabe · **V-11** kein Backup-Schreiben · **V-12** keine Impersonation; **M-1** bis **M-4**; Mount-Matrix; *Offene Deploymentwerte* |
| Permission Model | A2 | OS-Dateirechte als eigene Ebene; nicht privilegierte UIDs; kanonischer Bestand für Dienstkonten nicht schreibbar; **bei unklarer Berechtigung gilt `forbidden`** |
| Profil-A-Bundle | A2 | `read_only`, **`cap_drop: ALL`**, `no-new-privileges`, kein `privileged`; acht Bereiche mit abstrakten Ownerrollen; **`KB-04 → filesystem-permission-target-model`**; UID und GID **ausschließlich** als fail-closed Operatorvariablen |
| Installation Runbook §2 | A2 | Pflichtwerte einschließlich **UID und GID** werden **im lokalen Operator-Workspace außerhalb des Repositorys** befüllt; **eine befüllte Operator-Datei wird niemals zurück ins Repository kopiert** |
| Readiness Gate 3, 5 | A2 | *OS-Rechte umgesetzt — Rechteauflistung, keine world-writable* (Stufe 2) · *Canonical read-only nachgewiesen — NT-04 bestanden* (Stufe 4) |
| Mapping-Gate 7, 8, 11 | A2 | KB-01…KB-04 als Voraussetzung; Symlink-Verhalten geprüft |
| **OD-37** | offen | produktive Isolation auf der Ziel-VM (KB-03, KB-04) — **Deployment Required** |
| **D-057**, **D-058** | A0 | Registrierung und ADR-Gate von CBP-WP-022 |

**Keine dieser Quellen wird durch diesen ADR überschrieben.**

## Sicherheitsinvarianten

Die sieben in Phase B1A hergeleiteten Invarianten sind **unverändert bindend**
und die Prüfgröße jeder späteren Umsetzung.

| # | Invariante | Beleg |
| --- | --- | --- |
| **I-1** | **Deny-by-default auf Dateiebene** | Spezifikation §KB-04 |
| **I-2** | **Keine world-writable geschützten Artefakte** | §KB-04, Acceptance Matrix |
| **I-3** | **Retrieval besitzt keinen Schreibzugriff auf Canonical** | §KB-04, V-5, Mount-Matrix |
| **I-4** | **Ingest besitzt keinen unkontrollierten Schreibzugriff auf Canonical** | §KB-04, V-5 |
| **I-5** | **Symlink-Escapes werden verhindert** | §KB-04, M-4, **NT-05** |
| **I-6** | **Schreibvorgänge erzeugen keinen unsicheren Zwischenzustand** | §KB-04; ADR-0010, ADR-0011 |
| **I-7** | **Rechtefehler führen fail-closed, nicht zu stiller Abschwächung** | §KB-04, SB-S04, Permission Model |

## Entscheidungsfaktoren

| # | Faktor | Gewicht | Herkunft |
| ---: | --- | :---: | --- |
| 1 | Einhaltung von **I-1 bis I-7** | **Ausschlusskriterium** | B1A, Spezifikation |
| 2 | **V-1** kein root, **V-3** kein privilegierter Container | **Ausschlusskriterium** | Identity Model |
| 3 | Vereinbarkeit mit **`cap_drop: ALL`**, `no-new-privileges`, `read_only` | **Ausschlusskriterium** | Profil-A-Bundle |
| 4 | **Keine realen UID-/GID-Werte, Modi, Benutzer oder Gruppen im Repository** | **Ausschlusskriterium** | Spezifikation §469, Identity Model, Runbook §2 |
| 5 | Least Privilege im Dauerbetrieb | hoch | Permission Model |
| 6 | Trennung von Setup und Runtime | hoch | D-058 Achse 5.2 |
| 7 | Fail-closed ohne stille Abschwächung | hoch | I-7, SB-S04 |
| 8 | Nachweisbarkeit durch **NT-04** und **NT-05** | hoch | Acceptance Matrix |
| 9 | Kompatibilität mit **ADR-0010/ADR-0011** | hoch | implementierter Bestand |
| 10 | Reversibilität der konkreten Werte | mittel | D-058 Teil E |
| 11 | Portabilität und Werkzeugarmut (stdlib-only) | mittel | Projektpraxis |
| 12 | Auditierbarkeit | mittel | Nachweis „vor und nach dem Start" |
| 13 | Komplexität | mittel | Angemessenheit |
| 14 | Eignung für **Profil A** | hoch | ADR-0002, Runbooks |

## Bewertete Optionen

**Option A — Host-authoritative Deployment Enforcement.** Der Setup- und
Deploymentvorgang auf dem Host besitzt die Authority. Besitz und Rechte werden
**vor** dem Runtime-Start hergestellt. Die Runtime läuft mit vorgegebenen
unprivilegierten Identitäten, **validiert** den Zustand und scheitert
fail-closed. Kein Langläufer korrigiert Rechte.

**Option B — Privileged Bootstrap, Unprivileged Runtime.** Ein abgegrenzter
Initialisierungsprozess **innerhalb der Bereitstellungseinheit** darf beim Setup
oder Start Besitz und Rechte herstellen; danach läuft die Runtime
unprivilegiert. Bootstrap und Runtime sind getrennte Verantwortlichkeiten; die
Initialisierung muss idempotent sein.

**Option C — Runtime Self-Repair.** Die Runtime-Komponenten korrigieren Besitz
und Rechte beim Start oder im Betrieb selbst. Erfordert erhöhte Rechte
beziehungsweise zusätzliche Capabilities.

**Option D — ACL-centric Enforcement.** POSIX-ACLs sind die Hauptdurchsetzung;
Owner-, Gruppen- und Modusbits sind nur Basis oder Fallback. Erfordert
zusätzliche Werkzeuge, Dateisystemoptionen und Plattformzusagen.

**Option E — Declarative Target Model without Runtime Validation.** *(ergänzt,
weil `bundle.json` KB-04 bereits als `filesystem-permission-target-model`
führt.)* Das Repository beschreibt das Zielmodell rein dokumentarisch; die
Runtime prüft nichts. Diese Option macht den heutigen Zustand explizit und dient
als Nullvergleich.

### Optionsmatrix

| Kriterium | **A** | **B** | **C** | **D** | **E** |
| --- | :---: | :---: | :---: | :---: | :---: |
| **I-1 bis I-7 vollständig erfüllbar** | **ja** | ja | **nein** (I-7) | teilweise | **nein** (I-7) |
| Least Privilege im Dauerbetrieb | **hoch** | hoch | **niedrig** | mittel | n. a. |
| Fail-closed | **stark** | stark | **schwach** — Korrektur statt Ablehnung | mittel | **keines** |
| Trennung Setup / Runtime | **vollständig** | vollständig | **keine** | unabhängig | n. a. |
| Root- oder Privilegbedarf | **keiner in der Runtime** | Bootstrap privilegiert | **Runtime privilegiert** | Setup privilegiert | keiner |
| Vereinbarkeit `cap_drop: ALL`, `read_only` | **ja** | **nein** im Bundle | **nein** | ja | ja |
| Vereinbarkeit **V-1 / V-3** | **ja** | **konfliktnah** | **nein** | ja | ja |
| Host-/Container-Konsistenz | **explizit erklärt und geprüft** | im Bootstrap gekapselt | **driftanfällig** | zusätzlich ACL-Ebene | ungeprüft |
| Migrationsfähigkeit | explizit, operatorgeführt | automatisierbar | **implizit und unkontrolliert** | komplex | keine |
| Reparierbarkeit | explizit, getrennter Modus | gut | **still** | mittel | keine |
| Auditierbarkeit | **hoch** — Auflistung vor und nach dem Start | mittel | **niedrig** | mittel | keine |
| Portabilität, stdlib-only | **hoch** | mittel | mittel | **niedrig** | hoch |
| Komplexität | **niedrig** | mittel | mittel | **hoch** | minimal |
| Reversibilität konkreter Werte | **hoch** — Werte außerhalb des Repositorys | mittel | niedrig | niedrig | n. a. |
| Missbrauchsrisiko | **gering** | mittel | **hoch** — Eskalationsfläche | mittel | n. a. |
| Wirkung auf **OD-37** | **strukturiert** | strukturiert | verlagert | verkompliziert | **keine** |
| Nachweis durch **NT-04 / NT-05** | **direkt** | direkt | **verfälscht** — Selbstheilung maskiert den Befund | zusätzlich | **nicht möglich** |
| Wirkung auf beide Gates | vorbereitend | vorbereitend | vorbereitend | vorbereitend | **keine** |
| Kompatibilität **ADR-0010/0011** | **vollständig** | vollständig | vollständig | vollständig | vollständig |
| Eignung für **Profil A** | **hoch** | mittel | **unvereinbar** | niedrig | n. a. |

## Entscheidung — Ausgewählte Architektur

**Gewählt wird Option A** in der ausformulierten Gestalt

> **Host-authoritative Enforcement mit deklarativem Zielmodell und
> read-only Runtime-Validierung.**

Die Architektur trennt drei Schichten mit **disjunkten** Befugnissen.

| Schicht | Ort | Befugnis | Ausdrücklich nicht |
| --- | --- | --- | --- |
| **Zielmodell** | dieses Repository | beschreibt **abstrakt**: Bereiche, Rollen, Zugriffsart, Rechteprofilklassen, Invarianten, Prüfregeln | enthält **keine** realen Identitäten, UIDs, GIDs, Modi, Benutzer, Gruppen oder Hostpfade |
| **Durchsetzung** | Deployment und Operator, **außerhalb** der Runtime, **außerhalb** des Repositorys | bindet Rollen an konkrete Identitäten, **setzt** Besitz und Rechte, **repariert** in einem ausdrücklich aufgerufenen Modus | ist **kein** Bestandteil der laufenden Dienste |
| **Validierung** | Runtime | **liest** den Ist-Zustand, vergleicht ihn mit dem Zielmodell, meldet, **scheitert fail-closed** | **setzt, ändert, repariert und mildert nichts** |

**Der Kern der Entscheidung:** Das Repository entscheidet das **Modell** und die
**Prüfung**; das Deployment liefert die **Werte** und die **Durchsetzung**; die
Runtime besitzt **ausschließlich Lese- und Ablehnungsrecht**.

Damit ist Option B nicht schlechthin verworfen, sondern **verortet**: die
Initialisierungsverantwortung von Option B existiert, sie liegt jedoch
**vollständig auf der Deployment-Seite der Grenze** und niemals in einer
privilegierten Komponente der Bereitstellungseinheit.

### 1 — Authority-Modell

| Rolle | Darf | Darf **niemals** |
| --- | --- | --- |
| **Deployment-/Setup-Akteur** (operatorgeführt, host-seitig) | Rollen an Identitäten binden · Besitz und Rechte **initial herstellen** · in einem **ausdrücklich aufgerufenen** Modus reparieren · Rücksetzung auf den dokumentierten Ausgangszustand | als Dauerprozess laufen · unbeaufsichtigt korrigieren |
| **Control Plane**, **Data Worker** | Rechte **lesen** · gegen das Zielmodell prüfen · Abweichung melden · **fail-closed abbrechen** | `chown`, `chmod`, Gruppen- oder Eigentümerzuweisung ändern · `umask` aufweichen · eine Abweichung tolerieren, umgehen, protokollieren-und-fortfahren |
| **Human Maintainer** | Zielmodell und Bindung freigeben · Rücksetzung anordnen | — |

**Kategorisch:** **Keine lang laufende Runtime-Komponente verändert jemals
Besitz, Gruppe, Modus oder Identität** — weder beim Start, noch im Betrieb, noch
zur Fehlerbehebung. Das ist eine **Architekturaussage**, keine
Konfigurationsoption, und gilt unabhängig davon, ob die Umgebung die nötigen
Privilegien böte.

### 2 — Identitätsmodell

**Getrennte Prozessidentitäten**, wie in D-034 und im Identity Model bereits
festgelegt: `svc-control-plane` und `svc-data-worker` bleiben **logische**
Rollen. Ergänzend entscheidet dieser ADR:

| Punkt | Entscheidung |
| --- | --- |
| Rollenprinzip | **getrennte Identitäten**, **keine** gemeinsame Sammelidentität |
| Gruppenprinzip | **rollenbezogene Gruppen**; eine gemeinsame Gruppe ausschließlich dort, wo eine Rolle schreibt und eine andere **lesen muss** |
| Kein Ersatz | Gruppenmitgliedschaft ersetzt **niemals** den Mountmodus (M-3) und **niemals** die Anwendungsautorisierung (KB-05) |
| Host-/Container-Abbildung | **explizite Identitätsbindung**, im Deployment erklärt, im Repository **nur** als abstrakte Rolle sichtbar |
| Herkunft der Werte | **konfigurierbar im Deployment**, **nie** im Repository, **nie** abgeleitet, **nie** mit Default |
| Prüfung | Die Runtime prüft beim Start, ob ihre **effektive** Identität der erklärten Bindung entspricht |
| Fehlende Bindung | **fail-closed** |
| Kollidierende Bindung — zwei Rollen auf dieselbe Identität | **fail-closed**; die Trennung ist der Zweck (KB-02) |
| Unauflösbare oder unbekannte Identität | **fail-closed**; keine Ersatzannahme, kein „unbekannt = erlaubt" |
| Drift | Jede Abweichung zwischen erklärter und effektiver Identität ist eine **Vertragsverletzung**, kein zu korrigierender Zustand |

**Keine realen UID- oder GID-Werte, Benutzer- oder Gruppennamen werden in diesem
ADR oder in irgendeinem Repository-Artefakt festgelegt.**

### 3 — Rechteprofil-Modell

Entschieden wird das **Modell**, nicht die endgültigen Einzelwerte. Jeder
geschützte Bereich erhält **genau eine** Profilklasse.

| Klasse | Bedeutung | Zugriff | Typischer Bereich |
| --- | --- | --- | --- |
| **PP-1** | **owner-write** | Eigentümerrolle liest und schreibt · **kein** Gruppenschreiben · **kein** World-Zugriff | rollenexklusive Schreibbereiche |
| **PP-2** | **owner-write, group-read** | Eigentümerrolle schreibt · **kontrollierte** Gruppe liest · **kein** Gruppenschreiben · **kein** World-Zugriff | Bereiche, die eine Rolle schreibt und eine andere liest |
| **PP-3** | **service-read-only** | **keine** Service-Identität besitzt Schreibrecht; Eigentümer liegt außerhalb der Service-Identitäten | **Canonical** |
| **PP-4** | **not-present** | Bereich wird **gar nicht** eingebunden — die stärkste Klasse | **Backup**, **RT-2** |

**Kategorische Regeln der Klassen:**

| # | Regel |
| --- | --- |
| 1 | **Kein World-Zugriff als Grundzustand** — deny-by-default (I-1); world-writable ist **ausnahmslos** verboten (I-2) |
| 2 | **Kein Gruppenschreibrecht**, außer eine Klasse verlangt es ausdrücklich; „bequem" ist kein Grund |
| 3 | **Execute-Bit nur zur Verzeichnisdurchquerung**, **niemals** auf Datenartefakten |
| 4 | **Kein setuid und kein setgid auf Dateien**; **setgid auf Verzeichnissen** ausschließlich dort, wo PP-2 Gruppenvererbung benötigt |
| 5 | **Restriktive `umask`** — sie darf **kein** World-Bit und **kein** Gruppenschreibrecht entstehen lassen; Neuanlagen erfüllen ihre Profilklasse **bei der Erstellung**, nicht nachträglich |
| 6 | **PP-4 schlägt jede andere Klasse** — ein nicht eingebundener Bereich braucht keine Rechte (M-3) |
| 7 | **Konfigurierbar sind ausschließlich die Bindungswerte** (Identitäten und deren Abbildung). **Profilklassen, Bereichszuordnung und Invarianten sind nicht konfigurierbar.** Es gibt **keinen** unsicheren Default und **keinen** Fallback; ein fehlender Pflichtwert blockiert — dasselbe Muster, das das Profil-A-Bundle bereits mit `${...:?...}` durchsetzt |
| 8 | **Ein Rechteprofil ersetzt niemals den Mountmodus.** Beide gelten; die schwächere Aussage gewinnt nie |

Die vollständige **Pfad-zu-Rolle-zu-Modus-Matrix** und die exakten symbolischen
oder numerischen Werte werden nach **§469 Deployment Required** gebunden und in
**B1C** vertraglich gefasst — siehe *Offene Implementierungsparameter*.

### 4 — Initialisierung

| Punkt | Entscheidung |
| --- | --- |
| Verantwortlich | **ausschließlich** der Deployment-/Setup-Akteur |
| Zeitpunkt | **vor** dem ersten Start der Runtime |
| Privilegien | die für Besitz- und Modussetzung nötigen Rechte — **host-seitig**, **außerhalb** der Bereitstellungseinheit, **nicht** als privilegierter Container (V-3) |
| Idempotenz | **erforderlich** — ein wiederholter Lauf über einen bereits korrekten Bereich verändert nichts und meldet „unverändert" |
| Teilweise Vorbereitung | **kein** Teilerfolg: ein unvollständig vorbereiteter Bereich gilt als **nicht vorbereitet** und blockiert den Start |
| Inkonsistente Bestandsdaten | **nicht automatisch anfassen** — melden, blockieren, dem Migrationsweg zuführen |
| Ergebnis | ein **dokumentierter Ausgangszustand** im Sinne der Rücksetzungsregel aus §KB-04 |

### 5 — Validierung

Validierung findet an **mehreren** Zeitpunkten statt und ist **überall
read-only**.

| Zeitpunkt | Gegenstand | Wirkung bei Abweichung |
| --- | --- | --- |
| **Installationszeit** | Zielmodell und Bindung vollständig, widerspruchsfrei, ohne Platzhalter | Installation **anhalten** |
| **Startzeit** *(vor der Aufnahme des Dienstes)* | effektive Identität gegen erklärte Bindung; Rechte und Modi der eingebundenen Bereiche; Mountmodi; Abwesenheit von PP-4-Bereichen | **Start verweigern** — der Dienst nimmt seine Aufgabe **nicht** auf |
| **Schreibzeit** | Einhaltung von I-6 bei jedem Schreibvorgang | Schreibvorgang **ablehnen** (bestehende Semantik aus ADR-0010/ADR-0011, unverändert) |
| **Gate-Zeitpunkt** | Nachweis für Readiness-Gate 3 und 5 | Kriterium bleibt **nicht erfüllt** — **keine** Hochstufung |

| Punkt | Entscheidung |
| --- | --- |
| Charakter | **strikt read-only**; die Validierung ist ein **Beobachter**, kein Akteur |
| Nachweisform | **Rechteauflistung vor und nach dem Start** — wie in §KB-04 gefordert |
| Fail-closed | **nicht feststellbar = nicht erfüllt.** Ein Zustand, der nicht **positiv** als vertragskonform belegt ist, gilt als Verletzung |
| Keine Abschwächung | **kein** Warnmodus, der trotzdem startet · **kein** „nur protokollieren" · **kein** Überspringen per Konfiguration · **kein** Fortfahren nach Teilprüfung |
| Ereignis | Eine Verletzung ist ein **`incident`** im Sinne von §KB-04 |
| Grenze | Die Validierung ist **kein** Ersatz für Mountmodi, Prozessidentität oder Anwendungsautorisierung — Stufe 1 wird durch spätere Stufen **ergänzt, nie ersetzt** (§11) |
| Dauerbetrieb | **keine** dauerhafte Hintergrundüberwachung als Sicherheitszusage; wiederholte Prüfung ist zulässig, ersetzt aber weder Startprüfung noch Mountgrenze |

### 6 — Migration und Reparatur

| Punkt | Entscheidung |
| --- | --- |
| Automatische Migration | **ausgeschlossen** |
| Auslösung | **nur** ausdrücklich, operatorgeführt, außerhalb des normalen Dienstbetriebs |
| Planungsmodus | **Architekturprinzip: Plan vor Wirkung.** Ein Reparatur- oder Migrationsvorgang muss zuerst einen **wirkungsfreien Plan** erzeugen können, der jede beabsichtigte Änderung benennt |
| Auditspur | **Pflicht** — Ausgangszustand, geplante Änderung, Ergebnis. Reparatur ohne Nachweis ist unzulässig |
| Aufbewahrung | Der Nachweis ist **Operational Evidence (RT-2)** im Sinne von ADR-0007. **RT-2 ist nicht implementiert**; solange es fehlt, ist die Nachweispflicht **nicht erfüllbar** und damit die Reparatur **nicht freigegeben** |
| Rückfall | **Rücksetzung auf den dokumentierten Ausgangszustand** (§KB-04) ist der Rückfallweg. **Kein** Datenrollback und **kein** Backupzugriff — V-11 verbietet Backup-Schreiben, PP-4 lässt Backup gar nicht erst zu |
| Rekursion | **nicht implizit.** Ein rekursiver Vorgang muss ausdrücklich verlangt, im Plan sichtbar und auf einen benannten Bereich begrenzt sein |
| Unbekannte Dateien | **niemals stillschweigend anpassen** — melden und blockieren; eine unbekannte Datei in einem geschützten Bereich ist ein Befund, kein Formatproblem |
| Falscher Besitzer oder Modus | **Befund**, nicht Nebenwirkung: erst melden, dann — getrennt und ausdrücklich — beheben |
| Nebenläufigkeit | **verboten**: kein Langläufer, kein Start-Hook, kein Nebenpfad repariert |

### 7 — Link- und Pfadsicherheit

| Gegenstand | Entscheidung |
| --- | --- |
| **Symlinks** | Ein Symlink, dessen Ziel den Bereich verlässt, ist **unzulässig** (M-4, I-5, **NT-05**). Innerhalb geschützter Bereiche wird ein Symlink **nicht** aufgelöst, sondern **abgelehnt** — bestehende Praxis aus ADR-0010/ADR-0011 |
| **Hardlinks** | In geschützten Bereichen **unzulässig** — ein Hardlink unterläuft die Bereichsgrenze, ohne als Link sichtbar zu sein |
| **Root-Boundary** | Jeder Bereich besitzt eine feste Wurzel. **Jeder** Pfad wird gegen sie geprüft; ein Ergebnis außerhalb der Wurzel wird abgelehnt — bestehende Praxis (`*_WRITE_OUTSIDE_ROOT`) |
| **Pfadauflösung** | Prüfung und Wirkung beziehen sich auf **denselben aufgelösten Pfad**; getrennt aufgelöste Pfade dürfen nicht gegeneinander geprüft werden |
| **TOCTOU** | **Ausdrücklich anerkannt und nicht wegdefiniert.** Eine Prüfung ist eine Aussage über einen Zeitpunkt. Deshalb ist die Rechteprüfung **nie die einzige** Absicherung: Mountmodus (KB-03), Prozessidentität (KB-01/KB-02) und atomare Schreibsemantik (I-6) tragen unabhängig. **Prüfergebnisse werden nicht über einen Schreibvorgang hinweg als weiterhin gültig behandelt** |
| **Mountgrenzen** | Ein Bereichswechsel über eine Mountgrenze hinweg ist **kein** zulässiger Pfad innerhalb eines Bereichs |
| **Unbekannte oder nicht zugeordnete Pfade** | **fail-closed** — ein Pfad ohne Bereichszuordnung ist verboten, nicht „neutral" (Permission Model: *bei unklarer Berechtigung gilt `forbidden`*) |

### 8 — Plattformgrenze

| Punkt | Entscheidung |
| --- | --- |
| Zielplattform | **Linux/POSIX**, **Profil A** — dedizierte VM, Container-Laufzeit gemäß Profil-A-Bundle |
| Hostdateisystem | Ort der Durchsetzung: Besitz und Modi entstehen **dort** |
| Containerdateisystem | Ort der **Validierung**; Wurzeldateisystem `read_only`, Schreibrecht ausschließlich über erklärte Bereiche |
| Grenze | Die Durchsetzung ist eine **Host-Zusage**. Die Bereitstellungseinheit **erbt** sie und **erzeugt** sie nicht |
| Nicht unterstützte Plattform | Die Durchsetzung ist **nicht verfügbar**. Ergebnis ist **nicht** „bestanden" und **nicht** „übersprungen", sondern **„nicht feststellbar"** — und das ist nach I-7 ein **fail-closed** Ergebnis für jede Readiness-Aussage |
| Entwicklungsumgebungen | Auf Nicht-POSIX-Plattformen sind **ausschließlich synthetische Formprüfungen** des Zielmodells möglich. **Eine synthetisch gültige Form ist keine Sicherheitswirkung** |

### 9 — Nachweisgrenze

| Nachweis | Wo prüfbar |
| --- | --- |
| Vollständigkeit und Widerspruchsfreiheit des Zielmodells | **synthetisch**, offline |
| Vollständigkeit der Bereichs-, Rollen- und Profilzuordnung | **synthetisch**, offline |
| Fail-closed-Verhalten bei fehlender, unbekannter oder kollidierender Bindung | **synthetisch**, offline |
| Ablehnung unbekannter Pfade, Symlink- und Hardlink-Fälle in der Prüflogik | **synthetisch**, offline |
| **NT-04 — Schreibversuch auf Canonical scheitert** | **nur real**, Nachweisstufe **4**, Profil-A-Instanz |
| **NT-05 — Symlink Escape blockiert** | **nur real**, Nachweisstufe **4**, Profil-A-Instanz |
| Rechteauflistung vor und nach dem Start | **nur real** |
| **SB-S04** wirksam | **nur real** |
| Readiness-Gate **3** und **5** | **nur real** — bleiben `NOT EVALUATED` |
| Mapping-Gate **7, 8, 11** | **nur real** — bleiben `NOT EVALUATED` |
| **OD-37** | **nur real** — bleibt **offen** |

**NT-04 und NT-05 sind nicht ausgeführt** (0 von 32 Negativtests, 0 von 1
Positivtest). **Dieser ADR führt keinen Test aus und wertet kein Gate aus.**

## Konsequenzen

### Positiv

| # | Konsequenz |
| --- | --- |
| 1 | Die Runtime benötigt **keinerlei** Rechteprivilegien — vereinbar mit **V-1**, **V-3**, `cap_drop: ALL`, `no-new-privileges` und `read_only`, ohne eine dieser Zusagen aufzuweichen |
| 2 | **Keine realen Werte im Repository.** Die Publikationsfähigkeit des Cores bleibt unberührt; §469 und die Runbook-Regel „niemals zurück ins Repository" werden eingehalten |
| 3 | Eine Rechteabweichung wird **sichtbar**, statt von einer Selbstheilung überdeckt zu werden — **NT-04** und **NT-05** bleiben aussagekräftig |
| 4 | Die konkreten Werte bleiben **außerhalb** und damit **neu bindbar**, ohne Repository- oder Architekturänderung |
| 5 | Die Verantwortlichkeiten sind **disjunkt**: wer setzt, prüft nicht; wer prüft, setzt nicht |
| 6 | Die bestehende atomare Schreibsemantik bleibt **unverändert gültig**; kein implementierter Code wird durch diese Entscheidung in Frage gestellt |
| 7 | **OD-37** ist erstmals **strukturiert**: es ist klar, welcher Anteil dokumentarisch und welcher deploymentseitig zu schließen ist |
| 8 | Der Nachweis entspricht **wörtlich** der Vorgabe „Rechteauflistung vor und nach dem Start" |

### Negativ

| # | Konsequenz |
| --- | --- |
| 1 | **Die Sicherheit hängt an einem Vorgang außerhalb dieses Repositorys.** Ein nachlässiges Deployment kann die Zusage unterlaufen; dagegen wirkt nur die Startprüfung |
| 2 | Ein falsch vorbereiteter Bereich führt zu **Startverweigerung statt Selbstheilung** — betrieblich unbequem, sicherheitsseitig gewollt |
| 3 | Bestandsdaten mit falschen Rechten benötigen einen **ausdrücklichen, manuell ausgelösten** Migrationsweg |
| 4 | Der Reparaturweg ist **an RT-2 gebunden** und deshalb bis auf Weiteres **nicht freigegeben** |
| 5 | Ein Teil der Sicherheitszusage ist **nur real prüfbar** — Nachweisstufe 4 bleibt bis zu einer Profil-A-Instanz unerreichbar |
| 6 | **Zwei Wahrheitsorte** — Zielmodell hier, Werte dort — erfordern eine dauerhaft gepflegte, geprüfte Bindung |
| 7 | Auf Nicht-POSIX-Plattformen ist **keine** Durchsetzungsaussage möglich |

## Risiken und Gegenmaßnahmen

**Keine neue Risiko-ID.** Die folgenden Risiken sind Eigenschaften der
Entscheidung und werden hier benannt, nicht registriert.

| Risiko | Wirkung | Gegenmaßnahme in dieser Architektur |
| --- | --- | --- |
| Deployment setzt Rechte falsch oder gar nicht | Kontrollkette ab Stufe 1 unwirksam | **Startprüfung verweigert den Start**; Nachweis vor und nach dem Start |
| Host- und Containeridentität laufen auseinander | Rechte greifen ins Leere | **explizite Bindung**, Startprüfung gegen die **effektive** Identität, fail-closed |
| Betriebsdruck erzeugt einen „Warnmodus" | stille Abschwächung, I-7 verletzt | **Architektonisch ausgeschlossen** — kein Umgehungsschalter vorgesehen |
| Reparatur wird als Bequemlichkeit in die Runtime gezogen | Option C durch die Hintertür | **Kategorisches Verbot** für Langläufer, unabhängig von verfügbaren Privilegien |
| Rechteprüfung wird als vollständige Absicherung missverstanden | TOCTOU-Fehlschluss | Prüfung **ausdrücklich** als Zeitpunktaussage deklariert; Mount-, Identitäts- und Schreibkontrollen tragen unabhängig |
| Zielmodell und reale Bindung driften auseinander | Prüfung wird zur Formalie | Bindung ist **Pflichtwert ohne Default**; Installationsprüfung erzwingt Vollständigkeit |
| Der ADR wird als Fortschritt der Control gelesen | falsche Reifeaussage | **KB-04 bleibt `DOCUMENTED ONLY`**; ausdrücklich im Statusspiegel und in D-059 |

## Verworfene Optionen

**Option C — Runtime Self-Repair: verworfen, und zwar nicht als schwächere
Wahl, sondern als repository-widersprüchlich.** Sie verlangt Privilegien, die
**V-1** und **V-3** verbieten und die das bereits committete Profil-A-Bundle mit
`cap_drop: ALL` und `no-new-privileges` entzieht. Sie verletzt **I-7**, weil sie
eine Abweichung **behebt statt abzulehnen**, und sie entwertet **NT-04** und
**NT-05**, deren Aussagekraft davon abhängt, dass ein falscher Zustand
**bestehen bleibt und auffällt**.

**Option D — ACL-centric Enforcement: verworfen als Hauptmechanismus.** Sie
setzt Werkzeuge, Dateisystemoptionen und Plattformzusagen voraus, die das
Projekt nicht führt und die seiner stdlib-only-Praxis widersprechen. Die
Spezifikation formuliert die Anforderung in **Owner-, Gruppen- und
world-writable-Begriffen**, also im klassischen Modusmodell. Eine ACL-Ebene darf
später **zusätzlich** gehärtet werden; sie darf das Grundmodell **nie ersetzen**
— analog zur Regel aus §11, dass eine spätere Stufe eine frühere technische
Kontrolle nicht ersetzt.

**Option E — Zielmodell ohne Runtime-Validierung: verworfen.** Ohne Prüfung
gibt es keinen Nachweis, keine Fail-closed-Wirkung und keinen Unterschied zum
heutigen Zustand `DOCUMENTED ONLY`. Die Option beschreibt den Ausgangspunkt,
nicht ein Ziel.

**Option B — Privileged Bootstrap: nicht verworfen, sondern verortet.** Ihre
Initialisierungsverantwortung ist Teil der gewählten Architektur; sie liegt
**auf der Deployment-Seite der Grenze**. Als **privilegierte Komponente
innerhalb** der Bereitstellungseinheit wird sie verworfen, weil das Bundle genau
zwei Service-Identitäten kennt, `privileged` ausschließt und die
Privilegientrennung sonst nur verschöbe statt sie herzustellen.

## Offene Implementierungsparameter

Ausdrücklich **nicht** in diesem ADR entschieden und in **B1C** zu binden:

| # | Parameter |
| --- | --- |
| 1 | vollständige **Pfad-zu-Rolle-zu-Modus-Matrix** über alle geschützten Bereiche |
| 2 | exakte **symbolische oder numerische Modusprofile** je Klasse PP-1 bis PP-4 |
| 3 | konkreter **`umask`**-Wert |
| 4 | Zuordnung der acht Bereiche des Profil-A-Bundles zu den Profilklassen |
| 5 | **Konfigurationsschema** der Identitätsbindung |
| 6 | Vertrag der **Identitätsvalidierung** |
| 7 | **Initialisierungs- und Validierungsvertrag** |
| 8 | **Migrations- und Reparaturvertrag** |
| 9 | **Fehlerklassen** |
| 10 | Bedarf an **Issue- und Exitcodes** — in diesem ADR **bewusst keine festgelegt** |
| 11 | **Testmatrix** und die Abbildung auf **NT-04** und **NT-05** |
| 12 | Abgrenzung synthetischer gegen reale Nachweise |
| 13 | **Implementierungs- und Dateiscope für B2** |
| 14 | reale UID-, GID-, Benutzer- und Gruppenwerte — **Deployment Required**, **niemals im Repository** |

## Nachfolgende Contract-Finalisierung

**B1C — Enforcement Contract and Validation Plan.** **Nicht autorisiert.**

B1C konkretisiert die vierzehn offenen Parameter zu einem prüfbaren Vertrag und
legt den Datei- und Implementierungsscope für B2 fest. **B2 bleibt gesperrt.**
Ohne B1C ist keine technische Implementierung zulässig.

## Non-Goals

Dieser ADR entscheidet **nicht**: Application-Level-Autorisierung (KB-05) ·
Approval-Zustände (KB-06) · Git- und GitHub-Rechte (KB-07) · Secret-Verwaltung
(KB-08) · Audit- und RT-2-Implementierung (KB-09) · Netzgrenzen (KB-10) ·
Leakschutz (KB-11) · Backup-Isolation (KB-12) · **KB-01/KB-02-Implementierung** ·
**KB-03-Implementierung** · **KB-04 Stage 2** · Verschlüsselung ruhender Daten ·
Mandantentrennung · Rechteverwaltung für menschliche Benutzer · Kubernetes,
Orchestrierung oder ein zweites Deploymentprofil.

## Do-not-start-Grenzen

**Dieser ADR autorisiert keine Implementierung.** Nicht autorisiert sind:
Runtime-Code · neue Python-Dateien · Tests oder Testausführung · Änderungen an
Bundle oder Validator · Containerstart · Deployment · Setzen realer Rechte oder
Besitzverhältnisse · Festlegen realer UIDs, GIDs, Benutzer, Gruppen oder
Hostpfade · Control-Hochstufung · Gateauswertung oder -freigabe ·
Capability-Änderung · neue Risiko-ID · Schließung von **OD-37** · **B1C** ·
**B2** · **KB-04 Stage 2** · **CBP-WP-023** · Commit, Push, Tag oder Release.

## Reversibilität

| Ebene | Bewertung |
| --- | --- |
| **Architekturentscheidung** | **mittel** — die Verortung der Authority ist eine Grundsatzwahl; eine spätere Umkehr zu Option C wäre durch **V-1**, **V-3** und das Bundle ohnehin gesperrt |
| **Konkrete Werte** | **hoch** — sie liegen im Deployment und sind ohne Repository- oder Architekturänderung neu bindbar |
| **Persistente Wirkung auf Bestände** | **gering** — einmal gesetzte Besitz- und Modusverhältnisse über Canonical, Quarantine, Registry und Freigabebereich erfordern einen ausdrücklichen Migrationsweg |

Die gewählte Architektur **verbessert** die Reversibilität gegenüber C und D,
weil sie die schwer umkehrbaren Werte aus dem Repository heraushält. Der
schwer reversible Anteil bleibt bestehen — er ist der Grund, warum D-058
`ADR_REQUIRED` festgestellt hat.

## Security Impact

**Hoch.** KB-04 ist die unterste tragende Ebene; versagt sie, sind KB-05 bis
KB-07 wirkungslos. Diese Architektur entzieht der Runtime jede Möglichkeit,
eine Rechteabweichung zu verdecken, und macht die Startverweigerung zur
Regelantwort. **Sie erhöht die Sicherheitsreife jedoch nicht**: es ist kein
Recht gesetzt, kein Test gelaufen und kein Nachweis erbracht.

**KB-04 bleibt `DOCUMENTED ONLY`.** Alle zwölf Controls bleiben
`DOCUMENTED ONLY`. Beide Runtime-Gates bleiben `NOT EVALUATED`. Capabilities
**0 von 29**. **NT-04 und NT-05 nicht ausgeführt.** **SB-S04 ist nicht
wirksam.**

## Deployment Impact

| Gegenstand | Wirkung |
| --- | --- |
| **OD-37** | **bleibt offen** — strukturiert, nicht geschlossen |
| Profil-A-Bundle | **unverändert**; die Entscheidung ist mit `read_only`, `cap_drop: ALL`, `no-new-privileges` und dem Muster `${...:?...}` vereinbar |
| Installation Runbook | die spätere Konkretisierung ergänzt einen Vorbereitungsschritt **vor** dem Start — **in diesem Lauf nicht geschrieben** |
| Operator-Workspace | Ort der realen Werte (W-3, ADR-0007) — **nicht angelegt** |
| DRC | **unverändert**; keine neue Zusage, kein neuer Prüfpunkt |
| Reale Bereitstellung | **keine** |
| RT-2 | **nicht implementiert**; blockiert bis auf Weiteres den Reparaturweg |

## Acceptance Criteria

Eine spätere Umsetzung gilt nur dann als konform zu diesem ADR, wenn:

| # | Kriterium |
| --- | --- |
| 1 | **keine** Runtime-Komponente Besitz, Gruppe oder Modus verändert |
| 2 | die Runtime ohne Rechteprivilegien auskommt und **V-1**, **V-3**, `cap_drop: ALL` und `no-new-privileges` unangetastet lässt |
| 3 | fehlende, unbekannte oder kollidierende Identitätsbindung **fail-closed** endet |
| 4 | die Host-/Container-Abbildung **explizit erklärt** und beim Start gegen die **effektive** Identität geprüft wird |
| 5 | **keine** realen UID-, GID-, Benutzer-, Gruppen- oder Hostpfadwerte im Repository stehen |
| 6 | **kein** unsicherer Default und **kein** Fallback existiert; ein fehlender Pflichtwert blockiert |
| 7 | geschützte Artefakte **niemals** world-writable sind |
| 8 | Retrieval **keinen** Schreibzugriff auf Canonical besitzt |
| 9 | Ingest **keinen** unkontrollierten Schreibzugriff auf Canonical besitzt |
| 10 | Symlink-Escapes und Hardlinks in geschützten Bereichen abgelehnt werden |
| 11 | die atomare Schreibsemantik aus ADR-0010/ADR-0011 **unverändert** gilt |
| 12 | Initialisierung, Validierung, Migration und Reparatur **getrennte** Verantwortlichkeiten sind |
| 13 | Reparatur **niemals** still, nebenläufig oder durch einen Langläufer erfolgt |
| 14 | Bestandsdaten **nicht** ohne ausdrücklichen Modus, Plan und Auditspur rekursiv verändert werden |
| 15 | ein nicht nachweisbar sicherer Zustand **Start oder Freigabe blockiert** |
| 16 | **kein** Control- und **kein** Gatestatus durch die Umsetzung hochgestuft wird, solange die realen Nachweise fehlen |

## Autoritätsgrenzen

Dieser ADR autorisiert **keine** technische Implementierung. Er autorisiert
**nicht**: reale Quelle, Ziel-VM, Netzwerk, Secrets, Credentials, RT-2,
Persistenz, Enforcement, Security Readiness, Gate-Pass, Human Approval,
Aktivierung, Bereitstellung oder Rechtevergabe.

**Eine entschiedene Architektur ist keine Sicherheitswirkung.**

## Bezug

- **ADR-0009** (A1) — Technische Sicherheitsgrundlage: KB-01 bis KB-12,
  Readiness-Gate. **Wird konkretisiert, nicht abgelöst.**
- **ADR-0010**, **ADR-0011** (A1) — atomare Schreibsemantik; **unverändert
  übernommen** (I-6).
- **ADR-0007** (A1) — Repository- und Workspace-Grenze; RT-1/RT-2/RT-3;
  Bereichsmodell W-3 für den Operator-Workspace.
- **ADR-0002** (A1) — Referenzprofil und Pilotlaufzeit: Profil A.
- **D-034** (A0) — zwei getrennte logische Service-Identitäten.
- **D-057** (A0) — Registrierung von CBP-WP-022.
- **D-058** (A0) — ADR-Gate, Ergebnis **`ADR_REQUIRED`**.
- **D-059** (A0) — Annahme dieses ADR.
- **CBP-WP-011** — Ursprung der Sicherheitsgrundlage: Spezifikation, Acceptance
  Matrix, Identity Model und Readiness-Gate wurden dort erfasst.
- **CBP-WP-022** — Phase B1A Contract Boundary, Fundstellentabelle,
  Invarianten I-1 bis I-7.
- **NT-04**, **NT-05**, **SB-S04**, Readiness-Gate 3 und 5, Mapping-Gate 7, 8
  und 11 — **sämtlich nicht ausgeführt beziehungsweise `NOT EVALUATED`**.
- **OD-37** — **bleibt offen**.
