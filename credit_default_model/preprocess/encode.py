"""
Handles encoding of categorical variables
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder

def encode_vars(data_frame: pd.DataFrame, encoding_type='one-hot', columns=None) -> pd.DataFrame:
    type_counts = data_frame.dtypes.value_counts()
    all_object_columns = type_counts[type_counts.index == 'object'][0]

    if encoding_type == 'one-hot':
        print(
            f"Applying one-hot encoding of object dtypes in data frame to "
            f"{all_object_columns if columns is None else len(columns)} columns"
        )
        return pd.get_dummies(data_frame, columns=columns)

    if encoding_type == 'label-encoding':
        print(f"Applying label encoding of object dtypes in data frame to {all_object_columns if columns is None else len(columns)} columns")
        le = LabelEncoder()
        le_count = 0
        for col in columns if columns is not None else data_frame:
            if data_frame[col].dtype == 'object':
                data_frame[col] = le.fit_transform(data_frame[col])
                le_count += 1
        
        return data_frame

    raise ValueError(f"encoding_type must be one of ['one-hot', 'label-encoding'].  Received {encoding_type}")