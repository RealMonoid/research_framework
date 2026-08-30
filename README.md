# Research Framework

Governance-first framework for developing, falsifying, and validating market
research hypotheses without silently promoting an observed pattern to a causal
mechanism, forward prediction, or executable net trading edge.

The normative documents are written in German. AI agents and human reviewers
start with the compact [QUICKSTART.md](QUICKSTART.md). Detailed documents are
loaded by status and task instead of being mandatory up-front:

1. Record or reject a raw idea with the tiered hypothesis-intake schema.
2. Read [agent instructions](00_RESEARCH_AGENT_README.md) and the
   [research standard](01_RESEARCH_STANDARD.md) only after promotion.
3. Load the case template, selected methods, causal tooling, and operational
   rules when that part of the workflow is activated.

The machine-readable entry point for a new idea is the
[hypothesis candidate schema](schemas/hypothesis_candidate.schema.json), with a
small [inbox example](examples/hypothesis_candidate.inbox.json) and a full
[promoted example](examples/hypothesis_candidate.minimal.json). Architecture
decisions are recorded in [`decisions/`](decisions/), and deterministic agent
regression tests live in [`evals/`](evals/).

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

This validates JSON Schema contracts, the producer/scorer protocol, and the
regression suite. The bundled score-1.000 result is explicitly a protocol smoke,
not evidence of live-agent quality. A release claim requires a produced
`LIVE_AGENT` result.

## Direct raw entry point for automated readers

If a connector cannot traverse the GitHub interface, fetch the normative entry
point directly:

<https://raw.githubusercontent.com/RealMonoid/research_framework/main/QUICKSTART.md>
