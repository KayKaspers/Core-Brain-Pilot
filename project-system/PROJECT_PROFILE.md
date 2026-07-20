# Project Profile – Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Autoritaetsklasse | A2 |
| Stand | 2026-07-20 |

Struktur nach `framework/project-system/templates/PROJECT_PROFILE_TEMPLATE.md`
(NDF v1.0.0).

## Ziel

Ein serverzentriertes und portables KI-Wissens- und Arbeitssystem, das Claude
und anderen Implementation Agents die kleinste ausreichende Menge relevanter,
aktueller, autoritativer und datenschutzrechtlich erlaubter Informationen
bereitstellt.

## Zielgruppe

Ein privater Human Maintainer mit mehreren Geraeten einschliesslich mobiler
Nutzung. Kein Mehrmandantenbetrieb, keine oeffentliche Bereitstellung in
Phase 0.

Sekundaer: Implementation Agents (Claude und andere) als maschinelle
Konsumenten des Retrieval-Pfads.

## Kernfunktionen

Alle geplant, **keine implementiert**:

- Kanonischer Markdown-Wissensbestand unter Git-Historie
- Deterministischer Quellenindex mit stabiler Source-ID und Content Hash
- Ingest-Quarantaene mit Secret- und PII-Pruefung
- Lokale Hybrid-Suche: Volltext, semantisch, kombiniert
- Brain-First-Retrieval mit Autoritaets-, Datenschutz- und Aktualitaetsfilter
- Context Budgets B0–B4 und reproduzierbare Context Packs
- Erklaerbarer Retrieval-Trace
- Menschlich kontrollierte Konflikt-, Review- und Verifikations-Queues
- Vault Doctor als periodische Bestandspruefung
- Backup, Restore und Rebuild

Vollstaendig in [CAPABILITY_MATRIX.md](CAPABILITY_MATRIX.md).

## Technische Basis

**Noch nicht festgelegt.** Bisher stehen nur Rahmenbedingungen fest:

| Aspekt | Festlegung |
| --- | --- |
| Kanonisches Format | Markdown |
| Versionierung | Git |
| Suche | lokal, austauschbar |
| Web-UI | austauschbar |
| Programmiersprache | offen |
| Suchmaschine | offen |
| Embedding-Modell | offen |
| Datenhaltung abgeleitet | offen |

Sprach-, Engine- und Modellwahl sind offene Entscheidungen — siehe
[DECISION_REGISTER.md](DECISION_REGISTER.md).

## Deployment

| Aspekt | Festlegung | Status |
| --- | --- | --- |
| Referenzplattform | Proxmox | erste Referenz, **nicht** Produktgrenze |
| Bevorzugte Laufzeit | Docker Compose in dedizierter Linux-VM | geplant, **gesperrt** in Phase 0 |
| Architekturbindung | keine | deployment-neutral |

Es existiert **keine** Installation. Docker Compose steht auf der Sperrliste
in [../docs/product/DO_NOT_START.md](../docs/product/DO_NOT_START.md).

## Risiken

Zusammenfassung; vollstaendig in [RISK_REGISTER.md](RISK_REGISTER.md).

- Vorgezogene Implementierung praejudiziert offene Architekturentscheidungen
- Secret gelangt in die Git-Historie und ist praktisch nicht mehr entfernbar
- Abgeleitete Daten werden faelschlich als autoritativ behandelt (A6 ueber A0–A5)
- Scope-Ausweitung ueber 29 Capabilities ohne Priorisierung
- Zwei verbindliche Eingangsquellen lagen nicht vor (OI-01)

## Bekannte Einschraenkungen

- Kein lauffaehiges System, kein Wissensbestand, kein Index
- Scope ist **nicht** gelockt; Gate G0 nicht definiert (OI-04)
- Context Budgets B0–B4 inhaltlich undefiniert (OI-03)
- Keine Lizenz festgelegt; `LICENSE` in Phase 0 ausdruecklich verboten
- Kein Git-Remote, kein Commit
- Kein Retrieval-Benchmark, damit keine Qualitaetsaussage moeglich

## Roadmap

| Phase | Inhalt | Status |
| --- | --- | --- |
| Phase 0 | Discovery und Scope Lock | **laufend** |
| Gate G0 | Discovery and Scope Lock | offen, Kriterien undefiniert |
| Phase 1+ | Noch nicht geplant | — |

Nachfolgende Phasen werden erst nach bestandenem G0 durch Nova geplant. Eine
Roadmap vor dem Scope Lock waere Spekulation.

## NDF-Notizen

Framework: **Nova Development Framework v1.0.0**, verbindlich, ausschliesslich
freigegebene Version. Keine v1.1-Planung.

Zehn dokumentierte Abweichungen AB-01 bis AB-10 in
[../docs/ndf/ADOPTION_NOTES.md](../docs/ndf/ADOPTION_NOTES.md).

Anwendung des Frameworks in
[../docs/ndf/README.md](../docs/ndf/README.md).
