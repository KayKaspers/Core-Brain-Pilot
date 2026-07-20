# Project Definition — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Status dieses Dokuments | Entwurf zur Scope-Lock-Pruefung an Gate G0 |
| Autoritaetsklasse | A2 (formeller Projektstatus) |
| Stand | 2026-07-20 |

## Definition

Core Brain Pilot ist ein **serverzentriertes und portables KI-Wissens- und
Arbeitssystem**.

Ziel ist, Claude und anderen Implementation Agents nur die **kleinste
ausreichende Menge** relevanter, aktueller, autoritativer und
datenschutzrechtlich erlaubter Informationen bereitzustellen.

## Zielsetzung im Detail

Die Formulierung "kleinste ausreichende Menge" traegt vier gleichrangige
Filterdimensionen. Ein Ergebnis muss **alle vier** erfuellen:

| Dimension | Bedeutung |
| --- | --- |
| Relevanz | Bezug zur konkreten Aufgabe |
| Aktualitaet | nicht veraltet, nicht superseded |
| Autoritaet | A0–A6-Rang ausreichend fuer die Fragestellung |
| Datenschutz | Datenklasse fuer den Zielkontext freigegeben |

Ein Treffer, der nur drei Dimensionen erfuellt, wird nicht ausgeliefert.

## Plattform und Portabilitaet

- **Proxmox** ist die **erste Referenzplattform**, ausdruecklich **nicht die
  Produktgrenze**.
- **Docker Compose** ist als bevorzugte **spaetere** Anwendungslaufzeit
  innerhalb einer dedizierten Linux-VM vorgesehen.
- Die Architektur ist **deployment-neutral**: die Bindung an Proxmox oder
  Compose darf nicht in den kanonischen Wissensbestand oder in das Datenmodell
  einsickern.

Zum Zeitpunkt dieses Dokuments ist **nichts davon installiert oder
implementiert**.

## Nutzungskontext

- Private Nutzung durch einen Human Maintainer.
- Mehrgeraete-Nutzung einschliesslich mobiler Zugriffe.
- Kein Mehrmandantenbetrieb, keine oeffentliche Bereitstellung in Phase 0.

## Abgrenzung

Core Brain Pilot ist **nicht**:

- ein oeffentliches Produkt oder eine Marke (kein oeffentliches Branding in
  Phase 0),
- ein allgemeiner Dokumentenspeicher,
- ein Ersatz fuer die Git-Historie kuratierter Inhalte,
- ein autonom handelnder Agent — jede kuratierende Entscheidung bleibt
  menschlich kontrolliert.

## Kanonisch vs. abgeleitet

| Klasse | Beispiele | Eigenschaft |
| --- | --- | --- |
| Kanonisch | Kuratierter Markdown-Wissensbestand, Source Manifest, ADRs | Einzige Wahrheitsquelle, versioniert in Git |
| Abgeleitet | Index, Cache, Embeddings, Knowledge Graph, Web-UI-Zustand, Context Packs | Reproduzierbar, nie autoritativ |

**Invariante:** Der vollstaendige Verlust aller abgeleiteten Daten fuehrt zu
keinem Wissensverlust. Ein Rebuild aus dem kanonischen Bestand stellt den
Systemzustand wieder her.

## Offene Punkte fuer Gate G0

Der Scope ist noch **nicht** gelockt. Offene Fragen und fehlende Information:

- [docs/discovery/DISCOVERY_QUESTIONS.md](../discovery/DISCOVERY_QUESTIONS.md)
- [docs/discovery/OPEN_INFORMATION.md](../discovery/OPEN_INFORMATION.md)
