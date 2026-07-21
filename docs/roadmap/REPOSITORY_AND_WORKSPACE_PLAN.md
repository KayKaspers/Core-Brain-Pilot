# Repository and Workspace Plan — Entscheidungsvorbereitung OD-26

| Feld | Wert |
| --- | --- |
| **Status der Empfehlung** | **ANGENOMMEN** — Modell **W-3** gewählt |
| Stream | F1 · Backlogpunkt P1 |
| Erfasst in | CBP-WP-008 · **entschieden in CBP-WP-009** |
| Autoritätsklasse | A3 |
| Baut auf | [REPOSITORY_LAYOUT_OPTIONS.md](../architecture/REPOSITORY_LAYOUT_OPTIONS.md) (A3, CBP-WP-004) |
| Betrifft | **OD-26 — geschlossen**; OD-05, OD-11, OD-29 bleiben offen |
| Stand | 2026-07-21 |

> **Entscheidung liegt vor.** Der Human Maintainer hat am 2026-07-21 **Modell
> W-3** gewählt — **D-030**, Autorität **A0**, festgehalten in
> [ADR-0007](../decisions/ADR-0007-repository-und-workspace-grenze.md).
> Gemeinsam mit **D-029** (Layout-Option B) schließt das **OD-26**.
>
> **Die Entscheidung legt Zielarchitektur fest, keine Umsetzung.** Der
> Operator-Workspace ist **nicht angelegt**, der Runtime-Bereich **nicht
> definiert**.

**Es wurde keine Datei und kein Ordner verschoben.** Dieses Dokument bereitete
die Entscheidung vor.

---

## Verhältnis zur bestehenden Vorlage

`REPOSITORY_LAYOUT_OPTIONS.md` vergleicht **Verzeichnislayouts** des
Core-Repositorys (dort Optionen **A**, **B**, **C**) und empfiehlt **Option B
jetzt, Option C vorbereitet**.

Dieses Dokument beantwortet die davon unabhängige Frage: **Wie viele
Arbeitsbereiche gibt es, und wo verläuft die Grenze zwischen ihnen?** Die
Modelle heißen hier **W-1**, **W-2**, **W-3** — ausdrücklich **nicht** A/B/C,
um eine Verwechslung mit der Layoutvorlage auszuschließen.

| Frage | Dokument | Bezeichner |
| --- | --- | --- |
| Welches Verzeichnislayout im Core-Repository? | REPOSITORY_LAYOUT_OPTIONS | Option A/B/C |
| Wie viele Bereiche, und wo liegt die Grenze? | **dieses Dokument** | **W-1/W-2/W-3** |

Beide Fragen zusammen bilden **OD-26**.

---

## Drei Bereiche

Die Trennung folgt aus **ADR-0006** (`accepted`, D-028) und der
Canonical-/Derived-Regel aus **ADR-0003**.

### 1. Core Repository

| Enthält | Enthält **nicht** |
| --- | --- |
| Anwendungscode | **Private Wissensbestände** |
| Architektur | **Ausgefüllte Source Mappings** |
| Governance (NDF, ADRs, Register, Work Packages) | **Secrets** |
| Tests | **Private Zugangskonfiguration** |
| Synthetische Fixtures und Benchmarkkorpus | |
| Deploymentvorlagen ohne Werte | |

**Merkmal:** **`publication-capable by design`** — privater Bestand, produktive
Mappings und Secrets sind ausgeschlossen, sodass nichts herausgelöst werden
müsste. Versioniert in Git.

> **Das ist keine Veröffentlichungsfreigabe.** Das Repository bleibt zunächst
> **privat**; eine öffentliche Veröffentlichung benötigt eine separate
> **A0-Entscheidung** (OD-11 offen). Lizenz (OD-23), Produktname (OD-28) und
> die Sperrlisteneinträge zu Branding und Release bleiben unberührt.

### 2. Private Operator Workspace

| Enthält | Enthält **nicht** |
| --- | --- |
| Ausgefüllte Deployment Mappings | **Secrets im Klartext** |
| Private Collection-Konfiguration | Anwendungscode |
| Source Registry | Architektur oder Governance |
| **Verweise** auf den Secret Store | |

**Merkmal:** **keine Verpflichtung zur Veröffentlichung.** Kann versioniert
sein, muss aber nicht — das entscheidet der Betreiber. Enthält kanonische Daten
und ist deshalb **sicherungspflichtig**.

### 3. Runtime Data Area

**Nicht kanonisch — aber nicht durchgehend reproduzierbar.** Drei Unterklassen
mit verschiedenen Aufbewahrungs- und Backupanforderungen, verbindlich in
[ADR-0007](../decisions/ADR-0007-repository-und-workspace-grenze.md):

| Klasse | Inhalt | Reproduzierbar | Sicherungspflicht |
| --- | --- | --- | --- |
| **RT-1** Rebuildable Derived Data | Index, Embeddings, Cache, generierte Context Packs, Suchprojektionen, abgeleitete Katalogansichten | **ja** — aus kanonischen Quellen, Registry und versionierter Konfiguration | **nein** |
| **RT-2** Operational Evidence | Auditlogs, Approval- und Review-Nachweise, Incident Records, Sicherheitsereignisse, abgeschlossene Jobhistorie, Lösch-, Rebuild- und Restore-Nachweise | **nein** | **ja** |
| **RT-3** Transient Runtime State | Temporäre Dateien, Locks, aktive Jobzustände, Verarbeitungspuffer, nicht freigegebene Context Packs | entfällt | **nein** — kontrolliert verwerfen |

**Nur RT-1 erfüllt den Rebuild-Vertrag aus ADR-0003.** Sein Verlust verursacht
keinen Wissensverlust.

**RT-2 darf nicht als Cache behandelt werden.** Auditnachweise sind nicht
rekonstruierbar; sie brauchen definierte Aufbewahrung, Zugriffsschutz,
gegebenenfalls Integritätsnachweise und Sicherung. Eine Technologie —
append-only oder gleichwertig — ist **nicht gewählt**.

**RT-3 darf nach einem Neustart nie die alleinige Statuswahrheit sein.**

Keine der drei Klassen gehört in das Core-Git-Repository.

---

## Bewertung der drei Modelle

### W-1 — Ein Repository für alles

Core, Konfiguration und Wissensbestand in einer Historie.

| Aspekt | Bewertung |
| --- | --- |
| Vorteile | Einfachste Handhabung; ein `git clone`; keine Synchronisationsfragen |
| Nachteile | **Verletzt ADR-0006** |
| **Datenschutzwirkung** | **Schlecht** — privater Bestand landet in der Git-Historie; begünstigt R-01 strukturell |
| Portabilität | schlecht — Konfiguration und Kern untrennbar |
| Lokales Entwicklererlebnis | gut, kurzfristig |
| Backupgrenzen | unklar — kanonisch und abgeleitet vermischt |
| Git-Grenzen | Historie wächst mit dem Wissensbestand; ein History Rewrite wird praktisch unmöglich |
| Migrationspfad | — |

**Nicht weiter zu betrachten.** ADR-0006 ist angenommen und bindend; W-1
widerspricht ihm unmittelbar. Das Modell steht hier, damit die Ablehnung
begründet ist, nicht als Option.

### W-2 — Getrennte Repositories

Core-Repository und ein zweites, dauerhaft privates Repository für den
Wissensbestand. Entspricht **Layout-Option C**.

| Aspekt | Bewertung |
| --- | --- |
| Vorteile | **Strukturelle Trennung**; ein versehentlicher Commit landet sichtbar im falschen Repository |
| Nachteile | Zwei Historien, zwei Klone, zwei Backupziele; Querverweise brechen leichter |
| **Datenschutzwirkung** | **Stark** — die Grenze ist eine Repository-Grenze, keine Disziplinfrage |
| Portabilität | stark — der Kern ist ohne den Bestand vollständig beschreibbar |
| Lokales Entwicklererlebnis | mittel — zwei Arbeitsbereiche parallel |
| Backupgrenzen | **klar** — je Repository ein eigener Sicherungsvertrag |
| Git-Grenzen | sauber; die Kernhistorie bleibt klein und veröffentlichungsfähig |
| Migrationspfad | Core bleibt, zweites Repository entsteht neu |

### W-3 — Privater Arbeitsbereich neben dem Core-Repository

Ein Core-Repository plus einen Operator Workspace **außerhalb** davon, dazu eine
getrennte Runtime Data Area. Verträgt sich mit **Layout-Option B**.

| Aspekt | Bewertung |
| --- | --- |
| Vorteile | Ein Repository für die Arbeit; Konfiguration liegt daneben, nicht darin; Runtime Data ohnehin getrennt |
| Nachteile | Die Grenze ist eine **Pfadgrenze**, keine Repository-Grenze — schwächer als W-2 |
| **Datenschutzwirkung** | **Gut**, sofern der Bereich außerhalb des Repositorys liegt. Ein `.gitignore`-Unterordner wäre **unzureichend** |
| Portabilität | stark |
| Lokales Entwicklererlebnis | **gut** — ein Klon, ein Arbeitsbereich |
| Backupgrenzen | drei klare Ziele: Repository, Workspace, Runtime |
| Git-Grenzen | Kernhistorie bleibt sauber, sofern der Bereich wirklich außerhalb liegt |
| Migrationspfad | **geringster Aufwand** — der Bereich entsteht neu, nichts wird verschoben |

---

## Vergleich

| Kriterium | W-1 | W-2 | W-3 |
| --- | --- | --- | --- |
| ADR-0006-konform | **nein** | ja | ja |
| Datenschutzwirkung | schlecht | **stark** | gut |
| Portabilität | schlecht | stark | stark |
| Lokales Entwicklererlebnis | gut | mittel | **gut** |
| Backupgrenzen | unklar | klar | **klar** |
| Git-Grenzen | schlecht | **sauber** | sauber |
| Migrationsaufwand | — | mittel | **gering** |
| Umkehrbarkeit | — | schwer | **leicht** |
| Setzt OD-11 voraus | — | **ja** | nein |

---

## Empfehlung

**W-3 jetzt, mit vorbereitetem Weg zu W-2** — in Verbindung mit
**Layout-Option B**.

Das ist **dieselbe Linie** wie in `REPOSITORY_LAYOUT_OPTIONS.md`: der kleinste
Schritt, der den strengeren späteren Schritt nicht verbaut.

**Begründung in drei Punkten:**

1. **W-3 erfüllt ADR-0006 vollständig** und hat den geringsten
   Migrationsaufwand: der private Bereich entsteht neu, nichts wird verschoben.
   Das ist heute billig und nach dem ersten Ingest teuer.

2. **W-2 ist strenger, aber heute verfrüht.** Ein zweites Repository setzt eine
   Entscheidung über die Repository-Sichtbarkeit (**OD-11**) und den Ablageort
   des kanonischen Bestands (**OD-05**) voraus. Beide sind offen. Wer W-2
   wählt, bevor sie entschieden sind, legt sie implizit fest — genau das
   Vorgehen, das ADR-0006 vermeiden soll.

3. **W-3 verbaut W-2 nicht.** Wird der Workspace von Beginn an als
   eigenständige Einheit geschnitten, ist der spätere Übergang zu W-2 eine
   Initialisierung, keine Migration.

**Konkreter Vorschlag für CBP-WP-009:** W-3 annehmen und dabei festschreiben,
dass der Operator Workspace **außerhalb des Core-Repositorys** liegt — nicht
als ignorierter Unterordner. **`.gitignore` ist eine Vorsichtsmaßnahme, keine
Grenze:** es schützt vor Unachtsamkeit, nicht vor einem `git add -f`, und es
wirkt gar nicht auf eine Datei, die bereits verfolgt wird.

**Die Empfehlung wurde angenommen.** Der Human Maintainer hat W-3 gewählt und
dabei ausdrücklich festgehalten, dass der Workspace außerhalb liegt, Secrets
nirgends im Klartext stehen und eine Runtime-Projektion der Registry nie die
einzige Quelle kanonischer Registry-Metadaten ist.

**Registry-Grenze:** Schema, Validierungsregeln und **synthetische** Beispiele
liegen im Core Repository. Die konkreten **operatorbezogenen kanonischen**
Registry-Metadaten liegen im privaten Workspace. Eine **Runtime-Projektion**
für Suche und Betrieb darf existieren — sie ist **nicht** die kanonische
Registry, und ihr Verlust ist über einen normalen Index-Rebuild behebbar. Der
Verlust der kanonischen Metadaten ist es **nicht**.

### Was die Empfehlung nicht entscheidet

| Punkt | Register | Status |
| --- | --- | --- |
| Repository-Struktur insgesamt | **OD-26** | **geschlossen** (D-029, D-030) |
| Repository-Sichtbarkeit | **OD-11** | **offen** |
| Ablageort des kanonischen Bestands | **OD-05** | **offen** |
| Konkrete Quellen | **OD-06** | **offen** |
| NDF-Abweichungen AB-03…AB-08 | **OD-29** | **offen** |
| Manifestformat | OD-13 | offen |

Die Layoutwahl und die Bereichswahl sind **unabhängig** voneinander; OD-26
braucht beide.

## Migrationspfad

| Schritt | Inhalt | Verschiebung nötig |
| --- | --- | --- |
| 1 | OD-26 entscheiden — Layout **und** Bereichsmodell (CBP-WP-009) | nein |
| 2 | Core-Layout gemäß Entscheidung herstellen | **ja**, innerhalb des Repositorys |
| 3 | Operator Workspace als leere Struktur außerhalb anlegen | nein |
| 4 | Runtime Data Area definieren, weiterhin über `.gitignore` ausgeschlossen | nein |
| 5 | Erste Mappings im Workspace ablegen (F2) | nein |
| 6 | *Optional später:* Workspace zu eigenem Repository erheben (W-2) | nein — Initialisierung |

**Nur Schritt 2 bewegt bestehende Dateien**, und ausschließlich innerhalb des
Core-Repositorys. Kein Schritt verschiebt privaten Bestand — den gibt es noch
nicht, und das ist der Vorteil, den es zu erhalten gilt.

## Status

**ANGENOMMEN — Modell W-3.** **OD-26 ist am 2026-07-21 geschlossen**, durch
zwei getrennte A0-Entscheidungen: **D-029** (Layout-Option B) und **D-030**
(Bereichsmodell W-3). Verbindlich ist ab jetzt
[ADR-0007](../decisions/ADR-0007-repository-und-workspace-grenze.md) (A1) —
dieses Dokument bleibt A3 und dient als Begründungsgrundlage.

**W-2 bleibt vorbereitet, nicht beschlossen.** Der Übergang setzt weiterhin
OD-11 und OD-05 voraus.

**Es existiert kein Operator-Workspace, kein Runtime-Bereich und kein
Zielverzeichnis.** Es wurde nichts verschoben und nichts angelegt.

**Implementierung erlaubt: nein.**
