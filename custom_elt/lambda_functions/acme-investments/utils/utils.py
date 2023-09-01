import pandas as pd
import re


def standardize_columns(df):
    def clean_column_name(col_name):
        cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', col_name)
        cleaned = re.sub(r'_+', '_', cleaned)
        cleaned = cleaned.strip('_')
        return cleaned

    new_columns = [clean_column_name(col) for col in df.columns]

    df.columns = new_columns

    return df
