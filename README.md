# zipbiaschecker

One challenge of assessing algorithmic racial bias is sometimes that the data are missing (not collected as part of sign-up forms, for example) or unavailable for privacy reasons. In these cases, zipcode-level bias is an indirect measure. We can go one step further by analyzing Census data that contain racial demographic data by zip code. This package helps run this indirect check by looking at the correlation between the algorithmic output and the percentage of Black, Hispanic, and Indigenous people in that zip code.

## Installation

This package can be installed using the command below:
```
pip install zipbiaschecker
```

## Example

In this example, the data is taken from the [Illinois Department of Public Health COVID statistics](https://www.dph.illinois.gov/covid19/covid19-statistics) as of 7/15/20. We will examine the correlation between the positive rate of testing by zip code vs. the demographics of the zip code to check the disparate impact of COVID on racial minorities.


```python
import pandas as pd
from zipbiaschecker import zipbiaschecker as zbc

df = pd.read_csv('zipbiaschecker/data/example/2020_07_15_illinois_covid_data.csv')
df['positive_rate'] = df['Positive Cases'] / df['Tested']
print(df.shape)
df.head()
```

    (646, 4)





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Zip</th>
      <th>Tested</th>
      <th>Positive Cases</th>
      <th>positive_rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>60002</td>
      <td>1925</td>
      <td>130</td>
      <td>0.067532</td>
    </tr>
    <tr>
      <th>1</th>
      <td>60004</td>
      <td>9441</td>
      <td>406</td>
      <td>0.043004</td>
    </tr>
    <tr>
      <th>2</th>
      <td>60005</td>
      <td>4771</td>
      <td>255</td>
      <td>0.053448</td>
    </tr>
    <tr>
      <th>3</th>
      <td>60007</td>
      <td>4191</td>
      <td>383</td>
      <td>0.091386</td>
    </tr>
    <tr>
      <th>4</th>
      <td>60008</td>
      <td>4672</td>
      <td>380</td>
      <td>0.081336</td>
    </tr>
  </tbody>
</table>
</div>



To interpret the cell below, we see that the rate of positive cases has a positive correlation of about .278 with the proportion of Black people in the zip code, .585 with the proportion of Hispanic people in the zip code, and .108 with the proportion of Indigenous people in the zip code.


```python
zip_bias_checker = zbc.ZipBiasChecker()
zip_bias_checker.check_bias(df, zip_col_name='Zip', target_col_name='positive_rate')
```

    1 row(s) could not be matched out of 646

    percent_black         0.277773
    percent_hispanic      0.585238
    percent_indigenous    0.107945
    Name: positive_rate, dtype: float64



## Documentation notebook for process to generate reference data

In the `notebooks` folder, the process to map zip codes to demographic data is documented in a Jupyter notebook. To run the notebook, clone this repository to obtain the data used.
