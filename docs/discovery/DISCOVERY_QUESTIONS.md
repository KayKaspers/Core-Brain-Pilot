# Human-Maintainer-Fragebogen — Discovery Phase 0

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Nächstes Gate | G0 – Discovery and Scope Lock (**NOT PASSED**) |
| Überarbeitet in | CBP-WP-002 |
| Autoritätsklasse | A2 |
| Stand | 2026-07-20 |

Dies ist der **einzige** Fragebogen des Projekts. Fragen werden hier gebündelt
und nicht über mehrere Dokumente verteilt — entsprechend Projektübergabe §18:
Fragen bündeln, statt den Human Maintainer mit vielen Einzelrückfragen zu
unterbrechen.

**Keine Frage wird durch Annahme beantwortet.** Unbeantwortet ist ein
gültiger Zustand; eine geratene Antwort ist es nicht.

## Prioritäten

| Prio | Bedeutung |
| --- | --- |
| **P0** | Blockiert G0 |
| **P1** | Vor der Architekturentscheidung erforderlich |
| **P2** | Später beantwortbar |

Die Spalte **G0** verweist auf das zugehörige Kriterium in
[G0_SCOPE_LOCK_CRITERIA.md](G0_SCOPE_LOCK_CRITERIA.md).

---

## 1 — Infrastruktur

| # | Frage | Prio | G0 |
| --- | --- | --- | --- |
| 1.1 | Welche Proxmox-Version läuft? | **P0** | B-1 |
| 1.2 | Einzelhost oder Cluster? Bei Cluster: wie viele Knoten? | **P0** | B-2 |
| 1.3 | Wie viele CPU-Kerne können der VM dauerhaft zugesagt werden? | **P0** | B-3 |
| 1.4 | Wie viel RAM kann der VM dauerhaft zugesagt werden? | **P0** | B-4 |
| 1.5 | Wie viel Speicher steht zur Verfügung, getrennt nach System- und Datendisk? | **P0** | B-5 |
| 1.6 | Welche Storage-Technologie wird verwendet — ZFS, LVM oder eine andere? | **P0** | B-6 |
| 1.7 | Welche Backupziele existieren, mit welchem Verfahren und welcher Frequenz? | **P0** | B-7 |
| 1.8 | Existiert eine Backupkopie außerhalb des Proxmox-Hosts? Falls nein: ist eine geplant? | **P0** | B-8 |
| 1.9 | Welche Linux-Distribution ist für die VM vorgesehen? | P1 | F-1 |
| 1.10 | Welche VM-Ressourcengröße wird für den Pilot angesetzt? | P1 | F-1 |

## 2 — Netzwerk

| # | Frage | Prio | G0 |
| --- | --- | --- | --- |
| 2.1 | Existiert bereits ein VPN? Falls ja, welches Produkt? | **P0** | C-1 |
| 2.2 | Wird Tailscale oder WireGuard eingesetzt oder ist eines vorgesehen? | **P0** | C-2 |
| 2.3 | Welche ausgehenden Verbindungen darf das System herstellen? | **P0** | C-5 |
| 2.4 | Über welche Methode soll der mobile Zugriff erfolgen? | **P0** | C-6 |
| 2.5 | Wie erfolgt die interne DNS-Auflösung? | P1 | C-3 |
| 2.6 | Existiert ein Reverse Proxy oder ist einer geplant? | P1 | C-4 |

> Randbedingung aus Projektübergabe §10: keine öffentliche Freigabe interner
> Dienste als Standard. Fragen 2.1 bis 2.4 klären, wie der private Zugang
> stattdessen aussieht.

## 3 — Geräte

| # | Frage | Prio | G0 |
| --- | --- | --- | --- |
| 3.1 | Wer ist der primäre Nutzer? | **P0** | A-1 |
| 3.2 | Wie viele Nutzer werden erwartet? | **P0** | A-2 |
| 3.3 | Wie viele Geräte, aufgeschlüsselt nach Typ? | **P0** | A-3 |
| 3.4 | Welche Arbeitsfälle sollen am Desktop möglich sein? | **P0** | A-4 |
| 3.5 | Welche Arbeitsfälle mobil — und Android oder iOS? | **P0** | A-5 |
| 3.6 | Welche Anwendungsfälle müssen offline funktionieren? | **P0** | A-6 |
| 3.7 | Wird native Obsidian-Nutzung auf mehreren Geräten benötigt, oder genügt serverzentrierte Bearbeitung? | **P0** | A-7 |
| 3.8 | Welches Obsidian-Synchronisationsmodell wird bevorzugt, falls native Nutzung erforderlich ist? | P1 | A-7 |

> Zu 3.7: Projektübergabe §9 verlangt, serverzentrierte Bearbeitung ohne
> Dateisynchronisation und native Mehrgerätenutzung **getrennt** zu prüfen. Die
> Antwort entscheidet über einen erheblichen Teil der Architektur.

## 4 — Daten

| # | Frage | Prio | G0 |
| --- | --- | --- | --- |
| 4.1 | Welche Wissensquellen sollen aufgenommen werden? | **P0** | D-1 |
| 4.2 | Welche Größenordnung — Dateizahl und Volumen? | **P0** | D-2 |
| 4.3 | Welche Dateiformate kommen vor? | **P0** | D-3 |
| 4.4 | Welche Datenklasse gilt je Quelle? | **P0** | D-4 |
| 4.5 | Welche Daten sind ausdrücklich auszuschließen (`excluded-from-ai`)? | **P0** | D-5 |
| 4.6 | In welchem Umfang sind personenbezogene Daten enthalten, und auf welcher Rechtsgrundlage? | **P0** | D-6 |
| 4.7 | Welche vertraulichen Informationen sind enthalten und wie sind sie zu behandeln? | **P0** | D-7 |
| 4.8 | Welches Verfahren gilt, wenn ein Secret in die Git-Historie gelangt ist? | **P0** | D-8 |
| 4.9 | Wie ist eine Wissenseinheit geschnitten — Datei, Abschnitt oder Block? | P1 | — |
| 4.10 | Welche Frontmatter-Felder sollen verpflichtend sein? | P1 | — |
| 4.11 | Wie wird eine stabile Source-ID gebildet, die Umbenennung überlebt? | P1 | — |
| 4.12 | Wann gilt Wissen als veraltet — feste Frist oder je Quelle? | P1 | — |

## 5 — Claude und GitHub

| # | Frage | Prio | G0 |
| --- | --- | --- | --- |
| 5.1 | Wie wird Claude Desktop heute konkret genutzt? | **P0** | E-1 |
| 5.2 | Auf welche Repositories darf zugegriffen werden, getrennt nach Lese- und Schreibrecht? | **P0** | E-2 |
| 5.3 | Welche GitHub-Zugriffe sind erlaubt? | **P0** | E-3 |
| 5.4 | Welche Berechtigungsstufe gilt je Bereich — `read`, `draft`, `write with approval`, `publish with approval`, `forbidden`? | **P0** | E-4 |
| 5.5 | Wie läuft das Freigabeverfahren ab? | **P0** | E-5 |

> Randbedingung aus Projektübergabe §10: keine pauschalen GitHub-Schreibrechte,
> kein allgemeiner Schreibzugriff auf alle Repositories.

## 6 — Betrieb

| # | Frage | Prio | G0 |
| --- | --- | --- | --- |
| 6.1 | Wird die dedizierte Linux-VM als Referenzbetrieb bestätigt? | **P0** | F-1 |
| 6.2 | Wird Docker Compose als Pilotlaufzeit innerhalb der VM bestätigt? | **P0** | F-2 |
| 6.3 | Welche Backup- und Restore-Zielwerte gelten — maximal tolerierter Datenverlust und maximale Wiederherstellungsdauer? | **P0** | F-4 |
| 6.4 | Welche Bedingungen müssen erfüllt sein, bevor UI und Wiki beginnen dürfen? | **P0** | F-6 |
| 6.5 | Welche Suchlösung wird geprüft — ist qmd gesetzt oder nur Kandidat? | P1 | — |
| 6.6 | Welche Datenbank und welche Web-UI-Technologie kommen in Frage? | P1 | — |
| 6.7 | Welche Backupsoftware wird eingesetzt? | P1 | B-7 |
| 6.8 | Wie wird paralleler Schreibzugriff mehrerer Geräte verhindert oder aufgelöst? | P1 | — |
| 6.9 | Welche Ausfallzeit ist akzeptabel? | P2 | — |

> Zu 6.5: Projektübergabe §9 untersagt eine Vorentscheidung zugunsten von qmd
> ohne Installations-, Plattform-, Lizenz-, Wartungs- und Sicherheitsprüfung.

## 7 — Spätere Zielgruppe

| # | Frage | Prio | G0 |
| --- | --- | --- | --- |
| 7.1 | Bleibt das Repository dauerhaft privat? | **P0** | A-8 |
| 7.2 | Welche Nicht-Ziele sollen ausdrücklich festgeschrieben werden? | **P0** | A-8 |
| 7.3 | Welche Lizenz soll gelten? | P1 | — |
| 7.4 | Welche spätere öffentliche Zielgruppe wird erwartet? | P2 | — |
| 7.5 | Welcher öffentliche Produktname ist denkbar? | P2 | — |
| 7.6 | Welche Option aus Phase 7 wird angestrebt — nur intern, Open-Source-Referenz, wiederverwendbares Framework, Integration in Core, eigenes Produkt oder no-go? | P2 | — |

> Zu 7.5 und 7.6: Projektübergabe §1 und §15 Phase 7 halten beides ausdrücklich
> offen und untersagen eine automatische Entscheidung zugunsten eines neuen
> öffentlichen Produkts.

---

## Zusammenfassung

| Prio | Anzahl |
| --- | --- |
| **P0 — blockiert G0** | **35** |
| P1 — vor Architekturentscheidung | 16 |
| P2 — später | 4 |
| **Summe** | **55** |

Bearbeitungsreihenfolge: Alle P0-Fragen zuerst, gebündelt in einer Sitzung.
Sie decken die 39 blockierenden G0-Kriterien ab.

## Bearbeitung

Beantwortete Fragen werden **nicht gelöscht**. Die Antwort wird ergänzt, der
Status des zugehörigen G0-Kriteriums nachgeführt, und bei bindender Wirkung
entsteht ein ADR in [../decisions/](../decisions/README.md).

Die Erhebung der Antworten ist Gegenstand des vorgeschlagenen Work Packages
CBP-WP-003.
