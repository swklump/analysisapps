from django.test import TestCase
from requests import request
import json
import pandas as pd
# Create your tests here.
response = request(url="https://api.census.gov/data/2020/acs/acs5/profile/variables.json", method='get')
data=json.loads(response.text)['variables']# pick the 'people' data source from json
df_vars = pd.DataFrame(data).transpose()
df_vars['name'] = df_vars.index
df_vars = df_vars[df_vars['name'].str.slice(-2, )=='PE']
df_vars.to_excel('test.xlsx',index=False)