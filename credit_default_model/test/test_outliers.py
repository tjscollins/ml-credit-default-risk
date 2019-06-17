import unittest

import pandas as pd

from credit_default_model.preprocess.outliers import identify_outliers

class TestEncodeVars(unittest.TestCase):

    def test_identify_outliers(self):
        test_data = pd.DataFrame({
            'X': [1, 2, 3, 4, -10000, 10000]
        })

        self.assertEqual(
            identify_outliers(test_data),
            pd.DataFrame({
                'X': [-10000, 10000]
            })
        )