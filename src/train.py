import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

PROCESSED_DATA_PATH = "data/processed"
MODEL_PATH = "models/model.pkl"


def create_and_train_model(train: pd.DataFrame):
    """
    Creates and trains a gradient boosting regression model using the provided training data.
    """

    X_cols = ["total_meters", "rooms_count", "floors_count", "floor"]
    y_col = ["price"]
    model = GradientBoostingRegressor()
    model.fit(train[X_cols], train[y_col])

    return model


def main():
    train = pd.read_csv(f"{PROCESSED_DATA_PATH}/train.csv")
    model = create_and_train_model(train)

    joblib.dump(model, MODEL_PATH)


if __name__ == "__main__":
    main()
