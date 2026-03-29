# Results

## 1. Descriptive Patterns

The cross-country distribution of net nominal wages, net real wages, and implied price levels shows large heterogeneity across European economies.

- Countries with high **net nominal wages** tend, on average, to display higher **price levels**.
- However, the ranking of countries in terms of **net real wages** differs noticeably from the ranking in terms of **net nominal wages**, reflecting the role of differences in cost of living.
- A first inspection of the data already suggests that some countries manage to combine relatively high real wages with comparatively moderate price levels, while others face the opposite configuration.

These descriptive patterns motivate a more formal comparison based on Pareto efficiency and regression analysis.

---

## 2. France as Benchmark

France is used as an initial benchmark to assess relative performance.

For each country in the sample, we compare:

- its **average net real wage** with that of France; and
- its **price level** with that of France.

A country is said to **dominate France** if it simultaneously has:

- a **higher** net real wage; and
- a **lower** price level.

Under this criterion:

- No country in the sample simultaneously offers a higher average net real wage and a lower price level than France.
- France is therefore **Pareto-optimal** in the two-dimensional space defined by (real wage, price level).

This does not mean France is the “best” country on any single dimension, but that there is no strictly better combination of income and cost of living in the observed panel.

---

## 3. Pareto-Optimal Countries in the Panel

The Pareto analysis is then extended to all countries.

A country is classified as **Pareto-optimal** if there is no other country in the sample that simultaneously:

- has a **higher** net real wage; and
- has a **lower** price level.

The resulting Pareto set:

- contains France and a small subset of other countries;
- consists of **non-dominated** country profiles where any further gain in real wage would require accepting a higher price level, or any reduction in price level would come with a lower real wage.

In other words, these countries lie on the empirical “efficiency frontier” defined by purchasing power and cost of living.

---

## 4. Most Dominated Countries

The analysis then looks at the opposite cases: countries that are dominated by many others.

For each country, the number of **dominating countries** is counted, where a dominating country is defined as one that has:

- a higher net real wage; and
- a lower price level.

The **most dominated** countries are those for which this count is largest. These economies:

- face the most unfavourable combination of relatively low real income and relatively high prices;
- can be seen as being in a systematically worse position than a large portion of the sample.

This ranking highlights where the gap in living standards and cost of living is most pronounced relative to the rest of Europe.

---

## 5. Log-Linear Regressions

To quantify the relationship between wages and price levels, two log-log regressions are estimated:

1. \(\ln(\text{Price Level})\) on \(\ln(\text{Net Nominal Wage})\)  
2. \(\ln(\text{Price Level})\) on \(\ln(\text{Net Real Wage})\)

Formally:
\[
\ln P_i = \alpha + \beta \ln W_i + \varepsilon_i
\]
where:
- \(P_i\) is the price level in country \(i\),
- \(W_i\) is either the net nominal wage or the net real wage,
- \(\beta\) is the wage–price elasticity.

The main findings are:

- In both specifications, the estimated elasticity \(\beta\) is **positive**.
- Countries with higher net nominal wages tend to have higher price levels.
- Countries with higher net real wages also tend to have higher price levels.

This is consistent with the intuitive idea (and the Balassa–Samuelson mechanism) that richer countries, in terms of wages, tend to exhibit higher price levels.

---

## 6. Residual Analysis and Atypical Countries

Beyond the average relationship captured by the regressions, the **residuals** are used to identify atypical countries.

- A **large positive residual** means that the country’s price level is **higher** than what its wage level would predict (expensive relative to income).
- A **large negative residual** means that the price level is **lower** than predicted (cheap relative to income).

Two sets of residuals are obtained:

1. Residuals from the **nominal wage vs. price** regression.
2. Residuals from the **real wage vs. price** regression.

A key empirical result is that:

- The list of the 10 countries with the largest residuals in the **real wage vs. price** regression differs from the list obtained in the **nominal wage vs. price** regression.

This difference reflects the fact that **nominal and real wages are not colinear**:

- The gap between nominal and real wages is precisely the effect of the price level.
- Countries that move significantly between the two residual rankings are those where the price level plays the most decisive role in transforming nominal income into real purchasing power.

In practical terms, these countries are particularly interesting because:

- they may appear “high income” in nominal terms but lose much of this advantage once prices are taken into account; or
- they may look modest in nominal terms but deliver surprisingly high purchasing power thanks to low price levels.

---

## 7. Interpretation

Taken together, the results indicate that:

- Cross-country differences in net nominal wages in Europe cannot be read independently of price levels.
- Some countries, such as those on the Pareto frontier (including France), manage to occupy positions where no other country strictly dominates them in both real wages and prices.
- Other countries are substantially dominated, with many peers offering both higher real wages and lower prices.
- The divergence between residual-based rankings in the nominal and real specifications highlights where the **cost of living** is the main driver of the gap between nominal income and actual purchasing power.

These patterns motivate further work to decompose nominal wage differences into price effects versus “pure” real wage differences, and to relate these to structural or institutional characteristics of the economies considered.
