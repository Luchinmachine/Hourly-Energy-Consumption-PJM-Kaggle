from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# cargar datos
real = pd.read_sql("SELECT datetime, aep_mw FROM clean_load", engine)
forecast = pd.read_sql("SELECT datetime, yhat FROM forecast_hourly", engine)

# transformar
real["type"] = "real"
real.rename(columns={"aep_mw": "value"}, inplace=True)

forecast["type"] = "forecast"
forecast.rename(columns={"yhat": "value"}, inplace=True)

# concatenar
df = pd.concat([real, forecast], ignore_index=True)

# limpieza final (importante)
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.sort_values("datetime")

# opcional: eliminar duplicados por seguridad
df = df.drop_duplicates(subset=["datetime", "type"])

# guardar
df.to_sql("dashboard_final", engine, if_exists="replace", index=False)

print("tabla lista para Power BI")