import os
import glob
import re
import dotenv
import time
from typing import List, Dict

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection

dotenv.load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

db_engine = create_engine(DATABASE_URL)
db_connection = db_engine.connect()

def load_data(*args):
    """
    Parse CSV data and load it into the relational database
    """
    print(f"Loading data from data/ directory to relational database...")
    files = glob.glob('data/*.csv')
    table_name_regex = re.compile('(\w+)\.csv$')
    id_col_regex = re.compile('SK.*ID')

    for filename in files[:1]:
        match = table_name_regex.search(filename)
        if match is None:
            continue
        
        tablename = match.groups()[0]
        start_time = time.monotonic()
        print(
            f"\n  Loading {tablename}\n"
            f"  ______________________________________\n"
        )
        data = pd.read_csv(filename)
        data.to_sql(tablename, db_connection, if_exists='replace', chunksize=1000)
        finish_time = time.monotonic()
        print(f"  Completed loading {tablename} after {finish_time - start_time} seconds")
            
        for column in data.columns:
            if id_col_regex.search(column) is not None:
                print(f"  Creating index on {column} of {tablename} ... ", end='')
                query = text(
                    f"CREATE INDEX ON {tablename} USING btree(\"{column}\");"
                )
                try:
                    db_connection.execute(query)
                    print(f"Successfully created unique index.")
                except Exception as err:
                    print(f"Skipping index due to: {err}")
        
        print("  ______________________________________\n")
