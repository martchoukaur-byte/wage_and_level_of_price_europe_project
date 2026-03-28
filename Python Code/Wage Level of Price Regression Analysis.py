import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
import os

# ================================
# Output folders
# ================================
base_output_dir = "output"
fig_dir = os.path.join(base_output_dir, "figures")
reg_dir = os.path.join(base_output_dir, "regressions")

os.makedirs(fig_dir, exist_ok=True)
os.makedirs(reg_dir, exist_ok=True)

# ================================
# Load data
# ================================
df = pd.read_csv(
    r"C:/Users/aumar/OneDrive/Documents/Python SQL Project Real Wage Level Of Price/csv files/wage_level_by_country.csv",
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

# ================================
# C) OLS 1 : log_ppp_wage ~ log_price_level_index
# ================================
x_log = df["log_price_level_index"]
X_log_real = sm.add_constant(x_log)
y_log_real = df["log_ppp_wage"]
model_log_real = sm.OLS(y_log_real, X_log_real).fit()

# Save regression summary
with open(os.path.join(reg_dir, "ols_log_ppp_vs_log_price.txt"), "w", encoding="utf-8") as f:
    f.write(model_log_real.summary().as_text())

x_log_grid = np.linspace(x_log.min(), x_log.max(), 100)
X_log_grid = sm.add_constant(x_log_grid)
y_log_pred_real = model_log_real.predict(X_log_grid)

plt.figure(figsize=(6, 4))
plt.scatter(x_log, y_log_real, color="#A96F2D", alpha=0.85, label="log real wage (PPP)")
plt.plot(x_log_grid, y_log_pred_real, color="black", linewidth=2, label="OLS log-log (PPP)")

# Regression line parameters
intercept_log_real = model_log_real.params["const"]
beta_log_real = model_log_real.params["log_price_level_index"]
r2_log_real = model_log_real.rsquared

text_log_real = (
    f"log(PPP wage) = {intercept_log_real:.2f} + {beta_log_real:.4f} * log(price)\n"
    f"Intercept: {intercept_log_real:.2f}\n"
    f"Coeff: {beta_log_real:.4f}\n"
    f"R²: {r2_log_real:.3f}"
)

plt.text(
    0.05, 0.95,
    text_log_real,
    transform=plt.gca().transAxes,
    fontsize=8,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.7)
)

plt.xlabel("log(price level index)")
plt.ylabel("log(real wage, PPP)")
plt.title("Log-log OLS: log(PPP wage) vs log(price level index)")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "ols_log_ppp_vs_log_price.png"), dpi=300)
plt.show()

# ================================
# D) OLS 2 : log_nominal_wage ~ log_price_level_index
# ================================
X_log_nom = sm.add_constant(x_log)
y_log_nom = df["log_nominal_wage"]
model_log_nom = sm.OLS(y_log_nom, X_log_nom).fit()

# Save regression summary
with open(os.path.join(reg_dir, "ols_log_nominal_vs_log_price.txt"), "w", encoding="utf-8") as f:
    f.write(model_log_nom.summary().as_text())

y_log_pred_nom = model_log_nom.predict(X_log_grid)

plt.figure(figsize=(6, 4))
plt.scatter(x_log, y_log_nom, color="#5D3A00", alpha=0.85, label="log nominal wage")
plt.plot(x_log_grid, y_log_pred_nom, color="black", linewidth=2, label="OLS log-log (nominal)")

# Regression line parameters
intercept_log_nom = model_log_nom.params["const"]
beta_log_nom = model_log_nom.params["log_price_level_index"]
r2_log_nom = model_log_nom.rsquared

text_log_nom = (
    f"log(nominal wage) = {intercept_log_nom:.2f} + {beta_log_nom:.4f} * log(price)\n"
    f"Intercept: {intercept_log_nom:.2f}\n"
    f"Coeff: {beta_log_nom:.4f}\n"
    f"R²: {r2_log_nom:.3f}"
)

plt.text(
    0.05, 0.95,
    text_log_nom,
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
plt.savefig(os.path.join(fig_dir, "ols_log_nominal_vs_log_price.png"), dpi=300)
plt.show()
