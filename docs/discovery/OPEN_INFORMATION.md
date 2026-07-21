# Open Information — fehlende Eingangsinformation

| Feld | Wert |
| --- | --- |
| Phase | **Phase 0 COMPLETE** · Phase 1 AUTHORIZED FOR PLANNING |
| Überarbeitet in | **CBP-WP-009** |
| Autoritätsklasse | A2 |
| Stand | 2026-07-21 |

Dieses Dokument verzeichnet fehlende oder nicht zugängliche
**Eingangsinformation**.

---

## OI-01 — Zwei verbindliche Quellen lagen zunächst nicht vor

**Schweregrad:** hoch · **Status:** **GESCHLOSSEN** (2026-07-20, CBP-WP-002)

Beide Originalquellen wurden gelesen und abgeglichen, die Provenienz der
A6-Textfassung zur A4-PDF ist dokumentiert, keine ungeklärte inhaltliche
Abweichung. Vollständig in
[SOURCE_RECONCILIATION.md](SOURCE_RECONCILIATION.md).

**Verbleibende Einschränkung:** Der PDF-Fließtext war lokal nicht extrahierbar;
eine visuelle Detailprüfung wird nicht behauptet. Erfasst als R-22, R-23.

---

## OI-02 — Herkunft und Rang der Kernprinzipien

**Schweregrad:** mittel · **Status:** teilweise aufgelöst · **Adressat:** Human Maintainer

Inhaltliche Herkunft geklärt (20 bestätigte Übereinstimmungen). **Offen bleibt
der formale Rang** — die Prinzipien tragen A2 und sind nicht als ADR
ausgefertigt. Weiterverfolgt als OD-03 und G0-Kriterium F-3.

---

## OI-03 — Definition der Context Budgets B0–B4

**Schweregrad:** mittel · **Status:** **GESCHLOSSEN** (2026-07-20, CBP-WP-002)

Definiert in [../architecture/CONTEXT_BUDGETS.md](../architecture/CONTEXT_BUDGETS.md).
Kalibrierung der Token-Richtwerte als OD-02b offen.

---

## OI-04 — Gate-Kriterien für G0

**Schweregrad:** mittel · **Status:** **GESCHLOSSEN** (2026-07-20, CBP-WP-002),
**überarbeitet in CBP-WP-003**

47 Kriterien liegen vor, seit CBP-WP-003 dreistufig klassifiziert in Core
Required (25), Deployment Required (16) und Conditional (6).

**Gate-Status seit 2026-07-21: PASSED WITH NOTES** (A0, CBP-WP-007).

---

## OI-05 — Zielumgebung nicht verifiziert

**Schweregrad:** niedrig · **Status:** umklassifiziert · **Adressat:** Human Maintainer

Das Betriebsprofil ist entschieden (D-015). Die konkreten Werte sind bewusst
nicht erhoben und nun **Deployment Required**; geprüft werden sie im
[DRC](../operations/DEPLOYMENT_READINESS_CHECK.md), der auf **NOT EVALUATED**
steht.
---

## OI-06 — Benchmarkfragen

**Schweregrad:** hoch · **Status:** **GESCHLOSSEN** (2026-07-21, CBP-WP-005)

36 versionierte Benchmarkfragen liegen vor, verteilt auf sechs Kategorien
(24 Development / 12 Holdout), mit erwarteten Quellen, Antwortformen und
kritischen Fehlern. Erfolgsmetriken, Baseline-Protokoll und Dataset Governance
sind definiert. G-1 bis G-6 stehen auf `accepted`.

**Verbleibende Einschränkung:** Der Benchmark ist **entworfen, nicht
durchgeführt**. Es existiert keine Messung, kein Index, keine Suchsoftware.
Risiko R-21 bleibt deshalb `gemindert`, nicht geschlossen; die Pilotziele in
der Rubrik sind ungemessene Setzungen, und OD-02b bleibt offen.

Die ursprüngliche Abhängigkeit von der Bestandsgrößenordnung (D-2) hat sich
nicht als blockierend erwiesen: der Benchmark arbeitet auf einem kontrollierten
synthetischen Korpus und ist von der Größe des Realbestands unabhängig. Für die
**Kalibrierung** der Schwellenwerte bleibt sie relevant.
---

## OI-07 — Repository-Struktur nicht freigegeben

**Schweregrad:** mittel · **Status:** **GESCHLOSSEN** (2026-07-21, CBP-WP-009)

Drei Strukturvorstellungen stehen nebeneinander: Projektübergabe §13 (`core/`,
`deployments/`, `docs/`, `examples/`), NDF v1.0.0 und die aktuelle Struktur aus
CBP-WP-001.

Die Abweichungen AB-03 bis AB-08 bleiben nur **vorläufig für den Bootstrap**
akzeptiert. Siehe W-05, OD-26, OD-29.

**Aufgelöst am 2026-07-21** durch zwei getrennte A0-Entscheidungen in
CBP-WP-009: **D-029** wählt das Ziel-Monorepo nach Layout-Option B, **D-030**
das Bereichsmodell **W-3**. Festgehalten in
[ADR-0007](../decisions/ADR-0007-repository-und-workspace-grenze.md) (A1).
**OD-26 ist geschlossen.**

**Verbleibende Einschränkung:** Die Entscheidung autorisiert **keine
Reorganisation**. Das aktuelle Layout bleibt bestehen; die Migration braucht
ein separates, ausdrücklich freigegebenes Work Package und muss die
Git-Historie erhalten. **AB-03 bis AB-08 bleiben offen** (OD-29) — die
Layoutwahl beantwortet die NDF-Abweichungen nicht.

---

## OI-08 — Berechtigungsmodell

**Schweregrad:** hoch · **Status:** **GESCHLOSSEN** (2026-07-20, CBP-WP-004)

Der Intake hatte diesen Block bewusst nicht erhoben. Aufgelöst durch
[PERMISSION_MODEL.md](../security/PERMISSION_MODEL.md) und **ADR-0004**:
9 Rollen × 12 Ressourcen, fünf Aktionsklassen, fünf technische
Durchsetzungsebenen, Default deny. E-2 bis E-5 stehen auf `accepted`,
OD-32 ist geschlossen.

**Verbleibende Einschränkung:** Erfüllt ist die **dokumentarische**
Anforderung. Es existiert keine Anwendung, kein Dienstkonto, keine API.
**R-25 und R-27 bleiben ausdrücklich `offen`** — ein Berechtigungsmodell auf
Papier ist keine Zugriffskontrolle.

---

## OI-09 — Verfahren bei Secret in der Git-Historie

**Schweregrad:** hoch · **Status:** **GESCHLOSSEN** (2026-07-20, CBP-WP-004)

Aufgelöst durch
[SECRET_INCIDENT_RESPONSE.md](../security/SECRET_INCIDENT_RESPONSE.md):
14 Schritte, Rollenverteilung und zwei Reihenfolgeregeln — **Rotation vor
History Cleanup** und **Bereinigung vor Rebuild**. D-8 steht auf `accepted`,
OD-10 ist geschlossen.

**Verbleibende Einschränkung:** Es gibt keine automatische Erkennung, keine
technische Durchsetzung der Reihenfolge und keine Werkzeugunterstützung.
**R-01 bleibt `teilweise gemindert`**, nicht geschlossen.

---

## OI-10 — Konkreter produktiver Quellenbestand

**Schweregrad:** hoch · **Status:** **teilweise aufgelöst** (2026-07-21, CBP-WP-006)

**Aufgelöst:** Die **Quellenarten und ihre Regeln** sind definiert —
[PILOT_SOURCE_CONTRACT.md](../sources/PILOT_SOURCE_CONTRACT.md) mit sieben
logischen Source Slots, [SOURCE_SLOT_MODEL.md](../sources/SOURCE_SLOT_MODEL.md)
mit 24 Feldern und 10 Validierungsregeln. **D-1 steht auf `accepted`.**

**Weiterhin offen:** der **konkrete produktive Bestand**. Welche Verzeichnisse,
Repositories und Handoffs tatsächlich angebunden werden, ist nicht benannt.

**ADR-0006 wurde am 2026-07-21 angenommen** (D-028, A0). Die Ebenentrennung ist
damit bindend: private Bestände bleiben außerhalb des Kern-Repositorys. Die
konkrete Zuordnung erfolgt in Phase 1, Backlogpunkt **P2**.

Die Auflösung erfolgte über eine Ebenentrennung (ADR-0006, `proposed`):

| Ebene | Stand |
| --- | --- |
| Logical Source Slot — welche Art von Quelle, welche Regeln | **entschieden** |
| Deployment Mapping — welcher Ort in einer Installation | **offen**, fail-closed im DRC |

**D-1 `accepted` bedeutet nicht, dass eine Quelle angebunden wurde.** Es
bedeutet, dass der zulässige Quellenraum definiert und begrenzt ist.

Verbleibend: **OD-05** (Ablageort des kanonischen Bestands, von P0 auf P1
präzisiert) und **OD-06** (konkrete Quellen und Nicht-Quellen, ebenfalls P1).
Beide bleiben offen und werden im Deployment Mapping beziehungsweise mit dem
Human Maintainer geklärt.

**Stand nach CBP-WP-008:** Das **Schema** eines Deployment Mappings liegt vor
([PILOT_SOURCE_MAPPING_PLAN.md](../roadmap/PILOT_SOURCE_MAPPING_PLAN.md), 19
Felder, fail-closed Defaults). **Es existiert kein einziges Mapping.** OD-05 und
OD-06 bleiben offen; vorgesehen für CBP-WP-010, ausdrücklich erst nach
Human-Eingabe.

---

## OI-11 — Secret-Store-Technologie nicht bestimmt

**Schweregrad:** mittel · **Status:** **NEU** (2026-07-21, CBP-WP-008) ·
**Adressat:** Human Maintainer

Kontrollbereich **KB-08** und das Mappingfeld `location_reference` setzen einen
Secret Store voraus, auf den ausschließlich **verwiesen** wird. Weder die
Technologie noch das Verweisformat sind bestimmt, und die Frage war bisher in
keinem Register geführt.

Aufgenommen als **OD-34**. Blockiert CBP-WP-012, nicht die aktuelle Planung.
---

## Bearbeitung

Ein Eintrag wird nicht gelöscht, sondern auf `geschlossen` gesetzt und mit der
auflösenden Quelle oder Entscheidung verknüpft.
