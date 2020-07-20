import unittest
import pandas as pd
from ..zipbiaschecker import ZipBiasChecker
from ..data import example
try:
    import importlib.resources as pkg_resources
# For Python version 3.4 through 3.8
except ImportError:
    import importlib_resources as pkg_resources


class CheckBiasTest(unittest.TestCase):
    def test_check_bias(self):
        with pkg_resources.path(example, '2020_07_15_illinois_covid_data.csv') as test_data_path:
            test_data = pd.read_csv(test_data_path)
        test_data['positive_rate'] = test_data['Positive Cases'] / test_data['Tested']

        zbc = ZipBiasChecker()
        test_results = zbc.check_bias(data_to_check=test_data, zip_col_name='Zip', target_col_name='positive_rate')
        expected_test_results = pd.Series([.2778, .5852, .1079], index=['percent_black', 'percent_hispanic',
                                                                        'percent_indigenous'])
        self.assertTrue(test_results.round(4).equals(expected_test_results))
