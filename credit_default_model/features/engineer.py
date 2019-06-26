import time
import re
from typing import Dict, Tuple
import os
import dotenv

from featuretools import selection
import featuretools as ft
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer

from load.loader import TABLES, save_data_frame
from preprocess.encode import align_data
from .selection import prune_features

dotenv.load_dotenv()

MAX_FEATURES = int(os.environ.get('MAX_FEATURES', default='250'))
MAX_FT_DEPTH = int(os.environ.get('MAX_FT_DEPTH', default='3'))
USE_PCA = os.environ.get('USE_PCA', default='False')

def engineer_features(*args, **kwargs):
    data, train_table, test_table = collect_processed_data()

    # Add pseudo columns to distinguish training and test data so we can separate
    # them again after we finish feature engineering
    data[train_table]['DATA_SET'] = 0
    data[test_table]['DATA_SET'] = 1
    data[test_table]['TARGET'] = np.nan

    data[test_table], data[train_table] = align_data(data[test_table], data[train_table])

    data['combined_train_test'] = data[train_table].append(
        data[test_table],
        ignore_index=True,
        sort=False
    )

    labels = data['combined_train_test']['SK_ID_CURR']

    train_data, test_data = create_feature_set(data, train_table, test_table)

    train_labels = train_data['TARGET']
    train_ids = train_data.index
    test_ids = test_data.index

    train_data = train_data.drop(columns=['DATA_SET', 'TARGET'])
    test_data = test_data.drop(columns=['DATA_SET', 'TARGET'])

    train_data, test_data = impute_and_scale(train_data, test_data)

    if USE_PCA == 'True':
        print(f"\nApplying PCA to reduce dimensionality of engineered features")
        print(f"  PCA_DIMENSIONS={PCA_DIMENSIONS}")
        train_data, test_data = prune_features(train_data, test_data)

    train_data.index = train_ids
    train_data['TARGET'] = train_labels
    test_data.index = test_ids
    print('final: \n', train_data)

    save_data_frame(train_data, f"features_training_data")
    save_data_frame(test_data, f"features_testing_data")

def create_feature_set(data: pd.DataFrame, train_table: str, test_table: str):
    es = create_entity_set(data, train_table, test_table)

    print(f"\nBeginning automated feature engineering using entity set")
    print(f"  MAX_FEATURES={MAX_FEATURES}")
    print(f"  MAX_FT_DEPTH={MAX_FT_DEPTH}")

    start = time.monotonic()
    feature_matrix, feature_names = ft.dfs(
        entityset=es,
        target_entity='combined_train_test',
        max_depth=MAX_FT_DEPTH,
        max_features=MAX_FEATURES,
        verbose=True
    )
    end = time.monotonic()

    print(f"Automated feature engineering completed in {round(end - start)} seconds")

    feature_matrix = selection.remove_low_information_features(feature_matrix)

    print(f"  Found {feature_matrix.shape[1]} features")

    train_data: pd.DataFrame = pd.DataFrame(feature_matrix[feature_matrix['DATA_SET'] == 0])
    test_data: pd.DataFrame = pd.DataFrame(feature_matrix[feature_matrix['DATA_SET'] == 1])

    return train_data, test_data

def impute_and_scale(train_data: pd.DataFrame, test_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    print(f"Cleaning dataset by imputation and scaling")
    columns = train_data.columns

    imputer = SimpleImputer(strategy='median')
    scaler = MinMaxScaler(feature_range = (0, 1))

    start = time.monotonic()
    imputer.fit(train_data)

    train_data = imputer.transform(train_data)
    test_data = imputer.transform(test_data)

    scaler.fit(train_data)

    train_data = scaler.transform(train_data)
    test_data = scaler.transform(test_data)
    end=time.monotonic()

    print(f"  Completed in {round(end - start)} seconds")

    return pd.DataFrame(train_data, columns=columns), pd.DataFrame(test_data, columns=columns)

def create_entity_set(data: pd.DataFrame, train_table: str, test_table: str) -> ft.EntitySet:
    print(f"\nCreating entity set based on client data")
    start = time.monotonic()
    es = ft.EntitySet(id = 'clients')

    es = es.entity_from_dataframe(
        entity_id='combined_train_test',
        dataframe=data['combined_train_test'],
        index='SK_ID_CURR'
    )

    es = es.entity_from_dataframe(
        entity_id='bureau',
        dataframe=data['bureau'],
        index='SK_ID_BUREAU'
    )

    es = es.entity_from_dataframe(
        entity_id='bureau_balance',
        dataframe=data['bureau_balance'],
        make_index=True,
        index = 'bureaubalance_index'
    )

    es = es.entity_from_dataframe(
        entity_id='previous_application',
        dataframe=data['previous_application'],
        index='SK_ID_PREV'
    )

    es = es.add_relationships([
        ft.Relationship(es['combined_train_test']['SK_ID_CURR'], es['bureau']['SK_ID_CURR']),
        ft.Relationship(es['bureau']['SK_ID_BUREAU'], es['bureau_balance']['SK_ID_BUREAU']),
        ft.Relationship(es['combined_train_test']['SK_ID_CURR'], es['previous_application']['SK_ID_CURR'])
    ])
    end = time.monotonic()

    print(f"  Entity set creation completed in {round(end - start)} seconds")

    return es

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

    for table in TABLES:
        if test_regex.search(table) is not None:
            test_table = table
            print(f"Identified test data table {table}")
        elif train_regex.search(table) is not None:
            train_table = table
            print(f"Identified training data table {table}")
        else:
            print(f"Identified additional data table {table}")
        data[table] = pd.read_pickle(f"data/processed_{table}.pkl")
        print(f"  {table} has shape {data[table].shape}\n")
    
    return data, train_table, test_table
