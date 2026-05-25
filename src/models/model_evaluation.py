from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from xgboost import XGBRegressor

from src.utils.db import get_engine

engine = get_engine()

df = pd.read_sql("SELECT * FROM features_hourly", engine)
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.sort_values("datetime")

features = ["hour", "dayofweek", "is_weekend", 
            "lag_1", "lag_24", "lag_168", 
            "rolling_24", "rolling_168"]

target = "aep_mw"

horizon = 24
window_size = 24 * 30
step = 24

all_results = []

for start in range(0, len(df) - window_size - horizon, step):
    
    train = df.iloc[start:start+window_size]
    test = df.iloc[start+window_size:start+window_size+horizon]

    X_train = train[features]
    y_train = train[target]

    X_test = test[features]
    y_test = test[target]

    model = XGBRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    temp = pd.DataFrame({
        "datetime": test["datetime"],
        "real": y_test,
        "forecast": preds
    })

    temp["error"] = temp["real"] - temp["forecast"]
    temp["abs_error"] = np.abs(temp["error"])

    all_results.append(temp)

# unir todo
results_df = pd.concat(all_results)

# guardar en SQL
results_df.to_sql("model_evaluation", engine, if_exists="replace", index=False)

print("tabla model_evaluation lista")