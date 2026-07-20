# Secret Incident Response — Core Brain Pilot

| Feld | Wert |
| --- | --- |
| Phase | Phase 0 – Discovery und Scope Lock |
| Erfasst in | CBP-WP-004 |
| Autoritätsklasse | A2 |
| Status | **Verfahren dokumentiert, technisch nicht unterstützt** |
| Stand | 2026-07-20 |

Belegt G0-Kriterium **D-8**.

Dieses Dokument enthält **keine echten Secrets, keine Beispielschlüssel und
keine realistischen Credential-Formate** — auch nicht als Illustration. Es
enthält **keine ausführbaren Bereinigungsskripte**.

---

## Anwendungsbereich

Das Verfahren gilt, wenn ein Secret in einen dieser Orte gelangt ist:

Arbeitsdatei · Git-Commit · Remote-Repository · Suchindex · Embeddingbestand ·
Context Pack · Modellkontext

Als Secret gelten Zugangsdaten und Geheimnisse jeder Art im Sinne der
Datenklasse `secret` in
[../privacy/DATA_CLASSIFICATION.md](../privacy/DATA_CLASSIFICATION.md).

## Zwei Grundsätze

### Rotation vor History Cleanup

> **Zuerst widerrufen oder rotieren, dann bereinigen.**

Die Bereinigung dauert; die Kompromittierung wirkt sofort. Wer zuerst die
Historie umschreibt, lässt ein gültiges Geheimnis so lange in fremder Hand, wie
die Bereinigung braucht. Umgekehrt ist ein widerrufenes Secret in einer noch
unbereinigten Historie zwar unschön, aber wirkungslos.

### Löschen ist keine Behebung

> **Das Entfernen eines Secrets aus einer Datei gilt nicht als Behebung.**

Solange das Geheimnis gültig ist, ist es kompromittiert — unabhängig davon, ob
es noch irgendwo sichtbar steht. Ein Commit „removed key" behebt nichts; er
dokumentiert nur, dass es da war.

---

## Ablauf

### 1. Vorfall erkennen und Arbeit stoppen

Der Fund ist ein **Blocker**. Laufende Work Packages werden angehalten, keine
weiteren Commits, Pushes, Ingest-Läufe oder Rebuilds. Der Implementation Agent
meldet und bereinigt **nicht selbstständig**.

### 2. Exposition begrenzen

Betroffene Dienste, Freigaben oder Zugänge einschränken, soweit ohne
Kollateralschaden möglich. Keine Panikaktionen, die Spuren vernichten.

### 3. Secret sofort widerrufen oder rotieren

**Der wichtigste Schritt und der erste wirksame.** Beim ausgebenden System:
widerrufen, wo möglich; sonst rotieren. Erst danach beginnt die Bereinigung.

### 4. Betroffene Systeme und Revisionen bestimmen

Welche Datei, welcher Commit, welcher Branch, welches Remote, welcher
Indexstand, welche Embeddings, welche Context Packs, welche Modellaufrufe. Ohne
diese Liste ist Schritt 5 bis 9 Ratearbeit.

### 5. Aktuelle Arbeitskopien bereinigen

Arbeitsverzeichnis, Zwischenstände, lokale Kopien. Beim Human Maintainer, nicht
beim Agenten.

### 6. Git-Historie bei Bedarf kontrolliert bereinigen

Nur nach Schritt 3. Kontrolliert heißt: bewusst, dokumentiert, mit
Rückfallpunkt. Ein History-Rewrite ist selbst ein Risiko und braucht eine
Entscheidung, keine Reflexhandlung.

### 7. Remote-Kopien und Forks berücksichtigen

Ein Rewrite auf `main` erreicht keine Forks, Klone, Pull-Request-Referenzen,
Caches oder Spiegel. Diese sind gesondert zu prüfen. **Genau deshalb steht
Schritt 3 vorn:** ein widerrufenes Secret in einem fremden Klon ist harmlos.

### 8. Abgeleitete Daten löschen

| Datenart | Maßnahme |
| --- | --- |
| Suchindex | betroffene Einträge löschen |
| Embeddings | betroffene Vektoren löschen |
| Cache | invalidieren |
| Context Packs | verfallen lassen und löschen |

Abgeleitete Daten sind reproduzierbar — ihr Verlust kostet nichts als Rechenzeit.

### 9. Abgeleitete Daten erst nach Bereinigung neu erzeugen

**Reihenfolge ist zwingend.** Ein Rebuild vor der Bereinigung schreibt das
Secret in den frischen Index zurück. Rebuild nach dem Rebuild-Vertrag in
[../architecture/SYSTEM_ARCHITECTURE.md](../architecture/SYSTEM_ARCHITECTURE.md).

### 10. Logs und externe Modellübertragung prüfen

Wurde das Secret an ein externes Modell übertragen? Steht es in Audit-Logs,
Traces oder Fehlermeldungen? Übertragung an Dritte lässt sich nicht
zurücknehmen — sie verschiebt die Bewertung von „bereinigt" zu „rotiert und
dauerhaft als kompromittiert geführt".

### 11. Vorfall und Maßnahmen dokumentieren

Zeitpunkt, Fundort, betroffene Systeme, durchgeführte Schritte, Entscheidungen.
**Ohne den Secret-Wert und ohne rekonstruierbare Teile davon.**

### 12. Verifikation durch eine zweite Prüfung

Eine unabhängige Prüfung bestätigt: Secret widerrufen, Arbeitskopien sauber,
Historie behandelt, abgeleitete Daten neu erzeugt, keine Restspuren in Index,
Embeddings, Packs oder Logs. Die Prüfung erfolgt **nicht** durch dieselbe
Instanz, die bereinigt hat.

### 13. Wiederfreigabe ausdrücklich dokumentieren

Der Human Maintainer erklärt die Arbeit ausdrücklich für wieder aufgenommen.
Ohne diesen Schritt bleibt der Vorfall offen.

### 14. Präventionsmaßnahme ableiten

Was hätte den Vorfall verhindert? `.gitignore`-Lücke, fehlende
Pre-Commit-Prüfung, fehlende Ingest-Prüfung, Ablage am falschen Ort?
Ergebnis wird eine konkrete Maßnahme im Risikoregister — kein Vorsatz.

---

## Reihenfolge auf einen Blick

```text
   erkennen ─► stoppen ─► ROTATION/WIDERRUF ─► Umfang bestimmen
                              (Schritt 3)
                                   │
                                   ▼
   Arbeitskopien ─► Git-Historie ─► Remotes/Forks ─► Derived löschen
                                                            │
                                                            ▼
   Logs/KI-Übertragung ◄─ Rebuild ◄─────────────────────────┘
            │
            ▼
   dokumentieren ─► zweite Prüfung ─► Wiederfreigabe ─► Prävention
```

Die beiden kritischen Kanten: **Rotation vor Cleanup** und **Bereinigung vor
Rebuild**.

## Rollen

| Rolle | Zuständigkeit |
| --- | --- |
| **Human Maintainer** | Alle Schritte. Rotation, Historienbereinigung, Wiederfreigabe |
| **Implementation Agent** | **Melden und anhalten.** Keine eigenständige Bereinigung, kein History-Rewrite, kein Zugriff auf den Secret Store |
| **Zweite Prüfinstanz** | Verifikation in Schritt 12; nicht identisch mit der bereinigenden Instanz |

## Was dieses Verfahren nicht leistet

- Keine automatische Erkennung — der Security Scanner ist geplant, nicht gebaut
- Keine technische Durchsetzung der Reihenfolge
- Keine Werkzeugempfehlung für History-Rewrites
- Keine Aussage über rechtliche Meldepflichten; bei personenbezogenen Daten ist
  gesondert zu prüfen (D-022 stellt PII außerhalb des Pilotumfangs)

## G0-Zuordnung

| Kriterium | Beleg | Status |
| --- | --- | --- |
| **D-8** Secret-Verfahren im Schadensfall | Dieses Dokument, 14 Schritte, Rollen, Reihenfolgeregeln | dokumentarisch erfüllt |

> **Einschränkung.** Erfüllt ist die **dokumentarische** Anforderung. Die
> technische Unterstützung — Erkennung, Sperrung, Rebuild-Automatik — existiert
> nicht. Risiko R-01 bleibt „teilweise gemindert", nicht geschlossen.

## Bezug

- [../privacy/DATA_CLASSIFICATION.md](../privacy/DATA_CLASSIFICATION.md) — Datenklasse `secret`
- [PERMISSION_MODEL.md](PERMISSION_MODEL.md) — Secret Store getrennt vom Wissensbestand
- [../architecture/TRUST_BOUNDARIES.md](../architecture/TRUST_BOUNDARIES.md) — TB-6 Repository-Grenze
- [../../.gitignore](../../.gitignore) — erste Verteidigungslinie, keine Garantie
