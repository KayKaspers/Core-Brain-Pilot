# Project Brain – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Überarbeitet in | **CBP-WP-016** |
| Autoritätsklasse | A2 |
| Stand | 2026-07-22 |

Kuratiertes Projektgedächtnis und Einstiegspunkt für jede neue Sitzung. Dieses
Dokument **verweist**, statt Inhalte zu duplizieren.

## Projektstatus

**Phase 0 – COMPLETE.** G0 am 2026-07-21 als **PASSED WITH NOTES** freigegeben (A0). Phase 1 ist **AUTHORIZED FOR PLANNING**.

Das Repository enthält Dokumentation, seit CBP-WP-012 einen **lokalen,
fail-closed Foundation Runtime Skeleton** und seit CBP-WP-013 einen **lokalen,
synthetisch testbaren Ingest-Quarantäneprototyp** (beide
Python-Standardbibliothek). **Keine operative Wirkung:** keine angebundene
Quelle, kein Index, kein Wissensbestand, keine durchgesetzte
Sicherheitskontrolle, keine Promotion. `run` und `quarantine release`
verweigern deterministisch.

| Feld | Wert |
| --- | --- |
| Aktuelles Work Package | **CBP-WP-022** (`in-review`, **Phase B2D-ENV-GOV – D-065 Profile-A Reference Environment Preparation Model**) — **D-057** Registrierung, **D-058** ADR-Gate (**`ADR_REQUIRED`**), **D-059** Architekturannahme und **D-060** Enforcement Contract (alle `accepted`, **A0**, 2026-08-03); **ADR-0014 `accepted`, A1** — **Host-authoritative Enforcement mit deklarativem Zielmodell und read-only Runtime-Validierung**. Wesentliche Konsequenzen: die Runtime benötigt **keinerlei Rechteprivilegien** und ist mit **V-1**, **V-3**, `cap_drop: ALL` und `read_only` vereinbar; **keine realen UID-, GID-, Benutzer- oder Gruppenwerte im Repository**; eine Rechteabweichung führt zur **Startverweigerung statt Selbstheilung** und bleibt für **NT-04/NT-05** sichtbar; **Reparatur nur ausdrücklich, geplant und auditiert** — und ist mangels **RT-2** bis auf Weiteres **nicht freigegeben**. **D-060 finalisiert die Contract Boundary** in [KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md](../docs/security/KB_04_STAGE_1_ENFORCEMENT_CONTRACT.md): **elf Pfadklassen PC-01 bis PC-11** an den bereits committeten Bundle-Containerpfaden · **zehn Akteure** mit zwölf Befugnisspalten · **Rechteprofile PP-1 `0600`/`0700`, PP-2 `0640`/`0750`, PP-3a `0640`/`0750`, PP-3b `0444`/`0555` (**eng begrenztes Kompatibilitätsprofil, nur PC-07, secretfrei, ausdrückliche Ausnahme statt sicherer Default**) und PP-4 *not-present*** mit `umask` `0077` beziehungsweise `0027` · **Identitätsbindungsvertrag** mit elf Feldern, ohne Default, ohne Ableitung, ohne Fallback · **Initialisierung strikt getrennt von Bestandsmigration** · **vier read-only Validierungszeitpunkte** · **24 Fehlerklassen `KB04-*`** · **vier getrennte Prüfdimensionen** D-I Host, D-II Mount, D-III Runtimeobjekt und D-IV Identität — der Bundlemodus belegt die Host-Quellrechte nicht · **Test- und Evidenzplan** mit zwölf positiven und dreiunddreißig negativen Fällen, synthetisch und real getrennt · **Reparatur an RT-2 gebunden und gesperrt**. **B2A implementiert** das interne, read-only Enforcement-Paket `core/core_brain/enforcement/` in **sechs Modulen**: `contract.py` (elf Pfadklassen, fünf Profilausprägungen, zehn Akteure, vier Dimensionen, Dokument- und Modellhash gegen Drift), `binding.py` (Identitätsbindung mit zehn Pflichtfeldern, ohne Auflösung realer Identitäten, ohne Default und ohne Fallback), `paths.py` (Root-Boundary, Symlink- und Hardlinkablehnung, Objektartklassifikation, dokumentierte TOCTOU-Grenze), `validator.py` (injizierbare Beobachtungsmodelle für **D-I bis D-IV** und die read-only Prüfungen) und `aggregate.py` (Befunde, fail-closed Faltung, deterministische Serialisierung) sowie **21 additive `KB04-*`-ReasonCodes**. **Entscheidend ist die Trennung von logischer und operativer Konformität:** jede Beobachtung trägt eine explizite Herkunft — `SYNTHETIC`, `DECLARED` oder `OBSERVED` —, und `operationally_verified` wird **nur** bei durchgängig beobachteter Herkunft wahr. **PP-3b bleibt eng begrenzt**: nur PC-07, mit deklarativer Inhaltsklassifikation; `UNCLASSIFIED` und eine fehlende Klassifikation sind **`INDETERMINATE`**, `SENSITIVE_OR_SECRET` ist eine **Verletzung** — es gibt **keinen Default auf secret-free** und **keine Inhaltsanalyse**. **Keine Mutation**: kein `chmod`, kein `chown`, keine Initialisierung, Migration oder Reparatur. **Offen bleiben die realen Deploymentgrenzen** — reale Containeridentität, reale Supplementary Groups, tatsächlicher Mountmodus, reale Schreibfähigkeit, **NT-04**, **NT-05**, Nachweisstufe 4, **OD-37** und Gate-Evidenz. **KB-04 Enforcement Stage 1** bleibt **`DOCUMENTED ONLY`**; B0 `committed` `e4caa14`, B1A `committed` `1a7696d`, B1B `committed` `b86a35f`, B1C `committed` `24de07e`, B2A `committed` `929d10b`, B2B-P uncommitted. **B2B-P ergänzt Plan-only**: `filesystem_adapter.py` ist ein **rein lesendes** `Protocol` — `mkdir`, `open`, `chmod`, `chown` und `unlink` existieren dort nicht einmal als Methode. `initialization.py` implementiert die **Neu-und-leer-Definition** mit genau zwei zulässigen Ausgangszuständen (**N-1** Root fehlt, **N-2** Root ist Verzeichnis mit **null** Einträgen, versteckte eingeschlossen), das **Boundary- und Planmodell** (opaker `target_ref`, ausschließlich relative Pfade, kein absoluter Pfad in `to_dict()`, pfadfreier Request-Digest), die **Bestandsklassifikation** (`ALREADY_INITIALIZED` · `PARTIAL` · `MIGRATION_REQUIRED` · `REPAIR_REQUIRED` · `INDETERMINATE` · `BLOCKED`) sowie **Race-Guards mit ausdrücklicher Revalidierung**: weicht der Zustand zwischen zwei Beobachtungen ab, ist das Ergebnis `KB04-STATE-INDETERMINATE` und **niemals** ein anwendbarer Plan. **Keine Mutation**: es gibt kein `apply_plan`, keinen `mkdir`-Aufruf, kein `chmod`, kein `chown`, kein Löschen und kein Cleanup; `operationally_verified` ist **immer `False`**. **Die ADR-Frage für Apply bleibt offen** — ADR-0014 verortet die Durchsetzungsschicht außerhalb der Runtime und außerhalb des Repositorys; wo das Setup-Werkzeug lebt, ist ungeklärt. **B2C.0** hat den verbleibenden Phasenzuschnitt read-only geprüft: Der Contract definiert **B2C** an genau einer Stelle als *„Synthetic Tests and Evidence · Unit- und Contract-Tests · negative Fixtures · Vorbereitung von NT-04/NT-05 · keine reale Deploymentausführung“*. Zwei dieser drei Punkte waren bereits geliefert, und **„Evidence“ war nicht definiert** — daher **`DECISION REQUIRED`**. **D-061** (`accepted`, **A0**) wählt **Variante T**: die **45** Contract-Testkennungen `KB04-T-P01…P12` und `KB04-T-N01…N33` bilden die **Traceability-Basis**; **39** Fälle sind synthetisch abdeckbar, **sechs** sind ausschließlich real ausführbar und bleiben **B2D**: `KB04-T-N07` und `KB04-T-N08` (**NT-04**), `KB04-T-N14` (**NT-05**), `KB04-T-N31`, `KB04-T-N33` sowie die reale Dimension **D-I** von `KB04-T-P12`. **Variante E** — ein Security-Control-Form- oder Gate-Evidence-Artefakt — ist **nicht autorisiert**, damit die **Eingabefläche des Gate-Evaluators** nicht als Nebenwirkung einer Testphase erweitert wird; KB-04 trägt dort die Bindungen **(7, KB-04)**, **(8, KB-04)** und **(11, KB-04)**. **Evidence- und Gategrenze:** B2C darf synthetische Unit-, Contract- und statische Integrationsnachweise liefern, aber **keine** reale Linux-/POSIX- oder Profil-A-Evidenz; **eine Vorbereitung ist kein Nachweis, ein Fixture keine NT-Ausführung, eine synthetische Abdeckung keine operative Evidenz**. **Keine Implementierungsfreigabe für B2C-T, B2B-Apply oder B2D.** **B2C.1 ist `committed` (`38eb33f`).** Der erste **B2C-T-Implementierungslauf endete `BLOCKED` — vor jeder Dateiänderung, null geänderte Dateien**, weil der read-only Audit **zwei** als *synthetisch abdeckbar* geführte Kennungen fand, die **derzeit nicht abgedeckt** sind. **Die tragende Unterscheidung lautet: *synthetisch abdeckbar* ist nicht *synthetisch abgedeckt*.** *Abdeckbar* ist eine Aussage über die **Prüfbarkeit im Grundsatz**, *abgedeckt* eine Aussage über einen **tatsächlich existierenden funktionalen Test**; D-061 Teil E verwendete bewusst den ersten Begriff, der B2C-T-Prompt las ihn als den zweiten. **D-062** (`accepted`, **A0**, `B2C_TRACEABILITY_COVERAGE_SPLIT_RECONCILED`, **`ADR_NOT_REQUIRED`**, 2026-08-04) führt daraufhin **drei Dispositionen** ein — **`SYNTHETIC_COVERED`**, **`SYNTHETIC_COVERAGE_GAP`** und **`B2D_REAL_ONLY`** — mit dem kanonischen Split **37 / 2 / 6** über unverändert **45** Kennungen. Die zwei Lücken sind exakt **`KB04-T-P10`** (atomare Ersetzung, temporäres Objekt im gleichen Schreibkontext) und **`KB04-T-N25`** (temporäres Objekt außerhalb des Kontexts, `KB04-WRITE-CONTRACT-VIOLATION`). Beide gehören zu **Contract §10.3 Schreibzeitvalidierung** — der **offenen technischen Grenze** dieses Enforcement-Stands: es existiert **keine Schreibzeitvalidierungsfunktion**, **keine Prüfung atomarer Ersetzung**, **keine Prüfung des temporären Schreibkontexts** und **kein produktiver Verwendungsort** des ReasonCodes, der ausschließlich in `errors.py` deklariert ist. Beide bleiben **grundsätzlich synthetisch testbar** und sind **keine B2D-Fälle**; `covered_by` bleibt **leer**, eine Gapbeschreibung ist **verpflichtend**, und eine Zuordnung zu benachbarten Root-Boundary-Tests ist **unzulässig** — sie prüfen einen anderen Gegenstand mit einem anderen ReasonCode. **Es wird keine falsche Abdeckungsbehauptung erzeugt: eine dokumentierte Lücke ist keine Bestehensaussage, und eine vollständige Matrix ist keine vollständige technische Abdeckung.** **D-061 bleibt unverändert und `accepted`**; D-062 ist **additiv und präzisierend** und ist `committed` (`117647f`). **Phase B2C-T-R setzt das Traceability-Modell technisch um.** Drei neue Dateien — `tests/kb04_nt_fixtures.py`, `tests/test_kb04_contract_traceability.py` und `tests/test_kb04_nt_preparation.py` — bilden **alle 45** Contractkennungen mit den **drei Dispositionen** ab: **37 `SYNTHETIC_COVERED`** sind auf vorhandene funktionale KB-04-Tests der sechs zulässigen Module abgebildet, jede referenzierte Kennung ist vollständig qualifiziert und wird gegen das reale Testinventar geprüft; Mehrfachzuordnungen sind im `coverage_note` begründet. **2 `SYNTHETIC_COVERAGE_GAP`** — `KB04-T-P10` und `KB04-T-N25` — tragen ein **leeres `covered_by`**, eine verpflichtende Gapbeschreibung mit **Contract §10.3** und, bei N25, den ReasonCode `KB04-WRITE-CONTRACT-VIOLATION`; für P10 wird **kein ReasonCode erfunden**. Eine Ersatzzuordnung zu Root-Boundary-Tests ist ausgeschlossen, und ein eigener Test belegt, dass **keine unverneinte Abdeckungs- oder Bestehensbehauptung** im Text steht. **6 `B2D_REAL_ONLY`** sind rein deklarativ vorbereitet — `PREPARED_ONLY`/`NOT_EXECUTED`, Vorbereitung `SYNTHETIC`, spätere Ausführung `OBSERVED` auf einer Profil-A-Instanz; die Modelle besitzen **kein Feld `passed`, `conform` oder `operationally_verified`**. **P12 bleibt die Sondergrenze**: die Kennung ist real-only, weil allein die **Dimension D-I** eine reale Instanz verlangt; die synthetischen Vorprüfungen stehen ausschließlich unter `synthetic_support_tests` und **niemals** unter `covered_by`. **152 neue Tests**, Gesamtsuite **1202 grün, 0 übersprungen**; das Traceability-Manifest ist kanonisch sortiert und byte-stabil. **Keine operative Evidenz**: kein Security-Control-Form-Artefakt, kein Evidence-Producer, keine Gate-Eingabe, keine NT-Ausführung, kein Produktionscode. **Contract §10.3 bleibt die offene technische Grenze.** **Phase B2D-P legt das B2D-Phasenmodell fest**: **B2D-P** (Planung, autorisiert) · **B2D-H** (optionaler operator-geführter Harness) · **B2D-E** (reale Ausführung) · **B2D-V** (read-only Verifikation und Anonymisierung) · **B2D-G** (Gate- und OD-37-Reconciliation) — die letzten vier **nicht autorisiert**. Verbindlich: **B2D-P muss committed und geprüft sein, bevor eine Folgephase erwogen wird**, **B2D-E und B2D-G dürfen niemals im selben Lauf stattfinden**, und **B2D-E löst keinen automatischen Übergang** aus. **B2D ist von B2B-Apply unabhängig**: ADR-0014 verortet den **Setup-Akteur hostseitig und operatorgeführt, außerhalb von Runtime und Repository**, und erlaubt ihm, Besitz und Rechte **initial herzustellen**; die Runtime bleibt **strikt read-only**, es gibt **kein `apply_plan`**, und ein mutierender Repo-Helfer wäre dieselbe Grenzverletzung unter anderem Namen — **B2B-Apply bleibt unabhängig gesperrt**. Als Referenzumgebung ist ausschließlich eine **dedizierte, nicht produktive VM** geplant; **ein Container ist nicht als gleichwertiger Ersatz festgelegt**, weil die getrennte Feststellbarkeit von **D-I gegenüber D-III** von der verfügbaren Host- und Mountsicht abhängt — Contract §7.1 führt dies ausdrücklich als offenen Punkt der realen Deployment-Evidenz. Für Evidenz gilt eine **Sequenzbedingung**: Contract §18 nennt „Gate-Evidenz" im B2D-Scope, **D-061 Teil O** bindet deren Integration jedoch an eine **eigenständige A0-Entscheidung**, weil KB-04 runtime-scoped ist und die Gate-Eingabefläche berührt würde; nach **ADR-0013** wäre ein solches Artefakt zudem **negative-evidence-only** und könnte ein Gate nur blockieren, nie freigeben. **Gate und OD-37 bleiben strikt getrennt**: B2D bereitet Nachweise vor, wertet **kein** Gate aus, setzt **kein** PASS, hebt **keine** Control hoch, setzt **SB-S04 nicht wirksam** und **schließt OD-37 nicht** — OD-37 verlangt zusätzlich einen **KB-03-Anteil**, reale Ziel-Instanz-Nachweise, einen **RT-2-nahen Auditeintrag**, eine separate Reconciliation und eine separate A0-Decision. **Phase B2D-GOV kanonisiert die Ausführungsvoraussetzungen** über **D-063** (`accepted`, **A0**, `B2D_EXECUTION_PREREQUISITES_ESTABLISHED`, **`ADR_NOT_REQUIRED`**). **Zwei neue kanonische Risiken:** **R-35** — *reale KB-04-Nachweisausführung trifft eine falsche oder unzureichend isolierte Zielinstanz* — bündelt vier der sechs B2D-P-Kandidaten und führt die **Beschädigung realer Daten als Auswirkung**, nicht als eigenen Auslöser; **R-36** — *Ausführung ohne bestätigten Wiederherstellungspunkt* — verankert das **Recovery-Gate R-1 bis R-4**, obwohl der Contract in §9.3 **keine Rollbackzusage** gibt. Beide sind **hoch** und **offen**. **Kandidat 3 — Umgehung der B2B-Apply-Grenze — ist durch R-12 vollständig abgedeckt** (Sperrliste, Aufhebung nur per A0) und erhielt **keine eigene ID**; **R-20 wurde nicht erweitert**, **R-18 bleibt eine nicht wiederverwendete Nummernlücke**. **Die Harnessfrage ist mit `NO_HARNESS_REQUIRED` entschieden**, und zwar aus der Architektur heraus: die **Erhebung** ist nach ADR-0014 **hostseitig und operatorgeführt**, die **Validierung** existiert bereits — `validate_observation()` nimmt injizierte Beobachtungen mit Herkunft **`OBSERVED`** entgegen —, sodass **kein Repositorybaustein fehlt**; **kein H1, H2 oder H3, keine CLI, kein Script, kein durch das Repository definiertes externes Werkzeug**. Ein optionaler späterer H1-Testhelper verlangt eine eigene Freigabe. **Das Freigabemodell ist per-run**: **D-063 autorisiert keinen Lauf**; jeder spätere B2D-E-Lauf verlangt zehn Bestätigungen und eine **einmalige, nicht übertragbare und nicht wiederverwendbare** Freigabe, die bei anderer Instanz, anderem Strukturzustand, geänderter Bindung, geändertem Fallumfang, ausgelöster Stop-Bedingung oder Änderung von Contract, ADR-0014 oder D-063 **verfällt**; **eine globale Pauschalfreigabe ist unzulässig**. **Keine Producer- oder Gatekopplung**: B2D-E benötigt **keinen Evidence-Producer**, lokale Formen bleiben **lokal-only** und sind **keine Gate-Eingabe**. Die **Risk-Register-Aggregate** wurden auf **hoch 20 · mittel 14 · niedrig 1 · Summe 35** reconciliiert; die frühere Abweichung zerfiel in **zwei unabhängige Fehler** und war **nicht allein R-34** zuzuschreiben. **Phase B2D-AUTH legt mit D-064** (`accepted`, **A0**, `B2D_E_RUN_AUTHORIZATION_ARTIFACT_FORM_SELECTED`, **`ADR_NOT_REQUIRED`**) **die Form der per-run Autorisierung fest** und löst damit die Vertagung aus D-063 Teil H ein. **Gewählt ist Variante A1** — **`VERSIONED_EMPTY_TEMPLATE_WITH_LOCAL_FILLED_COPY`**: im Repository liegt ein **vollständig leeres Template**, **jede ausgefüllte Kopie bleibt im lokalen Operator-Workspace** und darf niemals zurückkopiert oder committed werden; **leere Pflichtwerte sind beabsichtigt und fail-closed**. **Genau 20 Pre-run-Pflichtfelder** `AUTH-01` bis `AUTH-20` sind ratifiziert, klassifiziert als **10 `REPO_NEUTRAL_BINDING` · 4 `LOCAL_ONLY_VALUE` · 6 `VERSIONED_DEFINITION_LOCAL_VALUE`** — **kein `AUTH-21`**, weil das Post-run-Feld nicht zum Pre-run-Record gehört. **Die einmalige lokale Run-ID** ist das Element, das „genau ein Lauf" überhaupt identifizierbar macht; sie bleibt ebenso **lokal-only** wie die **opake Zielinstanzreferenz**, deren Versionierung über mehrere Läufe **Anzahl, Reihenfolge und Zeitpunkte** realer Instanzen offenlegte. Eine Freigabe ist erst mit **elf gemeinsamen Bindungen** vollständig — fünf repo-neutrale (HEAD, D-063, Contract-Revision und -Hash, ADR-0014, Fallumfang) und sechs lokale (Zielinstanz, Recovery-Punkt, Identitätsbindung, Startzeitfenster, Run-ID, Sign-off); fehlt eine, gilt **`INCOMPLETE_FAIL_CLOSED`** und der Lauf darf nicht beginnen. **Pre-run und Post-run sind strikt getrennt**: das Record wird nach Laufbeginn **nicht ergänzt** und trägt **kein Pass/Fail, keine Konformitätsaussage, keine Beobachtung und keine Cleanup-Bestätigung**; ein Post-run Operator Record ist ein **separates lokales Artefakt** außerhalb dieses Work Packages. **Kein Evidence- oder Gate-Effekt**: das Template ist weder Evidenz noch Gate-Eingabe, und **eine Ausführungsfreigabe ist kein Sicherheitsnachweis**. **Phase B2D-ENV-GOV wählt mit D-065** (`accepted`, **A0**, `B2D_REFERENCE_ENVIRONMENT_PREPARATION_MODEL_SELECTED`, **`ADR_NOT_REQUIRED`**) **das Referenzumgebungsmodell**: **`DEDICATED_NON_PRODUCTION_PROFILE_A_VM_WITH_LOCAL_PER_TARGET_APPROVAL`** — eine **dedizierte, nicht produktive Linux/POSIX-VM**, die ausschließlich der KB-04-Profile-A-Vorbereitung dient. **Eine bestehende isolierte VM darf verwendet werden, eine neue darf, muss aber nicht**; **ein Container gilt für den ersten Profile-A-Realnachweis nicht automatisch als gleichwertig** und verlangt eine **separate A0-Prüfung**. **Keine konkrete VM wird im Repository benannt oder registriert.** **Die lokale Per-Target-Freigabe** ist der Kern des Modells: jede konkrete Auswahl verlangt eine ausdrückliche Human-Maintainer-Freigabe mit Bindung an **genau eine** Instanz, Bestätigung des nicht produktiven Charakters, der Isolation und der Unberührtheit produktiver Daten sowie eine festgelegte Cleanup-Verantwortung — sie ist **keine kanonische Decision**, **wird nicht versioniert**, **bleibt vollständig lokal** und ist **nicht übertragbar**. **Identitätsgrenze:** **neue Benutzer oder Gruppen sind nicht automatisch erforderlich**; vorhandene, dedizierte und hinreichend isolierte Identitäten dürfen verwendet werden, neue nur, wenn die vorhandenen die Contract-Anforderungen nicht erfüllen können — konkrete UID-, GID- und Namenswerte bleiben lokal. **Recovery-Grenze:** bei einer **neu angelegten, disponiblen** VM darf ein reproduzierbarer Basis- oder Clone-Zustand als Grundlage gelten, bei einer **bestehenden** VM ist **vor jeder mutierenden Vorbereitung** ein bestätigter Recovery-Punkt erforderlich; **der Contract gibt weiterhin keine Rollbackzusage, und R-36 bleibt offen**. **Reihenfolge nach dem Commit:** D-065 committen → lokale Referenzumgebung auswählen → Nova erhält nur die planungsnotwendigen lokalen Angaben → target-spezifischer Vorbereitungsplan → ausdrückliche Human-Maintainer-Freigabe → erst dann reale Vorbereitung → `AUTH-15` bis `AUTH-18` nach wahrheitsgemäßer Prüfung → `AUTH-12` und `AUTH-20` zuletzt → **B2D-E verlangt weiterhin eine separate Freigabe**. **Eine lokale Templatekopie darf erst nach dem D-065-Commit entstehen**, weil `AUTH-03` an den Repository-HEAD bindet. **B2B-Apply und B2D nicht autorisiert.** Zuletzt abgeschlossen **CBP-WP-021** (`committed`, `complete`; B0 `0cb4ea9`, B1/B2 `271acc7`, C `0344774`). **CBP-WP-023 nicht registriert, nicht autorisiert** |
| Zuletzt abgeschlossen | **CBP-WP-021** (`committed`, `complete`, 2026-08-03; **D-056**; kanonisches Security-Testinventar **32 / 1 / 33**, **0 von 32** und **0 von 1** ausgeführt; B0 `0cb4ea9`, B1/B2 `271acc7`). Zuvor abgeschlossen **CBP-WP-020** (`committed`, `complete`; **D-055**; **Z1 erreicht / S2 abgeschlossen / P1 eingehalten**; B0 `17057e2`, B1/B2 `9c6c0fb`, C `d6a1a3c`). **CBP-WP-023 nicht registriert, nicht autorisiert** |
| Gate G0 | **PASSED WITH NOTES** — 2026-07-21 |
| G0-Kriterien | **47**, dreistufig klassifiziert |
| davon blockierend | **25** Core Required (zuvor 45) |
| davon `accepted` | **25** — alle |
| verbleibende Blocker | **0** |
| Phase 1 | AUTHORIZED FOR PLANNING — [Backlog](../docs/roadmap/PHASE_1_BACKLOG.md), [Foundation Plan](../docs/roadmap/PHASE_1_FOUNDATION_PLAN.md) |
| Geplante Work Packages | **CBP-WP-022** `in-review` (D-057 Registrierung, D-058 ADR-Gate, **D-059** Architekturannahme, **D-060** Enforcement Contract; **Phase B2B-P**, B0 `committed` `e4caa14`, B1A `committed` `1a7696d`, B1B `committed` `b86a35f`, B1C `committed` `24de07e`, B2A `committed` `929d10b`, B2B-P uncommitted; **ADR-0014 `accepted`/A1**, **Host-authoritative Enforcement mit deklarativem Zielmodell und read-only Runtime-Validierung**; Vertrag `accepted contract`; **B2 nicht autorisiert**). **CBP-WP-021** ist `committed` und `complete` (D-056; B0 `0cb4ea9`, B1/B2 `271acc7`). **CBP-WP-020** ist `committed` und `complete` (D-055; B0 `17057e2`, B1/B2 `9c6c0fb`, C `d6a1a3c`), B3 **ausgeschlossen**; CBP-WP-019 ist `committed` (`3c437f2`, D-054). **CBP-WP-023 nicht registriert, nicht begonnen, nicht autorisiert** — das KB-04-Paket ist lediglich als möglicher Kandidat vorgemerkt |
| **Repository-Struktur** | **entschieden** — Ziel-Monorepo + Workspace W-3 (ADR-0007); **Migration nicht autorisiert** |
| **Mappingkonvention** | **entschieden** — ADR-0008; **0 Mappings, 0 Quellen**, Gate `NOT EVALUATED` |
| **Sicherheitsgrundlage** | **spezifiziert** — ADR-0009; **12 Kontrollen `DOCUMENTED ONLY`** |
| **Runtime Skeleton** | **lokal implementiert** (CBP-WP-012) — `run` fail-closed, nicht produktionsbereit |
| **Ingest-Quarantäne MVP** | **lokaler Prototyp** (CBP-WP-013, ADR-0010) — synthetic-only, fail-closed, keine Promotion, nicht produktiv |
| **Source-Registry MVP** | **lokaler Prototyp** (CBP-WP-014, ADR-0011) — synthetic-only, fail-closed, **deaktiviert**, `activate` verweigert, nicht produktiv |
| **Source-Mapping-Draft-Validator MVP** | **lokaler Prototyp** (CBP-WP-015, ADR-0012) — synthetic-only, read-only, fail-closed, **31-Feld-Vertrag** (29+2), externe read-only Registry-Bindung, `mapping_id` nur validiert, `activation-check` verweigert, nicht produktiv |
| **Mapping-Activation-Gate-Evaluator MVP** | **lokaler Prototyp** (CBP-WP-016, D-050) — synthetic-only, read-only, nicht persistent, fail-closed; **20 Gate-Kriterien**, Ausgabestatus nur `NOT_EVALUATED`/`BLOCKED`; `activation-evaluate` endet immer `BLOCKED` (Exit 14); nicht produktiv |
| **Synthetic Evidence Contract 3.0 MVP** | **lokaler Prototyp** (CBP-WP-018, ADR-0013, D-052/D-053, `committed` `5ee2e83`) — Evidence-Schema 3.0 mit eingebetteten Artefakten, `security-control-form` + `control_id`, Provenance-/Binding-Hashes inkl. Security-Contract-Bindung, deterministische Invalid-/Stale-/Conflict-Erkennung, **negative-evidence-only**; Schema 1.0 **und 2.0** fail-closed; kein RT-2/Persistenz/Aktivierung; **558 Tests**, nicht produktiv |
| **Security Foundation Readiness Contract MVP** | **lokaler Prototyp** (CBP-WP-018, ADR-0013, D-053, `committed` `5ee2e83`) — statischer, reiner Vertrag 1.0 ohne I/O/Uhr/Zufall/Netz; **12 Controls / 7 runtime-scoped / 11 `(criterion, control_id)`-Bindungen**; nur synthetische Formprüfung, rein negativ; Kriterium 5 Human-only, Kriterium 9 non-security-structural; **keine** Security-Evaluation/Enforcement/Readiness; Readiness Gate `NOT EVALUATED`, nicht produktiv |
| **Profile-A Deployment Bundle** | **Repository-Artefakt, `committed` `9c6c0fb`** (CBP-WP-020, D-055) — sieben Dateien unter `deployments/profile-a/`; zwei getrennte Service-Identitäten, fail-closed Compose- und Konfigurationsvorlagen, maschinenlesbare Mount-/Egress-/Secret-/Backup-/RT-2-Verträge, **deterministischer stdlib-only Offline-Validator** (Exit 0, byte-identisch), **166 Bundle-Validation-Tests**; Statusaussage ausschließlich *repository artifact implemented* / *offline validation passed* — **nicht deployed, nicht operational, nicht production-ready** |
| Implementierte Capabilities | **keine (0 von 29)** — Bausteine belegt; Capability 5/6 bleiben `planned` |
| Nachweise oberhalb Stufe 1 | **keine** (lokale Bausteine, keine KB-Kontrolle) |
| Commits | **29** — aktueller Git-Gesamtzähler auf `main`, HEAD `9c6c0fb` |

## Ziel

Ein serverzentriertes und portables KI-Wissens- und Arbeitssystem, das
Implementation Agents die kleinste ausreichende Menge relevanter, aktueller,
autoritativer und datenschutzrechtlich erlaubter Informationen bereitstellt.

**Das Problem dahinter:** zu hoher Token- und Kontextverbrauch. Das System soll
Limits nicht umgehen, sondern Kontext effizienter nutzen.

## Pilotumfang — festgelegt in CBP-WP-003

Der Human Discovery Intake hat den Umfang auf **Profilebene** entschieden.
Konkrete Infrastrukturwerte sind bewusst nicht erhoben.

| Dimension | Festlegung | Entscheidung |
| --- | --- | --- |
| Betriebsprofil | Proxmox-VM, dedizierte Linux-VM als Referenzbetrieb | D-015 |
| Anwendungslaufzeit | Docker Compose **bevorzugt** innerhalb der VM | D-016 |
| Portabilität | Weitere Profile bleiben dokumentierbar, kein Lock-in | D-017 |
| Nutzung | Einzelperson, 1 Nutzer; Multi-User kein Pflichtumfang | D-018 |
| Quellen im Pilot | Markdown-Verzeichnisse, Git-Repositories, Chat-Handoffs, Obsidian-Vault als Markdown | HDI A3 |
| Quellen später | PDF und Office **nur über kontrollierte Quarantäne** | D-019 |
| Datenklassen im Pilot | `public`, `internal` | HDI A4 |
| `confidential` | nicht im Pilot, Architektur muss die Klasse tragen | D-020 |
| `excluded-from-ai` | **von Anfang an im Modell**, Sperrwirkung mit Testdaten prüfen | D-021 |
| Personenbezogene Daten | nicht im Pilot; spätere Aufnahme nur nach gesonderter Prüfung | D-022 |
| Zugriff | privates VPN oder privates Netz, keine öffentliche Freigabe | D-023 |
| Web-UI und mobil | im Pilot — Web-UI erst nach funktionierendem Retrieval | D-024 |
| Obsidian nativ, Wiki, Connectoren, Graph | vertagt beziehungsweise nicht Pilotumfang | D-025 |

Vollständig in
[docs/discovery/HUMAN_DISCOVERY_INPUT.md](../docs/discovery/HUMAN_DISCOVERY_INPUT.md).

## Architekturstand

Kein Komponentenschnitt. Festgehalten sind Prinzipien, Grenzen und seit
CBP-WP-003 ein dreistufiges Kriterienmodell.

- 16 Kernprinzipien (A2, kein ADR) —
  [ARCHITECTURE_PRINCIPLES.md](../docs/architecture/ARCHITECTURE_PRINCIPLES.md)
- 6 Vertrauensgrenzen plus Sicherheitsmodell mit fünf Berechtigungsstufen,
  **keine durchgesetzt** —
  [TRUST_BOUNDARIES.md](../docs/architecture/TRUST_BOUNDARIES.md)
- 5 Datenklassen mit Flussmatrix —
  [DATA_CLASSIFICATION.md](../docs/privacy/DATA_CLASSIFICATION.md)
- Context Budgets B0–B4 —
  [CONTEXT_BUDGETS.md](../docs/architecture/CONTEXT_BUDGETS.md)
- **Kriterienmodell Core Required / Deployment Required / Conditional** (D-026)
  — [G0_SCOPE_LOCK_CRITERIA.md](../docs/discovery/G0_SCOPE_LOCK_CRITERIA.md)

**Invariante:** Der Verlust eines Indexes oder einer Oberfläche darf nicht zum
Verlust des Wissens führen.

**Klarstellung:** Index und Suche laufen lokal, die Sprachverarbeitung nicht.
Ausgewählte Inhalte werden an Claude übertragen — daraus entsteht die
Notwendigkeit der Datenklassifikation. **Standardwert: Übertragung wird
verweigert, bis eine Datenklasse sie erlaubt.**

## Entscheidungen

Angenommene ADRs: **14** (ADR-0001 bis ADR-0014; **ADR-0013** legt Evidence
Schema 3.0 mit Security-Control-Identität und Contract-Binding fest, D-052;
technisch umgesetzt unter **D-053**. **ADR-0014** entscheidet die **KB-04-Stage-1-Durchsetzungsarchitektur**, D-059 — angenommen, **nicht
implementiert**).
ADR-0006 hält privaten
Bestand konstruktiv außerhalb des Kern-Repositorys (D-028); **ADR-0007**
(D-029, D-030) legt Zielstruktur und Bereichsgrenze fest und **schließt
OD-26**; **ADR-0008** (D-031…D-033) legt die Mappingkonvention fest;
**ADR-0009** (D-034…D-037) die technische Sicherheitsgrundlage und **schließt
OD-34 und OD-35** (alle vier am 2026-07-21); **ADR-0010** (D-038…D-041) den
Ingest-Quarantäne-MVP und **ADR-0011** (D-042…D-045) den
Source-Registry-MVP (beide 2026-07-22); **ADR-0012** (D-046…D-049) den
Source-Mapping-Draft-Validator (2026-07-27), der **ADR-0008** präzisiert und
den 31-Feld-Vertrag unverändert lässt.

**61** getroffene Entscheidungen, davon **57** mit A0. **23** offene, davon
**5** mit P0. Geführt in
[project-system/DECISION_REGISTER.md](../project-system/DECISION_REGISTER.md).

> **Zählkorrektur in CBP-WP-008.** Dieses Dokument führte zuvor 26/20/25/10 und
> das Register 28/22/21/8. Die Auszählung ergab **28/24/22/6** — der **vierte**
> Zählfehler des Projekts, erfasst unter R-33. Die Werte oben sind in
> CBP-WP-009 erneut aus den Quelltabellen ausgezählt.

**Ein Konflikt wurde durch A0 aufgelöst:** In CBP-WP-002 hatte ich Docker
Compose gestützt auf Projektübergabe §4 (A5) von „bevorzugt" zu „vorgesehen"
abgeschwächt. Der Human Maintainer bestätigt ausdrücklich „bevorzugte
Anwendungslaufzeit". **A0 schlägt A5**; die Abschwächung ist aufgehoben. Die
Nachführung in `PROJECT_DEFINITION.md` erfolgte in CBP-WP-004; **OD-31 ist
geschlossen**.

## Risiken

32 erfasste Risiken, davon 17 hoch. Geführt in
[project-system/RISK_REGISTER.md](../project-system/RISK_REGISTER.md).

**Weiterhin kritisch:** Berechtigungen ohne technische Durchsetzung und ohne
erhobene Zuordnung (R-25, R-27) · ungeprüfte Sperrwirkung von
`excluded-from-ai` (R-31) · fehlende Quarantäne für Nicht-Markdown-Quellen
(R-32) · 16 vertagte Deployment-Kriterien ohne zuständiges Gate (R-34) ·
kein Benchmark (R-21).

**In CBP-WP-008 wurde kein Risiko geschlossen oder gemindert.** Die
Phase-1-Planung benennt je Risiko einen Schließungsweg und die dafür nötige
Nachweisstufe — beschritten ist keiner. Nach
[PHASE_1_EVIDENCE_PLAN.md](../docs/roadmap/PHASE_1_EVIDENCE_PLAN.md) stehen
sämtliche Artefakte auf **Stufe 1 `dokumentiert`**, und Stufe 1 schließt
definitionsgemäß kein Risiko.

## Offene Fragen

- **G0:** alle 25 Core-Required-Kriterien `accepted`, **0 Blocker** —
  [G0_SCOPE_LOCK_CRITERIA.md](../docs/discovery/G0_SCOPE_LOCK_CRITERIA.md)
- **Fragebogen:** 56 Fragen; **0 offen und Core Required**, 16 vertagt
  (Deployment Required), 1 offen ohne Core-Bezug (7.1 / OD-11) —
  [DISCOVERY_QUESTIONS.md](../docs/discovery/DISCOVERY_QUESTIONS.md)
- **Fehlende Information:** OI-02, OI-07 und OI-10 offen beziehungsweise
  teilweise aufgelöst —
  [OPEN_INFORMATION.md](../docs/discovery/OPEN_INFORMATION.md)

Der dominierende Rest ist **nicht mehr dokumentarisch, sondern technisch**:
**fünf** offene P0-Entscheidungen (OD-04, OD-07, OD-08, OD-11, OD-29) und
**null erbrachte technische Nachweise**. **OD-26 ist am 2026-07-21
geschlossen.**

## Lessons Learned

**Aus CBP-WP-001:** Ein Work Package, das seine fachliche Substanz mitführt,
bleibt ausführbar, auch wenn hinterlegtes Projektwissen im Sitzungskontext
fehlt.

**Aus CBP-WP-002:** Zwei Ausführungsversuche endeten in der Vorprüfung mit
BLOCKED, beide vor jeder Dateiänderung. Ohne Vorprüfung wäre ein Quellenabgleich
mit erfundenen Seitenreferenzen entstanden. Der Abgleich fand außerdem eine
sachlich falsche Aussage im Fundament (Ü-01), die aus dem Work-Package-Wortlaut
allein nicht erkennbar war.

**Aus CBP-WP-003, erste Lektion:** Fortgeschriebene Kennzahlen driften. Die in
CBP-WP-002 berichteten Summen (41/39/35/55) waren falsch addiert; die
tatsächlichen Werte sind 47/45/38/56. Die Dokumente selbst waren korrekt — nur
die Summen. Konsequenz: Kennzahlen werden ausgezählt, nicht fortgeschrieben
(R-33).

**Aus CBP-WP-003, zweite Lektion:** Der erste Fragebogen mit 15 Fragen war
handwerklich korrekt, aber konzeptionell falsch — er hätte den allgemeinen
Scope Lock von einer konkreten Proxmox-Installation abhängig gemacht. Das
Nova-Review hat das erkannt und das dreistufige Kriterienmodell eingeführt.
Ergebnis: 20 Blocker weniger, ohne ein Kriterium zu streichen. Die Trennung
zwischen Produktentscheidung und Installationsdetail war die eigentliche
Erkenntnis.

## Lessons Learned aus CBP-WP-010

**Eine Gruppierung ist keine Berechtigung.** Die hybride Collection-Strategie
wäre ohne den Zusatz des Human Maintainers — dass die Collection nichts
verleiht — die riskanteste der drei Optionen gewesen. Bequeme Sortierordnungen
werden mit der Zeit zu impliziten Rechtequellen, wenn niemand das ausdrücklich
ausschließt.

**Ein Default, der „alles" bedeutet, ist ein Ausfall.** `allowed_subpaths: []`
nimmt **nichts** auf. Die naheliegende Lesart — leerer Filter gleich kein
Filter — ist der häufigste Weg zu unbeabsichtigtem Ingest und deshalb als
Beispiel 6 dokumentiert.

## Lessons Learned aus CBP-WP-009

**Eine zusammengesetzte offene Entscheidung schließt nicht durch eine Antwort.**
OD-26 sah wie eine Frage aus und waren zwei. Wäre nur Teil A entschieden worden,
hätte das Projekt eine Zielstruktur ohne Aussage darüber gehabt, wo private
Daten liegen — und umgekehrt. Die Trennung in Phase A hat das sichtbar gemacht.

## Lessons Learned aus CBP-WP-008

**Die Zählregel wirkt nachlaufend, nicht vorbeugend.** Der vierte Zählfehler
des Projekts entstand in CBP-WP-007 — **nachdem** die Regel eingeführt worden
war — und wurde erst ein Work Package später gefunden. Eine Dokumentregel macht
Fehler später sichtbar; sie verhindert sie nicht. R-33 bleibt deshalb offen.

**Zwei Dokumente können dieselben Bezeichner verschieden belegen.** Die
Layoutoptionen A/B/C aus CBP-WP-004 und ein zweiter, unabhängiger
Bereichsschnitt hätten in derselben Entscheidung kollidiert. Die
Arbeitsbereichsmodelle heißen deshalb **W-1/W-2/W-3**. OD-26 braucht beide
Antworten.

## Repository- und Bereichsgrenze — entschieden

**ADR-0007**, 2026-07-21, A0. Drei Bereiche mit verschiedenem Lebenszyklus:

| Bereich | Inhalt | Klasse | Sicherung |
| --- | --- | --- | --- |
| **Core Repository** | Code, Architektur, Governance, Tests, synthetische Fixtures, Deploymentvorlagen | **publication-capable by design** — nicht freigegeben | Git + Backup |
| **Privater Operator-Workspace** *(außerhalb)* | Konkrete Mappings, private Collections, **operatorbezogene kanonische Registry-Metadaten**, Verweise auf den Secret Store | **kanonisch** | **nur Backup** |
| **RT-1** Rebuildable Derived Data | Index, Embeddings, Cache, generierte Context Packs, Suchprojektionen | derived | **Rebuild** |
| **RT-2** Operational Evidence | Auditlogs, Approval- und Incident-Nachweise, Jobhistorie, Restore-Nachweise | **nicht reproduzierbar** | **Backup erforderlich** |
| **RT-3** Transient Runtime State | Temporäre Dateien, Locks, aktive Jobzustände, Puffer | flüchtig | **keine** — verwerfen |

**Das Core-Repository ist `publication-capable by design`, nicht
veröffentlicht.** Es bleibt privat; eine Veröffentlichung benötigt eine
separate **A0-Entscheidung** (OD-11).

**RT-2 ist kein Cache.** Auditnachweise sind nicht rekonstruierbar und brauchen
Aufbewahrung, Zugriffsschutz und Sicherung.

**Zielstruktur des Core-Repositorys:** `core/`, `adapters/`, `deployments/`,
`config/`, `docs/`, `examples/`, `tests/`.

**Nichts davon existiert.** Kein Verzeichnis angelegt, kein Workspace erzeugt,
keine Datei verschoben. Die Migration braucht ein eigenes, freigegebenes Work
Package und muss die Git-Historie erhalten.

## Mappingkonvention — entschieden

**ADR-0008**, 2026-07-21, A0. Drei Teilentscheidungen:

| Teil | Entscheidung | Grundsatz |
| --- | --- | --- |
| **A** (D-031) | YAML 1.2 Strict Subset, **JSON Schema als Vertragsgrenze** | **M-A** — was mehrdeutig geparst werden kann, ist unzulässig |
| **B** (D-032) | Fachliche Collection **plus** verpflichtender Slot | **M-B** — eine Collection verleiht nichts |
| **C** (D-033) | **Eine** Source Boundary je Mapping | **M-C** — was gemeinsam gemappt ist, wird gemeinsam widerrufen |

Verbindlich in
[PILOT_SOURCE_MAPPING_SPECIFICATION.md](../docs/sources/PILOT_SOURCE_MAPPING_SPECIFICATION.md):
31 Felder, 10 Zustände, 24 Validierungsregeln, 18 Negativtests, 20 Gate-Punkte.

**Nichts davon existiert.** Kein Mapping, keine angebundene Quelle, kein
Validator. Das
[Aktivierungsgate](../docs/operations/PILOT_MAPPING_ACTIVATION_GATE.md) steht
auf `NOT EVALUATED` und ist **ohne den F3-Strang nicht durchlaufbar** — acht
seiner zwanzig Punkte verlangen Nachweisstufe 4.

## Technische Sicherheitsgrundlage — spezifiziert

**ADR-0009**, 2026-07-21, A0. Vier Teilentscheidungen:

| Teil | Entscheidung | Grundsatz |
| --- | --- | --- |
| **A** (D-034) | Getrennte Identitäten: **Control Plane** und **Data Worker** | **S-A** — Verarbeitung erteilt keine Freigabe |
| **B** (D-035) | Versionierter Referenzvertrag `cbp-secret:v1:…`, OS-geschützter Datei-Provider | **S-B** — Eine Referenz ist kein Secret |
| **C** (D-036) | Egress **deny-by-default**, vierfach gebunden | **S-C** — Eine Netzwerkerlaubnis ist keine Datenfreigabe |
| **D** (D-037) | RT-2 **append-only und verkettet** | **S-D** — Ein überschreibbarer Nachweis ist kein Nachweis |

**Zwölf Kontrollbereiche** KB-01…KB-12, **neunstufige Durchsetzungsreihenfolge**
(Promptregeln nur auf Stufe 9), **32 Negativtests plus 1 Positivtest**, **16 Stop-Bedingungen**,
Readiness Gate mit **24 Punkten**.

**Nichts davon existiert.** Alle zwölf stehen auf **DOCUMENTED ONLY**, kein
Test wurde ausgeführt. **OD-34 und OD-35 sind geschlossen** — die konkrete
RT-2-Aufbewahrungsdauer bleibt **Deployment Required**.

## Runtime Skeleton — lokal implementiert

**CBP-WP-012**, 2026-07-21, erste technische Umsetzung. Human-Autorisierung
APPROVE WITH NOTES (A0), Stack A1 (Python 3.13, Standardbibliothek), CLI B1,
additive Struktur C1.

| Gegenstand | Wert |
| --- | --- |
| Runtime-Module | 9 unter `core/core_brain/` |
| CLI | `version`, `validate-config`, `doctor`, `run` |
| Ports | 4, alle **verweigernd** |
| Tests | **69 bestanden**, 0 fehlgeschlagen (67 + 2 Netzwerk-Guard) |
| Python | 3.13.14, keine Abhängigkeiten |
| `run` | verweigert (Exit 4) |

**Keine KB-Kontrolle durchgesetzt.** Der Doctor meldet `PASS`/`NOT APPLICABLE`
als **Skeleton-Ergebnisse**, kein Deploymentnachweis. Alle drei Gates bleiben
`NOT EVALUATED`.

## Lessons Learned aus CBP-WP-012

**Ein grüner Testlauf ist erst nach der Auszählung glaubwürdig.** Der erste
Lauf fand zwei Fehler — beide in den Tests, nicht im Code: `mock.patch` ohne
`create=True` scheitert auf Windows, und ein Grep traf Prosa im Docstring statt
echter Nutzung. Die berichtete Zahl (67 im Erstlauf, 69 nach dem im
Nova-REWORK ergänzten Netzwerk-Guard) stammt jeweils aus dem grünen Lauf, nicht
aus einer Annahme (R-33).

**Ein `PASS` braucht eine Grenze.** Der Doctor meldet Erfolg für Skeleton-
Prüfungen; ohne den ausdrücklichen Zusatz „kein Deploymentnachweis" wäre daraus
schnell „Sicherheitsgrundlage implementiert" geworden — dieselbe Übererweiterung
wie „veröffentlichbar" in CBP-WP-009 und „gültig" in CBP-WP-010.

## Ingest-Quarantäne MVP — lokal implementiert

**CBP-WP-013**, 2026-07-22, zweite technische Umsetzung. Human-Autorisierung
APPROVE WITH NOTES (A0), A1/B1/C1/D1; **A0-Modellsubstitution** auf Opus 4.8
(Fable 5 nicht verfügbar). Festgehalten in **ADR-0010** (D-038…D-041).

| Gegenstand | Wert |
| --- | --- |
| Quarantäne-Module | 6 unter `core/core_brain/quarantine/` |
| CLI | `quarantine scan`, `stage`, `inspect`, `release` |
| Zustände | `READY_FOR_HUMAN_REVIEW`, `REVIEW_REQUIRED`, `BLOCKED` |
| Exitcodes | 0 / 5 / 6 / 7 |
| Store | content-addressed, außerhalb Repo, atomar, idempotent |
| Tests | **137 bestanden** (Basislinie 69), 0 fehlgeschlagen |
| `release` | verweigert immer (Exit 7) |

**Synthetic-only-Grenze technisch durchgesetzt** (Flag + `synthetic:`-Präfix +
Marker). **Keine reale Quelle, kein Mapping, keine Promotion, keine
Indexierung.** Scanner ist ein **Indikator**, keine vollständige Secret-/PII-
Erkennung. **R-01, R-32, R-33 bleiben offen**; Capability 5/6 bleiben `planned`.

## Source-Registry MVP — lokal implementiert

**CBP-WP-014**, 2026-07-22, dritte technische Umsetzung. Human-Autorisierung
APPROVE WITH NOTES (A0), A1/B1/C1/D1. Festgehalten in **ADR-0011** (D-042…D-045).

| Gegenstand | Wert |
| --- | --- |
| Registry-Module | 6 unter `core/core_brain/registry/` |
| CLI | `source-registry validate-definition`, `register`, `list`, `inspect`, `retire`, `activate` |
| Zustände | `REGISTERED_DISABLED`, `RETIRED` |
| Exitcodes | 8 / 9 / 10 / 11 (neu) |
| Speicher | unveränderliche Records, append-only Events, atomarer Katalog, außerhalb Repo |
| Tests | **212 bestanden** (Basislinie 137), 0 fehlgeschlagen |
| `activate` | verweigert immer (Exit 11) |

**Synthetic-only-Grenze technisch durchgesetzt.** Source ID deterministisch aus
Namespace und Source Key; Records und Katalog **ohne** Pfad, URL, Inhalt oder
Mapping-Locator. **Keine reale Quelle, kein Mapping, keine Aktivierung, keine
Indexierung.** **R-33 bleibt offen**; Capability 2/3/7 bleiben nicht vollständig
`implemented`.

## Source-Mapping-Draft-Validator MVP — lokal implementiert

**CBP-WP-015**, 2026-07-27, vierte technische Umsetzung. Human-Autorisierung
APPROVE WITH NOTES (A0), A1/B1/C1/D1. Festgehalten in **ADR-0012** (D-046…D-049).
Ein Reconciliation-Lauf klärte zuvor den **19/31-Blocker**: der angenommene
Vertrag hat **31 Felddefinitionen**, nicht 19.

| Gegenstand | Wert |
| --- | --- |
| Mapping-Module | 6 unter `core/core_brain/mapping/` |
| CLI | `source-mapping validate-draft`, `activation-check` |
| Vertrag | **31 Felddefinitionen** (29 Pflicht + 2 optional), unverändert |
| Dokumentprofil | kanonisches JSON (MVP), BOM/Duplikate/`NaN`/`Infinity` fail-closed |
| Registry-Bindung | extern, **read-only**; nur `collection`/`data_class` exakt |
| `mapping_id` | nur validiert (V4/V21), **nie berechnet** |
| Report | nicht persistiert, deterministisch, minimiert |
| Exitcodes | 12 / 13 (neu) |
| Tests | **315 bestanden** (Basislinie 212), 0 fehlgeschlagen |
| `activation-check` | verweigert immer (Exit 13) |

**Synthetic-only- und read-only-Grenze technisch durchgesetzt.** Kein realer
Pfad, keine URL, kein Source-Inhalt, keine `source_reference` im Report; die
Registry bleibt bytegenau unverändert. **Kein Mapping gespeichert, keine
Aktivierung, keine verbotenen Crosswalks** (`project`↔`domain`,
`ai_transfer`↔`ai_eligibility`). **R-33 bleibt offen** (neunter
Konsistenzvorgang, 19/31-Korrektur); die Bildungsvorschrift von `mapping_id`
bleibt offen; Capability 2/7 bleiben nicht vollständig `implemented`.

## Nächste Arbeitspakete

Siehe
[project-system/WORK_PACKAGE_QUEUE.md](../project-system/WORK_PACKAGE_QUEUE.md)
und [PHASE_1_WORK_PACKAGE_MAP.md](../docs/roadmap/PHASE_1_WORK_PACKAGE_MAP.md).

**CBP-WP-016 — Deterministic Mapping Activation Gate Evaluator** ist unter der
A0-Freigabe **D-050** (APPROVE WITH NOTES, A1/B1-eng/C1/D1) implementiert und
**committed** (`04c427c`). **CBP-WP-017 — Synthetic Evidence Contract &
Provenance Foundation** ist unter **D-051** (APPROVE WITH NOTES, A2/B1/C2/D1/E2)
implementiert und **committed** (`d3168c4`). **CBP-WP-018 — Security Foundation
Readiness Contract & Synthetic Form-Validator** ist **`committed`**: **ADR-0013**
(Evidence Schema 3.0) angenommen, **D-052** (Governance Foundation, `committed`
`4dec921`) und **D-053** (Technical Implementation, `committed` `5ee2e83`)
dokumentiert; der Runtime-Stand ist damit **Evidence Schema 3.0** mit statischem
**Security Contract 1.0** (12 Controls, 7 runtime-scoped, 11 Bindungen),
**558 Tests – OK**. **CBP-WP-019 — Deployment Readiness Intake and Profile-A
Target Specification** ist unter **D-054** (`ADR_NOT_REQUIRED`) **`committed`**
(`3c437f2`, 2026-07-29): der Deployment Readiness Check wurde von
18 auf **19 Prüfpunkte** erweitert (neu **DRC-19 – RT-2-Aufbewahrung**, ohne
G0-Herkunft), **DRC-16** auf das Betreiber-Backup-Regime präzisiert und für
**Profil A** vollständig erhoben — **19 `ready`, 0 `blocked`**; der Human
Maintainer hat den **DRC-Gesamtstatus** am **2026-07-29** auf
**APPROVED BY HUMAN MAINTAINER** gesetzt. Die Freigabe ist **rein
dokumentarisch** und **keine** Installations-, Betriebs-, Security-Readiness-,
Mapping- oder Capability-Freigabe; **R-20 bleibt offen**.
Die Profil-A-Zielspezifikation ist dokumentiert, **nicht bereitgestellt**.
**Keine Installation, kein Deployment, keine Betriebsfreigabe.**

**CBP-WP-020 — Controlled Profile-A Deployment Foundation** ist unter **D-055**
(`ADR_NOT_REQUIRED`) **`committed` und `complete`**: Phase B0 `17057e2`, Phase
B1/B2 `9c6c0fb`. **Zielzustand Z1 erreicht, Scope S2 abgeschlossen, RT-2-Grenze
P1 eingehalten.** In B1/B2 wurde das
**Profil-A-Bundle** als Repository-Artefakt angelegt — **genau sieben Dateien**
unter `deployments/profile-a/` mit zwei getrennten Service-Identitäten,
fail-closed Compose- und Konfigurationsvorlagen sowie maschinenlesbaren Mount-,
Egress-, Secret-, Backup- und RT-2-Verträgen — und mit einem
**deterministischen, stdlib-only Offline-Validator** geprüft:
`PROFILE-A-BUNDLE VALID`, `issues=0`, **Exit 0**, bei zwei Läufen
**byte-identisch**. Hinzu kommen drei Runbooks, ein Runtime-Vertrag und **166
Bundle-Validation-Tests** (Gesamtstand **724 Tests OK**, **0 übersprungen**).

**Zulässig ist ausschließlich:** *repository artifact implemented* · *offline
validation implemented* · *offline validation passed*. **Es wurde nichts
installiert, gestartet, verbunden oder durchgesetzt**; **B3 (reale
Bereitstellung) ist ausgeschlossen** und verlangt ein eigenes
Folge-Work-Package mit eigenem Human Gate. Mapping Activation Gate und Security
Foundation Readiness Gate bleiben `NOT EVALUATED`, die zwölf KB-Kontrollen
`DOCUMENTED ONLY`, **Security-Negativtests 0 von 32** (D-056), Capabilities **0 von
29**, **R-20 offen**.

**Phase C — Post-Commit Reconciliation (dieser Stand, uncommitted):** Nach
`9c6c0fb` (Parent `17057e2`, Commitzahl **29**, `origin/main` synchron) ist
**CBP-WP-020 das zuletzt abgeschlossene Work Package**; **kein Work Package ist
aktiv** und **kein Folge-Work-Package autorisiert**. **R-33 fortgeschrieben von
16/19 auf 17/20.** Decisions, A0-Decisions und ADRs standen zum Abschluss von
CBP-WP-020 auf **55 / 51 / 13**; keine Capability hochgestuft, keine neue
Decision, kein ADR, keine neue Risiko-ID.

**CBP-WP-021 — Canonical Security Test Inventory Reconciliation (dieser Stand,
uncommitted):** Unter **D-056** (`ADR_NOT_REQUIRED`) registriert, Status
**`committed`** und **`complete`** (abgeschlossen 2026-08-03; B0 `0cb4ea9`, B1/B2 `271acc7`). D-056
stellt das kanonische Security-Foundation-Testinventar verbindlich fest:
**32 Negativtests** (NT-01…NT-24 und NT-26…NT-33), **1 Positivtest** (PT-01),
**33 Testfälle**. **NT-25 ist nicht aktiv** — der Fall ist korrekt als PT-01
klassifiziert, die Nummer bleibt nach Regel **TT-5** bewusst frei. **NT-32 und
NT-33 sind gültig** und lösen die frühere dokumentübergreifende Doppelvergabe
von NT-23 und NT-24 auf; die ursprünglichen Matrix-Fälle bleiben unverändert
aktiv. **Die Zahl 31 ist ein überholter, falsch etikettierter Ableitungswert** —
der von CBP-WP-011 auf 33 korrigierte Gesamtwert, in einer nicht nachgeführten
Zusammenfassungszeile fälschlich als „Negativtests" geführt.

**Ausgeführt sind 0 von 32 Negativtests und 0 von 1 Positivtest.** Die
Feststellung eines Inventarwerts ist **keine** Testausführung und **keine**
Gateauswertung. Die **Durchführung** der Reconciliation erfolgt erst in
**B1/B2** und umfasst ausdrücklich auch die **ausführbaren** Profil-A-Artefakte
(`bundle.json`, `validate.py`, Bundle-Tests). Bis dahin besteht eine bekannte,
eingegrenzte **Übergangsabweichung**; das bestehende Bundle bleibt unverändert
und gegen seinen bisherigen Vertrag gültig, darf aber hinsichtlich der
Security-Test-Gesamtzahl **nicht als kanonisch** bezeichnet werden.

**Phase C (dieser Stand, uncommitted):** Nach `271acc7` (Parent `0cb4ea9`,
`origin/main` synchron) ist **CBP-WP-021 `committed` und `complete`**,
Abschlussdatum **2026-08-03**; die Übergangsabweichung ist **aufgelöst**, die
Reconciliation umfasste auch `bundle.json`, `validate.py`, die Bundle-Tests und
die Profil-A-README. **Kein Work Package ist aktiv, kein Folge-Work-Package
autorisiert.** **R-33 fortgeschrieben von 17/20 auf 18/21** — achtzehnter
Konsistenzvorgang, identisch in `RISK_REGISTER.md` und `COMPLIANCE_CHECK.md`
gespiegelt und **genau einmal gezählt**.

Decisions, A0-Decisions und ADRs standen zum Abschluss von CBP-WP-021 auf
**56 / 52 / 13**. Capabilities bleiben **0 von 29**, beide Gates `NOT EVALUATED`,
die zwölf KB-Kontrollen `DOCUMENTED ONLY`, **R-20 offen**, **R-33
fortgeschrieben 17/20 → 18/21** in Phase C. **KB-04 war nicht Bestandteil von
CBP-WP-021**; das KB-04-Paket ist inzwischen als **CBP-WP-022** registriert
(D-057, Phase B0, Registration-only) — die **technische Umsetzung bleibt
nicht autorisiert**.

## Rückmeldung an Nova

CBP-WP-012 ist ausgeführt — **das erste Artefakt mit technischer Wirkung**. Ein
lokaler, fail-closed Runtime Skeleton, 69 Tests bestanden, `run` verweigert.
**Es wurde nichts angebunden, nichts aufgelöst, nichts verbunden und nichts
gestartet.**

**Drei Punkte zur Hervorhebung:**

1. **Ein `PASS` im Doctor ist kein Deploymentnachweis.** Keine der sechs
   `PASS`-Zeilen belegt eine durchgesetzte KB-Kontrolle. Sie bleiben
   `DOCUMENTED ONLY`; der reale Nachweis entsteht auf der Ziel-VM.
2. **`run` verweigert strukturell.** Selbst mit beiden Gate-Status auf
   `ACCEPTED` startet keine Runtime — ein Test belegt das. Der Skeleton *kann*
   nicht produktiv laufen.
3. **Zwei Testdefekte, keine Codedefekte.** Die Testzahl (67 → 69) stammt aus dem
   grünen Lauf nach der Korrektur.

**Kein Risiko wurde geschlossen.** R-25, R-26, R-27, R-30, R-31, R-32 und R-20
bleiben offen — ein Skeleton ist keine durchgesetzte Kontrolle.
