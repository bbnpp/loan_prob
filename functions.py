import pandas as pd
import numpy as np


def has_pk(data:pd.DataFrame):
    for col in data.columns:
        if data[col].nunique() == data.shape[0]:
            print(f'primary_key: {col}')
            return
    print('pk is not found')
    

def check_null_status(data:pd.DataFrame):
    n = data.shape[0]
    count_null = data.isnull().sum()
    null_ratio = (count_null / n).sort_values(ascending=False)
    return null_ratio


def search_categoric(data:pd.DataFrame, cardinality_limit=10):
    return [col for col in data if data[col].nunique() < cardinality_limit]


def aggregate_numeric(data:pd.DataFrame, primary_key, drop_cols):
    aggregated = (data.drop(drop_cols, axis=1)
                      .groupby(primary_key)
                      .agg([np.nanmean, np.nanstd, len]))
    aggregated.columns = ['_'.join(col).strip() for col in aggregated.columns.values]
    return aggregated


# def aggregate_categoric

    