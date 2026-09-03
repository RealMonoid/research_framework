# Reconstructing strategies from prose

This path translates strategies from books, articles, videos, or courses into
a comprehensible specification. It is a **translation aid**, not a backtest,
strategy generator, or effectiveness gate.

## Why keep a separate artifact?

A source can describe a recognizable strategy while leaving terms such as
“strong volume,” “clear breakout,” “the pullback holds,” or “near resistance”
open. If those gaps are filled silently, it is no longer possible to tell what
came from the source and what was added by the researcher.

[`schemas/strategy_reconstruction.schema.json`](../schemas/strategy_reconstruction.schema.json)
therefore separates:

1. the source passage that was reviewed;
2. source-faithful, paraphrased statements;
3. statements that are essential to the strategy's identity;
4. open constructs and their source status;
5. possible operationalizations and their origin; and
6. a later, explicit decision.

Before a reconstruction is completed and a definition is frozen, the
[`scientific-philosophy-critic`](../agents/scientific-philosophy-critic.md)
also creates a [`strategy_concept_audit`](../schemas/strategy_concept_audit.schema.json).
This early examination is part of the reconstruction. It is not a backtest and
not an additional effectiveness gate.

## Four types of conditions

The concept audit must distinguish:

1. **Strategy-defining conditions:** Without them, it would no longer be the
   same source strategy.
2. **Conditions of use stated by the source:** The source recommends or
   requires them, but that does not yet show that they cause success or are
   necessary for it.
3. **Suspected success modifiers:** Literature, theory, or the researcher
   considers them plausible. They remain candidates and are not silently added
   as filters.
4. **Unknown conditions of success:** The framework does not claim to know all
   requirements. This uncertainty is explicitly retained.

## Construction dependencies

Trace the trigger, state, target, and outcome back to their raw data, windows,
and deterministic calculations. Shared inputs or windows can create a
statistical relationship or change the question being answered. That is:

- not causal evidence;
- not automatically a construction error; and
- not a reason to silently replace the source-oriented target with another one.

The audit only makes visible which part of the observable relationship could
come from the researcher's construction and therefore needs separate
interpretation.

## Regime and state filters

A filter is first of all a **provisional measuring instrument**. It does not
prove that a literally real hidden market state exists, and it does not identify
an actor or mechanism. The share of observations that a filter assigns to a
class is not, by itself, evidence that the filter separates anything useful.

A later assessment therefore asks whether the fixed classification distinguishes
future behaviour that was not already used to calculate the filter, and whether
it adds information beyond its continuous inputs or a simple comparison rule.
If the filter is not informative, the state claim that depends on it fails. An
event claim that can be evaluated independently of the filter may remain open.

## Source status of a construct

| Status | Meaning |
|---|---|
| `SOURCE_SPECIFIED` | The source defines a reproducible definition. |
| `SOURCE_ALTERNATIVES` | The source gives several definitions or ways to act. |
| `UNSPECIFIED` | The construct is named but not defined measurably. |
| `DISCRETIONARY` | Human contextual judgement is an explicit part of the method. |
| `CONTRADICTORY` | The reviewed passages use incompatible definitions. |

A source claim also receives `source_force`. In particular, `ILLUSTRATIVE`
remains an example and does not silently become a rule.

## Candidates are neither a selection nor tests

`operationalization_candidates` may contain definitions from the source, domain
conventions, external literature, a documented researcher proposal, or a human
protocol. The list records possibilities. It does not mean:

- that one variant has been chosen;
- that every variant should be tested;
- that the number of variants is already a statistical multiplicity count; or
- that a proposed definition appeared in the source.

A later decision sets `decision.status`. If variants are compared later in a
result-dependent way, the search space actually examined at that point is the
one that counts. The reconstruction artifact itself does not access market
data.

## Possible end states

- `REPLICATION`: only when all essential definitions genuinely come from the
  source.
- `DOCUMENTED_RECONSTRUCTION`: open points were made visible and supplemented
  with reasons.
- `SIMPLIFIED_VARIANT`: essential discretionary or optional parts were
  deliberately removed.
- `PLAYBOOK_ONLY`: the source remains a decision framework, not one unique
  executable rule.

A mechanical partial replica of a discretionary source is therefore not called
a replication.

## Workflow

The research conductor saves an orchestration checkpoint before starting and
follows the decision from `scripts/route_research_task.py`. The specialist agent
does not address the user directly; its audit returns to the conductor, who
routes the work again.

1. Record only the sections actually read in `locators_reviewed`.
2. Paraphrase statements and separate rules, recommendations, options, and
   examples.
3. Record `strategy_identity_claim_refs`: What must not disappear without
   creating a different strategy?
4. Classify every construct and record open questions.
5. Record possible definitions with their actual origin.
6. Leave `decision.status = UNDECIDED` initially.
7. Before selecting a definition, complete the concept audit: classify
   conditions, identify construction dependencies, distinguish measuring
   instruments, and preserve unknown conditions of success.
8. Only then, in a genuine reconstruction, choose definitions or set a human
   protocol and assign the fidelity label.

## Quantitative inquiry into conditions

After a provisional operationalization, the
[`condition-inquiry-analyst`](../agents/condition-inquiry-analyst.md) may create a
[`condition_inquiry`](../schemas/condition_inquiry.schema.json). This artifact
is not only a control; it can also produce new, testable condition hypotheses:

- construction-dependence checks and neutral simulations for possible built-in
  relationships;
- a multiverse or specification curve for dependence on defensible measurement
  definitions;
- interpretable partitions and conditional forecasting for the question of how
  the result changes under conditions known at the decision time; and
- time and environment stability checks for whether a condition recurs.

A condition found in data is recorded as a **new success-modifier hypothesis**.
It is not retrospectively declared to have been a prerequisite of the source
strategy all along.

## If later validation fails

A failure does not automatically prove that the selected operationalization was
the part that was wrong; the test covered the complete bundle of the core
hypothesis and its auxiliary assumptions. It also does not permit choosing a
more favourable definition from the candidate list after seeing the result and
then rescuing the old test.

If continuation is considered, the
[`scientific-philosophy-critic`](../agents/scientific-philosophy-critic.md)
creates a [`scientific_philosophy_review`](../schemas/scientific_philosophy_review.schema.json).
The old result remains unchanged. An alternative definition may be pursued
empirically only under a new Research-ID if it creates a new, refutable
prediction that can be tested on independent data.

The worked source example is
[`examples/strategy_reconstruction.vwap_wave_price_discovery.json`](../examples/strategy_reconstruction.vwap_wave_price_discovery.json).
It deliberately ends at `SOURCE_EXTRACTION`: no definition is selected.

## Inspect and summarize

```bash
python scripts/inspect_strategy_reconstruction.py \
  examples/strategy_reconstruction.vwap_wave_price_discovery.json
```

The inspector checks the schema, IDs, references, selection consistency, and
inappropriate replication labels. It selects nothing and does not test a
market strategy.

The two additional contracts can be inspected separately:

```bash
python scripts/inspect_strategy_concept_audit.py \
  examples/strategy_concept_audit.synthetic.json

python scripts/inspect_condition_inquiry.py \
  examples/condition_inquiry.synthetic_measurement.json
```

Both examples are synthetic and contain no market results.
