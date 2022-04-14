
def DP05_parse_demo(sheet, num_cols, num_rows, location_id, index_estimate):
    import pandas as pd
    from WebApp.census.parse.tracts._helperfunctions import get_rowindex

    ####AGE
    #Get rows
    rownames_age = []
    rownames_age_index = []
    for n in range(num_rows):
        if sheet.cell_value(n,0) == 'Under 5 years':
            rowname_age_startindex = n
        if sheet.cell_value(n,0) == '85 years and over':
            rowname_age_endindex = n
    for n in range(rowname_age_startindex,rowname_age_endindex+1):
        rownames_age.append(sheet.cell_value(n,0))
        rownames_age_index.append(n)

    #Create table
    dict_age = {'location_id':[],'age_range':[], 'people':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_age)):
            dict_age['location_id'].append(location_id[x])
            dict_age['age_range'].append(rownames_age[c])
            dict_age['people'].append(int(sheet.cell_value(rownames_age_index[c],index_estimate[x]).replace(',','')))


    ####SEX
    #Get rows
    rownames_sex= ['Male','Female']
    rownames_sex_index = get_rowindex(sheet, num_rows, rownames_sex)

    #create table
    rownames_sex = ['Male','Female','Male','Female','Male','Female']
    rownames_sex_age = ['All Ages','All Ages','18 years and over','18 years and over','65 years and over','65 years and over']
    dict_sex = {'location_id':[],'sex':[], 'age_range':[],'people':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_sex)):
            dict_sex['location_id'].append(location_id[x])
            dict_sex['sex'].append(rownames_sex[c])
            dict_sex['age_range'].append(rownames_sex_age[c])
            dict_sex['people'].append(int(sheet.cell_value(rownames_sex_index[c],index_estimate[x]).replace(',','')))

    ####RACE
    #Get rows
    rownames_race_index = []
    rownames_race = ['Two or more races', 'White','Black or African American','American Indian and Alaska Native','Asian','Native Hawaiian and Other Pacific Islander',
    'Some other race']
    for n in range(num_rows):
        if sheet.cell_value(n,0) == 'Race alone or in combination with one or more other races':
            break
        elif sheet.cell_value(n,0) in rownames_race:
            rownames_race_index.append(n)

    #Create table
    dict_race = {'location_id':[],'race':[], 'race_sub':[],'people':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_race)):
            if rownames_race[c] in ['American Indian and Alaska Native','Asian','Native Hawaiian and Other Pacific Islander']:
                temp_estimate_foraian = int(sheet.cell_value(rownames_race_index[c], index_estimate[x]).replace(',', ''))
                for d in range(rownames_race_index[c]+1,rownames_race_index[c+1]):
                    dict_race['location_id'].append(location_id[x])
                    dict_race['race'].append(rownames_race[c])
                    dict_race['race_sub'].append(sheet.cell_value(d, 0))
                    dict_race['people'].append(int(sheet.cell_value(d, index_estimate[x]).replace(',', '')))
                    if rownames_race[c] == 'American Indian and Alaska Native':
                        temp_estimate_foraian -= int(sheet.cell_value(d, index_estimate[x]).replace(',', ''))
                if rownames_race[c] == 'American Indian and Alaska Native':
                    dict_race['location_id'].append(location_id[x])
                    dict_race['race'].append(rownames_race[c])
                    dict_race['race_sub'].append('Other American Indian and Alaska Native')
                    dict_race['people'].append(temp_estimate_foraian)

            else:
                dict_race['location_id'].append(location_id[x])
                dict_race['race'].append(rownames_race[c])
                dict_race['race_sub'].append('-')
                dict_race['people'].append(int(sheet.cell_value(rownames_race_index[c],index_estimate[x]).replace(',','')))

    ####HISPANIC OR LATINO AND RACE
    # Get rows
    rownames_hisp = []
    rownames_hisp_index = []
    for n in range(num_rows):
        if sheet.cell_value(n, 0) == 'Hispanic or Latino (of any race)':
            rowname_hisp_startindex = n
        if sheet.cell_value(n, 0) == 'Not Hispanic or Latino':
            rowname_hisp_endindex = n
    for n in range(rowname_hisp_startindex+1, rowname_hisp_endindex):
        rownames_hisp.append(sheet.cell_value(n, 0))
        rownames_hisp_index.append(n)

    dict_hisp = {'location_id': [], 'hispanic_latino': [], 'people': []}
    for x in range(len(location_id)):
        for c in range(len(rownames_hisp)):
            dict_hisp['location_id'].append(location_id[x])
            dict_hisp['hispanic_latino'].append(rownames_hisp[c])
            dict_hisp['people'].append(int(sheet.cell_value(rownames_hisp_index[c], index_estimate[x]).replace(',', '')))

    ####Create output file
    df_age = pd.DataFrame(dict_age,columns=['location_id','age_range','people'])
    df_sex = pd.DataFrame(dict_sex,columns=['location_id','sex','age_range','people'])
    df_race = pd.DataFrame(dict_race,columns=['location_id','race','race_sub','people'])
    df_hisp = pd.DataFrame(dict_hisp, columns=['location_id', 'hispanic_latino', 'people'])
    dfs = [df_age, df_sex, df_race, df_hisp]
    excelname, sheetnames = 'DP05_parsed.xlsx', ['Age', 'Sex', 'Race', 'HispanicOrLatino']
    return dfs, excelname, sheetnames
