def B01001_parse_age(sheet, numcols, num_rows, location_id, index_estimate):
    import pandas as pd

    #Get rows names and indices
    rownames = []
    # Get male numbers
    rownames_index_m = []
    for n in range(num_rows):
        if sheet.cell_value(n,0) == 'Male:':
            startindex = n+1
        if sheet.cell_value(n,0) == 'Female:':
            endindex = n
    for n in range(startindex,endindex):
        rownames.append(sheet.cell_value(n,0))
        rownames_index_m.append(n)

    # Get female numbers
    rownames_index_f = []
    for n in range(num_rows):
        if sheet.cell_value(n,0) == 'Female:':
            startindex = n+1
        if sheet.cell_value(n,0) == '85 years and over':
            endindex = n+1
    for n in range(startindex,endindex):
        rownames_index_f.append(n)

    # Create table
    dict = {'location_id':[],'age':[], 'people':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames)):
            dict['location_id'].append(location_id[x])
            dict['age'].append(rownames[c])
            dict['people'].append(int(sheet.cell_value(rownames_index_m[c],index_estimate[x]).replace(',','')) +
                int(sheet.cell_value(rownames_index_f[c],index_estimate[x]).replace(',','')))

    ###Create output file
    dfs = [pd.DataFrame(dict,columns=['location_id','age', 'people'])]
    excel_names, sheetnames = 'B01001_parsed.xlsx', ['Age']
    return dfs, excel_names, sheetnames







