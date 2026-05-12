from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

input_path = BASE_DIR / "data" / "properties.csv"
output_path = BASE_DIR / "data" / "properties_clean.csv"

df = pd.read_csv(input_path)

df["title"] = df["title"].str.replace('"', "", regex=False)

df.loc[df["title"].str.contains("ático|atico", case=False, na=False), "property_type"] = "penthouse"
df.loc[df["title"].str.contains("piso|apartamento", case=False, na=False), "property_type"] = "flat"
df.loc[df["title"].str.contains("casa|adosado|chalet|dúplex", case=False, na=False), "property_type"] = "house"
df.loc[df["title"].str.contains("estudio", case=False, na=False), "property_type"] = "studio"
df.loc[df["floor"].astype(str).str.contains("bajo", case=False, na=False), "property_type"] = "ground-floor apartment"

df["rooms"] = df["rooms"].astype(str).str.extract(r"(\d+)")
df["bathrooms"] = df["bathrooms"].astype(str).str.extract(r"(\d+)")
df["square_meters"] = df["square_meters"].astype(str).str.extract(r"(\d+)")

floor_numbers = df["floor"].astype(str).str.extract(r"(\d+)")
df["floor"] = floor_numbers.fillna("")

df.loc[df["property_type"] == "penthouse", "floor"] = "top floor"
df.loc[df["property_type"] == "ground-floor apartment", "floor"] = "ground floor"

df.loc[(df["property_type"] == "house") & (df["floor"] == ""), "floor"] = "not applicable"
df.loc[(df["property_type"] == "flat") & (df["floor"] == ""), "floor"] = "unknown"

df.to_csv(output_path, index=False)