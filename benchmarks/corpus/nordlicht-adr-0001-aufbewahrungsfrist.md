---
source_id: NOR-ADR-0001
title: Aufbewahrungsfrist für Nordlicht-Messreihen
project: Nordlicht
source_type: adr
authority_class: A1
data_class: internal
revision: 1
reviewed_at: 2026-02-08
freshness_status: current
verification_status: verified
valid_from: 2026-02-08
valid_until: null
ai_transfer: allowed
conflict_refs: [NOR-WIKI-AUFBEWAHRUNG]
test_fixture: true
---

# ADR-0001 — Aufbewahrungsfrist für Nordlicht-Messreihen

**Status:** accepted

## Kontext

Rohmessreihen des fiktiven Projekts Nordlicht wachsen schnell. Es war zu
entscheiden, wie lange sie vorgehalten werden.

## Entscheidung

Rohmessreihen werden **90 Tage** aufbewahrt und danach verdichtet.

Verdichtete Reihen bleiben unbefristet erhalten.

## Konsequenzen

Der Speicherbedarf bleibt begrenzt. Eine nachträgliche Auswertung auf
Rohdatenebene ist nach 90 Tagen nicht mehr möglich.

## Hinweis

Die abgeleitete Zusammenfassung `NOR-WIKI-AUFBEWAHRUNG` nennt eine abweichende
Frist und ist nicht bestätigt.
