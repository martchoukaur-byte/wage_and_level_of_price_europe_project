import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np


# =================================
# Load data
# =================================
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

x_log = df["log_price_level_index"]


# =================================
# 1) OLS log real wage (PPP)
# =================================
X_real = sm.add_constant(x_log)
y_real = df["log_ppp_wage"]
model_real = sm.OLS(y_real, X_real).fit()

df["residual_ppp"] = model_real.resid

top_pos_ppp = df.sort_values("residual_ppp", ascending=False).head(10)
top_neg_ppp = df.sort_values("residual_ppp", ascending=True).head(10)

x_log_grid = np.linspace(x_log.min(), x_log.max(), 100)
X_log_grid = sm.add_constant(x_log_grid)
y_pred_real = model_real.predict(X_log_grid)

intercept_real = model_real.params["const"]
beta_real = model_real.params["log_price_level_index"]
r2_real = model_real.rsquared
text_real = (
    f"log(PPP wage) = {intercept_real:.2f} + {beta_real:.4f} * log(price)\n"
    f"Intercept: {intercept_real:.2f}\n"
    f"Slope: {beta_real:.4f}\n"
    f"R²: {r2_real:.3f}"
)

# --- Figure 1: Top 10 positive residuals (log PPP) ---
plt.figure(figsize=(6, 4))
plt.scatter(x_log, y_real, color="#CCCCCC", alpha=0.5, label="Other countries")
plt.plot(x_log_grid, y_pred_real, color="black", linewidth=2, label="OLS log-log (PPP)")

plt.scatter(
    top_pos_ppp["log_price_level_index"],
    top_pos_ppp["log_ppp_wage"],
    color="green",
    alpha=0.9,
    label="Top 10 positive residuals"
)

for _, row in top_pos_ppp.iterrows():
    plt.annotate(
        row["country"],
        (row["log_price_level_index"], row["log_ppp_wage"]),
        xytext=(3, 3),
        textcoords="offset points",
        fontsize=7,
        color="green"
    )

plt.text(
    0.03, 0.97,
    text_real,
    transform=plt.gca().transAxes,
    fontsize=8,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.7)
)

plt.xlabel("log(price level index)")
plt.ylabel("log(real wage, PPP)")
plt.title("Top 10 positive residuals – log(PPP wage) vs log(price level index)")
plt.legend()
plt.tight_layout()
plt.show()


# --- Figure 2: Top 10 negative residuals (log PPP) ---
plt.figure(figsize=(6, 4))
plt.scatter(x_log, y_real, color="#CCCCCC", alpha=0.5, label="Other countries")
plt.plot(x_log_grid, y_pred_real, color="black", linewidth=2, label="OLS log-log (PPP)")

plt.scatter(
    top_neg_ppp["log_price_level_index"],
    top_neg_ppp["log_ppp_wage"],
    color="red",
    alpha=0.9,
    label="Top 10 negative residuals"
)

for _, row in top_neg_ppp.iterrows():
    plt.annotate(
        row["country"],
        (row["log_price_level_index"], row["log_ppp_wage"]),
        xytext=(3, 3),
        textcoords="offset points",
        fontsize=7,
        color="red"
    )

plt.text(
    0.03, 0.97,
    text_real,
    transform=plt.gca().transAxes,
    fontsize=8,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.7)
)

plt.xlabel("log(price level index)")
plt.ylabel("log(real wage, PPP)")
plt.title("Top 10 negative residuals – log(PPP wage) vs log(price level index)")
plt.legend()
plt.tight_layout()
plt.show()


# =================================
# 2) OLS log nominal wage
# =================================
X_nom = sm.add_constant(x_log)
y_nom = df["log_nominal_wage"]
model_nom = sm.OLS(y_nom, X_nom).fit()

df["residual_nominal"] = model_nom.resid

top_pos_nom = df.sort_values("residual_nominal", ascending=False).head(10)
top_neg_nom = df.sort_values("residual_nominal", ascending=True).head(10)

y_pred_nom = model_nom.predict(X_log_grid)

intercept_nom = model_nom.params["const"]
beta_nom = model_nom.params["log_price_level_index"]
r2_nom = model_nom.rsquared
text_nom = (
    f"log(nominal wage) = {intercept_nom:.2f} + {beta_nom:.4f} * log(price)\n"
    f"Intercept: {intercept_nom:.2f}\n"
    f"Slope: {beta_nom:.4f}\n"
    f"R²: {r2_nom:.3f}"
)

# --- Figure 3: Top 10 positive residuals (log nominal) ---
plt.figure(figsize=(6, 4))
plt.scatter(x_log, y_nom, color="#CCCCCC", alpha=0.5, label="Other countries")
plt.plot(x_log_grid, y_pred_nom, color="black", linewidth=2, label="OLS log-log (nominal)")

plt.scatter(
    top_pos_nom["log_price_level_index"],
    top_pos_nom["log_nominal_wage"],
    color="green",
    alpha=0.9,
    label="Top 10 positive residuals"
)

for _, row in top_pos_nom.iterrows():
    plt.annotate(
        row["country"],
        (row["log_price_level_index"], row["log_nominal_wage"]),
        xytext=(3, 3),
        textcoords="offset points",
        fontsize=7,
        color="green"
    )

plt.text(
    0.03, 0.97,
    text_nom,
    transform=plt.gca().transAxes,
    fontsize=8,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.7)
)

plt.xlabel("log(price level index)")
plt.ylabel("log(nominal wage)")
plt.title("Top 10 positive residuals – log(nominal wage) vs log(price level index)")
plt.legend()
plt.tight_layout()
plt.show()


# --- Figure 4: Top 10 negative residuals (log nominal) ---
plt.figure(figsize=(6, 4))
plt.scatter(x_log, y_nom, color="#CCCCCC", alpha=0.5, label="Other countries")
plt.plot(x_log_grid, y_pred_nom, color="black", linewidth=2, label="OLS log-log (nominal)")

plt.scatter(
    top_neg_nom["log_price_level_index"],
    top_neg_nom["log_nominal_wage"],
    color="red",
    alpha=0.9,
    label="Top 10 negative residuals"
)

for _, row in top_neg_nom.iterrows():
    plt.annotate(
        row["country"],
        (row["log_price_level_index"], row["log_nominal_wage"]),
        xytext=(3, 3),
        textcoords="offset points",
        fontsize=7,
        color="red"
    )

plt.text(
    0.03, 0.97,
    text_nom,
    transform=plt.gca().transAxes,
    fontsize=8,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.7)
)

plt.xlabel("log(price level index)")
plt.ylabel("log(nominal wage)")
plt.title("Top 10 negative residuals – log(nominal wage) vs log(price level index)")
plt.legend()
plt.tight_layout()
plt.show()
