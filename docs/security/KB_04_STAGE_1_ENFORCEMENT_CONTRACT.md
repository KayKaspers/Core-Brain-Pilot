# KB-04 Stage 1 Enforcement Contract and Validation Plan

| Feld | Wert |
| --- | --- |
| **Status** | **accepted contract** |
| Datum | **2026-08-03** |
| Authority | **D-060** (A0) · **ADR-0014** (A1) · **CBP-WP-022**, Phase B1C |
| Autoritätsklasse dieses Dokuments | **A2** — formeller Projektstand innerhalb ADR-0014 |
| Gegenstand | **KB-04 — Dateisystemrechte**, Durchsetzungsstufe **1** |
| Deploymentprofil | **Profil A** |
| Plattform | **Linux/POSIX** |

> **Dieser Vertrag ist implementierungsfähig, aber keine Implementierung.**
> **KB-04 bleibt `DOCUMENTED ONLY`.** Es ist kein Recht gesetzt, kein Besitz
> zugewiesen, kein Test ausgeführt und kein Gate ausgewertet. **B2 ist nicht
> autorisiert.**

---

## 1 — Authority Chain

| Quelle | Klasse | Beitrag zu diesem Vertrag |
| --- | :---: | --- |
| **ADR-0014** | **A1** | **Bindende Architektur.** Host-authoritative Enforcement, deklaratives Zielmodell, read-only Runtime-Validierung; Invarianten I-1 bis I-7; Profile PP-1 bis PP-4; vierzehn offene Parameter, die dieser Vertrag bindet |
| **ADR-0009** | **A1** | Technische Sicherheitsgrundlage; KB-01 bis KB-12; Readiness-Gate |
| **ADR-0010**, **ADR-0011** | **A1** | Atomare Schreibsemantik und Storelayout — **unverändert übernommen, nicht neu entschieden** |
| **ADR-0013** | **A1** | Evidence-Schema 3.0, `security-control-form`, `control_id` — Form der späteren Nachweise |
| **D-057** | A0 | Registrierung CBP-WP-022 |
| **D-058** | A0 | ADR-Gate, **`ADR_REQUIRED`** |
| **D-059** | A0 | Annahme von ADR-0014 |
| **D-060** | **A0** | **Annahme dieses Vertrags**, `ADR_NOT_REQUIRED` innerhalb ADR-0014 |
| Spezifikation §KB-04, §11, §469 | A2 | Anforderung, Stufe 1, **Dateimodi/Owner/Gruppen = Deployment Required** |
| Acceptance Matrix §KB-04 | A2 | **NT-04**, **NT-05**, Nachweisstufe **4**, **SB-S04**, Status `DOCUMENTED ONLY` |
| Identity Model | A2 | Zwei logische Identitäten; **V-1**, **V-3**, **V-5**, **V-11**, **V-12**; **M-1** bis **M-4**; Mount-Matrix; *Offene Deploymentwerte* |
| Permission Model | A2 | OS-Dateirechte als eigene Ebene; *bei unklarer Berechtigung gilt `forbidden`* |
| Profil-A-Bundle | A2 | Acht Datenbereiche mit abstrakten Ownerrollen · `container_paths` · `tmpfs_targets` · Config-Bindmount **`mode: 292` = `0444`** · `read_only`, `cap_drop: ALL`, `no-new-privileges` · `KB-04 → filesystem-permission-target-model` |
| Installation Runbook | A2 | Pflichtwerte einschließlich UID und GID **im lokalen Operator-Workspace**, **niemals zurück ins Repository** |
| Validation Runbook | A2 | Offline-Validator **vor** jeder Compose-Auswertung; Exitcodes gelten **nur** für das Offline-Werkzeug |
| Rollback Runbook | A2 | Zielstand muss den Offline-Validator mit Exitcode 0 bestehen |
| Readiness Gate | A2 | Punkt **3** (OS-Rechte, Stufe 2) · Punkt **5** (Canonical read-only, **NT-04**, Stufe 4) |
| Mapping Activation Gate | A2 | Punkte **7**, **8**, **11** |
| **OD-37** | offen | Produktive Isolation auf der Ziel-VM (KB-03, KB-04) — **Deployment Required** |
| **RT-2** / Operational Evidence Policy | A2 | RET-1 Aufbewahrung verpflichtend; **RT-2 nicht implementiert** |
| **CBP-WP-011** | — | Ursprung von Spezifikation, Acceptance Matrix, Identity Model und Readiness-Gate |
| **CBP-WP-022** | — | Contract Boundary B1A, Architektur B1B, dieser Vertrag B1C |

**Konflikte: keine.** Jede Festlegung dieses Vertrags liegt vollständig
innerhalb ADR-0014.

## 2 — Scope

**KB-04 Enforcement Stage 1** — Besitz, Gruppe und Modus der geschützten
Dateisystembereiche, ihre Initialisierung durch das Deployment und ihre
**read-only** Validierung durch die Runtime.

| Gegenstand | Festlegung |
| --- | --- |
| Deploymentprofil | **Profil A** |
| Plattform | **Linux/POSIX** |
| Authority | **Host-Dateisystem** — das Deployment stellt Besitz und Rechte **vor** dem Start her |
| Runtimeidentitäten | **gebundene** Containeridentitäten, beim Start gegen die Bindung geprüft |
| Repositoryanteil | **abstraktes Zielmodell** — Pfadklassen, Rollen, Profile, Prüfregeln |
| Runtimeanteil | **read-only Validierung** mit fail-closed Ablehnung |

## 3 — Non-Goals

Dieser Vertrag enthält und autorisiert **nicht**: technische Implementierung ·
Runtime-Code · reale UID- oder GID-Werte · reale Benutzer- oder Gruppennamen ·
reale Hostpfade · Runtime-Reparatur · automatisches `chown` oder `chmod` durch
Langläufer · Gateauswertung · Control-Hochstufung · reale Testausführung ·
KB-04 **Stage 2** · KB-01-, KB-02- oder KB-03-Implementierung · KB-05 bis
KB-12 · **RT-2-Implementierung** · ein zweites Deploymentprofil · ein
Nicht-POSIX-Backend.

---

## 4 — Pfadklassifikation

Alle Kennungen sind **abstrakt**. Die Containerpfade stammen unverändert aus
`container_paths` und `tmpfs_targets` des bereits committeten
Profil-A-Bundles; **es wird kein Rootpfad erfunden und kein Hostpfad genannt**.

| Kennung | Bereich | Containeranker | Objektarten | Owner-Rollentyp | Lesegruppe | Schreibrollen | **PP** | Mountmodus | Runtime-Erwartung |
| --- | --- | --- | --- | --- | --- | --- | :---: | --- | --- |
| **PC-01** | Canonical Store | `/var/lib/cbp/canonical` | Verzeichnis, reguläre Datei | **maintainer-owned** (außerhalb der Service-Identitäten) | gemeinsame Lesegruppe beider Dienste | **keine** | **PP-3a** | **ro** beidseitig | lesen, **niemals** schreiben |
| **PC-02** | Quarantine Store | `/var/lib/cbp/quarantine` | Verzeichnis, reguläre Datei | `data-worker` | — | `data-worker` | **PP-1** | **rw** nur Data Worker | schreiben nach Storelayout ADR-0010 |
| **PC-03** | Source Registry | `/var/lib/cbp/source-registry` | Verzeichnis, reguläre Datei | `control-plane` | Lesegruppe Data Worker | `control-plane` | **PP-2** | **rw** CP · **ro** DW | Layout ADR-0011 |
| **PC-04** | Mapping Registry | `/var/lib/cbp/mapping-registry` | Verzeichnis, reguläre Datei | `control-plane` | Lesegruppe Data Worker | `control-plane` | **PP-2** | **rw** CP · **ro** DW | Mappingartefakte |
| **PC-05** | Released Artifacts | `/var/lib/cbp/released` | Verzeichnis, reguläre Datei | `control-plane` | — | `control-plane` | **PP-1** | **rw** nur CP | Freigabebereich |
| **PC-06** | Derived Indices | `/var/lib/cbp/derived` | Verzeichnis, reguläre Datei | `data-worker` | — | `data-worker` | **PP-1** | **rw** nur DW | RT-1, reproduzierbar |
| **PC-07** | Konfigurationsartefakte — **ausschließlich nicht geheime, unveränderlich eingebundene Runtime-Konfiguration** | `/etc/cbp` | Verzeichnis, reguläre Datei | **deployment-owned** | beide Dienste | **keine** | **PP-3b** | **ro** beidseitig | **nur lesen**, keine Schreibfähigkeit; Dateimodus **bundle-fixiert `0444`**; **Secrets und sensible Werte unzulässig** (§6.1) |
| **PC-08** | Transiente Laufzeitbereiche | `/run/cbp`, `/tmp` | Verzeichnis, reguläre Datei | `service` | — | beide Dienste, getrennt | **PP-1** | **tmpfs**, rw | RT-3, flüchtig, nie Statuswahrheit |
| **PC-09** | RT-2 Operational Evidence | — **nicht eingebunden** | — | `human-maintainer` | — | — | **PP-4** | **not mounted** | **nicht erreichbar** (M-2) |
| **PC-10** | Backup Storage | — **nicht eingebunden** | — | außerhalb | — | — | **PP-4** | **not mounted** | **nicht erreichbar** (V-11) |
| **PC-11** | **Unbekannt / nicht zugeordnet** | jeder nicht klassifizierte Pfad | — | — | — | — | — | — | **fail-closed** |

**Artefaktarten innerhalb der Klassen** — abgeleitet aus den bereits
dokumentierten Storelayouts, **keine neuen Roots**:

| Art | Vorkommen | Regel |
| --- | --- | --- |
| **Objekt/Blob** | `objects/sha256/<prefix>/<digest>.blob` (PC-02) | unveränderlich; Pfad **nur** aus validiertem Digest |
| **Record** | `records/<id>.json` (PC-02, PC-03) | unveränderlich; wird nie überschrieben |
| **Event** | `events/<id>/<event-id>.json` (PC-03) | append-only |
| **Katalog/abgeleitet** | `catalog/catalog.json` (PC-03) | atomar ersetzt |
| **Metadaten** | Manifeste und Kataloge in PC-02 bis PC-05 | Profil der **umgebenden** Pfadklasse; **kein** eigenes Profil |
| **Temporäres Schreibartefakt** | innerhalb derselben Pfadklasse | gleiche Klasse, **gleichwertiger Sicherheitskontext**, nie außerhalb der Root |
| **Status-/Lock-Artefakt** | PC-08 | **RT-3**; nie alleinige Statuswahrheit |
| **Evidenzartefakt** | RT-1-Anteil in PC-06 · **RT-2 in PC-09 nicht erreichbar** | RT-1 synthetisch; RT-2 ausschließlich über die Evidence-Schnittstelle |

**Symlink- und Hardlinkregel für alle Klassen:** bereichsverlassende Symlinks
**unzulässig**; Hardlinks in geschützten Bereichen **unzulässig**; siehe §11.

**Migrations- und Reparaturstatus:** PC-01 bis PC-08 **plan-only**; PC-09 und
PC-10 **nicht anwendbar** (nicht eingebunden); PC-11 **keine Migration** —
unbekannte Pfade werden gemeldet und blockieren, sie werden nicht eingeordnet.

---

## 5 — Akteurs- und Rollenmatrix

`E` entdecken · `R` lesen · `W` schreiben · `C` erstellen · `X` ersetzen ·
`D` löschen · `O` Owner/Gruppe ändern · `M` Modus ändern · `B` Bindung ändern ·
`V` validieren · `P` reparieren · `G` Gate-Evidenz erzeugen.

| Akteur | E | R | W | C | X | D | **O** | **M** | **B** | V | **P** | G |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **deployment/setup** (host-seitig, operatorgeführt) | ✔ | ✔ | ✔¹ | ✔¹ | ✔¹ | ✖ | **✔** | **✔** | **✔** | ✔ | **plan-only** | ✖ |
| **operator** (Mensch) | ✔ | ✔ | ✖ | ✖ | ✖ | ✖ | ✖ | ✖ | ✖ | ✔ | **anordnen, nicht ausführen** | ✖ |
| **ingest** | ✔ | ✔ | PC-02 | PC-02 | PC-02 | ✖ | **✖** | **✖** | **✖** | ✔ | **✖** | ✖ |
| **retrieval** | ✔ | ✔ | **✖ auf PC-01** | ✖ | ✖ | ✖ | **✖** | **✖** | **✖** | ✔ | **✖** | ✖ |
| **registry** | ✔ | ✔ | PC-03 | PC-03 | PC-03 | ✖ | **✖** | **✖** | **✖** | ✔ | **✖** | ✖ |
| **mapping** | ✔ | ✔ | PC-04 | PC-04 | PC-04 | ✖ | **✖** | **✖** | **✖** | ✔ | **✖** | ✖ |
| **release** | ✔ | ✔ | PC-05 | PC-05 | PC-05 | ✖ | **✖** | **✖** | **✖** | ✔ | **✖** | ✖ |
| **validation** | ✔ | ✔ | **✖** | ✖ | ✖ | ✖ | **✖** | **✖** | **✖** | ✔ | **✖** | ✔ |
| **gate** | ✔ | ✔ | **✖** | ✖ | ✖ | ✖ | **✖** | **✖** | **✖** | ✔ | **✖** | ✔ |
| **evidence** | ✔ | ✔ | **RT-1 nur** | RT-1 | RT-1 | ✖ | **✖** | **✖** | **✖** | ✔ | **✖** | ✔ |

¹ **ausschließlich** auf einer nachweislich neuen, leeren Zielstruktur (§9.1).

**Verbindliche Verbote:**

| # | Regel | Beleg |
| --- | --- | --- |
| 1 | **Nur der Setup-/Deployment-Akteur** setzt initial Besitz und Rechte | ADR-0014 |
| 2 | **Keine normale Runtime-Komponente** verändert jemals Besitz, Gruppe, Modus oder Bindung | ADR-0014, kategorisch |
| 3 | **Retrieval schreibt Canonical nicht** | I-3, V-5, Mount-Matrix |
| 4 | **Ingest schreibt Canonical nicht unkontrolliert** | I-4, V-5 |
| 5 | **Validation ist strikt read-only** | ADR-0014 |
| 6 | **Gate-Evidenz ist keine Reparaturbefugnis** | ADR-0013, ADR-0014 |
| 7 | **Operatorbefugnis ersetzt keine implementierte RT-2-Autorität** | RET-1; RT-2 nicht implementiert |
| 8 | **Keine Identität beschreibt PC-09 oder PC-10** | M-2, V-9, V-11 |

---

## 6 — Rechteprofile PP-1 bis PP-4

Gemeinsame, **nicht konfigurierbare** Regeln aller Profile:

| # | Regel |
| --- | --- |
| G-1 | **Kein World-Schreibbit — ausnahmslos** (I-2) |
| G-2 | **Kein World-Lesebit**, außer eine Profilvariante fixiert es ausdrücklich (nur **PP-3b**) |
| G-3 | **Kein setuid auf Dateien, kein setgid auf Dateien** |
| G-4 | **Kein Execute-Bit auf Datenartefakten** — Execute ausschließlich zur Verzeichnisdurchquerung |
| G-5 | **Keine ACLs als Ersatz** — ACLs sind kein Bestandteil dieses Vertrags; eine vorgefundene ACL, die die Profilaussage erweitert, ist eine **Vertragsverletzung** |
| G-6 | **Unbekannte Zusatzbits** (setuid, setgid außerhalb der Ausnahme, sticky außerhalb PC-08) → `KB04-MODE-SPECIAL-BITS`, fail-closed |
| G-7 | **Konformität bei der Erstellung**, nicht nachträglich — die `umask` muss das Profil unmittelbar erzeugen |
| G-8 | **Konfigurierbar sind ausschließlich die Bindungswerte** (§8). Modi, Profile und Zuordnungen sind **nicht** konfigurierbar; es gibt **keinen** unsicheren Default und **keinen** Fallback |

| Profil | Zweck | Owner | Gruppe | **Datei** | **Verzeichnis** | **umask** | setgid | sticky | world |
| --- | --- | --- | --- | :---: | :---: | :---: | --- | --- | --- |
| **PP-1** | owner-write — rollenexklusiv | Rollenidentität | Rollengruppe, **ohne** Rechte | **`0600`** | **`0700`** | **`0077`** | **verboten** | verboten | **keine Bits** |
| **PP-2** | owner-write mit kontrolliertem group-read | schreibende Rolle | **kontrollierte Lesegruppe** | **`0640`** | **`0750`** | **`0027`** | **`2750`** zulässig, **nur** wo Gruppenvererbung nötig ist | verboten | **keine Bits** |
| **PP-3a** | service-read-only, gruppenbeschränkt | **außerhalb** der Service-Identitäten | gemeinsame Lesegruppe | **`0640`** | **`0750`** | **`0027`** | **verboten** | verboten | **keine Bits** |
| **PP-3b** | service-read-only, **deployment-fixiertes Kompatibilitätsprofil** — **nur PC-07** | deployment-owned | — | **`0444`** | **`0555`** | n. a. — vom Deployment gesetzt | **verboten** | verboten | **World-Read ausnahmsweise fixiert** (§6.1), **World-Write verboten** |
| **PP-4** | not-present | — | — | **kein Modus** | **kein Modus** | n. a. | n. a. | n. a. | **Pfad darf nicht existieren und nicht eingebunden sein** |

**PP-3 besitzt genau zwei Varianten und keine weiteren.**

### 6.1 — PP-3b: eng begrenztes Kompatibilitätsprofil

**PP-3b ist kein allgemeines read-only Profil.** Es ist ein **eng begrenztes
Kompatibilitätsprofil**, das ausschließlich existiert, weil das **bereits
committete** Profil-A-Bundle den Config-Bindmount mit `mode: 292`, also
**`0444`**, führt (D-055). Dieser Vertrag **ändert das Bundle nicht** und
**schreibt keinen abweichenden Wert vor** — er **übernimmt** den Wert als
vorgefundene, bundle-autoritative Zusage und **validiert** ihn.

#### Exklusiver Scope

| # | Regel |
| --- | --- |
| **3b-1** | PP-3b gilt **ausschließlich für PC-07 — Konfigurationsartefakte**. |
| **3b-2** | Es gilt **nur** für Artefakte, die **unveränderlich** in die Runtime eingebunden werden, von der Runtime **ausschließlich gelesen** werden, **keine geheimen oder sensiblen Werte** enthalten und **bereits durch den committeten Bundlevertrag** als entsprechende Runtime-Konfiguration vorgesehen sind. |
| **3b-3** | **PP-3b darf auf keine andere Pfadklasse übertragen werden.** Eine Verwendung außerhalb PC-07 ist eine Vertragsverletzung (`KB04-CONTRACT-INVALID`). |
| **3b-4** | **PP-3b darf nicht als allgemeines read-only Profil verwendet werden.** Für service-read-only Datenbereiche gilt **PP-3a**. |
| **3b-5** | Erfüllt ein Artefakt **eine** der Bedingungen aus 3b-2 nicht, ist es **nicht** PP-3b. |

#### Verbotene Inhalte

Unter PP-3b sind **ausdrücklich unzulässig**: Secrets · Tokens ·
Passwörter · private Schlüssel · Recovery- oder Zugriffsschlüssel ·
Credential-Werte · konkrete lokale UID- oder GID-Werte · konkrete lokale
Benutzer- oder Gruppennamen · vollständige lokale Identitätsbindungen ·
sensible Operatorwerte · sensible Deploymentparameter · private Hostpfade ·
**jede weitere Information, deren Offenlegung gegenüber einer beliebigen
lokalen Runtimeidentität eine Sicherheitsgrenze verletzt**.

> Die vorstehenden Begriffe bezeichnen **verbotene Inhaltsklassen**. **Es wird
> kein Wert genannt.**

| # | Regel |
| --- | --- |
| **3b-6** | Ein Artefakt mit einem solchen Inhalt **darf nicht als PP-3b klassifiziert werden**. |
| **3b-7** | Es **darf nicht still in PC-07 übernommen** werden. |
| **3b-8** | Fehlt eine sichere Alternativklassifikation, ist das Ergebnis **fail-closed** — `KB04-CONTRACT-INVALID`; ist die Inhaltsklasse **nicht feststellbar**, gilt `KB04-STATE-INDETERMINATE`. |
| **3b-9** | Dieser Vertrag definiert **keine Secret-Management-Architektur**. Er hält ausschließlich die **Unzulässigkeit unter PP-3b** fest; die Secret-Bereitstellung bleibt **KB-08** und dem bestehenden Referenzvertrag vorbehalten. |

#### World-Read-Ausnahme

| # | Regel |
| --- | --- |
| **3b-10** | **`0444`/`0555` ist kein allgemeiner sicherer Default.** |
| **3b-11** | **Der Grundzustand bleibt: kein World-Zugriff** (I-1, Regel G-2). |
| **3b-12** | PP-3b ist eine **explizite, auf PC-07 begrenzte Ausnahme**. |
| **3b-13** | Die Ausnahme beruht **ausschließlich** auf dem bereits committeten Bundlevertrag — auf keiner Sicherheitsüberlegung dieses Vertrags. |
| **3b-14** | Sie darf **keine andere Profilklasse und keine Sicherheitsinvariante abschwächen**. |
| **3b-15** | **`world-writable` bleibt ausnahmslos verboten** (I-2). |
| **3b-16** | Eine **zukünftige Verschärfung von PC-07** bleibt zulässig und ist **kein Vertragsbruch**, sofern sie die erforderliche Runtime-Lesbarkeit erhält. Sie wäre eine **Bundle- und damit Deployment-Entscheidung** in einem ausdrücklich autorisierten technischen Scope — **hier nicht getroffen**. |

**In diesem Lauf wird keine Bundle-Datei geändert.**

**Fail-closed-Bedingungen aller Profile:** abweichender Owner · abweichende
Gruppe · abweichender Modus · jedes World-Schreibbit · nicht ausdrücklich
erlaubtes World-Lesebit · verbotene Zusatzbits · Execute auf Datenartefakten ·
erweiternde ACL · nicht feststellbarer Modus · Existenz eines PP-4-Pfades.

---

## 7 — Mount- und POSIX-Rechte getrennt

| # | Regel |
| --- | --- |
| MT-1 | **POSIX-Rechte ersetzen keinen Mountmodus.** |
| MT-2 | **Ein Mountmodus ersetzt keine POSIX-Rechte.** |
| MT-3 | **Runtime-Schreibzugriff verlangt alle vier Bedingungen gleichzeitig:** passender Mountmodus · passende Rolle · passendes PP-Profil · **positive** Identitätsbindung. Fehlt eine, ist der Zugriff verboten. |
| MT-4 | **Read-only ist doppelt durchzusetzen** — am Mount **und** am Rechteprofil; die Validierung prüft beide getrennt. |
| MT-5 | **Eine Gruppenmitgliedschaft überschreibt niemals einen read-only Mount.** |
| MT-6 | **Ein read-write Mount legitimiert niemals ein verbotenes Rechteprofil.** |
| MT-7 | **Unbekannter Mountstatus = fail-closed** (`KB04-MOUNT-MODE-MISMATCH`). |
| MT-8 | **M-3 schlägt alles:** ein nicht benötigter Bereich wird **gar nicht** eingebunden, nicht nur `ro`. |

### 7.1 — Vier getrennte Prüfdimensionen

Host- und Runtime-/Container-Berechtigungen sind **verschiedene Gegenstände**.
Der Vertrag unterscheidet deshalb **vier** Dimensionen, die **einzeln** zu
prüfen sind.

| Dimension | Gegenstand | Prüfgrößen |
| --- | --- | --- |
| **D-I Host-Quellobjekt** | das Objekt auf dem Host, bevor es eingebunden wird | Owner · Gruppe · Modus · Objektart · Linkstatus |
| **D-II Mountvertrag** | die Einbindung selbst | read-only oder read-write · erwartetes Ziel · **keine unerwartete zusätzliche Einbindung** |
| **D-III Runtime-sichtbares Objekt** | das Objekt, wie die Runtime es sieht | sichtbarer Modus · Objektart · Pfadauflösung · effektive Lesbarkeit · **fehlende Schreibfähigkeit** |
| **D-IV Runtimeidentität** | wer prüft und wer zugreift | effektive Identität · Supplementary Groups · erwartete Rollenbindung |

| # | Regel |
| --- | --- |
| **MT-9** | **Ein im Bundle deklarierter Modus ist kein alleiniger Nachweis der Host-Quellrechte.** Er belegt **D-II**, nicht **D-I**. |
| **MT-10** | **Sichere Hostrechte lassen sich nicht allein aus der Runtimeansicht ableiten** — **D-III** belegt **D-I** nicht. |
| **MT-11** | **Eine sichere Runtimeansicht lässt sich nicht allein aus den Hostrechten ableiten** — **D-I** belegt **D-III** nicht. |
| **MT-12** | Mountmodus und POSIX-Modus bleiben **getrennte, jeweils notwendige** Prüfschritte (MT-1, MT-2, MT-4). |
| **MT-13** | **Eine nicht prüfbare Dimension gilt als nicht erfüllt** — `KB04-STATE-INDETERMINATE`, fail-closed. |
| **MT-14** | Der Gesamtzustand ist **nur dann konform, wenn alle erforderlichen Dimensionen positiv validiert** wurden. Eine übersprungene Dimension ist **keine bestandene Dimension**. |

> Dieser Vertrag trifft **keine** Aussage über konkrete Container- oder
> Compose-Implementierungsdetails, die nicht repository-intern belegt sind.
> Welche Dimension mit welchem Mittel feststellbar ist, ist ein **offener
> Punkt der realen Deployment-Evidenz** — siehe §10.6 und §18.

**Keine Bundle-Datei wird durch diesen Vertrag geändert.**

---

## 8 — Identitätsbindungsvertrag

Ein **implementierungsneutrales Schema**. **Es wird keine Konfigurationsdatei
angelegt und kein realer Wert eingetragen.**

| Feld | Pflicht | Datentyp | Werteklasse | Verbotene Werte |
| --- | :---: | --- | --- | --- |
| `role_id` | **ja** | Zeichenkette | abstrakte Rollenkennung aus §5 | unbekannte Rolle |
| `host_identity_ref` | **ja** | opake Referenz | **lokal** aufzulösen, außerhalb des Repositorys | Klartext-UID/GID, Benutzername, Hostpfad |
| `container_identity_ref` | **ja** | opake Referenz | lokal aufzulösen | s. o. |
| `expected_effective_identity` | **ja** | opake Referenz | muss zur Laufzeit **beobachtbar** sein | „beliebig", Platzhalter |
| `primary_group_ref` | **ja** | opake Referenz | genau eine | leer |
| `read_group_refs` | optional | Liste opaker Referenzen | nur für **PP-2** und **PP-3a** | jede Gruppe mit Schreibwirkung |
| `path_class_refs` | **ja** | Liste | **PC-01** bis **PC-08** | **PC-09**, **PC-10**, **PC-11** |
| `profile_ref` | **ja** | Kennung | **PP-1**, **PP-2**, **PP-3a**, **PP-3b**, **PP-4** | freier Text |
| `value_origin` | **ja** | Aufzählung | `operator-workspace` — **einzig zulässiger Wert** | `repository`, `derived`, `default` |
| `validation_state` | **ja** | Aufzählung | `unvalidated` · `validated` · `rejected` | „angenommen gültig" |
| `collision_state` | **ja** | Aufzählung | `none` · `duplicate-role` · `duplicate-identity` · `cross-bound` | fehlend |

**Kategorische Regeln:** **keine sicheren Defaults für lokale Identitäten** ·
**keine stille Ableitung** bei fehlenden Angaben · **keine automatische
Fallback-Identität** · eine Bindung ist erst gültig, wenn sie **positiv**
validiert wurde.

| Fall | Verhalten | Fehlerklasse |
| --- | --- | --- |
| fehlende Bindung | **fail-closed** | `KB04-BINDING-MISSING` |
| doppelte Bindung derselben Rolle | **fail-closed** | `KB04-BINDING-COLLISION` |
| kollidierende Identität zweier Rollen | **fail-closed** — die Trennung ist der Zweck (KB-02) | `KB04-BINDING-COLLISION` |
| unbekannte Rolle | **fail-closed** | `KB04-ROLE-UNKNOWN` |
| nicht auflösbare Identität | **fail-closed** | `KB04-STATE-INDETERMINATE` |
| Host-/Container-Abweichung | **fail-closed** | `KB04-IDENTITY-MISMATCH` |
| unerwartete Supplementary Group | **fail-closed** | `KB04-GROUP-MISMATCH` |
| unerwartete effektive Identität | **fail-closed** | `KB04-IDENTITY-MISMATCH` |

---

## 9 — Initialisierungsvertrag

### 9.1 Neue, leere Zielstruktur

Der **Setup-Akteur** darf: abstrakte Pfadklassen binden · Verzeichnisse und
Dateien vertragsgemäß initialisieren · Besitz, Gruppe und Modus **vor** dem
ersten Runtime-Start setzen · das Ergebnis **read-only** verifizieren.

**Alle sechs Voraussetzungen müssen gleichzeitig erfüllt sein:** Ziel leer oder
nachweislich neu · **keine** unbekannten Bestandsartefakte · vollständige
Identitätsbindung · vollständiges Contract-Modell · **keine** Teilanwendung ·
**kein** Runtimeprozess aktiv. Fehlt eine, ist der Vorgang **keine
Initialisierung**, sondern **Migration** (§9.2).

**Idempotenz:** ein wiederholter Lauf über einen bereits vertragskonformen
Bereich **verändert nichts** und meldet „unverändert".

### 9.2 Bestehende Zielstruktur

Sobald vorhandene Daten, unbekannte Dateien oder abweichende Rechte bestehen:
**kein automatisches Apply** · **keine rekursive Korrektur** · **kein stilles
`chown` oder `chmod`** · Einstufung als **Migration oder Reparatur** ·
**plan-only** · Auditbedarf · **RT-2-Grenze** · **ausführende Reparatur nicht
freigegeben** (`KB04-MIGRATION-REQUIRED`, `KB04-REPAIR-RT2-REQUIRED`).

### 9.3 Transaktionsgrenze

| Stufe | Gegenstand | Wirkung |
| --- | --- | --- |
| **Preflight** | Contract, Bindung, Zielklassifikation, Plattform | **read-only**; Abbruch vor jeder Wirkung |
| **Plan** | vollständige beabsichtigte Änderungsliste | **wirkungsfrei**; ohne Plan kein Apply |
| **Apply** | **ausschließlich** neue, leere Strukturen nach §9.1 | eng begrenzt |
| **Post-Validation** | Ist-Zustand gegen Zielmodell | **read-only**; Pflicht |
| **Teilerfolg** | teilweise angewandter Plan | **`KB04-INIT-PARTIAL`**, fail-closed; der Bereich gilt als **nicht vorbereitet** |
| **Nicht feststellbar** | Zustand nicht ermittelbar | **`KB04-STATE-INDETERMINATE`**, fail-closed |
| **Rollback** | — | **Es wird keine Rollback-Zusage gegeben.** Ein Rücksetzungsmechanismus existiert nicht; die einzige dokumentierte Rückfallform ist die **Rücksetzung auf den dokumentierten Ausgangszustand** nach §KB-04, operatorgeführt |

**Keine Funktion wird implementiert.**

---

## 10 — Validierungsvertrag

**Alle vier Zeitpunkte sind strikt read-only.** Grundregel: **nicht feststellbar
= nicht erfüllt.** Ein Zustand, der nicht **positiv** als vertragskonform belegt
ist, ist eine Verletzung.

### 10.1 Installationsvalidierung

Contract vollständig · Identitätsbindung vollständig · Pfadklassen vollständig ·
Zielstruktur neu **oder** klassifiziert · Owner · Gruppe · Datei- und
Verzeichnismodus · Mountmodus · Objektart · Linkstatus · unbekannte Inhalte ·
Plattformunterstützung. **Fehler → Installation anhalten.**

### 10.2 Startvalidierung — vor Dienstaufnahme

Effektive Runtimeidentität · Host-/Container-Bindung · **Supplementary
Groups** · Mountmodus · Owner · Gruppe · Modus · PP-Profil · Symlink- und
Hardlinkstatus · Root-Boundary · unbekannte Pfade · **Schreibfähigkeit
verbotener Rollen** (negativ zu belegen).

**Fehler → Dienststart wird blockiert.** Exitcode **`RUNTIME_START_BLOCKED` (4)**
— bestehende, unveränderte Semantik.

### 10.3 Schreibzeitvalidierung

**Die atomare Schreibsemantik aus ADR-0010/ADR-0011 wird nicht neu entschieden.**
Ergänzend gilt je Schreibvorgang: Zielpfad innerhalb der erwarteten Root ·
Zielpfadklasse erlaubt den Vorgang · Akteur besitzt die Schreibrolle ·
**temporärer Pfad im gleichwertigen Sicherheitskontext** (gleiche Pfadklasse,
gleiches Profil, gleiche Root) · Ersetzung bleibt **innerhalb derselben
Sicherheitsgrenze** · Ergebnis entspricht dem Contract · **kein unsicherer
Zwischenzustand**. Verletzung → `KB04-WRITE-CONTRACT-VIOLATION`.

### 10.4 Laufzeitvalidierung

| Zulässig | Unzulässig |
| --- | --- |
| **read-only** Wiederholung der Startprüfung, ausdrücklich angestoßen (Diagnose, Operatoranforderung) | **periodischer Self-Repair** |
| **read-only** Schreibzeitprüfung je Vorgang (§10.3) | **nebenläufige Rechteänderung** |
| Meldung eines Befundes als `incident` | Herabstufung eines Befundes zur Warnung |

**Eine Laufzeitwiederholung ersetzt weder die Startprüfung noch die
Mountgrenze.** Sie begründet **keine** eigenständige Sicherheitszusage, weil
sie eine Zeitpunktaussage bleibt (§11, TOCTOU).

### 10.5 Gate-Zeitpunkt

Ausschließlich **read-only Evidenz** · **keine Reparatur** · **keine
Statushochwertung allein aufgrund synthetischer Evidenz** · Nachweisstufe **4**
verlangt **reale** Nachweise auf einer Profil-A-Instanz · **keine automatische
Gatefreigabe**. Unvollständige Evidenz → `KB04-EVIDENCE-INCOMPLETE`.

### 10.6 PP-3b-Validierung

PP-3b verlangt wegen seiner World-Read-Ausnahme eine **eigene, vollständige**
Prüffolge über alle vier Dimensionen aus §7.1. **Es wird keine neue
Fehlerklasse eingeführt** — jede Abweichung fällt in eine der
vierundzwanzig Klassen aus §13.

| # | Prüfung | Dimension | Fehlerklasse bei Abweichung |
| ---: | --- | :---: | --- |
| 1 | **Pfadklasse ist exakt PC-07** | — | `KB04-CONTRACT-INVALID` |
| 2 | Objekt ist **reguläre Datei** oder ausdrücklich erlaubtes Verzeichnis | D-I / D-III | `KB04-OBJECT-KIND-INVALID` |
| 3 | Artefakt ist **als nicht geheim klassifiziert** (Regeln 3b-6 bis 3b-8) | — | `KB04-CONTRACT-INVALID` · nicht feststellbar: `KB04-STATE-INDETERMINATE` |
| 4 | **Keine lokale Identitätsbindung und kein sensibler Operatorwert** enthalten | — | `KB04-CONTRACT-INVALID` |
| 5 | **Mount ist read-only** | **D-II** | `KB04-MOUNT-MODE-MISMATCH` |
| 6 | **Runtime besitzt keine Schreibfähigkeit** — negativ zu belegen | **D-III** | `KB04-MOUNT-MODE-MISMATCH` beziehungsweise `KB04-MODE-MISMATCH` |
| 7 | **Runtime-sichtbarer Modus entspricht dem Contract** (`0444`/`0555`) | **D-III** | `KB04-MODE-MISMATCH` |
| 8 | **Host-Quellzustand separat geprüft** — oder **als reale Deployment-Evidenz offen ausgewiesen** | **D-I** | `KB04-STATE-INDETERMINATE` |
| 9 | **Keine Symlink- oder Hardlinkabweichung** | D-I / D-III | `KB04-LINK-SYMLINK-ESCAPE` · `KB04-LINK-HARDLINK` |
| 10 | **Keine zusätzliche unerwartete Einbindung** | **D-II** | `KB04-MOUNT-MODE-MISMATCH` |
| 11 | **Effektive Identität und Supplementary Groups** entsprechen der Rollenbindung | **D-IV** | `KB04-IDENTITY-MISMATCH` · `KB04-GROUP-MISMATCH` |
| 12 | **Bundlemodus und tatsächlich sichtbarer Zustand stimmen überein** | D-II gegen D-III | `KB04-MODE-MISMATCH` |

**Ein nicht feststellbarer Zustand in irgendeiner dieser Prüfungen ist
fail-closed** (MT-13). **Der Bundlemodus allein genügt nicht** (MT-9): er
belegt die Mountzusage, **nicht** den Host-Quellzustand. Solange **D-I** nicht
positiv validiert werden kann, ist der Host-Quellzustand **offen auszuweisen**
und darf **nicht** als erfüllt dargestellt werden.

---

## 11 — Link- und Pfadsicherheit

| # | Regel |
| --- | --- |
| LP-1 | **Normalisierte Pfadauflösung** vor jeder Aussage; Vergleiche niemals allein auf String-Präfixen |
| LP-2 | **Feste Root-Boundary** je Pfadklasse; Ergebnis außerhalb → `KB04-PATH-OUTSIDE-ROOT` |
| LP-3 | **Bereichsverlassende Symlinks unzulässig** (M-4, I-5) → `KB04-LINK-SYMLINK-ESCAPE` |
| LP-4 | **Interne Symlinks** werden **nicht aufgelöst, sondern abgelehnt** — bestehende Praxis aus ADR-0010/ADR-0011 |
| LP-5 | **Hardlinks in geschützten Bereichen unzulässig** — sie unterlaufen die Bereichsgrenze, ohne als Link sichtbar zu sein → `KB04-LINK-HARDLINK` |
| LP-6 | **Unzulässige Objektarten:** Device Files, FIFOs, Sockets → `KB04-OBJECT-KIND-INVALID` |
| LP-7 | **Mountpoints und Bind Mounts** innerhalb einer Pfadklasse sind **kein** zulässiger Pfadbestandteil; ein Bereichswechsel über eine Mountgrenze ist verboten |
| LP-8 | **Path Traversal** wird durch LP-1 und LP-2 abgefangen, nicht durch Zeichenkettenfilter |
| LP-9 | **TOCTOU:** Prüfung und Wirkung beziehen sich auf **dasselbe aufgelöste Objekt**. Ein Prüfergebnis gilt **nicht** über einen Schreibvorgang hinaus. Die Rechteprüfung ist **niemals** die einzige Absicherung — Mountmodus (KB-03), Prozessidentität (KB-01/KB-02) und atomare Schreibsemantik (I-6) tragen unabhängig |
| LP-10 | **Unbekannte oder nicht eindeutig prüfbare Situation = fail-closed** (`KB04-STATE-INDETERMINATE`) |

**Es wird keine Bibliothek und keine System-API verbindlich festgelegt** — das
Repository gibt keine vor.

---

## 12 — Migration und Reparatur

### Migration

Bewusster Operatorvorgang · **vollständiger Scan** · **Plan vor Wirkung** ·
nachvollziehbare Differenzliste · **keine implizite Rekursion** · **keine
unbekannte Datei ohne ausdrückliche Entscheidung** · **keine automatische
Übernahme unsicherer Zustände** · **keine Ausführung in B1C**.

### Reparatur

**Niemals** Runtime-Self-Repair · **niemals** still · **niemals** nebenläufig ·
**Auditspur erforderlich** · diese Auditspur ist **RT-2** · **RT-2 ist nicht
implementiert** · **der ausführende Reparaturmodus bleibt gesperrt**
(`KB04-REPAIR-RT2-REQUIRED`).

### Erlaubter und gesperrter B2-Scope

| B2 darf **ohne RT-2 höchstens** | B2 darf **ohne neue Freigabe nicht** |
| --- | --- |
| read-only **Detection** | **Apply auf bestehende Daten** |
| **Planerzeugung** | **rekursive Reparatur** |
| **Validierung** | **automatische `chown`-/`chmod`-Korrektur** |
| **Fail-closed-Ablehnung** | **Rollbackversprechen** |
| **Initialisierung einer nachweislich neuen, leeren Zielstruktur** nach §9.1 | **produktive Migration** |

---

## 13 — Fehlerklassen

**Vierundzwanzig Klassen. Alle fail-closed.** Wirkungsspalten: **I** Installation
· **S** Start · **L** Laufzeit · **G** Gate. `—` = nicht anwendbar.

| # | Bezeichnung | I | S | L | G | reparierbar | Operatoraktion | Evidenzbedarf |
| ---: | --- | :-: | :-: | :-: | :-: | :-: | --- | --- |
| 1 | `KB04-CONTRACT-MISSING` | Stopp | Stopp | Stopp | blockiert | nein | Contract bereitstellen | Contract-Referenz |
| 2 | `KB04-CONTRACT-INVALID` | Stopp | Stopp | Stopp | blockiert | nein | Contract korrigieren | Befundliste |
| 3 | `KB04-BINDING-MISSING` | Stopp | Stopp | Stopp | blockiert | nein | Bindung im Operator-Workspace ergänzen | Bindungsstatus |
| 4 | `KB04-BINDING-COLLISION` | Stopp | Stopp | Stopp | blockiert | nein | Kollision auflösen | Kollisionsstatus |
| 5 | `KB04-IDENTITY-MISMATCH` | Stopp | **Startsperre** | Stopp | blockiert | nein | Bindung oder Deployment korrigieren | Ist-/Soll-Identität, opak |
| 6 | `KB04-ROLE-UNKNOWN` | Stopp | Stopp | Stopp | blockiert | nein | Rolle klären | Rollenkennung |
| 7 | `KB04-PATHCLASS-UNKNOWN` | Stopp | Stopp | Stopp | blockiert | nein | Pfad klassifizieren oder entfernen | Pfadklasse, relativ |
| 8 | `KB04-OBJECT-KIND-INVALID` | Stopp | Stopp | Stopp | blockiert | **plan-only** | Objekt entfernen | Objektart |
| 9 | `KB04-OWNER-MISMATCH` | Stopp | **Startsperre** | Stopp | blockiert | **plan-only** | Migration planen | Rechteauflistung |
| 10 | `KB04-GROUP-MISMATCH` | Stopp | **Startsperre** | Stopp | blockiert | **plan-only** | Migration planen | Rechteauflistung |
| 11 | `KB04-MODE-MISMATCH` | Stopp | **Startsperre** | Stopp | blockiert | **plan-only** | Migration planen | Rechteauflistung |
| 12 | `KB04-MODE-WORLD-BITS` | Stopp | **Startsperre** | Stopp | blockiert | **plan-only** | sofortige Operatorprüfung | Rechteauflistung, `incident` |
| 13 | `KB04-MODE-SPECIAL-BITS` | Stopp | **Startsperre** | Stopp | blockiert | **plan-only** | Zusatzbits klären | Rechteauflistung |
| 14 | `KB04-MOUNT-MODE-MISMATCH` | Stopp | **Startsperre** | Stopp | blockiert | nein | Deployment korrigieren | Mountliste |
| 15 | `KB04-LINK-SYMLINK-ESCAPE` | Stopp | **Startsperre** | Stopp | blockiert | **plan-only** | Link entfernen | Linkbefund, `incident` |
| 16 | `KB04-LINK-HARDLINK` | Stopp | **Startsperre** | Stopp | blockiert | **plan-only** | Link entfernen | Linkbefund |
| 17 | `KB04-PATH-OUTSIDE-ROOT` | Stopp | **Startsperre** | Stopp | blockiert | nein | Pfadmodell korrigieren | Pfadbefund, relativ |
| 18 | `KB04-PLATFORM-UNSUPPORTED` | Stopp | **Startsperre** | Stopp | blockiert | nein | Profil A verwenden | Plattformbefund |
| 19 | `KB04-STATE-INDETERMINATE` | Stopp | **Startsperre** | Stopp | blockiert | nein | Ursache klären | Prüfprotokoll |
| 20 | `KB04-MIGRATION-REQUIRED` | Stopp | **Startsperre** | — | blockiert | **plan-only** | Migration anordnen | Differenzliste |
| 21 | `KB04-REPAIR-RT2-REQUIRED` | Stopp | — | — | blockiert | **nein — gesperrt** | RT-2 zuerst umsetzen | RT-2-Status |
| 22 | `KB04-INIT-PARTIAL` | Stopp | **Startsperre** | — | blockiert | **plan-only** | Zielstruktur neu bewerten | Planvergleich |
| 23 | `KB04-WRITE-CONTRACT-VIOLATION` | — | — | **Vorgang abgelehnt** | blockiert | nein | Vorgang untersuchen | Schreibbefund, `incident` |
| 24 | `KB04-EVIDENCE-INCOMPLETE` | — | — | — | **blockiert** | nein | Nachweise vervollständigen | Evidenzlücke |

**Alle Sicherheitsverletzungen sind fail-closed.** „Reparierbar: plan-only"
bedeutet: ein Plan **darf** erzeugt werden; die **Ausführung bleibt gesperrt**
(§12).

---

## 14 — Issue- und Exitcodes

### Bestandsaudit

| Ebene | Bestand | Konvention |
| --- | --- | --- |
| Issue-Code-Präfixe | **`BND`** (Bundle-Offline-Validator), **`MAP`** (Mapping-Draft-Validator), **`GATE`** (Activation Gate), **`QF`** (Quarantäne-Befunde) | `<PRÄFIX>-<BEREICH>-<BEDINGUNG>`, SCREAMING-KEBAB |
| CLI-Exitcodes | `0`, `2`–`14` belegt; `64` `USAGE_ERROR`; `70` `INTERNAL_ERROR` | stabiler `StrEnum`-Name + feste Zahl; *„Ein Exitcode wird nach seiner Dokumentation nicht mehr verändert."* |
| Nächste freie Zahl | **15** | — |
| Präfixkollision `KB04` | **0 Treffer** im gesamten Repository | frei |

### Entscheidung

**Gemischt — für Exitcodes Möglichkeit A, für Issue-Codes Möglichkeit B.**

**Möglichkeit A — Wiederverwendung ohne Überladung:**

| Fall | Bestehender Code | Begründung |
| --- | --- | --- |
| Startvalidierung schlägt fehl | **`RUNTIME_START_BLOCKED` (4)** | dokumentierte Semantik ist exakt *„`run` verweigert fail-closed"* |
| Contract- oder Bindungsdatei ungültig | **`CONFIG_INVALID` (2)** | dokumentierte Semantik *„Konfiguration ungültig"* |
| Falsche Kommandozeile | **`USAGE_ERROR` (64)** | unverändert |

**Möglichkeit B — vertraglich reservierte, noch nicht implementierte Codes:**

| Name | Zahl | Kategorie | Semantik | Fehlerklassen |
| --- | :---: | --- | --- | --- |
| `FILESYSTEM_ENFORCEMENT_BLOCKED` | **15** | reserviert, **nicht implementiert** | Rechte-, Link-, Mount- oder Plattformbefund verhindert den Vorgang fail-closed | 1–19, 23, 24 |
| `FILESYSTEM_MIGRATION_REQUIRED` | **16** | reserviert, **nicht implementiert** | Bestand weicht ab; Migration ist erforderlich und **nicht** freigegeben | 20, 21, 22 |

**Issue-Codes:** Präfix **`KB04-`**, vierundzwanzig Namen nach §13, **reserviert
und nicht implementiert**.

**Verbindlich:** keine bestehende Nummer oder Kennung wird überschrieben · keine
semantische Überladung · **keine neue Security-Test-ID** · **NT-25 bleibt nach
Regel TT-5 frei und wird nicht wiederverwendet** · die Reservierung ist durch
ADR-0014, offener Parameter 10, ausdrücklich gedeckt und erfordert **keine**
neue Architekturentscheidung.

### Bedeutung der Reservierung

| # | Regel |
| --- | --- |
| **RC-1** | Die Codes sind in B1C **ausschließlich Contract-Reservierungen**. |
| **RC-2** | Sie sind **nicht implementiert**. |
| **RC-3** | **Kein aktueller CLI-, Validator-, Gate- oder Runtimepfad emittiert sie.** |
| **RC-4** | **Bestehende Codes werden nicht umgedeutet.** `RUNTIME_START_BLOCKED` (4), `CONFIG_INVALID` (2) und `USAGE_ERROR` (64) werden **ausschließlich** ihrer bereits dokumentierten Semantik zugeordnet. |
| **RC-5** | **Die Reservierung verändert das heutige öffentliche Verhalten nicht.** |
| **RC-6** | **B2 muss Implementierung, Dokumentation und Tests gemeinsam liefern** — kein Code ohne Vertrag und ohne Nachweis. |
| **RC-7** | **Vor einer Implementierung ist erneut zu prüfen:** Nummer weiterhin frei · Name weiterhin kollisionsfrei · Semantik weiterhin eindeutig · **keine öffentliche Kompatibilitätskollision**. |
| **RC-8** | **Bei einer späteren Kollision:** **keine stille Neunummerierung** · **keine semantische Überladung** · **B2 stoppen** · neue Contract- beziehungsweise Governance-Prüfung. |
| **RC-9** | **Die bloße Reservierung ist kein Implementierungs- und kein Releaseversprechen.** |
| **RC-10** | **Aus der Reservierung wird keine Security-Test-ID abgeleitet.** |

**In diesem Lauf wird keine bestehende Codeimplementierung geändert.**

---

## 15 — Validierungs- und Testplan

**Zwölf positive** (`KB04-T-P01`…`P12`) und **dreiunddreißig negative**
Fälle (`KB04-T-N01`…`N33`).

**Kennungen `KB04-T-*` sind vorläufige interne Testkennungen. Sie sind
ausdrücklich keine Security-Test-IDs** und stehen in keinem Bezug zur
NT-Nummerierung. **Kein Testfall wird in B1C ausgeführt** — bei jedem Fall gilt
*Ausführung in B1C: nein*.

### Positive Fälle

| ID | Anforderung | Klasse | Rolle | Profil | Ausgangszustand | Aktion | Erwartung | Ebene | Fixture | Gate |
| --- | --- | --- | --- | :---: | --- | --- | --- | --- | --- | --- |
| `KB04-T-P01` | PP-1 Datei | PC-02 | data-worker | PP-1 | `0600`, korrekter Owner | validieren | konform | synthetisch | Temp-Baum | — |
| `KB04-T-P02` | PP-1 Verzeichnis | PC-06 | data-worker | PP-1 | `0700` | validieren | konform | synthetisch | Temp-Baum | — |
| `KB04-T-P03` | PP-2 Datei | PC-03 | control-plane | PP-2 | `0640`, Lesegruppe | validieren | konform | synthetisch | Temp-Baum | — |
| `KB04-T-P04` | PP-2 Verzeichnis | PC-04 | control-plane | PP-2 | `0750` bzw. `2750` | validieren | konform | synthetisch | Temp-Baum | — |
| `KB04-T-P05` | PP-3a Leseberechtigung | PC-01 | beide | PP-3a | `0640`/`0750`, Owner außerhalb | lesen prüfen | lesbar, **nicht** schreibbar | synthetisch | Temp-Baum | RG-3 |
| `KB04-T-P06` | PP-3b bundle-fixiert | PC-07 | beide | PP-3b | `0444`/`0555` | validieren | konform zum Bundle | synthetisch | Bundlewerte | — |
| `KB04-T-P07` | PP-4 nicht vorhanden | PC-09, PC-10 | — | PP-4 | Pfad existiert nicht | validieren | konform | synthetisch | Abwesenheit | — |
| `KB04-T-P08` | Host-/Container-Bindung | — | alle | — | Bindung vollständig, effektiv passend | Startprüfung | konform | synthetisch | Bindungsattrappe | RG-1 |
| `KB04-T-P09` | read-only Mount | PC-01 | beide | PP-3a | `ro` beidseitig | Mountprüfung | konform | synthetisch | Mountmodell | RG-5 |
| `KB04-T-P10` | atomare Ersetzung | PC-03 | control-plane | PP-2 | Temp im gleichen Kontext | Ersetzung prüfen | konform, kein Zwischenzustand | synthetisch | Storelayout | — |
| `KB04-T-P11` | neue leere Zielstruktur | PC-02 | setup | PP-1 | leer, kein Bestand | Preflight, Plan, Post-Validation | vollständig, idempotent | synthetisch | leerer Baum | — |
| `KB04-T-P12` | **PP-3b über alle vier Dimensionen** (§10.6) | PC-07 | beide | PP-3b | nicht geheim klassifiziert, `0444`/`0555`, ro-Mount, Hostquelle geprüft | zwölf Prüfungen aus §10.6 | konform, **keine Schreibfähigkeit** | synthetisch für D-II/D-III/D-IV, **real für D-I** | Bundlewerte, Dimensionsattrappe | — |

### Negative Fälle

| ID | Gegenstand | Klasse | Erwartung | Fehlerklasse | Ebene | NT-Bezug |
| --- | --- | --- | --- | --- | --- | --- |
| `KB04-T-N01` | world-writable Datei | PC-02 | **abgelehnt** | `KB04-MODE-WORLD-BITS` | synthetisch | — |
| `KB04-T-N02` | world-writable Verzeichnis | PC-06 | **abgelehnt** | `KB04-MODE-WORLD-BITS` | synthetisch | — |
| `KB04-T-N03` | falscher Owner | PC-03 | **abgelehnt** | `KB04-OWNER-MISMATCH` | synthetisch | — |
| `KB04-T-N04` | falsche Gruppe | PC-04 | **abgelehnt** | `KB04-GROUP-MISMATCH` | synthetisch | — |
| `KB04-T-N05` | falscher Modus | PC-05 | **abgelehnt** | `KB04-MODE-MISMATCH` | synthetisch | — |
| `KB04-T-N06` | verbotene Supplementary Group | — | **abgelehnt** | `KB04-GROUP-MISMATCH` | synthetisch | — |
| `KB04-T-N07` | **Retrieval kann Canonical schreiben** | PC-01 | **Schreibversuch scheitert** | `KB04-MODE-MISMATCH` / `KB04-MOUNT-MODE-MISMATCH` | **real** | **NT-04** |
| `KB04-T-N08` | **Ingest schreibt Canonical unkontrolliert** | PC-01 | **Schreibversuch scheitert** | wie N07 | **real** | **NT-04** |
| `KB04-T-N09` | Host-/Container-Identität weicht ab | — | **Startsperre** | `KB04-IDENTITY-MISMATCH` | synthetisch | — |
| `KB04-T-N10` | Bindung fehlt | — | **abgelehnt** | `KB04-BINDING-MISSING` | synthetisch | — |
| `KB04-T-N11` | Bindung kollidiert | — | **abgelehnt** | `KB04-BINDING-COLLISION` | synthetisch | — |
| `KB04-T-N12` | unbekannte Rolle | — | **abgelehnt** | `KB04-ROLE-UNKNOWN` | synthetisch | — |
| `KB04-T-N13` | unbekannte Pfadklasse | PC-11 | **abgelehnt** | `KB04-PATHCLASS-UNKNOWN` | synthetisch | — |
| `KB04-T-N14` | **Symlink-Escape** | PC-02 | **blockiert** | `KB04-LINK-SYMLINK-ESCAPE` | **real** | **NT-05** |
| `KB04-T-N15` | Hardlink | PC-03 | **abgelehnt** | `KB04-LINK-HARDLINK` | synthetisch | — |
| `KB04-T-N16` | Path Traversal | PC-04 | **abgelehnt** | `KB04-PATH-OUTSIDE-ROOT` | synthetisch | — |
| `KB04-T-N17` | unbekannte Objektart (FIFO, Socket, Device) | PC-02 | **abgelehnt** | `KB04-OBJECT-KIND-INVALID` | synthetisch | — |
| `KB04-T-N18` | read-write Mount für read-only Rolle | PC-01 | **abgelehnt** | `KB04-MOUNT-MODE-MISMATCH` | synthetisch | — |
| `KB04-T-N19` | Zustand nicht feststellbar | beliebig | **abgelehnt** | `KB04-STATE-INDETERMINATE` | synthetisch | — |
| `KB04-T-N20` | Bestand erfordert Reparatur | PC-05 | **plan-only, kein Apply** | `KB04-MIGRATION-REQUIRED` | synthetisch | — |
| `KB04-T-N21` | Reparatur ohne RT-2 | — | **gesperrt** | `KB04-REPAIR-RT2-REQUIRED` | synthetisch | — |
| `KB04-T-N22` | partielle Initialisierung | PC-02 | **abgelehnt**, Bereich gilt als nicht vorbereitet | `KB04-INIT-PARTIAL` | synthetisch | — |
| `KB04-T-N23` | nicht unterstützte Plattform | — | **nicht feststellbar → fail-closed** | `KB04-PLATFORM-UNSUPPORTED` | synthetisch | — |
| `KB04-T-N24` | verbotene Zusatzbits | PC-06 | **abgelehnt** | `KB04-MODE-SPECIAL-BITS` | synthetisch | — |
| `KB04-T-N25` | Schreibzeitverletzung, Temp außerhalb des Kontexts | PC-03 | **Vorgang abgelehnt** | `KB04-WRITE-CONTRACT-VIOLATION` | synthetisch | — |
| `KB04-T-N26` | **PP-3b-Artefakt enthält Secretmaterial** — Fixture nutzt einen **synthetischen Marker**, **keinen Wert** | PC-07 | **abgelehnt, nicht als PP-3b klassifizierbar** | `KB04-CONTRACT-INVALID` | synthetisch | — |
| `KB04-T-N27` | **PP-3b außerhalb PC-07 verwendet** | beliebig ≠ PC-07 | **abgelehnt** | `KB04-CONTRACT-INVALID` | synthetisch | — |
| `KB04-T-N28` | **Host-Quellrechte nicht feststellbar** | PC-07 | **abgelehnt** | `KB04-STATE-INDETERMINATE` | synthetisch | — |
| `KB04-T-N29` | Runtimeobjekt erscheint read-only, **Hostquelle nicht positiv validiert** | PC-07 | **abgelehnt** — D-III belegt D-I nicht (MT-10) | `KB04-STATE-INDETERMINATE` | synthetisch | — |
| `KB04-T-N30` | **Mount ist read-write** | PC-07 | **abgelehnt** | `KB04-MOUNT-MODE-MISMATCH` | synthetisch | — |
| `KB04-T-N31` | **Runtime kann das Artefakt verändern** | PC-07 | **abgelehnt** | `KB04-MOUNT-MODE-MISMATCH` · `KB04-MODE-MISMATCH` | **real** | — |
| `KB04-T-N32` | **Unerwartete Identität kann auf das Artefakt zugreifen** | PC-07 | **abgelehnt** | `KB04-IDENTITY-MISMATCH` · `KB04-GROUP-MISMATCH` | synthetisch | — |
| `KB04-T-N33` | **Bundlemodus und tatsächlich sichtbarer Zustand weichen ab** | PC-07 | **abgelehnt** — der Bundlewert wird **nicht** automatisch akzeptiert (MT-9) | `KB04-MODE-MISMATCH` | **real** | — |

**Synthetisch prüfbar:** Modell-, Zuordnungs-, Bindungs-, Ablehnungs- und
Fehlerklassenlogik auf einem temporären Baum außerhalb des Repositorys.
**Nur real prüfbar:** `KB04-T-N07`, `KB04-T-N08`, `KB04-T-N14`,
`KB04-T-N31`, `KB04-T-N33`, die Dimension **D-I Host-Quellobjekt** in
`KB04-T-P12` sowie jede
Rechteauflistung „vor und nach dem Start" — Nachweisstufe **4**, Profil-A-Instanz.

---

## 16 — NT-04 und NT-05

**Wörtlich aus der bestehenden Authority; keine Umdeutung, keine neue NT-ID,
keine Ausführung.**

| | **NT-04** | **NT-05** |
| --- | --- | --- |
| Gegenstand | **Schreibversuch auf Canonical** | **Symlink Escape aus dem Bereich** |
| Erwartung | **scheitert** | **blockiert** |
| Controls | **KB-03, KB-04** | **KB-04** |
| Betroffene Vertragsregeln | I-3, I-4 · PC-01 mit **PP-3a** · MT-3 bis MT-6 · Rollenmatrix Zeilen *retrieval* und *ingest* | I-5 · LP-1 bis LP-4 · LP-9 |
| Benötigter Fehlzustand | eine Rolle ohne Canonical-Schreibrecht versucht zu schreiben | ein Symlink innerhalb eines geschützten Bereichs zeigt nach außen |
| Erwartetes Ablehnungsverhalten | Schreibvorgang scheitert **auf Betriebssystemebene**, nicht erst in der Anwendung | Auflösung wird **verweigert**, nicht gefolgt |
| Synthetisch erzeugbar | Prüf- und Ablehnungslogik, Fehlerklassenzuordnung, Fixtures | Erkennungs- und Ablehnungslogik, Fixtures |
| Nur real | **das tatsächliche Scheitern** auf einer Profil-A-Instanz | **die tatsächliche Blockade** auf einer Profil-A-Instanz |
| Ein bestandener Test belegt **nicht** | dass KB-03 vollständig ist · dass andere Bereiche geschützt sind · dass ein Gate erfüllt ist · dass eine Control hochgestuft werden darf | dass Hardlinks abgedeckt sind · dass TOCTOU gelöst ist · dass ein Gate erfüllt ist |

**Beide sind nicht ausgeführt** — Stand **0 von 32** Negativtests, **0 von 1**
Positivtest.

---

## 17 — SB-S04, OD-37 und Gates

### SB-S04

| Feld | Inhalt |
| --- | --- |
| Auslösekriterium | **Schreibzugriff auf Canonical** |
| Bezug | **NT-04** unmittelbar; **NT-05** mittelbar über I-5 |
| Stop-Wirkung | **Schreibpfad sperren**; Nachweis: Rechteauflistung und Auditeintrag |
| Aufhebung | Bestand gegen Git und Backup abgleichen · Read-only erzwungen · **KB-04 negativ getestet** · Freigabe **A0** |
| Aktueller Stand | **nicht wirksam** — keine Instanz, kein Test, keine Auditkette |
| Wirkung dieses Vertrags | **keine Statusänderung** |

### OD-37

| Anteil | Durch diesen Vertrag |
| --- | --- |
| Bereichsschnitt, Rollen, Profile, Bindungsschema, Validierungszeitpunkte, Fehlerklassen | **strukturiert** |
| Konkrete lokale Identitäten und Modi der Zielinstanz | **offen — Deployment Required** |
| Tatsächliche Isolation, Unzugänglichkeit für den Indexer, Rechteauflistung | **nur real prüfbar** |
| **Warum D-060 OD-37 nicht schließt** | OD-37 verlangt den **Nachweis auf der Ziel-VM**. Ein Vertrag ist kein Nachweis; es existiert keine Instanz, kein gesetztes Recht und kein ausgeführter Test |
| Später benötigte Evidenz | Rechteauflistung vor und nach dem Start · **NT-04**, **NT-05** bestanden · Mountliste je Identität · Auditeintrag |

### Security Foundation Readiness Gate

| Punkt | Gegenstand | Contract-Evidenz | Art |
| --- | --- | --- | --- |
| **3** | OS-Rechte umgesetzt — Rechteauflistung, keine world-writable | PP-Profile, §13 Klassen 9–13 | **real** (Stufe 2) |
| **5** | Canonical read-only nachgewiesen — **NT-04 bestanden** | PC-01/PP-3a, MT-3 bis MT-6 | **real** (Stufe 4) |

**Status bleibt `NOT EVALUATED`.**

### Mapping Activation Gate

| Punkt | Gegenstand | KB-04-Abhängigkeit |
| --- | --- | --- |
| **7** | Minimale Rechte bestätigt | mittelbar über Rollenmatrix und PP-Profile |
| **8** | Read-only technisch nachgewiesen — Schreibversuch scheitert tatsächlich | mittelbar über PC-01 und NT-04 |
| **11** | Symlink-Verhalten geprüft | mittelbar über LP-3, LP-4 und NT-05 |

**Keine Auswertung. Status bleibt `NOT EVALUATED`.**

---

## 18 — B2-Kandidatenscope

**Nicht autorisiert. B1C autorisiert keine der Teilphasen.**

| Teilphase | Möglicher Scope | Ausdrücklich nicht |
| --- | --- | --- |
| **B2A — Contract Model and Read-only Validator** | Contract-Datenmodell · Pfadklassenmodell · Rollenmodell · PP-Profile · Bindungsvalidierung · read-only Dateisystemvalidierung · Fehlerklassen | **keine Deploymentmutation** |
| **B2B — New-target Initialization Boundary** | **ausschließlich** neue, leere Zielstrukturen · Setup-Akteur · idempotente Initialisierung · Post-Validation | **kein Bestand**, **kein Reparaturmodus** |
| **B2C — Synthetic Tests and Evidence** | Unit- und Contract-Tests · negative Fixtures · **Vorbereitung** von NT-04/NT-05 | **keine reale Deploymentausführung** |
| **B2D — Profile-A Deployment Integration** | lokale Identitätsbindung · reale Profil-A-Instanz · reale Nachweise · OD-37 · Gate-Evidenz | **späterer Kandidat, nicht autorisiert** |

**Gesperrter Scope:** produktive Reparatur · Migration bestehender Daten · RT-2 ·
reale Gatefreigabe · Control-Uplift · **Stage 2**.

### B2-Grenze für PP-3b

**B2 darf PP-3b nur implementieren oder übernehmen, wenn alle drei
Bedingungen erfüllt sind:**

| # | Bedingung |
| --- | --- |
| **B2-3b-1** | Die Dimensionen **D-I Host**, **D-II Mount**, **D-III Runtimeobjekt** und **D-IV Identität** sind **getrennt validierbar**. |
| **B2-3b-2** | **Secretfreiheit beziehungsweise zulässiger Inhalt** ist **vertraglich prüfbar** (Regeln 3b-6 bis 3b-8). |
| **B2-3b-3** | **Keine Dimension wird still übersprungen.** |

**Ermöglicht die spätere technische Plattform die zugesagte Trennung oder
Prüfung nicht zuverlässig, gilt:**

| # | Regel |
| --- | --- |
| **B2-3b-4** | **Kein stiller Fallback.** |
| **B2-3b-5** | **Kein bloßer Warnmodus.** |
| **B2-3b-6** | **Keine automatische Akzeptanz des Bundlewerts** (MT-9). |
| **B2-3b-7** | **B2 stoppt mit einem klaren Blocker.** |
| **B2-3b-8** | Eine **Architektur- oder Contract-Neubewertung** ist erforderlich. |

**Kandidatenbefund für eine spätere Bewertung, hier nicht entschieden:** eine
Verschärfung des Config-Bindmounts von `0444` auf ein gruppenbeschränktes
Profil wäre eine **Bundle- und Deployment-Entscheidung**, läge außerhalb
dieses Vertrags und dürfte **nur in einem ausdrücklich autorisierten
technischen Scope** erfolgen — unter Erhalt der erforderlichen
Runtime-Lesbarkeit (Regel 3b-16).

---

## 19 — Aussagegrenzen

| Nicht belegt | Tatsächlicher Stand |
| --- | --- |
| KB-04 sei implementiert, getestet oder enforced | **`DOCUMENTED ONLY`** |
| Ein Security-Foundation-Test sei ausgeführt | **0 von 32** NT, **0 von 1** PT |
| Ein Gate sei ausgewertet | beide **`NOT EVALUATED`** |
| Eine Capability sei erreicht | **0 von 29** |
| SB-S04 sei wirksam | **nicht wirksam** |
| OD-37 sei geschlossen | **offen** |
| RT-2 existiere | **nicht implementiert** |
| Eine Bereitstellung existiere | **keine** |
| Ein Recht sei gesetzt | **keines** |

**Ein implementierungsfähiger Vertrag ist keine Implementierung, und eine
geplante Prüfung ist kein Nachweis.**
