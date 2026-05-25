# ⚡ Energy Load Forecasting (End-to-End Data Science Project)

## 📌 Overview

Este proyecto consiste en el desarrollo de una solución end-to-end de forecasting de demanda eléctrica horaria, simulando un caso real de planificación energética.

El objetivo es predecir el consumo eléctrico a corto plazo (24h) para apoyar la toma de decisiones operativas, reduciendo costos asociados a sobre/infra estimación de demanda.

---

## 🧠 Problem Statement

En industrias como energía, una predicción precisa de la demanda es clave para:

* Optimizar la generación eléctrica
* Reducir costos operacionales
* Evitar sobrecarga o déficit de suministro

Este proyecto aborda el problema de predecir consumo eléctrico horario utilizando datos históricos.

---

## 🏗️ Architecture

Pipeline implementado:

```
Raw Data → Cleaning → Feature Engineering → Modeling → Forecast → Database → Visualization
```

---

## ⚙️ Tech Stack

* **Python** (pandas, numpy, scikit-learn, XGBoost)
* **PostgreSQL** (almacenamiento de datos)
* **Docker** (infraestructura reproducible)
* **Power BI** (visualización)
* **SQLAlchemy** (conexión Python-DB)

---

## 📊 Data

Dataset: [Hourly Energy Consumption (PJM) — Kaggle](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption)

* Fuente: PJM Interconnection LLC (AEP region)
* Frecuencia: Horaria
* Variable objetivo: consumo eléctrico (MW)
* Periodo: histórico multianual

> El archivo CSV no está incluido en el repositorio. Descargarlo desde el enlace anterior y colocarlo en `data/raw/AEP_hourly.csv`.

---

## 🧹 Data Processing

Se implementaron procesos de:

* Normalización de timestamps
* Eliminación de duplicados
* Reconstrucción de frecuencia horaria
* Imputación de valores faltantes

Arquitectura de datos:

* `raw_load`: datos originales
* `clean_load`: datos limpios
* `features_hourly`: dataset con features

---

## 🧬 Feature Engineering

Se construyeron features específicas para series de tiempo:

### Variables de calendario

* Hora del día
* Día de la semana
* Indicador fin de semana

### Variables autoregresivas

* Lag 1, 24 y 168 horas

### Estadísticas móviles

* Media móvil 24h y 168h

---

## 🤖 Modeling Approach

Se utilizó un enfoque **Champion–Challenger**:

### Champion

* Seasonal Naive (lag 168)

### Challenger

* XGBoost Regressor

Evaluación mediante **backtesting temporal (rolling window)**.

---

## 📈 Results

| Modelo         | WAPE |
| -------------- | ---- |
| Seasonal Naive | 8.6% |
| XGBoost        | 1.5% |

El modelo XGBoost logró capturar patrones no lineales y mejorar significativamente el baseline.

---

## 🔮 Forecasting

Se generaron predicciones para las próximas 24 horas utilizando el modelo entrenado, simulando un escenario de producción.

Los resultados se almacenan en la tabla:

* `forecast_hourly`

---

## 📊 Visualization

Se desarrolló un dashboard en Power BI con:

* Comparación Real vs Forecast
* Análisis de error
* Patrones de consumo

---

## 🚀 How to Run

### 1. Clonar el repositorio y configurar entorno

```bash
git clone <repo-url>
cd proyectds-energy

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con las credenciales de tu base de datos PostgreSQL
```

### 3. Obtener el dataset

Descargar el archivo `AEP_hourly.csv` desde [Kaggle](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption) y colocarlo en `data/raw/AEP_hourly.csv`.

### 4. Levantar PostgreSQL

```bash
docker run --name ds_db -e POSTGRES_USER=ds_user -e POSTGRES_PASSWORD=ds_pass \
  -e POSTGRES_DB=ds_db -p 5432:5432 -d postgres
```

### 5. Ejecutar el pipeline

```bash
python src/data/docker_clean_data.py   # Carga y limpia datos → PostgreSQL
python src/features/build_features.py  # Genera features
python src/models/train_model.py       # Entrena modelo y genera forecast
python src/data/prep_table_bi.py       # Prepara tabla para visualización
```

---

## 🧠 Key Learnings

* Implementación de pipelines end-to-end
* Manejo de series de tiempo
* Evaluación con backtesting
* Uso de modelos baseline vs avanzados
* Integración de datos y visualización

---

## 📌 Future Improvements

* Forecast multi-step (iterativo)
* Incorporación de variables exógenas (clima)
* Modelos probabilísticos (intervalos de confianza)
* Automatización con Airflow/Dagster

---

## 👤 Author

Luis Altamirano
Data Scientist
