# ADR-014: Bounded Workflow Review and Runtime Boundary

- **Status:** Accepted
- **Date:** 2026-09-03
- **Deciders:** Research owner and repository maintainer

## Context

The framework already has one research owner: the Research Conductor. It uses a
deterministic router, JSON contracts, specialist instructions, fingerprint
checks, and regression tests. The AI-Psychiatry plugin can provide useful
red-team and anti-loop observations, but a plugin must not become a second
research authority. OpenAI Developers was also consulted as an architecture
review aid. The repository does not contain a runnable agent service, an MCP
server, or an Agents SDK application.

## Decision

1. The Research Conductor remains the sole owner of the user's request, the
   effective research state, acceptance, and final communication.
2. Five controls are permanent on every task: scope lock, one-level bounded
   delegation, evidence-bound material conclusions, no equivalent repeat check
   without changed evidence, and evidence-backed completion. The router records
   their constants so a relaxed route fails schema validation.
3. `framework-control-reviewer` is a provider-neutral, bounded review contract.
   AI Psychiatry may supply these modes when available, but only when a named
   trigger or observable signal warrants review. The reviewer may return one
   narrow corrective action or a visible proposal; it may not change research
   state, set goals, promote claims, run a backtest, or commit to `main`.
4. The scientific-philosophy, causal-identification, condition, and other
   domain critics retain their existing conditional or mandatory routes. The
   workflow-control reviewer does not replace or duplicate them.
5. OpenAI Developers is an implementation and architecture aid, not a durable
   research role. No Agents SDK or MCP runtime migration is made now: there is
   no existing runtime to improve, and a second orchestration path would add
   state, error, and handoff failure modes without a demonstrated benefit.
   Reconsideration requires a concrete runtime need and an evaluation of the
   actual execution trajectory.

## Consequences

- The framework gains explicit, machine-checked boundaries for the most common
  orchestration failures while preserving the existing single-owner design.
- AI Psychiatry can challenge workflow truthfulness without taking over a
  scientific or capital decision.
- The repository remains provider-neutral and does not acquire an untested
  dependency or parallel state machine.
- Caller enforcement remains a known limitation. A route artifact can still be
  fabricated unless a future harness owns invocation; live-agent evaluation must
  measure that limitation rather than hide it.

## References

- [OpenAI Agents orchestration](https://developers.openai.com/api/docs/guides/agents/orchestration)
- [OpenAI guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- [`AGENTS.md`](../AGENTS.md) for the repository's authoritative policy
