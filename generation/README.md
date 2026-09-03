# Short-horizon hypothesis generator

This upstream generator creates research ideas for intraday and short-swing
horizons of up to five trading days. It works from a versioned mechanism
catalogue and produces `INBOX` records only.

It explicitly performs no screening, backtesting, evidence grading, ranking, or
promotion.

## Run directly

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

The target folder must be empty or new. The producer never overwrites existing
results. It writes:

- `generation-run.json` with catalogue, mechanism, and operator provenance;
- `candidates/*.json` as valid, unscreened hypothesis intakes.

The generation run is also the complete candidate-universe reference. If all
created candidates are screened using data, record their number as
`planned_screen_count` in a search-space register before the first screen.

## Extending the catalogue

The catalogue is the source of candidate ideas. Each mechanism therefore has an
`entry_origin` containing its origin type, references, short rationale, and
timestamp. Repeated observations by the owner are recorded as
`INTERNAL_OBSERVATION` with a stable journal or observation reference. An origin
makes an entry eligible for generation; it does not make the idea true or
profitable.

## Generation routes

- `CONSTRAINT_FIRST`: scheduled or forced transactions;
- `MICROSTRUCTURE_STATE`: order-book, flow, or liquidity conditions;
- `LINKAGE_OR_IDENTITY`: futures, ETFs, basis, spreads, and hedge chains;
- `LITERATURE_REPLICATION`: published short-term findings turned into new
  candidates;
- `OBSERVATION_DRIVEN`: observed deviations or recurring sequences.

A named forced actor is plausible only for `CONSTRAINT_FIRST`; it is not a
general requirement for every candidate.

## Operators

- `PHASE_PATH`: anticipation, active phase, absorption, transmission,
  exhaustion, and unwind;
- `EXPECTATION_VIOLATION`: a missing or inverted expected imprint becomes a
  separate hypothesis;
- `MECHANISM_CONNECTION`: mechanisms with a common clock, venue, flow,
  hedge path, or payoff are connected;
- `ASSUMPTION_RELAXATION`: move the observable imprint from price direction to
  depth, spread, basis, volume, volatility, timing, or a linked instrument.

The optional agent contract is in
[`agents/intraday-hypothesis-generator.md`](../agents/intraday-hypothesis-generator.md).
A reproducible example is in
[`examples/generated-run/`](../examples/generated-run/).
