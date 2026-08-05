# CLAUDE.md — Core Brain Pilot

Betriebsanweisung für Implementation Agents in diesem Repository.
Verbindlich nach **Nova Development Framework v1.0.0**.

## Rollenmodell

| Rolle | Verantwortung |
| --- | --- |
| Nova (ChatGPT) | Plant Architektur und Work Packages: Typ, Scope, Akzeptanzkriterien |
| Implementation Agent (Claude Desktop) | Führt **genau ein** freigegebenes Work Package aus und berichtet strukturiert |
| Human Maintainer | Prüft, entscheidet GO / GO WITH NOTES / REWORK / SPLIT / STOP, committet und pusht |

## Lifecycle

```
Classify → Plan → Execute → Report to Nova → Review → Commit
```

Kein Schritt wird ausgelassen.

## Harte Regeln

1. Arbeite ausschließlich innerhalb von `D:\Projects\Core-Brain-Pilot`.
2. Benachbarte Projekte werden weder gelesen noch verändert. Ausdrücklich
   benannte Quelldateien dürfen gelesen werden.
3. Führe nur das aktuell freigegebene Work Package aus.
4. Keine stillschweigenden Scope-Erweiterungen.
5. Keine Commits, Pushes, Remotes oder GitHub-Aktionen ohne ausdrückliche
   Freigabe. Commit-Autorität liegt beim Human Maintainer.
6. Keine Secrets, Zugangsdaten oder privaten Schlüssel erzeugen, lesen,
   speichern oder indexieren — auch keine Beispiel-Secrets.
7. Vor jeder Dateiänderung: Zielpfad prüfen, aktuellen Zustand lesen, Scope
   und erlaubte Dateien prüfen.
8. Bei Konflikten, unklaren Entscheidungen oder fehlender Autorisierung:
   nicht raten, Arbeit sicher anhalten, Blocker melden.
9. Befehle für den Human Maintainer ausschließlich als vollständige
   **PowerShell**-Befehle ausgeben.
10. Keine Bash-, CMD- oder WSL-Anweisungen für den Human Maintainer.
11. Nach jedem Work Package einen strukturierten NDF Implementation Report
    erzeugen.
12. Neue und geänderte Dokumente verwenden **UTF-8 mit echten deutschen
    Umlauten**.

## Autoritätsmodell A0–A6

| Klasse | Quelle |
| --- | --- |
| A0 | Ausdrücklicher Human-Maintainer-Beschluss |
| A1 | Release, Tag oder angenommener ADR |
| A2 | Formeller Projektstatus oder Work-Package-Queue |
| A3 | Freigegebene Roadmap oder Gate-Dokumentation |
| A4 | README und erläuternde Dokumentation |
| A5 | Freigegebene Projektchat-Übergabe |
| A6 | Automatisch abgeleitete Zusammenfassung oder Wiki-Inhalt |

**A6 darf A0 bis A5 niemals automatisch überschreiben.**

Bei Konflikt gewinnt die niedrigere Zahl. Ein Konflikt zwischen gleichrangigen
Quellen wird **nicht** automatisch aufgelöst, sondern dem Human Maintainer
vorgelegt.

### Quellen dieses Projekts

| Quelle | Klasse |
| --- | --- |
| `Bauanleitung_Second-Brain.pdf` | **A4** — Originalquelle, sechs Inhaltsseiten |
| `Second-Brain-Bauanleitung-Textfassung.md` | **A6** — abgeleitete Arbeitsrepräsentation |
| `docs/discovery/Core-Brain-Project-Handoff.md` | **A5** — kanonisch, getrackt |
| Nova Development Framework v1.0.0 | **A1** |
| `docs/decisions/ADR-0001` bis `ADR-0009` | **A1** — angenommen und bindend |

Die A6-Textfassung beansprucht keine höhere Autorität als die A4-PDF.

## Kanonisch vs. abgeleitet

- **Kanonisch** — kuratierter Markdown-Wissensbestand unter Git-Historie.
  Einzige Wahrheitsquelle.
- **Abgeleitet** — Index, Cache, Embeddings, Graph, Web-UI-Zustand.
  Jederzeit reproduzierbar, nie autoritativ, nie in Git.

Der Verlust von Index, Cache, Embeddings, Graph oder Web-UI darf **keinen
Wissensverlust** verursachen.

**Runtime-Daten sind nicht durchgehend abgeleitet** (ADR-0007): **RT-1**
Rebuildable Derived Data ist reproduzierbar · **RT-2 Operational Evidence**
(Audit-, Approval-, Incident- und Restore-Nachweise) ist **nicht**
reproduzierbar und aufbewahrungs- sowie sicherungspflichtig · **RT-3**
Transient Runtime State ist flüchtig und nie alleinige Statuswahrheit.

## Prompt Modes ≠ Context Budgets

Zwei getrennte Konzepte. Die Verwechslung ist als Risiko R-24 erfasst.

### NDF Prompt Modes (A1)

| Modus | Einsatz |
| --- | --- |
| **Full** | Governance-kritische Arbeit: Scope Lock, Architektur, Security, Release, destruktive Aktionen |
| **Standard** | Normale, begrenzte Work Packages und Dokumentationsreviews |
| **Short** | Standardisierte Folgearbeit mit vorhandenem Context Pack |

### Core-Brain Context Budgets (A2)

| Budget | Name | Quellen |
| --- | --- | --- |
| B0 | Micro | 1 Abschnitt |
| B1 | **Lean** | 1 Quelle |
| B2 | Standard | ≤ 3 Quellen |
| B3 | Extended | ≤ 3 Hauptquellen, begründet |
| B4 | Exceptional | begründet, Freigabe vorab |

> **„Lean" ist kein NDF Prompt Mode**, sondern ausschließlich der Name von B1
> (D-009). Vollständig in
> [docs/architecture/CONTEXT_BUDGETS.md](docs/architecture/CONTEXT_BUDGETS.md).

## Brain-First-Suchleiter

1. Index lesen → 2. Quellentyp und Autoritätsklasse bestimmen → 3. Status
prüfen → 4. Wiki nur als abgeleitete Orientierung → 5. Suche auf Collection
begrenzen → 6. Kandidaten über Metadaten prüfen → 7. kleinste ausreichende Zahl
von Quellen öffnen → 8. nur relevante Abschnitte lesen → 9. Fakten,
Ableitungen, Empfehlungen und Unsicherheit trennen → 10. Quellen und Revisionen
nennen.

**Keine blinden Vollscans.**

## Aktueller Zustand

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 – COMPLETE** |
| **Gate G0** | **PASSED WITH NOTES** — 2026-07-21, A0 |
| **Phase 1** | **AUTHORIZED FOR PLANNING** — keine Implementierung freigegeben |
| Aktuelles Work Package | **CBP-WP-022** (`in-review`, **Phase B2D-E-N07-GOV – D-066 Profile-A Retrieval Role Instantiation Boundary**) — **D-057** Registrierung, **D-058** ADR-Gate (**`ADR_REQUIRED`**), **D-059** Architekturannahme und **D-060** Enforcement Contract (**`ADR_NOT_REQUIRED`** innerhalb ADR-0014) — alle `accepted`, **A0**, 2026-08-03; **KB-04 Enforcement Stage 1** = Stufe 1 der neunstufigen Durchsetzungsreihenfolge (**OS-Dateirechte**); **ADR-0014 `accepted`, A1** — **Host-authoritative Enforcement mit deklarativem Zielmodell und read-only Runtime-Validierung**: das Repository hält nur das **abstrakte** Zielmodell, das Deployment setzt Besitz und Rechte **vor** dem Start, die Runtime **prüft ausschließlich und scheitert fail-closed**; **keine Runtime-Komponente verändert jemals Besitz, Gruppe, Modus oder Identität**. **D-060** nimmt den implementierungsfähigen Vertrag [KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md](docs/security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md) an — elf Pfadklassen, zehn Akteure, Rechteprofile **PP-1** bis **PP-4**, Identitätsbindung, vier read-only Validierungszeitpunkte, **24 Fehlerklassen** und zwei **reservierte, nicht implementierte** Exitcodes; **ausführende Reparatur bleibt an RT-2 gebunden und gesperrt**. **B2A implementiert** das interne, **read-only** Enforcement-Paket `core/core_brain/enforcement/` — sechs Module (Contract-Teilmodell, Identitätsbindung, Pfad- und Linkprüfung, Beobachtungsmodelle und Validierung, Befundaggregation) plus **21 additive `KB04-*`-ReasonCodes** in `errors.py`; **206 neue Tests**, Gesamtsuite **930 grün, 0 übersprungen**. **Keine CLI, keine Config-Datei, keine Deploymentänderung, kein neuer Exitcode, keine Mutation** — kein `chmod`, kein `chown`, keine Initialisierung, keine Migration, keine Reparatur. **Beobachtungen sind injiziert und tragen eine explizite Herkunft** (`SYNTHETIC`, `DECLARED`, `OBSERVED`); `operationally_verified` bleibt bei synthetischer oder deklarierter Herkunft **`False`**. **Keine operative KB-04-Evidenz**: NT-04 und NT-05 bleiben unausgeführt, OD-37 offen, beide Gates `NOT EVALUATED`, KB-04 **`DOCUMENTED ONLY`**. B0 `committed` (`e4caa14`), B1A `committed` (`1a7696d`), B1B `committed` (`b86a35f`), B1C `committed` (`24de07e`), B2A `committed` (`929d10b`), B2B-P `committed` (`fff8227`), B2C.1 `committed` (`38eb33f`), B2C.2 `committed` (`117647f`), B2C-T-R `committed` (`9cde9de`), B2D-P `committed` (`b409d25`), B2D-GOV `committed` (`7e8328a`), B2D-AUTH `committed` (`1222ec0`), **B2D-ENV-GOV uncommitted**. **B2B-P ergänzt Plan-only:** `filesystem_adapter.py` (**rein lesendes** `Protocol`, ohne `mkdir`, `open`, `chmod`, `chown`, `unlink`) und `initialization.py` (strikter **Neu-und-leer-Nachweis** N-1/N-2, Bestands-, Teil- und Reparaturklassifikation, deterministisches Planmodell mit **nur** `CREATE_ROOT`, `CREATE_CLASS_DIRECTORY` und `POST_VALIDATE`, Boundary-, Link-, Mount- und **Race-Guards mit Revalidierung**) plus die **drei zuvor reservierten `KB04-*`-ReasonCodes** — damit sind **alle 24 Contract-Fehlerklassen** registriert. **120 neue Tests**, Gesamtsuite **1050 grün, 0 übersprungen**. **Es gibt kein `apply_plan`, kein `mkdir`, kein `chmod`, kein `chown`, kein Löschen und kein Cleanup**; `applicable=True` heißt ausschließlich *nach Contract ausführbar*, **nicht ausgeführt**, und `operationally_verified` ist **immer `False`**. **B2B-Apply bleibt gesperrt** und verlangt eine erneute ADR-Erforderlichkeitsprüfung sowie die Klärung, wo das Setup-Werkzeug lebt. **B2C.0** hat den verbleibenden Phasenzuschnitt read-only geprüft und **`DECISION REQUIRED`** ergeben; **D-061** (`accepted`, **A0**) legt die B2C-Lesart fest: **Variante T** — eine **ausschließlich synthetische** Test-, Fixture- und Rückverfolgbarkeitsphase über die **45** Contract-Testkennungen (**39** synthetisch abdeckbar, **sechs** real-only und damit **B2D**). **Variante E — Security-Control-Form- oder Gate-Evidence-Artefakt — ist für CBP-WP-022 nicht autorisiert**; eine spätere Integration verlangt eine eigene A0-Entscheidung. **Keine Evidence-Producer, keine Gate-Eingabe, kein neues Produktionsmodul, keine CLI, keine Config, kein Deployment, keine neuen ReasonCodes.** **B2C.1 ist `committed` (`38eb33f`).** Der anschließende **B2C-T-Implementierungslauf endete `BLOCKED` — vor jeder Dateiänderung, null geänderte Dateien**: der read-only Audit fand **zwei** als *synthetisch abdeckbar* geführte Kennungen, die **derzeit nicht abgedeckt** sind. **D-062** (`accepted`, **A0**, `B2C_TRACEABILITY_COVERAGE_SPLIT_RECONCILED`, **`ADR_NOT_REQUIRED`**, 2026-08-04) setzt daraufhin die **kanonische Aufteilung der 45 Kennungen** auf **37 `SYNTHETIC_COVERED` · 2 `SYNTHETIC_COVERAGE_GAP` · 6 `B2D_REAL_ONLY`** und führt damit **drei** Dispositionen ein. Die zwei Lücken sind exakt **`KB04-T-P10`** und **`KB04-T-N25`**; beide betreffen **Contract §10.3 Schreibzeitvalidierung**, die weder als Produktionslogik noch als funktionaler Test existiert — **`KB04-WRITE-CONTRACT-VIOLATION`** ist ausschließlich in `errors.py` deklariert. **§10.3 bleibt offen**; eine spätere Implementierung verlangt eine **eigene Scopefreigabe** sowie eine erneute ADR- und Decision-Erforderlichkeitsprüfung. Beide Lücken bleiben **grundsätzlich synthetisch testbar**, sind **keine B2D-Fälle**, behalten ein **leeres `covered_by`** und dürfen **niemals als abgedeckt oder bestanden** ausgegeben werden. **D-061 bleibt unverändert und `accepted`** — D-062 ist **additiv und präzisierend**: *synthetisch abdeckbar ist nicht synthetisch abgedeckt*. **D-062 ist `committed` (`117647f`).** **B2C-T-R implementiert** die Traceability: drei neue Testdateien (`tests/kb04_nt_fixtures.py`, `tests/test_kb04_contract_traceability.py`, `tests/test_kb04_nt_preparation.py`) bilden **alle 45 Contractkennungen vollständig** ab — **37 `SYNTHETIC_COVERED`** mit belegter Zuordnung auf vorhandene funktionale KB-04-Tests, **2 `SYNTHETIC_COVERAGE_GAP`** (`KB04-T-P10`, `KB04-T-N25`) mit leerem `covered_by` und expliziter Gapbeschreibung, **6 `B2D_REAL_ONLY`** mit deklarativen Vorbereitungs-Fixtures (`PREPARED_ONLY`/`NOT_EXECUTED`). **152 neue Tests**, Gesamtsuite **1202 grün, 0 übersprungen**; deterministisches Traceability-Manifest mit stabilem SHA-256. **Kein Produktionscode, keine Änderung vorhandener Tests, keine neue Contract-Testkennung, kein neuer ReasonCode, keine CLI, keine Config, kein Deployment. Keine operative Evidenz**: kein Security-Control-Form-Artefakt, kein Evidence-Producer, keine Gate-Eingabe, keine NT-Ausführung. **Contract §10.3 Schreibzeitvalidierung bleibt technisch offen** — eine Umsetzung verlangt eine eigene Scopefreigabe. **B2C-T-R ist `committed` (`9cde9de`).** **B2D.0** hat den Deployment-Integrationsrahmen **read-only** geprüft (`PASS WITH NOTES`) und **keine Konflikte** gefunden; **B2D-P** legt daraufhin den Plan vor: [KB_04_PROFILE_A_INTEGRATION_PLAN.md](docs/runtime/KB_04_PROFILE_A_INTEGRATION_PLAN.md) — zwanzig Kapitel, **plan-only**, mit fünfstufigem Phasenmodell (**B2D-P** · **B2D-H** · **B2D-E** · **B2D-V** · **B2D-G**), Sequenzregeln (**B2D-E und B2D-G niemals im selben Lauf**), **VM-Referenzvariante** (ein Container ist **nicht** als gleichwertig festgelegt), **Snapshot-/Recovery-Gate als Nova-Ausführungsvoraussetzung** (der Contract gibt **keine** Rollback-Zusage), einer **dreizehnteiligen Precondition-Checkliste** für B2D-E, den sechs real-only Nachweisspezifikationen, **neun Evidenzoptionen ohne Auswahl** und **sechs Risikokandidaten mit Status `RISK_CANDIDATE_NOT_REGISTERED`**. **B2D hängt nicht von B2B-Apply ab** — der Setup-Akteur ist hostseitig und operatorgeführt, außerhalb von Runtime und Repository (ADR-0014); **B2B-Apply bleibt unabhängig gesperrt**. **Reale Infrastruktur nicht autorisiert · B2D-H, B2D-E, B2D-V und B2D-G nicht autorisiert.** **B2D-P ist `committed` (`b409d25`).** **B2D.1** hat Risiken, Harnessbedarf und Freigabemodell **read-only** geprüft (`PASS WITH NOTES`); **B2D-GOV** registriert daraufhin **D-063** (`accepted`, **A0**, `B2D_EXECUTION_PREREQUISITES_ESTABLISHED`, **`ADR_NOT_REQUIRED`**, 2026-08-04): von sechs Risikokandidaten werden **zwei** kanonisch — **R-35** (falsche oder unzureichend isolierte Zielinstanz, integriert die Datenbeschädigung als Auswirkung) und **R-36** (Ausführung ohne bestätigten Wiederherstellungspunkt), beide **hoch** und **offen**; **Kandidat 3 ist durch R-12 abgedeckt**, **R-20 unverändert**, **R-18 bleibt unbenutzt**. Die Harnessfrage ist mit **`NO_HARNESS_REQUIRED`** entschieden — die Erhebung bleibt **hostseitig und operatorgeführt**, der vorhandene Validator verarbeitet Beobachtungen mit Herkunft **`OBSERVED`**, **kein H1, H2 oder H3, keine CLI, kein Script**. **B2D-E bliebe auf die sechs real-only Fälle beschränkt und benötigt keinen Evidence-Producer**; jeder spätere Lauf verlangt eine **einmalige, nicht übertragbare und nicht wiederverwendbare** Freigabe über zehn Bestätigungen — **eine Pauschalfreigabe ist unzulässig**. Die **Risk-Register-Aggregate wurden reconciliiert**: **hoch 20 · mittel 14 · niedrig 1 · Summe 35**, `offen` **13**; die frühere Abweichung ließ sich **nicht allein R-34** zuschreiben. **B2D-GOV ist `committed` (`7e8328a`).** **B2D-E0** hat die Form der per-run Freigabe **read-only** geprüft (`PASS WITH NOTES`); **B2D-AUTH** registriert daraufhin **D-064** (`accepted`, **A0**, `B2D_E_RUN_AUTHORIZATION_ARTIFACT_FORM_SELECTED`, **`ADR_NOT_REQUIRED`**, 2026-08-05) und löst damit die Vertagung aus **D-063 Teil H** ein. Gewählt ist **Variante A1** — **`VERSIONED_EMPTY_TEMPLATE_WITH_LOCAL_FILLED_COPY`**: das neue, **vollständig leere** [KB_04_B2D_E_RUN_AUTHORIZATION_TEMPLATE.md](docs/runtime/KB_04_B2D_E_RUN_AUTHORIZATION_TEMPLATE.md) liegt versioniert im Repository, **jede ausgefüllte Kopie bleibt ausschließlich im lokalen Operator-Workspace** und darf **niemals** zurückkopiert oder committed werden; **leere Pflichtwerte sind beabsichtigt und fail-closed**. Ratifiziert sind **genau 20 Pre-run-Pflichtfelder** **`AUTH-01`** bis **`AUTH-20`** in der Klassifikation **10 repo-neutral · 4 lokal-only · 6 versionierte Definition mit lokalem Wert** — **kein `AUTH-21`**, denn das Post-run-Feld gehört **nicht** zum Pre-run-Record. Eine Freigabe ist erst mit **elf gemeinsamen Bindungen** vollständig, gilt für **genau einen Lauf, eine Zielinstanz und einen Fallumfang**, wird **mit dem Laufbeginn verbraucht** und verfällt bei jeder bindungsrelevanten Änderung; fehlt eine, gilt **`INCOMPLETE_FAIL_CLOSED`**. **Auch opake Zielinstanzreferenz, Run-ID sowie Zeit- und Recovery-Angaben bleiben lokal-only.** **Pre-run und Post-run sind strikt getrennt** — kein Pass/Fail, keine Konformitätsaussage, keine Ergänzung nach Laufbeginn. **Das Template ist keine Freigabe und kein Nachweis.** **B2D-AUTH ist `committed` (`1222ec0`).** **B2D-E1** hat das committete Template **read-only** als reif bewertet (`PASS WITH NOTES`), die sofortige lokale Input Collection aber **noch nicht übernommen**: **`AUTH-03` bindet an den Repository-HEAD**, sodass eine vor dem nächsten Commit angelegte Kopie **unmittelbar verfiele**. **B2D-ENV-GOV** registriert daraufhin **D-065** (`accepted`, **A0**, `B2D_REFERENCE_ENVIRONMENT_PREPARATION_MODEL_SELECTED`, **`ADR_NOT_REQUIRED`**, 2026-08-05) mit dem Modell **`DEDICATED_NON_PRODUCTION_PROFILE_A_VM_WITH_LOCAL_PER_TARGET_APPROVAL`** — eine **dedizierte, nicht produktive Linux/POSIX-VM**, **bestehend oder neu** zulässig, **Container nicht automatisch gleichwertig** (separate A0-Prüfung), **keine konkrete Instanz im Repository benannt oder registriert**. Jede konkrete Auswahl verlangt eine **lokale, nicht übertragbare und nicht versionierte Per-Target-Freigabe**; **neue Identitäten sind nicht automatisch erforderlich**, der Zielbereich **muss neu und leer sein**, und **vor jeder mutierenden Vorbereitung einer bestehenden VM ist ein bestätigter Recovery-Punkt erforderlich** — **der Contract gibt weiterhin keine Rollbackzusage, R-36 bleibt offen**. **Eine lokale Templatekopie darf erst nach dem D-065-Commit entstehen.** **Keine konkrete Referenzumgebung ausgewählt, keine reale Vorbereitung autorisiert, keine lokale Kopie erzeugt.** **B2D-ENV-GOV ist `committed` (`0cd21f5`).** Der read-only Lauf **B2D-PREP-PLAN** und die Korrektur **B2D-PREP-PLAN-N1** haben den target-spezifischen Baselineplan hergeleitet; der anschließende Lauf **B2D-E-N07-PREP** sollte daraus ein Einzellaufpaket für **`KB04-T-N07`** ableiten und endete mit **`N07_IDENTITY_MAPPING_INSUFFICIENT`**: die Contract-Rolle **`retrieval`** besitzt in der gegenwärtigen Profile-A-Ausbaustufe **keine belegte actor-specific Bindung an eine Runtimeidentität** — `deployments/profile-a/**` enthält **null** Fundstellen, das Bundle definiert **genau zwei** Dienste (`control-plane`, `data-worker`), von denen **keiner** ein Retrieval-Dienst ist, `contract.py` führt `RETRIEVAL` als **einzelnes Enum-Mitglied** ohne Bindung, und **beide** Konfigurationsvorlagen setzen `canonical_data = "read-only"` und liefern damit **kein Unterscheidungsmerkmal**. **B2D-E-N07-GOV** registriert daraufhin **D-066** (`accepted`, **A0**, `PROFILE_A_RETRIEVAL_NOT_INSTANTIATED_N07_DEFERRED`, **`ADR_NOT_REQUIRED`**, 2026-08-05), **Variante C**: die abstrakte Rolle **`retrieval` ist derzeit nicht instanziiert** — **weder** als eigenständige Runtimekomponente **noch** als eindeutig gebundene Runtimeidentität — und wird **nicht** auf `control-plane`, `data-worker`, eine Eigentümeridentität oder eine deployment-owned Identität abgebildet. **Variante A** (Zuordnung ohne zusätzliche Governance) ist verworfen, weil keine kanonisch eindeutige Zuordnung vorliegt und die Zuordnung **den Testausgang bestimmt**; **Variante B** (jetzt neue Retrieval-Identität oder -Komponente) ist verworfen wegen vorgezogener Implementierung, der Phase-0-Sperrgrenzen und **R-12**. **`KB04-T-N07` ist zurückgestellt, nicht gescheitert**: der Fall bleibt **`B2D_REAL_ONLY`** mit **unveränderter Traceability-Disposition**; **kein Schreibversuch**, **kein actor-specific Host-Precheck** und **keine lokale N07-Autorisierungskopie** sind autorisiert, **AUTH-14 bleibt für N07 `INCOMPLETE_FAIL_CLOSED`** und **AUTH-20 ungesetzt**. Ein vollständiger N07-Lauf verlangt zusätzlich **D-II** und **D-III**, die **ohne autorisierte Runtime nicht beobachtbar** sind; ein Hostprozess unter einer POSIX-Identität ist **kein vollständiger Ersatz** für eine gebundene Runtimeidentität. **AUTH-18 ist präzise abgegrenzt**: die Bindungen der **bereits instanziierten** Rollen und die **fixturefreie Baseline bleiben gültig und lokal belegbar** — unbelegbar ist AUTH-18 **ausschließlich im N07-spezifischen** Autorisierungsrecord. **Betriebssystembeobachtung und KB-04-ReasonCode bleiben strikt getrennt**: ohne tatsächlichen Validatorlauf darf **kein** ReasonCode als beobachtet behauptet werden, und **D-066 registriert keine Validatorbeobachtung**. **Fünf Reopen-Trigger** sind festgehalten. **`KB04-T-N14`** darf **nach Commit und Reconciliation von D-066** als nächster Planungskandidat **geprüft** werden und ist **nicht autorisiert**. **Keine neue Risiko-ID** — R-12, R-25, R-35 und R-36 decken das Feld ab. **B2D-E weiterhin nicht autorisiert, reale Infrastruktur weiterhin nicht autorisiert.** Keine Ausführung, keine Evidenz, keine Gate-Eingabe, keine OD-37-Schließung. KB-04 bleibt **`DOCUMENTED ONLY`**. **B2B-Apply und B2D nicht autorisiert.** Zuletzt abgeschlossen **CBP-WP-021** (`committed`, `complete`; B0 `0cb4ea9`, B1/B2 `271acc7`, C `0344774`). **CBP-WP-023 nicht registriert, nicht autorisiert** |
| Zuletzt abgeschlossen | **CBP-WP-021** (`committed`, `complete`, 2026-08-03; **D-056**, `ADR_NOT_REQUIRED`; kanonisches Security-Testinventar **32 / 1 / 33**, **0 von 32** und **0 von 1** ausgeführt; B0 `0cb4ea9`, B1/B2 `271acc7`, C `0344774`) |
| **Kanonisches Security-Testinventar** | **32 Negativtests · 1 Positivtest · 33 Testfälle** (D-056, A2-Acceptance-Matrix). **NT-25 ist nicht aktiv** — der Fall ist als **PT-01** klassifiziert, die Nummer bleibt nach Regel **TT-5** bewusst frei. **NT-32 und NT-33 sind gültig** und lösen die frühere Doppelvergabe von NT-23/NT-24 auf; die Matrix-Fälle NT-23 und NT-24 bleiben unverändert aktiv. **Die Zahl 31 ist ein überholter, falsch etikettierter Ableitungswert.** **Ausgeführt: 0 von 32 Negativtests, 0 von 1 Positivtest** — weder die Feststellung eines Inventarwerts noch dessen Reconciliation ist eine Testausführung. **In B1/B2 reconciliiert**, einschließlich `bundle.json`, `validate.py` und der Bundle-Tests |
| **Deployment Readiness (DRC)** | **APPROVED BY HUMAN MAINTAINER** — Profil A, **2026-07-29** (CBP-WP-019, D-054); **19 Prüfpunkte** (17 G0-abgeleitet + 2 ohne G0-Herkunft: DRC-01, DRC-19), **19 `ready`**, **0 `blocked`**; der Gesamtstatus wurde **nicht** automatisch abgeleitet. **Rein dokumentarisch: keine Installation, keine Bereitstellung, keine Betriebs-, Security-, Mapping- oder Capability-Freigabe.** Alle Angaben sind Zusagen des Human Maintainers, keine verifizierten Messwerte |
| Core-Kriterien | 25 von 25 `accepted`, 0 `answered`, 0 `open`, 0 `blocked` |
| Entscheidungen | **66** getroffen, davon **62** mit A0 |
| **R-33** | **19 Konsistenzvorgänge in 22 Work Packages** (`19/22`) — `gemindert, nicht geschlossen`, Kritikalität **mittel**; neunzehnter Vorgang: **D-066-Zählerspiegel-Reconciliation** (CBP-WP-022, B2D-E-N07-GOV, **erstes** R-33-Erfassen von CBP-WP-022), registriert **identisch** in `RISK_REGISTER.md` und `COMPLIANCE_CHECK.md` und **nur einmal gezählt**; achtzehnter Vorgang: kanonisches Security-Testinventar (CBP-WP-021, D-056) |
| Angenommene ADRs | **14** (A1) |
| **Mappingkonvention** | **entschieden** — ADR-0008; **0 Mappings, 0 Quellen, Gate `NOT EVALUATED`** |
| **Sicherheitsgrundlage** | **spezifiziert** — ADR-0009; **12 Kontrollen `DOCUMENTED ONLY`**, Readiness Gate `NOT EVALUATED` |
| **Runtime Skeleton** | **lokal implementiert** (CBP-WP-012) — Python-Standardbibliothek, `run` fail-closed, **nicht produktionsbereit** |
| **Ingest-Quarantäne MVP** | **lokaler Prototyp** (CBP-WP-013, ADR-0010) — synthetic-only, fail-closed, content-addressed Store außerhalb Repo, **keine Promotion**; **nicht produktiv** |
| **Source-Registry MVP** | **lokaler Prototyp** (CBP-WP-014, ADR-0011) — synthetic-only, fail-closed, **deaktiviert**, deterministische Source IDs, unveränderliche Records, append-only Retirement, minimierter Katalog; `activate` verweigert; **nicht produktiv** |
| **Source-Mapping-Draft-Validator MVP** | **lokaler Prototyp** (CBP-WP-015, ADR-0012) — synthetic-only, read-only, fail-closed, **31-Feld-Vertrag** (29 Pflicht + 2 optional), externe read-only Registry-Bindung, `mapping_id` nur validiert, nicht persistierter Report; `activation-check` verweigert; **nicht produktiv** |
| **Mapping-Activation-Gate-Evaluator MVP** | **lokaler Prototyp** (CBP-WP-016, D-050) — synthetic-only, read-only, nicht persistent, fail-closed; **20 Gate-Kriterien**, Ausgabestatus nur `NOT_EVALUATED`/`BLOCKED`; `READY FOR ACTIVATION DECISION`/`APPROVED FOR ACTIVATION`/`REVOKED` **nicht emittierbar**; `activation-evaluate` endet immer `BLOCKED` (Exit 14); Security Foundation/DRC keine Kriterien 21/22; **nicht produktiv** |
| **Synthetic Evidence Contract 2.0 MVP** | **abgelöst durch 3.0** (CBP-WP-017, D-051, `committed` `d3168c4`) — Schema 2.0 wird seit CBP-WP-018 **fail-closed** abgewiesen; D-051 bleibt historisch gültig (A2/B1/E2), C2/D1 abgelöst durch D-052 |
| **Synthetic Evidence Contract 3.0 MVP** | **lokaler Prototyp** (CBP-WP-018, ADR-0013, D-052/D-053, `committed` `5ee2e83`) — synthetic-only, read-only, nicht persistent, fail-closed; Evidence-Schema **3.0** mit eingebetteten strukturierten Artefakten, **`security-control-form` + `control_id`**, Provenance-/Binding-Hashes inkl. Security-Contract-Bindung, deterministische **Invalid-/Stale-/Conflict-Erkennung** (ohne Uhr), **negative-evidence-only** (keine positive Gate-Erfüllung); Schema 1.0 **und 2.0** fail-closed; kein RT-2, keine Persistenz, keine Aktivierung; **558 Tests**, **nicht produktiv** |
| **Security Foundation Readiness Contract MVP** | **lokaler Prototyp** (CBP-WP-018, ADR-0013, D-053, `committed` `5ee2e83`) — statischer, reiner Vertrag (Revision **1.0**) ohne I/O, Uhr, Zufall oder Netz; **12 dokumentierte** Controls, **7 runtime-scoped** Controls, **11 `(criterion, control_id)`-Bindungen**; ausschließlich **synthetische Formprüfung**, rein negative Faltung, Binding-Zähler mit Summeninvariante; **keine** Security-Evaluation, **kein** Enforcement, **keine** Readiness-Aussage; Kriterium 5 Human-only, Kriterium 9 non-security-structural; 12 Kontrollen bleiben `DOCUMENTED ONLY`, Readiness Gate `NOT EVALUATED`; **nicht produktiv** |
| **Profile-A Deployment Bundle** | **Repository-Artefakt, `committed` `9c6c0fb`** (CBP-WP-020, D-055) — **genau sieben Dateien** unter `deployments/profile-a/`; zwei getrennte Service-Identitäten (`svc-control-plane`, `svc-data-worker`), fail-closed Compose- und Konfigurationsvorlagen (Images, UID und GID **ausschließlich** als `${...:?...}`), `read_only`/`cap_drop: ALL`/`no-new-privileges`/kein `privileged`/keine Ports, **genau ein internes Netz**, `canonical-data` beidseitig read-only, `backup-storage` und RT-2 **nicht gemountet**; maschinenlesbare Mount-/Egress-/Secret-/Backup-/RT-2-Verträge in `bundle.json`; **deterministischer Offline-Validator** (stdlib-only, read-only, Exit 0/1/2, byte-identisch); **166 Bundle-Validation-Tests**. Zulässig ausschließlich *repository artifact implemented* · *offline validation implemented* · *offline validation passed*. **Nicht deployed, nicht operational, nicht production-ready**; kein Containerstart, kein Docker-Kommando, kein Netz, keine Secret-Auflösung, kein Backup, kein Restore |
| **Repository-Zielstruktur** | **entschieden** — Ziel-Monorepo (D-029, ADR-0007); **Migration nicht autorisiert**; `deployments/profile-a/` in CBP-WP-020 **rein additiv** angelegt — keine Datei verschoben, umbenannt oder gelöscht |
| **Bereichsmodell** | **W-3** — privater Operator-Workspace außerhalb des Core-Repositorys (D-030); **nicht angelegt** |
| **Veröffentlichung** | Core-Repository `publication-capable by design`, **bleibt privat** — Freigabe benötigt A0 (OD-11) |
| DRC | **APPROVED BY HUMAN MAINTAINER** — Profil A, 2026-07-29; 19 Prüfpunkte, **19 `ready` / 0 `blocked`** (D-054); rein dokumentarisch |
| Benchmark | **entworfen, nicht ausgeführt** (Dataset 2.0.0) |
| Technische Implementierung | **Skeleton + Quarantäne- + Registry- + Mapping-Draft-Validator- + Gate-Evaluator- + Evidence-3.0-/Security-Contract-Prototyp lokal** (CBP-WP-012/013/014/015/016/017/018) **+ Profil-A-Deployment-Bundle als offline validiertes Repository-Artefakt** (CBP-WP-020) — keine KB-Kontrolle durchgesetzt, keine Quelle angebunden, kein Mapping gespeichert, kein Gate ausgeführt, keine Security evaluiert, **nichts bereitgestellt**, nichts aktiviert |
| Implementierte Capabilities | **keine (0 von 29)** — lokale Bausteine belegt; **Capability 2/3/5/6/7 bleiben nicht vollständig `implemented`** |

> **Criteria complete ≠ Technical implementation ≠ Deployment ready.**
> G0 sperrt den Produkt- und Pilot-Scope. **16 der 25 Kriterien beschreiben
> Kontrollen, die nicht existieren.** Die Freigabe autorisiert ausschließlich
> die **Planung** von Phase 1 — siehe
> [docs/roadmap/PHASE_1_BACKLOG.md](docs/roadmap/PHASE_1_BACKLOG.md).

## Sperrliste Phase 0

25 gesperrte Gegenstände, verbindlich in
[docs/product/DO_NOT_START.md](docs/product/DO_NOT_START.md).

Kurzfassung: produktive Implementierung, Docker Compose, Web-UI,
Suchintegration, Wiki-Ingest, Knowledge Graph, Obsidian-Synchronisation,
MCP-Integration, externe Connectoren, automatisierte Commits, öffentliches
Branding, Kubernetes, Multi-Tenant, SaaS, Proxmox-API-Integration, neue
NDF-Skills, CDF-, CoreOps- und CDS-Integration, öffentliche Cloudinstanz.

Superpowers darf als Referenz untersucht, aber **nicht** als zweites
Governance-System eingeführt werden.
