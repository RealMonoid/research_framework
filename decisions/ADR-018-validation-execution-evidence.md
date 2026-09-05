# ADR-018: Bind validation decisions to frozen protocols and execution evidence

- Status: Adopted for the supported contracts and local synthetic runner.
- Date: 2026-09-05.
- Decision protected: whether a test may enter validation and whether its
  result may support a prediction or executable edge. This implements existing
  safeguards; it does not authorize research or replace data fitness.

## Problem and decision

The previous outcome contract accepted a frozen test without a protocol and
silently preferred one of two protocol fields. Repeated random walks bypassed
the negative-control check. Pipeline results could consist entirely of typed
success declarations, and the router trusted `COMPLETE` references without
opening them. These defects were reproduced on the pre-change implementation.

Outcome contracts and pipeline assessments use schema version **2.0.0**.
Checkpoints and routing decisions use **1.10.0**. There is one canonical
`validation_protocol`; the legacy `forward_testing_protocol` is rejected,
including when its contents agree with the canonical field.

The protocol specifies a zoned start timestamp and either an integer observation
or trade count, or explicit calendar/historical start and end timestamps. The
adapter counts each eligible observation or completed trade as one observation
event according to the frozen measurement rule. Calendar boundaries are exact
inclusive boundary instants, not date strings interpreted in a local timezone.
Data coverage and eligibility still require the binding data-fitness assessment;
an observation log cannot prove that the source omitted no data.

No-interim policies admit no inspection. Fixed audits require ordered dates or
counts within the horizon and cannot terminate the test. Alpha-spending policies
require each inspection's allocated alpha and p-value threshold, plus a total
budget. The implemented conservative allocation requires each threshold to be
no larger than its allocation and the sum no larger than the budget. This is a
union-bound allocation, not a generic implementation of every sequential test.
Validity of each p-value and the frozen multiplicity family remain prerequisites.
An alpha crossing ends the test immediately; later observations, even at the
same timestamp, invalidate it. Safety aborts remain permitted operationally but
do not become valid completed evidence.

The complete research fingerprint protects both the canonical protocol digest
and the pre-test outcome-design digest. Assessment fields are excluded from
that design projection, avoiding a self-referential hash. Protected artifact IDs
must be unique: one fingerprint cannot offer several alternative commitments.

## Execution and ordinary call paths

An assessed outcome contract references a separate `validation_execution` file.
It binds the original frozen contract, complete fingerprint and protocol to an
observer event log. `validation_observer.py` derives counts, boundaries,
termination, inspections and deviations from individual `START`, `OBSERVATION`,
`INSPECTION`, `DEVIATION`, and `END` events. The summary must match that stream.
The validator then compares it with the original frozen protocol and outcome
design. Early or late completion, clipping, an unplanned inspection, changed
rules, missing evidence, or any recorded deviation returns `INVALID_TEST`
errors. Such an artifact cannot pass as prediction or executable-edge support.
An `execution_validation` classification must equal the computed violations.
An invalid execution can be retained as a consistent invalid-test assessment
only when every outcome is `INVALID_TEST` and no evidence stage is supported;
the existing frozen decision effects still apply. This preserves post-failure
review without admitting the failed run as valid evidence.
The evidence is retained; validation never repairs the protocol or rewrites a
result. A missing original commitment cannot be reconstructed after results.

`route_research_task.py` opens the `evidence_file` (path and SHA-256) of every
outcome/pipeline artifact declared `COMPLETE`, invokes its full validator and
checks its identity and effective fingerprint. A recorded result additionally
requires an assessed outcome contract and compatible primary-outcome results,
before interpretation or post-result specialist routing. `PRECISE_NULL` uses
the contradicted-outcome category; this compatibility check does not establish
precision, which still requires the frozen inference evidence. Routing errors
are failures, not routing decisions. The conductor must record the prerequisite
problem through the existing problem-record path before continuing.

File references resolve relative to the containing artifact, not the shell's
working directory. API callers can pass `base_dir`; command-line entry points
set it from the input file. Schema-only checks are not substitutes for these
semantic and evidence checks.

## Pipeline execution and numerical evidence

Required null families are compared as a set. One or many random walks alone
cannot satisfy the gate. Every control records its complete unique seed list,
planned count, completed count, numerical detection-rate acceptance interval,
precision target, and uncertainty result. Completed runs must equal the frozen
plan; there is no seed selection, early success, or extra replication option.

The supported uncertainty method is independent Bernoulli detection-rate
standard error: `sqrt(p * (1-p) / n)`. Planning uses the conservative bound
`sqrt(0.25 / n)` and requires at least `ceil(0.25 / requested_SE^2)` runs. The
existing 200-run floor is retained: under this method it guarantees a worst-case
standard error at most approximately 0.03536. It is neither a universal Monte
Carlo sufficiency rule nor evidence that a reference model is adequate. Tighter
precision requires more runs. Dependent replications or other uncertainty
methods need an explicit reviewed extension, not prose substitution.

`pipeline_execution.py PLAN --output NEW_DIRECTORY` is the explicit local
synthetic runner. It refuses an existing output directory and empirical inputs.
The plan must already pass validation, match the runtime and be hash-protected.
The complete candidate entrypoint runs in a **new subprocess for each
replication**, with one generated input and the frozen configuration. It cannot
receive the other replications through this interface. Each receipt records the
seed, request digest, output and exit status; input and output files are retained.
The assessment is calculated from those outputs and the frozen numerical rules.
Failed subprocesses leave partial evidence and no successful assessment.

The pipeline manifest protects the entrypoint, declared dependencies,
configuration and Python runtime. The control-plan commitment also protects the
generator, seeds, structure claims, expected truth and acceptance rules. The
locked plan, source hashes and result evidence are rechecked. A positive sentinel
must require detection above all null acceptance intervals.

Only the bundled paired-uniform synthetic generator currently has an independent
truth verifier. Its shifted/unshifted inputs are reconstructed from every seed;
the shift must match the declared known-effect direction or no-effect null.
The verifier recognizes within-pair dependence only. A generator name, custom
script, asserted known effect, or claimed additional preserved structure cannot
pass in its place. New generators require a reviewed truth/structure verifier.
This narrow interface fixture is not a verified market backtest backend.

## Migration

1. Preserve original v1 artifacts and their history. Do not edit private cases
   automatically. A v1 frozen/assessed artifact fails current validation.
2. For a genuinely unexecuted draft, replace the alias with the canonical field,
   specify exact boundaries and complete inspection rules from pre-existing
   commitments, and produce a visible new version through normal change control.
   Do not infer a historical horizon from observed results or convert free text
   without a recorded interpretation.
3. Prepare the complete fingerprint with the protocol/design and pipeline/control
   commitments. Keep original frozen snapshots. Save evidence references in the
   new checkpoint before declaring completion.
4. Old control `PASS` text is not migratable execution evidence. Preserve it as
   history and require a separately authorized fresh run under a locked plan.
   The repository's former illustrative control example is now explicitly
   `PLANNED`; no historical success is represented as having actually run.
5. Outcome/observer examples are synthetic parser fixtures, not real execution
   records. Tests produce fresh pipeline receipts in temporary directories.
   They bind the host runtime before execution and do not commit platform paths
   or runtime-produced results. Content-addressed committed fixtures use LF bytes.

## Verification and limits

The ordinary Python and PowerShell framework entry points include targeted
execution tests. They cover valid count/calendar/holdout protocols, frozen and
assessed missing/conflicting protocols through the router CLI, early/late/aborted
tests, clipping, undeclared inspection, fixed audits, alpha boundaries, duplicate
fingerprint commitments, false sentinel truth, repeated random walks, altered
seeds/statistics/output bytes, cross-version results, isolated replications and
contradictory checkpoint classifications. Existing specialist, schema, outcome
separation and protocol-smoke tests remain in place.

This is **caller-enforced outside the supplied entry points**. The host must
invoke the router/validators, approve adapters, disclose all material dependencies,
collect all observations and inspections, and preserve the accepted baseline.
The subprocess is not a sandbox: a hostile candidate can access undeclared files
or external state. Hashes and local receipts detect inconsistencies, not a
coordinated fabrication of the producer, observer, files and checkpoint. They
are not signed independent attestations. The framework does not silently execute
arbitrary code merely to validate a receipt. Live-agent bypass resistance and any
stronger trusted harness remain priorities 4 and 6. Data fitness remains binding
before every empirical test; priority 7 is additional enforcement only.
