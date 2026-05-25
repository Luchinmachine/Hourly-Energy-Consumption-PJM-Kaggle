from sqlalchemy import create_engine
import pandas as pd
import numpy as np

from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# conexión
engine = create_engine("postgresql://ds_user:ds_pass@localhost:5432/ds_db")

# cargar datos
df = pd.read_sql("SELECT * FROM features_hourly", engine)
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.sort_values("datetime")

# features y target
features = [
    "hour", "dayofweek", "is_weekend",
    "lag_1", "lag_24", "lag_168",
    "rolling_24", "rolling_168"
]

target = "aep_mw"

# parámetros backtesting
horizon = 24
window_size = 24 * 30
step = 24

# modelos
models = {
    "ridge": Ridge(alpha=1.0),
    "random_forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "xgboost": XGBRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        random_state=42
    )
}

# resultados
results = []

# loop backtesting
for name, model in models.items():
    print(f"Entrenando modelo: {name}")
    
    maes = []
    wapes = []

    for start in range(0, len(df) - window_size - horizon, step):
        
        train = df.iloc[start:start+window_size]
        test = df.iloc[start+window_size:start+window_size+horizon]

        X_train = train[features]
        y_train = train[target]

        X_test = test[features]
        y_test = test[target]

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        # métricas
        mae = np.mean(np.abs(y_test - preds))
        wape = np.sum(np.abs(y_test - preds)) / np.sum(y_test)

        maes.append(mae)
        wapes.append(wape)

    results.append({
        "model": name,
        "mae_mean": np.mean(maes),
        "wape_mean": np.mean(wapes)
    })

# resultados finales
results_df = pd.DataFrame(results)

print("\nResultados comparativos:")
print(results_df)

# guardar en DB
results_df.to_sql("model_comparison", engine, if_exists="replace", index=False)

print("tabla model_comparison guardada")