# ADR-0005 — Deployment Readiness Check als eigenes Prüfmodell

| Feld | Wert |
| --- | --- |
| Status | **accepted** |
| Datum | 2026-07-20 |
| Entscheider | Human Maintainer |
| Supersedes | — |
| Superseded by | — |
| Belegt durch | D-026 (A0), Nova-Review zu CBP-WP-003 |

## Kontext

Die ursprünglichen G0-Kriterien machten den allgemeinen Scope Lock von
konkreten Werten einer einzelnen Proxmox-Installation abhängig — Version, CPU,
RAM, Storage, VPN-Produkt, Backupziele. Das koppelte eine **Produktentscheidung**
an ein **Installationsdetail**.

Das dreistufige Kriterienmodell (D-026) trennt seither Core Required (25),
Deployment Required (16) und Conditional (6). Damit entstand die Frage, wo die
16 vertagten Kriterien geprüft werden — und das Risiko R-34, dass Vertagtes
schlicht vergessen wird.

## Entscheidung

Es wird ein eigenes Prüfmodell eingeführt: der **Deployment Readiness Check
(DRC)**.

1. Der DRC ist ein **fail-closed Prüfmodell** vor einer konkreten Installation.
   Fehlt ein erforderlicher Nachweis, wird nicht installiert.
2. Er ist **kein zusätzliches Governance-Framework** und **kein Ersatz für
   NDF v1.0.0**.
3. Er ist **je Deploymentprofil separat** auszuführen. Ein für Profil A
   bestandener DRC sagt nichts über Profil D.
4. Er übernimmt **alle 16 Deployment-Required-Kriterien**, aufgefächert in 18
   Prüfpunkte mit dokumentierter G0-Herkunft.
5. Sein Ausgangszustand ist **NOT EVALUATED**. Er ist nicht automatisch
   bestanden.
6. **Deployment-Required-Kriterien blockieren G0 nicht** — sie blockieren die
   Installation.
7. Der Abschluss erfordert die ausdrückliche Freigabe des Human Maintainers.
   Kein Implementation Agent stellt das Bestehen fest.

Ein neuer **Gate-Name** wird bewusst nicht eingeführt; der DRC ist ein
Prüfmodell, kein Gate im NDF-Sinne.

## Alternativen

**Deployment-Kriterien in G0 belassen.** Verworfen: verhindert den Scope Lock
aus Gründen, die mit dem Produkt-Scope nichts zu tun haben.

**Deployment-Kriterien streichen.** Verworfen: sie sind für einen sicheren
Betrieb erforderlich. Streichen wäre kein Fortschritt, sondern Verlust.

**Prüfung informell zur Installationszeit.** Verworfen: genau das ist R-34. Ohne
festen Ort und festen Status verschwinden vertagte Anforderungen.

**Ein zweites Gate im NDF-Sinne.** Verworfen: NDF v1.0.0 ist die verbindliche
Prozessgrundlage; ein paralleles Gate-System wäre ein zweites
Governance-Modell, das Projektübergabe §14 ausschließt.

## Konsequenzen

**Leichter:** G0 wird erreichbar, ohne dass eine Zeile Infrastruktur
feststeht. Der Scope Lock kann stattfinden, bevor die VM existiert.

**Schwerer:** Zwei Prüfmodelle sind zu pflegen, und ihre Grenze muss klar
bleiben. Bei jedem Profilwechsel ist der DRC neu auszuführen.

**Bedingung:** OD-33 darf erst geschlossen werden, wenn der DRC vollständig
dokumentiert und in allen relevanten Statusdokumenten verlinkt ist.

## Bezug

D-026 · OD-33 · Risiko R-34 · alle 16 Deployment-Required-Kriterien ·
[../operations/DEPLOYMENT_READINESS_CHECK.md](../operations/DEPLOYMENT_READINESS_CHECK.md) ·
[../discovery/G0_SCOPE_LOCK_CRITERIA.md](../discovery/G0_SCOPE_LOCK_CRITERIA.md)
