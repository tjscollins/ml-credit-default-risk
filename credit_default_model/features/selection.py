from typing import Dict, Tuple
import re
import time
import os
import dotenv

from featuretools import selection
from sklearn.decomposition import PCA
import featuretools as ft
import numpy as np
import pandas as pd

from load import save_data_frame, TABLES, load_data
from preprocess.cleaners import clean_column_name
from preprocess.encode import align_data

dotenv.load_dotenv()

PCA_DIMENSIONS = int(os.getenv('PCA_DIMENSIONS', default='10'))

def prune_features(train_data: pd.DataFrame, test_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    pca = PCA(n_components=PCA_DIMENSIONS, svd_solver='full')

    print(f"\nBeginning PCA analysis of data")
    start = time.monotonic()
    pca.fit(train_data)
    end = time.monotonic()
    print(f"  Completed PCA analysis of data after {round(end - start)} seconds\n")

    print(f"PCA analysis identified {pca.n_components_} components of significance")
    pd.to_pickle(pca, "data/pca.pkl")

    train_data = pd.DataFrame(pca.transform(train_data))
    test_data = pd.DataFrame(pca.transform(test_data))

    return train_data, test_data
