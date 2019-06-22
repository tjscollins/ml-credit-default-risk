import unittest

import pandas as pd
import numpy as np

from credit_default_model.preprocess.cleaners import remove_days_employed_outliers

class TestEncodeVars(unittest.TestCase):

    def test_identify_outliers(self):
        test_data = pd.DataFrame({
            'DAYS_EMPLOYED': [-1, -2, -3, -4, 365243, 365243]
        })

        cleaned_data = remove_days_employed_outliers(test_data, 'application_train')
        self.assertEqual(
            
            cleaned_data.loc[0]['DAYS_EMPLOYED'], -1
        )
        self.assertTrue(
            np.isnan(cleaned_data.loc[5]['DAYS_EMPLOYED'])
        )
        self.assertEqual(
            cleaned_data.loc[1]['DAYS_EMPLOYED'], -2
        )
        self.assertEqual(
            cleaned_data.loc[0]['DAYS_EMPLOYED_ANOM'], False
        )
        self.assertEqual(
            cleaned_data.loc[5]['DAYS_EMPLOYED_ANOM'], True
        )