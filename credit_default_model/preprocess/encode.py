"""
Handles encoding of categorical variables
"""
from typing import Tuple

import pandas as pd
from sklearn.preprocessing import LabelEncoder

def encode_vars(data_frame: pd.DataFrame, encoding_type='one-hot', columns=None) -> pd.DataFrame:
    """
    Encode categorical variables using either one-hot or label encoding.
    Defaults to one-hot.

    Paramters
    ---------------
        data_frame (pd.DataFrame)
            Data frame with categorical variables that need encoding

        encoding_type (str)
            One of 'one-hot' or 'label-encoding'

        columns (NoneType or List[str])
            List of columns to be encoded.  If None, all 'object' type columns
            will be encoded.

    Return
    ----------------
        data_frame (pd.DataFrame)
            New data frame with categorical variables stored in the desired encoding
    """
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

def align_data(training_data: pd.DataFrame, test_data: pd.DataFrame, preserve=['TARGET']) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Align the data between a training_data set and a test_data set while
    preserving all columns specified by preserve in the training_data.

    Parameters
    ------------------
        training_data (pd.DataFrame)
            data frame of the training features.  Must include the columns 
            specified by the value of preserve
        
        test_data (pd.DataFrame)
            corresponding data frame of the test data
        
        preserve (List[str])
            list of columns from training_data to be preserved and restored
            after the data frames are aligned
    
    Return
    -------------------
        aligned_training_data (pd.DataFrame)
            training_data aligned with test_data and columns specified by 
            preserve
        
        aligned_test_data (pd.DataFrame)
            test_data aligned with training_data

    """
    print(f"Aligning training and test data before combining for feature engineering:")

    preserved_features = training_data[preserve]
    aligned_training_data, aligned_test_data = training_data.align(test_data, join='inner', axis=1)

    aligned_training_data[preserve] = preserved_features

    print(f"  Aligned data has shape {aligned_training_data.shape}")

    return aligned_training_data, aligned_test_data
