import os

import pandas as pd
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"


def concat_data() -> pd.DataFrame:
    """
    Concatenates multiple CSV files from the raw data directory into a single DataFrame.
    """

    files = os.listdir(RAW_DATA_PATH)[:3]

    dfs = []
    for file in files:
        df = pd.read_csv(f"{RAW_DATA_PATH}/{file}")
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)

    return df


def remove_outliers_iqr(df: pd.DataFrame, column: str, threshold: float = 1.5):
    """
    Removes outliers from a DataFrame using the IQR method.
    """

    if column not in df.columns:
        raise ValueError(f"Column '{column}' doesn't exist in DataFrame.")

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR

    filtered_df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    return filtered_df.reset_index(drop=True)


def transform_data(df: pd.DataFrame):
    """
    Transforms the DataFrame by cleaning and removing unnecessary columns,
    handling missing values, and removing outliers.
    """

    labels_to_drop = [
        "location",
        "deal_type",
        "accommodation_type",
        "price_per_month",
        "commissions",
        "url",
        "author",
        "author_type",
        "residential_complex",
    ]

    df.drop(labels_to_drop, axis=1, inplace=True)

    cols = ["floor", "floors_count", "total_meters"]

    for col in cols:
        remove_outliers_iqr(df, col)


def split_data(df: pd.DataFrame):
    """
    Splits the DataFrame into training and testing sets.
    """

    features = ["total_meters", "rooms_count", "floors_count", "floor"]
    target = "price"

    X = df[features]
    y = df[target]
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    train = pd.concat([x_train.reset_index(drop=True), y_train.reset_index(drop=True)], axis=1)
    train.columns = features + [target]

    test = pd.concat([x_test.reset_index(drop=True), y_test.reset_index(drop=True)], axis=1)
    test.columns = train.columns

    return train, test


def main():
    df = concat_data()
    transform_data(df)

    train, test = split_data(df)

    train.to_csv(f"{PROCESSED_DATA_PATH}/train.csv")
    test.to_csv(f"{PROCESSED_DATA_PATH}/test.csv")


if __name__ == "__main__":
    main()
