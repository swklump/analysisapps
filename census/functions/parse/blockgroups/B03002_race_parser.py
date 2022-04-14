def B03002_parse_race(sheet, numcols, num_rows, location_id, index_estimate):
    import pandas as pd

    #Get rows names and indices
    rownames, rownames_index = [], []
    for n in range(num_rows):
        if sheet.cell_value(n,0) == 'Not Hispanic or Latino:':
            startindex = n+1
        if sheet.cell_value(n,0) == 'Hispanic or Latino:':
            endindex = n
    for n in range(startindex,endindex):
        rownames.append(sheet.cell_value(n,0))
        rownames_index.append(n)
    rownames, rownames_index = rownames[:-2], rownames_index[:-2]
    # Get subcategory row names
    rownames_sub = ['Two races including Some other race', 'Two races excluding Some other race, and three or more races']
    rownames_sub_index = [n for n in range(num_rows) if sheet.cell_value(n, 0) in rownames_sub][0:2]

    # Create table
    dict = {'location_id':[],'hisp_latino':[],'race':[], 'race_sub':[],'people':[]}
    for x in range(len(location_id)):
        for c in range(0, 2):
            # Not hispanic
            if c==0:
                for c in range(len(rownames)):
                    if rownames[c] == 'Two or more races:':
                        for d in range(len(rownames_sub_index)):
                            dict['location_id'].append(location_id[x])
                            dict['hisp_latino'].append('Not Hispanic or Latino')
                            dict['race'].append(rownames[c])
                            dict['race_sub'].append(rownames_sub[d])
                            dict['people'].append(int(sheet.cell_value(rownames_sub_index[d], index_estimate[x]).replace(',', '')))
                    else:
                        dict['location_id'].append(location_id[x])
                        dict['hisp_latino'].append('Not Hispanic or Latino')
                        dict['race'].append(rownames[c])
                        dict['race_sub'].append('-')
                        dict['people'].append(int(sheet.cell_value(rownames_index[c],index_estimate[x]).replace(',','')))

            # Hispanic/Latino
            else:
                for c in range(len(rownames)):
                    if rownames[c] == 'Two or more races:':
                        for d in range(len(rownames_sub_index)):
                            dict['location_id'].append(location_id[x])
                            dict['hisp_latino'].append('Hispanic or Latino')
                            dict['race'].append(rownames[c])
                            dict['race_sub'].append(rownames_sub[d])
                            dict['people'].append(int(sheet.cell_value(rownames_sub_index[d]+10, index_estimate[x]).replace(',', '')))
                    else:
                        dict['location_id'].append(location_id[x])
                        dict['hisp_latino'].append('Hispanic or Latino')
                        dict['race'].append(rownames[c])
                        dict['race_sub'].append('-')
                        dict['people'].append(int(sheet.cell_value(rownames_index[c]+10,index_estimate[x]).replace(',','')))


    ###Create output file
    dfs = [pd.DataFrame(dict,columns=['location_id','hisp_latino','race', 'race_sub', 'people'])]
    excel_names, sheetnames = 'B03002_parsed.xlsx', ['Race']
    return dfs, excel_names, sheetnames