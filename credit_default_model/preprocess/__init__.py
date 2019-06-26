from sqlalchemy import text
import pandas as pd

from load import save_data_frame, TABLES
from preprocess.encode import encode_vars
from preprocess.clean import run_cleaners

def clean_data(*args, **kwargs):
    """
    Apply data cleaning logic to raw data tables and store them in processed_
    data tables.
    """
    for table_name in TABLES:
        data_frame = pd.read_pickle(f"data/{table_name}.pkl")

        print(
            f"Preprocessing data from {table_name} with shape {data_frame.shape}\n"
            f"Data has the following categorical variables: \n\n"
            f"{data_frame.select_dtypes('object').apply(pd.Series.nunique, axis=0)}\n"
        )

        labelable_columns = [
            column_name for column_name in data_frame.columns
            if data_frame[column_name].dtype == 'object' \
                and len(list(data_frame[column_name].unique())) <= 2
        ]

        encoded_data_frame = encode_vars(
            data_frame,
            encoding_type='label-encoding',
            columns=labelable_columns
        )

        print(
            f"After applying label encoding to categorical values with 2 or fewer values, the data in {table_name} has shape {encoded_data_frame.shape}\n"
            f"Data has the remaining categorical variables: \n\n"
            f"{encoded_data_frame.select_dtypes('object').apply(pd.Series.nunique, axis=0)}\n"
        )

        encoded_data_frame = encode_vars(encoded_data_frame)

        print(
            f"After default one-hot encoding the data in {table_name} has shape {encoded_data_frame.shape}\n"
            f"Cleaned data has the remaining categorical variables: \n\n"
            f"{encoded_data_frame.select_dtypes('object').apply(pd.Series.nunique, axis=0)}\n"
        )

        cleaned_data_frame = run_cleaners(encoded_data_frame, table_name)

        save_data_frame(cleaned_data_frame, f"processed_{table_name}")
