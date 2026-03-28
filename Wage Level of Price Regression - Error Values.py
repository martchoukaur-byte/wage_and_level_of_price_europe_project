import pandas as pd
import statsmodels.api as sm
import numpy as np
import os


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


# ================================
# 1) Log-log OLS: real wage (PPP)
# ================================
X_real = sm.add_constant(df["log_price_level_index"])
y_real = df["log_ppp_wage"]
model_real = sm.OLS(y_real, X_real).fit()
df["residual_ppp"] = model_real.resid

top10_pos_ppp = df.sort_values("residual_ppp", ascending=False).head(10).reset_index(drop=True)
top10_neg_ppp = df.sort_values("residual_ppp", ascending=True).head(10).reset_index(drop=True)


# ================================
# 2) Log-log OLS: nominal wage
# ================================
X_nom = sm.add_constant(df["log_price_level_index"])
y_nom = df["log_nominal_wage"]
model_nom = sm.OLS(y_nom, X_nom).fit()
df["residual_nominal"] = model_nom.resid

top10_pos_nom = df.sort_values("residual_nominal", ascending=False).head(10).reset_index(drop=True)
top10_neg_nom = df.sort_values("residual_nominal", ascending=True).head(10).reset_index(drop=True)


# ================================
# 3) Common countries (real AND nominal)
# ================================
common_pos_countries = list(set(top10_pos_ppp["country"]) & set(top10_pos_nom["country"]))
common_neg_countries = list(set(top10_neg_ppp["country"]) & set(top10_neg_nom["country"]))

common_pos = (
    df[df["country"].isin(common_pos_countries)][["country", "residual_ppp", "residual_nominal"]]
    .sort_values("residual_ppp", ascending=False)
    .reset_index(drop=True)
)
common_neg = (
    df[df["country"].isin(common_neg_countries)][["country", "residual_ppp", "residual_nominal"]]
    .sort_values("residual_ppp", ascending=True)
    .reset_index(drop=True)
)


# ================================
# 4) Display tables
# ================================
pd.set_option("display.float_format", "{:.4f}".format)
pd.set_option("display.max_rows", 20)
pd.set_option("display.width", 100)

tables = {
    "1) Top 10 ABOVE the line – LOG REAL WAGE (PPP)":
        top10_pos_ppp[["country", "residual_ppp"]],
    "2) Top 10 BELOW the line – LOG REAL WAGE (PPP)":
        top10_neg_ppp[["country", "residual_ppp"]],
    "3) Top 10 ABOVE the line – LOG NOMINAL WAGE":
        top10_pos_nom[["country", "residual_nominal"]],
    "4) Top 10 BELOW the line – LOG NOMINAL WAGE":
        top10_neg_nom[["country", "residual_nominal"]],
    "5) Common countries ABOVE the line – BOTH real and nominal":
        common_pos,
    "6) Common countries BELOW the line – BOTH real and nominal":
        common_neg,
}

for title, tbl in tables.items():
    print(f"\n=== {title} ===")
    print(tbl.to_string(index=True))


# ================================
# 5) Export CSV
# ================================
out_dir = r"C:\Users\aumar\OneDrive\Documents\Python SQL Project Real Wage Level Of Price\csv files"

export_map = {
    "residuals_log_ppp_top10_pos.csv":      top10_pos_ppp[["country", "residual_ppp"]],
    "residuals_log_ppp_top10_neg.csv":      top10_neg_ppp[["country", "residual_ppp"]],
    "residuals_log_nominal_top10_pos.csv":  top10_pos_nom[["country", "residual_nominal"]],
    "residuals_log_nominal_top10_neg.csv":  top10_neg_nom[["country", "residual_nominal"]],
    "residuals_log_common_top10_pos.csv":   common_pos,
    "residuals_log_common_top10_neg.csv":   common_neg,
}

for filename, tbl in export_map.items():
    tbl.to_csv(os.path.join(out_dir, filename), index=False)
    print(f"Saved: {filename}")

print("\nAll CSV files saved to:", out_dir)