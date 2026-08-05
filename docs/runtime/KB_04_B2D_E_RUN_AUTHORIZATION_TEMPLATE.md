# KB-04 B2D-E Run Authorization Template

**Leeres, versioniertes Pre-run-Autorisierungstemplate der Teilphase B2D-E**

> ## Vor jeder Verwendung lesen
>
> - **Diese versionierte Datei ist kein ausgefülltes Autorisierungsrecord.**
> - **Sie autorisiert keinen B2D-E-Lauf.**
> - Vor Verwendung ist eine **Kopie außerhalb dieses Repositorys** im
>   **lokalen Operator-Workspace** anzulegen.
> - **Nur die lokale Kopie darf ausgefüllt werden.**
> - **Eine ausgefüllte Kopie darf niemals zurück in das Repository gelangen** —
>   weder kopiert noch gestaged, committed, gepusht oder veröffentlicht.
> - **Leere Pflichtwerte sind beabsichtigt und fail-closed.**
> - **Bleibt ein Pflichtfeld leer, darf der Lauf nicht beginnen.**

---

## 1 — Status und Zweck

| Feld | Wert |
| --- | --- |
| Work Package | **CBP-WP-022** — KB-04 Enforcement Stage 1 |
| Eingeführt in | **B2D-AUTH** |
| Grundlage | **D-064**, `accepted`, **A0** |
| Artefaktvariante | **A1** — versioniertes leeres Template mit lokaler ausgefüllter Kopie |
| Charakter | **dokumentarisches Governance-Template** |
| Autorisierungswirkung | **keine** |

**Was dieses Dokument ist:** ein leeres Formular, das den Pflichtfeldsatz einer
späteren, ausschließlich lokal auszufüllenden Pre-run-Autorisierung festlegt.

**Was dieses Dokument nicht ist:** kein Runbook · kein Script · keine
Konfiguration · kein Deploymentartefakt · kein Evidenzartefakt · keine
Gate-Eingabe · **keine Ausführungsfreigabe**.

---

## 2 — Authority und Quellen

| Quelle | Beitrag |
| --- | --- |
| **D-064** (A0) | wählt Variante **A1**, ratifiziert **genau zwanzig** Pre-run-Pflichtfelder und die Trennung von Template und lokaler Kopie |
| **D-063** (A0) | zehn Bestätigungen je Lauf · Einmaligkeit · Nichtübertragbarkeit · Verfallsgründe · **Verbot der Pauschalfreigabe**; vertagte die Form auf D-064 |
| **ADR-0014** (A1) | Durchsetzung **außerhalb der Runtime und außerhalb des Repositorys**; Runtime strikt read-only |
| **ADR-0013** (A1) | Security-Control-Form ist **negative-evidence-only** und **autorisiert nichts** |
| **Contract §3** | keine realen UID-/GID-Werte, keine realen Benutzer- oder Gruppennamen, keine realen Hostpfade |
| **Contract §8** | Identitätsbindung; `value_origin` ausschließlich **operator-workspace**, **niemals repository** |
| **Contract §9.1 / §9.3** | nachweislich neue und leere Zielstruktur; **keine Rollback-Zusage** |
| **Contract §15 / §16** | die sechs real-only Fälle sowie NT-04 und NT-05 |
| **Contract §17 / §19** | Gates ohne Auswertung; *„eine geplante Prüfung ist kein Nachweis"* |
| **Profile-A-Integrationsplan** | Phasenmodell, Recovery-Gate, Preconditions, Stop-Bedingungen |
| **R-35**, **R-36** | die beiden hohen offenen Risiken, die dieser Feldsatz mindert |

Ein Statusspiegel steht **niemals** über einer dieser Quellen.

---

## 3 — Handling- und Speicherregeln

| # | Regel |
| --- | --- |
| H-1 | Die versionierte Datei bleibt **dauerhaft leer**. |
| H-2 | Vor jedem geplanten Lauf wird eine **Kopie in den lokalen Operator-Workspace** gelegt — außerhalb dieses Repositorys. |
| H-3 | **Ausschließlich die lokale Kopie** wird ausgefüllt. |
| H-4 | Die ausgefüllte Kopie wird **niemals** zurückkopiert, gestaged, committed, gepusht oder veröffentlicht. |
| H-5 | Je Lauf entsteht **genau eine** lokale Kopie. |
| H-6 | Die lokale Kopie verbleibt im Operator-Workspace und unterliegt dessen Aufbewahrung. |
| H-7 | Wird ein Wert in einem Repositoryartefakt gefunden, ist das eine **Stop-Bedingung**. |

---

## 4 — Public-Neutrality-Grenze

**Ausschließlich lokal — niemals in einem Commit:**

Hostname · VM-Name · Node-Name · IP-Adresse · Netzbereich · lokale Pfade ·
Mountpunkte · UID · GID · Benutzername · Gruppenname ·
Recovery-Punktbezeichnung · Snapshotname · **lokale Run-ID** · konkrete
Zeitwerte · lokale Protokolle · Personennamen · Secrets · Tokens.

> **Auch eine opake Referenz bleibt lokal.** Eine einzelne opake Kennung
> verrät den Wert nicht, aber ihre Versionierung über mehrere Läufe legt
> **Anzahl, Reihenfolge und Zeitpunkte** realer Instanzen offen. Das ist ein
> Inferenzkanal über die Infrastruktur und daher unzulässig.

**Zulässig in der versionierten Datei:** Felddefinitionen · Wertklassen ·
Semantik und Aussagegrenzen · Stop- und Verfallsbedingungen · abstrakte
Rollen, Pfadklassen, Rechteprofile und Dimensionen · Contract-Testkennungen ·
Decision-, Risk- und ADR-Kennungen · **leere Platzhalter**.

---

## 5 — Pre-run Lifecycle

| Zustand | Bedeutung |
| --- | --- |
| **`INCOMPLETE_FAIL_CLOSED`** | mindestens ein Pflichtfeld oder eine Bindung fehlt — **der Lauf darf nicht beginnen** |
| **`AUTHORIZED_SINGLE_RUN`** | vollständig ausgefüllt und lokal freigegeben — **gültig für genau einen Lauf** |
| **`EXPIRED`** | eine Verfallsbedingung ist eingetreten |
| **`REVOKED`** | die Freigabe wurde vor dem Lauf zurückgezogen |

**Im versionierten Template ist kein Zustand ausgewählt.** Nur eine
vollständig ausgefüllte **lokale** Kopie darf durch den Human Maintainer
**lokal** auf `AUTHORIZED_SINGLE_RUN` gesetzt werden.

---

## 6 — Pflichtfelder AUTH-01 bis AUTH-20

**Genau zwanzig Felder.** Alle sind **zwingend**. Es gibt **kein AUTH-21**.

### 6.1 — Repo-neutrale Bindungen · Wertklasse `REPO_NEUTRAL_BINDING`

| Feld | Feldname | Zweck | Speicherort des Werts | Bindungswirkung | Verfallswirkung |
| --- | --- | --- | --- | --- | --- |
| **AUTH-01** | Work Package und Phase | ordnet den Lauf eindeutig ein | lokale Kopie | bindet an CBP-WP-022 / B2D-E | Änderung der Phase entwertet die Freigabe |
| **AUTH-02** | D-063-Bindung | benennt den Rechtsgrund der Voraussetzungen | lokale Kopie | bindet an das Voraussetzungsmodell | Änderung von D-063 lässt die Freigabe verfallen |
| **AUTH-03** | Repository-HEAD | bindet an einen exakten Codestand | lokale Kopie | macht den Prüfstand nachvollziehbar | jede HEAD-Änderung lässt die Freigabe verfallen |
| **AUTH-04** | Contract-Revision und Contract-Hash | bindet an den geltenden Vertragstext | lokale Kopie | verhindert Vertragsdrift | jede Contractänderung lässt die Freigabe verfallen |
| **AUTH-05** | ADR-0014-Bindung | bindet an die Enforcement-Architektur | lokale Kopie | sichert die Akteursverortung | Änderung von ADR-0014 lässt die Freigabe verfallen |
| **AUTH-06** | exakter Fallumfang | benennt die im Lauf adressierten real-only Kennungen | lokale Kopie | begrenzt den Lauf | jede Änderung des Umfangs lässt die Freigabe verfallen |
| **AUTH-07** | Ausschluss von `KB04-T-P10` und `KB04-T-N25` | hält die beiden Coverage Gaps ausdrücklich außerhalb | lokale Kopie | verhindert eine unbelegte Abdeckungsaussage | Aufnahme eines der beiden ist unzulässig |
| **AUTH-08** | Verfallsbedingungen | benennt die anerkannten Verfallsgründe | lokale Kopie | macht Veralten erkennbar | Eintritt eines Grundes lässt die Freigabe verfallen |
| **AUTH-09** | Stop-Bedingungen | benennt die anerkannten Abbruchgründe | lokale Kopie | erzwingt den Abbruch | Auslösung lässt die Freigabe verfallen |
| **AUTH-10** | Bestätigung, dass **B2D-G nicht gleichzeitig autorisiert** ist | hält Ausführung und Gatearbeit getrennt | lokale Kopie | sichert die Sequenzregel | gleichzeitige B2D-G-Freigabe lässt die Freigabe verfallen |

### 6.2 — Ausschließlich lokale Werte · Wertklasse `LOCAL_ONLY_VALUE`

> Diese vier Werte werden **niemals** versioniert — auch nicht in opaker Form.

| Feld | Feldname | Zweck | Speicherort des Werts | Bindungswirkung | Verfallswirkung |
| --- | --- | --- | --- | --- | --- |
| **AUTH-11** | opake lokale Zielinstanzreferenz | bindet an **genau eine** Instanz | **nur lokal** | verhindert die Übertragung auf einen anderen Host | jede andere Instanz lässt die Freigabe verfallen |
| **AUTH-12** | lokales Startzeitfenster | begrenzt die Gültigkeit zeitlich | **nur lokal** | verhindert die Nutzung einer alten Freigabe | Verstreichen lässt die Freigabe verfallen |
| **AUTH-13** | einmalige lokale Run-ID | macht **genau einen Lauf** identifizierbar | **nur lokal** | **verhindert Wiederverwendung** | mit Laufbeginn verbraucht |
| **AUTH-14** | lokaler Pre-run-Status | hält den Lifecycle-Zustand fest | **nur lokal** | steuert die Startfähigkeit | jeder Zustand außer `AUTHORIZED_SINGLE_RUN` verhindert den Start |

### 6.3 — Versionierte Definition mit lokalem Wert · Wertklasse `VERSIONED_DEFINITION_LOCAL_VALUE`

> Die **Definition** steht hier; der **Wert** entsteht ausschließlich lokal.

| Feld | Feldname | Zweck | Speicherort des Werts | Bindungswirkung | Verfallswirkung |
| --- | --- | --- | --- | --- | --- |
| **AUTH-15** | Bestätigung des **nicht produktiven** Zustands | schließt produktive Instanzen aus | **nur lokal** | mindert **R-35** | Erkennen produktiver Daten lässt die Freigabe verfallen |
| **AUTH-16** | Bestätigung einer **neuen und leeren** Zielstruktur | adressiert die Anforderung aus Contract §9.1 zur neuen und leeren Zielstruktur | **nur lokal** | schließt Bestand und Migration aus | ein nicht leerer Zielbereich lässt die Freigabe verfallen |
| **AUTH-17** | Bestätigung eines **gültigen Recovery-Punkts** | sichert die Rückführbarkeit | **nur lokal** | mindert **R-36** | Ungültigkeit lässt die Freigabe verfallen |
| **AUTH-18** | Bestätigung der **vollständigen lokalen Identitätsbindung** | adressiert die Bindungsanforderungen aus Contract §8 | **nur lokal** | sichert die Rollentrennung | jede Änderung lässt die Freigabe verfallen |
| **AUTH-19** | **Cleanup-Verantwortung** | benennt die Zuständigkeit für Testartefakte | **nur lokal** | sichert die Beseitigung des Verweisobjekts aus `KB04-T-N14` | ungesicherter Cleanup lässt die Freigabe verfallen |
| **AUTH-20** | **Human-Maintainer-Freigabe und Sign-off** | ist die eigentliche Autorisierungshandlung | **nur lokal** | trägt die A0-Ebene der Freigabe | Rücknahme setzt den Zustand auf `REVOKED` |

### 6.4 — Eintragsbereich

> **In der versionierten Datei bleibt dieser Bereich vollständig leer.**
> Ein leerer Eintrag ist **beabsichtigt** und **fail-closed**.

| Feld | Wertklasse | Eintrag |
| --- | --- | --- |
| AUTH-01 | `REPO_NEUTRAL_BINDING` | |
| AUTH-02 | `REPO_NEUTRAL_BINDING` | |
| AUTH-03 | `REPO_NEUTRAL_BINDING` | |
| AUTH-04 | `REPO_NEUTRAL_BINDING` | |
| AUTH-05 | `REPO_NEUTRAL_BINDING` | |
| AUTH-06 | `REPO_NEUTRAL_BINDING` | |
| AUTH-07 | `REPO_NEUTRAL_BINDING` | |
| AUTH-08 | `REPO_NEUTRAL_BINDING` | |
| AUTH-09 | `REPO_NEUTRAL_BINDING` | |
| AUTH-10 | `REPO_NEUTRAL_BINDING` | |
| AUTH-11 | `LOCAL_ONLY_VALUE` | |
| AUTH-12 | `LOCAL_ONLY_VALUE` | |
| AUTH-13 | `LOCAL_ONLY_VALUE` | |
| AUTH-14 | `LOCAL_ONLY_VALUE` | |
| AUTH-15 | `VERSIONED_DEFINITION_LOCAL_VALUE` | |
| AUTH-16 | `VERSIONED_DEFINITION_LOCAL_VALUE` | |
| AUTH-17 | `VERSIONED_DEFINITION_LOCAL_VALUE` | |
| AUTH-18 | `VERSIONED_DEFINITION_LOCAL_VALUE` | |
| AUTH-19 | `VERSIONED_DEFINITION_LOCAL_VALUE` | |
| AUTH-20 | `VERSIONED_DEFINITION_LOCAL_VALUE` | |

**Die Feldkennungen `AUTH-01` bis `AUTH-20` sind dokumentarische
Feldkennungen.** Sie sind **keine** Decision-IDs, **keine** Risk-IDs,
**keine** Control-IDs, **keine** Security-Test-IDs und **keine**
Gate-Kriterien.

---

## 7 — Elf gemeinsame Bindungen

Eine Freigabe ist **nur dann vollständig**, wenn **alle elf** gemeinsam
vorliegen.

| # | Bindung | Herkunft |
| ---: | --- | --- |
| 1 | Repository-HEAD | AUTH-03 |
| 2 | D-063 | AUTH-02 |
| 3 | Contract-Revision und -Hash | AUTH-04 |
| 4 | ADR-0014 | AUTH-05 |
| 5 | exakter Fallumfang | AUTH-06 |
| 6 | Zielinstanzreferenz | AUTH-11 |
| 7 | Recovery-Punktreferenz | AUTH-17 |
| 8 | Identitätsbindungszustand | AUTH-18 |
| 9 | Startzeitfenster | AUTH-12 |
| 10 | einmalige lokale Run-ID | AUTH-13 |
| 11 | Human-Maintainer-Sign-off | AUTH-20 |

**Fehlt eine Bindung:** Zustand **`INCOMPLETE_FAIL_CLOSED`** — **der Lauf darf
nicht beginnen.**

---

## 8 — Maximaler Fallumfang

| Kennung | Gegenstand |
| --- | --- |
| **`KB04-T-N07`** | Retrieval kann Canonical schreiben — **NT-04** |
| **`KB04-T-N08`** | Ingest schreibt Canonical unkontrolliert — **NT-04** |
| **`KB04-T-N14`** | Symlink-Escape — **NT-05**, **Cleanup verpflichtend** |
| **`KB04-T-N31`** | Runtime kann das Artefakt verändern — Dimension **D-III** |
| **`KB04-T-N33`** | Bundlemodus weicht vom sichtbaren Zustand ab — **D-II gegen D-III** |
| **`KB04-T-P12`** | ausschließlich die reale Dimension **D-I** |

**Teilmengen sind zulässig.** **Jede Teilmenge benötigt eine eigene
Freigabe**, weil eine Änderung des Fallumfangs die Freigabe verfallen lässt.
**`KB04-T-N07` und `KB04-T-N08` bleiben getrennte Fälle** — ein einzelner
Schreibversuch belegt nicht beide.

---

## 9 — Ausschluss von KB04-T-P10 und KB04-T-N25

**`KB04-T-P10` und `KB04-T-N25` sind ausgeschlossen.** Beide sind
`SYNTHETIC_COVERAGE_GAP` und betreffen **Contract §10.3
Schreibzeitvalidierung**, die nicht implementiert ist.

Sie dürfen **nicht** in den Fallumfang aufgenommen, **nicht** beobachtet und
**nicht** in einer Aussage über den Lauf geführt werden. **Kein B2D-E-Lauf
schließt Contract §10.3.**

---

## 10 — Stop- und Verfallsbedingungen

Bei **jeder** Bedingung gilt: **die Freigabe verfällt**, der Lauf **darf nicht
beginnen** oder **muss abbrechen**, und **eine neue Freigabe ist
erforderlich**.

| # | Bedingung |
| ---: | --- |
| 1 | Repository-HEAD geändert |
| 2 | Contract geändert |
| 3 | ADR-0014 geändert |
| 4 | D-063 oder D-064 geändert |
| 5 | andere Zielinstanz |
| 6 | anderer Host |
| 7 | Zielstruktur nicht mehr leer |
| 8 | produktive Daten erkannt |
| 9 | Recovery-Punkt nicht gültig |
| 10 | Identitätsbindung geändert |
| 11 | Mountzustand geändert |
| 12 | Fallumfang geändert |
| 13 | Startzeitfenster verstrichen |
| 14 | Cleanup nicht gesichert |
| 15 | B2D-G gleichzeitig autorisiert |
| 16 | **unerwarteter Schreibzugriff erfolgreich** — SB-S04 ist berührt, sofortiger Abbruch |
| 17 | **Symlink-Auflösung nicht sicher blockiert** — sofortiger Abbruch |
| 18 | reale Werte in Repositoryartefakten erkannt |
| 19 | eine Stop-Bedingung wurde bereits ausgelöst |

Ergänzend gilt die Grundregel des Contracts: **nicht feststellbar ist nicht
erfüllt.**

---

## 11 — Einmaligkeit und Verbrauch

| # | Regel |
| --- | --- |
| E-1 | Eine Freigabe gilt für **genau einen Lauf**. |
| E-2 | Eine Freigabe gilt für **genau eine Zielinstanz**. |
| E-3 | Eine Freigabe gilt für **genau einen Fallumfang**. |
| E-4 | Eine Freigabe ist **nicht übertragbar**. |
| E-5 | Eine Freigabe ist **nicht wiederverwendbar**. |
| E-6 | Eine Freigabe wird **mit dem Beginn des Laufs verbraucht**. |
| E-7 | Eine Freigabe **verfällt bei jeder bindungsrelevanten Änderung**. |
| E-8 | **Eine globale oder pauschale Freigabe für mehrere Läufe ist unzulässig.** |

**Keine kryptografische Signatur erforderlich. Keine Schlüsselverwaltung
eingeführt.** Eine lokale Hashbindung lokaler Artefakte bleibt **optional**
und ist **keine Voraussetzung** der Autorisierung.

---

## 12 — Aussagegrenzen

| Nicht belegt | Tatsächlicher Stand |
| --- | --- |
| Ein Lauf sei autorisiert | dieses Template autorisiert **nichts** |
| Eine Profil-A-Instanz existiere | **keine** |
| NT-04 oder NT-05 seien ausgeführt | **nicht ausgeführt** |
| Eine der sechs Kennungen sei bestanden | **keine** |
| Ein Gate sei ausgewertet | beide **`NOT EVALUATED`** |
| Eine Control sei hochgestuft | **KB-04 bleibt `DOCUMENTED ONLY`** |
| SB-S04 sei wirksam | **nicht wirksam** |
| OD-37 sei geschlossen | **offen** |
| Contract §10.3 sei umgesetzt | **technisch offen** |

---

## 13 — Autorisierung ist keine Evidence

**Eine Ausführungsfreigabe ist kein Sicherheitsnachweis.**

**Verbotene Aussagen in diesem Template und in jeder ausgefüllten Kopie:**
„bestanden" · „erfüllt" · „nachgewiesen" · „konform" · „verified" ·
„`operationally_verified`" · „Gate erfüllt" · „Control hochgestuft" ·
„SB-S04 wirksam" · „OD-37 geschlossen" · „Contract §10.3 abgedeckt".

Ein Autorisierungsartefakt **wird zu einem Evidenzartefakt**, sobald es eine
Konformitäts- oder Bestehensaussage zu einer Contract-Testkennung trägt oder
für eine Gate-Verarbeitung aufbereitet ist. **Beides ist hier unzulässig.**

---

## 14 — Pre-run und Post-run strikt getrennt

| Regel |
| --- |
| Das Pre-run-Record wird **nach Laufbeginn nicht ergänzt**. |
| Es enthält **keine Ausführungsergebnisse**. |
| Es enthält **kein Pass/Fail**. |
| Es enthält **keine Contract-Konformitätsaussage**. |
| Es enthält **keine Beobachtung**. |
| Es enthält **keine Cleanup-Bestätigung**. |

Ein späterer **Post-run Operator Record** ist ein **separates lokales
Artefakt**. Er ist **nicht Bestandteil dieses Templates**, wird hier **nicht
definiert** und **nicht erzeugt**; eine versionierte Form benötigte eine
**eigene Freigabe**.

---

## 15 — Do-not-commit

| # | Regel |
| --- | --- |
| C-1 | **Keine ausgefüllte Kopie gelangt in das Repository.** |
| C-2 | **Kein konkreter Run-Wert wird committed** — auch nicht in opaker Form. |
| C-3 | **Keine Zielinstanz, keine Run-ID, keine Recovery-Referenz, keine Zeitangabe, kein Sign-off** wird versioniert. |
| C-4 | Die versionierte Datei bleibt **unverändert leer**, sofern nicht der Feldsatz selbst durch eine neue A0-Decision geändert wird. |
| C-5 | Wird ein realer Wert in einem Repositoryartefakt gefunden, ist das eine **Stop-Bedingung** und die Freigabe verfällt. |

---

## 16 — Fail-closed

| # | Regel |
| --- | --- |
| F-1 | **Ein leeres Pflichtfeld verhindert den Start.** |
| F-2 | **Eine fehlende Bindung verhindert den Start.** |
| F-3 | **Ein nicht feststellbarer Zustand gilt als nicht erfüllt.** |
| F-4 | **Im Zweifel gilt `INCOMPLETE_FAIL_CLOSED`.** |
| F-5 | **Es gibt keinen sicheren Default und keine Fallback-Identität.** |

---

## 17 — Nicht autorisierte Folgeschritte

**Nach D-064 weiterhin nicht autorisiert:** **B2D-E** · **B2D-V** ·
**B2D-G** · **B2D-H** (`NO_HARNESS_REQUIRED`) · **reale Infrastruktur** ·
**B2B-Apply** · **Evidence-Producer** · **Security-Control-Form** ·
**Gate-Eingabe** · **Gateauswertung** · **OD-37-Reconciliation und
-Schließung** · **Contract-§10.3-Implementierung** · **CBP-WP-023**.

**Dieses Template enthält keine ausführbaren Befehle, keine Shell- oder
PowerShell-Kommandos, keine CLI- oder Config-Semantik und keine
maschinenlesbare Autorisierungsstruktur.**

**Ein leeres Formular ist keine Freigabe, und eine Freigabe ist kein
Nachweis.**
