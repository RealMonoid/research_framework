# Short-horizon hypothesis generator

Dieser vorgelagerte Generator erzeugt Research-Ideen für Intraday- und kurze
Swing-Horizonte bis fünf Handelstage. Er arbeitet aus einem versionierten
Mechanismenkatalog und endet bei günstigen `INBOX`-Datensätzen.

Er führt ausdrücklich kein Screening, Backtesting, Evidence Grading, Ranking
oder Promotion durch.

## Direkt ausführen

```bash
python scripts/generate_hypotheses.py \
  --output-dir artifacts/futures-ideas-001 \
  --run-id generation:futures-ideas-001 \
  --markets FUTURES \
  --horizons MINUTES HOURS SESSION \
  --max-candidates 20
```

PowerShell:

```powershell
python .\scripts\generate_hypotheses.py `
  --output-dir artifacts\futures-ideas-001 `
  --run-id generation:futures-ideas-001 `
  --markets FUTURES `
  --horizons MINUTES HOURS SESSION `
  --max-candidates 20
```

Der Zielordner muss leer oder neu sein. Der Producer überschreibt keine
vorhandenen Ergebnisse. Er schreibt:

- `generation-run.json` mit Katalog-, Mechanismen- und Operator-Provenienz,
- `candidates/*.json` als valide, ungescreente Hypothesen-Intakes.

Der Generation-Run ist zugleich die vollständige Kandidatenuniversums-Referenz.
Wer alle erzeugten Kandidaten datenbasiert screent, trägt deren Anzahl vor dem
ersten Screen als `planned_screen_count` in ein Search-Space-Register ein.

## Katalog erweitern

Der Katalog ist der eigentliche Ideenbestand. Jeder Mechanismus besitzt deshalb
ein `entry_origin` mit Ursprungstyp, Referenzen, Kurzbegründung und Zeitpunkt.
Eigene wiederholte Beobachtungen werden als `INTERNAL_OBSERVATION` mit einer
stabilen Journal- oder Beobachtungsreferenz aufgenommen. Der Ursprung macht den
Eintrag generierbar, aber noch nicht wahr oder profitabel.

## Erzeugungsrouten

- `CONSTRAINT_FIRST`: terminierte oder erzwungene Transaktionen,
- `MICROSTRUCTURE_STATE`: Orderbuch-, Flow- oder Liquiditätszustände,
- `LINKAGE_OR_IDENTITY`: Futures, ETFs, Basis, Spreads und Hedge-Ketten,
- `LITERATURE_REPLICATION`: publizierte Kurzfristbefunde als neue Kandidaten,
- `OBSERVATION_DRIVEN`: beobachtete Abweichungen oder wiederkehrende Abläufe.

Ein benannter gezwungener Akteur ist nur bei `CONSTRAINT_FIRST` naheliegend und
keine allgemeine Bedingung.

## Operatoren

- `PHASE_PATH`: Antizipation, aktive Phase, Absorption, Transmission,
  Erschöpfung und Unwind,
- `EXPECTATION_VIOLATION`: ein ausbleibender oder invertierter Abdruck wird zu
  einer separaten Hypothese,
- `MECHANISM_CONNECTION`: Mechanismen mit gemeinsamem Takt, Venue, Flow,
  Hedge-Pfad oder Payoff werden verbunden,
- `ASSUMPTION_RELAXATION`: der beobachtbare Abdruck wird von Preisrichtung auf
  Tiefe, Spread, Basis, Volumen, Volatilität, Timing oder ein verknüpftes
  Instrument verschoben.

Der optionale Agentenvertrag steht in
[`agents/intraday-hypothesis-generator.md`](../agents/intraday-hypothesis-generator.md).
Ein reproduzierbares Beispiel liegt unter
[`examples/generated-run/`](../examples/generated-run/).
