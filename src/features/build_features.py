from sqlalchemy import create_engine
import pandas as pd

# Conexion y carga
engine = create_engine("postgresql://ds_user:ds_pass@localhost:5432/ds_db")

# cargar clean
df = pd.read_sql("SELECT * FROM clean_load", engine)

df["datetime"] = pd.to_datetime(df["datetime"])
df = df.sort_values("datetime")

# Features de tiempo
df["hour"] = df["datetime"].dt.hour
df["dayofweek"] = df["datetime"].dt.dayofweek
df["is_weekend"] = df["dayofweek"].isin([5,6]).astype(int)

# Lag features
df["lag_1"] = df["aep_mw"].shift(1)
df["lag_24"] = df["aep_mw"].shift(24)
df["lag_168"] = df["aep_mw"].shift(168)

# Rolling features
df["rolling_24"] = df["aep_mw"].shift(1).rolling(24).mean()
df["rolling_168"] = df["aep_mw"].shift(1).rolling(168).mean()

# Eliminar filas con NA
df = df.dropna()

# Guardar en SQL
df.to_sql("features_hourly", engine, if_exists="replace", index=False)

print("features_hourly lista")