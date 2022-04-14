def B08134_parse_commute(sheet, numcols, num_rows, location_id, index_estimate):
    import pandas as pd

    #Get rows names and indices
    rownames_mode = ['Car, truck, or van:','Public transportation (excluding taxicab):','Walked:','Taxicab, motorcycle, bicycle, or other means:']
    rownames_mode_sub = ['Drove alone:','Carpooled:']
    rownames_mode_sub1 = ['In 2-person carpool:', 'In 3-or-more-person carpool:']
    rownames_mode_index = [n for n in range(num_rows) if sheet.cell_value(n, 0) in rownames_mode]
    rownames_mode_sub_index = [n for n in range(num_rows) if sheet.cell_value(n, 0) in rownames_mode_sub]
    rownames_mode_sub1_index = [n for n in range(num_rows) if sheet.cell_value(n, 0) in rownames_mode_sub1]

    # Create table
    dict = {'location_id':[],'commute_mode':[],'commute_mode_sub':[], 'commute_mode_sub1':[],'travel_time':[], 'workers_16_nothome':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_mode)):
            if rownames_mode[c] == 'Car, truck, or van:':
                for d in range(len(rownames_mode_sub)):
                    if rownames_mode_sub[d] == 'Carpooled:':
                        for e in range(len(rownames_mode_sub1)):
                            for s in range(1, 10):
                                dict['location_id'].append(location_id[x])
                                dict['commute_mode'].append(rownames_mode[c])
                                dict['commute_mode_sub'].append(rownames_mode_sub[d])
                                dict['commute_mode_sub1'].append(rownames_mode_sub1[e])
                                dict['travel_time'].append(sheet.cell_value(rownames_mode_sub1_index[c]+s, 0))
                                dict['workers_16_nothome'].append(int(sheet.cell_value(rownames_mode_sub1_index[e]+s, index_estimate[x]).replace(',', '')))
                    else:
                        for s in range(1, 10):
                            dict['location_id'].append(location_id[x])
                            dict['commute_mode'].append(rownames_mode[c])
                            dict['commute_mode_sub'].append(rownames_mode_sub[d])
                            dict['commute_mode_sub1'].append('-')
                            dict['travel_time'].append(sheet.cell_value(rownames_mode_sub_index[c] + s, 0))
                            dict['workers_16_nothome'].append(int(sheet.cell_value(rownames_mode_sub_index[d]+s, index_estimate[x]).replace(',', '')))
            else:
                for s in range(1,10):
                    dict['location_id'].append(location_id[x])
                    dict['commute_mode'].append(rownames_mode[c])
                    dict['commute_mode_sub'].append('-')
                    dict['commute_mode_sub1'].append('-')
                    dict['travel_time'].append(sheet.cell_value(rownames_mode_index[c]+s,0))
                    dict['workers_16_nothome'].append(int(sheet.cell_value(rownames_mode_index[c]+s,index_estimate[x]).replace(',','')))

    ###Create output file
    dfs = [pd.DataFrame(dict,columns=['location_id','commute_mode', 'commute_mode_sub', 'commute_mode_sub1','travel_time','workers_16_nothome']).replace({':': ''}, regex=True)]
    excel_names, sheetnames = 'B08134_parsed.xlsx', ['Commute']
    return dfs, excel_names, sheetnames