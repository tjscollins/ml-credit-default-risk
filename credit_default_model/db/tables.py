from sqlalchemy import text
import pandas as pd

from db.connection import db_connection

def get_raw_tables():
    """
    Retrieve the list of tables containing raw, unprocessed data
    """
    query = text(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' "
            "AND table_name NOT LIKE 'processed/_%' escape '/'"
            "AND table_name NOT LIKE 'features/_%' escape '/';"
    )
    return [
        result[0]
        for result in db_connection.execute(query).fetchall()
    ]

def get_processed_tables():
    """
    Retrieve the list of tables containing preprocessed and cleaned data
    """
    query = text(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' "
            "AND table_name LIKE 'processed/_%' escape '/';"
    )
    return [
        result[0]
        for result in db_connection.execute(query).fetchall()
    ]

def get_feature_tables():
    """
    Retrieve the list of tables containing engineered features for model training
    """
    query = text(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' "
            "AND table_name LIKE 'features/_%' escape '/';"
    )
    return [
        result[0]
        for result in db_connection.execute(query).fetchall()
    ]

ORDERINGS = {
    'processed_application_train': 'SK_ID_CURR',
    'processed_application_test': 'SK_ID_CURR',
    'processed_bureau': 'SK_ID_CURR',
    'processed_bureau_balance': 'SK_BUREAU_ID',
    'processed_previous': 'SK_ID_CURR'
}

def load_table_to_data_frame(table_name: str, order_by='SK_ID_CURR', row_limit=None) -> pd.DataFrame:
    """
    Retrieve the contents of the given table from the relational database and return
    a pandas DataFrame containing the data

    Parameters
    -------------
        table_name (str)
            The name of the table to be retrieved from the relational database

        row_limit (None or int)
            The number of rows to be retreived.  If None, then all rows are retrieved
    
    Returns
    --------------
        data_fram (pd.DataFrame)
            DataFrame containing the data from the relational table
    """

    # order_by_clause = ORDERINGS.get(table_name, "")
    
    # if row_limit is not None:
    #     query = text(f"SELECT * FROM {table_name} {order_by_clause} LIMIT :row_limit;")
    # else:
    #     query = text(f"SELECT * FROM {table_name} {order_by_clause};")
    # executable = db_connection.execute(query, row_limit=row_limit)
    # columns = executable.keys()
    # data = executable.fetchall()

    return pd.read_pickle(f"data/{table_name}.pkl")