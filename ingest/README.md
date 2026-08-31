# Ingest-Adapter

Dieses Verzeichnis enthaelt **nicht-normative** Bezugsquellen. Es gehoert nicht
zum Regelwerk des Frameworks und entscheidet nichts ueber Hypothesen, Evidenz
oder Promotion.

Ein Adapter hat genau eine Aufgabe: Rohdaten beschaffen und daraus einen
Snapshot nach
[`schemas/data_snapshot.schema.json`](../schemas/data_snapshot.schema.json)
erzeugen. Der Vertrag ist anbieterneutral; weitere Adapter koennen ergaenzt
werden, ohne dass sich das Schema aendert.

## Warum getrennt vom Vertrag?

Das Framework ist governance-first und venue-neutral. Ein Adapter haengt
dagegen an der URL-Struktur und den Dateiformaten eines konkreten Anbieters.
Diese Kopplung bleibt bewusst ausserhalb der Normdokumente, damit eine Aenderung
bei einer Boerse kein Vertragsproblem erzeugt.

Aus demselben Grund ist die CI netzwerkfrei: Planung, Pruefsummen-Parsing,
Abdeckungsanalyse und Snapshot-Aufbau sind reine Funktionen und werden offline
gegen Fixtures geprueft. Nur `fetch` und `run` sprechen mit dem Netz und werden
nicht automatisch getestet.

## Binance Public Data

`binance_public_data.py` laedt aus dem oeffentlichen Archiv
`data.binance.vision`. **Kein API-Key, kein Account, keine Zugangsdaten.**
Werden fuer eine Quelle jemals Zugangsdaten noetig, gehoeren sie nicht in dieses
Repository und nicht in einen Adapter.

Unterstuetzt werden `klines`, `aggTrades`, `trades` und `fundingRate` fuer
`spot`, `um` (USD-M-Futures) und `cm` (COIN-M-Futures).

Erst planen, ohne etwas zu laden:

```bash
python ingest/binance_public_data.py --symbol ETHUSDT --interval 1m \
  --from-month 2019-11 --to-month 2026-07 --out data/ --plan-only
```

Dann laden, Pruefsummen verifizieren und Snapshot schreiben:

```bash
python ingest/binance_public_data.py --symbol ETHUSDT --interval 1m \
  --from-month 2019-11 --to-month 2026-07 --out data/binance/um/ETHUSDT/1m \
  --snapshot artifacts/snapshots/ethusdt-1m.json
```

Jede Archivdatei wird gegen die vom Anbieter mitgelieferte `.CHECKSUM` geprueft;
eine Abweichung bricht ab und loescht die Datei.

## Groessenordnungen

| Datenart | Umfang |
|---|---|
| `klines` 1m, ein Symbol, mehrere Jahre | Dutzende bis wenige hundert MB |
| `fundingRate` | sehr klein |
| `aggTrades` | zweistellige bis dreistellige GB pro Symbol ueber Jahre |

`aggTrades` sind die einzige Quelle fuer echtes Volume-at-Price. Wer POC, Value
Area oder Low-Volume-Bereiche aus `klines` bildet, arbeitet mit einer Naeherung.
Ein OHLCV-Snapshot traegt diesen Hinweis deshalb automatisch in
`known_limitations`.

## Was ein Snapshot nicht ist

Ein Snapshot belegt Herkunft, Abdeckung und Integritaet. Er belegt **nicht**,
dass die Daten fuer eine bestimmte Hypothese ausreichen. Ob Historientiefe und
Ereignisdichte tragen, entscheidet die Machbarkeitspruefung vor Phase 1 — nicht
der Download.
