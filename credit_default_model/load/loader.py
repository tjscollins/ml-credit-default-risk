from typing import List, Dict
import glob
import re
import time

from sqlalchemy import text 
import pandas as pd

TABLES = [
    "application_test",
    "application_train",
    "bureau_balance",
    "bureau",
    "previous_application"
]

DATA_FILES = [f"data/{table}.csv" for table in TABLES]

def load_data(*args, **kwargs):
    """
    Parse CSV data supplied from external sources and load it into the
    relational database.  CSV files will be sourced from the data/ directory
    and loaded as a pandas DataFrame before being passed to save_data_frame
    along with a table_name derived from the file's basename.
    """
    print(f"Loading data from data/ directory to relational database...")
    table_name_regex = re.compile('(\w+)\.csv$')

    print(f"  Will load the following files: ")
    for filename in DATA_FILES:
        print(f"    {filename}")

    for filename in DATA_FILES:
        match = table_name_regex.search(filename)
        if match is None:
            continue
        
        table_name = match.groups()[0]
        data = pd.read_csv(filename)
        save_data_frame(data, table_name)

def save_data_frame(data_frame: pd.DataFrame, table_name: str, index_col_pattern='SK.*ID', row_limit=25000, row_offset=0) -> None:
    """
    Saves the data stored in a pandas DataFrame into a table named table_name
    in the relational database.  Applies indexes to all columns matching the
    supplied index_col_pattern.

    Parameters
    -------------------
        data_frame (pd.DataFrame)
            Dataframe containing the data to be saved to the relational database
        
        table_name (str)
            Name of the table the Dataframe's data will be loaded into
    
    Return
    ------------------
        None
    """
    print(
        f"\n  Saving {table_name}\n"
        f"  ______________________________________\n"
    )
    index_col_regex = re.compile(index_col_pattern)
    if re.compile('application_test').search(table_name) is not None:
        row_offset = 0
    data_frame = data_frame.iloc[row_offset:row_limit,:]
    print(f"  Saving {table_name} with shape {data_frame.shape}")
    start_time = time.monotonic()
    data_frame.to_pickle(f"data/{table_name}.pkl")
    finish_time = time.monotonic()
    print(f"  Completed saving {table_name} after {round(finish_time - start_time, 3)} seconds")
    
    print("  ______________________________________\n")