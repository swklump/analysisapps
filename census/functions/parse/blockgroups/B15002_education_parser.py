def B15002_parse_edu(sheet, numcols, num_rows, location_id, index_estimate):
    import pandas as pd

    #Get rows names and indices
    rownames = []
    rownames_index = []
    for n in range(num_rows):
        if sheet.cell_value(n,0) == 'Male:':
            startindex = n+1
        if sheet.cell_value(n,0) == 'Female:':
            endindex = n
    for n in range(startindex,endindex):
        rownames.append(sheet.cell_value(n,0))
        rownames_index.append(n)

    # Create table
    dict = {'location_id':[],'education':[], 'sex':[],'people_25':[]}
    for x in range(len(location_id)):
        for c in range(0,2):
            # Male
            if c == 0:
                for d in range(len(rownames)):
                    dict['location_id'].append(location_id[x])
                    dict['education'].append(rownames[d])
                    dict['sex'].append('Male')
                    dict['people_25'].append(int(sheet.cell_value(rownames_index[d],index_estimate[x]).replace(',','')))
            # Female
            else:
                for d in range(len(rownames)):
                    dict['location_id'].append(location_id[x])
                    dict['education'].append(rownames[d])
                    dict['sex'].append('Female')
                    dict['people_25'].append(int(sheet.cell_value(rownames_index[d]+17,index_estimate[x]).replace(',','')))


    ###Create output file
    dfs = [pd.DataFrame(dict,columns=['location_id','education', 'sex','people_25'])]
    excel_names, sheetnames = 'B15002_parsed.xlsx', ['Education']
    return dfs, excel_names, sheetnames