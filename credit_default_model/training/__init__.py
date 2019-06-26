import re
from typing import Dict, Tuple
import os
from dotenv import load_dotenv

from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
import numpy as np
import pandas as pd
from joblib import dump, load

from load import save_data_frame
from preprocess.encode import align_data

load_dotenv()

DT_MIN_SAMPLES_LEAF = int(os.getenv('RF_N_ESTIMATORS', default='5'))
DT_MAX_DEPTH = int(os.getenv('DT_MAX_DEPTH', default='10'))
str_or_none = os.getenv('DT_RANDOM_STATE', default=None)
DT_RANDOM_STATE = int(str_or_none) if str_or_none is not None else None

RF_N_ESTIMATORS = int(os.getenv('RF_N_ESTIMATORS', default='10'))
RF_MAX_DEPTH = int(os.getenv('RF_MAX_DEPTH', default='10'))
RF_MIN_SAMPLES_LEAF = int(os.getenv('RF_MIN_SAMPLES_LEAF', default='5'))
str_or_none = os.getenv('RF_RANDOM_STATE', default=None)
RF_RANDOM_STATE = int(str_or_none) if str_or_none is not None else None

MODELS = {
    'DecisionTree': DecisionTreeRegressor(
        min_samples_leaf=DT_MIN_SAMPLES_LEAF,
        max_depth=DT_MAX_DEPTH,
        random_state=DT_RANDOM_STATE
    ),
    'RandomForest': RandomForestRegressor(
        min_samples_leaf=RF_MIN_SAMPLES_LEAF,
        max_depth=RF_MAX_DEPTH,
        verbose=1,
        n_estimators=RF_N_ESTIMATORS,
        n_jobs=6,
        random_state=RF_RANDOM_STATE
    )
}

def train_model(model_type='RandomForest'):
    training_data: pd.DataFrame = pd.read_pickle("data/features_training_data.pkl")

    training_ids = training_data.index
    training_labels = training_data['TARGET']
    training_data = training_data.drop(columns=['TARGET'])

    testing_data = pd.read_pickle("data/features_testing_data.pkl")

    testing_ids = testing_data.index

    features = list(training_data.columns)

    print(f"Training data shape: {training_data.shape}")
    print(f"Testing data shape: {testing_data.shape}")

    model = MODELS[model_type]
    model.fit(training_data, training_labels)

    feature_importance_values = model.feature_importances_
    feature_importances = pd.DataFrame({
        'feature': features,
        'importance': feature_importance_values
    })
    
    model_predictions = model.predict(testing_data)

    dump(model, 'data/trained_dt_model.joblib')

    validation_data = pd.DataFrame(index=testing_ids, data={
        'TARGET': model_predictions
    })

    validation_data.to_csv('data/validation.csv')
    feature_importances.to_csv('data/feature_importances.csv')
