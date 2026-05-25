from sqlalchemy import create_engine
import pandas as pd
from xgboost import XGBRegressor

engine = create_engine("postgresql://ds_user:ds_pass@localhost:5432/ds_db")

# cargar features
df = pd.read_sql("SELECT * FROM features_hourly", engine)
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.sort_values("datetime")

features = ["hour", "dayofweek", "is_weekend", 
            "lag_1", "lag_24", "lag_168", 
            "rolling_24", "rolling_168"]

target = "aep_mw"

# entrenar con TODOS los datos históricos
train = df.copy()

X_train = train[features]
y_train = train[target]

model = XGBRegressor(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    random_state=42
)

model.fit(X_train, y_train)

# ----------------------------
# GENERAR FUTURO (24 horas)
# ----------------------------
last_date = df["datetime"].max()

future_dates = pd.date_range(
    start=last_date + pd.Timedelta(hours=1),
    periods=24,
    freq="h"
)

future_df = pd.DataFrame({"datetime": future_dates})

# features de calendario
future_df["hour"] = future_df["datetime"].dt.hour
future_df["dayofweek"] = future_df["datetime"].dt.dayofweek
future_df["is_weekend"] = future_df["dayofweek"].isin([5,6]).astype(int)

# usar últimos valores para lags
for lag in [1, 24, 168]:
    future_df[f"lag_{lag}"] = df["aep_mw"].iloc[-lag]

# rolling aproximado (simplificado)
future_df["rolling_24"] = df["aep_mw"].iloc[-24:].mean()
future_df["rolling_168"] = df["aep_mw"].iloc[-168:].mean()

# predecir
future_df["yhat"] = model.predict(future_df[features])

print(future_df.head())

# guardar predicciones
future_df.to_sql("forecast_hourly", engine, if_exists="replace", index=False)

# importancia de features
importance = model.feature_importances_

feat_imp = pd.DataFrame({
    "feature": features,
    "importance": importance
}).sort_values(by="importance", ascending=False)

print(feat_imp)