# ADR-002: Version- and integrity-aware governance of academic sources

**Status:** Accepted  
**Date:** 2026-08-30  
**Deciders:** Research owner and research-framework maintainer

## Context

The previous evidence contract recognized the source type `ACADEMIC`, but did
not distinguish a peer-reviewed journal version from an accepted manuscript,
working paper, or preprint. As a result, the framework could:

- mistakenly treat an arXiv version as peer reviewed;
- count several versions of the same work as independent confirmations;
- overlook corrections, expressions of concern, or retractions;
- confuse journal prestige with methodological quality; or
- record replication, code, or data claims without verifiable references.

Trading research also needs access to scientific primary sources. These include
original work in journals such as *The Journal of Finance* and *The Journal of
Financial Economics*, as well as current manuscripts in arXiv `q-fin`
categories. These channels have different review and version states and must not
be treated as equivalent.

## Decision

We introduce an explicit academic-source protocol.

1. Each academic source identifies a specific document version and receives
   complete `academic_metadata`.
2. All versions of the same work share a stable `work_id`. A journal version,
   accepted manuscript, working paper, and preprint are therefore one version
   family, not independent evidence.
3. Publication status is exactly one of
   `PEER_REVIEWED_VERSION_OF_RECORD`, `ACCEPTED_MANUSCRIPT`, `WORKING_PAPER`,
   `PREPRINT`, or `OTHER`. Peer review is derived from this status rather than
   represented by a redundant Boolean field.
4. `study_type` distinguishes original research, replication, systematic review,
   meta-analysis, methods paper, commentary, and other contributions. The
   academic channel alone does not make a source a primary study.
5. For arXiv, store the ID, concrete version, submission/change time, and one of
   the official categories `q-fin.CP`, `q-fin.EC`, `q-fin.GN`, `q-fin.MF`,
   `q-fin.PM`, `q-fin.PR`, `q-fin.RM`, `q-fin.ST`, or `q-fin.TR`. `q-fin` is a
   subject classification, not a review or quality seal.
6. Before evidence is used, verify integrity through the publisher, Crossmark,
   DOI metadata, or repository. A correction, expression of concern,
   retraction, or withdrawal requires a linked notice.
7. Record code and data availability as access states. Openness matters for
   reproducibility, but does not replace design or identification checks; lack
   of openness is not automatically evidence of poor research.
8. A positive, negative, or mixed replication statement needs references to
   genuinely independent work. Additional versions of the same `work_id` do
   not suffice.
9. Journal name, impact factor, and citation count are not evidence-grade
   rules. *The Journal of Finance* and *The Journal of Financial Economics* are
   targeted research channels, not a whitelist or quality guarantee.
10. A verified preprint may carry the narrow `SOURCE_FACT` that the work
    reports a result. A sole, independently unreproduced preprint must not raise
    a decision-bearing claim to `SUFFICIENT` or support activation by itself.

The machine-readable implementation uses `schemas/evidence.schema.json` version
`2.0.0`; the changed grade semantics use
`evidence_assessment.ruleset_version = 1.1.0`.

## Primary references for the protocol

- [arXiv category taxonomy](https://arxiv.org/category_taxonomy)
- [arXiv versioning help](https://info.arxiv.org/help/versions.html)
- [Crossref Crossmark](https://www.crossref.org/services/crossmark/)

These references define repository categories, permanent versions, and ways to
check for updates or integrity notices. They do not evaluate the substantive
quality of individual research papers.

## Options considered

### Option A: Keep `ACADEMIC` without substructure

Simple, but publication, version, and integrity status remain implicit. The
agent could express important differences only in free text; automated testing
and deduplication would not be reliable.

### Option B: Journal whitelist as a quality filter

Easy to understand, but methodologically wrong. Even renowned journals contain
different designs, later corrections, and unreproduced results. High-quality
working papers and preprints can also provide relevant early evidence.

### Option C: Explicit version-family and integrity model

This requires more metadata, but review status, document version, integrity,
reproducibility, and independence are kept separate and made machine-testable.
This option is chosen.

## Consequences

- Existing `ACADEMIC` objects require migration; the evidence schema therefore
  receives a major version.
- Non-academic sources remain compatible and must not carry non-null
  `academic_metadata`.
- New arXiv versions do not overwrite old snapshots. The version used remains
  permanently referenced, and a newer version creates a source delta.
- A new correction, expression of concern, retraction, or confirmed replication
  problem can trigger a material or breaking delta.
- JSON Schema can test field consistency, but cannot fully determine whether two
  `work_id` values denote the same work or whether a replication is methodologically
  independent. Those cross-object rules remain the work of validators, evals,
  and human review.

## Action items

1. [x] Supplement Evidence Schema 2.0 with academic metadata and conditional
   contracts.
2. [x] Create positive and negative schema fixtures for journal and q-fin
   sources.
3. [x] Include academic-source governance in the operations standard and case
   checklist.
4. [x] Add an eval case for correct treatment of a q-fin preprint.
5. [ ] Implement a cross-object validator for `work_id` deduplication and
   replication references.
