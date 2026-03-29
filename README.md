# Wage and Price Levels in Europe

## Overview

This project studies the relationship between **net nominal wages**, **net real wages**, and **price levels** across European countries. The core question is whether cross-country differences in net nominal wages are primarily driven by differences in price levels or by differences in real purchasing power.

The analysis uses data collected from Wikipedia on average net wages and cost-of-living indicators. From these, a synthetic price level is constructed as the link between nominal and real net wages.

## Research Questions

- To what extent do differences in **net nominal wages** across European economies reflect:
  - differences in **price levels**, versus
  - differences in **net real wages** (purchasing power)?

- Which countries are **Pareto-optimal** when jointly considering:
  - average net real wage, and
  - price level (cost of living)?

- Which countries are the **most dominated**, i.e. have many other countries that simultaneously offer:
  - a higher average net real wage, and
  - a lower price level?

## Data

- **Source:** Wikipedia pages on:
  - Average net nominal wages by country
  - Cost of living / price level indicators

- **Variables:**
  - Net nominal wage (monthly, in local currency or EUR, depending on Wikipedia)
  - Net real wage (adjusted for purchasing power)
  - Implied price level (constructed from the relation between nominal and real net wages)

The analysis is performed on a panel of European countries for which all three variables can be consistently obtained.

## Methodology

### 1. Construction of the Price Level

For each country, a synthetic price level is derived from the relationship between net nominal and net real wages. Intuitively:

- Higher nominal wages for a given level of real wages imply a **higher** price level.
- Conversely, lower nominal wages for a given real wage imply a **lower** price level.

This price level measure is used to compare the **cost of living** across countries.

### 2. France as Initial Benchmark

The analysis starts by using France as a reference point:

- For each country, we compare:
  - its average net real wage to that of France, and
  - its price level to that of France.

A country would **dominate** France if it had both:

- a higher net real wage, and
- a lower price level.

Result: in the sample considered, **no country simultaneously offers a higher average net real wage and a lower price level than France**. France is therefore Pareto-optimal in this two-dimensional space (real wage, price level).

### 3. Pareto-Optimal Countries in the Panel

The analysis is then extended to all countries:

- A country is defined as **Pareto-optimal** if no other country in the panel dominates it simultaneously on:
  - higher net real wage, and
  - lower price level.

This yields a set of countries that are **non-dominated** in terms of purchasing power and cost of living.

Only a limited number of countries share the same type of Pareto-optimal position as France on this criterion.

### 4. Most Dominated Countries

The project then looks at the opposite situation:

- For each country, we count how many other countries:
  - have a higher net real wage, and
  - have a lower price level.

Countries with the **largest number of such dominating countries** are identified as the **most dominated** in the sample: many other economies offer both higher real wages and lower prices.

This provides a ranking of countries that are in the least favorable position when combining income and cost of living.

### 5. Log-Linear Regressions

To quantify the relationship between wages and prices, two log-log regressions are estimated:

- \(\ln(\text{Price Level})\) on \(\ln(\text{Net Nominal Wage})\)
- \(\ln(\text{Price Level})\) on \(\ln(\text{Net Real Wage})\)

These specifications allow the estimation of **elasticities**:

- How much the price level increases (in %) when nominal or real wages increase by 1%.

In both cases, a **positive relationship** is found:

- Countries with higher nominal or real net wages tend to have higher price levels.

### 6. Residual Analysis

For each regression, the **residuals** (error terms) are used to detect **atypical countries**:

- Large **positive** residual:
  - The country’s price level is **higher** than what its wage level would predict.
  - Interpreted as a relatively **expensive** cost of living given its income.

- Large **negative** residual:
  - The country’s price level is **lower** than predicted.
  - Interpreted as relatively **cheap** given its income.

A key feature of the results is that:

- The set of the 10 countries with the largest residuals in the **real wage vs. price** regression is **not the same** as the set obtained in the **nominal wage vs. price** regression.

This reflects the fact that nominal and real wages are not colinear: the gap between the two is precisely the effect of the price level. Countries whose ranking changes between the two regressions are those where the price level plays the most decisive role in transforming nominal income into real purchasing power.
