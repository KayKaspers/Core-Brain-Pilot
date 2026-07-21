# Phase 1 Stop Conditions — Abbruch- und Rücksetzbedingungen

| Feld | Wert |
| --- | --- |
| **Status** | **PROPOSED** |
| Erfasst in | CBP-WP-008 |
| Autoritätsklasse | A3 |
| Gilt für | Streams **F1–F5**, Work Packages **CBP-WP-009 bis CBP-WP-014** |
| Stand | 2026-07-21 |

Eine Abbruchbedingung ist **kein Warnhinweis**. Tritt sie ein, wird die Arbeit
angehalten und gemeldet — nicht umgangen, nicht umformuliert und nicht durch
eine angepasste Prüfung entschärft.

> **Präzedenzfall.** In CBP-WP-005 wurde eine Anforderung verengt und
> anschließend die zugehörige Prüfung an die Verengung angepasst. Dieses
> Dokument existiert, damit so etwas ein benannter Abbruch ist und keine
> Auslegungsfrage.

---

## Gemeinsame Sofortmaßnahme

| # | Schritt |
| --- | --- |
| 1 | **Arbeit anhalten.** Keine weitere Änderung am betroffenen Gegenstand |
| 2 | **Nichts rückgängig machen**, was die Ursache verschleiern könnte |
| 3 | Zustand festhalten: was, wann, welcher Schritt, welches Work Package |
| 4 | **Blocker melden** — an Nova und, bei Autorität A0, an den Human Maintainer |
| 5 | **Keine Selbstfreigabe.** Wiederaufnahme nur nach der genannten Bedingung |

**Schritt 5 ist der Kern.** Wer die Wiederaufnahmebedingung selbst feststellt,
hat keine Abbruchbedingung, sondern eine Formulierung.

---

## Zwölf Stop-Bedingungen

### SB-01 — Unerwarteter Schreibzugriff auf Canonical

| Feld | Inhalt |
| --- | --- |
| **Erkennung** | Änderung am kanonischen Bestand ohne Freigabe; Auditeintrag eines nicht berechtigten Dienstes |
| **Sofortmaßnahme** | Schreibpfad sperren; betroffene Komponente anhalten; Änderung **nicht** überschreiben |
| **Incident-Prozess** | Umfang bestimmen; kanonischen Stand gegen Git und Backup abgleichen; Ursache auf Ebene KB-03/KB-04 suchen |
| **Wiederaufnahme** | Schreibrechte korrigiert **und** Negativtest zu KB-04 bestanden |
| **Autorität** | **A0** |

### SB-02 — Secret in Repository, Index oder Context Pack

| Feld | Inhalt |
| --- | --- |
| **Erkennung** | Fund durch Scan, Review oder Zufall — in Repository, Mapping, Index, Context Pack, Log oder Quarantäne |
| **Sofortmaßnahme** | Jeden weiteren Ingest blockieren (S5); **Secret nicht in den Bericht kopieren** |
| **Incident-Prozess** | [SECRET_INCIDENT_RESPONSE.md](../security/SECRET_INCIDENT_RESPONSE.md) — **Rotation vor History Cleanup**, **Bereinigung vor Rebuild** |
| **Wiederaufnahme** | Rotation abgeschlossen **und** Bereinigung bestätigt **und** Rebuild durchgeführt |
| **Autorität** | **A0** |

### SB-03 — `excluded-from-ai`-Inhalt überschreitet die externe Modellgrenze

| Feld | Inhalt |
| --- | --- |
| **Erkennung** | So klassifizierter Inhalt erscheint in Suchergebnis, Context Pack, Antwort oder Sammelanfrage |
| **Sofortmaßnahme** | Retrieval-Pfad stoppen; **betroffene Context Packs verwerfen**; keine weitere Modellanfrage |
| **Incident-Prozess** | Ausbreitung bestimmen — insbesondere, **ob externer Modellkontext erreicht wurde**; Vorfall dokumentieren |
| **Wiederaufnahme** | KB-11 auf **allen** tragenden Ebenen negativ getestet, Zielwert **null Leaks** |
| **Autorität** | **A0** |

### SB-04 — Root- oder Host-Ausführung

| Feld | Inhalt |
| --- | --- |
| **Erkennung** | Ein Dienst läuft als Root oder direkt auf dem Hypervisor-Host |
| **Sofortmaßnahme** | Dienst anhalten; **nicht** im laufenden Betrieb umkonfigurieren |
| **Incident-Prozess** | Prüfen, welche Ressourcen mit erhöhten Rechten berührt wurden; Auditspur sichern |
| **Wiederaufnahme** | KB-01 und KB-02 umgesetzt und negativ getestet |
| **Autorität** | A2 — **A0**, wenn kanonische Daten berührt wurden |

### SB-05 — Öffentliche Erreichbarkeit ohne Freigabe

| Feld | Inhalt |
| --- | --- |
| **Erkennung** | Ein Dienst ist außerhalb des privaten Netzes erreichbar |
| **Sofortmaßnahme** | **Egress und Ingress sperren** — der sichere Zustand ist kein Netz |
| **Incident-Prozess** | Expositionsdauer bestimmen; Zugriffe im Audit prüfen; **D-023** gegenprüfen |
| **Wiederaufnahme** | KB-10 negativ getestet; Zugriff nachweislich nur über privates Netz oder VPN |
| **Autorität** | **A0** |

### SB-06 — Unkontrollierter Git-Push

| Feld | Inhalt |
| --- | --- |
| **Erkennung** | Push, Branch, Tag, Release oder Remote-Änderung ohne Human-Maintainer-Autorität |
| **Sofortmaßnahme** | Keine weitere Git-Operation; Zugang der auslösenden Identität sperren |
| **Incident-Prozess** | Prüfen, **ob privater Bestand oder ein Secret veröffentlicht wurde** — falls ja, zusätzlich SB-02 |
| **Wiederaufnahme** | Rechte korrigiert; KB-07 negativ getestet; Human Maintainer bestätigt den Remote-Stand |
| **Autorität** | **A0** |

### SB-07 — Quelle ohne bestätigte Datenklasse

| Feld | Inhalt |
| --- | --- |
| **Erkennung** | Eintrag mit `data_class: unknown` erreicht Indexierung oder Übertragung |
| **Sofortmaßnahme** | Eintrag auf `classification-required`; **jede externe Übertragung sperren** |
| **Incident-Prozess** | Prüfen, ob bereits übertragen wurde; betroffene Context Packs verwerfen |
| **Wiederaufnahme** | Datenklasse **menschlich bestätigt**; M4 negativ getestet |
| **Autorität** | A2 — **A0** bei erfolgter Übertragung |

### SB-08 — Index enthält eine gelöschte Quelle

| Feld | Inhalt |
| --- | --- |
| **Erkennung** | Ein getombsteinter oder widerrufener Eintrag ist auffindbar |
| **Sofortmaßnahme** | Index für die betroffene Collection sperren; **Derived Cleanup ausführen** |
| **Incident-Prozess** | Prüfen, ob der Eintrag durch einen Rebuild zurückkehrte (T-4) oder nie entfernt wurde (T-3) |
| **Wiederaufnahme** | Tombstone überlebt einen Rebuild nachweislich |
| **Autorität** | A2 |

### SB-09 — Fehlender Rollback

| Feld | Inhalt |
| --- | --- |
| **Erkennung** | Eine Änderung lässt sich nicht in einen definierten Ausgangszustand zurückführen |
| **Sofortmaßnahme** | Keine weitere Änderung; Ist-Zustand vollständig dokumentieren |
| **Incident-Prozess** | Prüfen, ob Backup oder Git den Ausgangszustand tragen; Lücke benennen |
| **Wiederaufnahme** | Rücksetzstrategie dokumentiert **und** einmal erprobt |
| **Autorität** | A2 |

### SB-10 — Nicht reproduzierbare Registry

| Feld | Inhalt |
| --- | --- |
| **Erkennung** | Zwei Läufe bei unverändertem Input ergeben verschiedene Indexzustände |
| **Sofortmaßnahme** | Rebuild-Vertrag als **nicht erfüllt** kennzeichnen; **R-10 bleibt offen** |
| **Incident-Prozess** | Abweichung eingrenzen; Reihenfolge-, Zeit- und Hashabhängigkeiten prüfen |
| **Wiederaufnahme** | Determinismus **und** Tombstone-Persistenz belegt |
| **Autorität** | A2 |

### SB-11 — Backup überschrieben oder unlesbar

| Feld | Inhalt |
| --- | --- |
| **Erkennung** | Sicherung fehlt, ist überschrieben oder nicht wiederherstellbar |
| **Sofortmaßnahme** | **Keine weitere Sicherung auf dasselbe Ziel**; vorhandene Stände einfrieren |
| **Incident-Prozess** | Prüfen, welche Identität geschrieben hat (KB-12); ältesten lesbaren Stand bestimmen |
| **Wiederaufnahme** | Backup-Isolation negativ getestet **und** ein Restore durchgeführt |
| **Autorität** | **A0** |

### SB-12 — Unerwartete Änderung außerhalb des Work-Package-Scopes

| Feld | Inhalt |
| --- | --- |
| **Erkennung** | Eine Datei außerhalb der erlaubten Liste ist verändert; oder die Autorisierung ist mehrdeutig |
| **Sofortmaßnahme** | **Nicht raten.** Änderung nicht fortsetzen, nicht committen |
| **Incident-Prozess** | Betroffene Dateien auflisten; Blocker mit genauer Frage melden; Alternativen benennen, **keine wählen** |
| **Wiederaufnahme** | Ausdrückliche Autorisierung liegt vor, oder die Änderung ist zurückgenommen |
| **Autorität** | **A0** |

---

## Übersicht

| ID | Gegenstand | Autorität | Betroffene WP |
| --- | --- | --- | --- |
| SB-01 | Schreibzugriff auf Canonical | **A0** | 012, 013, 014 |
| SB-02 | Secret gefunden | **A0** | alle |
| SB-03 | `excluded-from-ai` durchgebrochen | **A0** | 013, 014 |
| SB-04 | Root- oder Hostbetrieb | A2 / A0 | 012 |
| SB-05 | Öffentliche Erreichbarkeit | **A0** | 012 |
| SB-06 | Unkontrollierter Git-Push | **A0** | alle |
| SB-07 | Quelle ohne Datenklasse | A2 / A0 | 010, 013 |
| SB-08 | Gelöschte Quelle im Index | A2 | 014 |
| SB-09 | Fehlender Rollback | A2 | 012, 013, 014 |
| SB-10 | Registry nicht reproduzierbar | A2 | 014 |
| SB-11 | Backup überschrieben | **A0** | 012 |
| SB-12 | Änderung außerhalb des Scopes | **A0** | alle |

**Sieben der zwölf erfordern A0.** Bei diesen darf weder Nova noch der
Implementation Agent die Wiederaufnahme feststellen.

## Zusätzliche Prozessbedingungen

Diese gelten ergänzend in **jedem** Work Package:

| Bedingung | Wirkung |
| --- | --- |
| **Eine Prüfung wird an das Ergebnis angepasst** | Abbruch; vollständige Offenlegung; A0 entscheidet REWORK oder Annahme |
| **Eine Anforderung wird stillschweigend verengt** | Abbruch; Verengung als **Blocker** melden, nicht als Entscheidung |
| **Eine Kontrolle ruht allein auf Promptregeln** | Als **nicht durchgesetzt** kennzeichnen; nicht als erfüllt berichten |
| **Eine Kennzahl weicht von der Auszählung ab** | Bericht anhalten; **auszählen, nicht fortschreiben** (R-33) |
| **A6 soll A0 bis A5 überschreiben** | Höherrangige Quelle gewinnt; Widerspruch vorlegen |

## Verhältnis zu den Risiken

Eine eingetretene Stop-Bedingung ist ein **realisiertes Risiko**, kein neues:
SB-02 ist R-01 · SB-03 ist R-31 und R-02 · SB-04 ist R-26 · SB-05 ist R-05 ·
SB-06 ist R-27 · SB-07 ist R-03 · SB-08 ist R-06 · SB-10 ist R-10 · SB-11 ist
R-20.

Das Anhalten mindert das Risiko nicht — es verhindert nur, dass die Folge
weitergetragen wird.

## Status

**PROPOSED.** Keine Bedingung ist in Phase 1 eingetreten, weil Phase 1 nicht
begonnen hat.

**Implementierung erlaubt: nein.**
