from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# leer data
df = pd.read_csv("./data/raw/AEP_hourly.csv")

# renombrar columnas
df = df.rename(columns={"Datetime": "datetime", "AEP_MW": "aep_mw"})

# ---- 1. RAW ----
df.to_sql("raw_load", engine, if_exists="replace", index=False)
print("raw_load lista")

# ---- 2. CLEAN ----
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.sort_values("datetime")

# eliminar duplicados (promedio por hora)
df = df.groupby("datetime", as_index=False)["aep_mw"].mean()

# completar rango horario
full_range = pd.date_range(df["datetime"].min(), df["datetime"].max(), freq="h")
df = df.set_index("datetime").reindex(full_range)
df.index.name = "datetime"

# interpolar faltantes
df["aep_mw"] = df["aep_mw"].interpolate(method="time")

df = df.reset_index()

# guardar clean
df.to_sql("clean_load", engine, if_exists="replace", index=False)

print("clean_load lista")

