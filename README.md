# Trading Research Framework

## The goal

This project exists to answer one practical question:

> Does a trading idea justify risking capital as a complete, executable
> strategy—and if not, what exactly has the investigation established?

The programme aims to identify or develop trading strategies with a defensible
positive expected **net** edge. “Net” matters: an apparent pattern is not enough.
The edge must remain credible after realistic costs, liquidity, slippage,
capacity, execution, portfolio interaction, and risk. The complete strategy must
also survive genuinely unseen data or a controlled forward test before it can
support a capital decision.

The project follows two routes under the same evidential standard:

1. **Test an existing strategy rigorously.** Preserve what its source actually
   said, expose missing definitions, and test the resulting research version
   without silently improving it after seeing results.
2. **Develop a new strategy hypothesis.** Generate candidates through bounded,
   explicit, literature- or market-grounded search, retain the full search
   history, and subject selected candidates to independent evidence.

Both routes must learn from positive, negative, inconclusive, blocked, and
not-testable outcomes. That learning may improve later representations,
measurements, candidate generation, or test design. It does not become evidence
for a different strategy unless the transfer itself is tested.

Scientific discipline is therefore a means to the trading objective, not the
end product. Methodological cleanliness does not create an edge; it helps the
owner avoid risking money on artifacts and recognize a real effect if one is
present. An individual case may correctly end without an active strategy. That
protects capital without changing the programme-level goal.

The adopted mission decision is recorded in
[ADR-016](decisions/ADR-016-applied-interdisciplinary-trading-research-mission.md).
The [interdisciplinary foundations](references/INTERDISCIPLINARY_TRADING_RESEARCH_FOUNDATIONS.md)
and [ADR-017](decisions/ADR-017-interdisciplinary-claim-coordinates-and-production-loop.md)
explain how finance, cognitive science, AI search, philosophy of science,
experimental design, statistics, machine learning, decision theory, and
production engineering contribute without being blended into one theory.

## Why this is difficult

Trading ideas often sound more precise than they are. A source may say that a
market is “in balance,” volume is “strong,” or a breakout has “failed” without
defining how to measure those statements. The researcher or AI agent must fill
in the gaps, and those choices can quietly become a different strategy.

Other errors arise later: searching many definitions but reporting only the
winner, reusing validation data, presenting association as causation, adding a
new condition after a failed test, or treating a promising backtest as if data
quality, execution, costs, capacity, portfolio effects, and operational risk
were already solved.

The framework makes those choices and transitions visible. It cannot discover
the correct missing condition by logic alone, guarantee that a viable strategy
exists, or turn a plausible mechanism into predictive evidence.

## The research path in plain language

```text
existing strategy -> faithful source reconstruction --\
                                                    -> explicit research version
new hypothesis  -> bounded, recorded candidate search /
    -> feasibility and data checks
    -> fixed candidate pipeline and outcome evidence contract
    -> pipeline integrity checks and freeze
    -> independent validation and robustness assessment
    -> separate conclusions for phenomenon, prediction, mechanism/causality, and net edge
    -> data, execution, cost, capacity, portfolio, risk, attribution, and operations
    -> complete-strategy unseen-data or controlled forward evidence
    -> capital decision, monitoring, revalidation, suspension, or rejection
```

In a typical case:

1. Record the idea, source, market, horizon, and intended claim.
2. Separate explicit rules from examples, interpretations, assumptions, and
   genuinely unknown conditions.
3. Define measurable alternatives without selecting the one that looks best in
   hindsight.
4. Perform the current phase-0 feasibility and available-data checks without
   consuming validation data. The stronger prospective data-fitness gate is a
   separately recorded planned feature, not a completed control.
5. Let the owner approve the complete research version before empirical work.
6. Freeze the claim, outcomes, analysis, search family, and stopping rules.
7. Test on the data role permitted for that stage and report uncertainty,
   dependence, multiplicity, stability, and limitations.
8. Preserve the result. Any material revision becomes a visible proposal for a
   new Research-ID or version rather than a repair of the old outcome.
9. Only after a validated phenomenon and an explicit continuation decision,
   engineer and retest the complete strategy under realistic production
   conditions.

Reconstructing or generating an idea does not authorize a backtest. A successful
backtest does not authorize deployment or capital allocation. The research
owner alone makes capital decisions; no status, artifact, agent, or validator
does so automatically.

## What the framework protects

The framework:

- preserves the identity and provenance of the strategy being tested;
- protects scarce independent data from undocumented search and repeated use;
- records definitions, parameters, filters, exclusions, costs, data choices,
  outcomes, and other material decisions as one research version;
- keeps observation, prediction, mechanism, causality, executable net edge, and
  capital action as separate claims with separate evidence requirements;
- makes proposed changes visible to the owner instead of silently replacing the
  effective version;
- assigns one lead owner to the next question for each selected bottleneck while
  retaining competing and coupled constraints;
- treats independent data history, compute, elapsed time, attention, capital,
  liquidity, and risk-bearing capacity as different scarce resources rather than
  one score that can buy permission to ignore a hard rule;
- invokes bounded specialist review only when the relevant question and
  prerequisites require it; and
- treats data quality, execution, costs, capacity, portfolio construction,
  sizing and ruin risk, profit-and-loss (PnL) attribution, monitoring, and
  operations as part of strategy engineering.

## Legitimate outcomes and cumulative learning

A Research Case does not have to produce a strategy. It may support or contradict
the frozen claim, remain inconclusive, identify a remediable data gap, be not
testable with the available evidence, or stop because further research is not
worth its cost. These are decision-relevant outcomes, not failed paperwork.

An adverse result applies first to the tested bundle of claim, definitions,
data, implementation, and auxiliary assumptions. It does not identify one guilty
component by itself. A revised feature, regime, mechanism, condition, or trading
rule is a new candidate or research version. Prior findings may guide its design,
but they do not confer edge evidence on it.

## Scope, readers, and privacy

This is a private decision-support framework for one research owner working with
AI agents. It is not an academic-publication workflow, an external-review
package, a human-team onboarding system, a trading strategy, a profitability
claim, or an automated approval to run a backtest.

The repository serves two necessary readers:

- the owner, who must be able to understand and revisit a decision later; and
- the agents, which need precise rules despite limited context and no reliable
  memory of earlier sessions.

Public repository content is limited to framework material. Proprietary
strategies, private data, real Research Cases, and empirical results belong
outside the tracked repository or under the ignored `private_research/` path.
Existing examples require a separate privacy classification before removal.

A rule, artifact, or planned feature belongs here only when it protects a
research or capital decision or demonstrably improves an existing protection.
Work solely for presentation, external persuasion, or hypothetical contributors
is out of scope. The normative and agent-facing repository material is maintained
in English.

## Start here

- Begin with the compact [QUICKSTART](QUICKSTART.md).
- For a strategy described in prose, use the
  [strategy reconstruction path](reconstruction/README.md).
- If no initial idea exists, the
  [short-horizon generator](generation/README.md) can create an unranked,
  literature-anchored candidate set.
- After promotion, use the [agent entry point](00_RESEARCH_AGENT_README.md) and
  [research standard](01_RESEARCH_STANDARD.md).

## Technical reference

The sections below describe the machine-readable contracts, routing rules, and
validation tools used to enforce the research process. This repository is a
provider-neutral specification and toolkit used by a host AI agent; it is not a
standalone research service, broker connection, or execution engine. Some rules
are machine-checked, while others still depend on caller enforcement or expert
judgement, or remain planned gaps. The
[hard-gate inventory](HARD_GATE_INVENTORY.md) records that difference rather
than claiming end-to-end enforcement.

[`AGENTS.md`](AGENTS.md) is the sole authoritative policy for agents and controls
every conflict. `QUICKSTART.md`, the research standard, ADRs, schemas, and this
README explain or implement parts of that policy; none is a second authority.

| Layer | Main implementation |
|---|---|
| Authority and entry | [`AGENTS.md`](AGENTS.md) is the sole agent-policy source; [`QUICKSTART.md`](QUICKSTART.md) is the compact human and agent entry path. |
| Research state | Versioned JSON artifacts record candidates, checkpoints, evidence roles, fingerprints, reviews, and results under [`schemas/`](schemas/). |
| Coordination | The conductor owns the conversation and state; the deterministic router returns the next hard-rule action. |
| Change control | Complete fingerprints compare the candidate state with the effective research version before returned work is accepted. |
| Evidence gates | Outcome contracts separate claim roles; pipeline integrity controls must pass before validation is frozen. |
| Specialist work | Philosophy, condition inquiry, data analysis, causal identification, and workflow-control review are bounded routes with explicit triggers. |
| Verification | Semantic validators, schema tests, generator tests, and adversarial evaluations run through `scripts/validate_framework.py`. |

Key terms used below:

| Term | Meaning in this repository |
|---|---|
| `INBOX` candidate | A recorded raw idea, not a confirmed or fully specified research case. |
| `PROMOTED` candidate | An idea precise and basically testable enough to enter phase 0; promotion confirms no phenomenon, forecast, mechanism, or edge. |
| Research Case | One versioned investigation with a defined question, scope, evidence roles, and protected decision history. |
| Test freeze | The point after the outcome contract and pipeline-integrity gate when the validation design becomes fixed. |
| Validated phenomenon | A phenomenon supported under its frozen design; not by itself a mechanism, complete strategy, or executable net edge. |
| Effective research version | The currently accepted material state against which proposed work is compared. |
| Material change | A change to the question, strategy identity, scope, definitions, data, rules, assumptions, inference, result, or continuation decision protected by the complete fingerprint. |
| Complete strategy | The full signal, rules, data path, execution, costs, capacity, portfolio, risk, attribution, and operating specification that must receive its own unseen-data or forward evidence. |

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

Before a specialist call or an availability blocker, the conductor records a
validated
[specialist capability check](schemas/specialist_capability_check.schema.json)
against the exact routing decision. It must inspect the live tool inventory and
use a suitable internal agent interface when one exists. A same-conversation
return does not make the specialist run non-independent: the relevant
independence is a separate bounded run with restricted inputs and no authority
over the user conversation or research state. Incomplete discovery is
`UNKNOWN`, not evidence that the specialist is unavailable.

The conductor also applies five permanent workflow controls on every task:
scope is locked to the user's request, delegation has one bounded level,
material conclusions need validated evidence, unchanged checks are not repeated,
and completion statuses require their evidence and validation. These controls
are recorded in every routing decision; they do not depend on AI Psychiatry and
do not turn specialized critics into universal steps.

Every routing decision also carries a plain-language progress brief: the
current position, the framework's next action, what follows, and whether the
owner needs to act. Required choices include weighted alternatives and a
recommendation. A blocking or materially disruptive problem is separately
recorded with the acting model, timestamps, description, impact, and recovery
options before it is presented to the owner; real-case records remain private.

### Bounded quantitative data analysis

For a concrete quantitative question that needs more than simple arithmetic,
the conductor can call the bounded, provider-neutral
[data analyst](agents/data-analyst.md). The role may examine referenced
price/volume/volatility or other research data and report provenance, data
quality, decision-time availability, uncertainty, stability, alternatives, and
limits in a [data-analysis report](schemas/data_analysis_report.schema.json).
It keeps intraday and swing scopes separate, checks leakage and regime/session
mixing where relevant, and includes costs, slippage, liquidity, and
in-sample/out-of-sample separation for a trading evaluation. It never makes a
trade, risk, causal, activation, or research-state decision; association is not
causality and a report is not authorization to run a backtest. If the data are
not coherent or sufficient, it records a limited or blocked result. The
conductor validates the report and performs the full fingerprint comparison.
The planned prospective data-fitness gate remains a separate prerequisite for
future cases.

### Conditional workflow-control review

When the owner explicitly asks for a framework stress test, or a concrete trace
shows a possible bypass, the conductor can invoke the
[framework-control reviewer](agents/framework-control-reviewer.md). The reviewer
uses one bounded mode—red-team, loophole, strategy identity, scope, root cause,
rule conflict, or memory validation—to examine observable workflow evidence.
Its machine-readable report is checked by
[`validate_framework_control_review.py`](scripts/validate_framework_control_review.py)
against [`framework_control_review.schema.json`](schemas/framework_control_review.schema.json).

This is a conditional, caller-enforced control review, not an extra gate on
ordinary research and not a clinical assessment. The optional AI-Psychiatry
plugin can provide the same provider-neutral modes, but it is not a second rule
source. The review cannot run a backtest, change the effective research state,
or replace the scientific-philosophy or causal-identification specialist. Any
material proposal still goes through the full fingerprint and user-decision
process.

### Technical architecture review (OpenAI Developers)

The architecture review recorded in
[ADR-014](decisions/ADR-014-framework-control-review-and-runtime-boundary.md)
used OpenAI Developers as an implementation aid on 2026-09-03. It found that
the existing conductor, deterministic router, structured artifacts, bounded
specialist work orders, and regression tests already provide the useful parts
of a manager-led agent design. No Agents SDK or MCP runtime was added: this
repository has no runnable agent service. Adding a second orchestration path
would create new state and failure modes
without a demonstrated reliability, cost, or research-quality benefit. If a
runtime is introduced later, it should keep one conductor as owner, use typed
tool contracts and server-side validation, make material writes explicit, and
evaluate the actual execution path rather than only the final text.

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
authorizes a new Research-ID or research version. A fingerprint protects only
the material state that was actually recorded and hashed; it cannot prove that
an omitted or incorrectly recorded choice never occurred.

The [hard-gate inventory](HARD_GATE_INVENTORY.md) distinguishes controls that
are automatically invoked from executable checks that still depend on the
host agent, schema-only constraints, judgement calls, prose rules, and missing
controls. It also records the stop consequence, regression evidence, and known
bypass for each gate. This prevents the existence of a validator from being
mistaken for proof that every live research run actually used it.

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

## Framework validation

These commands validate repository contracts, generators, and regression
behavior. They do not validate a trading strategy, market claim, empirical
result, capital decision, or live agent.

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

Prioritized work, conditional options, and completed foundations are listed in
[`ROADMAP.md`](ROADMAP.md).

## Direct raw entry point for automated readers

If a connector cannot traverse the GitHub interface, fetch the normative entry
point directly:

<https://raw.githubusercontent.com/RealMonoid/trading-research-framework/main/QUICKSTART.md>
