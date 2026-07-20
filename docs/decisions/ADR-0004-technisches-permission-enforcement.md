# ADR-0004 — Technische Durchsetzung von Berechtigungen

| Feld | Wert |
| --- | --- |
| Status | **accepted** |
| Datum | 2026-07-20 |
| Entscheider | Human Maintainer |
| Supersedes | — |
| Superseded by | — |
| Belegt durch | Projektübergabe §10 (A5), D-023 (A0) |

## Kontext

Das System führt Daten mehrerer Schutzklassen und lässt Agenten auf ihnen
arbeiten. Projektübergabe §10 verlangt ausdrücklich, Berechtigungen
**technisch** umzusetzen und nicht nur über Promptregeln.

Der Human Discovery Intake hat das Berechtigungsmodell nicht erhoben (OI-08).
Die Risiken R-25 und R-27 blieben dadurch kritisch offen: Berechtigungen
existieren als Absicht, nicht als Kontrolle.

## Entscheidung

Berechtigungen werden **technisch durchgesetzt**. Eine Promptregel ist keine
Sicherheitsgrenze.

**Aktionsklassen:** `read` · `draft` · `write with approval` ·
`publish with approval` · `forbidden`

**Durchsetzungsebenen, kumulativ:**

1. OS-Dateirechte
2. Container-User und Mount-Modi
3. API-Autorisierung
4. Netzwerkgrenzen
5. Approval-Zustände

**Bindende Einzelregeln:**

- **Default deny.** Bei unklarer Berechtigung gilt `forbidden`.
- Claude erhält **keinen** allgemeinen Schreibzugriff auf Repositories und
  **keine** pauschalen GitHub-Schreibrechte.
- Indexer und Retrieval Service erhalten **keine** kanonischen Schreibrechte.
- Die Web-UI erhält **keine** administrativen Hostrechte.
- **Backup Storage ist für Web-UI, Suche und Claude nicht beschreibbar.**
- Der **Secret Store ist vom Wissensbestand getrennt.**
- `publish with approval` umfasst Push, Release, Veröffentlichung und
  produktive Status- oder Gateänderungen.
- **`excluded-from-ai` erreicht niemals ein externes Modell** — lokal
  klassifizierbar, gegebenenfalls lokal durchsuchbar, nie übertragbar.

## Alternativen

**Promptbasierte Regeln.** Verworfen: widerspricht Projektübergabe §10. Ein
Modell, das seine eigenen Grenzen durchsetzen soll, ist keine Kontrolle.

**Ein einziger Dienstbenutzer für alle Komponenten.** Verworfen: hebt die
Trennung der Schreibpfade auf und macht ADR-0003 wirkungslos.

**Berechtigungen erst bei Mehrbenutzerbetrieb einführen.** Verworfen: der
Schutzbedarf entsteht aus den **Datenklassen**, nicht aus der Nutzerzahl. Auch
im Single-User-Betrieb gibt es Komponenten mit unterschiedlichem
Vertrauensniveau.

## Konsequenzen

**Leichter:** Fehler in Web-UI, Suche oder Agent können den kanonischen
Bestand und die Sicherung nicht beschädigen.

**Schwerer:** Der Betrieb braucht mehrere Dienstkonten, getrennte Volumes und
eine serverseitige Autorisierung. Bequeme Abkürzungen entfallen.

**Wichtige Einschränkung:** Erfüllt ist bislang die **dokumentarische**
Anforderung. Es existiert keine Anwendung, kein Dienstkonto, keine API.
**Nichts hiervon ist implementiert.** R-25 und R-27 bleiben offen; der Nachweis
gehört in spätere Gates.

## Bezug

G0-Kriterien **E-2, E-3, E-4, E-5** · Risiken R-25, R-27, R-31 · OI-08 ·
[../security/PERMISSION_MODEL.md](../security/PERMISSION_MODEL.md) ·
[../architecture/TRUST_BOUNDARIES.md](../architecture/TRUST_BOUNDARIES.md)
