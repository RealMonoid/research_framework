# ADR-004: Executable gates and tiered entry

**Status:** ACCEPTED
**Date:** 2026-08-30

## Context

The framework described an agent regression gate, but the published harness only
scored a hand-authored fixture. No producer connected catalog inputs to an agent
run. The same fixture therefore scored 1.000 without measuring a model or prompt.
Validation had no CI workflow and the documented aggregate entry point was
PowerShell-centric.

At the research-entry layer, almost all hypothesis-candidate fields were required
for every status. Registering or rejecting an idea therefore carried much of the
cost of promotion. Detailed documents were also mandatory up-front.

Finally, four constraint/lever labels were normative prose without a machine
contract. The early Goldratt/ECE path duplicated later DAG and response work and
created repeated N/A obligations.

## Decision

### 1. Separate protocol smoke from agent quality

`eval-results.v2` requires `run_kind` and producer provenance.

- `PROTOCOL_SMOKE` validates contracts, scoring, and regression detection only.
- `LIVE_AGENT` is produced through a COMMAND or HTTP_JSON adapter.

`evals/produce_results.py` invokes one adapter call per case and never sends
`expected.assertions`. A release scorer must require `LIVE_AGENT`; the reference
fixture cannot satisfy that gate.

### 2. Add two automated validation layers

`scripts/validate_framework.py` is the cross-platform entry point. The existing
PowerShell entry remains supported. GitHub Actions runs Linux/Python and
Windows/PowerShell integrity jobs on push and pull request.

A separate manual workflow can produce and score a live result when an agent
endpoint is configured. Framework-integrity CI is not relabeled as a live-agent
quality gate.

### 3. Make intake requirements status-dependent

`INBOX`, `MERGED`, and `REJECTED` no longer require the full promoted research
payload. IDs, provenance, raw idea, consumed-information references, status, and
the appropriate transition record remain mandatory. `PROMOTED` retains full
scope, alternatives, data, feasibility, and epistemic-stage requirements.

### 4. Encode only decision-critical label invariants

`schemas/constraint_assessment.schema.json` defines the four labels. It enforces
that an `IDENTIFIED_CAUSAL_LEVER` has a passed identification gate and estimand,
and that an `IMPLEMENTATION_CONSTRAINT` follows phenomenon validation and
implementation feasibility. The schema does not attempt to encode all research
prose.

### 5. Route documentation instead of loading it all

`QUICKSTART.md` is the only universal entry. Detailed documents are loaded after
promotion and by activated method or artifact. Non-activated optional methods do
not produce N/A series.

The early Goldratt/ECE map is removed from the standard path. Goldratt remains
only as an optional prioritization aid for already evidenced implementation
constraints after phenomenon validation.

### 6. Keep the missing worked case explicit

No completed real Research Case is added by this decision. The repository must
state that it is not yet end-to-end practice-validated. Schema fixtures, eval
cases, and producer integration tests must not be presented as substitutes.

## Consequences

- A score of 1.000 now carries an explicit run class.
- The repository has an executable path from blind catalog input to agent output
  to release scoring, but a real quality claim still requires a configured agent.
- Small ideas can be captured or rejected without constructing a full research
  case.
- The sharp causal/implementation label rules are machine-testable.
- Initial context cost is reduced without weakening the promoted research path.
- Practical end-to-end process validation remains open until a suitable real case
  exists.

## Rejected alternatives

- Treating the reference fixture as a model baseline.
- Adding CI that only reruns the fixture while calling it an agent release gate.
- Encoding every prose rule in additional JSON Schema.
- Creating synthetic or invented worked Research Cases merely to close a
  documentation checkbox.
- Keeping the early ECE map while removing only its N/A checks.
