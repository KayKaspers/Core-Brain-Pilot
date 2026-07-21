# ADR-0007 — Repository-Zielstruktur und Workspace-Grenze

| Feld | Wert |
| --- | --- |
| Status | **accepted** |
| Datum | 2026-07-21 |
| Entscheider | **Human Maintainer** |
| Angenommen am | **2026-07-21** |
| Autorität | **A0** — direkte Human-Maintainer-Entscheidung |
| Supersedes | — |
| Superseded by | — |
| Vorbereitet in | CBP-WP-008 · entschieden in **CBP-WP-009** |
| Belegt durch | ADR-0006 (A1), ADR-0003, ADR-0001, Übergabe §13 (A5), REPOSITORY_LAYOUT_OPTIONS (A3), REPOSITORY_AND_WORKSPACE_PLAN (A3) |
| Schließt | **OD-26** |

> **Dieser ADR ist angenommen und bindend.** Er trägt Autoritätsklasse **A1**.

---

## Kontext

**OD-26** war seit CBP-WP-001 offen und bestand aus **zwei unabhängigen
Teilfragen**, die bis CBP-WP-008 nicht getrennt waren:

| Teil | Frage | Vorlage |
| --- | --- | --- |
| **A** | Welche Zielstruktur hat das allgemeine Core-Repository? | [REPOSITORY_LAYOUT_OPTIONS.md](../architecture/REPOSITORY_LAYOUT_OPTIONS.md) — Optionen A/B/C |
| **B** | Wo verläuft die Grenze zu privaten Operator-Daten? | [REPOSITORY_AND_WORKSPACE_PLAN.md](../roadmap/REPOSITORY_AND_WORKSPACE_PLAN.md) — Modelle W-1/W-2/W-3 |

Drei Strukturvorstellungen standen nebeneinander: Projektübergabe §13 (A5),
NDF v1.0.0 (A1) und die gewachsene Struktur aus CBP-WP-001 (A2). Die
Abweichungen AB-03 bis AB-08 waren nur **vorläufig für den Bootstrap**
akzeptiert (W-05, OI-07, OD-29).

**ADR-0006** hatte bereits bindend festgelegt, dass private und produktive
Wissensbestände außerhalb des allgemeinen Core-Repositorys bleiben — ohne zu
bestimmen, **wo** sie stattdessen liegen. Genau diese Lücke schließt Teil B.

---

## Human-Entscheidung Teil A

*Wortlaut aus dem Entscheidungsblock, unverändert übernommen:*

> **SELECT A2 – Ziel-Monorepo nach Layout-Option B**
>
> Die langfristige Zielstruktur des allgemeinen Core-Repositorys verwendet
> getrennte Bereiche für:
>
> - core/
> - adapters/
> - deployments/
> - config/
> - docs/
> - examples/
> - tests/
>
> Diese Entscheidung autorisiert noch keine Verschiebung, Umbenennung oder
> Reorganisation bestehender Dateien und Ordner.
>
> Das aktuelle Layout bleibt bestehen, bis ein separates, ausdrücklich
> freigegebenes Migrations-Work-Package vorliegt.
>
> Die Migration muss nachvollziehbar, schrittweise, rücksetzbar und ohne
> Verlust der Git-Historie geplant werden.

## Human-Entscheidung Teil B

*Wortlaut aus dem Entscheidungsblock, unverändert übernommen:*

> **SELECT B3 – privater Operator-Workspace außerhalb des Core-Repositorys**
>
> Private und produktive Wissensbestände, konkrete Source Mappings, private
> Collection-Konfigurationen sowie operatorbezogene kanonische
> Registry-Metadaten liegen außerhalb des allgemeinen Core-Repositorys.
>
> Der private Operator-Workspace darf lokal betrieben und später bei Bedarf in
> ein getrenntes privates Repository nach W-2 überführt werden.
>
> Der Runtime-Datenbereich bleibt ein dritter, separater Bereich für abgeleitete
> und betriebliche Daten wie:
>
> - Suchindex,
> - Cache,
> - temporäre Context Packs,
> - Jobs,
> - Auditdaten,
> - weitere Derived Data.
>
> Secrets dürfen weder im Core-Repository noch im Operator-Workspace im
> Klartext gespeichert werden. Dort sind nur Verweise auf einen getrennten
> Secret Store zulässig.
>
> Eine Runtime-Kopie der Source Registry darf niemals die einzige Quelle der
> kanonischen Registry-Metadaten sein.

---

## Entscheidung

**Das Projekt führt drei getrennte Bereiche mit unterschiedlichem Lebenszyklus
und unterschiedlicher Veröffentlichbarkeit.**

### 1. Core Repository — Zielstruktur

| Bereich | Inhalt |
| --- | --- |
| `core/` | Deployment-neutraler Kern |
| `adapters/` | Austauschbare Adapter — Suche, UI, Backup, MCP |
| `deployments/` | Profilspezifische Vorlagen **ohne private Werte** |
| `config/` | Konfigurationsvorlagen, **keine Werte** |
| `docs/` | Architektur, Betrieb, Sicherheit, Governance |
| `examples/` | **Synthetische** Beispielbestände |
| `tests/` | Unit, Integration, Retrieval-Benchmark |

Die NDF-Artefakte `project-system/`, `project-brain/` und `work-packages/`
bleiben erhalten.

**Das Core Repository wird `publication-capable by design` gestaltet.**

| Das bedeutet | Das bedeutet **nicht** |
| --- | --- |
| Private Wissensbestände sind ausgeschlossen | öffentliche Freigabe |
| Produktive Source Mappings sind ausgeschlossen | Open-Source-Freigabe |
| Secrets sind ausgeschlossen | Lizenzentscheidung |
| Synthetische Fixtures dürfen enthalten sein | Branding-Freigabe |
| Allgemeiner Code, Architektur, Governance und Vorlagen dürfen enthalten sein | Release-Autorisierung |
| | Zusicherung, dass alle **aktuellen** Dokumente öffentlich geeignet sind |

**Das Repository bleibt zunächst privat.** Eine öffentliche Veröffentlichung
benötigt eine **separate, ausdrückliche Human-Maintainer-Entscheidung mit
Autorität A0** — OD-11 ist offen, OD-23 (Lizenz) und OD-28 (Produktname)
ebenfalls. Die Sperrlisteneinträge zu öffentlichem Branding, Release und
Veröffentlichung in [DO_NOT_START.md](../product/DO_NOT_START.md) bleiben
bestehen.

> `publication-capable by design` beschreibt eine **Bauweise**, keinen
> Freigabezustand: Es müsste nichts herausgelöst werden, *falls* jemand
> veröffentlichen wollte. Ob, wann und in welcher Form das geschieht, ist
> unentschieden.

### 2. Privater Operator-Workspace — außerhalb des Core-Repositorys

| Enthält | Enthält **nicht** |
| --- | --- |
| Konkrete Source Mappings | **Secrets im Klartext** |
| Private Collection-Konfiguration | Anwendungscode |
| **Operatorbezogene kanonische Registry-Metadaten** | Architektur oder Governance |
| Lokale Betriebsparameter | Derived Data |
| **Verweise** auf den Secret Store | |

**Kanonisch und damit sicherungspflichtig.** Keine Verpflichtung zur
Veröffentlichung. Lokaler Betrieb zulässig; spätere eigene Versionierung
zulässig.

### 3. Runtime-Datenbereich — dritter, separater Bereich

**Nicht kanonisch, aber auch nicht durchgehend reproduzierbar.** Der Bereich
zerfällt in **drei Unterklassen** mit verschiedenen Aufbewahrungs- und
Backupanforderungen. Sie pauschal als „Cache" zu behandeln wäre falsch.

#### RT-1 — Rebuildable Derived Data

Suchindex · Embeddings · Cache · generierte Context Packs · Suchprojektionen ·
abgeleitete Katalogansichten · temporäre Visualisierungsdaten.

| Eigenschaft | Regel |
| --- | --- |
| Klasse | nicht kanonisch |
| Erzeugung | aus kanonischen Quellen, Registry-Metadaten und **versionierter** Konfiguration neu erzeugbar |
| Löschung | verursacht **keinen** kanonischen Wissensverlust |
| Rebuild | muss **überprüfbar** sein |
| Versionierung | nicht als Laufzeitbestand im Core-Git-Repository |

#### RT-2 — Operational Evidence

Auditlogs · Approval- und Review-Nachweise · Incident Records ·
Sicherheitsereignisse · abgeschlossene Jobhistorie · Lösch- und
Rebuild-Nachweise · Restore-Nachweise.

| Eigenschaft | Regel |
| --- | --- |
| Klasse | **kein kanonischer Wissensbestand — aber auch kein Cache** |
| Reproduzierbarkeit | **nicht notwendigerweise gegeben** |
| Behandlung | **darf nicht pauschal als Cache behandelt werden** |
| Aufbewahrung | **erforderlich, definiert** |
| Zugriffsschutz | **erforderlich** |
| Integrität | gegebenenfalls Integritätsnachweise erforderlich |
| Backup | muss von der späteren Betriebs- und Backupentscheidung erfasst werden |
| Ablage | **gehört nicht in das allgemeine Core-Git-Repository** |

Operational Evidence **darf** technisch append-only oder anderweitig
manipulationsgeschützt gestaltet werden. **In diesem ADR wird dafür keine
Technologie ausgewählt.**

#### RT-3 — Transient Runtime State

Temporäre Dateien · Locks · aktive Jobzustände · kurzlebige
Verarbeitungspuffer · **nicht freigegebene** temporäre Context Packs.

| Eigenschaft | Regel |
| --- | --- |
| Klasse | nicht kanonisch |
| Verwerfbarkeit | kontrolliert verwerfbar |
| Abbruch | nach Abbruch **sicher bereinigbar** |
| Neustart | **darf nach einem Neustart nicht zur alleinigen Statuswahrheit werden** |

> **Nur RT-1 ist beliebig wiederherstellbar.** RT-2 nicht — ein verlorener
> Auditnachweis ist verloren. RT-3 soll gar nicht überleben.

---

## Grenzen

Diese Grenzen gelten unabhängig von jeder späteren Ausgestaltung:

| # | Grenze |
| --- | --- |
| **G1** | **Private oder produktive Wissensbestände liegen nie im allgemeinen Core-Repository** |
| **G2** | **Secrets liegen weder im Core-Repository noch im Operator-Workspace im Klartext** — dort ausschließlich Verweise |
| **G3** | **`.gitignore` ist keine Sicherheitsgrenze.** Es schützt vor Unachtsamkeit, nicht vor `git add -f`, und wirkt nicht auf bereits verfolgte Dateien |
| **G4** | Der Operator-Workspace liegt **außerhalb** des Core-Repositorys — nicht als ignorierter Unterordner |
| **G5** | **Eine Runtime-Projektion der Source Registry ist nie die einzige Quelle kanonischer Registry-Metadaten** |
| **G9** | **Operational Evidence (RT-2) wird nicht als Cache behandelt** — sie braucht Aufbewahrung, Zugriffsschutz und Sicherung |
| **G10** | **Transient Runtime State (RT-3) ist nie die alleinige Statuswahrheit** nach einem Neustart |
| **G6** | Private Mappings und private Registry-Metadaten dürfen **nicht durch einen allgemeinen Core-Push veröffentlicht werden können** |
| **G7** | **Registry-Schema** (Core Repository) und **konkrete Registry-Metadaten** (Operator-Workspace) bleiben getrennt |
| **G8** | Diese Entscheidung autorisiert **keine** Verschiebung, Umbenennung oder Reorganisation |

**G3 ist der Grund für G4.** Wäre der Workspace ein ignorierter Unterordner,
ruhte die gesamte Trennung auf einer Textdatei, die jede Komponente mit
Schreibrecht ändern kann.

**G6 folgt aus G4:** Was außerhalb des Repositorys liegt, kann ein `git push`
nicht erfassen. Das ist eine strukturelle Eigenschaft, keine Regel, an die sich
jemand erinnern muss.

### Registry-Grenze im Einzelnen

Die Source Registry existiert an **zwei** Orten mit **verschiedenem Rang**.
Diese Unterscheidung ist die Grundlage von G5 und G7.

| # | Gegenstand | Ort | Rang |
| --- | --- | --- | --- |
| **1** | Registry-**Schema**, allgemeine Validierungsregeln, **synthetische** Beispiele | **Core Repository** | veröffentlichungsfähig |
| **2** | Konkrete **operatorbezogene kanonische** Registry-Metadaten | **privater Operator-Workspace** oder später ein getrenntes privates Repository | **kanonisch** |
| **3** | **Runtime-Projektion** der Registry für Suche und Betrieb | Runtime-Datenbereich, RT-1 | **abgeleitet** |

| # | Regel |
| --- | --- |
| **RG-1** | Eine Runtime-Projektion **darf** für Suche und Betrieb existieren |
| **RG-2** | **Diese Runtime-Projektion ist nicht die kanonische Registry** |
| **RG-3** | Der Verlust der **einzigen** kanonischen Registry-Metadaten wäre **Datenverlust** und ist **nicht** durch einen normalen Index-Rebuild behebbar |
| **RG-4** | Operatorbezogene Registry-Metadaten **und** Operational Evidence (RT-2) benötigen später **eigene Backup- und Restore-Nachweise** |

**RG-3 ist der Kern.** Ein Rebuild erzeugt die Projektion neu — aus den
kanonischen Metadaten. Fehlen diese, erzeugt er nichts.

---

## Konsequenzen

| Gegenstand | Wirkung |
| --- | --- |
| Zielstruktur | **Festgelegt** — sieben Bereiche, verbindlich für spätere Arbeit |
| Aktuelles Layout | **Bleibt unverändert bestehen** bis zu einem eigenen Migrations-Work-Package |
| Migration | Muss **nachvollziehbar, schrittweise, rücksetzbar und ohne Verlust der Git-Historie** geplant werden |
| Operator-Workspace | **Noch nicht angelegt.** Anlage ist nicht Teil dieses Work Packages |
| Runtime-Bereich | **Noch nicht angelegt** |
| CBP-WP-010 | Kann beginnen — die Bereichsgrenze steht; ausgefüllte Mappings gehören in den Workspace |
| ADR-0006 | **Bleibt `accepted`**; ADR-0007 konkretisiert ihn, ersetzt ihn nicht |
| AB-03…AB-08 | **Bleiben offen** (OD-29) — die Layoutwahl beantwortet die NDF-Abweichungen nicht |
| Capabilities | **Unverändert 0 von 29 implementiert** |

> **Eine Strukturentscheidung ist kein Fortschritt am System.** Es wurde nichts
> gebaut, nichts verschoben und nichts angelegt.

## Datenschutzwirkung

**Hoch positiv, aber noch nicht wirksam.**

| Aspekt | Wirkung |
| --- | --- |
| Trennung | Beruht auf einer **Pfadgrenze**, nicht auf Disziplin |
| Schwächer als W-2 | Eine Repository-Grenze wäre strenger als eine Pfadgrenze |
| Secrets | Weiterhin **nur Verweise**; Technologie offen (OD-34) |

### Was W-3 für R-01 tatsächlich leistet

**Gemindert wird genau ein Pfad:**

```text
private Information
  → versehentlich in Core aufgenommen
    → allgemeiner Core-Push
      → unbeabsichtigte Veröffentlichung
```

**W-3 implementiert nicht:**

| Nicht implementiert | Zuständig |
| --- | --- |
| Secret-Erkennung | KB-08, CBP-WP-012 |
| Secret-Rotation | SECRET_INCIDENT_RESPONSE |
| Secret Store | **OD-34**, offen |
| Scanning | CBP-WP-013 |
| Zugriffskontrolle | KB-01…KB-05, CBP-WP-012 |

**R-01 bleibt offen — teilweise gemindert ausschließlich hinsichtlich des
Veröffentlichungspfads.** Ein Secret, das jemand direkt in eine Core-Datei
schreibt, wird durch W-3 in keiner Weise erkannt oder verhindert.

## Git- und Veröffentlichungswirkung

| Aspekt | Wirkung |
| --- | --- |
| Core-Historie | Bleibt klein und **publication-capable by design** — **nicht** zur Veröffentlichung freigegeben |
| **Aktuelle Sichtbarkeit** | **privat** — unverändert |
| **Öffentliche Freigabe** | benötigt eine **separate A0-Entscheidung**; OD-11 offen |
| Operator-Workspace | Von jedem Core-Push **konstruktiv ausgeschlossen** (G6) |
| Runtime-Bereich | Nie versioniert |
| Migration | Darf die Git-Historie **nicht verlieren** — ausdrückliche Auflage |
| **OD-11** | **Bleibt offen** — die Sichtbarkeit des Core-Repositorys ist nicht entschieden |

**B3 setzt OD-11 nicht voraus.** Das war der Grund, W-3 vor W-2 zu wählen: W-2
hätte eine Aussage über Sichtbarkeit und Ablageort implizit vorweggenommen.

## Backupwirkung

**Fünf Sicherungsverträge, nicht drei** — der Runtime-Bereich zerfällt in
RT-1, RT-2 und RT-3.

| Bereich | Sicherungspflicht | Wiederherstellung |
| --- | --- | --- |
| Core Repository | ja | Git plus Backup |
| **Operator-Workspace** | **ja — kanonisch** | **nur aus Backup**, nicht durch Rebuild |
| RT-1 Rebuildable Derived Data | **nein** | **Rebuild** |
| **RT-2 Operational Evidence** | **ja** — Aufbewahrung und Zugriffsschutz definiert | **nur aus Backup**; **nicht rekonstruierbar** |
| RT-3 Transient Runtime State | nein | **gar nicht** — kontrolliert verwerfen |

**Zwei kritische Sicherungsgegenstände, nicht einer:**

1. **Der Operator-Workspace** enthält kanonische Registry-Metadaten, die aus
   dem Index nicht rekonstruierbar sind (G5, RG-3).
2. **Operational Evidence (RT-2)** — Auditlogs, Approval-Nachweise, Incident
   Records und Restore-Nachweise — lässt sich ebenfalls **nicht vollständig
   rekonstruieren**. Ein verlorener Auditnachweis ist verloren.

Beide sind in die spätere Backup-, Restore- und Aufbewahrungsregelung
einzubeziehen (RG-4). **Eine Technologie wird hier nicht gewählt.**

**R-20 bleibt offen:** Es wurde kein Restore durchgeführt — für keinen der fünf
Bereiche.

## Portabilitätswirkung

| Aspekt | Wirkung |
| --- | --- |
| Deployment-Neutralität | **Gestärkt** — `deployments/` bildet die fünf Profile ab, `core/` bleibt frei davon |
| Kern ohne Bestand | Vollständig beschreib- und ausliefbar |
| Adaptertausch | `adapters/` macht Suche, UI, Backup und MCP austauschbar |
| Zweite Installation | Braucht nur einen eigenen Workspace, kein zweites Core |

Bestätigt **ADR-0001**: Proxmox bleibt Referenzplattform, nicht Produktgrenze.

## Migrationspfad

| Schritt | Inhalt | Autorisiert |
| --- | --- | --- |
| 1 | **Entscheidung** — dieser ADR | **ja, erfolgt** |
| 2 | Migrations-Work-Package planen: Reihenfolge, Rücksetzpunkte, Historienerhalt | nein |
| 3 | Core-Layout schrittweise herstellen | **nein** |
| 4 | Operator-Workspace außerhalb anlegen | **nein** |
| 5 | Runtime-Bereich definieren | **nein** |
| 6 | Erste Mappings im Workspace ablegen (CBP-WP-010) | nein |
| 7 | *Optional später:* Workspace nach **W-2** überführen | nein |

**Nur Schritt 1 ist erfolgt.** Schritt 3 ist der einzige, der bestehende
Dateien bewegt — ausschließlich innerhalb des Core-Repositorys, schrittweise,
rücksetzbar und ohne Verlust der Git-Historie.

**Schritt 7 bleibt möglich, ist aber nicht beschlossen.** Der Workspace ist so
zu schneiden, dass die spätere Überführung nach W-2 eine **Initialisierung**
bleibt, keine Migration.

## Verworfene und vertagte Alternativen

| Option | Bewertung |
| --- | --- |
| **A1** — aktuelles Layout als Zielzustand | **verworfen.** Kein Ort für Adapter, Deploymentprofile und Tests; die Struktur entstünde später ungeplant |
| **A3** — Strukturentscheidung vertagen | **verworfen.** Der Migrationsaufwand ist heute am geringsten, weil kein Code existiert |
| **B1 / W-1** — ein gemeinsames Repository | **verworfen.** Widerspricht ADR-0006; begünstigt R-01 strukturell |
| **B2 / W-2** — getrenntes privates Repository | **vertagt, nicht verworfen.** Strenger, setzt aber OD-11 und OD-05 voraus — beide offen. Bleibt der vorbereitete nächste Schritt |
| **B4** — Bereichsentscheidung vertagen | **verworfen.** Ohne Bereichsgrenze wäre jedes Mapping ortlos; CBP-WP-010 bliebe blockiert |

## Offene Folgefragen

| Punkt | Register | Status |
| --- | --- | --- |
| Ablageort des kanonischen Bestands | **OD-05** | **offen** |
| Konkrete Quellen und Nicht-Quellen | **OD-06** | **offen** |
| Repository-Sichtbarkeit | **OD-11** | **offen** |
| NDF-Abweichungen AB-03…AB-08 | **OD-29** | **offen** |
| Secret-Store-Technologie und Verweisformat | **OD-34** | **offen** |
| Manifestformat `PROJECT_MANIFEST.md` gegen `project-manifest.yaml` | OD-13 | offen |
| Zeitpunkt und Zuschnitt der Migration | **neu** | eigenes Work Package erforderlich |
| Übergang nach W-2 | **neu** | optional, nicht beschlossen |
| **Aufbewahrungsfrist für RT-2 Operational Evidence** | **neu** | offen |
| **Integritätsschutz für RT-2** (append-only oder gleichwertig) | **neu** | offen — **keine Technologie gewählt** |
| **Backup- und Restore-Nachweise für Workspace und RT-2** | **neu** | offen (RG-4) |
| Öffentliche Veröffentlichung des Core-Repositorys | **OD-11** | **offen — benötigt A0** |

**Keine dieser Fragen wird durch ADR-0007 beantwortet.** Die Entscheidung legt
Zielstruktur und Bereichsgrenze fest — nicht, was in den Bereichen liegt.
