# ADR-006: Vorgelagerter Mechanismenkatalog als echter Ideengenerator

**Status:** Accepted
**Date:** 2026-08-31
**Deciders:** Projektverantwortlicher und Maintainer des Research-Frameworks

## Context

Das Framework konnte eingehende Hypothesen bereits streng aufnehmen, routen und
prüfen. Es enthielt aber keinen Producer, der vor dem Intake tatsächlich neue
Ideen erzeugt. Ohne externe Eingebung blieb die Inbox leer; weitere
Screeningregeln hätten diese Lücke nicht geschlossen.

Die Kurzfristliteratur dokumentiert mehrere produktive Mechanismenfamilien:
Orderbuch-Ungleichgewichte, geteilte Großaufträge, Intermediärinventar,
Stop-Cluster, Derivate-Hedging, Optionsverfall, vorhersehbare Futures-Rolls,
Schlussauktionen, Cross-Market-Preisfindung, Intraday-Wiederholungen,
Index-Rebalancing sowie Funding- und Liquidationsmechaniken. Diese Arbeiten
belegen keine konkrete neue Strategie, liefern aber Mechanismen, erwartete
Signaturen und natürliche Zeithorizonte, aus denen Kandidaten deduziert werden
können.

Eine reine Akteursfrage greift zu kurz. Nicht jede produktive Intraday-Idee hat
einen eindeutig identifizierbaren gezwungenen Akteur; Orderbuchzustände,
Lead-Lag-Beziehungen und replizierbare Clock-Time-Muster können ebenfalls Ideen
erzeugen. Umgekehrt erzeugt ein bekannter Zwang nicht nur direkten Preisdruck:
Antizipation, zusätzliche Liquiditätsbereitstellung und ein späterer Unwind sind
eigenständige Kandidaten.

Aus der Diskussion um Einsichtsheuristiken werden nur drei produktive
Transformationen übernommen: Widerspruch, Verbindung und Lockerung einer
Annahme. Sie erzeugen neue Kandidaten, aber keine Validitäts- oder
Evidenzaussage. Premortem, intuitive Selbsteinstufung und Prozessmetaphern werden
nicht in die Erzeugungsschicht übernommen.

## Decision

1. `generation/mechanism_catalog.v1.json` wird der versionierte, ausschließlich
   auf Intraday- und kurze Swing-Horizonte bis fünf Handelstage begrenzte
   Ausgangskatalog.
2. Der Katalog unterstützt fünf gleichwertige Erzeugungsrouten:
   `CONSTRAINT_FIRST`, `MICROSTRUCTURE_STATE`, `LINKAGE_OR_IDENTITY`,
   `LITERATURE_REPLICATION` und `OBSERVATION_DRIVEN`.
3. Der Generator verwendet die Grammatik
   `Mechanismus × Phase × beobachtbare Reaktion` und die Operatoren
   `PHASE_PATH`, `EXPECTATION_VIOLATION`, `MECHANISM_CONNECTION` und
   `ASSUMPTION_RELAXATION`.
4. `scripts/generate_hypotheses.py` ist ein deterministischer Producer. Er
   erzeugt einen Generation-Run und echte minimale `INBOX`-Artefakte.
5. `agents/intraday-hypothesis-generator.md` definiert eine optionale
   agentische Erweiterung mit denselben Auslösern, Grenzen und Outputfeldern.
6. Ein Generation-Run endet immer vor Screening und Promotion. Er vergibt keine
   Evidenzstufe, keinen Confidence Score und keine Aussage über Profitabilität.
7. Das bestehende `INBOX` bleibt günstig. Reichere Generator-Provenienz wird im
   separaten Generation-Run gespeichert und im Candidate nur referenziert.

## Explicit Non-Decisions

Nicht eingeführt werden:

- ein universell verpflichtendes `actor_constraint`,
- ein Premortem-Feld oder Premortem-Operator im Generator,
- eine selbst vergebene Validity-Klasse,
- ein Promotionsverbot für beobachtungsgetriebene Ideen,
- ein neues Noise-, Backtest- oder Sicherheitsgate,
- Kaizen-, Gemba- oder andere Managementmetaphern als Normprosa,
- eine Aussage, dass Ablehnungscluster automatisch Marktanomalien seien,
- Portfoliotheorie oder langfristige Investmentfaktoren.

Diese Ausschlüsse verhindern nicht die bestehenden nachgelagerten
Research-Prüfungen. Sie halten nur die Erzeugungsschicht von Prüfung und
Freigabe getrennt.

## Consequences

- Das Framework besitzt nun einen ausführbaren Pfad von einem versionierten
  Mechanismenkatalog zu neuen Intake-Artefakten.
- Widersprüche retten keine alte Hypothese, sondern erzeugen eine neue
  Ideenfamilie mit eigener ID.
- Vorhersehbare Flows erzeugen auch Antizipations-, Absorptions- und
  Unwind-Ideen statt nur naive Richtungswetten.
- Der Katalog kann quellen- und versionskontrolliert erweitert werden, ohne das
  Intake-Schema mit Pflichtfeldern aufzublähen.
- Die Qualität oder Handelbarkeit der erzeugten Ideen bleibt offen und wird
  erst im bestehenden nachgelagerten Prozess untersucht.

## Sources motivating the initial catalog

- Cont, Kukanov und Stoikov (2014),
  <https://doi.org/10.1093/jjfinec/nbt003>
- Gould und Bonart (2016), <https://arxiv.org/abs/1512.03492>
- Moro et al. (2009), <https://doi.org/10.1103/PhysRevE.80.066102>
- Hendershott und Menkveld (2014),
  <https://doi.org/10.1016/j.jfineco.2014.08.001>
- Osler (2003), <https://doi.org/10.1111/1540-6261.00588>
- Baltussen et al. (2021),
  <https://doi.org/10.1016/j.jfineco.2021.04.029>
- Ni, Pearson und Poteshman (2005),
  <https://doi.org/10.1016/j.jfineco.2004.08.005>
- Bessembinder et al. (2016),
  <https://www.sciencedirect.com/science/article/pii/S0304405X16300113>
- Wu und Jegadeesh (2022),
  <https://doi.org/10.1016/j.jfineco.2021.12.003>
- Chan (1992), <https://doi.org/10.1093/rfs/5.1.123>
- Heston, Korajczyk und Sadka (2010),
  <https://doi.org/10.1111/j.1540-6261.2010.01573.x>
- Pavlova und Sikorskaya (2023),
  <https://doi.org/10.1093/rfs/hhac055>
- Greenwood und Sammon (2025), <https://doi.org/10.1111/jofi.13410>
- Cheng, Deng, Wang und Yu (2021), <https://arxiv.org/abs/2102.04591>
- He, Manela, Ross und von Wachter (2022),
  <https://arxiv.org/abs/2212.06888>

## Action Items

1. [x] Mechanismenkatalog und Schemas anlegen.
2. [x] Deterministischen Producer implementieren.
3. [x] Agentenvertrag mit Triggerbeispielen und Outputvertrag anlegen.
4. [x] Reproduzierbaren Vier-Operatoren-Lauf als Beispiel persistieren.
5. [x] Positive, negative und end-to-end Producer-Tests in CI integrieren.
6. [ ] Katalog nach praktischer Nutzung um weitere venue- und
   instrumentspezifische Mechanismen ergänzen.
