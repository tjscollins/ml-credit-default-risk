import numpy as np
import pandas as pd

def remove_days_employed_outliers(data_frame: pd.DataFrame, table_name):
    """
    Removes anomalous DAYS_EMPLOYED quantity by replacing with NaN and adding a
    column that indicates this operation was performed.  This allows the model
    to treat the anomalous value differently from the non-anomalous values.
    """
    print('Addressing anomalous days of employment in %s' % table_name)
    anom = data_frame[data_frame['DAYS_EMPLOYED'] == 365243]
    non_anom = data_frame[data_frame['DAYS_EMPLOYED'] != 365243]

    print('There are %d anomalous days of employment in %s' % (len(anom), table_name))

    data_frame['DAYS_EMPLOYED_ANOM'] = data_frame['DAYS_EMPLOYED'] == 365243
    data_frame['DAYS_EMPLOYED'].replace({ 365243: np.nan }, inplace=True)

    return data_frame

def handle_outliers(data_frame, table_name):
    """
    Applies the handler_methods to a data frame if that data frame comes
    from the matching table_name the handler methods are assigned to.  This
    allows us to define handler methods for each data table based on manually
    identified outliers that we may wish to treat.
    """
    handler_methods = {
        'application_test': [remove_days_employed_outliers],
        'application_train': [remove_days_employed_outliers]
    }

    print(
        f"\n  Handling Outliers for {table_name}\n"
        f"  _________________________________________________\n"
    )

    for method in handler_methods.get(table_name, []):
        data_frame = method(data_frame, table_name)
    
    return data_frame