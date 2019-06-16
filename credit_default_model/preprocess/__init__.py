from sqlalchemy import text
import pandas as pd

from db import db_connection

from .encode import encode_vars
from load import save_data_frame

def clean_data(*args, **kwargs):
    query = text(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' "
            "AND table_name NOT LIKE 'processed/_%' escape '/'"
            "AND table_name NOT LIKE 'features/_%' escape '/';"
    )
    tables = db_connection.execute(query).fetchall()

    for table_name in tables:
        table_name = table_name[0]
        query = text(
            f"SELECT * FROM {table_name};"
        )
        executable = db_connection.execute(query)
        columns = executable.keys()
        data = executable.fetchall()

        data_frame = pd.DataFrame(data, columns=columns)

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

        save_data_frame(encoded_data_frame, f"processed_{table_name}")
