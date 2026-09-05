# Interdisciplinary foundations for bounded trading research

**Version:** 1.3

**As of:** 2026-09-04

**Status:** Academic foundation for the adopted project mission; the source
ledger and disciplinary synthesis remain non-normative

**Scope:** This note supplies the interdisciplinary basis for the mission adopted
in `AGENTS.md` and ADR-016. It does not define a concrete strategy, authorize
data access or a market test, prescribe a backtest, or independently amend a
framework rule.

## Applied project mission

The project uses the modular interdisciplinary architecture developed below to
pursue three connected applied functions:

1. rigorously reconstruct and test existing trading strategies;
2. generate and develop new strategy hypotheses through bounded, recorded
   search; and
3. accumulate scoped learning from positive, negative, inconclusive, blocked,
   and not-testable results about markets, representations, mechanisms,
   conditions, measurements, methods, and failure modes.

The program-level objective is to identify or develop executable trading
strategies with a defensible positive expected net edge after realistic costs,
liquidity, slippage, capacity, execution, and risk. Scientific discipline and
the disciplinary boundaries in this note protect that applied objective; they
are not substitutes for it.

Learning is cumulative only when its provenance, scope, and evidential status
remain visible. It may change which candidates are generated or which tests are
informative, but it does not confer support on another strategy without an
appropriate test. Likewise, a valid case-level rejection or stop protects the
program and informs later search without becoming the program's end goal.

## Direct answer

Academic findings can be combined coherently for trading research by using a
**modular research architecture**, not by merging their vocabularies into one
theory. Each discipline should have one primary epistemic job, a declared input,
and a declared output. The output may constrain the next discipline, but it may
not perform the next discipline's job.

This is consistent with research on interdisciplinary integration: productive
integration connects fields around a shared phenomenon, a concrete problem, and
explicit relations between their contributions. It does not require theoretical
reduction or agreement on one vocabulary. Integrative pluralism adds that
complex, contingent systems may need several partial models, while boundary
objects can coordinate heterogeneous perspectives without erasing their
differences. Applied here, the shared objects are not slogans such as
"rationality" or "information," but traceable research artifacts. [C19]

The proposed synthesis is:

```text
decision mandate and constraints
    -> market-domain model and conditions
    -> problem representation
    -> candidate-hypothesis family
    -> resource-bounded search policy and search record
    -> claim and rival-explanation map
    -> discriminating evidence design
    -> statistical or ML estimation and generalization assessment
    -> strategy engineering and production assessment
    -> strategy-level out-of-sample or forward evidence
    -> capital decision and monitoring under risk, ambiguity, and model uncertainty
```

This is a synthesis developed for the project, not a result asserted by any one
source. Its central separation is:

- bounded and resource rationality govern **how much inquiry is affordable**;
- financial economics and market microstructure constrain **which entities,
  mechanisms, observables, and frictions are plausible in the stated market**;
- computational cognitive science distinguishes the **problem, representation,
  algorithm, and implementation**;
- AI search and planning govern **which candidates or research actions are
  considered and in what order**;
- representation change and abduction help **generate alternatives**;
- philosophy of science determines **what a result bears on and how auxiliary
  assumptions limit that inference**;
- experimental design determines **which observation would discriminate among
  live alternatives**;
- statistics and ML quantify **estimation, prediction, uncertainty, and
  generalization under a recorded search**;
- strategy engineering determines whether a validated phenomenon or other
  limited supported claim survives **data, cost, execution, capacity, portfolio,
  risk, attribution, and operational constraints as a complete strategy**;
- decision theory maps **evidence and unresolved uncertainty to action given
  explicit consequences**.

The practical anti-substitution rule is therefore:

> A useful idea is not evidence; a good explanation is not identification; a
> significant estimate is not generalization; predictive performance is not a
> mechanism; information gain is not decision value; and a decision rule does
> not make its premises true.

## Role-and-interface map

The following map is a project synthesis. The cited claim identifiers refer to
the claim-to-source ledger below.

| Discipline | Question it is entitled to answer | Required input | Output passed forward | Boundary it must not cross |
|---|---|---|---|---|
| Interdisciplinary integration | Which contributions address the same phenomenon, and through which explicit relation or shared object can they be connected? | A concrete trading-research problem, disciplinary claims, scopes, and terms | Interface map, shared boundary objects, preserved disagreements | Coordination does not imply reduction, consensus, or transfer of evidential force between fields. [C19] |
| Financial economics and market microstructure | Which institutions, participant constraints, order-flow processes, and frictions make a market representation plausible? | Named market, venue, instrument, horizon, rules, and observable events | Scoped domain ontology, mechanism candidates, observables, and boundary conditions | A mechanism or association found in one venue, instrument, or period is not automatically causal, stable, tradable, or portable. [C22, C23] |
| Bounded and procedural rationality | What search and decision procedure is feasible under finite time, computation, attention, and data? | Decision objective, environment, resource limits | Search budget, aspiration or stopping policy, procedural constraints | It does not show that a heuristic is accurate in the market merely because it is cheap or psychologically plausible. [C1, C2] |
| Resource/computational rationality and metareasoning | Which additional computation is worth performing relative to acting or stopping now? | Candidate computations, external decision consequences, time/computation costs | Priority or stopping decision for research operations | An assumed utility/cost model is not an empirically validated model of the research process or market. [C3] |
| Computational cognitive science | At what level is a claim being made: task, representation/algorithm, or implementation? | A stated research task and candidate procedure | Level-specific description and non-equivalence warnings | Success at one level does not identify the representation, algorithm, mechanism, or implementation at another. [C4] |
| AI search and planning | How can a state/action or candidate space be traversed without exhaustive enumeration? | Explicit states, actions, transitions, goals, costs, and constraints | Candidate sequence, plan, provenance, frontier, and termination condition | Search efficiency is not statistical evidence for the candidates found, and the formalism does not supply the right state space by itself. [C5] |
| Representation change and hypothesis-generation research | When can changing features, constraints, decomposition, or framing make previously inaccessible candidates reachable? | Current representation, failed search trace, alternative feature/decomposition operators | Explicitly new representation and newly reachable candidates | Human laboratory results do not establish that a trading reinterpretation is correct, that an AI shares the same process, or that post-result reframing is permissible. [C6, C20] |
| Abduction and explanatory inference | Which hypotheses could explain a surprising observation, and which explanatory contrasts matter? | Observation, background assumptions, rival explanations | Candidate explanations and contrastive consequences | Abduction generates or ranks hypotheses; it does not by itself confer truth, causal identification, or predictive validity. [C7] |
| Philosophy of science | What bundle of hypothesis, measurement, operationalization, data, and auxiliary assumptions did evidence actually confront? | Claim, auxiliaries, design, and result | Claim-scope statement, unresolved alternatives, continuation rationale | Underdetermination does not license unlimited rescue, and one anomaly does not logically identify the failed component. [C8, C9] |
| Experimental design | Which feasible observation or test best separates the live alternatives for the decision at hand? | Rival hypotheses, predicted observations, loss/utility, admissible data path | Comparison of designs, predeclared sampling/stopping rule, expected discrimination or decision value | Generic entropy reduction is not automatically useful, and an adaptive design does not license unaccounted repeated peeking. [C10-C14] |
| Statistics and ML | How well does a fixed or fully recorded procedure estimate, predict, and generalize, with what uncertainty? | Frozen target, data-generating assumptions, candidate/search record, sampling design | Estimate or predictive assessment with uncertainty, multiplicity, dependence, stability, and generalization limits | Prediction does not establish explanation or causation; testing the selected winner as if it were the only model understates search uncertainty. [C16-C18, C21, C23, C24] |
| Strategy engineering and production | Can a validated phenomenon or other limited supported claim become a complete, executable strategy under the actual data, execution, cost, liquidity, capacity, portfolio, risk, attribution, and operating environment? | Exact supported claim and evidence status, full rule set, production data path, cost/execution assumptions, capital and risk constraints | Implementable strategy specification, production-fitness assessment, unresolved engineering risks, and strategy-level test candidate | Engineering can reject or defer an implementation and can improve execution, but it cannot manufacture evidence for the phenomenon, prediction, mechanism, or net edge. |
| Decision theory | What action follows from current beliefs or probability sets, consequences, and risk/ambiguity attitude? | Action set, consequences, uncertainty representation, utility/loss, robustness criterion | Decision, sensitivity, value of further information, or justified abstention | A mathematically optimal decision is only conditional on its state space, beliefs, utilities, and model class; it does not validate them. [C14, C15] |

## Relevance filter for imported research

For this project, an academic result is relevant only if it changes at least one
declared research object: the market representation, candidate family,
measurement, evidence design, uncertainty assessment, or capital decision. The
strength of its contribution depends on how directly it travels to trading:

1. **Domain evidence** studies markets directly. It may constrain mechanisms,
   observables, frictions, stability, or selection effects, but remains limited
   to its instruments, venues, periods, and design. [C17, C18, C22-C24]
2. **Transportable method** supplies a formal procedure for search, experimental
   choice, inference, or decision. Its theorem or guarantee travels only when
   the project's assumptions match the source assumptions. [C3, C5, C11-C15,
   C21]
3. **Diagnostic analogy** from psychology, cognitive science, or philosophy can
   expose a failure mode or organize inquiry. It does not become empirical
   evidence about markets or AI agents without a separate transfer test. [C4,
   C6-C10, C20]

This three-way classification is a project synthesis. It prevents a useful
human-cognition result from being treated like market evidence, and prevents a
finance result from being generalized beyond its empirical domain.

## Integration principles

The principles in this section are explicit **project synthesis**, derived from
the source-backed findings but not presented as an academic consensus.

### 1. Integrate by typed interfaces, not shared vocabulary

Terms such as *rational*, *information*, *model*, *explanation*, and *optimal*
mean different things across the disciplines. Every handoff should therefore
name the object transferred:

| Handoff | Interface object | Minimum content |
|---|---|---|
| Decision theory -> bounded inquiry | Research mandate | Available actions, consequences protected, horizon, resource ceiling, and what abstention means |
| Representation -> search | Representation record | Objects, features, relations, constraints, excluded possibilities, and provenance of each choice |
| Abduction -> search | Candidate-family record | Candidates, common parent idea, rival explanations, generation route, and ungenerated/unknown regions |
| Search -> statistics | Search ledger | Every inspected family, model, parameterization, filter, outcome, stopping event, and rejection—not only survivors |
| Philosophy -> design | Claim-evidence map | Claim type, auxiliaries, rival accounts, observations predicted under each, and conclusions a result cannot support |
| Design -> estimation | Evidence contract | Sampling rule, target, comparison, timing, multiplicity family, stopping rule, and analysis boundary |
| Statistics/ML -> strategy engineering | Evidence report | Estimates/predictions, uncertainty, dependence, generalization scope, costs represented, and unresolved model uncertainty |
| Strategy engineering -> strategy-level test | Executable specification | Data path, order and fill model, costs, capacity, portfolio interaction, risk controls, attribution, operating controls, and version identity |
| Strategy-level test -> decision theory | Strategy evidence report | Complete-strategy results, uncertainty, dependence, implementation deviations, monitoring limits, and unresolved model or operational risk |
| Decision theory -> owner | Decision record | Action, loss/utility assumptions, robustness or regret criterion, sensitivity, and value of further research |

No interface object in this note is a proposed repository requirement. The table
is a conceptual test of whether disciplines are being combined coherently.

### 2. Keep four kinds of adequacy separate

The same candidate can be assessed for four different properties:

1. **Procedural adequacy:** Was it generated and evaluated within realistic
   resource limits and a declared search process? [C1-C3]
2. **Epistemic adequacy:** Did the evidence genuinely probe the stated claim and
   relevant alternatives? [C7-C10]
3. **Statistical/predictive adequacy:** Does the result survive the appropriate
   uncertainty, dependence, selection, and generalization checks? [C16-C18]
4. **Decision adequacy:** Is the resulting action defensible for the stated
   consequences and unresolved uncertainty? [C14, C15]

A candidate may pass one and fail another. The categories should not be averaged
into a single informal confidence score.

### 3. Separate generation from warrant

Abduction and representation change are appropriate upstream tools for creating
candidate explanations. Their output must be marked *generated*, not
*supported*. Statistical or experimental results may later warrant a limited
claim, but only under the design and auxiliary assumptions actually used.
[C6-C10]

### 4. Price the search, but expose the search

Resource rationality and metareasoning support prioritizing high-value research
operations. They do not support erasing low-priority, failed, or abandoned
candidates. The computational budget and the inferential multiplicity record
solve different problems: the first controls cost; the second preserves the
reference set needed to judge selected results. [C2, C3, C17, C18]

### 5. Select evidence for discrimination and decision relevance

An informative next observation should be judged against named rival
explanations and the downstream decision. Bayesian expected information gain,
Blackwell informativeness, and decision value are related but not identical:
they rank experiments under different objects and assumptions. A design may
reduce uncertainty without changing any available action; conversely, a modest
amount of information near a decision threshold may be valuable. [C11, C12,
C14]

### 6. Preserve the level of every claim

Marr's levels offer a useful discipline even though his subject was vision. A
claim that a research objective is appropriate, a claim that an algorithm
searches well, and a claim that one implementation executed correctly are
different claims. Likewise, an observed prediction, an explanatory model, and
a market mechanism should not be collapsed. This use in trading research is an
analogy and extension, not a direct empirical finding about markets. [C4]

### 7. Treat robustness as conditional, not magical

Multiple priors, minimax regret, and robust control offer explicit responses to
ambiguity or misspecification. They are alternative normative commitments, not
automatic upgrades to ordinary expected utility. The uncertainty set,
misspecification neighborhood, loss, and robustness penalty must remain visible.
[C15]

### 8. Make disagreement part of the architecture

Where fields disagree, the system should preserve the disagreement instead of
blending it away:

- ecological and fast-and-frugal work stresses environment-matched simple
  heuristics; resource-rational analysis models constrained optimization; Simon's
  procedural view asks how decisions are actually produced. These are not
  interchangeable accounts. [C1, C2]
- Harman and Lipton defend explanatory inference; van Fraassen disputes the
  move from explanatory attractiveness to truth. Explanatory ranking should
  therefore remain a candidate-selection aid, followed by independent probing.
  [C7]
- Bayesian information measures and Mayo's severe-testing account embody
  different views of evidential warrant. Both can inform a workflow, but one
  numerical score must not be described as resolving the foundational dispute.
  [C10, C12]
- predictive/algorithmic modeling and explanatory data modeling pursue different
  goals. Breiman's distinction is a warning against judging one entirely by the
  other's criterion, not a proof that explanation is dispensable. [C16]

### 9. Locate claims by explanatory level and target

When an interdisciplinary claim could be misread, locate it on two independent
coordinates:

1. **Explanatory level:** the objective or problem being solved; the
   representation and algorithm used; or the concrete implementation that ran.
2. **Target:** the market and its participants; the research process and its
   agents; or the strategy, portfolio, and production system.

For example, bounded rationality may describe a participant, prescribe a
research-budget policy, or constrain a live decision procedure. Those are not
the same claim. The coordinates expose that difference; they are not themselves
evidence and do not imply that Marr's original framework is a market theory.
[C1-C4]

### 10. Give each selected bottleneck a lead owner, not a monopoly on causation

For each material bottleneck selected for action, name one discipline or
production lane as the primary owner of its next question. Other fields and
competing bottlenecks remain explicit constraints, critics, or dependencies.
This is a coordination rule: it does not establish that the system has one true
bottleneck, that the named owner explains the failure, or that coupled
bottlenecks may be ignored. If ownership is genuinely undecidable, preserve the
competing diagnoses and choose a discriminating check rather than assigning
certainty by fiat.

### 11. Treat scarce resources as a vector subject to hard admissibility rules

Independent data history, compute, elapsed time, attention, capital, liquidity,
and risk-bearing capacity are not safely interchangeable by default. Expected
decision value or value of computation may rank otherwise admissible research
actions, but no scalar score may purchase permission to waive provenance,
leakage, identification, validation, risk, or change-control requirements. A
resource-efficient invalid inference remains invalid. [C1-C3, C14, C15]

### 12. Close the loop through production reality

Methodological cleanliness protects the search for an edge; it is not itself an
edge. A research result reaches the applied mission only through data quality,
cost and execution modeling, liquidity and capacity, portfolio construction,
risk and ruin controls, PnL attribution, operational reliability, and a new test
of the complete strategy. Conversely, a production improvement can improve net
implementation without retrospectively validating the upstream phenomenon or
mechanism.

## Source-backed findings

The statements below summarize what the cited works establish or argue in their
own domains. Trading consequences are developed separately in the ledger.

1. **Finite agents require procedural accounts of rationality.** Simon replaces
   omniscient global optimization with models of simplified choice, satisficing,
   and decision procedures fitted to environmental structure. [C1]

2. **A heuristic's quality is environment-relative.** Fast-and-frugal models can
   perform well under specified cue structures, while resource-rational analysis
   asks whether behavior uses limited computational resources effectively. The
   latter is a modeling framework and must not be silently turned into the
   empirical assertion that people—or agents—are resource-rational. [C2]

3. **Computation itself can be treated as a costly action.** Computational
   rationality and metareasoning evaluate additional computation by its expected
   effect on external decisions, net of time and computation costs. [C3]

4. **Problem, representation/algorithm, and implementation are distinct levels
   of explanation.** Marr introduced this separation for vision; it prevents a
   successful implementation from answering what is computed or why, and
   prevents an abstract objective from specifying a unique algorithm. [C4]

5. **Search requires a represented space and selective operators.** AI search
   and planning formalize states, actions, transitions, objectives, and
   heuristics for navigating large spaces. They do not derive the correct
   representation from evidence automatically. [C5]

6. **Changing a representation can change problem solvability.** Controlled
   insight studies show that cue salience, generators, constraints, constraint
   relaxation, and chunk decomposition can make solutions accessible in the
   studied laboratory tasks. [C6]

7. **Abduction/IBE is a candidate-forming or candidate-ranking mode, not a
   deductive guarantee.** Peirce places abduction within an inquiry cycle;
   Harman and Lipton develop inference to the best explanation, while van
   Fraassen challenges its truth-conduciveness. [C7]

8. **Evidence generally confronts an interconnected body of assumptions.**
   Quine's holism undermines a simple one-statement/one-observation picture of
   confirmation. [C8]

9. **A research programme may rationally survive anomalies only under
   disciplined conditions.** Lakatos distinguishes progressive change, which
   produces additional empirical content, from degenerating accommodation. This
   is methodological appraisal, not a mechanical test. [C9]

10. **Scientific learning is iterative, and evidential strength depends on the
    capacity of a test to reveal error.** Box describes iterative confrontation
    between model and practice; Mayo argues that warrant requires a severe probe
    capable of detecting flaws relevant to the claim. [C10]

11. **Experiments can be compared by their usefulness across decision
    problems.** Blackwell formalizes when one experiment is at least as
    informative as another through attainable risks/garbling relations. [C11]

12. **Expected information gain is objective-relative and model-relative.**
    Lindley measures expected Bayesian information from an experiment; MacKay
    derives different active-selection criteria for different learning targets
    and explicitly notes dependence on a correct hypothesis space. [C12]

13. **Sequential observation requires a sequential design.** Wald's framework
    specifies continue/accept/reject rules and their operating characteristics;
    it does not validate arbitrary repeated inspection under a fixed-sample
    analysis. [C13]

14. **Information has decision value only through consequences.** Howard's value
    of information combines probabilities with economic consequences, so
    Shannon-style surprise alone is insufficient for decision importance. [C14]

15. **There is no single uncontested rule for action under ambiguity.** Multiple
    priors/maxmin utility, robust control, and minimax-regret or related partial-
    knowledge criteria formalize different attitudes and assumptions. [C15]

16. **Prediction and explanatory modeling are distinct research cultures.**
    Breiman argues for evaluating algorithmic models by predictive performance
    and criticizes overreliance on assumed stochastic data models. [C16]

17. **Selection over many models changes the inferential reference set.** White
    develops a test for the best model encountered in a specification search;
    Sullivan, Timmermann, and White apply search-adjusted inference to a large
    universe of technical trading rules. [C17]

18. **Finance has an accumulated multiple-testing problem.** Harvey, Liu, and
    Zhu derive higher testing hurdles for a literature containing many attempted
    return predictors. Their framework addresses a defined testing history; it
    cannot recover unrecorded searches perfectly. [C18]

19. **Interdisciplinary integration can preserve plurality.** Interfield and
    cross-disciplinary accounts treat integration as constructing explicit
    relations among contributions aimed at a shared phenomenon or problem.
    Integrative pluralism rejects the assumption that one complete model must
    replace multiple partial models, and boundary-object research shows how
    heterogeneous groups can coordinate through shared, traceable objects.
    [C19]

20. **Bias can enter before hypothesis evaluation.** In controlled human
    inference tasks, Dasgupta, Schulz, and Gershman find that judgments can be
    close to Bayesian when alternatives are supplied, yet framing-dependent
    biases arise when participants must generate a small subset from a large
    hypothesis space. The result concerns human cognition, but it identifies a
    general workflow risk that evaluation-only safeguards cannot detect. [C20]

21. **Adaptive analysis changes generalization risk.** Work on adaptive data
    analysis shows that choosing later analyses after seeing earlier results can
    overfit even a holdout set. Specialized mechanisms can control particular
    adaptive interactions under formal assumptions; their existence does not
    make undocumented reuse safe. [C21]

22. **Market-domain knowledge constrains representations rather than validating
    strategies.** Microstructure studies relate short-horizon price changes to
    order-flow imbalance, depth, inventory, and liquidity in specified markets.
    Such findings make some variables and mechanisms plausible while leaving
    portability, causal interpretation, execution, and net profitability open.
    [C22]

23. **Trading prediction is exposed to instability and adaptation.** Local
    forecast rankings can vary over time, and published cross-sectional return
    predictors have shown lower returns outside their original samples and
    after publication. Evolutionary market accounts make adaptation conceptually
    plausible, but do not identify a regime or justify a filter by themselves.
    [C23]

24. **Financial ML is a predictive layer with an enlarged search space.** In a
    major U.S.-equity study, flexible nonlinear methods improved out-of-sample
    risk-premium prediction relative to the studied benchmarks. The result is
    scoped to that design and illustrates both ML's predictive value and its
    dependence on regularization, model selection, and out-of-sample evaluation;
    it does not independently identify a mechanism or universal trading edge.
    [C24]

## Anti-eclecticism rules

These are analytical rules for reading and combining the literature in this
sidecar. They are not proposed normative changes to the repository.

1. **One selected question, one primary disciplinary owner.** Other fields may
   constrain or criticize it, and coupled or uncertain bottlenecks remain
   visible. Primary ownership coordinates the next step; it does not identify a
   sole cause or give one field authority over the whole research problem.
2. **No traveling conclusions.** A conclusion retains the scope, population,
   task, assumptions, and level at which its source established it.
3. **No metaphor-to-evidence conversion.** Terms borrowed from cognition or AI
   may organize trading research; they are not market evidence.
4. **No generative-to-evaluative conversion.** Abduction, analogy, insight, and
   representation change generate candidates; independent design and evidence
   evaluate them.
5. **No efficiency-to-validity conversion.** A cheap heuristic or efficient
   search can conserve resources without making the selected result reliable.
6. **No prediction-to-mechanism conversion.** Out-of-sample prediction can
   support a predictive claim; it does not identify why the relationship holds.
7. **No explanation-to-identification conversion.** Explanatory attractiveness
   must not substitute for a design that rules out relevant alternatives.
8. **No information-to-value conversion.** Uncertainty reduction must be linked
   to available actions and consequences before it is called valuable.
9. **No robustness-by-label.** "Robust," "Bayesian," "AI," "causal," or
   "resource-rational" names do not carry guarantees across assumptions.
10. **No hidden search compression.** The candidate finally reported must remain
    linked to the family and sequence from which it was selected.
11. **No retrospective representation repair.** A new feature set, regime,
    mechanism, or decomposition created after an adverse result is a new
    candidate representation, not a reinterpretation of the old result.
12. **No forced foundational consensus.** Where Bayesian, error-statistical,
    explanationist, ecological, or ambiguity-sensitive approaches disagree,
    record which commitment is being used and test sensitivity where practical.
13. **No scalar-resource override.** A favorable utility, information-value, or
    compute-efficiency score cannot waive an evidential, risk, provenance, or
    change-control requirement.
14. **No universal trading shortcut.** A cost multiple, trade-count threshold,
    sample-size formula, ML cutoff, capacity assumption, or preferred research
    order is not portable unless its assumptions and target setting are stated
    and justified.

## Trading-research implications

The implications below are the author's synthesis from the source-backed
findings. None is evidence for a concrete trading edge.

### Hypothesis-space construction

- A trading hypothesis should record its representation before candidate search:
  entities, time scale, observable variables, relations, market constraints,
  target, and excluded interpretations.
- Alternative representations should be generated deliberately—for example,
  predictive pattern, institutional mechanism, measurement artifact, or common-
  input construction—but retained as rivals rather than blended into one story.
- Hypothesis provenance should distinguish source-derived, theory-derived,
  analogy-derived, and data-prompted candidates. This makes abduction useful
  without allowing it to masquerade as confirmation.
- A candidate family should include at least three distinct types when relevant:
  a market-mechanism account, a purely predictive alternative, and a
  measurement or data-process rival. This is a project design implication, not
  a fixed minimum mandated by the cited studies.

### Search and planning

- The research process can be represented as a partially observed sequence of
  states and research actions, but the state representation is itself fallible.
- Metareasoning can prioritize the next literature check, data-quality check,
  diagnostic, or test by expected effect on the eventual decision and by cost.
- Search-budget stopping and evidential stopping are separate. "Not worth more
  computation" means the inquiry should stop for resource reasons; it does not
  mean the hypothesis is false, supported, or fully tested.
- The search record must include discarded candidates and changed
  representations because data-snooping adjustments require a defensible
  reference family.

### Evidence design

- The next test should target a contrast: which observation differs between the
  leading hypothesis and at least one serious rival?
- Candidate designs should be ranked separately by feasibility, discriminatory
  power, expected information gain, and expected decision value. These rankings
  may disagree.
- Any adaptive or sequential research path requires a predeclared rule that
  accounts for continuation and stopping; ordinary fixed-sample thresholds do
  not automatically survive repeated looks.
- An adverse result applies first to the tested bundle. A continuation becomes
  scientifically stronger only when it exposes a new consequence to risk rather
  than merely absorbing the anomaly in a flexible story.

### Statistics and machine learning

- Statistics/ML enters after the target, candidate family, data role, and search
  history are defined. It estimates or predicts; it does not choose the meaning
  of the target or authorize a causal interpretation.
- Flexible ML expands the effective hypothesis space through features,
  architectures, hyperparameters, samples, losses, and stopping choices. Those
  choices belong in the search ledger even if an automated tool made them.
- A predictive model may be decision-useful without a validated mechanism. The
  permitted claim should then remain predictive, and its stability, costs,
  timing, and dependence on the data environment remain separate questions.
- Repeated reuse of validation data is part of the effective search, even when
  the later candidate was generated by an AI agent rather than a human analyst.
  Fresh temporal evidence or an explicitly valid adaptive-analysis design is
  needed to restore a defensible confirmation boundary.
- Global average performance should not hide local reversals. Stability over
  market time is a separate target from average out-of-sample performance.

### Trading-domain constraints

- Financial economics and microstructure should enter before feature search by
  specifying institutions, participant constraints, event timing, liquidity,
  and feasible execution. They constrain the representation; they do not get to
  certify the resulting strategy.
- Market findings should retain their instrument, venue, horizon, sample period,
  and institutional conditions. A result about NYSE equities at short horizons
  is evidence for that setting, not a universal microstructure law.
- Market adaptation and publication effects make a chronological evidence trail
  material. A historically real relationship may weaken after discovery without
  implying that the original observation was fabricated or that a new regime
  label explains the change.

### Strategy engineering and production reality

- Early cost and data-feasibility screens should protect scarce validation
  evidence, but they must use a strategy-specific uncertainty range rather than
  a universal movement-to-cost multiple.
- A complete production assessment covers the versioned data path and quality,
  decision-time availability, execution and microstructure, realistic costs,
  liquidity and capacity, portfolio interaction, risk and ruin exposure, PnL
  attribution, monitoring, and operating failure modes.
- These layers may invalidate, defer, or reshape an implementation. Any material
  reshaping creates a new strategy candidate or research version; it does not
  rescue the evidence status of the prior bundle.
- The operational profile must be declared. Discretionary retail day trading,
  systematic intraday research, swing trading, medium-frequency statistical
  work, macro, volatility, and high-frequency systems have different evidence
  and engineering constraints; none is the unstated project default.
- A supported phenomenon still requires the complete engineered strategy to be
  tested on unseen data or in a controlled forward process. Mechanistic
  plausibility cannot replace missing independent predictive evidence, including
  when the effective sample is small.

### Decision and capital relevance

- Evidence should reach a capital decision only through an explicit action and
  consequence model. The relevant question is not only "How uncertain are we?"
  but "Could resolving this uncertainty change the allowed action enough to
  justify the research cost?"
- When one defensible probability model is unavailable, ambiguity should remain
  explicit through bounds, multiple models, regret, or sensitivity analysis.
  Choosing one method expresses a normative attitude toward uncertainty; it does
  not eliminate uncertainty.
- Abstention, further research, and rejection are distinct decisions. A bounded
  process may rationally stop with unresolved epistemic uncertainty when further
  information has insufficient expected decision value.

## Fit with the current framework

The literature synthesis largely organizes protections already present in the
repository rather than implying a turn toward a new all-purpose ML layer:

| Existing project protection | Interdisciplinary function |
|---|---|
| [Mechanism-first hypothesis generation](../decisions/ADR-006-mechanism-first-hypothesis-generator.md) | Connects financial-domain knowledge, abduction, representation operators, and bounded search while keeping generation separate from testing. |
| [Claim axes and variable-selection provenance](../decisions/ADR-005-causal-axes-and-variable-selection.md) | Prevents predictive, causal, mechanism, and trading-status claims from inheriting one another's evidential support. |
| [Scientific-philosophy continuation review](../decisions/ADR-009-scientific-philosophy-continuation-review.md) | Applies underdetermination and progressive-versus-degenerating continuation without rewriting an adverse result. |
| [Outcome evidence contract](../schemas/outcome_evidence_contract.schema.json) | Serves as a boundary object between claim definition, experimental design, statistical analysis, and the decision consequence. |
| [Pipeline integrity assessment](../schemas/pipeline_integrity_assessment.schema.json) | Separates evidence that a pipeline detects known and null structures from evidence for a market hypothesis. |
| [Complete research fingerprint](../schemas/research_fingerprint.schema.json) | Preserves the identity of the shared research object across disciplines, agents, revisions, and decisions. |

This mapping is interpretive and non-normative. It does not establish that the
current controls work reliably in live agent behavior; that requires separate
behavioral and empirical evaluation.

## Limitations and unresolved disagreements

1. The bounded-rationality and insight literature largely studies human agents
   and controlled tasks. Its direct empirical claims do not transfer to AI-led
   trading research; the transfer here concerns workflow design and requires
   later validation.
2. Formal AI planning assumes specified states, actions, transition models, and
   objectives. Open-ended market research does not arrive with those objects
   already given. Representation choice remains an upstream judgment.
3. Peircean abduction, Harman/Lipton-style inference to the best explanation,
   and later computational uses of "abduction" are related but not identical.
   This memo uses *abduction* broadly only at the candidate-generation interface.
4. Explanationists and critics such as van Fraassen disagree about whether
   explanatory virtues are truth-conducive. The memo does not resolve that
   dispute.
5. Quinean holism and Lakatosian research programmes explain why a failed test
   need not isolate one guilty assumption, but neither supplies an algorithm for
   deciding which auxiliary to revise.
6. Blackwell comparison, Bayesian expected information gain, severe testing,
   and decision value answer different design questions. They need not rank the
   same test highest.
7. Classical experimental-design results often presuppose controlled sampling
   or known model classes. Trading research is usually observational,
   path-dependent, dependent across time/assets, and exposed to changing market
   institutions.
8. Sequential methods protect error properties only when their sampling and
   stopping rules are actually followed. They do not cleanse an undocumented
   history of peeking.
9. Decision rules under ambiguity are normatively plural. Maxmin, robust
   control, expected utility, and minimax regret can recommend different actions
   from the same evidence.
10. Data-snooping and multiple-testing methods require a sufficiently complete
    candidate universe and defensible dependence model. Hidden human or machine
    searches remain a residual risk.
11. The cited trading papers establish the importance of multiplicity in their
    studied universes; they do not prove that every technical rule, factor,
    research process, or ML model is invalid.
12. No cited source tests the integrated architecture proposed here. The memo
    therefore supports a coherent division of epistemic labor, not a claim that
    the architecture improves trading returns or agent reliability.
13. Interdisciplinary-integration and boundary-object studies analyze scientific
    collaboration and knowledge organization. Their use for an AI-led private
    trading workflow is an architectural analogy, not a direct effectiveness
    result.
14. The microstructure, forecast-instability, publication-effect, and financial-
    ML studies use different markets, horizons, targets, and sampling designs.
    They jointly motivate separate domain, stability, search, and prediction
    interfaces; they do not form one cumulative test of a single trading theory.
15. No source in this memo establishes a universal cost multiple, minimum trade
    count, sample-size shortcut, ML sample cutoff, or claim that capacity is
    immaterial. Such quantities require a design-specific dependence model,
    uncertainty target, market, horizon, execution model, and loss function.
16. Low effective sample size does not transfer the burden of proof from
    predictive evidence to a plausible mechanism. It may instead make the
    predictive or executable-edge claim currently not testable or blocked.
17. The relative importance of disciplinary and production lanes varies by
    market, horizon, implementation style, and available evidence. This memo
    therefore adopts no universal ranking of fields and no retail, discretionary,
    intraday, swing, institutional, or high-frequency default.

## Claim-to-source ledger

Each row distinguishes the source-backed finding from its project-specific
translation. "Does not justify" records the principal inference that must not be
smuggled across the disciplinary boundary.

| Claim | Primary academic sources | What the source actually establishes or argues | Scope | Precise contribution to trading research | What it does **not** justify |
|---|---|---|---|---|---|
| **C1 — Procedural bounded rationality** | Simon, ["A Behavioral Model of Rational Choice" (1955)](https://doi.org/10.2307/1884852); ["Rational Choice and the Structure of the Environment" (1956)](https://doi.org/10.1037/h0042769); ["From Substantive to Procedural Rationality" (1976)](https://doi.org/10.1017/CBO9780511572203.006) | Models rational choice under cognitive/informational limits, links simple procedures to environmental structure, and distinguishes rational outcomes from rational processes. | Economic and psychological theories of individual/organizational choice; not trading-system validation. | Makes resource limits, stopping, and procedure-environment fit first-class research objects. | That satisficing is always optimal; that any simple trading rule is ecologically valid; or that boundedness excuses unrecorded search. |
| **C2 — Heuristics and resource rationality** | Gigerenzer & Goldstein, ["Reasoning the Fast and Frugal Way" (1996)](https://doi.org/10.1037/0033-295X.103.4.650); Lieder & Griffiths, ["Resource-Rational Analysis" (2020)](https://doi.org/10.1017/S0140525X1900061X); Rahnev, ["Resource-Rational Analysis versus Resource-Rational Humans" (2020)](https://doi.org/10.1017/S0140525X19001699) | Supplies explicit fast-and-frugal algorithms and a framework combining rational objectives with computational constraints; commentary warns against converting the method into a descriptive claim about humans. | Cognitive inference tasks and a contested modeling programme. | Supports comparing research heuristics by cost, accuracy, and environment, while preserving the distinction between a normative model and observed agent behavior. | That a heuristic transfers to markets, that an AI is resource-rational, or that constrained optimization is the only account of bounded rationality. |
| **C3 — Computational rationality and metareasoning** | Gershman, Horvitz & Tenenbaum, ["Computational Rationality" (2015)](https://doi.org/10.1126/science.aac6076); Russell & Wefald, ["Principles of Metareasoning" (1991)](https://doi.org/10.1016/0004-3702(91)90015-C) | Frames rationality under computation costs and derives the value of computations from their expected effect on external action. | General AI/cognitive models with specified utilities, beliefs, and computational actions. | Provides a principled language for choosing whether another research operation is worth its delay and cost. | That the utility model is correct, that myopic value-of-computation is globally optimal in an open-ended inquiry, or that stopping implies evidential closure. |
| **C4 — Levels of analysis** | Marr, [*Vision* (1982; MIT Press edition 2010)](https://doi.org/10.7551/mitpress/9780262514620.001.0001) | Distinguishes computational task, representation/algorithm, and physical implementation in explaining vision. | A theory of explanation in vision and information-processing systems. | Prevents trading-research objectives, algorithms, data representations, and software executions from being treated as equivalent evidence. | A market ontology, a trading algorithm, or proof that exactly three levels exhaust research explanation. |
| **C5 — Search and planning** | Newell & Simon, ["Computer Science as Empirical Inquiry: Symbols and Search" (1976)](https://doi.org/10.1145/360018.360022); LaValle, [*Planning Algorithms* (2006)](https://doi.org/10.1017/CBO9780511546877) | Characterizes intelligent problem solving through representations and heuristic search; systematizes planning over state/action spaces, including uncertainty and decision-theoretic variants. | Formal and computational problem-solving domains with representable spaces. | Supports explicit candidate spaces, operators, goals, costs, frontiers, and search provenance. | That a formal search space contains the relevant market hypotheses, or that an efficient plan yields a true or profitable hypothesis. |
| **C6 — Representation change** | Kaplan & Simon, ["In Search of Insight" (1990)](https://doi.org/10.1016/0010-0285%2890%2990008-R); Knoblich et al., ["Constraint Relaxation and Chunk Decomposition in Insight Problem Solving" (1999)](https://doi.org/10.1037/0278-7393.25.6.1534) | Experiments and computational analyses link success on particular insight problems to representations, generators, cue salience, relaxed constraints, and decomposed chunks. | Specific laboratory insight tasks and human participants. | Motivates explicit representation alternatives and records of which constraints or decompositions produced a candidate. | That reframing a failed trading idea rescues it, that human insight mechanisms describe an AI, or that a newly reachable candidate is supported. |
| **C7 — Abduction and explanatory inference** | Peirce, [*The Essential Peirce*, vol. 2, including "Pragmatism as the Logic of Abduction" (1903/1998)](https://iupress.org/9780253211903/the-essential-peirce-volume-2/); Harman, ["The Inference to the Best Explanation" (1965)](https://doi.org/10.2307/2183532); Lipton, [*Inference to the Best Explanation*, 2nd ed. (2004)](https://www.routledge.com/Inference-to-the-Best-Explanation/Lipton/p/book/9780415242035); van Fraassen, [*Laws and Symmetry* (1989)](https://doi.org/10.1093/0198248601.001.0001) | Peirce treats abduction as part of inquiry; Harman and Lipton develop explanatory inference; van Fraassen criticizes the inference from explanatory merit to truth. | Logic and philosophy of scientific/non-deductive inference, with substantive disagreement. | Supports a disciplined generator/ranker of competing market explanations and contrastive predictions. | Truth, causal identification, probability calibration, or predictive success from explanatory attractiveness alone. |
| **C8 — Confirmation holism** | Quine, ["Two Dogmas of Empiricism" (1951)](https://doi.org/10.2307/2181906) | Argues against reductionism in which individual statements possess isolated empirical confirmation conditions, emphasizing a web of belief facing experience. | General epistemology; not a statistical or operational protocol. | Reminds trading research that results confront a bundle of target claim, data, measurement, implementation, and auxiliaries. | Unlimited freedom to protect a favored hypothesis or a method for identifying which component failed. |
| **C9 — Research programmes** | Lakatos, ["Falsification and the Methodology of Scientific Research Programmes" (1978 edition)](https://doi.org/10.1017/CBO9780511621123.003) | Develops methodological appraisal of programmes and distinguishes progressive theoretical/empirical change from degenerating accommodation. | Historical and normative philosophy of science; qualitative appraisal. | Supplies language for distinguishing risky continuation from retrospective strategy rescue. | A mechanical pass/fail rule, permission to revise after seeing trading results, or evidence for an unchanged hypothesis. |
| **C10 — Iteration and severe probing** | Box, ["Science and Statistics" (1976)](https://doi.org/10.1080/01621459.1976.10480949); Mayo, [*Statistical Inference as Severe Testing* (2018)](https://doi.org/10.1017/9781107286184) | Box presents model-practice iteration; Mayo argues that a claim is warranted only when a test had a strong capacity to reveal relevant errors. | Statistical methodology and philosophy; Mayo's error-statistical position is contested by other foundations. | Supports designing diagnostics around concrete ways a trading inference could be wrong and resisting result-only declarations. | That one generic robustness check is severe for every error, or that severity resolves Bayesian/frequentist disagreements. |
| **C11 — Comparison of experiments** | Blackwell, ["Equivalent Comparisons of Experiments" (1953)](https://doi.org/10.1214/aoms/1177729032) | Formalizes an ordering in which one experiment can attain every risk available from another, connected to stochastic garbling/sufficiency. | Statistical decision problems under specified state, experiment, action, and loss structures. | Provides a benchmark for asking whether one research design contains decision-relevant information unavailable from another. | A total ordering of real trading studies, usefulness without a loss function, or correctness of the assumed experiment family. |
| **C12 — Information-directed design** | Lindley, ["On a Measure of the Information Provided by an Experiment" (1956)](https://doi.org/10.1214/aoms/1177728069); MacKay, ["Information-Based Objective Functions for Active Data Selection" (1992)](https://doi.org/10.1162/neco.1992.4.4.590) | Defines expected Bayesian information and derives active-selection objectives that differ with the learning target; MacKay flags the assumed hypothesis space as a central weakness. | Bayesian parametric/model-based experiment and active-data-selection settings. | Supports selecting tests by their expected ability to distinguish named candidates, with the target and model dependence explicit. | That maximum entropy reduction maximizes trading value, that the hypothesis space is complete, or that adaptive selection leaves inference unchanged. |
| **C13 — Sequential testing** | Wald, ["Sequential Tests of Statistical Hypotheses" (1945)](https://doi.org/10.1214/aoms/1177731118) | Constructs sequential accept/reject/continue procedures with analyzable error and sample-size properties. | Formal sequential hypothesis testing under specified probabilistic assumptions. | Shows that repeated observation and stopping must be part of the design rather than informal researcher discretion. | Applying fixed-sample thresholds after arbitrary peeking, or validity when dependence/model assumptions fail. |
| **C14 — Value of information** | Howard, ["Information Value Theory" (1966)](https://doi.org/10.1109/TSSC.1966.300074) | Connects the value of resolving uncertainty to both probability and the economic consequences of the resulting decision. | Bayesian decision analysis with specified actions, beliefs, and utilities. | Distinguishes interesting market information from information likely to change a consequential research/capital choice. | That utility and probabilities are known, that information is costless, or that decision value supplies empirical warrant. |
| **C15 — Ambiguity and model uncertainty** | Gilboa & Schmeidler, ["Maxmin Expected Utility with Non-Unique Prior" (1989)](https://doi.org/10.1016/0304-4068%2889%2990018-9); Hansen & Sargent, ["Robust Control and Model Uncertainty" (2001)](https://doi.org/10.1257/aer.91.2.60); Manski, ["Identification Problems and Decisions under Ambiguity" (2000)](https://doi.org/10.1016/S0304-4076%2899%2900045-7) | Gives axiomatic multiple-prior maxmin preferences, robust-control responses to misspecification, and decision analysis under partial identification and ambiguity. | Formal normative decision problems; Manski's application concerns treatment choice, not trading. | Provides distinct, auditable options when one credible probability model is unavailable. | That the most conservative rule is uniquely rational, that an uncertainty set is empirically correct, or that robustness guarantees profitability. |
| **C16 — Prediction versus explanation** | Breiman, ["Statistical Modeling: The Two Cultures" (2001)](https://doi.org/10.1214/ss/1009213726) | Contrasts stochastic data-modeling with algorithmic predictive modeling and argues for stronger attention to out-of-sample prediction. | A methodological argument in statistics, followed by published commentary and disagreement. | Clarifies when an ML result supports a predictive objective rather than a structural explanation. | That prediction makes data provenance, causal identification, uncertainty, or domain interpretation unnecessary. |
| **C17 — Data snooping and trading-rule search** | White, ["A Reality Check for Data Snooping" (2000)](https://doi.org/10.1111/1468-0262.00152); Sullivan, Timmermann & White, ["Data-Snooping, Technical Trading Rule Performance, and the Bootstrap" (1999)](https://doi.org/10.1111/0022-1082.00163) | White tests whether the best model encountered in a specified search has predictive superiority; Sullivan et al. apply the method to an expanded universe of technical rules and long-run DJIA data. | Defined model/rule universes and bootstrap/dependence assumptions in the studied samples. | Makes the complete inspected family and selection procedure part of the evidence for a reported trading candidate. | Correction for unrecorded candidates, universal rejection/acceptance of technical analysis, causal interpretation, or future profitability. |
| **C18 — Multiple testing in empirical finance** | Harvey, Liu & Zhu, ["... and the Cross-Section of Expected Returns" (2016)](https://doi.org/10.1093/rfs/hhv059) | Constructs a multiple-testing framework and historical significance hurdles for a large literature of proposed return factors. | Cross-sectional return-predictor literature and its estimated testing history/dependence. | Shows why AI-expanded features, outcomes, transformations, and model families must remain visible in the effective hypothesis count. | A universal t-statistic cutoff, exact reconstruction of hidden industry research, or proof that a particular candidate has no value. |
| **C19 — Interdisciplinary integration without reduction** | Darden & Maull, ["Interfield Theories" (1977)](https://doi.org/10.1086/288723); O'Rourke, Crowley & Gonnerman, ["On the Nature of Cross-Disciplinary Integration" (2016)](https://doi.org/10.1016/j.shpsc.2015.10.003); Mitchell, ["Integrative Pluralism" (2002)](https://doi.org/10.1023/A:1012990030867); Star & Griesemer, ["Institutional Ecology, 'Translations' and Boundary Objects" (1989)](https://doi.org/10.1177/030631289019003001) | Describes bridge relations between fields, context-specific combination processes, plural partial accounts of complex systems, and shared objects that coordinate heterogeneous viewpoints. | Philosophy of science, biology-focused pluralism, and a historical study of scientific cooperation; not a tested trading architecture. | Supports explicit interfaces, complementary disciplinary roles, shared artifacts, and preserved disagreement rather than vocabulary blending. | That the disciplines reduce to one theory, that every perspective deserves equal weight, or that boundary objects alone validate research. |
| **C20 — Hypothesis-generation bottleneck** | Dasgupta, Schulz & Gershman, ["Where Do Hypotheses Come From?" (2017)](https://doi.org/10.1016/j.cogpsych.2017.05.001) | In four human experiments and a stochastic-sampling model, supplied candidate sets supported near-Bayesian judgments while self-generation from large spaces produced systematic, framing-sensitive effects. | Human probabilistic-inference tasks with fixed data; not AI-agent or market behavior. | Motivates auditing which trading hypotheses entered the candidate set, their framing and order, not only how selected hypotheses were scored. | That an AI samples like a human, that stochastic generation is uniquely correct, or that more candidates necessarily improve trading research. |
| **C21 — Adaptive data analysis** | Dwork et al., ["The Reusable Holdout" (2015)](https://doi.org/10.1126/science.aaa9375); Russo & Zou, ["Controlling Bias in Adaptive Data Analysis Using Information Theory" (2016)](https://proceedings.mlr.press/v51/russo16.html) | Shows that adaptively chosen analyses can overfit reused data and develops formal controls or bias bounds for specified adaptive interactions. | Formal statistical/learning settings under stated sampling, privacy, information, and query assumptions. | Makes human-plus-AI iteration, validation reuse, and information leaked by prior results part of the generalization problem. | That ordinary repeated holdout access is safe, that the published mechanisms fit time-dependent market data automatically, or that adaptivity correction proves an edge. |
| **C22 — Market microstructure as domain constraint** | Cont, Kukanov & Stoikov, ["The Price Impact of Order Book Events" (2014)](https://doi.org/10.1093/jjfinec/nbt003); Hendershott & Menkveld, ["Price Pressures" (2014)](https://doi.org/10.1016/j.jfineco.2014.08.001) | Relates short-horizon price changes to order-flow imbalance and depth in 50 NYSE stocks, and develops/tests a dynamic intermediary-inventory account of price pressure in NYSE data. | Specific U.S. equity, venue, period, data, and model settings. | Supplies scoped mechanism candidates, observables, frictions, and boundary conditions before statistical feature search. | Universal causal laws, portability to another market or horizon, executable profitability, or the correctness of any strategy using similar variables. |
| **C23 — Instability, adaptation, and publication effects** | Giacomini & Rossi, ["Forecast Comparisons in Unstable Environments" (2010)](https://doi.org/10.1002/jae.1177); McLean & Pontiff, ["Does Academic Research Destroy Stock Return Predictability?" (2016)](https://doi.org/10.1111/jofi.12365); Lo, ["The Adaptive Markets Hypothesis" (2004)](https://doi.org/10.3905/jpm.2004.442611) | Develops tests of local relative forecast performance under instability; documents lower returns for 97 published cross-sectional predictors out of sample and after publication; proposes an evolutionary conceptual account of changing market efficiency. | Forecast-comparison methods, published U.S. equity predictors, and a qualitative market framework. | Makes temporal stability, publication chronology, and possible strategic adaptation separate research targets rather than after-the-fact excuses. | That every edge decays, that publication caused every decline, that a regime is identified, or that arbitrary adaptive filters are warranted. |
| **C24 — Machine learning in empirical asset pricing** | Gu, Kelly & Xiu, ["Empirical Asset Pricing via Machine Learning" (2020)](https://doi.org/10.1093/rfs/hhaa009) | Compares regularized linear, tree, and neural-network methods for U.S. equity risk-premium prediction and reports strong out-of-sample gains for flexible nonlinear methods in the studied design. | U.S. equities, the paper's predictor set, samples, targets, portfolios, costs, and benchmark procedures. | Shows where ML can contribute: high-dimensional predictive estimation, regularization, specification search, and out-of-sample comparison after the research target is defined. | A universal ML advantage, causal mechanism, transfer to intraday or other assets, freedom from data snooping, or a net live-trading edge. |
| **C25 — Historical data roles under instability** | McLean & Pontiff, ["Does Academic Research Destroy Stock Return Predictability?" (2016)](https://doi.org/10.1111/jofi.12365); Chordia, Subrahmanyam & Tong, ["Have Capital Market Anomalies Attenuated in the Recent Era of High Liquidity and Trading Activity?" (2014)](https://doi.org/10.1016/j.jacceco.2014.06.001); Pesaran & Timmermann, ["Selection of Estimation Window in the Presence of Breaks" (2007)](https://doi.org/10.1016/j.jeconom.2006.03.010) | Documents attenuation in specified published U.S. equity-predictor and anomaly portfolios, and formalizes the bias-variance trade-off in choosing forecasting windows after structural breaks. | Published cross-sectional U.S. equity predictors and anomaly portfolios; regression forecasts under modeled breaks. | Separates the role of historical segments in testing historical existence, regime or stress exposure, and current executable net performance. Requires the design to state which role each segment serves before window or weighting selection. | A universal edge half-life, a fixed calendar window or weighting rule, automatic regime identification from a detected break, or current profitability from historical robustness alone. |

## Source inventory

The ledger cites original scholarly publications and primary-source volumes
across philosophy of science, cognitive science, AI, statistics, decision
theory, econometrics, and finance. Publisher pages, author repositories, and DOI
links are preferred. Later editions are identified where the original work
predates the linked digital edition. No popular or tertiary account is used as
the evidential basis for a material claim.
