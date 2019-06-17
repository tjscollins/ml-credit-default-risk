from typing import List, Dict
import glob
import re
import time

from sqlalchemy import text 
import pandas as pd

try:
    from db import db_connection
except:
    from ..db import db_connection

def load_data(*args):
    """
    Parse CSV data and load it into the relational database
    """
    print(f"Loading data from data/ directory to relational database...")
    files = glob.glob('data/*.csv')
    table_name_regex = re.compile('(\w+)\.csv$')

    for filename in files[:1]:
        match = table_name_regex.search(filename)
        if match is None:
            continue
        
        tablename = match.groups()[0]
        data = pd.read_csv(filename)
        save_data_frame(data)

def save_data_frame(data_frame, table_name):
    print(
        f"\n  Saving {table_name}\n"
        f"  ______________________________________\n"
    )
    id_col_regex = re.compile('SK.*ID')
    start_time = time.monotonic()
    data_frame.to_sql(table_name, db_connection, if_exists='replace')
    finish_time = time.monotonic()
    print(f"  Completed loading {table_name} after {round(finish_time - start_time)} seconds")
        
    for column in data_frame.columns:
        if id_col_regex.search(column) is not None:
            print(f"  Creating index on {column} of {table_name} ... ", end='')
            query = text(
                f"CREATE INDEX ON {table_name} USING btree(\"{column}\");"
            )
            try:
                db_connection.execute(query)
                print(f"Successfully created index.")
            except Exception as err:
                print(f"Skipping index due to: {err}")
    
    print("  ______________________________________\n")