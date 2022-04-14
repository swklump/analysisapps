def C17002_parse_incomepovratio(sheet, numcols, num_rows, location_id, index_estimate):
    import pandas as pd

    # Create table
    dict = {'location_id':[],'income_pov_ratio':[], 'people':[]}
    for x in range(len(location_id)):
        for c in range(3,num_rows):
            dict['location_id'].append(location_id[x])
            dict['income_pov_ratio'].append(sheet.cell_value(c,0))
            dict['people'].append(int(sheet.cell_value(c,index_estimate[x]).replace(',','')))

    ###Create output file
    dfs = [pd.DataFrame(dict,columns=['location_id','income_pov_ratio', 'people'])]
    excel_names, sheetnames = 'C17002_parsed.xlsx', ['IncomeToPovertyRatio']
    return dfs, excel_names, sheetnames