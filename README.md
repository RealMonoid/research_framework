# Research Framework

Market strategies are often described in language that sounds precise but is
not precise enough to test. A book may say that a market is "in balance," that
volume is "strong," or that a breakout has "failed" without defining how any
of those statements should be measured. A researcher or an AI system must then
fill in the missing details. Those choices can quietly become part of the
strategy even though the source never stated them.

This creates several recurring problems:

- the tested strategy may no longer be the strategy that was originally
  described;
- hidden assumptions and discretionary choices may determine the result;
- definitions, time windows, filters, or targets may be changed after seeing
  the data;
- an observed association may be presented as a cause, a reliable forecast, or
  a tradable edge without sufficient evidence;
- after a failed test, the explanation may be adjusted until the original idea
  can no longer fail.

This framework is designed to make those problems visible and controllable. It
is a research process for turning an informal market idea into a documented,
testable question without silently changing what is being investigated.

## What the framework does

The framework:

- preserves what the original source actually claims;
- separates stated rules from examples, interpretations, assumptions, and
  unknown conditions;
- identifies concepts that still need a measurable definition before any test
  can be meaningful;
- records the research question, definitions, data choices, filters, costs,
  outcomes, and other material decisions as one protected research version;
- requires proposed changes to be shown to the user instead of silently
  replacing the existing version;
- calls for specialist review when a question involves unclear concepts,
  unknown success conditions, causal claims, or a proposed continuation after
  a failed or undecidable result;
- keeps descriptive evidence, prediction, causal explanation, and an
  executable after-cost trading edge as separate claims with different
  evidence requirements.

The framework cannot determine by logic alone which unknown conditions make a
strategy work. It can, however, record what is unknown, compare alternative
definitions without pretending they are equivalent, and prevent an unknown
condition from being smuggled into the strategy as an established fact.

## What it is for

The framework is intended for researchers who examine market hypotheses,
including strategies taken from books, articles, videos, courses, or informal
trading rules. It is especially useful when AI agents help with the research,
because it gives those agents explicit boundaries and keeps the user in control
of material decisions.

It is not a trading strategy, a profitability claim, or an automated approval
to run a backtest. It does not guarantee that a hypothesis is true, useful, or
tradable. Its purpose is narrower: to make the path from idea to conclusion
traceable, critical, and resistant to hidden changes.

## A typical case in plain language

1. Record the original idea and the source without improving or completing it.
2. Identify vague terms, missing rules, hidden assumptions, and conditions that
   are genuinely unknown.
3. List defensible ways to define the missing parts without selecting the one
   that produces the most attractive result.
4. Ask the user to approve a complete research version before empirical work
   begins.
5. Keep that version fixed while the approved analysis is performed.
6. Report whether the result supports, contradicts, or cannot decide the stated
   question, without silently rewriting the question.
7. If a change is justified, present it as a visible proposal for a new research
   version.

## Where to start

Start with the compact [QUICKSTART](QUICKSTART.md). If the starting point is a
strategy described in prose, use the
[strategy reconstruction path](reconstruction/README.md). If no initial idea
exists, the [short-horizon generator](generation/README.md) can create an
unranked set of literature-anchored candidates. Generating or reconstructing an
idea does not authorize a backtest.

Many of the existing normative documents are still written in German. New and
changed repository content is written in English. Translation of the existing
material and a consolidated terminology guide are planned as a separate
migration.

## Technical reference

The sections below describe the machine-readable contracts, routing rules, and
validation tools used to enforce the research process.

### Entry points and staged document loading

Detailed documents are loaded according to the status and needs of a case:

1. Optionally generate raw ideas from the versioned market-mechanism catalog.
2. Record or reject a raw idea with the tiered hypothesis-intake schema.
3. Read the [agent instructions](00_RESEARCH_AGENT_README.md) and the
   [research standard](01_RESEARCH_STANDARD.md) after promotion.
4. Load the case template, selected methods, causal tooling, and operational
   rules only when that part of the workflow is activated.

The machine-readable entry point for a new idea is the
[hypothesis candidate schema](schemas/hypothesis_candidate.schema.json), with a
small [inbox example](examples/hypothesis_candidate.inbox.json) and a full
[promoted example](examples/hypothesis_candidate.minimal.json). Architecture
decisions are recorded in [`decisions/`](decisions/), and deterministic agent
regression tests live in [`evals/`](evals/).

### Research coordination

Every user-facing research task is coordinated by the
[research conductor](agents/research-conductor.md). It records a persistent
[orchestration checkpoint](schemas/orchestration_state.schema.json), obtains one
hard-rule next step from the executable
[router](scripts/route_research_task.py), and invokes a specialist only when the
relevant prerequisites and trigger are present. Specialists return bounded
work to the conductor; they do not take over the user conversation or the final
decision.

### Protection against silent research changes

Every material research step carries a complete
[research fingerprint](schemas/research_fingerprint.schema.json). It contains
the question, source strategy, definitions, parameters, filters, exclusions,
data and sampling choices, inference rules, execution assumptions, frozen
results, continuation decisions, and protected artifact hashes.

The deterministic
[fingerprint check](scripts/check_research_fingerprint.py) compares returned
work with the effective research version. Work can be accepted only when the
material state is unchanged. Every difference becomes a visible change
proposal. The existing version remains effective unless the user explicitly
authorizes a new Research-ID or research version.

### Outcome roles and contradiction handling

Before a validation test is frozen, the conductor creates an
[outcome evidence contract](06_OUTCOME_EVIDENCE_CONTRACT.md). It states which
measurement is primary, which measurements test the proposed mechanism, which
are robustness checks, and which are exploratory only. It also records shared
construction inputs, multiplicity families, result consequences, and
target-specific stability expectations.

This prevents a successful prediction from being used to preserve a failed
mechanism story. Prediction, mechanism, phenomenon, and executable after-cost
edge remain separate conclusions. A frozen test cannot proceed without a
complete validated contract.

### Controls against invented results

Before real validation, the unchanged full pipeline must pass the
[pipeline integrity controls](07_PIPELINE_INTEGRITY_CONTROLS.md). Repeated
negative controls check whether the process invents effects where none were
constructed. A known-effect sentinel checks whether it recovers a deliberately
inserted effect with the correct sign and timing.

The reference world must preserve the market structure relevant to the method;
one simple random walk cannot be the only required negative control. A passed
synthetic or surrogate control authorizes only the next freeze step. It is not
evidence for a market effect, a forward prediction, a causal mechanism, or an
after-cost trading edge.

### Causal claims

An interventional or counterfactual claim has an additional mandatory stop. The
[causal-identification critic](agents/causal-identification-critic.md) must
produce a validated
[identification assessment](schemas/causal_identification_assessment.schema.json)
before causal estimation or causal wording is accepted. The review uses a
versioned
[quantitative-finance research basis](references/CAUSAL_IDENTIFICATION_FOR_FINANCE.md)
and examines event timing, counterfactual return models, simultaneity,
information shocks, spillovers, post-treatment variables, dependence, and
regime instability. A question that remains explicitly predictive does not
trigger this causal gate.

### Idea generation

The generator combines mechanisms with market phases and observable responses,
then applies documented transformation operators. Its output remains an
unscreened `INBOX` candidate set. It does not backtest, rank, or promote ideas.
Generation runs record the candidate universe. Before data-driven screening,
the tested family and its multiplicity correction must be frozen.

### Reconstruction of strategies described in prose

Strategies from books, articles, videos, or courses use a separate
[prose-reconstruction path](reconstruction/README.md). It records the reviewed
source scope, distinguishes rules from examples, exposes missing or
discretionary definitions, and lists possible translations without choosing or
testing them. The committed
[VWAP example](examples/strategy_reconstruction.vwap_wave_price_discovery.json)
is a source extraction, not a backtest or profitability claim.

Before reconstruction is completed, the scientific-philosophy critic produces
a
[pre-operationalization concept audit](schemas/strategy_concept_audit.schema.json).
It separates strategy-defining conditions, application advice from the source,
suspected performance modifiers, and genuinely unknown success conditions. It
also records shared construction inputs and provisional state filters without
treating them as causal evidence.

After a provisional definition exists, the
[condition inquiry](schemas/condition_inquiry.schema.json) can assess the
measurement instrument, sensitivity to alternative definitions, interpretable
performance conditions, and their recurrence. A condition found in data is a
new hypothesis; it never silently rewrites the source strategy.

### Failed and undecidable results

When a frozen result fails or remains undecidable, the
[scientific-philosophy critic](agents/scientific-philosophy-critic.md) maps the
hypothesis together with its auxiliary assumptions and reviews proposed
continuations. Its
[review contract](schemas/scientific_philosophy_review.schema.json) preserves
the original result, blocks unique failure attribution without discriminating
evidence, and permits a new empirical branch only for a genuinely new,
falsifiable prediction under a new Research-ID.

### Variable selection and evidence levels

Promoted candidates record how their variables were selected. Predefined,
theory-led variables require a rationale. Data-driven and hybrid searches must
disclose the candidate universe, the role of each dataset, outcome visibility,
the search space, retained variables, and controls for selection bias. The
framework separately records mechanism evidence, forward out-of-sample
prediction, causal claim level, and executable after-cost edge.

## Validation

Cross-platform:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_framework.py
```

Or from PowerShell:

```powershell
.\scripts\validate_framework.ps1
```

This validates the JSON Schema contracts, the executable hypothesis generator,
the producer/scorer protocol, and the regression suite. The bundled score of
1.000 is a protocol smoke test, not evidence of live-agent quality. A release
claim requires a produced `LIVE_AGENT` result.

Features that are not yet implemented are listed explicitly in
[`PLANNED_FEATURES.md`](PLANNED_FEATURES.md).

## Direct raw entry point for automated readers

If a connector cannot traverse the GitHub interface, fetch the normative entry
point directly:

<https://raw.githubusercontent.com/RealMonoid/research_framework/main/QUICKSTART.md>
