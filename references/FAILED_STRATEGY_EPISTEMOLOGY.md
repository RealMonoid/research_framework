# Learning from failed strategies: an epistemic and statistical synthesis

## Scope and protected decision

This note asks whether a failed trading strategy can produce knowledge and how
such knowledge can be separated from retrospective storytelling. It combines
philosophy of science, mathematical/statistical foundations, and selected
quant-finance methods that constrain search, selection, and instability claims.
It does not inspect a strategy or its data, authorize a new test, or change any
framework rule.

The decision at stake is whether a failure justifies (a) reducing confidence in
a stated claim, (b) attributing the failure to a particular component, (c)
generating a new hypothesis, or (d) doing none of these beyond retaining the
negative result.

## Bottom line

Learning from failure is possible, but a bare outcome such as "the strategy
failed" is normally too compressed to identify why. The strongest default
inference is about the **tested conjunction**: under the stated
operationalization, observations, scope, assumptions, and decision rule, the
predicted performance was not obtained. Attribution to a mechanism, condition,
measurement, or implementation requires additional evidence that makes rival
explanations observationally different.

The literature supports a synthesis rather than a single solution:

1. **Duhem and Quine set the attribution limit:** evidence bears on a connected
   bundle, not an isolated proposition.
2. **Lakatos governs continuation:** a revision earns evidential credit only by
   adding risky empirical content; retrospective accommodation alone is not
   progress.
3. **Identifiability formalizes the limit:** if rival explanations induce the
   same distribution for all available observations, no estimator, test,
   additional sample size, or philosophical preference can distinguish them.
4. **Diagnostic and optimal design create the opportunity to learn:** specify
   rival explanations and seek observations on which their predictions differ.
5. **Severity and Bayesian comparison answer different questions:** severity
   asks whether a particular error would probably have been detected; Bayesian
   comparison measures relative updating among explicitly supplied models.
6. **Model criticism keeps the model set open:** choosing the least-bad listed
   explanation does not show that it is adequate or true.
7. **Selective inference and discovery/confirmation separation control
   adaptation:** patterns found while explaining the failure are hypothesis
   generators unless selection is accounted for or genuinely new evidence is
   used.
8. **Quant-finance diagnostics address characteristic distortions:** reality
   checks, superior-predictive-ability tests, model-confidence sets,
   backtest-overfitting measures, and local forecast comparisons can quantify
   selection risk or instability, but they do not identify a market mechanism
   by themselves.

The synthesis can therefore be stated compactly:

> A failure teaches only where the candidate explanations predicted
> detectably different outcomes, the relevant discrepancy had a serious chance
> to be found, the model assumptions are adequate for that inference, and the
> observation was not reused without accounting for the search that selected
> the explanation.

## 1. Why failure attribution is underdetermined

Duhem's argument is narrower and more concrete than the later Quinean thesis.
For Duhem, a test in physics necessarily uses a group of theoretical and
instrumental assumptions, so conflict with observation does not logically name
the guilty member of the group. Quine extends holism to a wider web of belief:
experience constrains the system, while more than one redistribution of revision
may remain possible. These are limits on **unique attribution**, not claims that
evidence is useless. ([Duhem 1906/2021, Chapter VI](https://doi.org/10.1515/9780691233857-014),
[Quine 1951](https://doi.org/10.2307/2181906))

For a strategy failure, let

\[
B = H \land A \land O \land M \land D \land I,
\]

where \(H\) is the substantive claim, \(A\) auxiliary assumptions, \(O\) the
operationalization, \(M\) measurement and statistical model, \(D\) data/scope,
and \(I\) implementation or observation procedure. A conflict with a prediction
of \(B\) is evidence against the bundle. It is not, without a discriminating
argument, a proof of \(\neg H\), \(\neg A\), or any other single negation.

### What can be inferred

- The exact tested bundle did not produce its required consequence.
- A component can receive specific blame when a diagnostic has different
  expected outcomes depending on whether that component or a rival component is
  defective.
- Several independent failures can reduce confidence in a shared core claim if
  the changed auxiliaries genuinely vary and the failures are not repetitions of
  the same unresolved weakness.

### What cannot be inferred

- The core market idea, mechanism, or any one auxiliary is uniquely false merely
  because the bundle failed.
- An untested replacement is better merely because it explains the observed
  anomaly after the fact.
- Failure in one operationalization or domain establishes universal absence.

### Design condition for learning

Represent the bundle explicitly and state which observations would discriminate
among component failures. If no such observations are available, the correct
result is non-identification, not a preferred narrative.

## 2. Lakatos: when continuation adds knowledge

Lakatos changes the unit of appraisal from one theory to a sequence of theories
within a research programme. A progressive problem shift increases empirical
content and, at least intermittently, receives corroboration through novel facts;
a degenerating shift mainly accommodates known anomalies. This does not provide
a mechanical stopping rule, but it blocks the inference that every post-failure
repair is scientific progress. ([Lakatos 1978, Chapter 1](https://doi.org/10.1017/CBO9780511621123.003))

### What can be inferred

- A continuation is epistemically promising when it entails a new observable
  consequence that the prior version did not already entail and risks a new
  failure.
- A history of revisions can be appraised by whether it repeatedly predicts new
  results or repeatedly explains only results already seen.

### What cannot be inferred

- A progressive revision is thereby true.
- A temporarily degenerating programme is logically refuted, or a programme
  without a current rival is confirmed.
- Renaming or versioning a repaired strategy creates new empirical content.

### Design condition for learning

Before obtaining the next relevant observation, record the changed assumption,
the newly implied prediction, a result that would count against it, and an
evaluation source not already consumed in generating the revision.

## 3. Severe testing and error statistics

Mayo's error-statistical account treats evidential warrant as claim- and
procedure-specific: a result warrants a claim to the extent that the procedure
would probably have exposed the relevant error if it were present. Her treatment
of learning from error explicitly addresses the Duhemian problem by emphasizing
local error probes that distinguish effects, artifacts, and sources of anomaly.
([Mayo 2010](https://errorstatistics.com/wp-content/uploads/2015/04/learning-from-error-henle.pdf))

Applied to a negative strategy result, "no useful effect" is informative only
relative to a discrepancy size and a test capable of detecting it. Failure to
reject a null with little sensitivity is not strong evidence of practical
absence. Conversely, a procedure with a high probability of revealing an effect
of decision-relevant size can support an upper bound or an absence claim when it
does not reveal one.

### What can be inferred

- The data can rule out discrepancies the procedure had a high probability of
  detecting.
- A targeted diagnostic can localize a particular error when it is a reliable
  probe for that error and not equally expected under rivals.
- Negative knowledge can be quantitative: for example, the data may constrain
  an effect below a predeclared decision-relevant magnitude rather than prove an
  exact zero.

### What cannot be inferred

- A null or absence claim from a low-sensitivity test.
- A mechanism from a predictive failure unless the mechanism itself received a
  severe, discriminating probe.
- Unique blame when the same result is probable under several error sources.

### Design condition for learning

Specify the exact claim, a practically relevant discrepancy, the sampling model,
and the probability that the procedure would expose that discrepancy. Severity
must be assessed for the inference actually drawn, not attached globally to a
test name.

## 4. Bayesian confirmation and model criticism

For explicit rival explanations \(M_1,\ldots,M_k\), Bayesian updating gives

\[
\frac{P(M_i\mid y,d)}{P(M_j\mid y,d)}
=
\frac{P(M_i)}{P(M_j)}
\times
\frac{p(y\mid M_i,d)}{p(y\mid M_j,d)},
\]

where \(d\) is the observation design. A failure favors \(M_i\) over \(M_j\)
only to the degree that the failure was more probable under \(M_i\). Bayes
factors make this relative evidence explicit but depend on the supplied model
space and priors. ([Kass and Raftery 1995](https://doi.org/10.1080/01621459.1995.10476572))

Relative confirmation is not absolute model adequacy. Box separates estimation
within a model from criticism of the model's predictive implications. Gelman,
Meng, and Stern develop posterior predictive discrepancies, while Gelman and
Shalizi emphasize that Bayesian model selection cannot discover defects absent
from the candidate space; model checking and revision remain necessary.
([Box 1980](https://doi.org/10.2307/2982063),
[Gelman, Meng, and Stern 1996](https://www3.stat.sinica.edu.tw/statistica/j6n4/j6n41/j6n41.htm),
[Gelman and Shalizi 2013](https://doi.org/10.1111/j.2044-8317.2011.02037.x))

### What can be inferred

- A specified failure pattern can shift relative belief among explicit
  explanations in proportion to their likelihoods.
- Posterior or prior predictive checks can reveal respects in which a fitted
  model fails to reproduce important observed structure.
- Sensitivity to priors, model variants, and discrepancy choices can reveal that
  an attribution is fragile.

### What cannot be inferred

- That the highest-posterior listed explanation is adequate, true, causal, or
  even close to the omitted data-generating process.
- Which omitted explanation would repair the model.
- That a posterior predictive discrepancy selected after inspecting the same
  data provides independent confirmation.

### Design condition for learning

State rival models and priors, record the outcome pattern each predicts, assess
relative evidence, and separately perform absolute model checks. Permit an
"all models inadequate" result. Use held-out or future observations for claims
suggested by the original model criticism when independent confirmation is
required.

## 5. Statistical identifiability and misspecification

Identifiability is the mathematical version of the attribution question. A
parameter or explanation is identified only when distinct values or models
produce distinct probability laws for the observable data. Rothenberg shows,
under regularity conditions in parametric models, the connection between local
identification and nonsingularity of the information matrix.
([Rothenberg 1971](https://doi.org/10.2307/1913267))

If

\[
p(y\mid M_i,d)=p(y\mid M_j,d)
\quad\text{for all observable }y\text{ and feasible }d,
\]

then \(M_i\) and \(M_j\) are observationally equivalent. More data from the same
design make estimates more precise within that equivalence; they do not separate
the explanations.

Misspecification creates a different problem. White shows that under regularity
conditions a quasi-maximum-likelihood estimator can converge to the member of a
misspecified family closest in Kullback-Leibler divergence, while conventional
likelihood-based inference may be invalid and the limiting parameter need not be
the substantive parameter of interest. ([White 1982](https://doi.org/10.2307/1912526))

### What can be inferred

- Rank, information, or observational-equivalence analysis can show that an
  attribution is impossible under the current design.
- Under explicit regularity conditions, robust or quasi-likelihood analysis can
  characterize a pseudo-true predictive approximation.
- Specification diagnostics can identify particular departures from a model
  family when they have power against those departures.

### What cannot be inferred

- A structural or mechanistic interpretation for an unidentified parameter.
- Truth of a model from stable estimation or good relative fit.
- That the pseudo-true member of a misspecified family is the true mechanism.
- Absence of all misspecification from failure to reject an omnibus check.

### Design condition for learning

Check whether candidate explanations map injectively to observable
distributions under the proposed measurement design. State which assumptions
deliver identification. Test decision-relevant misspecifications directionally
where possible, and use inference valid under the retained misspecification
class.

## 6. Diagnostic and optimal experimental design

Optimal design reverses the usual postmortem question. Instead of asking which
story best fits the failure already seen, it asks where rival models make the
most different predictions. Atkinson and Fedorov derive sequential and
non-sequential designs specifically for discriminating rival regression models;
Chernoff studies sequential choice among available experiments to reduce
uncertainty efficiently. ([Atkinson and Fedorov 1975](https://doi.org/10.1093/biomet/62.1.57),
[Chernoff 1959](https://doi.org/10.1214/aoms/1177706205))

A generic discrimination objective chooses a feasible design \(d\) that
maximizes expected separation, for example

\[
d^* \in \arg\max_d D\!\left(p_i(\cdot\mid d),p_j(\cdot\mid d)\right),
\]

where \(D\) may be expected log likelihood ratio, Kullback-Leibler divergence,
or a model-specific discrimination criterion. The formula does not guarantee
that the chosen models are adequate; it identifies where they are easiest to
tell apart if one of them is a useful approximation.

In an observational market setting, "design" may mean a prospectively chosen
measurement, outcome, sampling resolution, natural contrast, or future period.
It does not by itself create an intervention or identify a causal mechanism.

### What can be inferred

- A well-chosen future observation can distinguish specified explanations more
  efficiently than another repetition of the original aggregate test.
- A sequence of diagnostics can localize failure when each stage has known,
  differing implications under the candidates.

### What cannot be inferred

- Causality from a merely predictive discrimination design.
- Adequacy of the candidate set.
- Identifiability when every feasible design leaves the candidate distributions
  equal or nearly equal.

### Design condition for learning

Specify rival predictive distributions before the diagnostic observation,
select a feasible contrast with material separation and acceptable uncertainty,
and retain a model-adequacy check. Stop with non-identification when no such
contrast exists.

## 7. Selective and post-hoc inference

Failure analysis is highly adaptive: researchers inspect outcomes, subgroups,
parameters, diagnostics, and stories, then report the most coherent explanation.
Ordinary inferential guarantees generally assume that the tested hypothesis was
not selected by the same random information. Fithian, Sun, and Taylor formalize
selective inference by controlling error conditional on the selection event and
show the trade-off between information used for selection and information left
for inference. ([Fithian, Sun, and Taylor 2014](https://arxiv.org/abs/1410.2597))

### What can be inferred

- Valid inference may remain possible after data-dependent selection when the
  selection procedure is known and the analysis conditions on or otherwise
  accounts for it.
- Data splitting or genuinely future data can provide a simpler separation of
  explanation generation and confirmation, at a cost in information or time.

### What cannot be inferred

- Nominal p-values, intervals, posterior comparisons, or severity claims that
  ignore the search that selected the reported explanation.
- Valid selective inference when the effective search process is unknown or
  cannot be reconstructed.
- Independent confirmation from a diagnostic discovered and "confirmed" on the
  same exhausted information without a valid adjustment.

### Design condition for learning

Record the searched explanations, transformations, subgroups, and stopping
rules. Prefer fresh evidence for confirmation. If reuse is necessary, condition
on the documented selection event or use a valid multiplicity/post-selection
procedure whose assumptions fit the search. Otherwise label the result as
hypothesis generation.

## 8. Hypothesis generation versus confirmation

De Groot's 1956 distinction is directly relevant: exploratory work has an
unknown or data-dependent set of comparisons, whereas confirmatory inference
requires the hypothesis and analysis plan to be fixed independently of the data
used to test them. The translated primary article explicitly allows statistical
tools in exploration while denying them confirmatory evidential force in that
role. ([De Groot 1956/2014](https://doi.org/10.1016/j.actpsy.2014.02.001))

This distinction need not prohibit iterative science. A failed strategy can be
valuable raw material for generating explanations and new predictions. The
epistemic mistake is to treat the fit of the generated explanation to the data
that generated it as confirmation.

### What can be inferred

- Exploration can discover candidate boundaries, neglected variables,
  alternative mechanisms, and better discrepancy measures.
- A generated hypothesis gains confirmatory status only through new evidence or
  an analysis that validly accounts for its selection.

### What cannot be inferred

- That a coherent post-hoc explanation has evidential support merely because it
  matches the failure pattern.
- That preregistration alone repairs weak identification, misspecification, low
  sensitivity, or a non-discriminating design.

### Design condition for learning

Maintain a visible boundary between the consumed evidence that generated the
hypothesis and the evidence assigned to test it. Freeze the prediction and its
failure condition before the confirmatory observation.

## 9. Quant-finance contributions and their epistemic limits

Quantitative finance supplies methods for failure modes that are unusually
important when one historical path supports a large, adaptive strategy search.
These methods strengthen or weaken particular attributions; they do not form a
general root-cause engine.

White's Reality Check tests whether the best model found in a specification
search has predictive superiority over a benchmark while accounting for data
snooping. Hansen's Superior Predictive Ability test improves power and reduces
sensitivity to poor or irrelevant alternatives. Both require the effective
candidate family rather than only the surviving strategy. A rejection can
support predictive superiority of at least one searched candidate; a failure to
reject does not show that every candidate is useless or explain why a selected
strategy later failed. ([White 2000](https://doi.org/10.1111/1468-0262.00152),
[Hansen 2005](https://doi.org/10.1198/073500105000000063))

The Model Confidence Set procedure retains a set of models that the available
data cannot distinguish from the best under a chosen loss function. Informative
data shrink the set; uninformative data leave many survivors. This is a useful
analogue for failure attribution: preserve an epistemic set of live
explanations rather than force one winner. It compares predictive objects and
does not establish that any retained model is true or mechanistically adequate.
([Hansen, Lunde, and Nason 2011](https://doi.org/10.3982/ECTA5771))

The Probability of Backtest Overfitting estimates how often an in-sample winner
underperforms out of sample across symmetric sample partitions. The Deflated
Sharpe Ratio adjusts a reported Sharpe for selection across trials and
non-normal returns. They can make "selection artifact" more or less credible
when the searched family and trials are represented honestly. They cannot by
themselves distinguish data mining from market adaptation, measurement failure,
or a false mechanism, and neither validates a new explanation discovered after
the failure. ([Bailey et al. 2017](https://doi.org/10.21314/JCF.2016.322),
[Bailey and López de Prado 2014](https://doi.org/10.2139/ssrn.2460551))

Giacomini and Rossi replace one global forecast comparison with the time path
of local relative performance. Their fluctuation and one-time-reversal tests
can expose a signature that an overall average hides: persistent inferiority,
temporary breakdown, or reversal. This can discriminate some instability
stories from a stable lack of predictive value, but a detected break does not
name its economic cause and a condition found after inspection remains
exploratory. ([Giacomini and Rossi 2010](https://doi.org/10.1002/jae.1177))

McLean and Pontiff illustrate a more explicitly contrastive design. They
separate original-sample, post-sample, and post-publication periods for 97
published predictors. The different timing gives data-mining and
publication-informed trading different empirical signatures; they report a 26%
out-of-sample decline and a 58% post-publication decline, with the difference
interpreted as evidence consistent with investor learning. This is a model for
how failure analysis can become informative: rival explanations must imply
different patterns before one is favored. It is not a universal decomposition
for an individual strategy, and its interpretation still depends on the
comparability and identifying assumptions of those periods.
([McLean and Pontiff 2016](https://doi.org/10.1111/jofi.12365))

Harvey and Liu make the decision loss explicit by calibrating both false and
missed discoveries. This matters for failed strategies because conservative
multiple-testing controls can suppress false positives while also making false
negative conclusions more likely. A retirement rule therefore needs the cost
of continuing a false edge and the cost of discarding a real one; a nominal
non-rejection is not automatically evidence of absence.
([Harvey and Liu 2020](https://doi.org/10.1111/jofi.12951))

### Combined lesson from quant finance

The quant methods divide into four epistemic jobs:

1. **Selection accounting:** Reality Check, SPA, PBO, and DSR ask whether a
   selected result is credible after the search that produced it.
2. **Set-valued comparison:** Model Confidence Sets preserve several candidates
   when the data cannot justify unique selection.
3. **Failure-pattern localization:** local forecast comparisons ask when and
   under which pre-specified information relative performance changed.
4. **Decision calibration:** joint treatment of false and missed discoveries
   ties evidential thresholds to the cost of continuation and retirement.

None of these jobs substitutes for identification of a mechanism. They become
part of the broader synthesis only when their outputs enter an explicit
rival-explanation map and are interpreted at the claim level they actually test.

## 10. Proposed synthesis: from a binary failure to a discriminating failure map

The most useful synthesis is not a universal postmortem score. It is a sequence
of epistemic gates that converts an undifferentiated failure into explicit rival
predictions.

### Step 1: Preserve the full observation, not only the label

"Failed" is a decision event that discards information. Preserve the pattern of
relevant outcomes and diagnostics, their uncertainty, and the rule that produced
the failure label. This pattern is the evidence \(y\); the label alone is rarely
sufficient for attribution.

### Step 2: State the tested bundle and the claim actually exposed

Separate the substantive claim, operationalization, measurement, scope,
statistical assumptions, and implementation. State the narrowest claim for
which the existing procedure had meaningful sensitivity.

### Step 3: Build a rival-explanation signature table

For each live explanation \(M_j\), state before new observation:

- which part of the bundle it changes;
- the distribution or directional pattern it predicts for each diagnostic;
- which observations would count against it;
- which other explanations remain observationally equivalent.

If two explanations have the same signature over every feasible diagnostic,
record them as not identified rather than rank them by plausibility.

### Step 4: Choose a discriminating observation

Select a future observation or diagnostic where the live explanations predict
materially different results. Quantify expected separation and detectability.
Do not choose only a diagnostic on which the preferred explanation is flexible
enough to fit either outcome.

### Step 5: Evaluate both relative and absolute adequacy

- **Relative track:** use likelihood ratios, Bayes factors, or another explicit
  comparison to measure which supplied explanation better predicted the result.
- **Absolute track:** use severity/error probes and model criticism to ask
  whether the surviving explanation reproduces the aspects that matter and
  whether a decision-relevant error would likely have been found.

The relative winner may still fail the absolute track. "None of the supplied
models is adequate" must remain an available conclusion.

### Step 6: Account for adaptation

If the explanation or diagnostic was selected after seeing the failure, treat
its current status as generated. Confirm it on new evidence or use a valid
post-selection procedure based on the documented selection mechanism.

### Step 7: Classify the epistemic output

The output should be one or more of the following, kept separate:

1. **Bundle-level negative knowledge:** the exact tested conjunction did not
   meet its required consequence.
2. **Bounded negative knowledge:** effects or discrepancies above a stated size
   were severely probed and are constrained under the stated scope.
3. **Discriminated attribution:** one explanation predicted the diagnostic
   pattern materially better than specified rivals and passed relevant adequacy
   checks.
4. **Generated hypothesis:** a plausible new boundary, mechanism, or
   operationalization was discovered but is not yet confirmed.
5. **Non-identification:** available observations do not distinguish the live
   explanations.
6. **Model-set failure:** all specified explanations are inadequate.

### Step 8: Apply the programme-level continuation rule

Any continued strategy idea must produce new empirical content, a prospective
failure condition, and an independent evaluation path. Otherwise it is a
diagnostic or retrospective accommodation, not confirmation of a repaired
strategy.

## 11. Main hazards introduced by this broader question

The broader epistemic inquiry is worthwhile, but it creates characteristic
failure modes:

- **Narrative overfitting:** searching mechanisms and conditions until one fits
  the consumed result.
- **Attribution inflation:** turning evidence against a conjunction into blame
  for one component.
- **Closed-world Bayes:** assigning high probability to the best listed model
  while every listed model is poor.
- **Precision without identification:** obtaining narrow uncertainty around a
  parameter that has no unique structural meaning.
- **Pseudo-truth reification:** interpreting the best approximation inside a
  misspecified family as the actual mechanism.
- **Diagnostic double use:** designing a discrepancy from the anomaly and then
  citing its fit to the same anomaly as confirmation.
- **Low-sensitivity absence claims:** interpreting failure to detect as evidence
  of no relevant effect.
- **Programme immunization:** repeatedly adding conditions that explain known
  failures without risking a novel prediction.
- **Scope overreach:** translating a local negative result into a universal
  claim about a strategy family or market mechanism.
- **Causal leakage:** treating predictive discrimination among stories as
  identification of an intervention or mechanism.

These hazards do not imply that failure analysis should be abandoned. They
imply that its most honest and often most valuable outputs are bounded negative
knowledge, better discriminating designs, and explicit non-identification—not
necessarily a new strategy.

## Source inventory

All substantive sources below are original works, author-hosted manuscripts, or
official journal/publisher records.

1. Pierre Duhem, *The Aim and Structure of Physical Theory*, Chapter VI,
   "Physical Theory and Experiment" (original 1906; Princeton edition 2021).
   [Publisher chapter and DOI](https://doi.org/10.1515/9780691233857-014).
2. W. V. O. Quine, "Two Dogmas of Empiricism," *The Philosophical Review*
   60(1), 1951, 20–43. [JSTOR DOI](https://doi.org/10.2307/2181906).
3. Imre Lakatos, "Falsification and the Methodology of Scientific Research
   Programmes," in *The Methodology of Scientific Research Programmes*, 1978.
   [Cambridge University Press DOI](https://doi.org/10.1017/CBO9780511621123.003).
4. Deborah G. Mayo, "Learning from Error: The Theoretical Significance of
   Experimental Knowledge," *The Modern Schoolman* 87, 2010, 191–217.
   [Author-hosted manuscript](https://errorstatistics.com/wp-content/uploads/2015/04/learning-from-error-henle.pdf).
5. George E. P. Box, "Sampling and Bayes' Inference in Scientific Modelling and
   Robustness," *JRSS A* 143(4), 1980, 383–430.
   [Official journal record and DOI](https://doi.org/10.2307/2982063).
6. Andrew Gelman, Xiao-Li Meng, and Hal S. Stern, "Posterior Predictive
   Assessment of Model Fitness via Realized Discrepancies," *Statistica Sinica*
   6, 1996, 733–807. [Official journal page](https://www3.stat.sinica.edu.tw/statistica/j6n4/j6n41/j6n41.htm).
7. Andrew Gelman and Cosma Rohilla Shalizi, "Philosophy and the Practice of
   Bayesian Statistics," *British Journal of Mathematical and Statistical
   Psychology* 66, 2013, 8–38.
   [Journal DOI](https://doi.org/10.1111/j.2044-8317.2011.02037.x) and
   [author-hosted manuscript](https://stat.columbia.edu/~gelman/research/published/philosophy.pdf).
8. Robert E. Kass and Adrian E. Raftery, "Bayes Factors," *Journal of the
   American Statistical Association* 90(430), 1995, 773–795.
   [Official journal DOI](https://doi.org/10.1080/01621459.1995.10476572).
9. Thomas J. Rothenberg, "Identification in Parametric Models," *Econometrica*
   39(3), 1971, 577–591. [JSTOR DOI](https://doi.org/10.2307/1913267).
10. Halbert White, "Maximum Likelihood Estimation of Misspecified Models,"
    *Econometrica* 50(1), 1982, 1–25.
    [JSTOR DOI](https://doi.org/10.2307/1912526).
11. A. C. Atkinson and V. V. Fedorov, "The Design of Experiments for
    Discriminating Between Two Rival Models," *Biometrika* 62(1), 1975, 57–70.
    [Official journal DOI](https://doi.org/10.1093/biomet/62.1.57).
12. Herman Chernoff, "Sequential Design of Experiments," *The Annals of
    Mathematical Statistics* 30(3), 1959, 755–770.
    [Project Euclid DOI](https://doi.org/10.1214/aoms/1177706205).
13. William Fithian, Dennis Sun, and Jonathan Taylor, "Optimal Inference After
    Model Selection," 2014. [Author manuscript on arXiv](https://arxiv.org/abs/1410.2597).
14. A. D. de Groot, "The Meaning of 'Significance' for Different Types of
    Research" (original 1956; translated and annotated 2014), *Acta
    Psychologica* 148, 188–194.
    [Official journal DOI](https://doi.org/10.1016/j.actpsy.2014.02.001).
15. Halbert White, "A Reality Check for Data Snooping," *Econometrica* 68(5),
    2000, 1097–1126.
    [Official journal DOI](https://doi.org/10.1111/1468-0262.00152).
16. Peter R. Hansen, "A Test for Superior Predictive Ability," *Journal of
    Business & Economic Statistics* 23(4), 2005, 365–380.
    [Official journal DOI](https://doi.org/10.1198/073500105000000063).
17. Peter R. Hansen, Asger Lunde, and James M. Nason, "The Model Confidence
    Set," *Econometrica* 79(2), 2011, 453–497.
    [Official journal DOI](https://doi.org/10.3982/ECTA5771).
18. David H. Bailey, Jonathan M. Borwein, Marcos López de Prado, and Qiji Jim
    Zhu, "The Probability of Backtest Overfitting," *Journal of Computational
    Finance* 20(4), 2017, 39–69.
    [Journal DOI](https://doi.org/10.21314/JCF.2016.322) and
    [open repository record](https://escholarship.org/uc/item/4w1110bb).
19. David H. Bailey and Marcos López de Prado, "The Deflated Sharpe Ratio:
    Correcting for Selection Bias, Backtest Overfitting and Non-Normality,"
    *Journal of Portfolio Management* 40(5), 2014, 94–107.
    [Author manuscript record and DOI](https://doi.org/10.2139/ssrn.2460551).
20. Raffaella Giacomini and Barbara Rossi, "Forecast Comparisons in Unstable
    Environments," *Journal of Applied Econometrics* 25(4), 2010, 595–620.
    [Official journal DOI](https://doi.org/10.1002/jae.1177).
21. R. David McLean and Jeffrey Pontiff, "Does Academic Research Destroy Stock
    Return Predictability?" *The Journal of Finance* 71(1), 2016, 5–32.
    [Official journal DOI](https://doi.org/10.1111/jofi.12365).
22. Campbell R. Harvey and Yan Liu, "False (and Missed) Discoveries in
    Financial Economics," *The Journal of Finance* 75(5), 2020, 2503–2553.
    [Official journal DOI](https://doi.org/10.1111/jofi.12951) and
    [author-hosted manuscript](https://people.duke.edu/~charvey/Research/Published_Papers/P143_False_and_missed.pdf).
