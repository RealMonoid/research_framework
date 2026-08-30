# Research Framework

Governance-first framework for developing, falsifying, and validating market
research hypotheses without silently promoting an observed pattern to a causal
mechanism, forward prediction, or executable net trading edge.

The normative documents are written in German. AI agents and human reviewers
must start with [00_RESEARCH_AGENT_README.md](00_RESEARCH_AGENT_README.md) and
follow its mandatory reading order:

1. [Agent instructions](00_RESEARCH_AGENT_README.md)
2. [Research standard](01_RESEARCH_STANDARD.md)
3. [Research case template](02_RESEARCH_CASE_TEMPLATE.md)
4. [Research methods](03_RESEARCH_METHODS.md)
5. [Causal tooling](04_CAUSAL_TOOLING.md)
6. [Agent operations](05_AGENT_OPERATIONS.md)

The machine-readable entry point for a new idea is the
[hypothesis candidate schema](schemas/hypothesis_candidate.schema.json), with a
[minimal example](examples/hypothesis_candidate.minimal.json). Architecture
decisions are recorded in [`decisions/`](decisions/), and deterministic agent
regression tests live in [`evals/`](evals/).

## Validation

From PowerShell, run:

```powershell
.\scripts\validate_framework.ps1
```

This validates the JSON Schema contracts, the reference eval run, and the
regression test suite.

## Direct raw entry point for automated readers

If a connector cannot traverse the GitHub interface, fetch the normative entry
point directly:

<https://raw.githubusercontent.com/RealMonoid/research_framework/main/00_RESEARCH_AGENT_README.md>

