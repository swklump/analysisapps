def S1810_parse_disab(sheet, num_cols, num_rows, location_id, index_estimate):
    import pandas as pd

    rownames_disabled = ['With a disability', 'Without a disability']
    dfs = []

    ####SET UP
    #Get census tract names
    location_id_unprocessed = [sheet.cell_value(0, n) for n in range(num_cols) if sheet.cell_value(0, n) != '']
    index_estimate = [n for n in range(num_cols) if sheet.cell_value(1, n) == 'Total']
    index_estimate_disab = [n for n in range(num_cols) if sheet.cell_value(1, n) == 'With a disability']

    ####DIFFICULTIES
    #Get rows
    rownames_disability = ['With a hearing difficulty','With a vision difficulty','With a cognitive difficulty','With an ambulatory difficulty','With a self-care difficulty',
    'With an independent living difficulty',]
    rownames_disability_index = []
    rownames_disability_age = ['Population under 5 years', 'Population 5 to 17 years', 'Population 18 to 34 years','Population 35 to 64 years','Population 65 to 74 years','Population 75 years and over']

    for n in range(num_rows):
        for r in range(len(rownames_disability)):
            if sheet.cell_value(n,0) == rownames_disability[r]:
                rownames_disability_index.append(n)

        if sheet.cell_value(n,0) == 'Total civilian noninstitutionalized population':
            row_disab_index = n
    rownames_disability_index.append(num_rows)

    #Create table
    dict_disability = {'location_id':[],'difficulty':[], 'age_range':[], 'people':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_disability)):
            for r in range(len(rownames_disability_age)):
                dict_disability['location_id'].append(location_id[x])
                dict_disability['difficulty'].append(rownames_disability[c])
                dict_disability['age_range'].append(rownames_disability_age[r])

                not_there = ''
                for d in range(rownames_disability_index[c],rownames_disability_index[c+1]):
                    if sheet.cell_value(d,0) == rownames_disability_age[r]:
                        dict_disability['people'].append(int(sheet.cell_value(d,index_estimate[x]).replace(',','')))
                        not_there = 'there'
                if not_there == '':
                    dict_disability['people'].append(0)
    dfs.append(pd.DataFrame(dict_disability,columns=['location_id','difficulty', 'age_range','people']))


    ### DEFINE MAIN FUNCTION
    def disab_characteristics(rownames,characteristic, location_id, rownames_disabled, index_estimate, index_estimate_disab, dfs):
        rownames_index = [n for n in range(num_rows) if sheet.cell_value(n, 0) in rownames]
        dict = {'location_id': [], characteristic: [], 'disability': [], 'people': []}
        for x in range(len(location_id)):
            for c in range(len(rownames)):
                for d in range(len(rownames_disabled)):
                    dict['location_id'].append(location_id[x])
                    dict[characteristic].append(rownames[c])
                    if rownames_disabled[d] == 'With a disability':
                        dict['disability'].append(rownames_disabled[d])
                        dict['people'].append(int(sheet.cell_value(rownames_index[c], index_estimate_disab[x]).replace(',', '')))
                    else:
                        dict['disability'].append(rownames_disabled[d])
                        not_disab = int(sheet.cell_value(rownames_index[c], index_estimate[x]).replace(',', '')) - \
                                  int(sheet.cell_value(rownames_index[c], index_estimate_disab[x]).replace(',', ''))
                        dict['people'].append(not_disab)
        dfs = dfs.append(pd.DataFrame(dict,columns=['location_id',characteristic, 'disability','people']))

    # by sex
    rownames_sex = ['Male','Female']
    disab_characteristics(rownames_sex, 'sex', location_id, rownames_disabled, index_estimate, index_estimate_disab, dfs)

    # dby race
    rownames_race = ['White alone', 'Black or African American alone','American Indian and Alaska Native alone','Asian alone','Native Hawaiian and Other Pacific Islander alone','Some other race alone','Two or more races']
    disab_characteristics(rownames_race, 'race', location_id, rownames_disabled, index_estimate, index_estimate_disab, dfs)

    # by age
    rownames_age = ['Under 5 years','5 to 17 years','18 to 34 years','35 to 64 years','65 to 74 years','75 years and over']
    disab_characteristics(rownames_age, 'age', location_id, rownames_disabled, index_estimate, index_estimate_disab, dfs)

    ### CREATE OUTPUT FILE
    excel_name, sheetnames = 'S1810_parsed.xlsx', ['Difficulties','DisabilitiesBySex','DisabilitiesByRace','DisabilitiesByAge']
    return dfs, excel_name, sheetnames