def B25034_parse_houseage(sheet, numcols, num_rows, location_id, index_estimate):
    import pandas as pd

    # Create table
    dict = {'location_id':[],'house_age':[], 'houses':[]}
    for x in range(len(location_id)):
        for c in range(3,num_rows):
            dict['location_id'].append(location_id[x])
            dict['house_age'].append(sheet.cell_value(c,0))
            dict['houses'].append(int(sheet.cell_value(c,index_estimate[x]).replace(',','')))

    ###Create output file
    dfs = [pd.DataFrame(dict,columns=['location_id','house_age', 'houses'])]
    excel_names, sheetnames = 'B25034_parsed.xlsx', ['HousesByAge']
    return dfs, excel_names, sheetnames