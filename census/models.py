from pyexpat import model
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import pandas as pd

# Now figure out how to add data to fields
# Then how to query the data in app

# PULL AND FORMAT TABLES FROM CENSUS API-------------------------------------------------------------------------
# api_call = 'https://api.census.gov/data/2019/acs/acs5/profile?get=group(DP05)&for=tract:*&in=state:02&in=county:*&key=2d06b2407a7edc598608026ac92014c461d42dbb'

tables = ['DP05']
years = ['2019']
api_key = '2d06b2407a7edc598608026ac92014c461d42dbb'
df = pd.DataFrame({})
for y in range(len(years)):
    api_call = 'https://api.census.gov/data/'+ \
    str(years[y]) + '/acs/acs5/profile?get=group(' + 'DP05' + ')&for=tract:*&in=state:02&in=county:*&key='+api_key
    df_single = pd.read_json(str(api_call))
    df = pd.concat([df,df_single])

# promote first data row to header
new_header = df.iloc[0]
df = df[1:]
df.columns = new_header
table_cols = df.columns.tolist()
table_cols.insert(0,'DP05')

# Remove columns not ending in EA
df_new = pd.DataFrame({})
for x in df.columns.tolist():
    if x in ["GEO_ID","NAME","state","county","tract"]:
        df_new[x] = df[x].values.tolist()
    elif x[-2:] == 'PE':
        df_new[x] = df[x].values.tolist()


# CREATE TABLES AND ADD FIELDS-------------------------------------------------------------------------

# Create table
class DP05(models.Model):
    pass

# Add fields to table from df
for x in df_new.columns.tolist():
    DP05.add_to_class(x, models.CharField(max_length=255))



