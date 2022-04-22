from django.db import models
import pandas as pd

# # PULL AND FORMAT TABLES FROM CENSUS API-------------------------------------------------------------------------
# # api_call = 'https://api.census.gov/data/2019/acs/acs5/profile?get=group(DP05)&for=tract:*&in=state:02&in=county:*&key=2d06b2407a7edc598608026ac92014c461d42dbb'

# tables = {'DP04':[],'DP05':[]}
# api_key = '2d06b2407a7edc598608026ac92014c461d42dbb'
# year = '2019'
# state_id = '06' #California
# for k in tables.keys():
#     api_call = 'https://api.census.gov/data/' + year
#     if k[0] == 'B':
#         api_call += '/acs/acs5?get=group(' + k + ')&for=block%20group:*&in=state:' + state_id + '&in=county:*&in=tract:*'
#     elif k[0] == 'S':
#         api_call += '/acs/acs5/subject?get=group(' + k + ')&for=tract:*&in=state:' + state_id + '&in=county:*'
#     elif k[0] == 'D':
#         api_call += '/acs/acs5/profile?get=group(' + k + ')&for=tract:*&in=state:' + state_id + '&in=county:*'
#     elif k[0] == 'C':
#         api_call += '/acs/acs5/cprofile?get=group(' + k + ')&for=tract:*&in=state:' + state_id + '&in=county:*'
#     api_call += '&key='+api_key
#     df = pd.read_json(str(api_call))

#     # promote first data row to header
#     new_header = df.iloc[0]
#     df = df[1:]
#     df.columns = new_header
#     table_cols = df.columns.tolist()
#     table_cols.insert(0, k)

#     # Remove columns
#     df_new = pd.DataFrame({})
#     for x in df.columns.tolist():
#         if x in ["GEO_ID","NAME","state","county","tract","block group"]:
#             df_new[x] = df[x].astype(str).values.tolist()
#         elif k[0] in ['B','S'] and x[-1:] == 'E':
#             df_new[x] = df[x].values.tolist()
#         elif k[0] == 'D' and x[-2:] == 'PE':
#             df_new[x] = df[x].values.tolist()
    
#     # Send columns to dictionary
#     tables[k] = df_new.columns.tolist()

# # CREATE TABLES AND ADD FIELDS-------------------------------------------------------------------------

# Create table
class DP04(models.Model):
    GEO_ID = models.CharField(primary_key=True, max_length=255, default='na')

class DP05(models.Model):
    GEO_ID = models.CharField(primary_key=True, max_length=255, default='na')


# Add fields to table from df
tables = {'DP04':['DP04_0001PE', 'DP04_0002PE', 'DP04_0003PE', 'DP04_0004PE', 'DP04_0005PE', 'DP04_0006PE', 'DP04_0007PE', 'DP04_0008PE', 'DP04_0009PE', 'DP04_0010PE', 'DP04_0011PE', 'DP04_0012PE', 'DP04_0013PE', 'DP04_0014PE', 'DP04_0015PE', 'DP04_0016PE', 'DP04_0017PE', 'DP04_0018PE', 'DP04_0019PE', 'DP04_0020PE', 'DP04_0021PE', 'DP04_0022PE', 'DP04_0023PE', 'DP04_0024PE', 'DP04_0025PE', 'DP04_0026PE', 'DP04_0027PE', 'DP04_0028PE', 'DP04_0029PE', 'DP04_0030PE', 'DP04_0031PE', 'DP04_0032PE', 'DP04_0033PE', 'DP04_0034PE', 'DP04_0035PE', 'DP04_0036PE', 'DP04_0037PE', 'DP04_0038PE', 'DP04_0039PE', 'DP04_0040PE', 'DP04_0041PE', 'DP04_0042PE', 'DP04_0043PE', 'DP04_0044PE', 'DP04_0045PE', 'DP04_0046PE', 'DP04_0047PE', 'DP04_0048PE', 'DP04_0049PE', 'DP04_0050PE', 'DP04_0051PE', 'DP04_0052PE', 'DP04_0053PE', 'DP04_0054PE', 'DP04_0055PE', 'DP04_0056PE', 'DP04_0057PE', 'DP04_0058PE', 'DP04_0059PE', 'DP04_0060PE', 'DP04_0061PE', 'DP04_0062PE', 'DP04_0063PE', 'DP04_0064PE', 'DP04_0065PE', 'DP04_0066PE', 'DP04_0067PE', 'DP04_0068PE', 'DP04_0069PE', 'DP04_0070PE', 'DP04_0071PE', 'DP04_0072PE', 'DP04_0073PE', 'DP04_0074PE', 'DP04_0075PE', 'DP04_0076PE', 'DP04_0077PE', 'DP04_0078PE', 'DP04_0079PE', 'DP04_0080PE', 'DP04_0081PE', 'DP04_0082PE', 'DP04_0083PE', 'DP04_0084PE', 'DP04_0085PE', 'DP04_0086PE', 'DP04_0087PE', 'DP04_0088PE', 'DP04_0089PE', 'DP04_0090PE', 'DP04_0091PE', 'DP04_0092PE', 'DP04_0093PE', 'DP04_0094PE', 'DP04_0095PE', 'DP04_0096PE', 'DP04_0097PE', 'DP04_0098PE', 'DP04_0099PE', 'DP04_0100PE', 'DP04_0101PE', 'DP04_0102PE', 'DP04_0103PE', 'DP04_0104PE', 'DP04_0105PE', 'DP04_0106PE', 'DP04_0107PE', 'DP04_0108PE', 'DP04_0109PE', 'DP04_0110PE', 'DP04_0111PE', 'DP04_0112PE', 'DP04_0113PE', 'DP04_0114PE', 'DP04_0115PE', 'DP04_0116PE', 'DP04_0117PE', 'DP04_0118PE', 'DP04_0119PE', 'DP04_0120PE', 'DP04_0121PE', 'DP04_0122PE', 'DP04_0123PE', 'DP04_0124PE', 'DP04_0125PE', 'DP04_0126PE', 'DP04_0127PE', 'DP04_0128PE', 'DP04_0129PE', 'DP04_0130PE', 'DP04_0131PE', 'DP04_0132PE', 'DP04_0133PE', 'DP04_0134PE', 'DP04_0135PE', 'DP04_0136PE', 'DP04_0137PE', 'DP04_0138PE', 'DP04_0139PE', 'DP04_0140PE', 'DP04_0141PE', 'DP04_0142PE', 'DP04_0143PE', 'GEO_ID', 'NAME', 'state', 'county', 'tract'],
'DP05':['DP05_0001PE', 'DP05_0002PE', 'DP05_0003PE', 'DP05_0004PE', 'DP05_0005PE', 'DP05_0006PE', 'DP05_0007PE', 'DP05_0008PE', 'DP05_0009PE', 'DP05_0010PE', 'DP05_0011PE', 'DP05_0012PE', 'DP05_0013PE', 'DP05_0014PE', 'DP05_0015PE', 'DP05_0016PE', 'DP05_0017PE', 'DP05_0018PE', 'DP05_0019PE', 'DP05_0020PE', 'DP05_0021PE', 'DP05_0022PE', 'DP05_0023PE', 'DP05_0024PE', 'DP05_0025PE', 'DP05_0026PE', 'DP05_0027PE', 'DP05_0028PE', 'DP05_0029PE', 'DP05_0030PE', 'DP05_0031PE', 'DP05_0032PE', 'DP05_0033PE', 'DP05_0034PE', 'DP05_0035PE', 'DP05_0036PE', 'DP05_0037PE', 'DP05_0038PE', 'DP05_0039PE', 'DP05_0040PE', 'DP05_0041PE', 'DP05_0042PE', 'DP05_0043PE', 'DP05_0044PE', 'DP05_0045PE', 'DP05_0046PE', 'DP05_0047PE', 'DP05_0048PE', 'DP05_0049PE', 'DP05_0050PE', 'DP05_0051PE', 'DP05_0052PE', 'DP05_0053PE', 'DP05_0054PE', 'DP05_0055PE', 'DP05_0056PE', 'DP05_0057PE', 'DP05_0058PE', 'DP05_0059PE', 'DP05_0060PE', 'DP05_0061PE', 'DP05_0062PE', 'DP05_0063PE', 'DP05_0064PE', 'DP05_0065PE', 'DP05_0066PE', 'DP05_0067PE', 'DP05_0068PE', 'DP05_0069PE', 'DP05_0070PE', 'DP05_0071PE', 'DP05_0072PE', 'DP05_0073PE', 'DP05_0074PE', 'DP05_0075PE', 'DP05_0076PE', 'DP05_0077PE', 'DP05_0078PE', 'DP05_0079PE', 'DP05_0080PE', 'DP05_0081PE', 'DP05_0082PE', 'DP05_0083PE', 'DP05_0084PE', 'DP05_0085PE', 'DP05_0086PE', 'DP05_0087PE', 'DP05_0088PE', 'DP05_0089PE', 'GEO_ID', 'NAME', 'state', 'county', 'tract']}
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
