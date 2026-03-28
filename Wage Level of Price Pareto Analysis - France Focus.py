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

# Log explanatory variable
x_log = df["log_price_level_index"]

# France point
fr = df[df["country"] == "France"].iloc[0]
x_fr_log = fr["log_price_level_index"]
y_fr_real_log = fr["log_ppp_wage"]
y_fr_nom_log = fr["log_nominal_wage"]


# ================================
# A) OLS 1 : log_ppp_wage ~ log_price_level_index
# ================================
X_real_log = sm.add_constant(x_log)
y_real_log = df["log_ppp_wage"]
model_real_log = sm.OLS(y_real_log, X_real_log).fit()

# Grid for fitted line
x_log_grid = np.linspace(x_log.min(), x_log.max(), 100)
X_log_grid = sm.add_constant(x_log_grid)
y_pred_real_log = model_real_log.predict(X_log_grid)

# Params
intercept_real = model_real_log.params["const"]
beta_real = model_real_log.params["log_price_level_index"]
r2_real = model_real_log.rsquared

plt.figure(figsize=(6, 4))
# all countries
plt.scatter(x_log, y_real_log, color="#A96F2D", alpha=0.85, label="log real wage (PPP)")
# France in orange
plt.scatter(x_fr_log, y_fr_real_log, color="orange", edgecolor="black", s=60, zorder=3)
plt.annotate(
    "France",
    (x_fr_log, y_fr_real_log),
    xytext=(3, 3),
    textcoords="offset points",
    fontsize=8,
    color="black"
)
# OLS line
plt.plot(x_log_grid, y_pred_real_log, color="black", linewidth=2, label="OLS log-log (PPP)")

# Text box with regression parameters
text_real = (
    f"log(PPP wage) = {intercept_real:.2f} + {beta_real:.4f} * log(price)\n"
    f"Intercept: {intercept_real:.2f}\n"
    f"Coeff: {beta_real:.4f}\n"
    f"R²: {r2_real:.3f}"
)
plt.text(
    0.05, 0.95,
    text_real,
    transform=plt.gca().transAxes,
    fontsize=8,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.7)
)

plt.xlabel("log(price level index)")
plt.ylabel("log(real wage, PPP)")
plt.title("Log-log OLS: log(real wage, PPP) vs log(price level index)")
plt.legend()
plt.tight_layout()
plt.show()


# ================================
# B) OLS 2 : log_nominal_wage ~ log_price_level_index
# ================================
X_nom_log = sm.add_constant(x_log)
y_nom_log = df["log_nominal_wage"]
model_nom_log = sm.OLS(y_nom_log, X_nom_log).fit()

y_pred_nom_log = model_nom_log.predict(X_log_grid)

# Params
intercept_nom = model_nom_log.params["const"]
beta_nom = model_nom_log.params["log_price_level_index"]
r2_nom = model_nom_log.rsquared

plt.figure(figsize=(6, 4))
# all countries
plt.scatter(x_log, y_nom_log, color="#5D3A00", alpha=0.85, label="log nominal wage")
# France in orange
plt.scatter(x_fr_log, y_fr_nom_log, color="orange", edgecolor="black", s=60, zorder=3)
plt.annotate(
    "France",
    (x_fr_log, y_fr_nom_log),
    xytext=(3, 3),
    textcoords="offset points",
    fontsize=8,
    color="black"
)
# OLS line
plt.plot(x_log_grid, y_pred_nom_log, color="black", linewidth=2, label="OLS log-log (nominal)")

# Text box with regression parameters
text_nom = (
    f"log(nominal wage) = {intercept_nom:.2f} + {beta_nom:.4f} * log(price)\n"
    f"Intercept: {intercept_nom:.2f}\n"
    f"Coeff: {beta_nom:.4f}\n"
    f"R²: {r2_nom:.3f}"
)
plt.text(
    0.05, 0.95,
    text_nom,
    transform=plt.gca().transAxes,
    fontsize=8,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.7)
)

plt.xlabel("log(price level index)")
plt.ylabel("log(nominal wage)")
plt.title("Log-log OLS: log(nominal wage) vs log(price level index)")
plt.legend()
plt.tight_layout()
plt.show()