# Decision Register – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Überarbeitet in | **CBP-WP-011** |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

> **Ablageabweichung.** NDF v1.0.0 sieht `project-brain/DECISIONS.md` vor.
> Es existiert bewusst nur **eine** von beiden — AB-04.

## Getroffene Entscheidungen

### Aus CBP-WP-001 und CBP-WP-002

| ID | Entscheidung | Klasse | Datum | ADR |
| --- | --- | --- | --- | --- |
| D-001 | Verbindlich nach NDF v1.0.0; keine v1.1-Planung | A0 | 2026-07-20 | offen |
| D-002 | Phase 0 ist Discovery und Scope Lock; keine produktive Implementierung | A0 | 2026-07-20 | offen |
| D-003 | Commit-, Push- und Release-Autorität ausschließlich beim Human Maintainer | A0 | 2026-07-20 | offen |
| D-004 | Markdown ist das kanonische Wissensformat | A2 | 2026-07-20 | offen |
| D-005 | Abgeleitete Daten werden nicht versioniert und sind nie autoritativ | A2 | 2026-07-20 | offen |
| D-006 | Fünf Datenklassen; Secrets nie in Repository, Index, Context Pack oder Modellkontext | A2 | 2026-07-20 | offen |
| D-007 | Keine `LICENSE`-Datei in Phase 0 | A0 | 2026-07-20 | — |
| D-008 | Register in `project-system/`; keine Doppelstruktur | A2 | 2026-07-20 | offen |
| D-009 | NDF Prompt Modes sind Full, Standard, Short. „Lean" ist ausschließlich der Name von B1 | A0 | 2026-07-20 | offen |
| D-010 | A5-Projektübergabe dauerhaft als kanonische Quelle im Repository | A0 | 2026-07-20 | — |
| D-011 | Quellenklassifikation: PDF A4, Textfassung A6, Übergabe A5 | A0 | 2026-07-20 | — |
| D-012 | UTF-8 mit echten deutschen Umlauten | A0 | 2026-07-20 | — |
| D-013 | Dedizierte Linux-VM ist Referenzbetrieb; Docker Compose vorgesehene Laufzeit darin | A0 | 2026-07-20 | offen |
| D-014 | Wiki, Graph und Web-UI nicht vor bestandenem Retrieval-Pilot-Gate | A0 | 2026-07-20 | offen |

### Neu aus CBP-WP-003 — Human Discovery Intake

Alle folgenden Entscheidungen wurden vom Human Maintainer **ausdrücklich**
getroffen. Quelle jeweils
[../docs/discovery/HUMAN_DISCOVERY_INPUT.md](../docs/discovery/HUMAN_DISCOVERY_INPUT.md).

| ID | Entscheidung | Status | Autorität | Quelle | Datum | Betroffene Kriterien | Konsequenz |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **D-015** | Erstes Pilotprofil ist eine Proxmox-VM mit dedizierter Linux-VM als Referenzbetrieb | `accepted` | **A0** | HDI A1 | 2026-07-20 | F-1 | Referenzprofil A ist gewählt; Profile B–E bleiben dokumentierbar |
| **D-016** | Docker Compose ist die **bevorzugte** Anwendungslaufzeit innerhalb dieser VM | `accepted` | **A0** | HDI A1 | 2026-07-20 | F-2 | Präzisiert D-013 und **hebt die Abschwächung Ü-02 aus CBP-WP-002 auf** — siehe Hinweis unten |
| **D-017** | Deployment-Neutralität wird beibehalten: allgemeine Linux-VM, Docker/OCI und Einzelplatz bleiben dokumentierbare Profile | `accepted` | **A0** | HDI A1 | 2026-07-20 | F-5 | Kein Proxmox-Lock-in; Capability 29 bestätigt |
| **D-018** | Multi-User und Multi-Tenant sind kein Pflichtumfang des ersten Piloten; spätere Teamnutzung darf nicht verhindert werden | `accepted` | **A0** | HDI A2 | 2026-07-20 | A-1, A-2 | Single-User als Einstieg; Architektur bleibt erweiterbar |
| **D-019** | PDF- und Office-Dokumente gelangen nicht ungeprüft in den kanonischen Bestand; kontrollierte Ingest- und Quarantäne-Pipeline erforderlich | `accepted` | **A0** | HDI A3 | 2026-07-20 | D-1, D-3 | Capability 5 (Ingest-Quarantäne) wird Voraussetzung für Nicht-Markdown-Quellen |
| **D-020** | `confidential` ist nicht Teil des ersten Piloten, muss aber architektonisch unterstützt werden | `accepted` | **A0** | HDI A4 | 2026-07-20 | D-7 | D-7 wird `not-applicable` für den Pilot; Klasse bleibt im Modell |
| **D-021** | `excluded-from-ai` ist von Anfang an im Daten- und Berechtigungsmodell zu führen; Sperrwirkung mit synthetischen oder unkritischen Testdaten zu prüfen | `accepted` | **A0** | HDI A4 | 2026-07-20 | D-5 | Macht R-30 zu einer konkret prüfbaren Anforderung; **strenger als das bisherige Fundament** |
| **D-022** | Personenbezogene Daten sind nicht Teil des ersten Piloten; spätere Aufnahme erfordert vorher eine gesonderte Datenschutz- und Rechtsgrundlagenprüfung | `accepted` | **A0** | HDI A4 | 2026-07-20 | D-6 | D-6 wird `not-applicable`; OD-09 wird vertagt statt geschlossen |
| **D-023** | Zugriff nur über privates VPN oder privates Netz; keine öffentliche Freigabe interner Dienste | `accepted` | **A0** | HDI A5 | 2026-07-20 | C-5 (Grundsatz) | Zugriffsprofil festgelegt; Technologiewahl bleibt Deployment Required |
| **D-024** | Web-UI und mobile Nutzung gehören zum Pilotumfang; die Web-UI aber erst nach funktionierendem Index, Suche, Brain-First-Retrieval und Benchmark | `accepted` | **A0** | HDI A6 | 2026-07-20 | A-4, A-5, F-6 | Präzisiert D-014 mit einer konkreten Vorbedingung |
| **D-025** | Native Obsidian-Nutzung, Wiki-Pilot und externe Connectoren werden vertagt; Knowledge Graph ist nicht Pilotumfang | `accepted` | **A0** | HDI A6 | 2026-07-20 | A-7 | Vier Conditional-Kriterien bleiben inaktiv |
| **D-026** | Dreistufiges Kriterienmodell: Core Required, Deployment Required, Conditional. G0 sperrt den allgemeinen Produkt-Scope, nicht die Installationsdetails | `accepted` | **A0** | Nova-Review CBP-WP-003 | 2026-07-20 | alle 47 | Blocker von 45 auf 25 reduziert; separates Deployment-Readiness-Gate später zu definieren |
| **D-027** | **G0 – Discovery and Scope Lock: APPROVE G0 WITH NOTES.** Die Freigabe autorisiert ausschließlich die Planung von Phase 1; keine Freigabe für produktiven Betrieb, produktiven Ingest, öffentliche Erreichbarkeit oder zusätzliche sensible Datenklassen. Fünf Nachweise vor produktivem Betrieb; Web-UI und mobile Nutzung erst nach gemessenem Retrieval-Piloten | `accepted` | **A0** | Entscheidungsblock in G0_SCOPE_LOCK_REVIEW | 2026-07-21 | alle 25 Core-Kriterien | Phase 0 COMPLETE; Phase 1 AUTHORIZED FOR PLANNING |
| **D-028** | **ADR-0006 angenommen:** produktive und private Wissensbestände bleiben außerhalb des allgemeinen Core-Repositorys und werden über logische Source Slots und deploymentspezifische, fail-closed Mappings angebunden | `accepted` | **A0** | Entscheidungsblock in G0_SCOPE_LOCK_REVIEW | 2026-07-21 | D-1 | ADR-0006 von `proposed` auf `accepted` (A1); OD-05, OD-06, OD-26 bleiben offen |

### Neu aus CBP-WP-009 — Repository Boundary Decision

Beide Entscheidungen am **2026-07-21**, Autorität **A0**, Quelle: direkte
Human-Maintainer-Entscheidung im Entscheidungsblock. Wortlaut unverändert in
[ADR-0007](../docs/decisions/ADR-0007-repository-und-workspace-grenze.md).

| ID | Entscheidung | Status | Autorität | Quelle | Datum | Betroffen | Konsequenz |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **D-029** | **Teil A — Zielstruktur des Core-Repositorys: Ziel-Monorepo nach Layout-Option B.** Bereiche `core/`, `adapters/`, `deployments/`, `config/`, `docs/`, `examples/`, `tests/`. **Autorisiert keine Verschiebung**; das aktuelle Layout bleibt bis zu einem separaten, ausdrücklich freigegebenen Migrations-Work-Package. Migration nachvollziehbar, schrittweise, rücksetzbar und **ohne Verlust der Git-Historie** | `accepted` | **A0** | Entscheidungsblock CBP-WP-009 | 2026-07-21 | **OD-26 Teil A** | **ADR-0007** (A1); AB-03…AB-08 bleiben offen (OD-29) |
| **D-030** | **Teil B — Bereichsmodell W-3: privater Operator-Workspace außerhalb des Core-Repositorys.** Private und produktive Wissensbestände, konkrete Source Mappings, private Collection-Konfigurationen und **operatorbezogene kanonische Registry-Metadaten** liegen außerhalb. Runtime-Daten bilden einen dritten, separaten Bereich. **Secrets nirgends im Klartext** — nur Verweise auf einen getrennten Secret Store. Eine Runtime-Kopie der Source Registry ist **nie** die einzige Quelle kanonischer Registry-Metadaten | `accepted` | **A0** | Entscheidungsblock CBP-WP-009 | 2026-07-21 | **OD-26 Teil B** | **ADR-0007** (A1); konkretisiert ADR-0006; Überführung nach W-2 bleibt vorbereitet, **nicht beschlossen** |

> **Beide Entscheidungen legen Zielarchitektur fest, keine Umsetzung.** Es
> wurde keine Datei verschoben, kein Verzeichnis angelegt und kein Workspace
> erzeugt.

### Neu aus CBP-WP-010 — Pilot Source Mapping Specification

Alle drei am **2026-07-21**, Autorität **A0**, Quelle: direkte
Human-Maintainer-Entscheidung im Entscheidungsblock. Wortlaut unverändert in
[ADR-0008](../docs/decisions/ADR-0008-pilot-source-mapping-konvention.md).

| ID | Entscheidung | Status | Autorität | Quelle | Datum | Betroffen | Konsequenz |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **D-031** | **Teil A — Kanonisches Mappingformat: YAML 1.2 Strict Subset mit JSON-Schema-Validierung.** Nur ein klar begrenzter YAML-Teilumfang; **JSON Schema ist die verbindliche maschinenprüfbare Vertragsgrenze**. Unzulässig sind insbesondere Anchors, Aliases, Merge Keys, benutzerdefinierte Tags, doppelte Schlüssel und mehrere Dokumente je Datei | `accepted` | **A0** | Entscheidungsblock CBP-WP-010 | 2026-07-21 | PS-02, PS-03, PS-04 | **ADR-0008** (A1); Formatregeln F1–F7 im Mapping-Schema |
| **D-032** | **Teil B — Collection-Strategie: hybrid.** Collections primär nach fachlichem Projekt oder fachlicher Domäne; der **Source Slot bleibt verpflichtendes Metadatum** für Provenienz, Ingest-Regeln, Berechtigungen, Löschung und Audit. **Die Collection allein verleiht keine Autoritätsklasse, keine Datenklasse und keine AI-Transfer-Freigabe** | `accepted` | **A0** | Entscheidungsblock CBP-WP-010 | 2026-07-21 | Retrieval, Berechtigungen | **ADR-0008** (A1); Grundsatz M-B |
| **D-033** | **Teil C — Mapping-Granularität: genau eine Source Boundary je Mapping.** Bei PS-02 ein Markdown Root, bei PS-03 ein Git Repository, bei PS-04 ein Handoff Root. **Mehrere Quellen dürfen nicht durch ein gemeinsames Mapping gekoppelt werden** | `accepted` | **A0** | Entscheidungsblock CBP-WP-010 | 2026-07-21 | Rechte, Revisionen, Löschung, Tombstones | **ADR-0008** (A1); Grundsatz M-C |

> **Die drei Entscheidungen legen eine Konvention fest, kein Mapping.** Es
> wurde keine Quelle angebunden, kein Mapping erstellt, nichts aktiviert. Das
> [Aktivierungsgate](../docs/operations/PILOT_MAPPING_ACTIVATION_GATE.md) steht
> auf **`NOT EVALUATED`**.

### Neu aus CBP-WP-011 — Technical Security Foundation Specification

Alle vier am **2026-07-21**, Autorität **A0**, Quelle: direkte
Human-Maintainer-Entscheidung im Entscheidungsblock. Wortlaut unverändert in
[ADR-0009](../docs/decisions/ADR-0009-technische-sicherheitsgrundlage.md).

| ID | Entscheidung | Status | Autorität | Quelle | Datum | Betroffen | Konsequenz |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **D-034** | **Teil A — Service-Identity-Modell: getrennte logische Identitäten für Control Plane und Data Worker** mit minimalen, voneinander unabhängigen Rechten. Die Control Plane darf Canonical Sources nicht verändern und nicht automatisch publizieren; der **Data Worker erhält keine Approval-, Administrations- oder Publish-Rechte**. Konkrete Unix-Benutzer, Container-Identitäten, UID- und GID-Werte erst deploymentspezifisch | `accepted` | **A0** | Entscheidungsblock CBP-WP-011 | 2026-07-21 | KB-01, KB-02, KB-03, KB-05 | **ADR-0009** (A1); Grundsatz S-A |
| **D-035** | **Teil B — Secret-Modell: versionierter, providerneutraler Secret-Reference- und Resolver-Vertrag** plus **OS-geschützter Datei-Provider** für den Pilot, außerhalb von Core-Repository, Operator-Workspace und Runtime. Werte nur read-only an die berechtigte Identität; **niemals in Git, Konfiguration, Umgebungsvariablen, Kommandozeilen, Logs, RT-2, Context Packs, Fehlermeldungen oder Reports**. Referenzen enthalten keine Werte und keine Hostpfade; später ohne Änderung der Mappingkonvention migrierbar | `accepted` | **A0** | Entscheidungsblock CBP-WP-011 | 2026-07-21 | KB-08; **schließt OD-34** | **ADR-0009** (A1); Grundsatz S-B |
| **D-036** | **Teil C — Netzwerk-Egress: deny-by-default mit expliziter Allowlist**, gebunden an **Ziel, Provider, Zweck und Service-Identität**. Vor jeder externen Übertragung zusätzlich Datenklasse, AI-Transfer-Policy, Approval-Zustand, Zweck und freigegebenes Ziel prüfen. **Lokale Suche und Retrieval funktionieren ohne externen Netzwerkzugriff**; `excluded-from-ai` bleibt unabhängig von jeder Netzfreigabe blockiert | `accepted` | **A0** | Entscheidungsblock CBP-WP-011 | 2026-07-21 | KB-10, KB-11 | **ADR-0009** (A1); Grundsatz S-C |
| **D-037** | **Teil D — Operational Evidence: logisch append-only, integritätsverkettet, aufbewahrungs- und sicherungspflichtig.** Korrekturen durch nachvollziehbare Folgeereignisse statt stillschweigendem Überschreiben; stabile Ereignisidentitäten, getrennte Zugriffsrechte, Backup, Restore-Nachweis, **sichtbare Erkennung von Ketten- oder Integritätsbrüchen**. RT-2 ist weder Cache noch kanonische Wissensbasis und nicht zuverlässig rekonstruierbar. **Konkrete Aufbewahrungsdauer, Speichertechnologie und Implementierung bleiben deploymentspezifisch** | `accepted` | **A0** | Entscheidungsblock CBP-WP-011 | 2026-07-21 | KB-09, KB-12; **schließt OD-35** | **ADR-0009** (A1); Grundsatz S-D |
| **D-038** | **Teil A — Intake-Granularität: genau eine ausdrücklich angegebene Markdown-Datei je Intake.** Keine Verzeichnisrekursion, keine Mehrfachdateien, keine Archive, keine Symlink-Folgen, keine implizite Suche, kein Zugriff auf Canonical-Source-Roots | `accepted` | **A0** | Entscheidungsblock CBP-WP-013 | 2026-07-22 | Quarantäne-MVP, R-32 | **ADR-0010** (A1) |
| **D-039** | **Teil B — Quarantänespeicher: lokaler content-addressed Dateispeicher** mit unveränderlichem Payload und atomarem JSON-Manifest. Root explizit und außerhalb des Core-Repositorys; im Work Package nur temporär mit synthetischen Daten. Objektpfade nur aus validiertem SHA-256; Idempotenz; Kollision blockiert. **Weder Canonical Source noch RT-2, keine produktive Sicherheitsgrenze** | `accepted` | **A0** | Entscheidungsblock CBP-WP-013 | 2026-07-22 | Quarantäne-MVP | **ADR-0010** (A1) |
| **D-040** | **Teil C — Baseline-Scanner: strukturelle Prüfungen plus deterministische Credential- und PII-Indikatoren.** Fest verdrahtete Regeln, keine frei konfigurierbaren regulären Ausdrücke. **Indikatoren, keine vollständige Secret-, PII- oder Klassifikationskontrolle.** Befunde ohne Snippet, Pfad oder Wert | `accepted` | **A0** | Entscheidungsblock CBP-WP-013 | 2026-07-22 | R-01, R-32 | **ADR-0010** (A1) |
| **D-041** | **Teil D — Freigabemodell: drei Zustände `READY_FOR_HUMAN_REVIEW`, `REVIEW_REQUIRED`, `BLOCKED`; keine automatische Promotion.** Kein Zustand bedeutet `approved`, `released`, `enabled` oder `indexed`. `quarantine release` verweigert deterministisch fail-closed | `accepted` | **A0** | Entscheidungsblock CBP-WP-013 | 2026-07-22 | Quarantäne-MVP | **ADR-0010** (A1) |
| **D-042** | **Teil A — Registry-Identität: stabiler Namespace plus Source Key, daraus deterministisch abgeleitete Source ID** (`src-` + 24 Hex des SHA-256 aus Identitätsschema, Namespace, Source Key). Kein Display Name, Pfad, URL oder Inhalt in der ID; abweichende Identität/Definition unter bestehender ID blockiert | `accepted` | **A0** | Entscheidungsblock CBP-WP-014 | 2026-07-22 | Registry-MVP | **ADR-0011** (A1) |
| **D-043** | **Teil B — Registry-Speicher: unveränderliche JSON-Records plus atomar abgeleiteter Katalog außerhalb des Repositorys.** Kanonisches UTF-8-JSON, atomar, keine stille Überschreibung, Idempotenz, Konflikt bei abweichender Definition, kein Teilkatalog bei Integritätsfehler, vollständig rekonstruierbar. **Weder Canonical Source noch RT-2, keine produktive Isolationsgrenze** | `accepted` | **A0** | Entscheidungsblock CBP-WP-014 | 2026-07-22 | Registry-MVP | **ADR-0011** (A1) |
| **D-044** | **Teil C — Lifecycle: `REGISTERED_DISABLED` und `RETIRED`; Retirement als append-only Event; keine Aktivierung.** Keine Löschung, keine Aktualisierung, keine Reaktivierung; idempotent; keine Freitexte, Pfade oder Inhalte im Event | `accepted` | **A0** | Entscheidungsblock CBP-WP-014 | 2026-07-22 | Registry-MVP | **ADR-0011** (A1) |
| **D-045** | **Teil D — Katalogumfang: ausschließlich minimierte Metadaten** (10 Felder je Eintrag); keine Pfade, URLs, Source-Inhalte, Definition Hashes, Owner-Freitexte oder Mapping-Locators. Deterministisch nach `source_id` sortiert, aus Records und Events abgeleitet | `accepted` | **A0** | Entscheidungsblock CBP-WP-014 | 2026-07-22 | Registry-MVP | **ADR-0011** (A1) |
| **D-046** | **Teil A — Dokumentprofil: kanonisches JSON als JSON-kompatibles MVP-Profil des strikten YAML-Teilumfangs**; alle 31 Felddefinitionen unverändert (29 Pflicht + 2 optional). Keine allgemeine YAML-Unterstützung, keine externe Abhängigkeit; doppelte Schlüssel, `NaN`, `Infinity`, BOM, ungültiges UTF-8 und unbekannte Felder blockieren; optionale Felder bleiben optional. Präzisiert **D-031**, ändert ihn nicht | `accepted` | **A0** | Entscheidungsblock CBP-WP-015 | 2026-07-27 | Mapping-Draft-Validator | **ADR-0012** (A1) |
| **D-047** | **Teil B — externe read-only Registry-Bindung über `--source-id` und `--registry`; `source_id` ist kein Mapping-Feld.** Registry bytegenau unverändert; nur `collection`↔`collection_key` und `data_class`↔`data_class` exakt; **verbotene Crosswalks** `project`↔`domain_key`/`namespace`, `ai_transfer_policy`↔`ai_eligibility`, `location_reference`/`operator_reference`↔`source_id` | `accepted` | **A0** | Entscheidungsblock CBP-WP-015 | 2026-07-27 | Mapping-Draft-Validator | **ADR-0012** (A1) |
| **D-048** | **Teil C — genau eine deaktivierte synthetische Boundary mit bestehenden kanonischen Feldern/Werten.** Kein neues `slot:synthetic:`-Präfix, keine neuen Enum-Werte; `slot_id` ∈ {PS-02, PS-03, PS-04}; `location_reference` = belegter synthetischer V7-Platzhalter `synthetic-placeholder-*`; Subpath-Listen leer, `follow_symlinks=false`, `enabled=false`, `read_only=true`. Präzisiert **D-033**, ändert ihn nicht | `accepted` | **A0** | Entscheidungsblock CBP-WP-015 | 2026-07-27 | Mapping-Draft-Validator | **ADR-0012** (A1) |
| **D-049** | **Teil D — ausschließlich nicht persistierter, deterministischer Validierungsreport; Aktivierung immer verweigert.** `mapping_id` wird nach Vertrag (V4/V21) **validiert, nicht berechnet**; keine `map-`+SHA-256-Regel; `draft_sha256`/`policy_sha256` deterministisch; kein gespeicherter Report, keine Registry-Änderung; `VALID_DRAFT` bedeutet keine Freigabe und keine Aktivierung | `accepted` | **A0** | Entscheidungsblock CBP-WP-015 | 2026-07-27 | Mapping-Draft-Validator | **ADR-0012** (A1) |
| **D-050** | **Konsolidierte Freigabe des Mapping-Activation-Gate-Evaluators (WP-016): APPROVE IMPLEMENTATION WITH NOTES; A1** synthetisches Eingabe-/Evidenzmodell; **B1 – eng** (Ausgabestatus nur `NOT_EVALUATED`/`BLOCKED`; `READY FOR ACTIVATION DECISION`/`APPROVED FOR ACTIVATION`/`REVOKED` nicht emittierbar); **C1** fehlende/veraltete/NOT-EVALUATED/widersprüchliche Abhängigkeiten blockieren fail-closed, Human-only nie automatisch erfüllt; **D1** deterministischer, minimierter, nicht persistierter A6-Report. 20 Kriterien fest; Security Foundation/DRC keine Kriterien 21/22; keine Aktivierung, keine Persistenz | `accepted` | **A0** | Entscheidungsblock CBP-WP-016 | 2026-07-27 | Gate-Evaluator | **— (kein ADR)** |

> **Die vier Entscheidungen legen Sicherheitsarchitektur fest, keine
> Implementierung.** Es wurde keine Identität angelegt, kein Recht gesetzt,
> kein Secret bereitgestellt, keine Netzwerkregel verändert und kein Test
> ausgeführt. Alle zwölf Kontrollen stehen auf **DOCUMENTED ONLY**, das
> [Security Foundation Readiness Gate](../docs/operations/SECURITY_FOUNDATION_READINESS_GATE.md)
> auf **`NOT EVALUATED`**.

> **D-038 bis D-041 (CBP-WP-013) definieren einen lokalen, synthetisch
> testbaren Quarantäneprototyp — keine produktive Quarantäne.** Es wurde keine
> reale Quelle berührt, kein Mapping aktiviert, nichts freigegeben und nichts
> promotet. **R-01 und R-32 bleiben offen**; **OD-05 und OD-06 bleiben offen**.
> Festgehalten in [ADR-0010](../docs/decisions/ADR-0010-ingest-quarantaene-mvp.md).

> **D-042 bis D-045 (CBP-WP-014) definieren einen lokalen, synthetisch
> testbaren, deaktivierten Source-Registry-Prototyp — keine produktive
> Registry, kein Mapping, keine Aktivierung.** Keine reale Quelle, kein Pfad,
> keine URL, kein Source-Inhalt berührt; jede Registrierung ist
> `REGISTERED_DISABLED`; `activate` verweigert immer. **Kein Risiko
> geschlossen**; **OD-05, OD-06, OD-37, OD-38 bleiben offen**. Festgehalten in
> [ADR-0011](../docs/decisions/ADR-0011-deterministische-source-registry.md).

> **D-046 bis D-049 (CBP-WP-015) definieren einen lokalen, synthetisch
> testbaren, read-only Validator für Mapping-Entwürfe — kein gespeichertes
> Mapping, keine Aktivierung, keine Vertragsänderung.** Der angenommene Vertrag
> bleibt bei **31 Felddefinitionen** (29 Pflicht + 2 optional). Keine reale
> Quelle, kein Pfad, keine URL, kein Source-Inhalt berührt; die Registry bleibt
> bytegenau unverändert; `activation-check` verweigert immer. **Kein Risiko
> geschlossen**; **OD-05, OD-06, OD-37, OD-38 bleiben offen**; die
> Bildungsvorschrift von `mapping_id` bleibt offen. Festgehalten in
> [ADR-0012](../docs/decisions/ADR-0012-source-mapping-draft-validator.md).

> **Hinweis zu D-016.** In CBP-WP-002 hatte ich „bevorzugte Anwendungslaufzeit"
> zu „vorgesehene" abgeschwächt (Ü-02), gestützt auf Projektübergabe §4 (A5),
> wonach Containerisierung kein Pflichtziel der ersten Phase ist. Der Human
> Maintainer hat nun ausdrücklich „bevorzugte Anwendungslaufzeit" bestätigt.
> **A0 schlägt A5** — die Abschwächung ist damit aufgehoben.
>
> **Nachgeführt in CBP-WP-004:** `docs/architecture/PROJECT_DEFINITION.md`
> trägt jetzt die korrigierte Formulierung mit ausdrücklicher Abgrenzung
> („bevorzugt, aber nicht einzige Laufzeit und keine Produktgrenze"). OD-31 ist
> damit geschlossen; festgehalten in **ADR-0002**.

## Geschlossene offene Entscheidungen

| ID | War offen | Geschlossen durch | Datum |
| --- | --- | --- | --- |
| OD-12 | Prompt Mode „Lean" | D-009 | 2026-07-20 |
| OD-02 | Definition der Context Budgets | CONTEXT_BUDGETS.md; Restpunkt OD-02b | 2026-07-20 |
| OD-01 | Kriterien für Gate G0 | G0_SCOPE_LOCK_CRITERIA.md, dreistufig klassifiziert | 2026-07-20 |
| **OD-21** | Zugriffsweg für Mehrgeräte-Nutzung | **D-023** — privates VPN/Netz; Technologie bleibt Deployment Required | 2026-07-20 |
| **OD-27** | Obsidian-Synchronisationsmodell | **D-025** — serverzentriert zuerst, native Nutzung vertagt | 2026-07-20 |
| **OD-10** | Verfahren bei Secret in der Git-Historie | [SECRET_INCIDENT_RESPONSE.md](../docs/security/SECRET_INCIDENT_RESPONSE.md) — 14 Schritte, Rotation vor Cleanup. **Technische Unterstützung bleibt offen** | 2026-07-20 |
| **OD-32** | Berechtigungsstufen je Bereich und Freigabeverfahren | [PERMISSION_MODEL.md](../docs/security/PERMISSION_MODEL.md) und ADR-0004 — 9 Rollen × 12 Ressourcen. **Technische Durchsetzung bleibt offen** | 2026-07-20 |
| **OD-31** | Nachführungen außerhalb des CBP-WP-003-Scopes | CBP-WP-004: D-016 in `PROJECT_DEFINITION.md` korrigiert, Kriterienzahl auf 47 aktualisiert, Korrektur-Notiz in `CBP-WP-002.md` ergänzt | 2026-07-20 |
| **OD-34** | Secret-Store-Technologie und Credential-Reference-Format | **D-035** — versionierter, providerneutraler Referenzvertrag `cbp-secret:v1:<provider>:<opaque-id>` plus OS-geschützter Datei-Provider für den Pilot; festgehalten in [SECRET_REFERENCE_AND_PROVIDER_CONTRACT.md](../docs/security/SECRET_REFERENCE_AND_PROVIDER_CONTRACT.md). **Konkreter Ablageort, Dateimodi und registrierte Providernamen bleiben Deployment Required** | 2026-07-21 |
| **OD-35** | RT-2: Aufbewahrung, Integritätsschutz, Backup-/Restore-Nachweis | **D-037** — logisch append-only, verkettet, aufbewahrungs- und sicherungspflichtig; festgehalten in [OPERATIONAL_EVIDENCE_POLICY.md](../docs/operations/OPERATIONAL_EVIDENCE_POLICY.md). **Die konkrete Aufbewahrungsdauer bleibt Deployment Required** und wird im DRC geprüft | 2026-07-21 |
| **OD-26** | Endgültige Repository-Struktur | **D-029 und D-030** — Ziel-Monorepo nach Layout-Option B **und** Bereichsmodell W-3; festgehalten in [ADR-0007](../docs/decisions/ADR-0007-repository-und-workspace-grenze.md). **Keine Reorganisation autorisiert**; AB-03…AB-08 bleiben offen (OD-29) | 2026-07-21 |
| **OD-33** | Definition des Deployment-Readiness-Gates | [DEPLOYMENT_READINESS_CHECK.md](../docs/operations/DEPLOYMENT_READINESS_CHECK.md) und ADR-0005 — DRC vollständig dokumentiert und in G0, Manifest, Profil, README und Brain verlinkt | 2026-07-20 |

## Vertagte Entscheidungen

Nicht geschlossen, aber für den Pilotumfang **nicht mehr blockierend**:

| ID | Entscheidung | Grund der Vertagung |
| --- | --- | --- |
| OD-09 | Rechtsgrundlage für personenbezogene Daten | D-022 — keine PII im Pilot; Prüfung vor späterer Aufnahme |
| OD-20 | Programmiersprache, Suchmaschine, Embedding-Modell | Deployment Required |
| OD-22 | Sicherungsfrequenz und Sicherungsziel | Deployment Required |
| OD-30 | Backup- und Restore-Zielwerte | Deployment Required |

Vertagt heißt **nicht erledigt**. Diese Punkte gehören in das
Deployment-Readiness-Gate.

## Offene Entscheidungen

Legende: **P0** blockiert G0 · **P1** vor Architekturentscheidung · **P2** später.

| ID | Offene Entscheidung | Prio | Adressat | Bezug |
| --- | --- | --- | --- | --- |
| OD-03 | Rang der Kernprinzipien: weitere ADRs über ADR-0001 bis ADR-0005 hinaus | P1 | Human Maintainer | teilweise durch ADR-0001…0005 |
| OD-04 | Minimal nützlicher Funktionsumfang des Piloten | **P0** | Nova | A-8 |
| OD-05 | Ablageort des kanonischen Wissensbestands — **präzisiert:** Slot-Art entschieden (PS-02, `operator-managed`), konkreter Ort offen. **Vorgesehen für CBP-WP-010** | P1 | Human Maintainer | D-1 `accepted`; PILOT_SOURCE_MAPPING_PLAN |
| OD-06 | Quellen im ersten Scope — **präzisiert:** Quellen*arten* und Slot-Regeln entschieden, konkreter Bestand offen. **Vorgesehen für CBP-WP-010** | P1 | Human Maintainer | D-1 `accepted`; PILOT_SOURCE_MAPPING_PLAN |
| OD-07 | Vergabeverfahren für Autoritätsklassen A0–A6 | **P0** | Nova | — |
| OD-08 | Vergabeverfahren für Datenklassen | **P0** | Human Maintainer | D-4 |
| OD-11 | Repository dauerhaft privat? | **P0** | Human Maintainer | A-8 |
| OD-29 | Dauerhafte Behandlung der NDF-Abweichungen AB-03 bis AB-08 | **P0** | Nova + Human Maintainer | ADOPTION_NOTES |
| OD-02b | Kalibrierung der Token-Richtwerte für B0–B4 | P1 | Nova | CONTEXT_BUDGETS |
| OD-13 | Manifest auf `project-manifest.yaml` umstellen | P1 | Nova | AB-03 |
| OD-14 | NDF-Namensschema für Register | P1 | Nova | AB-04 |
| OD-15 | Schnitt einer Wissenseinheit | P1 | Nova | — |
| OD-16 | Bildungsvorschrift der stabilen Source-ID | P1 | Nova | — |
| OD-17 | Verpflichtende Frontmatter-Felder | P1 | Nova | — |
| OD-18 | Filterreihenfolge im Retrieval-Pfad | P1 | Nova | TB-4 |
| OD-19 | Umfang und Format des Retrieval-Trace | P1 | Nova | — |
| OD-23 | Lizenzwahl | P1 | Human Maintainer | D-007 |
| OD-25 | qmd als produktiver Suchdienst — nur nach Prüfung | P1 | Human Maintainer | — |
| **OD-36** | Bildungsvorschrift der `mapping_id`, zulässige Collection-Namen und deren Vergabe, unterstützte `schema_version`-Werte über `1.0` hinaus | P1 | Nova | ADR-0008; PILOT_SOURCE_MAPPING_SCHEMA |
| **OD-37** | Produktive Quarantäne-Isolation auf der Ziel-VM (KB-03, KB-04): OS-Rechte, getrennte Identität, Unzugänglichkeit für den Indexer | P1 | Human Maintainer | ADR-0010; **Deployment Required** |
| **OD-38** | Produktive Secret- und PII-Erkennung: Werkzeugauswahl, Erkennungsgüte, Verfahren nach D-019 | P1 | Nova + Human Maintainer | ADR-0010; R-01, R-32 |
| OD-24 | Akzeptable Ausfallzeit | P2 | Human Maintainer | — |
| OD-28 | Öffentlicher Produktname und Phase-7-Option | P2 | Human Maintainer | — |

## Zusammenfassung

| Kategorie | Anzahl |
| --- | --- |
| Getroffene Entscheidungen | **50** (davon **46** mit A0) |
| Angenommene ADRs | **12** (ADR-0001 bis ADR-0012, alle A1) |
| Vorgeschlagene ADRs | 0 |
| Neu in CBP-WP-003 | 12 (D-015 bis D-026) |
| Neu in CBP-WP-004 | 0 Entscheidungen, 5 ADRs |
| Neu in CBP-WP-007 | **2 A0-Entscheidungen** (D-027 G0, D-028 ADR-0006) |
| Neu in CBP-WP-008 | 0 Entscheidungen, 1 neue offene Entscheidung (OD-34) |
| Neu in CBP-WP-009 | **2 A0-Entscheidungen** (D-029 Teil A, D-030 Teil B), **1 ADR** |
| Neu in CBP-WP-010 | **3 A0-Entscheidungen** (D-031 Format, D-032 Collection, D-033 Granularität), **1 ADR**, 2 neue offene Entscheidungen (OD-35, OD-36) |
| Neu in CBP-WP-011 | **4 A0-Entscheidungen** (D-034 Identity, D-035 Secret, D-036 Egress, D-037 Evidence), **1 ADR**, **2 geschlossene** (OD-34, OD-35) |
| Neu in CBP-WP-013 | **4 A0-Entscheidungen** (D-038 Intake, D-039 Store, D-040 Scanner, D-041 Freigabe), **1 ADR**, 2 neue offene Entscheidungen (OD-37, OD-38) |
| Neu in CBP-WP-014 | **4 A0-Entscheidungen** (D-042 Identität, D-043 Store, D-044 Lifecycle, D-045 Katalog), **1 ADR**, 0 neue offene Entscheidungen |
| Neu in CBP-WP-015 | **4 A0-Entscheidungen** (D-046 Dokumentprofil, D-047 Registry-Bindung, D-048 Boundary, D-049 Report/Aktivierung), **1 ADR** (ADR-0012), 0 neue offene Entscheidungen |
| Neu in CBP-WP-016 | **1 konsolidierte A0-Entscheidung** (D-050 Gate-Evaluator: A1/B1-eng/C1/D1), **0 ADR**, 0 neue offene Entscheidungen |
| Geschlossene offene Entscheidungen | **12** |
| Vertagte Entscheidungen | 4 |
| Offene Entscheidungen | **23** |
| davon **P0** | **5** — OD-04, OD-07, OD-08, OD-11, OD-29 |

*Sämtliche Werte in CBP-WP-011 aus den Quelltabellen **ausgezählt**, nicht
fortgeschrieben (Zählregel 1 und 2). Jede gezählte Einheit ist einzeln
benennbar — kein offener Zusatz.*

> **Zu OD-35:** Die drei RT-2-Punkte waren inhaltlich bereits in ADR-0007 als
> „offene Folgefragen" benannt, aber in keinem Register geführt. Dieser Eintrag
> ist **keine Dublette**, sondern macht sie nachverfolgbar. Sie werden als
> **ein** Punkt geführt, nicht als drei.

> **Korrektur in CBP-WP-008 — vierter Zählfehler des Projekts.** Die
> Summenzeile führte zuvor **22 A0-Entscheidungen** und **8 offene
> P0-Entscheidungen**. Die Auszählung der Tabellen ergibt **24** und **6**. Die
> Tabellen selbst waren korrekt; nur die Summen stimmten nicht.
>
> Die sechs offenen P0-Punkte sind OD-04, OD-07, OD-08, OD-11, OD-26 und OD-29.
>
> **Der Fehler bestand seit CBP-WP-007 und wurde durch die Zähl- und
> Statusregel gefunden — aber erst ein Work Package später.** Genau deshalb
> bleibt **R-33 offen**: die Regel macht Fehler später sichtbar, sie verhindert
> sie nicht.

**Keine offene Entscheidung wird als A0 geführt.** Keine Entscheidung wurde aus
reinen Sachangaben abgeleitet — die Infrastrukturangaben aus dem Intake sind
Human-Evidenz, keine Beschlüsse.

## Pflege

Eine getroffene Entscheidung wird **nicht gelöscht**. Änderungen erfolgen durch
einen neuen Eintrag, der den alten als ersetzt kennzeichnet.
