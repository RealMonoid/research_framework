# ADR-005: Unabhängige Kausal- und Handelsachse sowie bedingte Variablenauswahl-Provenienz

**Status:** Angenommen
**Datum:** 2026-08-31

## Kontext

Das Framework führte bereits drei Claim-Level und getrennte Status für
Mechanismus, Forward-OOS-Prognose und ausführbare Netto-Edge. Die Beziehung
zwischen beiden Gruppen war jedoch nur implizit. Dadurch blieb der Fehlschluss
möglich, ein identifizierter kausaler Effekt sei automatisch prognostisch oder
nach Kosten handelbar.

Zugleich fehlte im Intake ein maschinenprüfbarer Unterschied zwischen vorab
fachlich festgelegten Variablen und einer datengetriebenen Suche über viele
Kandidaten. Eine universelle Pflicht zu Feature-Importance-Verfahren würde den
einfachen Fall belasten und kausale Relevanz vortäuschen.

## Entscheidung

1. Der Research-Claim-Level
   (`ASSOCIATIONAL_PREDICTIVE / INTERVENTIONAL / COUNTERFACTUAL`) und die
   Validierungs-/Handelsstatus (`mechanism_supported`, `forward_predictive_oos`,
   `executable_net_edge`) sind ausdrücklich unabhängige Achsen.
2. Ein kausaler Claim darf durch ein SCM/DAG, Potential-Outcomes-Design,
   strukturell-ökonometrisches oder anderes explizites Identifikationsmodell
   begründet werden. Die Notation selbst erhöht den Claim-Level nicht.
3. Jeder promovierte Intake deklariert die Variablenauswahl als `PREDEFINED`,
   `DATA_DRIVEN` oder `HYBRID`.
4. `PREDEFINED` benötigt nur Begründung und beibehaltene Variablen. Erst
   `DATA_DRIVEN` und `HYBRID` benötigen Kandidatenuniversum, Selektionsdaten und
   -rolle, Outcome-Sichtbarkeit, Methoden, effektive Kandidatenzahl, Suchraum und
   Auswahlbias-Kontrollen.
5. SHAP-, Shapley-, Impurity- und andere Feature-Importance-Verfahren bleiben
   optionale Diagnosen. Sie sind weder Pflicht noch Kausalitätsnachweis.
6. `VALIDATED_PHENOMENON` bestätigt weder einen kausalen Claim noch eine
   ausführbare Netto-Edge.

## Folgen

- Das Hypothesen-Schema steigt auf Version `1.2.0`; `PROMOTED` verlangt den neuen
  Auswahlrecord.
- Positive und negative Vertragstests prüfen sowohl den leichten
  `PREDEFINED`-Pfad als auch die strengere datengetriebene Provenienz.
- Ein Eval-Fall schützt die Trennung zwischen identifiziertem Effekt und
  wirtschaftlicher Handelbarkeit.
- Reale Research Cases werden durch diese Änderung nicht erfunden. Die bekannte
  end-to-end Validierungslücke bleibt bestehen, bis ein echter Fall verfügbar ist.

## Verworfene Alternativen

### Universeller DAG-Zwang

Verworfen, weil Potential-Outcomes- und andere explizite Designs ein Estimand
ohne zusätzlichen DAG identifizieren können. Ein Diagramm allein verbessert die
Identifikation nicht.

### Obligatorische SHAP-/MDI-Auswertung

Verworfen, weil diese Verfahren modell- und verteilungsabhängige Relevanz
beschreiben und keine allgemeine kausale Variablenauswahl liefern.

### Kausaler PASS als automatische Handelsfreigabe

Verworfen, weil ein wissenschaftlich identifizierter Effekt unterhalb von
Spread, Gebühren, Slippage oder Latenz ökonomisch wertlos sein kann.
