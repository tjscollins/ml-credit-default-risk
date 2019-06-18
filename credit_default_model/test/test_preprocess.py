import unittest

import pandas as pd

from credit_default_model.preprocess.encode import encode_vars, align_data

class TestEncodeVars(unittest.TestCase):

    def test_one_hot_all_columns(self):
        test_data = {
            'ID': [0, 1, 2, 3],
            'COLOR': ['red', 'green', 'red', 'blue'],
            'FLAVOR': ['strawberry', 'apple', 'cherry', 'blueberry']
        }

        test_data_frame = pd.DataFrame(test_data)

        encoded_data_frame = encode_vars(test_data_frame)

        self.assertEqual(
            encoded_data_frame.loc[0, 'COLOR_red'], True
        )
        self.assertEqual(
            encoded_data_frame.loc[0, 'COLOR_blue'], False
        )
        self.assertEqual(
            encoded_data_frame.loc[1, 'COLOR_red'], False
        )
        self.assertEqual(
            encoded_data_frame.loc[1, 'COLOR_green'], True
        )
        self.assertEqual(
            encoded_data_frame.loc[1, 'FLAVOR_cherry'], False
        )
        self.assertEqual(
            encoded_data_frame.loc[1, 'FLAVOR_apple'], True
        )

    def test_one_hot_select_columns(self):
        test_data = {
            'ID': [0, 1, 2, 3],
            'COLOR': ['red', 'green', 'red', 'blue'],
            'FLAVOR': ['strawberry', 'apple', 'cherry', 'blueberry']
        }

        test_data_frame = pd.DataFrame(test_data)

        encoded_data_frame = encode_vars(test_data_frame, columns=['COLOR'])

        self.assertEqual(
            encoded_data_frame.loc[0, 'COLOR_red'], True
        )
        self.assertEqual(
            encoded_data_frame.loc[0, 'COLOR_blue'], False
        )
        self.assertEqual(
            encoded_data_frame.loc[1, 'COLOR_red'], False
        )
        self.assertEqual(
            encoded_data_frame.loc[1, 'COLOR_green'], True
        )
        self.assertRaises(
            KeyError, lambda: encoded_data_frame.loc[1, 'FLAVOR_cherry']
        )
        self.assertRaises(
            KeyError, lambda: encoded_data_frame.loc[1, 'FLAVOR_apple']
        )

    def test_label_encode_all_columns(self):
        test_data = {
            'ID': [0, 1, 2, 3],
            'COLOR': ['red', 'green', 'red', 'blue'],
            'FLAVOR': ['strawberry', 'apple', 'cherry', 'blueberry']
        }

        test_data_frame = pd.DataFrame(test_data)

        encoded_data_frame = encode_vars(test_data_frame, encoding_type='label-encoding')

        self.assertEqual(
            encoded_data_frame.loc[0, 'COLOR'], 2
        )
        self.assertEqual(
            encoded_data_frame.loc[1, 'COLOR'], 1
        )
        self.assertEqual(
            encoded_data_frame.loc[0, 'FLAVOR'], 3
        )
        self.assertEqual(
            encoded_data_frame.loc[1, 'FLAVOR'], 0
        )

    def test_label_encode_select_columns(self):
        test_data = {
            'ID': [0, 1, 2, 3],
            'COLOR': ['red', 'green', 'red', 'blue'],
            'FLAVOR': ['strawberry', 'apple', 'cherry', 'blueberry']
        }

        test_data_frame = pd.DataFrame(test_data)

        encoded_data_frame = encode_vars(test_data_frame, encoding_type='label-encoding', columns=['COLOR'])

        self.assertEqual(
            encoded_data_frame.loc[0, 'COLOR'], 2
        )
        self.assertEqual(
            encoded_data_frame.loc[1, 'COLOR'], 1
        )
        self.assertEqual(
            encoded_data_frame.loc[0, 'FLAVOR'], 'strawberry'
        )
        self.assertEqual(
            encoded_data_frame.loc[1, 'FLAVOR'], 'apple'
        )

    def test_error_unknown_encoding_type(self):
        test_data = {
            'ID': [0, 1, 2, 3],
            'COLOR': ['red', 'green', 'red', 'blue'],
            'FLAVOR': ['strawberry', 'apple', 'cherry', 'blueberry']
        }

        test_data_frame = pd.DataFrame(test_data)

        self.assertRaises(ValueError, lambda: encode_vars(test_data_frame, encoding_type='random-encoding'))

class TestAlignFrames(unittest.TestCase):

    def test_basic_alignment(self):
        train_data = pd.DataFrame({
            'X': [1, 2, 3, 4],
            'Y': [4, 3, 2, 1],
            'TARGET': [0, 0, 0, 0]
        })

        test_data = pd.DataFrame({
            'X': [1, 2, 3, 4]
        })

        atrd, ated = align_data(train_data, test_data)

        self.assertRaises(
            KeyError, lambda: atrd.loc[0]['Y']
        )
        self.assertIsNotNone(
            atrd.loc[0]['X']
        )
        self.assertIsNotNone(
            atrd.loc[0]['TARGET']
        )
        self.assertRaises(
            KeyError, lambda: atrd.loc[3]['Y']
        )
        self.assertIsNotNone(
            atrd.loc[3]['TARGET']
        )
        self.assertIsNotNone(
            atrd.loc[3]['X']
        )
        

        self.assertIsNotNone(
            ated.loc[0]['X']
        )
        self.assertRaises(
            KeyError, lambda: ated.loc[0]['Y']
        )
        self.assertRaises(
            KeyError, lambda: ated.loc[0]['TARGET']
        )

    def test_preserve(self):
        train_data = pd.DataFrame({
            'X': [1, 2, 3, 4],
            'Y': [4, 3, 2, 1],
            'Z': ['a', 'b', 'c', 'd'],
            'TARGET': [0, 0, 0, 0]
        })

        test_data = pd.DataFrame({
            'X': [1, 2, 3, 4]
        })        

        atrd, ated = align_data(train_data, test_data, preserve=['Z', 'Y'])


        self.assertRaises(
            KeyError, lambda: atrd.loc[0]['TARGET']
        )
        self.assertIsNotNone(
            atrd.loc[0]['Z']
        )
        self.assertIsNotNone(
            atrd.loc[0]['Y']
        )
        self.assertRaises(
            KeyError, lambda: atrd.loc[3]['TARGET']
        )
        self.assertIsNotNone(
            atrd.loc[3]['X']
        )
        self.assertIsNotNone(
            atrd.loc[3]['Y']
        )
        

        self.assertIsNotNone(
            ated.loc[0]['X']
        )
        self.assertRaises(
            KeyError, lambda: ated.loc[0]['Y']
        )
        self.assertRaises(
            KeyError, lambda: ated.loc[0]['TARGET']
        )
