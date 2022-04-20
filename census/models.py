from django.db import models
import pandas as pd

# PULL AND FORMAT TABLES FROM CENSUS API-------------------------------------------------------------------------
# api_call = 'https://api.census.gov/data/2019/acs/acs5/profile?get=group(DP05)&for=tract:*&in=state:02&in=county:*&key=2d06b2407a7edc598608026ac92014c461d42dbb'

tables = {'DP04':[],'DP05':[]}
api_key = '2d06b2407a7edc598608026ac92014c461d42dbb'
year = '2019'
state_id = '06' #California
for k in tables.keys():
    api_call = 'https://api.census.gov/data/' + year
    if k[0] == 'B':
        api_call += '/acs/acs5?get=group(' + k + ')&for=block%20group:*&in=state:' + state_id + '&in=county:*&in=tract:*'
    elif k[0] == 'S':
        api_call += '/acs/acs5/subject?get=group(' + k + ')&for=tract:*&in=state:' + state_id + '&in=county:*'
    elif k[0] == 'D':
        api_call += '/acs/acs5/profile?get=group(' + k + ')&for=tract:*&in=state:' + state_id + '&in=county:*'
    elif k[0] == 'C':
        api_call += '/acs/acs5/cprofile?get=group(' + k + ')&for=tract:*&in=state:' + state_id + '&in=county:*'
    api_call += '&key='+api_key
    df = pd.read_json(str(api_call))

    # promote first data row to header
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    table_cols = df.columns.tolist()
    table_cols.insert(0, k)

    # Remove columns
    df_new = pd.DataFrame({})
    for x in df.columns.tolist():
        if x in ["GEO_ID","NAME","state","county","tract","block group"]:
            df_new[x] = df[x].astype(str).values.tolist()
        elif k[0] in ['B','S'] and x[-1:] == 'E':
            df_new[x] = df[x].values.tolist()
        elif k[0] == 'D' and x[-2:] == 'PE':
            df_new[x] = df[x].values.tolist()
    
    # Send columns to dictionary
    tables[k] = df_new.columns.tolist()

# CREATE TABLES AND ADD FIELDS-------------------------------------------------------------------------

# Create table
class DP04(models.Model):
    GEO_ID = models.CharField(primary_key=True, max_length=255, default='na')

class DP05(models.Model):
    GEO_ID = models.CharField(primary_key=True, max_length=255, default='na')


# Add fields to table from df
for k in tables.keys():
    if k == 'DP04':
        for x in tables[k]:
            if x == 'GEO_ID':
                pass
            else:
                # change up this data type later on
                DP04.add_to_class(x, models.CharField(max_length=255))
    elif k =='DP05':
        for x in tables[k]:
            if x == 'GEO_ID':
                pass
            else:
                # change up this data type later on
                DP05.add_to_class(x, models.CharField(max_length=255))



