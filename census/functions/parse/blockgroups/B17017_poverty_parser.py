def B17017_parse_poverty(sheet, numcols, num_rows, location_id, index_estimate):
    import pandas as pd

    #Get rows names and indices
    rownames_poverty = ['Income in the past 12 months below poverty level:','Income in the past 12 months at or above poverty level:']
    rownames_housetype = ['Family households:', 'Nonfamily households:']
    rownames_housetype_sub = ['Married-couple family:','Other family:', 'Male householder:','Female householder:']
    rownames_housetype_sub_index = [n for n in range(num_rows) if sheet.cell_value(n, 0) in rownames_housetype_sub]

    # 2019 onward uses "spouse", prior uses "wife" and "husband"
    rownames_housetype_sub11 = ['Male householder, no spouse present:', 'Female householder, no spouse present:']
    rownames_housetype_sub12 = ['Male householder, no wife present:', 'Female householder, no husband present:']
    whichsub = 1
    for n in range(num_rows):
        if sheet.cell_value(n, 0) in rownames_housetype_sub12:
            whichsub = 2
    if whichsub == 1:
        rownames_housetype_sub1 = rownames_housetype_sub11
    else:
        rownames_housetype_sub1 = rownames_housetype_sub12
    rownames_housetype_sub1_index = [n for n in range(num_rows) if sheet.cell_value(n, 0) in rownames_housetype_sub1]


    # Create table
    dict = {'location_id':[],'pov_level':[], 'household_type':[], 'household_type_sub':[], 'household_type_sub1':[], 'householder_age': [], 'households':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_poverty)):
            for d in range(len(rownames_housetype)):
                if rownames_housetype[d] == 'Family households:':
                    for e in range(0,2):
                        if rownames_housetype_sub[e] == 'Other family:':
                            for f in range(len(rownames_housetype_sub1)):
                                for s in range(1, 5):
                                    m = s
                                    if c != 0:
                                        m += 29
                                    dict['location_id'].append(location_id[x])
                                    dict['pov_level'].append(rownames_poverty[c])
                                    dict['household_type'].append(rownames_housetype[d])
                                    dict['household_type_sub'].append(rownames_housetype_sub[e])
                                    dict['household_type_sub1'].append(rownames_housetype_sub1[f])
                                    dict['householder_age'].append(sheet.cell_value(rownames_housetype_sub1_index[f] + m, 0))
                                    dict['households'].append(int(sheet.cell_value(rownames_housetype_sub1_index[f] + m, index_estimate[x]).replace(',', '')))
                        else:
                            for s in range(1,5):
                                m = s
                                if c != 0:
                                    m += 29
                                dict['location_id'].append(location_id[x])
                                dict['pov_level'].append(rownames_poverty[c])
                                dict['household_type'].append(rownames_housetype[d])
                                dict['household_type_sub'].append(rownames_housetype_sub[e])
                                dict['household_type_sub1'].append('-')
                                dict['householder_age'].append(sheet.cell_value(rownames_housetype_sub_index[e]+m,0))
                                dict['households'].append(int(sheet.cell_value(rownames_housetype_sub_index[e]+m,index_estimate[x]).replace(',','')))
                else:
                    for e in range(2,4):
                        if rownames_housetype_sub[e] == 'Other family:':
                            for f in range(len(rownames_housetype_sub1)):
                                for s in range(1, 5):
                                    m = s
                                    if c != 0:
                                        m += 29
                                    dict['location_id'].append(location_id[x])
                                    dict['pov_level'].append(rownames_poverty[c])
                                    dict['household_type'].append(rownames_housetype[d])
                                    dict['household_type_sub'].append(rownames_housetype_sub[e])
                                    dict['household_type_sub1'].append(rownames_housetype_sub1[f])
                                    dict['householder_age'].append(sheet.cell_value(rownames_housetype_sub1_index[f] + m, 0))
                                    dict['households'].append(int(sheet.cell_value(rownames_housetype_sub1_index[f] + m,index_estimate[x]).replace(',', '')))
                        else:
                            for s in range(1, 5):
                                m = s
                                if c != 0:
                                    m += 29
                                dict['location_id'].append(location_id[x])
                                dict['pov_level'].append(rownames_poverty[c])
                                dict['household_type'].append(rownames_housetype[d])
                                dict['household_type_sub'].append(rownames_housetype_sub[e])
                                dict['household_type_sub1'].append('-')
                                dict['householder_age'].append(sheet.cell_value(rownames_housetype_sub_index[e] + m, 0))
                                dict['households'].append(int(sheet.cell_value(rownames_housetype_sub_index[e] + m, index_estimate[x]).replace(',', '')))

    ###Create output file
    dfs = [pd.DataFrame(dict,columns=['location_id','pov_level', 'household_type', 'household_type_sub', 'household_type_sub1', 'householder_age', 'households']).replace({':': ''}, regex=True)]
    excel_names, sheetnames = 'B17017_parsed.xlsx', ['Poverty']
    return dfs, excel_names, sheetnames