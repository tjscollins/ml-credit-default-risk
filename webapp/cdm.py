from os import environ
import sys
import pickle
import featuretools
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
import boto3
import joblib

is_production_env = environ.get('PYTHON_ENV') == 'production'

if sys.argv[0] != 'flask':
    if is_production_env:
        pass
    else:
        column_descriptions: pd.DataFrame = pd.read_pickle('data/processed_HomeCredit_columns_description.pkl')
        raw_data: pd.DataFrame = pd.read_pickle('data/application_test.pkl')
        test_data: pd.DataFrame = pd.read_pickle('data/features_testing_data.pkl')
        credit_default_model: RandomForestRegressor = joblib.load('data/model.joblib')
        principal_components: PCA = joblib.load('data/PCA.joblib')

feature_importances = pd.DataFrame(credit_default_model.feature_importances_)
feature_importances = feature_importances.transpose()
feature_importances.columns = test_data.columns

def model_prediction(applicant_data: pd.DataFrame):
    prediction: dict = {}
    pred_data = credit_default_model.predict(applicant_data)

    print(pred_data, type(pred_data))

    risk = round(pred_data[0] * 100, 2)
    prediction['default_risk'] = risk
    prediction['recommended_interest'] = round(risk + 2.5, 2) if risk <= 10 else None

    return prediction

def model_analytics(applicant_data: pd.DataFrame):
    analytics: dict = {}
    return analytics

def get_feature_importances(n=None):
    importances = []

    for col in feature_importances.columns:
        try:
            importances.append((col, round(feature_importances[col][0], 6)))
        except KeyError:
            pass
    importances = sorted(
        importances,
        key=lambda i: i[1]
    )

    if n is not None and n < len(importances):
        return importances[-n:]

    return importances

exp_variances = pd.DataFrame(principal_components.explained_variance_ratio_)
predictions = credit_default_model.predict(test_data)