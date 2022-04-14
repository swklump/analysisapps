def C21007_parse_disab(sheet, numcols, num_rows, location_id, index_estimate):
    import pandas as pd

    # Get row indices
    rownames_age = ['18 to 64 years:', '65 years and over:']
    rownames_vet = ['Veteran:', 'Nonveteran:']
    rownames_pov = ['Income in the past 12 months below poverty level:', 'Income in the past 12 months at or above poverty level:']
    rownames_disab = ['With a disability', 'No disability']
    rownames_disab_index = [n for n in range(num_rows) if sheet.cell_value(n, 0) in rownames_disab]

    # Create table
    dict = {'location_id':[], 'age':[], 'veteran_status':[], 'poverty_level':[], 'disability':[],'people_18':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_age)):
            for d in range(len(rownames_vet)):
                for e in range(len(rownames_pov)):
                    for f in range(len(rownames_disab)):
                        dict['location_id'].append(location_id[x])
                        dict['age'].append(rownames_age[c])
                        dict['veteran_status'].append(rownames_vet[d])
                        dict['poverty_level'].append(rownames_pov[e])
                        dict['disability'].append(rownames_disab[f])
        for g in range(len(rownames_disab_index)):
            dict['people_18'].append(int(sheet.cell_value(rownames_disab_index[g], index_estimate[x]).replace(',','')))

    ###Create output file
    dfs = [pd.DataFrame(dict,columns=['location_id','age','veteran_status','poverty_level','disability','people_18']).replace({':': ''}, regex=True)]
    excel_names, sheetnames = 'C21007_parsed.xlsx', ['Disability']
    return dfs, excel_names, sheetnames