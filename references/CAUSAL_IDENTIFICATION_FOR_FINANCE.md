# Causal identification in quantitative finance

**Version:** 1.0

**Stand:** 2026-08-31

**Zweck:** Verbindliche Forschungsbasis für den `causal-identification-critic`.

## Kernaussage

Ein statistisches Verfahren kann einen Effekt nur innerhalb eines bereits
begründeten Designs schätzen. Es kann nicht selbst entscheiden, ob der
beobachtete Unterschied durch die behauptete Ursache, gemeinsame Nachrichten,
simultane Reaktionen, Selektion, ein falsches Renditemodell oder einen anderen
unbeobachteten Einfluss entstanden ist.

Für Finanzdaten werden daher vier Fragen getrennt:

1. **Identifikation:** Welcher Vergleich entspricht der behaupteten
   Intervention, und unter welchen Annahmen?
2. **Schätzung:** Wie groß ist der so identifizierte Effekt und wie unsicher ist
   er unter zeitlicher, marktweiter und ereignisbezogener Abhängigkeit?
3. **Vorhersage:** Hilft die Information bei späteren, wirklich unbekannten
   Beobachtungen?
4. **Handelbarkeit:** War sie rechtzeitig beobachtbar und nach Kosten nutzbar?

## Was der Prüfer aus der Quant-Forschung anwenden muss

| Forschungsfall | Vor einer kausalen Aussage zu klären |
|---|---|
| Finanzielle Event Study | Gegenfaktisches Renditemodell, systematisches Event-Timing, Volatilität, Horizont, andere Ereignisse und Abhängigkeit. Klassische abnormal returns können bei einem falschen Faktormodell einen Scheineffekt erzeugen. |
| High-Frequency Identification | Exakte Veröffentlichungszeit, Leakage, andere Meldungen im Fenster, Konstruktion der Überraschung, Vorhersagbarkeit aus Vorabinformationen, mögliche Informationsschocks, Separierbarkeit der Wirkungen und Dominanz des beabsichtigten Schocks. Ein enges Fenster ist hilfreich, aber keine vollständige Identifikation. |
| Order Flow und Preiswirkung | Simultanität, Reverse Causality, gemeinsamer Informationszufluss, Messreihenfolge und eine exogene Variation oder ein strukturelles Modell. |
| DiD und dynamische Event Study | Antizipation, parallele Trends, gestaffelte oder wiederholte Behandlung, Rückkopplung, zeitveränderliche Effekte, Spillover sowie cluster- und zeitgerechte Unsicherheit. Ein unauffälliger Pretrend-Test beweist die Annahme nicht. |
| Instrumentvariablen | Relevanz, Ausschluss anderer Wirkungspfade, Unabhängigkeit, Monotonie sofern benötigt und der tatsächlich lokale Effekt. |
| Synthetic Control | Glaubwürdige Spender, guter Fit vor dem Ereignis, keine Kontamination oder Spillover, geeignete Placebos und Sensitivität gegenüber Spendern und Zeitraum. |
| Backdoor-/Control-Design | Vollständigkeit der relevanten Vorbehandlungs-Confounder, Overlap, keine Collider oder Nachbehandlungsvariablen und Robustheit gegen unbeobachtete Confounder. |
| DML, Causal Forest, Local Projections | Diese Verfahren schätzen flexibel oder dynamisch. Die Identifikationsannahmen müssen vorher aus einem anderen Argument stammen. Zeitreihen benötigen passende Splits und Abhängigkeitskorrekturen. |
| Causal Discovery | Annahmen über Lags, Stationarität, latente Confounder, Messfehler und bedingte Unabhängigkeit. Das Ergebnis bleibt ein Kandidatengraph oder eine Äquivalenzklasse. |
| Mathematisch gekoppelte Variablen | Gemeinsame Fenster, Rohinputs, Nenner, Schwellen und deterministische Transformationen. Sie können eine Beziehung rechnerisch erzeugen oder das Estimand verändern; sie sind weder automatisch ein Fehler noch Kausalbeleg. |

## Primärquellen und ihre verbindliche Lehre

- Judea Pearl (2009/2010), *The Foundations of Causal Inference*: Kausale
  Schlussfolgerungen benötigen kausale Annahmen, die nicht vollständig aus der
  beobachteten Verteilung testbar sind.
  <https://ftp.cs.ucla.edu/pub/stat_ser/r350.pdf>
- Charles Kahn und Toni Whited (2018), *Identification Is Not Causality, and
  Vice Versa*: Exogene Variation und ein ökonomisches Modell beantworten
  unterschiedliche Teile einer kausalen Frage; ein Effekt identifiziert nicht
  automatisch den Mechanismus.
  <https://academic.oup.com/rcfs/article/7/1/1/4590088>
- Victor Chernozhukov et al. (2018), *Double/Debiased Machine Learning for
  Treatment and Structural Parameters*: DML schützt die Schätzung gegen
  Regularisierungsfehler unter vorausgesetzter Identifikation; es erzeugt diese
  Identifikation nicht.
  <https://www.nber.org/papers/w23564>
- John Cochrane und Monika Piazzesi (2002), *The Fed and Interest Rates – A
  High-Frequency Identification*: Grunddesign der zeitlich engen
  Überraschungsidentifikation.
  <https://www.nber.org/papers/w8839>
- Michael Bauer und Eric Swanson (2023), *A Reassessment of Monetary Policy
  Surprises and High-Frequency Identification*: Vorabinformationen können
  vermeintliche Überraschungen vorhersagen; Orthogonalisierung und
  Informationskanäle müssen geprüft werden.
  <https://www.nber.org/papers/w29939>
- Francesco Bianchi, Sydney Ludvigson und Sai Ma (überarbeitete Fassung 2026),
  *A Structural Approach to High-Frequency Identification of Monetary
  Non-Neutrality*: High-Frequency-Signale erhalten erst innerhalb eines
  strukturellen Modells ihre wirtschaftliche Interpretation.
  <https://www.nber.org/papers/w30072>
- Alessandro Casini und Adam McCloskey (Preprint 2024, überarbeitet 2025),
  *Identification and Estimation of Causal Effects in High-Frequency Event
  Studies*: Ein enges Zeitfenster reicht nicht aus. Die kausale Interpretation
  verlangt unter anderem Separierbarkeit und relative Exogenität, also dass der
  beabsichtigte Schock die übrigen Schocks im Fenster dominiert.
  <https://arxiv.org/abs/2406.15667>
- Paul Goldsmith-Pinkham und Tianshu Lyu (Preprint 2025), *Causal Inference in
  Financial Event Studies*: Faktormodell-Fehlspezifikation kann klassische
  Event-Study-Schätzer inkonsistent machen, besonders bei längeren, volatilen
  oder systematisch terminierten Ereignissen; replizierende Portfolios und
  quasi-experimentelle Designs sind mögliche Alternativen.
  <https://arxiv.org/abs/2511.15123>
- Jonathan B. Cohn, Travis L. Johnson und Zack Liu (JFE 2026), *Past is
  Prologue: Inference from the Cross Section of Returns Around an Event*: Die Event-Beziehung sollte gegen dieselbe
  Beziehung an Vor-Ereignis-Tagen geprüft werden, weil Confounding Events oft
  plausible Scheinergebnisse erzeugen.
  <https://www.sciencedirect.com/science/article/pii/S0304405X26000498>
- Òscar Jordà (2005), *Estimation and Inference of Impulse Responses by Local
  Projections*: Local Projections sind eine Schätzmethode für dynamische
  Reaktionen; die Identifikation des Schocks ist eine vorgelagerte Aufgabe.
  <https://www.aeaweb.org/articles?id=10.1257%2F0002828053828518>
- Jonathan Roth (2022), *Pretest with Caution*: Pretrend-Tests können geringe
  Teststärke haben und die Auswahl nach einem bestandenen Test kann die
  Inferenz verzerren.
  <https://www.aeaweb.org/articles?id=10.1257%2Faeri.20210236>
- Ashesh Rambachan und Jonathan Roth (2023), *A More Credible Approach to
  Parallel Trends*: Sensitivität und partielle Identifikation machen sichtbar,
  wie stark Ergebnisse von zulässigen Verletzungen paralleler Trends abhängen.
  <https://www.aeaweb.org/articles?id=10.1257%2Frestud.20220186>
- Alberto Abadie (2021), *Using Synthetic Controls*: Spenderpool, Vorperioden-
  Fit, keine Interferenz und Placebos sind zentrale Designbestandteile.
  <https://www.aeaweb.org/articles?id=10.1257%2Fjel.20191450>
- Wang Miao, Xu Shi und Eric Tchetgen Tchetgen (2020), *A Confounding Bridge
  Approach for Double Negative Control Inference*: Negativkontrollen helfen
  nur unter expliziten Annahmen und sind keine automatische Entwarnung.
  <https://academic.oup.com/jrsssb/article/82/2/521/7056052>
- Jakob Runge et al. (2019), *Inferring causation from time series in Earth
  system sciences*: Zeitreihen-Causal-Discovery benötigt Annahmen über
  Abhängigkeit, Lags und Confounding; das Verfahren ersetzt kein externes
  Identifikationsdesign.
  <https://www.nature.com/articles/s41467-019-10105-3>

Preprints und jüngere Arbeiten werden als solche gekennzeichnet. Sie ergänzen
die etablierten Identifikationsregeln, ersetzen sie aber nicht. Keine dieser
Quellen belegt für sich eine konkrete Trading-Edge.
