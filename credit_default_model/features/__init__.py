import re
from typing import Dict, Tuple

from featuretools import selection
import featuretools as ft
import numpy as np
import pandas as pd

from db.tables import get_processed_tables, load_table_to_data_frame
from preprocess.encode import align_data
from preprocess.cleaners import clean_column_name
from load import save_data_frame


def collect_processed_data() -> Tuple[Dict[str, pd.DataFrame], str, str]:
    """
    Collect all the processed data tables and load their data into pandas
    DataFrames, storing the individual DataFrames in a hashmap which we return
    for processing along with the names of the training and desting data

    Paramters
    ------------
        None
    
    Returns
    ------------
        data (Dict[str, pd.DataFrame])
            Hashmap that associates each DataFrame with the name of the table it
            was loaded from.

        train_table (str)
            The name of the table with the training data
        
        test_table (str)
            The name of the table with the testing data
    """
    data = {}
    test_table, train_table = '', ''
    test_regex = re.compile('test$')
    train_regex = re.compile('train$')

    for table in get_processed_tables():
        if test_regex.search(table) is not None:
            test_table = table
            print(f"Identified test data table {table}")
        elif train_regex.search(table) is not None:
            train_table = table
            print(f"Identified training data table {table}")
        else:
            print(f"Identified additional data table {table}")
        data[table] = load_table_to_data_frame(table)
        print(f"  {table} has shape {data[table].shape}\n")
    
    return data, train_table, test_table

def engineer_features(*args, **kwargs):
    data, train_table, test_table = collect_processed_data()

    # Add pseudo columns to distinguish training and test data so we can separate
    # them again after we finish feature engineering
    data[train_table]['DATA_SET'] = 0
    data[test_table]['DATA_SET'] = 1
    data[test_table]['TARGET'] = np.nan

    data[train_table], data[test_table] = align_data(data[train_table], data[test_table])

    data['combined_train_test'] = data[train_table].append(
        data[test_table], ignore_index=True, sort=False
    )

    es = create_entity_set(data, train_table, test_table)

    feature_matrix, feature_names = ft.dfs(
        entityset=es,
        target_entity='combined_train_test',
        max_depth=3
    )

    feature_matrix = selection.remove_low_information_features(feature_matrix)

    train_data = feature_matrix[feature_matrix['DATA_SET'] == 0]
    test_data = feature_matrix[feature_matrix['DATA_SET'] == 1]

    save_data_frame(train_data, f"features_training_data")
    save_data_frame(test_data, f"features_testing_data")

def create_entity_set(data: pd.DataFrame, train_table: str, test_table: str) -> ft.EntitySet:
    es = ft.EntitySet(id = 'clients')

    es = es.entity_from_dataframe(
        entity_id='combined_train_test',
        dataframe=data['combined_train_test'],
        index='SK_ID_CURR'
    )

    es = es.entity_from_dataframe(
        entity_id='processed_bureau',
        dataframe=data['processed_bureau'],
        index='SK_ID_BUREAU'
    )

    es = es.entity_from_dataframe(
        entity_id='processed_bureau_balance',
        dataframe=data['processed_bureau_balance'],
        make_index=True,
        index = 'bureaubalance_index'
    )

    es = es.entity_from_dataframe(
        entity_id='processed_previous_application',
        dataframe=data['processed_previous_application'],
        index='SK_ID_PREV'
    )

    es = es.add_relationships([
        ft.Relationship(es['combined_train_test']['SK_ID_CURR'], es['processed_bureau']['SK_ID_CURR']),
        ft.Relationship(es['processed_bureau']['SK_ID_BUREAU'], es['processed_bureau_balance']['SK_ID_BUREAU']),
        ft.Relationship(es['combined_train_test']['SK_ID_CURR'], es['processed_previous_application']['SK_ID_CURR'])
    ])

    return es