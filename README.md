# Research Framework

Governance-first framework for developing, falsifying, and validating market
research hypotheses without silently promoting an observed pattern to a causal
mechanism, forward prediction, or executable net trading edge.

The normative documents are written in German. AI agents and human reviewers
start with the compact [QUICKSTART.md](QUICKSTART.md). If no raw idea exists,
the executable [short-horizon generator](generation/README.md) can produce a
batch of literature-anchored intraday or short swing candidates first. Detailed
documents are loaded by status and task instead of being mandatory up-front:

1. Optionally generate raw ideas from the versioned market-mechanism catalog.
2. Record or reject a raw idea with the tiered hypothesis-intake schema.
3. Read [agent instructions](00_RESEARCH_AGENT_README.md) and the
   [research standard](01_RESEARCH_STANDARD.md) only after promotion.
4. Load the case template, selected methods, causal tooling, and operational
   rules when that part of the workflow is activated.

The machine-readable entry point for a new idea is the
[hypothesis candidate schema](schemas/hypothesis_candidate.schema.json), with a
small [inbox example](examples/hypothesis_candidate.inbox.json) and a full
[promoted example](examples/hypothesis_candidate.minimal.json). Architecture
decisions are recorded in [`decisions/`](decisions/), and deterministic agent
regression tests live in [`evals/`](evals/).

Every user-facing research task is coordinated by the
[research conductor](agents/research-conductor.md). It records a persistent
[orchestration checkpoint](schemas/orchestration_state.schema.json), obtains one
hard-rule next step from the executable
[router](scripts/route_research_task.py), and invokes the philosophy, condition,
or idea specialist only when its prerequisites and trigger are present. The
conductor retains the conversation, validates each returned artifact, and routes
again; a specialist never silently changes the research question.

The generator is deliberately not another gate. It combines mechanisms with
phases and observable responses, then applies phase-path,
expectation-violation, mechanism-connection, and assumption-relaxation
operators. Its output remains unscreened `INBOX`; it does not backtest, rank, or
promote ideas.

Strategies described in books, articles, videos, or courses have a separate
[prose-reconstruction path](reconstruction/README.md). It records the reviewed
source scope, distinguishes rules from examples, exposes missing or
discretionary definitions, and lists possible translations without choosing or
testing them. The committed
[VWAP example](examples/strategy_reconstruction.vwap_wave_price_discovery.json)
is a source extraction, not a backtest or profitability claim.

Before such a reconstruction is completed, the scientific-philosophy critic
produces a
[pre-operationalization concept audit](schemas/strategy_concept_audit.schema.json).
It separates strategy-defining conditions, source application advice,
suspected performance modifiers, and genuinely unknown success conditions. It
also records shared construction inputs and provisional state filters without
treating either as causal evidence. After a provisional definition exists, the
[condition inquiry](schemas/condition_inquiry.schema.json) can assess a
measurement instrument, definition sensitivity, interpretable performance
conditions, and their recurrence. A condition found in data remains a new
hypothesis and never silently rewrites the source strategy.

When a frozen result fails or remains undecidable, the dedicated
[scientific-philosophy critic](agents/scientific-philosophy-critic.md) maps the
hypothesis-plus-auxiliaries bundle and reviews proposed continuations. Its
[review contract](schemas/scientific_philosophy_review.schema.json) preserves
the original result, blocks unique failure attribution without discriminating
evidence, and permits a new empirical branch only for a genuinely new,
falsifiable prediction under a new Research-ID. The committed example is
synthetic and runs no backtest.

Generation runs are candidate-universe records. Before data-driven entry
screens begin, a search-space artifact freezes the tested family and its
multiplicity correction; a passing noise screen only authorizes Phase-0 effort.
Catalog entries also retain whether they originated in literature, a market
rule, or a stable internal-observation reference.

Promoted candidates record how their variables were chosen. Predefined,
theory-led variables need only a compact rationale; data-driven and hybrid
searches must disclose the candidate universe, data role, outcome visibility,
search space, retained variables, and selection-bias controls. The framework
also keeps causal claim level separate from mechanism evidence, forward OOS
prediction, and executable after-cost edge.

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

This validates JSON Schema contracts, the executable hypothesis generator, the
producer/scorer protocol, and the regression suite. The bundled score-1.000
result is explicitly a protocol smoke, not evidence of live-agent quality. A
release claim requires a produced `LIVE_AGENT` result.

## Direct raw entry point for automated readers

If a connector cannot traverse the GitHub interface, fetch the normative entry
point directly:

<https://raw.githubusercontent.com/RealMonoid/research_framework/main/QUICKSTART.md>
