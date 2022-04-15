def B25003_parse_housingtenure_house(sheet, numcols, num_rows, location_id, index_estimate):
    import pandas as pd

    #Get rows names and indices
    rownames = ['Owner occupied','Renter occupied']
    rownames_index = [n for n in range(num_rows) if sheet.cell_value(n, 0) in rownames]

    # Create table
    dict = {'location_id':[],'owner_renter':[], 'households':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames)):
            dict['location_id'].append(location_id[x])
            dict['owner_renter'].append(rownames[c])
            dict['households'].append(int(sheet.cell_value(rownames_index[c],index_estimate[x]).replace(',','')))

    ###Create output file
    dfs = [pd.DataFrame(dict,columns=['location_id','owner_renter', 'households'])]
    excel_names, sheetnames = 'B25003_parsed.xlsx', ['HousingTenure']
    return dfs, excel_names, sheetnames