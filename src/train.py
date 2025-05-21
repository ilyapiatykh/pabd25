import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

PROCESSED_DATA_PATH = "../data/processed"
MODEL_PATH = '../models/model.pkl'

def load_data():
    train = pd.read_csv(f"{PROCESSED_DATA_PATH}/train.csv")

def create_and_train_model(train: pd.DataFrame):
    X_cols = ['total_meters', "rooms_count", "floors_count", "floor"]
    y_col = ["price"]
    model = LinearRegression()
    model.fit(train[X_cols], train[y_col])

    return model

def main():
    train = pd.read_csv(f"{PROCESSED_DATA_PATH}/train.csv")
    model = create_and_train_model(train)

    joblib.dump(model, MODEL_PATH)


if __name__ == '__main__':
    main()
