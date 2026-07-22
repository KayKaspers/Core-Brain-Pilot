# ADR-0011 — Deterministische Source Registry und Catalog

| Feld | Wert |
| --- | --- |
| Status | **accepted** |
| Datum | 2026-07-22 |
| Entscheider | **Human Maintainer** |
| Angenommen am | **2026-07-22** |
| Autorität | **A0** — vier getrennte direkte Human-Maintainer-Entscheidungen |
| Supersedes | — |
| Superseded by | — |
| Entschieden in | **CBP-WP-014** |
| Belegt durch | ADR-0007, ADR-0008, ADR-0009, ADR-0010, PILOT_SOURCE_MAPPING_SPECIFICATION (A2) |
| Schließt | **keine** offene Entscheidung — OD-05, OD-06, OD-37, OD-38 bleiben offen |

> **Dieser ADR ist angenommen und bindend.** Er trägt Autoritätsklasse **A1**.
> Die zugrunde liegenden Human-Entscheidungen (D-042 bis D-045) tragen **A0**.
>
> **Er beschreibt einen lokalen, synthetisch testbaren, deaktivierten
> Prototyp.** Er ist **keine** produktive Registry, **kein** Source Mapping,
> **keine** Source-Aktivierung, **kein** Ingest, **kein** Index und **kein**
> Retrieval. Keine reale Quelle wird durch diesen ADR autorisiert.

---

## Kontext

**ADR-0008** legt die Pilot-Source-Mapping-Konvention fest; **ADR-0006/0007**
verankern logische Source Slots außerhalb des Core-Repositorys. Bevor ein
Mapping aktiviert werden kann, braucht es eine **deterministische,
auditierbare Identität** je Quelle. CBP-WP-014 baut einen Registry-Prototyp,
der genau diese Identität, Klassifikation und einen minimalen Lifecycle
katalogisiert — **ohne** bereits eine Source Boundary, einen Zugriffsweg oder
eine Aktivierung einzuführen. Vier Fragen mussten entschieden werden:

| Frage | Wirkt auf |
| --- | --- |
| **Wie entsteht Identität?** | Reproduzierbarkeit, Idempotenz, Konflikterkennung |
| **Wie wird gespeichert?** | Integrität, Rekonstruierbarkeit, Listenansichten |
| **Welcher Lifecycle?** | Auditierbarkeit ohne Aktivierung oder Löschung |
| **Was steht im Katalog?** | Minimierung, keine vorweggenommene Source Boundary |

## Entscheidung

### D-042 — Registry-Identität (Teil A)

**Stabiler Namespace plus Source Key, daraus deterministisch abgeleitete
Source ID.** Die Identität besteht ausschließlich aus Identitätsschema-Version,
normalisiertem `namespace` und `source_key`; die Source ID ist
`src-` + die ersten 24 Hex-Zeichen des SHA-256 und enthält **keinen** Display
Name, Pfad, URL oder Inhalt. Dieselbe Identität ergibt dieselbe Source ID;
abweichende Identität oder Definition unter bestehender ID blockiert
(Konflikt).

### D-043 — Registry-Speicher (Teil B)

**Unveränderliche JSON-Records plus atomar abgeleiteter Katalog außerhalb des
Repositorys.** Kanonisches UTF-8-JSON, atomare Erstellung/Ersetzung, keine
stillschweigende Überschreibung, Idempotenz, Konflikt bei abweichender
Definition, keine Hard-/Symlinks, kein Schreiben außerhalb des Roots, kein
Teilkatalog bei Integritätsfehler, vollständige Rekonstruierbarkeit. Der
Speicher ist **weder Canonical Source noch RT-2** und **keine** produktive
Sicherheits- oder Isolationsgrenze.

### D-044 — Lifecycle (Teil C)

**`REGISTERED_DISABLED` und `RETIRED`; Retirement als append-only Event; keine
Aktivierung.** Keine Record-Löschung, keine Aktualisierung, keine
Reaktivierung; identisches Retirement ist idempotent; keine Freitextbegründung,
keine Pfade oder Inhalte im Event. `RETIRED` bedeutet ausschließlich, dass die
synthetische Identität als stillgelegt geführt wird.

### D-045 — Katalogumfang (Teil D)

**Ausschließlich minimierte Metadaten; keine Pfade, URLs, Source-Inhalte oder
Mapping-Locators.** Zehn Felder je Eintrag (`source_id`, `namespace`,
`source_key`, `display_name`, `collection_key`, `domain_key`, `source_kind`,
`data_class`, `ai_eligibility`, `lifecycle_state`); **keine** `source_reference`,
kein Definition Hash, kein Owner-Freitext. Deterministisch nach `source_id`
sortiert, ausschließlich aus Records und Events abgeleitet.

## Trust Boundary

Die Registry sitzt **vor** jeder Aktivierung und jedem Mapping. Sie definiert
**keine** Source Boundary und **keinen** Zugriffsweg. Die
**Synthetic-only-Grenze** ist technisch durchgesetzt: jede schreibende
Operation verlangt das Flag `--synthetic-test-only`, `synthetic_test_only =
true`, `source_reference` mit Präfix `synthetic:` sowie
`activation_enabled`/`content_access_enabled`/`network_enabled` gleich `false`.

## Konsequenzen

| Wirkung | Beschreibung |
| --- | --- |
| **Datenschutz** | Records und Katalog enthalten keine Pfade, URLs, Inhalte oder personenbezogenen Daten; nur normalisierte Metadaten |
| **Secret** | Es wird **kein** Secret referenziert oder aufgelöst; `source_reference` ist opak (`synthetic:`) |
| **Portabilität** | Reine Standardbibliothek, kein Netzwerk, kein Dienst; der Speicher ist ein lokales Dateilayout ohne Datenbank |
| **Integrität** | Unveränderliche Records/Events, atomare Schreibweise, deterministische IDs, Katalog vollständig rekonstruierbar; ein beschädigter Record blockiert den Gesamtkatalog |
| **Idempotenz** | Identische Registrierung und identisches Retirement sind idempotent; abweichende Definition/Identität blockiert |
| **Aufbewahrung** | Der Prototyp erzeugt **keine** RT-2 Operational Evidence; alle Records sind aus synthetischen Definitionen reproduzierbar |

## Verworfene Alternativen

- **A2 (zufällige UUID):** keine Reproduzierbarkeit, keine Konflikterkennung; verworfen.
- **B2 (nur flüchtige Validierung):** kein auditierbarer Bestand; verworfen.
- **C2 (nur REGISTERED_DISABLED ohne Event):** kein minimaler Lifecycle-Nachweis; verworfen.
- **D2 (Locators im Katalog):** würde eine Source Boundary vorwegnehmen; verworfen.

## Aussagegrenzen

- Kein produktiver Ingest, kein Mapping, keine Aktivierung, keine Indexierung, kein Retrieval.
- `.gitignore` und OS-Rechte sind **keine** durchgesetzte Sicherheitsgrenze.
- Der Netzwerk-Guard belegt Netzwerkfreiheit der getesteten CLI-Pfade, **nicht** Deployment-Isolation, Firewall oder VM-Egress.
- Der Registry-Prototyp ist **keine** reale Source Governance.

## Offene Folgefragen

**OD-05, OD-06, OD-37 und OD-38 bleiben offen.** Dieser ADR entscheidet die
vier MVP-Teilfragen der Registry, nicht den konkreten Quellenbestand, den
Ablageort des kanonischen Bestands, die produktive Isolation oder die
produktive Secret-/PII-Erkennung.

## Verhältnis zum Autoritätsmodell

Ein angenommener ADR (A1) schlägt README (A4), abgeleitete Zusammenfassungen
(A6) und Projektchat-Übergaben (A5). Er wird nur durch einen ausdrücklichen
Human-Maintainer-Beschluss (A0) oder einen späteren ADR verdrängt.
