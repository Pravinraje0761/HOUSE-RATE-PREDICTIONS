"""Train and evaluate the house-price models, and save the one the app uses.

One scikit-learn Pipeline holds every preprocessing step (imputation, scaling, encoding),
so training and the Streamlit app transform inputs identically, and every step is fitted on
the training split only. No feature is derived from the price.

    python train.py            # writes models/house_price_pipeline.joblib and models/metrics.json
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "dataset" / "house_data.csv"
MODELS = ROOT / "models"
SEED = 42

NUMERIC = ["Area", "Number_of_Bedrooms", "Number_of_Bathrooms", "Number_of_Floors", "Parking",
           "Age_of_House", "Distance_to_City_Center", "Nearby_Schools", "Nearby_Hospitals"]
ORDINAL = {"Furnishing_Status": ["Unfurnished", "Semi-Furnished", "Furnished"],
           "Crime_Rate": ["Low", "Medium", "High"]}
NOMINAL = ["Location", "City", "Property_Type"]
FEATURES = NUMERIC + list(ORDINAL) + NOMINAL
TARGET = "Price"


def make_preprocessor() -> ColumnTransformer:
    return ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                          ("scale", StandardScaler())]), NUMERIC),
        ("ord", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("encode", OrdinalEncoder(categories=list(ORDINAL.values()),
                                                    handle_unknown="use_encoded_value",
                                                    unknown_value=-1))]), list(ORDINAL)),
        ("nom", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("encode", OneHotEncoder(handle_unknown="ignore"))]), NOMINAL),
    ])


def candidate_models() -> dict[str, object]:
    return {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=SEED),
        "Random Forest": RandomForestRegressor(n_estimators=200, random_state=SEED, n_jobs=-1),
    }


def build_input_frame(rows: list[dict] | dict) -> pd.DataFrame:
    """Raw feature rows (one dict per house) in the column order the pipeline expects."""
    rows = [rows] if isinstance(rows, dict) else rows
    return pd.DataFrame(rows).reindex(columns=FEATURES)


def load_data(path: Path = DATA) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(path)
    df = df.dropna(subset=[TARGET])
    return df[FEATURES], df[TARGET]


def evaluate(X: pd.DataFrame, y: pd.Series) -> tuple[dict, dict]:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)
    results, fitted = {}, {}
    for name, model in candidate_models().items():
        pipe = Pipeline([("prep", make_preprocessor()), ("model", model)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        cv = cross_val_score(Pipeline([("prep", make_preprocessor()), ("model", model)]),
                             X_train, y_train, cv=5, scoring="r2")
        results[name] = {
            "test_r2": round(float(r2_score(y_test, pred)), 4),
            "test_mae": round(float(mean_absolute_error(y_test, pred)), 0),
            "test_rmse": round(float(np.sqrt(mean_squared_error(y_test, pred))), 0),
            "cv_r2_mean": round(float(cv.mean()), 4),
            "cv_r2_std": round(float(cv.std()), 4),
        }
        fitted[name] = pipe
    return results, fitted


def main() -> None:
    X, y = load_data()
    results, fitted = evaluate(X, y)
    best = max(results, key=lambda n: results[n]["cv_r2_mean"])  # chosen on CV, not on test
    MODELS.mkdir(exist_ok=True)
    joblib.dump(fitted[best], MODELS / "house_price_pipeline.joblib")
    metrics = {"selected_model": best, "n_rows": int(len(y)), "split": "80/20, seed 42",
               "models": results}
    (MODELS / "metrics.json").write_text(json.dumps(metrics, indent=2))

    print(f"{'Model':<18} {'Test R²':>8} {'MAE ($)':>10} {'RMSE ($)':>10} {'CV R² (5-fold)':>16}")
    for name, r in results.items():
        print(f"{name:<18} {r['test_r2']:>8.4f} {r['test_mae']:>10,.0f} {r['test_rmse']:>10,.0f} "
              f"{r['cv_r2_mean']:>9.4f} ± {r['cv_r2_std']:.4f}")
    print(f"\nSaved {best} pipeline to models/house_price_pipeline.joblib")


if __name__ == "__main__":
    main()
