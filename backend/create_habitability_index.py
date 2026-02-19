import pandas as pd
import numpy as np

df = pd.read_csv("../nasa_full.csv", comment="#")

required_columns = [
    "pl_orbper",
    "pl_orbsmax",
    "pl_bmasse",
    "pl_eqt",
    "st_teff",
    "st_rad",
    "st_mass",
    "st_lum",
    "pl_rade",
    "pl_insol"
]

df = df[required_columns].dropna()

# Earth reference values
ideal_temp = 288
ideal_radius = 1
ideal_insol = 1

df["temp_score"] = 1 - abs(df["pl_eqt"] - ideal_temp) / ideal_temp
df["radius_score"] = 1 - abs(df["pl_rade"] - ideal_radius) / ideal_radius
df["insol_score"] = 1 - abs(df["pl_insol"] - ideal_insol) / ideal_insol

df[["temp_score", "radius_score", "insol_score"]] = \
    df[["temp_score", "radius_score", "insol_score"]].clip(lower=0)

df["habitability_score"] = (
    0.4 * df["temp_score"] +
    0.3 * df["radius_score"] +
    0.3 * df["insol_score"]
)

df["habitability_label"] = (df["habitability_score"] >= 0.5).astype(int)


df.to_csv("processed_exoplanets.csv", index=False)

print("Processed dataset rebuilt successfully.")
print("Total planets:", len(df))
print("Habitable planets:", df['habitability_label'].sum())
