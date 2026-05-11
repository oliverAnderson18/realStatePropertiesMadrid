import pandas as pd
import re

df = pd.read_csv("data/properties.csv")

df["title"] = df["title"].str.replace('"', "", regex=False)

df.loc[df["title"].str.contains("ático|atico", case=False, na=False), "property_type"] = "penthouse"
df.loc[df["title"].str.contains("piso|apartamento", case=False, na=False), "property_type"] = "flat"
df.loc[df["title"].str.contains("casa|adosado|chalet|dúplex", case=False, na=False), "property_type"] = "house"
df.loc[df["title"].str.contains("estudio", case=False, na=False), "property_type"] = "studio"

df["rooms"] = df["rooms"].astype(str).str.extract(r"(\d+)")
df["bathrooms"] = df["bathrooms"].astype(str).str.extract(r"(\d+)")
df["square_meters"] = df["square_meters"].astype(str).str.extract(r"(\d+)")
df["floor"] = df["floor"].astype(str).str.extract(r"(\d+)")

df.loc[df["property_type"] == "penthouse", "floor"] = "top floor"

df.loc[
    (df["property_type"] == "house") &
    (df["floor"].isna() | (df["floor"] == "")),
    "floor"
] = "not applicable"

df.loc[
    (df["property_type"] == "flat") &
    (df["floor"].isna() | (df["floor"] == "")),
    "floor"
] = "unknown"

df.to_csv("data/properties_clean.csv", index=False)