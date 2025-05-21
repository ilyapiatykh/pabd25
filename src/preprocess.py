#pyright: reportCallIssue=false
import os

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = "../data/raw"
PROCESSED_DATA_PATH = "../data/processed"

def concat_data() -> pd.DataFrame:
    files = os.listdir(RAW_DATA_PATH)[:3]

    dfs = []
    for file in files:
        df = pd.read_csv(f"{RAW_DATA_PATH}/{file}")
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)

    return df

def remove_outliers_iqr(df, column, threshold=1.5):
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
    labels_to_drop = [
        'location',
        'deal_type',
        'accommodation_type',
        'price_per_month',
        'commissions',
        'url',
        'author',
        'author_type',
        'residential_complex',
    ]

    df.drop(labels_to_drop, axis=1, inplace=True)

    cols = ["floor",	"floors_count",	"total_meters"]

    for col in cols:
        remove_outliers_iqr(df, col)


def split_data(df: pd.DataFrame):
    X = df[['total_meters', "rooms_count", "floors_count", "floor"]]
    y = df['price']
    train, test = train_test_split(X, y, test_size=0.2, random_state=42)

    return train, test

def main():
    df = concat_data()
    transform_data(df)

    train, test = split_data(df)

    train.to_csv(f"{PROCESSED_DATA_PATH}/train.csv")
    test.to_csv(f"{PROCESSED_DATA_PATH}/test.csv")

if __name__ == '__main__':
    main()
