# Eval-producer, scorer and regression gate

This directory separates three things that must not be confused:

1. A handwritten fixture checks contract and scorer.
2. The producer calls a real agent adapter blindly.
3. The scorer evaluates the produced result against catalog and baseline.

Producers and scorers only need the Python standard library. The platform-neutral schema suite uses the pinned development dependency from `requirements-dev.txt`.

## Artifacts

- `catalog.v1.json`: Versioned inputs and expected assertions.
- `examples/smoke-results.v1.json`: hand-authored `PROTOCOL_SMOKE` fixture
with `schema_version = eval-results.v2`; no agent quality certificate.
- `baseline.v1.json`: Minimum values and accepted comparison scores.
- `produce_results.py`: blind COMMAND-/HTTP_JSON producer.
- `run_evals.py`: structure check, scoring and regression gate.
- `tests/test_produce_results.py`: Producer blindness and run classes.
- `tests/test_run_evals.py`: scoring, error paths and regression detection.

The catalogue also examines the management of the research leader's processes: the mandatory conceptual examination before the operationalization of an incomplete prose strategy, the conditional analysis after a preliminary definition, the follow-up examination after a non-positive result and the counter-opposition of a pure explanation of results without unnecessary specialist agents.

Catalog, result and baseline must call the same `catalog_version`. Changes in input, expectation, weighting or fall meaning increase the catalog version.

## Framework integrity

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_framework.py
```

PowerShell is retained as a separately tested entry point in CI:

```powershell
.\scripts\validate_framework.ps1
```

Without `--live-results` both paths check framework and protocol integrity, not the quality of a model or prompt.

## Blinder Producer

The request contains `case_id`, capability, description, case input, sources and output contract. `expected.assertions` will never be sent to the adapter. Each catalog case will receive its own call.

Local adapter – the JSON array is executed without shell:

```bash
python evals/produce_results.py \
  --output artifacts/live-results.json \
  --run-id candidate-agent-001 \
  --run-kind LIVE_AGENT \
  --adapter-id local-agent \
  --command-json '["python","my_agent_adapter.py"]'
```

Provider-neutral HTTPS adapter:

```bash
python evals/produce_results.py \
  --output artifacts/live-results.json \
  --run-id candidate-agent-002 \
  --run-kind LIVE_AGENT \
  --adapter-id http-agent \
  --http-endpoint https://agent.example/eval \
  --token-env EVAL_AGENT_TOKEN
```

The adapter reads exactly one JSON request from stdin or HTTP body and delivers exactly one JSON case result. The producer assembles all cases, checks structure and source references, and writes the result atomically. Token values are neither stored nor hashed.

## Result adapter

Each case has a `claims` object. A claim contains at least:

```json
{
  "statement_class": "SOURCE_FACT",
  "evidence_status": "SUPPORTED",
  "source_ids": ["source_from_the_case"]
}
```

The permitted classes are `SOURCE_FACT`, `CALCULATED_VALUE`, `ESTIMATE`, `INFERENCE`, `FORECAST` and `HUMAN_JUDGMENT`. Evidence states are `SUPPORTED`, `PARTIAL`, `UNKNOWN`, `CONFLICTING`, `STALE` and `NOT_APPLICABLE`. Source IDs may only be displayed on the source of the respective catalog case.

## Run classes

- `PROTOCOL_SMOKE`: Contract test; no quality claim.
- `LIVE_AGENT`: agent run produced via COMMAND or HTTP_JSON.
A `LIVE_AGENT` result must not declare a `REFERENCE_FIXTURE` producer. A model/prompt release must explicitly require the running mode:

```bash
python evals/run_evals.py \
  --results artifacts/live-results.json \
  --require-run-kind LIVE_AGENT \
  --report artifacts/live-eval-report.json \
  --verbose
```

The supplied score-1.000 fixture fails due to this release gate because it is `PROTOCOL_SMOKE`.

## Assertions and exit codes

Supported operators are `equals`, `set_equals`, `approx_equals`, `is_empty` and `exists`. Each assertion has metric, weight and `critical`; missing paths fail explicitly.

- Exit `0`: requested structure, quality and regression gates passed.
- Exit `1`: at least one quality, runway or regression gate failed.
- Exit `2`: Structure, configuration, producer or report is incorrect.

`baseline.v1.json` requires a minimum of 0.95, for critical assertions 1.00 and for all safety/governance metrics the values documented there. `max_metric_drop` and `max_case_drop` are 0.0.

## CI and release

`framework-integrity.yml` runs the Linux/Python and Windows/PowerShell path on Push and Pull Request. This check can be requested as Branch Protection status, but remains an integrity check.

`live-agent-eval.yml` is a manual release workflow. It requires the repository variable `EVAL_AGENT_ENDPOINT` and optionally the Secret `EVAL_AGENT_TOKEN`, produces a `LIVE_AGENT` artifact and then forces the live gate. Without configured adapters, there is no live quality claim.

## Improvement rule

An observed agent error is first fixed as a reproducible catalog case or assertion. Afterwards, baseline and candidate are executed via the same blind producer. Expectations are not adjusted to the incorrect output; baseline changes require review. Smoke fixture and sample baseline are only evidence of the harness, not the agent.
