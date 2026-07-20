# Human Discovery Input — Erhebung beim Human Maintainer

| Feld | Wert |
| --- | --- |
| Datum der Erfassung | 2026-07-20 |
| Work Package | CBP-WP-003 |
| Quelle | **Direkte Antworten des Human Maintainers** im Projektchat |
| Erhebungsform | Minimal Human Discovery Questionnaire, sechs kombinierte Fragen |
| Autoritätsklasse dieses Dokuments | A2 |
| Stand | 2026-07-20 |

Dieses Dokument enthält **kein Chatprotokoll**, sondern normalisierte
Antworten. Es wurde nichts ergänzt, abgeleitet oder plausibilisiert, was nicht
ausdrücklich gesagt wurde.

> **Autoritätsregel.** Dieses Dokument ist **nicht pauschal A0**. Nur einzelne,
> ausdrücklich getroffene Entscheidungen tragen A0 und sind unten einzeln
> gekennzeichnet. Reine Infrastruktur- und Sachangaben sind Human-Evidenz,
> aber keine Projektentscheidungen.

Es wurden **keine Secrets, Zugangsdaten, IP-Pläne oder Konfigurationsdetails**
erfragt oder dokumentiert.

---

## A1 — Betriebsprofil

**Antwort (normalisiert).** Proxmox-VM. Die Anwendung soll innerhalb einer
dedizierten Linux-VM betrieben werden; Docker Compose ist als **bevorzugte**
Anwendungslaufzeit innerhalb dieser VM vorgesehen. Proxmox ist die erste
Referenzplattform, aber keine technische Produktgrenze. Allgemeine Linux-VMs,
Docker/OCI und lokale Einzelplatzinstallationen sollen später als weitere
Deploymentprofile dokumentierbar bleiben.

| Zuordnung | Wert |
| --- | --- |
| P0-Fragen | 6.1, 6.2 |
| G0-Kriterien | F-1, F-2, F-5 |
| Status | **accepted** |
| Autorität | **A0** — ausdrückliche Entscheidung |

**Enthaltene A0-Entscheidungen:** D-015, D-016, D-017 (siehe unten).

**Nicht enthalten:** Proxmox-Version, CPU-, RAM-, Storage- und Diskwerte. Diese
sind bewusst nicht erhoben worden und bleiben Deployment Required.

---

## A2 — Nutzungsmodus

**Antwort (normalisiert).** Einzelperson. Der erste Pilot ist für einen Human
Maintainer vorgesehen; ungefähre Nutzerzahl im ersten Pilot: 1. Die Architektur
soll spätere Nutzung durch ein kleines Team nicht verhindern. Multi-User- und
Multi-Tenant-Funktionen sind **kein Pflichtumfang** des ersten Piloten.

| Zuordnung | Wert |
| --- | --- |
| P0-Fragen | 3.1, 3.2 |
| G0-Kriterien | A-1, A-2 |
| Status | **answered** (Sachangabe) für A-1, A-2 · **accepted** für die Scope-Entscheidung |
| Autorität | A0 nur für die Abgrenzung „kein Pflichtumfang" (D-018) |

**Nicht enthalten:** Zahl und Typ der Geräte (A-3). Bleibt offen.

---

## A3 — Wissensquellen

**Antwort (normalisiert).**

Im ersten Pilot benötigt:

- Markdown-Verzeichnisse
- Git-Repositories
- Chat-Handoffs
- Obsidian-Vaults **als Markdown-Quelle**

Später, nach dem Markdown-Retrieval-Fundament:

- PDF-Dokumente
- Office-Dokumente
- weitere kontrollierte Quellenarten

PDF- und Office-Dokumente sollen **nicht ungeprüft direkt in den kanonischen
Bestand** gelangen. Dafür ist später eine kontrollierte Ingest- und
Quarantäne-Pipeline vorgesehen.

| Zuordnung | Wert |
| --- | --- |
| P0-Fragen | 4.1 (Quellenarten), 4.3 (Formate) |
| G0-Kriterien | D-1, D-3 |
| Status | **answered** für die Quellenarten · **accepted** für die Ingest-Abgrenzung |
| Autorität | A0 nur für „kein ungeprüfter Direkteingang für PDF/Office" (D-019) |

**Nicht enthalten:** Größenordnung, Dateizahl, Volumen (D-2). Ausdrücklich
nicht erfragt — keine vollständige Dateiinventur. Bleibt Deployment Required.

---

## A4 — Datenschutzprofil

**Antwort (normalisiert).**

| Datenklasse | Angabe |
| --- | --- |
| `public` / `internal` | Hauptsächlich diese beiden im ersten Pilot |
| `confidential` | **Nicht Bestandteil** des ersten produktiven Piloten. Die Architektur muss die Klasse jedoch unterstützen |
| `excluded-from-ai` | Muss **von Anfang an** im Daten- und Berechtigungsmodell enthalten sein. Die technische Sperrwirkung soll zunächst mit **synthetischen oder unkritischen Testdaten** geprüft werden |
| Personenbezogene Daten | **Nicht** für den ersten Pilot vorgesehen. Bei späterer Aufnahme ist vorher eine gesonderte Datenschutz- und Rechtsgrundlagenprüfung erforderlich |
| `secret` | **Immer verboten** in Wissensbestand, Git-Repository, Suchindex, Embeddings, Wiki und Context Packs |

| Zuordnung | Wert |
| --- | --- |
| P0-Fragen | 4.4, 4.5, 4.6 (verneint für Pilot), 4.7 (verneint für Pilot) |
| G0-Kriterien | D-4, D-5 · D-6 und D-7 werden `not-applicable` für den Pilotumfang |
| Status | **accepted** — mehrere ausdrückliche Entscheidungen |
| Autorität | **A0** für D-020, D-021, D-022 |

**Bemerkenswert:** Die Anforderung, `excluded-from-ai` von Anfang an im Modell
zu führen und die Sperrwirkung mit Testdaten zu prüfen, ist strenger als das
bisherige Fundament. Sie macht aus Risiko R-30 eine konkrete, prüfbare
Anforderung.

**Nicht enthalten:** Das **Verfahren**, wenn ein Secret in die Git-Historie
gelangt ist (D-8). Das Verbot ist bestätigt, der Ablauf im Schadensfall nicht.
**Bleibt offen und Core Required.**

---

## A5 — Zugriffsprofil

**Antwort (normalisiert).** Privates VPN beziehungsweise privates Netzwerk.
Interne Dienste sollen **nicht öffentlich freigegeben** werden. Die konkrete
Technologie — bestehendes VPN, Tailscale, WireGuard oder vergleichbar — wird
erst im Deployment-Readiness-Schritt ausgewählt.

| Zuordnung | Wert |
| --- | --- |
| P0-Fragen | 2.1, 2.2, 2.4 (Profilebene) |
| G0-Kriterien | C-1, C-2, C-6 — als Deployment Required vertagt |
| Status | **accepted** für das Zugriffsprofil · Technologiewahl bleibt **open** |
| Autorität | **A0** für D-023 |

**Nicht enthalten:** Netzwerkdetails, IP-Adressen, Konfigurationen. Ausdrücklich
nicht erfragt.

---

## A6 — Optionale Funktionen im Pilot

**Antwort (normalisiert).**

| Funktion | Einstufung | Bedingung laut Antwort |
| --- | --- | --- |
| Web-UI | **im Pilot benötigt** | Erst nachdem Index, Suche, Brain-First-Retrieval und Benchmark grundsätzlich funktionieren. Bleibt austauschbare Darstellungsschicht |
| Mobile Nutzung | **im Pilot benötigt** | Suche, Lesen, Projektstatus, Handoffs, kleine Freigaben. Keine vollständige mobile Entwicklungsumgebung |
| Native Obsidian-Nutzung | **später** | Serverzentrierte Nutzung hat Vorrang. Produktive Mehrgeräte-Synchronisation erst nach Test-Vault sowie Konflikt- und Restore-Prüfung |
| Wiki-Pilot | **später** | Erst nach bestandenem Retrieval-Pilot. Wiki-Inhalte bleiben abgeleitet, als A6 gekennzeichnet, dürfen autoritative Quellen nicht automatisch verändern |
| Externe Connectoren | **später** | Zunächst keine breite Anbindung. Jeder Connector benötigt einen eigenen Datenschutz-, Rechte- und Löschprozess |
| Knowledge Graph | **nicht für den ersten Pilot benötigt** | Später als reproduzierbare abgeleitete Sicht prüfbar, wenn Retrieval-Nutzen und Datenqualität belegt sind |

| Zuordnung | Wert |
| --- | --- |
| P0-Fragen | 3.4, 3.5 (Arbeitsfälle), 3.7 (Obsidian), 6.4 (UI-/Wiki-Gate), 7.2 (Nicht-Ziele, teilweise) |
| G0-Kriterien | A-4, A-5, A-7, F-6 |
| Status | **accepted** |
| Autorität | **A0** für D-024, D-025 |

---

## Ausdrücklich getroffene Entscheidungen (A0)

Jede dieser Markierungen ist auf eine konkrete Aussage begrenzt.

| ID | Entscheidung | Quelle |
| --- | --- | --- |
| D-015 | Erstes Pilotprofil ist eine Proxmox-VM mit dedizierter Linux-VM als Referenzbetrieb | A1 |
| D-016 | Docker Compose ist die **bevorzugte** Anwendungslaufzeit innerhalb dieser VM | A1 |
| D-017 | Deployment-Neutralität wird beibehalten: allgemeine Linux-VM, Docker/OCI und Einzelplatz bleiben dokumentierbare Profile | A1 |
| D-018 | Multi-User und Multi-Tenant sind **kein Pflichtumfang** des ersten Piloten; die Architektur darf spätere Teamnutzung nicht verhindern | A2 |
| D-019 | PDF- und Office-Dokumente gelangen **nicht ungeprüft** in den kanonischen Bestand; kontrollierte Ingest- und Quarantäne-Pipeline erforderlich | A3 |
| D-020 | `confidential` ist nicht Teil des ersten Piloten, muss aber architektonisch unterstützt werden | A4 |
| D-021 | `excluded-from-ai` ist **von Anfang an** im Daten- und Berechtigungsmodell zu führen; Sperrwirkung mit synthetischen oder unkritischen Testdaten zu prüfen | A4 |
| D-022 | Personenbezogene Daten sind nicht Teil des ersten Piloten; spätere Aufnahme erfordert vorher eine gesonderte Datenschutz- und Rechtsgrundlagenprüfung | A4 |
| D-023 | Zugriff nur über privates VPN oder privates Netz; **keine öffentliche Freigabe interner Dienste** | A5 |
| D-024 | Web-UI und mobile Nutzung gehören zum Pilotumfang, die Web-UI aber erst nach funktionierendem Index, Suche, Brain-First-Retrieval und Benchmark | A6 |
| D-025 | Native Obsidian-Nutzung, Wiki-Pilot und externe Connectoren werden vertagt; Knowledge Graph ist nicht Pilotumfang | A6 |

## Nicht getroffene Entscheidungen

Ausdrücklich **nicht** entschieden — hier wurde nichts abgeleitet:

| Punkt | Status |
| --- | --- |
| Konkrete VPN-Technologie | offen, Deployment Required |
| Verfahren bei Secret in der Git-Historie (D-8) | **offen, Core Required** |
| Berechtigungsstufen je Bereich und Freigabeverfahren (E-2 bis E-5) | **offen, Core Required** |
| Repository dauerhaft privat? (Teil von A-8) | **offen, Core Required** |
| Trennung canonical/derived als ADR (F-3) | offen, Core Required |
| Benchmarkplan (G-1 bis G-6) | offen, Core Required |
| Zahl und Typ der Geräte (A-3) | offen, Deployment Required |
| Größenordnung des Wissensbestands (D-2) | offen, Deployment Required |
| Alle konkreten Infrastrukturwerte (B-1 bis B-8, F-4) | offen, Deployment Required |

## Offene Rückfragen

Fünf Punkte, die dieser Intake **nicht** erhoben hat und die für den
allgemeinen Scope Lock weiterhin fehlen:

1. **Secret-Verfahren im Schadensfall** — das Verbot ist bestätigt, der Ablauf
   nicht (D-8).
2. **Berechtigungsmodell** — welche der fünf Stufen gilt je Bereich, und wie
   läuft die Freigabe (E-2 bis E-5)?
3. **Repository-Sichtbarkeit** — dauerhaft privat, oder später öffentlich?
4. **Explizite Nicht-Ziele** — A6 liefert funktionale Abgrenzungen, aber keine
   vollständige Nicht-Ziel-Liste (A-8).
5. **Benchmarkfragen** — mindestens 30, noch keine formuliert. Setzt die
   Größenordnung des Bestands voraus.

Diese sind Gegenstand des vorgeschlagenen Folge-Work-Packages.

## Nachweis der Nichtergänzung

- Es wurde keine Antwort erfunden, erweitert oder aus Kontext abgeleitet.
- Was nicht gefragt wurde, ist als „nicht enthalten" gekennzeichnet.
- Was gefragt, aber nicht beantwortet wurde, steht unter „Nicht getroffene
  Entscheidungen".
- `accepted` wurde ausschließlich vergeben, wo eine ausdrückliche Entscheidung
  vorliegt; Sachangaben tragen `answered`.
