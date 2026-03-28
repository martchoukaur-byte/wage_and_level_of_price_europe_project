import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np


# ================================
# Load data
# ================================
df = pd.read_csv(
    r"C:\Users\aumar\OneDrive\Documents\Python SQL Project Real Wage Level Of Price\csv files\wage_level_by_country.csv",
    header=None,
    names=[
        "country",
        "nominal_wage",
        "ppp_wage",
        "price_level_index",
        "log_nominal_wage",
        "log_ppp_wage",
        "log_price_level_index"
    ]
)

pareto = pd.read_csv(
    r"C:\Users\aumar\OneDrive\Documents\Python SQL Project Real Wage Level Of Price\csv files\pareto_efficient_countries.csv",
    header=None,
    names=[
        "country",
        "nominal_wage",
        "ppp_wage",
        "price_level_index",
        "dominator_count",
        "log_nominal_wage",
        "log_ppp_wage",
        "log_price_level_index"
    ]
)

pareto_countries = set(pareto["country"])
df_pareto = df[df["country"].isin(pareto_countries)].copy()


# ================================
# France
# ================================
fr = df[df["country"] == "France"].iloc[0]
x_fr_log = fr["log_price_level_index"]
y_fr_real_log = fr["log_ppp_wage"]
y_fr_nom_log = fr["log_nominal_wage"]


# ================================
# Variables
# ================================
x_log = df["log_price_level_index"]
y_real_log = df["log_ppp_wage"]
y_nom_log = df["log_nominal_wage"]


# ================================
# 1) OLS log real wage (PPP)
# ================================
X_real_log = sm.add_constant(x_log)
model_real_log = sm.OLS(y_real_log, X_real_log).fit()

intercept_real = model_real_log.params["const"]
coef_real = model_real_log.params["log_price_level_index"]
r2_real = model_real_log.rsquared

x_log_grid = np.linspace(x_log.min(), x_log.max(), 100)
X_log_grid = sm.add_constant(x_log_grid)
y_pred_real_log = model_real_log.predict(X_log_grid)


plt.figure(figsize=(8, 5))
plt.scatter(x_log, y_real_log, color="#A96F2D", alpha=0.6, label="log real wage (PPP)")

plt.scatter(
    df_pareto["log_price_level_index"],
    df_pareto["log_ppp_wage"],
    color="blue",
    alpha=0.9,
    label="Pareto-efficient countries (log PPP)"
)

for _, row in df_pareto.iterrows():
    plt.annotate(
        row["country"],
        (row["log_price_level_index"], row["log_ppp_wage"]),
        xytext=(3, 3),
        textcoords="offset points",
        fontsize=7,
        color="blue"
    )

plt.scatter(x_fr_log, y_fr_real_log, color="red", edgecolor="black", s=70, zorder=3)
plt.annotate(
    "France",
    (x_fr_log, y_fr_real_log),
    xytext=(3, 3),
    textcoords="offset points",
    fontsize=8,
    color="black"
)

plt.plot(x_log_grid, y_pred_real_log, color="black", linewidth=2, label="OLS log-log (PPP)")

eq_text_real = (
    f"log(PPP wage) = {intercept_real:.3f} + {coef_real:.3f} * log(price level index)\n"
    f"Intercept = {intercept_real:.3f}\n"
    f"Coefficient = {coef_real:.3f}\n"
    f"R² = {r2_real:.3f}"
)

plt.text(
    0.03, 0.97, eq_text_real,
    transform=plt.gca().transAxes,
    fontsize=9,
    verticalalignment="top",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor="black")
)

plt.xlabel("log(price level index)")
plt.ylabel("log(real wage, PPP)")
plt.title("Log-log regression: real wage (PPP) vs price level index")
plt.legend()
plt.tight_layout()
plt.show()


# ================================
# 2) OLS log nominal wage
# ================================
X_nom_log = sm.add_constant(x_log)
model_nom_log = sm.OLS(y_nom_log, X_nom_log).fit()

intercept_nom = model_nom_log.params["const"]
coef_nom = model_nom_log.params["log_price_level_index"]
r2_nom = model_nom_log.rsquared

y_pred_nom_log = model_nom_log.predict(X_log_grid)


plt.figure(figsize=(8, 5))
plt.scatter(x_log, y_nom_log, color="#5D3A00", alpha=0.6, label="log nominal wage")

plt.scatter(
    df_pareto["log_price_level_index"],
    df_pareto["log_nominal_wage"],
    color="blue",
    alpha=0.9,
    label="Pareto-efficient countries (log nominal)"
)

for _, row in df_pareto.iterrows():
    plt.annotate(
        row["country"],
        (row["log_price_level_index"], row["log_nominal_wage"]),
        xytext=(3, 3),
        textcoords="offset points",
        fontsize=7,
        color="blue"
    )

plt.scatter(x_fr_log, y_fr_nom_log, color="red", edgecolor="black", s=70, zorder=3)
plt.annotate(
    "France",
    (x_fr_log, y_fr_nom_log),
    xytext=(3, 3),
    textcoords="offset points",
    fontsize=8,
    color="black"
)

plt.plot(x_log_grid, y_pred_nom_log, color="black", linewidth=2, label="OLS log-log (nominal)")

eq_text_nom = (
    f"log(nominal wage) = {intercept_nom:.3f} + {coef_nom:.3f} * log(price level index)\n"
    f"Intercept = {intercept_nom:.3f}\n"
    f"Coefficient = {coef_nom:.3f}\n"
    f"R² = {r2_nom:.3f}"
)

plt.text(
    0.03, 0.97, eq_text_nom,
    transform=plt.gca().transAxes,
    fontsize=9,
    verticalalignment="top",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor="black")
)

plt.xlabel("log(price level index)")
plt.ylabel("log(nominal wage)")
plt.title("Log-log regression: nominal wage vs price level index")
plt.legend()
plt.tight_layout()
plt.show()
