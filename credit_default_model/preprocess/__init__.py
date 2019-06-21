from sqlalchemy import text
import pandas as pd

from db import db_connection
from db.tables import get_raw_tables, load_table_to_data_frame
from load import save_data_frame
from preprocess.encode import encode_vars
from preprocess.cleaners import run_cleaners

def clean_data(*args, **kwargs):
    """
    Apply data cleaning logic to raw data tables and store them in processed_
    data tables.
    """
    for table_name in get_raw_tables():
        data_frame = load_table_to_data_frame(table_name)

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
