import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np


# ================================
# Paths & Load data
# ================================
out_dir = r"C:\Users\aumar\OneDrive\Documents\Python SQL Project Real Wage Level Of Price\csv files"

df = pd.read_csv(
    out_dir + r"\wage_level_by_country.csv",
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

x_log = df["log_price_level_index"]
y_log_real = df["log_ppp_wage"]
y_log_nom = df["log_nominal_wage"]


# ================================
# 1) OLS log real wage (PPP)
# ================================
X_real = sm.add_constant(x_log)
model_real = sm.OLS(y_log_real, X_real).fit()
df["residual_ppp"] = model_real.resid

intercept_real = model_real.params["const"]
beta_real = model_real.params["log_price_level_index"]
r2_real = model_real.rsquared
text_real = (
    f"log(PPP wage) = {intercept_real:.2f} + {beta_real:.4f} * log(price)\n"
    f"Intercept: {intercept_real:.2f}\n"
    f"Slope: {beta_real:.4f}\n"
    f"R²: {r2_real:.3f}"
)

top10_pos_ppp = df.sort_values("residual_ppp", ascending=False).head(10)
top10_neg_ppp = df.sort_values("residual_ppp", ascending=True).head(10)


# ================================
# 2) OLS log nominal wage
# ================================
X_nom = sm.add_constant(x_log)
model_nom = sm.OLS(y_log_nom, X_nom).fit()
df["residual_nominal"] = model_nom.resid

intercept_nom = model_nom.params["const"]
beta_nom = model_nom.params["log_price_level_index"]
r2_nom = model_nom.rsquared
text_nom = (
    f"log(nominal wage) = {intercept_nom:.2f} + {beta_nom:.4f} * log(price)\n"
    f"Intercept: {intercept_nom:.2f}\n"
    f"Slope: {beta_nom:.4f}\n"
    f"R²: {r2_nom:.3f}"
)

top10_pos_nom = df.sort_values("residual_nominal", ascending=False).head(10)
top10_neg_nom = df.sort_values("residual_nominal", ascending=True).head(10)


# ================================
# 3) Common countries
# ================================
common_pos_countries = list(set(top10_pos_ppp["country"]) & set(top10_pos_nom["country"]))
common_neg_countries = list(set(top10_neg_ppp["country"]) & set(top10_neg_nom["country"]))

common_pos = df[df["country"].isin(common_pos_countries)].copy()
common_neg = df[df["country"].isin(common_neg_countries)].copy()

# OLS grid
x_log_grid = np.linspace(x_log.min(), x_log.max(), 100)
X_log_grid = sm.add_constant(x_log_grid)
y_pred_real = model_real.predict(X_log_grid)
y_pred_nom = model_nom.predict(X_log_grid)


# ================================
# A) Common TOP – log real wage (PPP)
# ================================
plt.figure(figsize=(6, 4))
plt.scatter(x_log, y_log_real, color="#CCCCCC", alpha=0.4, label="Other countries")
plt.plot(x_log_grid, y_pred_real, color="black", linewidth=2, label="OLS log-log (PPP)")
plt.scatter(common_pos["log_price_level_index"], common_pos["log_ppp_wage"],
            color="green", alpha=0.9, label="Common TOP")
for _, row in common_pos.iterrows():
    plt.annotate(row["country"],
                 (row["log_price_level_index"], row["log_ppp_wage"]),
                 xytext=(3, 3), textcoords="offset points", fontsize=7, color="green")
plt.text(0.03, 0.97, text_real, transform=plt.gca().transAxes,
         fontsize=8, verticalalignment="top",
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))
plt.xlabel("log(price level index)")
plt.ylabel("log(real wage, PPP)")
plt.title("Countries above the OLS line (both models) – log(PPP wage)")
plt.legend()
plt.tight_layout()
plt.savefig(out_dir + r"\common_top_log_real.png", dpi=300)
plt.show()


# ================================
# B) Common TOP – log nominal wage
# ================================
plt.figure(figsize=(6, 4))
plt.scatter(x_log, y_log_nom, color="#CCCCCC", alpha=0.4, label="Other countries")
plt.plot(x_log_grid, y_pred_nom, color="black", linewidth=2, label="OLS log-log (nominal)")
plt.scatter(common_pos["log_price_level_index"], common_pos["log_nominal_wage"],
            color="green", alpha=0.9, label="Common TOP")
for _, row in common_pos.iterrows():
    plt.annotate(row["country"],
                 (row["log_price_level_index"], row["log_nominal_wage"]),
                 xytext=(3, 3), textcoords="offset points", fontsize=7, color="green")
plt.text(0.03, 0.97, text_nom, transform=plt.gca().transAxes,
         fontsize=8, verticalalignment="top",
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))
plt.xlabel("log(price level index)")
plt.ylabel("log(nominal wage)")
plt.title("Countries above the OLS line (both models) – log(nominal wage)")
plt.legend()
plt.tight_layout()
plt.savefig(out_dir + r"\common_top_log_nominal.png", dpi=300)
plt.show()


# ================================
# C) Common BOTTOM – log real wage (PPP)
# ================================
plt.figure(figsize=(6, 4))
plt.scatter(x_log, y_log_real, color="#CCCCCC", alpha=0.4, label="Other countries")
plt.plot(x_log_grid, y_pred_real, color="black", linewidth=2, label="OLS log-log (PPP)")
plt.scatter(common_neg["log_price_level_index"], common_neg["log_ppp_wage"],
            color="red", alpha=0.9, label="Common BOTTOM")
for _, row in common_neg.iterrows():
    plt.annotate(row["country"],
                 (row["log_price_level_index"], row["log_ppp_wage"]),
                 xytext=(3, 3), textcoords="offset points", fontsize=7, color="red")
plt.text(0.03, 0.97, text_real, transform=plt.gca().transAxes,
         fontsize=8, verticalalignment="top",
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))
plt.xlabel("log(price level index)")
plt.ylabel("log(real wage, PPP)")
plt.title("Countries below the OLS line (both models) – log(PPP wage)")
plt.legend()
plt.tight_layout()
plt.savefig(out_dir + r"\common_bottom_log_real.png", dpi=300)
plt.show()


# ================================
# D) Common BOTTOM – log nominal wage
# ================================
plt.figure(figsize=(6, 4))
plt.scatter(x_log, y_log_nom, color="#CCCCCC", alpha=0.4, label="Other countries")
plt.plot(x_log_grid, y_pred_nom, color="black", linewidth=2, label="OLS log-log (nominal)")
plt.scatter(common_neg["log_price_level_index"], common_neg["log_nominal_wage"],
            color="red", alpha=0.9, label="Common BOTTOM")
for _, row in common_neg.iterrows():
    plt.annotate(row["country"],
                 (row["log_price_level_index"], row["log_nominal_wage"]),
                 xytext=(3, 3), textcoords="offset points", fontsize=7, color="red")
plt.text(0.03, 0.97, text_nom, transform=plt.gca().transAxes,
         fontsize=8, verticalalignment="top",
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.7))
plt.xlabel("log(price level index)")
plt.ylabel("log(nominal wage)")
plt.title("Countries below the OLS line (both models) – log(nominal wage)")
plt.legend()
plt.tight_layout()
plt.savefig(out_dir + r"\common_bottom_log_nominal.png", dpi=300)
plt.show()