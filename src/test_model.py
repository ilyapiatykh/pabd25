#pyright: reportCallIssue=false, reportArgumentType=false
import json

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

PROCESSED_DATA_PATH = "../data/processed"
MODEL_PATH = '../models/model.pkl'
METRICS_FILE = 'metrics.json'

# def get_feature_coefficients(model, feature_names):
#     coefficients = pd.DataFrame({
#         'Feature': feature_names,
#         'Coefficient': model.coef_,
#         'Absolute_Impact': np.abs(model.coef_)
#     }).sort_values('Absolute_Impact', ascending=False)

#     return coefficients

def evaluate_model(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    metrics = {
        'MAE': round(mae, 4),
        'MSE': round(mse, 4),
        'RMSE': round(rmse, 4),
        'R²': round(r2, 4),
    }

    return metrics

def main():
    test = pd.read_csv(f"{PROCESSED_DATA_PATH}/test.csv")

    model = joblib.load(MODEL_PATH)

    X_cols = ['total_meters', "rooms_count", "floors_count", "floor"]
    y_col = ["price"]

    y_pred = model.predict(test[X_cols])

    metrics = evaluate_model(test[y_col], y_pred)

    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=4)

if __name__ == '__main__':
    main()
