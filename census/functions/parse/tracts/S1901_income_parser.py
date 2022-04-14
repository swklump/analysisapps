
def S1901_parse_income(sheet, num_cols, num_rows, location_id, index_estimate):
    import xlrd
    import pandas as pd
    from WebApp.census.parse.tracts._helperfunctions import get_rowindex, get_rownameindex

    ####INCOME
    #Get income rows
    result = get_rownameindex(sheet, num_rows, 'Total', 'Median income (dollars)')
    rownames_income = result[0]
    rownames_income_index = result[1]
                  
    for n in range(num_rows):
        if sheet.cell_value(n,0) == 'Total':
            rownames_income_total_index = n
        elif sheet.cell_value(n,0) == 'Median income (dollars)':
            rownames_income_med_index = n
        elif sheet.cell_value(n,0) == 'Mean income (dollars)':
            rownames_income_mean_index = n


    #Create income table
    dict_income = {'location_id':[],'income_range':[], 'people':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_income)):
            dict_income['location_id'].append(location_id[x])
            dict_income['income_range'].append(rownames_income[c])
            if sheet.cell_value(rownames_income_index[c],index_estimate[x]) == '-':
                dict_income['people'].append(0)
            else:
                dict_income['people'].append(sheet.cell_value(rownames_income_index[c],index_estimate[x]).replace('%',''))

    dict_income_summary = {'location_id':[], 'total_households':[], 'median_income':[], 'mean_income':[]}
    for x in range(len(location_id)):
        dict_income_summary['location_id'].append(location_id[x])
        dict_income_summary['total_households'].append(int(sheet.cell_value(rownames_income_total_index,index_estimate[x]).replace(',','')))
        if sheet.cell_value(rownames_income_med_index,index_estimate[x]) in ['-','N']:
            dict_income_summary['median_income'].append(0)
        else:
            dict_income_summary['median_income'].append(int(sheet.cell_value(rownames_income_med_index,index_estimate[x]).replace(',','')))
        if sheet.cell_value(rownames_income_mean_index,index_estimate[x]) in ['-','N']:
            dict_income_summary['mean_income'].append(0)
        else:
            dict_income_summary['mean_income'].append(int(sheet.cell_value(rownames_income_mean_index,index_estimate[x]).replace(',','')))
            
    ####Create output file
    df_income = pd.DataFrame(dict_income,columns=['location_id','income_range', 'people'])
    df_income['people'] = pd.to_numeric(df_income['people']).div(100)
    df_income_summary = pd.DataFrame(dict_income_summary,columns=['location_id','total_households', 'median_income', 'mean_income'])

    dfs = [df_income, df_income_summary]
    excel_name, sheetnames = 'S1901_parsed.xlsx', ['Income', 'IncomeSummary']
    return dfs, excel_name, sheetnames