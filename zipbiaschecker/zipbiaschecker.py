import pandas as pd
import logging
from .data import processed
try:
    import importlib.resources as pkg_resources
# For Python versions 3.4 through 3.8
except ImportError:
    import importlib_resources as pkg_resources

log = logging.getLogger()


class ZipBiasChecker:

    def __init__(self):
        with pkg_resources.path(processed, 'zipcode_demographic_data.csv') as reference_data_path:
            self.reference_data = pd.read_csv(reference_data_path)
        self.reference_data['ZIP'] = [x.zfill(5) for x in self.reference_data['ZIP'].astype(str)]

    def check_bias(self, data_to_check, zip_col_name, target_col_name,
                   groups_to_check=['percent_black', 'percent_hispanic', 'percent_indigenous']):
        """Check the bias of a target column in a pandas Dataframe with row-level zip code

        :param data_to_check: pandas Dataframe containing zip_col_name and target_col_name
        :param zip_col_name: name of the column containing zip codes
        :param target_col_name: name of column to check for bias (e.g., model scores)
        :param groups_to_check: list of demographic groups to check for biases
        :return: pandas Series with the correlation of target_col_name against each element of groups_to_check
        """
        if [x for x in [zip_col_name, target_col_name] if x not in data_to_check.columns]:
            raise Exception("zip_col_name and/or target_col_name not present in data_to_check columns")

        data_to_check[zip_col_name] = data_to_check[zip_col_name].astype(str)
        # Handle non ZIP-5 values
        if any(data_to_check[zip_col_name].str.len() < 5):
            log.warning('Zip codes shorter than 5 digits detected, left-filling with zeros')
            data_to_check[zip_col_name] = [x.zfill(5) for x in data_to_check[zip_col_name]]
        if any(data_to_check[zip_col_name].str.len() > 5):
            log.warning('Zip codes long than 5 digits detected, taking first 5 digits')
            data_to_check[zip_col_name] = [x[:5] for x in data_to_check[zip_col_name]]

        data_to_check = pd.merge(data_to_check, self.reference_data, how='left',
                                 left_on=zip_col_name, right_on='ZIP', suffixes=('_check', ''))
        if data_to_check['ZIP'].isnull().sum() > 0:
            log.warning('{} row(s) could not be matched out of {}'.format(data_to_check['ZIP'].isnull().sum(),
                                                                          len(data_to_check)))

        if target_col_name in data_to_check.columns:
            corr_df = data_to_check[[target_col_name] + groups_to_check].corr()
        # In case target_col_name was changed by the merge above
        else:
            corr_df = data_to_check[[target_col_name + '_check'] + groups_to_check].corr()

        return corr_df.iloc[0, 1:]