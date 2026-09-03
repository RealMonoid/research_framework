# ADR-013: Full research fingerprint and visible changes

## Status

Accepted

## Problem

The previous drift check compared only the research question, strategy, market,
time horizon, trigger, and target. Those six points could remain unchanged while
an agent changed a lookback, measurement definition, filter, data source,
exclusion rule, or evaluation assumption. Such changes can materially affect
the result.

## Decision

Each Research version receives a complete, canonically ordered fingerprint. It
contains all materially effective decisions and the checksums of the underlying
material artifacts. Before a material work result is accepted, a candidate
fingerprint is derived from it and compared in full with the effective
fingerprint.

If the fingerprints are equal, the work may be accepted after the other
required checks. If any difference exists, the previous fingerprint remains
effective. The system creates a visible change proposal with the exact paths
that differ. Only an explicit user decision may turn that proposal into a new
Research ID or Research version. An existing state is never overwritten
silently.

The rule applies to specialist agents and to material work performed by the
main agent.

## Consequences

- Changes to previously unprotected details become visible.
- Reordering explicitly unordered lists does not trigger a false alarm.
- The fingerprint does not assess whether a change is scientifically good; it
  makes the change visible and prevents its silent adoption.
- The main agent must derive a complete candidate fingerprint from every
  material result.
- Live language-model behaviour still requires separate testing. The planned
  LLM stress test is recorded as not yet implemented in `PLANNED_FEATURES.md`.
