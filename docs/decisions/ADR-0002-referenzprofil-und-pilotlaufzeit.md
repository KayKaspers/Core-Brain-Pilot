# ADR-0002 — Proxmox-VM als Referenz, Docker Compose als bevorzugte Pilotlaufzeit

| Feld | Wert |
| --- | --- |
| Status | **accepted** |
| Datum | 2026-07-20 |
| Entscheider | Human Maintainer |
| Supersedes | — |
| Superseded by | — |
| Belegt durch | D-015, D-016 (beide A0) |

## Kontext

Der Pilot braucht eine konkrete Zielumgebung, ohne die Deployment-Neutralität
aus ADR-0001 aufzugeben. Zusätzlich bestand ein dokumentarischer Widerspruch:
Projektübergabe §4 (A5) führt Containerisierung als „kein Pflichtziel der
ersten Phase", während der Human Maintainer Docker Compose ausdrücklich als
**bevorzugte** Laufzeit benennt (A0).

In CBP-WP-002 war die Formulierung auf Basis der A5-Quelle abgeschwächt worden
(Abschwächung Ü-02). A0 schlägt A5; die Abschwächung ist aufgehoben.

## Entscheidung

1. **Referenzprofil des Piloten ist Profil A** — eine Proxmox-VM mit einer
   dedizierten Linux-VM als Referenzbetrieb.
2. **Docker Compose ist die bevorzugte Anwendungslaufzeit innerhalb dieser
   VM.**
3. Das bedeutet ausdrücklich **nicht**, dass Docker Compose die einzige
   unterstützte Laufzeit oder eine Produktgrenze ist. Profil B und C dürfen
   nativ betrieben werden.
4. Es gilt weiterhin: kein Betrieb auf dem Proxmox-Host, keine
   Proxmox-API-Berechtigung, keine Ausführung als Root.

**Ebenentrennung:** Proxmox ist eine Infrastrukturplattform, Docker Compose
eine Anwendungslaufzeit. Beides liegt auf verschiedenen Ebenen.

## Alternativen

**Nativer Betrieb ohne Container als Pilotlaufzeit.** Verworfen für den Pilot:
Compose vereinfacht Reproduzierbarkeit und Wegwerfbarkeit. Bleibt für Profil B
und C ausdrücklich offen.

**Container als Produktvoraussetzung festschreiben.** Verworfen: widerspricht
ADR-0001 und Projektübergabe §4.

**Bei der abgeschwächten Formulierung aus CBP-WP-002 bleiben.** Verworfen: eine
A0-Entscheidung schlägt eine A5-Quelle. Die Abschwächung war korrekt begründet,
ist aber überholt.

## Konsequenzen

**Leichter:** Reproduzierbarer Pilotaufbau; klare Zielumgebung für den DRC.

**Schwerer:** Profil B und C brauchen eine eigene, dokumentierte Beschreibung
des nativen Betriebs, damit die Neutralität nachweisbar bleibt.

**Nachführungsbedarf:** `PROJECT_DEFINITION.md` trug die überholte
Formulierung; korrigiert in CBP-WP-004 (OD-31).

## Bezug

G0-Kriterien F-1, F-2 · Abschwächung Ü-02 in
[../discovery/SOURCE_RECONCILIATION.md](../discovery/SOURCE_RECONCILIATION.md) ·
[../architecture/DEPLOYMENT_PROFILES.md](../architecture/DEPLOYMENT_PROFILES.md)
