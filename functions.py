import pandas as pd
import numpy as np
from scipy import stats


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


def aggregate_numerical(data:pd.DataFrame, drop_cols):
    aggregated = (data.select_dtypes(exclude='object')
                      .drop(drop_cols, axis=1)
                      .groupby(level=0)
                      .agg([np.nanmean, np.nanstd, len]))
    aggregated.columns = ['_'.join(col).strip() for col in aggregated.columns.values]
    return aggregated


def aggregate_categorical(data:pd.DataFrame):
    aggregated = (data.select_dtypes(include='object')
                      .groupby(level=0)
                      .agg([min, max])
                 )
    aggregated.columns = ['_'.join(col).strip() for col in aggregated.columns.values]
    return aggregated


def aggregate(data:pd.DataFrame, primary_key, drop_cols):
    data.set_index(primary_key, inplace=True)
    numerical = aggregate_numerical(data, drop_cols)
    
    categorical_columns = data.select_dtypes(include='object').columns
    if len(categorical_columns) > 0:
        categorical = aggregate_categorical(data)
        return pd.concat([numerical, categorical], axis=1, join='inner')
    else:
        return numerical
    