---
source_id: KAS-ADR-0001
title: Speicherformat des Kastanie-Archivs
project: Kastanie
source_type: adr
authority_class: A1
data_class: internal
revision: 2
reviewed_at: 2026-03-14
freshness_status: current
verification_status: verified
valid_from: 2026-03-14
valid_until: null
ai_transfer: allowed
conflict_refs: []
test_fixture: true
---

# ADR-0001 — Speicherformat des Kastanie-Archivs

**Status:** accepted

## Kontext

Das Archiv des fiktiven Projekts Kastanie soll langfristig lesbar bleiben. Zur
Auswahl standen ein proprietäres Binärformat und Markdown.

## Entscheidung

Das kanonische Speicherformat des Kastanie-Archivs ist **Markdown**.

Binärformate sind ausschließlich als Anhang zulässig und werden nicht
indexiert.

## Konsequenzen

Der Bestand bleibt ohne Spezialwerkzeug lesbar. Formatierungsreiche Dokumente
verlieren Layoutinformationen.
