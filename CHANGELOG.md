# Änderungsprotokoll

Dieses Protokoll richtet sich ausdrücklich an **Agenten, die dieses Repository
lesen oder verändern** — menschliche Mitarbeit eingeschlossen. Es beantwortet
die Frage, die aus `git log` allein nicht zuverlässig hervorgeht: *wer* hat
*was* aus *welchem Grund* geändert und *wann*.

Am Repository arbeiten mehrere Agenten parallel und mit getrennten Arbeitskopien.
Ein Agent, der eine Datei liest, sieht ihr Ergebnis, aber nicht die Absicht
dahinter. Ohne Protokoll wiederholt der nächste Lauf verworfene Alternativen
oder revidiert eine Entscheidung, deren Begründung er nie gesehen hat.

## Verhältnis zu anderen Dokumenten

| Artefakt | Beantwortet |
|---|---|
| `git log` | was technisch passiert ist |
| `decisions/ADR-*.md` | warum eine Architekturentscheidung so ausfiel |
| **dieses Protokoll** | wer wann was mit welcher Absicht geändert hat |

Ein Eintrag ersetzt keinen ADR. Architekturentscheidungen brauchen weiterhin
einen ADR; der Protokolleintrag verweist darauf.

## Pflicht

Jeder Agent, der an diesem Repository etwas ändert, trägt **vor Abschluss
seiner Arbeit** einen Eintrag ein und unterzeichnet ihn mit seinem Namen. Die
Regel steht normativ in `00_RESEARCH_AGENT_README.md` §16b. Die Struktur der
Einträge wird von `scripts/test_changelog.py` maschinell geprüft und läuft in
beiden Validierungspfaden mit; der Wahrheitsgehalt eines Eintrags wird dadurch
nicht geprüft und bleibt Selbstdeklaration.

## Format

Neueste Einträge stehen oben. Jeder Eintrag ist eine Überschrift der Form
`## JJJJ-MM-TT — Titel`, gefolgt von diesen Feldern:

| Feld | Inhalt |
|---|---|
| `Agent` | Name und Modell des Agenten, bei Werkzeugkontext in Klammern |
| `Commit` | Kurz-Hash oder `ausstehend`, falls noch nicht committet |
| `Was` | die Änderung, sachlich und ohne Wertung |
| `Warum` | der Anlass; welches Problem bestand vorher |
| `Berührt` | betroffene Pfade |
| `Nicht getan` | bewusst ausgelassene Teile — optional, aber dringend empfohlen |
| `Signatur` | Name des Agenten, Gedankenstrich, Zeitstempel des Eintragsdatums |

Der Name in `Signatur` muss mit dem in `Agent` übereinstimmen, und das Datum in
`Signatur` muss dem Datum der Überschrift entsprechen.

<!-- EINTRAEGE -->

## 2026-08-31 — Datensnapshot-Zweig auf die Begriffs- und Leitungsschicht gesetzt

- **Agent:** Claude Opus 5 (Claude Code)
- **Commit:** ausstehend
- **Was:** Den noch offenen Datensnapshot-Zweig auf den aktuellen Hauptstand gesetzt. Die eigene Architekturentscheidung von ADR-010 auf ADR-012 umnummeriert, weil 010 und 011 inzwischen für Begriffsprüfung und Forschungsleitung vergeben sind. Den README-Konflikt so aufgelöst, dass beide Absätze erhalten bleiben.
- **Warum:** Codex hat Begriffsprüfung, Bedingungsanfrage und eine zentrale Forschungsleitung ergänzt. Der offene Zweig kollidierte dadurch in der Nummerierung und im README. Ohne Auflösung wäre entweder fremde oder eigene Arbeit verlorengegangen.
- **Berührt:** `decisions/ADR-012-data-snapshot-contract-and-ingest-adapters.md`, `README.md`, `CHANGELOG.md`, `scripts/validate_framework.py`, `scripts/validate_framework.ps1`
- **Nicht getan:** Keine fremde Datei inhaltlich verändert. Die neuen Prüfstufen von Codex wurden unberührt übernommen und laufen zusammen mit den eigenen; die gesamte Prüfung ist grün.
- **Signatur:** Claude Opus 5 — 2026-08-31

---

## 2026-08-31 — Änderungsprotokoll und Signaturpflicht für Agenten

- **Agent:** Claude Opus 5 (Claude Code)
- **Commit:** 966a029
- **Was:** Dieses Protokoll eingeführt, die Pflicht zu Eintrag und Signatur als §16b in den Agentenanweisungen verankert, in QUICKSTART verlinkt und mit `scripts/test_changelog.py` strukturell prüfbar gemacht.
- **Warum:** Am Repository arbeiten mehrere Agenten mit getrennten Arbeitskopien. `git log` zeigt, was passiert ist, aber nicht die Absicht; ADRs decken nur Architekturentscheidungen ab. Dazwischen fehlte eine Spur, die ein nachfolgender Agent lesen kann, bevor er dieselbe Stelle anfasst.
- **Berührt:** `CHANGELOG.md`, `scripts/test_changelog.py`, `00_RESEARCH_AGENT_README.md`, `QUICKSTART.md`, `scripts/validate_framework.py`, `scripts/validate_framework.ps1`
- **Nicht getan:** Einträge für die 11 Commits vor dem 2026-08-31 wurden nicht rekonstruiert. Ihre Absicht ist mir nicht bekannt und wäre erfunden; für diesen Zeitraum bleiben `git log` und die ADRs die einzige Quelle.
- **Signatur:** Claude Opus 5 — 2026-08-31

---

## 2026-08-31 — Datensnapshot-Vertrag und Binance-Ingest-Adapter

- **Agent:** Claude Opus 5 (Claude Code)
- **Commit:** 9581145
- **Was:** Schema `data_snapshot` (1.0.0) mit Vertragstests eingeführt, dazu einen nicht-normativen Ingest-Adapter für das öffentliche Binance-Archiv in `ingest/` samt Offline-Tests. Entscheidung in ADR-012 festgehalten. Beide Validierungspfade um zwei Stufen erweitert.
- **Warum:** Zwischen `data_requirements` (welche Daten nötig sind) und `consumed_data_refs` (welche verbraucht wurden) fehlte jeder Vertrag. Eine Referenz wie `csv:SYMBOL:60:2024..2026` war weder auflösbar noch prüfbar, wodurch ein eingefrorener Suchraum wertlos wird, sobald der Datenstand darunter unbemerkt wechselt. Anlass war eine reale Machbarkeitsprüfung, die an Exportgrenzen und lückenhaften Indikatorspalten eines Chart-Werkzeugs scheiterte.
- **Berührt:** `schemas/data_snapshot.schema.json`, `scripts/test_data_snapshot.py`, `examples/data_snapshot.binance_klines.json`, `ingest/`, `decisions/ADR-012-data-snapshot-contract-and-ingest-adapters.md`, `README.md`, `.gitattributes`, `scripts/validate_framework.{py,ps1}`
- **Nicht getan:** QUICKSTART und die Normdokumente `00`–`05` blieben unverändert. Dass `consumed_data_refs` künftig auf `snapshot:`-Bezeichner zeigen soll, steht bisher nur in ADR-012 und README, nicht im verbindlichen Kurzpfad. Ebenso ist die Abdeckungsanalyse des Adapters nur für `klines` implementiert, nicht für `aggTrades`, `trades` oder `fundingRate`.
- **Signatur:** Claude Opus 5 — 2026-08-31

---
