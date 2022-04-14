def B25075_parse_housingvalue(sheet, numcols, num_rows, location_id, index_estimate):
    import pandas as pd

    #Get rows names and indices
    rownames = []
    rownames_index = []
    for n in range(num_rows):
        if sheet.cell_value(n,0) == 'Total:':
            startindex = n+1
    endindex = num_rows
    for n in range(startindex,endindex):
        rownames.append(sheet.cell_value(n,0))
        rownames_index.append(n)

    # Create table
    dict = {'location_id':[],'housevalue_range':[], 'households':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames)):
            dict['location_id'].append(location_id[x])
            dict['housevalue_range'].append(rownames[c])
            dict['households'].append(int(sheet.cell_value(rownames_index[c],index_estimate[x]).replace(',','')))

    ###Create output file
    dfs = [pd.DataFrame(dict,columns=['location_id','housevalue_range', 'households'])]
    excel_names, sheetnames = 'B25075_parsed.xlsx', ['HousingValue']
    return dfs, excel_names, sheetnames