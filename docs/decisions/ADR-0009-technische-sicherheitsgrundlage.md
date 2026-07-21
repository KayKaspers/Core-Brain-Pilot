# ADR-0009 — Technische Sicherheitsgrundlage

| Feld | Wert |
| --- | --- |
| Status | **accepted** |
| Datum | 2026-07-21 |
| Entscheider | **Human Maintainer** |
| Angenommen am | **2026-07-21** |
| Autorität | **A0** — vier getrennte direkte Human-Maintainer-Entscheidungen |
| Supersedes | — |
| Superseded by | — |
| Entschieden in | **CBP-WP-011** |
| Belegt durch | ADR-0004 (A1), ADR-0006, ADR-0007, ADR-0008, PERMISSION_MODEL (A2), DATA_CLASSIFICATION (A2), D-006, D-021, D-023 |
| Schließt | **OD-34**, **OD-35** |

> **Dieser ADR ist angenommen und bindend.** Er trägt Autoritätsklasse **A1**.
> Die zugrunde liegenden Human-Entscheidungen tragen **A0**.
>
> **Er implementiert nichts.** Keine Kontrolle dieses ADR existiert technisch.

---

## Kontext

**ADR-0004** verlangt technische Durchsetzung von Berechtigungen.
**TECHNICAL_SECURITY_FOUNDATION_PLAN.md** (CBP-WP-008) benannte zwölf
Kontrollbereiche KB-01 bis KB-12 und eine Durchsetzungsreihenfolge — ließ aber
vier Fragen offen, die sich nicht aus der Architektur ableiten lassen:

| Frage | Wirkt auf |
| --- | --- |
| **Wie viele Identitäten?** | Schadensbegrenzung bei Kompromittierung, Rechtevererbung |
| **Wie werden Secrets referenziert und bereitgestellt?** | R-01, Migrierbarkeit, OD-34 |
| **Erlaubt oder verboten als Netzwerk-Default?** | Datenabfluss, Offline-Fähigkeit |
| **Wie wird Operational Evidence geschützt?** | Nachweisbarkeit, OD-35 |

**R-25 und R-27 sind seit CBP-WP-004 offen**, weil ein Berechtigungsmodell auf
Papier keine Zugriffskontrolle ist. Dieser ADR beseitigt das nicht — er macht
die Kontrollen **entscheidungsreif und abnehmbar**.

---

## Teilentscheidung A — Service-Identity-Modell

**SELECT A2 — getrennte logische Identitäten für Control Plane und Data
Worker**

### Human Notes

*Wortlaut unverändert übernommen:*

> Control Plane und Data Worker werden als getrennte logische
> Service-Identitäten mit minimalen, voneinander unabhängigen Rechten geführt.
>
> Die Control Plane verwaltet Konfiguration, Status, Review- und
> Freigabevorgänge. Sie darf Canonical Sources nicht verändern und keine
> Veröffentlichung automatisch ausführen.
>
> Der Data Worker verarbeitet ausschließlich freigegebene und aktivierte Source
> Boundaries. Er erhält keine Approval-, Administrations- oder Publish-Rechte
> und darf nur in ausdrücklich erlaubte Runtime-Bereiche schreiben.
>
> Konkrete Unix-Benutzer, Container-Identitäten, UID- und GID-Werte werden erst
> deploymentspezifisch festgelegt.

## Teilentscheidung B — Secret-Reference- und Pilot-Provider-Modell

**SELECT B1 — versionierter providerneutraler Secret-Reference-Vertrag plus
OS-geschützter Datei-Provider für den Pilot**

### Human Notes

*Wortlaut unverändert übernommen:*

> Der Core definiert einen versionierten, providerneutralen Secret-Reference-
> und Resolver-Vertrag.
>
> Für den ersten lokalen Pilot wird ein durch Betriebssystemrechte geschützter
> Secret-Dateibereich verwendet. Dieser Bereich liegt außerhalb von:
>
> - Core-Repository,
> - privatem Operator-Workspace,
> - Runtime-Datenbereich.
>
> Secret-Werte werden nur der jeweils berechtigten Service-Identität, nur
> read-only und nur für den erforderlichen Zweck bereitgestellt.
>
> Secret-Werte dürfen insbesondere nicht erscheinen in:
>
> - Git,
> - Mapping- oder Konfigurationsdateien,
> - Umgebungsvariablen,
> - Kommandozeilen,
> - Logs oder Operational Evidence,
> - Context Packs,
> - Fehlermeldungen,
> - Implementation Reports.
>
> Secret-Referenzen enthalten keine Secret-Werte und keine Hostpfade. Der
> Vertrag muss später ohne Änderung der allgemeinen Mappingkonvention auf einen
> externen Secret Manager migrierbar sein.

## Teilentscheidung C — Netzwerk-Egress-Grundsatz

**SELECT C1 — deny-by-default mit expliziter Egress-Allowlist**

### Human Notes

*Wortlaut unverändert übernommen:*

> Der Default für Netzwerk-Egress ist deny.
>
> Jede Freigabe muss ausdrücklich an Ziel, Provider, Zweck und erlaubte
> Service-Identität gebunden sein.
>
> Eine technisch erlaubte Netzwerkverbindung ist keine Datenfreigabe. Vor jeder
> externen Übertragung müssen zusätzlich mindestens geprüft werden:
>
> - Datenklasse,
> - AI-Transfer-Policy,
> - Approval-Zustand,
> - zulässiger Zweck,
> - freigegebenes Ziel.
>
> Unbekannte Ziele, nicht freigegebene Redirects und allgemeiner
> Internet-Egress bleiben blockiert.
>
> Lokale Suche und lokales Retrieval müssen ohne externen Netzwerkzugriff
> funktionieren.
>
> `excluded-from-ai` darf unabhängig von einer Netzwerkfreigabe keine externe
> Modellgrenze überschreiten.

## Teilentscheidung D — Operational-Evidence-Schutz

**SELECT D1 — logisch append-only, integritätsverkettet, aufbewahrungs- und
sicherungspflichtig**

### Human Notes

*Wortlaut unverändert übernommen:*

> RT-2 Operational Evidence wird logisch append-only geführt.
>
> Korrekturen erfolgen durch nachvollziehbare Folgeereignisse und nicht durch
> stillschweigendes Überschreiben bestehender Nachweise.
>
> Approval-, Audit-, Incident-, Aktivierungs-, Widerrufs-, Lösch-, Rebuild-,
> Backup- und Restore-Nachweise benötigen:
>
> - stabile Ereignisidentitäten,
> - nachvollziehbare Verkettung oder gleichwertigen Manipulationsschutz,
> - getrennte Zugriffsrechte,
> - definierte Aufbewahrung,
> - Backup,
> - Restore-Nachweis,
> - sichtbare Erkennung von Ketten- oder Integritätsbrüchen.
>
> RT-2 ist weder Cache noch kanonische Wissensbasis, kann aber nicht
> zuverlässig rekonstruiert werden. Sein Verlust kann einen Nachweisverlust
> darstellen.
>
> Die konkrete Aufbewahrungsdauer, Speichertechnologie und technische
> Implementierung werden deploymentspezifisch in späteren Work Packages
> entschieden.

---

## Entscheidung

Die technische Sicherheitsgrundlage ruht auf **vier Festlegungen**, die
gemeinsam die zwölf Kontrollbereiche abnehmbar machen:

| Gegenstand | Festlegung |
| --- | --- |
| **Identitäten** | **Zwei** getrennte logische Service-Identitäten: **Control Plane** und **Data Worker** |
| **Secrets** | **Versionierter, providerneutraler Referenzvertrag**; Pilotprovider ist ein **OS-geschützter Dateibereich** außerhalb aller drei Datenbereiche |
| **Netzwerk** | **Deny-by-default** mit expliziter Allowlist, gebunden an Ziel, Provider, Zweck und Identität |
| **Operational Evidence** | **Logisch append-only**, verkettet, mit Aufbewahrung, Backup und Restore-Nachweis |

### Vier abgeleitete Grundsätze

| # | Grundsatz | Herkunft |
| --- | --- | --- |
| **S-A** | **Verarbeitung erteilt keine Freigabe.** Wer Daten liest, darf sie nicht freigeben — Data Worker hat keine Approval-, Administrations- oder Publish-Rechte | Teil A |
| **S-B** | **Eine Referenz ist kein Secret.** Sie verweist, ohne zu verraten — kein Wert, kein Pfad, keine Zugangsdaten | Teil B |
| **S-C** | **Eine Netzwerkerlaubnis ist keine Datenfreigabe.** Erreichbarkeit und Übertragbarkeit sind getrennte Prüfungen | Teil C |
| **S-D** | **Ein Nachweis, der überschrieben werden kann, ist kein Nachweis.** Korrekturen sind Folgeereignisse, keine Änderungen | Teil D |

**S-C ist die schärfste der vier.** Sie verhindert die verbreitetste
Fehlannahme in Netzarchitekturen: dass ein erreichbares Ziel auch ein
zulässiges Ziel ist. Datenklasse, AI-Transfer-Policy, Approval-Zustand und
Zweck werden **zusätzlich** geprüft.

---

## Scope

- Vier Architekturentscheidungen für die Foundation Runtime
- Ableitung der zwölf Kontrollbereiche KB-01 bis KB-12
- Durchsetzungsreihenfolge in **neun** Stufen
- Negativtests, Nachweisstufen, Stop-Bedingungen, Rücksetzwege

## Non-Goals

| Nicht Gegenstand | Zuständig |
| --- | --- |
| Konkrete Unix-Benutzer, Container-Identitäten, UID/GID | Deployment, DRC |
| Hostpfade, Ports, IP-Bereiche, Provider | Deployment, DRC |
| Logging-, Datenbank-, Backup- oder Secret-Manager-Technologie | spätere Work Packages |
| Konkrete Aufbewahrungsdauer für RT-2 | **Deployment Required**, DRC |
| Implementierung, Tests, Betrieb | **CBP-WP-012** ff. — nicht autorisiert |
| Konkrete Egress-Ziele | Deployment, nach Zweckbindung |

---

## Service-Identity-Wirkung

| Aspekt | Wirkung |
| --- | --- |
| Schadensbegrenzung | Ein kompromittierter Data Worker erhält **keine** Freigabe- oder Administrationsrechte |
| Rechtevererbung | **Ausgeschlossen** — keine gemeinsame administrative Identität, kein impliziter Übergang |
| Impersonation | **Verboten** — keine Identität darf in die Rolle einer anderen wechseln |
| Betriebsaufwand | höher — zwei Identitäten, zwei Rechtesätze, zwei Mount-Matrizen |
| Deploymentbindung | **keine** — nur logische Identitäten festgelegt |

Vollständig in
[SERVICE_IDENTITY_AND_PRIVILEGE_MODEL.md](../security/SERVICE_IDENTITY_AND_PRIVILEGE_MODEL.md).

## Secret-Wirkung

| Aspekt | Wirkung |
| --- | --- |
| Referenzform | **versioniert** — unbekannte Version blockiert, kein Fallback |
| Providerneutralität | Resolver-Typ ist austauschbar; der Vertrag bleibt |
| **R-01** | **strukturell gemindert** — Referenzen enthalten keine Werte. **Nicht geschlossen**: Erkennung fehlt weiterhin |
| Verbotene Kanäle | Git, Mapping, Konfiguration, **Umgebungsvariablen**, Kommandozeilen, Logs, RT-2, Context Packs, Fehlermeldungen, Reports |
| Rotation | **ohne Änderung der Referenz** möglich |
| Migration | externer Secret Manager **ohne** Änderung der Mappingkonvention |

**Der Ausschluss von Umgebungsvariablen und Kommandozeilen ist die wirksamste
Einzelregel** — beides ist auf einem Linux-System für andere Prozesse
einsehbar.

Vollständig in
[SECRET_REFERENCE_AND_PROVIDER_CONTRACT.md](../security/SECRET_REFERENCE_AND_PROVIDER_CONTRACT.md).
**Schließt OD-34.**

## Netzwerk-Wirkung

| Aspekt | Wirkung |
| --- | --- |
| Default | **deny** — jede Erlaubnis ist explizit |
| Bindung | Ziel **und** Provider **und** Zweck **und** Service-Identität |
| Zusätzliche Gates | Datenklasse, AI-Transfer-Policy, Approval-Zustand, Zweck, freigegebenes Ziel |
| DNS und Redirect | heben die Zielbindung **nicht** auf |
| **Offline-Fähigkeit** | **Lokale Suche und Retrieval funktionieren ohne externen Egress** |
| `excluded-from-ai` | bleibt **unabhängig** von jeder Netzfreigabe blockiert |

Vollständig in
[NETWORK_EGRESS_POLICY.md](../security/NETWORK_EGRESS_POLICY.md).

## Operational-Evidence-Wirkung

| Aspekt | Wirkung |
| --- | --- |
| Semantik | **logisch append-only** |
| Korrektur | **Folgeereignis**, nie stilles Überschreiben |
| Integrität | Verkettung oder gleichwertiger Manipulationsschutz; **Bruch wird sichtbar** |
| Klassifikation | **RT-2 — kein Cache, keine kanonische Wissensbasis** |
| Rekonstruierbarkeit | **nicht zuverlässig gegeben** — Verlust ist Nachweisverlust |
| Aufbewahrung | **verpflichtend**; Dauer **Deployment Required** |
| Backup und Restore | verpflichtend, mit **Nachweis** |

Vollständig in
[OPERATIONAL_EVIDENCE_POLICY.md](../operations/OPERATIONAL_EVIDENCE_POLICY.md).
**Schließt OD-35** — mit Ausnahme der konkreten Aufbewahrungsdauer, die
Deployment Required bleibt.

## Datenschutzwirkung

**Hoch positiv, aber vollständig unwirksam.**

| Aspekt | Wirkung |
| --- | --- |
| `excluded-from-ai` | zweifache Prüfung: vor Context-Pack-Erstellung **und** vor externer Übertragung |
| Sammelanfragen | ausdrücklich einbezogen; gemischte Treffer blockieren |
| Zielwert | **null externe Leaks** |
| Datenklassengate | vor jeder externen Übertragung |
| Secrets | in keinem der drei Bereiche im Klartext |

**Grenze:** Sämtliche Kontrollen sind **dokumentarisch**. **R-25, R-27, R-30,
R-31 und R-32 bleiben offen.** Sie schließen durch bestandene Negativtests,
nicht durch diesen ADR.

## Berechtigungswirkung

| Aspekt | Wirkung |
| --- | --- |
| Autorisierung | **serverseitig**, deny-by-default |
| Erreichbarkeit | **ist keine Autorisierung** — lokal oder privat erreichbar genügt nie |
| Rollenwahl | **kein Client darf seine Rolle selbst festlegen** |
| Prüfumfang | Rolle **und** Ressource **und** Aktion **und** Approval-Zustand |
| Fehlerantworten | dürfen keine Secrets offenlegen |

Konkretisiert **ADR-0004** und die Matrix 9 Rollen × 12 Ressourcen aus
`PERMISSION_MODEL.md`.

## Backupwirkung

| Bereich | Sicherungspflicht | Wiederherstellung |
| --- | --- | --- |
| Core Repository | ja | Git plus Backup |
| **Operator-Workspace** | **ja — kanonisch** | nur aus Backup |
| **Secret Store** | **ja — getrennt** | **nie zusammen mit veröffentlichbarem Core-Inhalt** |
| RT-1 | nein | **Rebuild** |
| **RT-2** | **ja** | nur aus Backup; **nicht rekonstruierbar** |
| RT-3 | nein | gar nicht |

| # | Regel |
| --- | --- |
| **B-1** | Das Backupziel darf **nicht vom Anwendungsprozess überschreibbar** sein |
| **B-2** | Restore erfolgt in eine **getrennte Zielumgebung** |
| **B-3** | **Kein Überschreiben des letzten bekannten guten Backups** |
| **B-4** | RPO und RTO bleiben **Deployment Required** |

**R-20 bleibt offen** — es wurde kein Restore durchgeführt.

## Portabilitätswirkung

| Aspekt | Wirkung |
| --- | --- |
| Deploymentprofile | Alle fünf Profile nutzen dasselbe Identitäts- und Rechtemodell |
| Ortsbindung | ausschließlich in Deploymentwerten, nicht im Modell |
| Providerbindung | **keine** — Resolver-Typ und Egress-Ziele sind austauschbar |
| Proxmox | bleibt Referenzplattform, **nicht Produktgrenze** (ADR-0001) |

## Migrationswirkung

**Keine Migration erforderlich.** Es existiert keine Runtime, kein Secret
Store, keine Egress-Regel und kein RT-2-Speicher.

Ein späterer Wechsel auf einen externen Secret Manager ist ein
**Resolver-Wechsel**, kein Vertragswechsel — die Referenzform bleibt, die
Mappingkonvention aus ADR-0008 bleibt unberührt.

---

## Verworfene und vertagte Alternativen

| Option | Bewertung |
| --- | --- |
| **A1** — eine gemeinsame Identität | **verworfen.** Ein kompromittierter Worker erhielte Freigabe- und Administrationsrechte; Grundsatz S-A wäre nicht durchsetzbar |
| **DEFER A** | **verworfen.** Ohne Identitätsmodell sind Rechte-, Mount- und API-Kontrollen nicht spezifizierbar |
| **B2** — ausschließlich externer Secret Manager | **verworfen für den Pilot**, nicht für später. Ein externer Manager setzt eine Technologiewahl und Betriebsinfrastruktur voraus, die es nicht gibt. Der Vertrag hält den Weg offen |
| **DEFER B** | **verworfen.** OD-34 blockiert sonst CBP-WP-012 |
| **C2** — privates Netz erlaubt, extern einzeln blockiert | **verworfen.** Blocklisten sind unvollständig per Konstruktion; jedes neue Ziel wäre erlaubt, bis jemand es bemerkt |
| **DEFER C** | **verworfen.** Ohne Netzgrundsatz ist KB-10 nicht abnehmbar |
| **D2** — veränderbare Betriebslogs mit Backup | **verworfen.** Ein überschreibbarer Nachweis belegt nichts; Grundsatz S-D wäre verletzt |
| **DEFER D** | **verworfen.** OD-35 blockiert sonst den produktiven Betrieb |

## Offene Folgefragen

| Punkt | Register | Status |
| --- | --- | --- |
| Konkrete Unix-/Container-Identitäten, UID, GID | — | **Deployment Required**, DRC |
| Hostpfade des Secret-Bereichs | — | **Deployment Required** |
| **Konkrete Aufbewahrungsdauer für RT-2** | — | **Deployment Required**, DRC |
| Logging-, Datenbank-, Backuptechnologie | — | spätere Work Packages |
| Konkrete Egress-Ziele, Ports, Provider | — | Deployment, nach Zweckbindung |
| Ablageort des kanonischen Bestands | **OD-05** | **offen** |
| Konkrete Pilotquellen | **OD-06** | **offen** |
| Repository-Sichtbarkeit | OD-11 | offen |
| ID-, Collection- und Versionsvorschriften | OD-36 | offen |

**Keine dieser Fragen wird durch ADR-0009 beantwortet.** Der ADR legt Modelle
fest — nicht Werte, nicht Technologie, nicht Betrieb.
