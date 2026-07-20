# NDF Adoption Notes — dokumentierte Abweichungen

| Feld | Wert |
| --- | --- |
| Framework | Nova Development Framework **v1.0.0** |
| Erfasst in | CBP-WP-001 |
| Stand | 2026-07-20 |

Dieses Dokument haelt fest, wo Core Brain Pilot von den kanonischen
NDF-v1.0.0-Vorlagen abweicht, und warum. Grundsatz aus CBP-WP-001: **keine
parallelen doppelten Strukturen**. Wo NDF und Work Package unterschiedliche
Pfade vorsehen, existiert genau **eine** Datei — nicht beide.

---

## Geprueft wurden

| NDF-Dokument | Zweck |
| --- | --- |
| `README.md` | Rollenmodell, WP-Typen, Lifecycle |
| `framework/standards/WORK_PACKAGE_TYPES.md` | WP-Typen |
| `framework/standards/WORK_PACKAGE_LIFECYCLE.md` | Lifecycle |
| `docs/agent-workflows/NDF_PROMPT_MODES.md` | Prompt Modes |
| `docs/agent-workflows/NDF_CONTEXT_ECONOMY.md` | Context Economy |
| `docs/workflow/NOVA_CHATGPT_ROLE.md` | Nova-Rolle |
| `framework/project-system/templates/` | Projektsystem-Vorlagen |
| `framework/project-starter/templates/` | Starter-Vorlagen |
| `framework/project-starter/templates/project-system-folder-structure.md` | kanonische Ordnerstruktur |

## Uebernommene Konventionen

- Rollenmodell Nova → Implementation Agent → Human Maintainer
- Lifecycle `Classify → Plan → Execute → Report to Nova → Review → Commit`
- WP-Typ `docs-only`
- Prompt Modes Full / Standard / Short
- Fuenf Kontextschichten, Compact Context Summary, Context Packs
- Verzeichnisnamen `project-system/` und `project-brain/`
- Dateinamen `PROJECT_PROFILE.md`, `CAPABILITY_MATRIX.md`,
  `WORK_PACKAGE_QUEUE.md`, `COMPLIANCE_CHECK.md`, `HEALTH_SCORE.md`,
  `PROJECT_BRAIN.md`
- Abschnittsgliederung von `PROJECT_PROFILE_TEMPLATE.md` und
  `INITIAL_PROJECT_BRAIN.md`
- Statuswert `planned` aus `CAPABILITY_MATRIX_TEMPLATE.md`
- Spalten `ID | Title | Priority | Status | Prompt` aus
  `WORK_PACKAGE_QUEUE_TEMPLATE.md`
- Regel "keine autonomen Commits oder Pushes"
- Fail-closed-, documentation-only-Grundhaltung (ADR-0032)
- Kein `LICENSE` — NDF fuehrt eine Lizenz im eigenen Repository, CBP-WP-001
  verbietet sie ausdruecklich fuer dieses Projekt

---

## AB-01 — Prompt Mode "Lean" existiert in NDF v1.0.0 nicht

**Feststellung.** CBP-WP-001 deklariert `Prompt Mode: Lean`. NDF v1.0.0 kennt
genau drei Modi: **Full**, **Standard**, **Short**. Ein Modus "Lean" ist in
`NDF_PROMPT_MODES.md` nicht definiert.

**Behandlung.** "Lean" wurde als **Standard Prompt Mode** ausgefuehrt. Das
passt zur Beschreibung des Standard-Modus — vorhersagbare, begrenzte Aufgabe,
Verweis auf dauerhafte Regeln, Abschluss mit Bericht an Nova — und zur
zusaetzlichen Angabe `Context Budget: B2 – Standard`.

**Offen fuer Nova.** Entweder kuenftig `Standard` schreiben, oder "Lean" als
projektinternes Synonym per ADR festschreiben.

---

## AB-02 — Context Budgets B0–B4 sind kein NDF-Konzept

**Feststellung.** CBP-WP-001 fuehrt `Context Budget: B2 – Standard` und listet
"Context Budgets B0–B4" unter den Kernprinzipien. NDF v1.0.0 kennt **keine**
benannten Budgetstufen; die Context Economy arbeitet mit fuenf Kontextschichten,
Compact Context Summary und Context Packs.

**Behandlung.** Beides wird **getrennt** gefuehrt:

| Konzept | Herkunft | Gegenstand |
| --- | --- | --- |
| Context Economy, Schichten 1–5 | NDF v1.0.0 | Kontext eines **Agentenauftrags** |
| Context Budgets B0–B4 | Core Brain Pilot | Umfang eines **Retrieval-Ergebnisses** |

Sie beschreiben unterschiedliche Dinge und werden nicht vermischt. B0–B4 ist
eine Produkteigenschaft des zu bauenden Systems, keine NDF-Erweiterung.

**Offen.** Die Stufen sind inhaltlich undefiniert — siehe OI-03.

---

## AB-03 — Projektmanifest als Markdown statt YAML

**Feststellung.** NDF v1.0.0 sieht kanonisch `project-system/project-manifest.yaml`
vor (Vorlagen `project-manifest.template.yaml`, `INITIAL_PROJECT_MANIFEST.yaml`).
CBP-WP-001 fordert `project-system/PROJECT_MANIFEST.md` und erlaubt als
Aenderungen ausschliesslich Markdown-Dokumentation, `.gitignore` und Ordner.

**Behandlung.** Angelegt wurde `PROJECT_MANIFEST.md`. Eine YAML-Datei waere
ausserhalb der in CBP-WP-001 erlaubten Dateitypen gewesen; die engere Grenze
des freigegebenen Work Packages hat Vorrang.

**Empfehlung.** In einem Folge-Work-Package auf `project-manifest.yaml`
umstellen und die Markdown-Fassung durch die YAML-Fassung **ersetzen** — nicht
ergaenzen.

---

## AB-04 — Entscheidungen und Risiken liegen in `project-system/`

**Feststellung.** NDF v1.0.0 sieht `project-brain/DECISIONS.md` und
`project-brain/RISKS.md` vor. CBP-WP-001 fordert
`project-system/DECISION_REGISTER.md` und `project-system/RISK_REGISTER.md`.

**Behandlung.** Der Vorgabe von CBP-WP-001 gefolgt. Die NDF-Pendants unter
`project-brain/` wurden **bewusst nicht** zusaetzlich angelegt, um doppelte
Strukturen zu vermeiden. `project-brain/PROJECT_BRAIN.md` verweist auf die
Register, statt deren Inhalt zu wiederholen.

**Offen fuer Nova.** Angleichung an das NDF-Namensschema oder dauerhafte
Abweichung per ADR — siehe Q-30.

---

## AB-05 — `project-brain/` bewusst schlank

**Feststellung.** NDF v1.0.0 sieht neben `PROJECT_BRAIN.md` auch
`DECISIONS.md`, `LESSONS_LEARNED.md`, `RISKS.md` und `OPEN_QUESTIONS.md` vor.

**Behandlung.** Nur `PROJECT_BRAIN.md` angelegt. Die uebrigen Themen sind
bereits abgedeckt: Entscheidungen und Risiken in `project-system/` (AB-04),
offene Fragen in `docs/discovery/`. `LESSONS_LEARNED` ist ohne Projekthistorie
inhaltsleer und wird angelegt, sobald es etwas zu lernen gibt. Die Abschnitte
sind als Gliederung in `PROJECT_BRAIN.md` erhalten.

---

## AB-06 — Work Packages unter `work-packages/` statt `prompts/claude/work-packages/`

**Feststellung.** NDF v1.0.0 sieht `prompts/claude/work-packages/` vor.
CBP-WP-001 fordert `work-packages/CBP-WP-001.md`.

**Behandlung.** Der Vorgabe gefolgt. `prompts/claude/` wurde nicht zusaetzlich
angelegt. Das flache Verzeichnis ist zudem agent-neutral — passend zum
Prinzip der Deployment- und Werkzeugneutralitaet.

---

## AB-07 — `docs/ndf/` ohne WORKFLOW / QUALITY_GATES / RELEASE_PROCESS

**Feststellung.** NDF v1.0.0 sieht unter `docs/ndf/` die Dateien
`WORKFLOW.md`, `QUALITY_GATES.md` und `RELEASE_PROCESS.md` vor. CBP-WP-001
fordert dort `README.md` und `ADOPTION_NOTES.md`.

**Behandlung.** Der Vorgabe gefolgt. Der Workflow-Inhalt steht in
[README.md](README.md). `QUALITY_GATES.md` und `RELEASE_PROCESS.md` wurden
**nicht** angelegt: Gate-Kriterien fuer G0 sind noch nicht definiert (OI-04),
und ein Releaseprozess ohne Implementierung und ohne Lizenzentscheidung waere
Spekulation. Beide sind als Folge-Work-Package vorgemerkt.

---

## AB-08 — `COMPLIANCE_CHECK.md` und `HEALTH_SCORE.md` ergaenzt

**Feststellung.** Beide sind Teil der kanonischen NDF-Ordnerstruktur, aber in
der Zielstruktur von CBP-WP-001 nicht aufgefuehrt.

**Behandlung.** Angelegt. CBP-WP-001 bezeichnet seine Zielstruktur als
"mindestens benoetigt" und weist ausdruecklich an, die Struktur an die
verbindlichen NDF-v1.0.0-Vorlagen anzupassen. Beide Dateien sind als Geruest
mit Phase-0-Status angelegt, ohne inhaltliche Bewertung.

Dies ist eine **offengelegte** Ergaenzung, keine stillschweigende
Scope-Erweiterung.

---

## AB-09 — Sprache Deutsch

**Feststellung.** NDF v1.0.0 mischt: englische Standarddokumente, deutsche
Vorlagenabschnitte (`Ziel`, `Zielgruppe`, `Rückmeldung an Nova`).

**Behandlung.** Projektdokumentation auf Deutsch, entsprechend Work Package und
Projektanweisungen. Englische NDF-Fachbegriffe (Work Package, Context Pack,
Gate, Prompt Mode, Capability) bleiben unuebersetzt, damit sie auf die
NDF-Quellen zurueckfuehrbar sind.

Dateinamen folgen dem englischen NDF-Schema in Grossbuchstaben.

---

## AB-10 — Umlaute in Fliesstext transkribiert

**Feststellung.** Die Dokumente verwenden ueberwiegend `ae`, `oe`, `ue`, `ss`
statt Umlauten.

**Behandlung.** Bewusst, zur Vermeidung von Encoding-Problemen zwischen
Windows-Werkzeugketten, Git und spaeteren Ingest-Pipelines. Rein kosmetisch,
inhaltlich ohne Bedeutung. Bei Bedarf per Folge-Work-Package auf echte Umlaute
umstellbar.

---

## Nicht uebernommen

| Gegenstand | Grund |
| --- | --- |
| v1.1-Planung | CBP-WP-001 untersagt sie ausdruecklich |
| `.claude/`-Skills-Bibliothek (38 Skills) | Nicht Gegenstand von CBP-WP-001 |
| `scripts/`, `build/`, `.github/` | Skripte und CI-Workflows sind verboten |
| `LICENSE` | Ausdruecklich verboten; Lizenzwahl offen (Q-28) |
| `branding/` | Oeffentliches Branding ist in Phase 0 gesperrt |
| `academy/`, `examples/` | Bestandteile des Framework-Repositorys, nicht eines Zielprojekts |
