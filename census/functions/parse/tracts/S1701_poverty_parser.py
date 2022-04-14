
def S1701_parse_poverty(sheet, num_cols, num_rows, location_id, index_estimate):
    import pandas as pd
    dfs = []

    ####SET UP
    #Get census tract names
    location_id_unprocessed = [sheet.cell_value(0,n) for n in range(num_cols) if sheet.cell_value(0,n) != '']
    index_estimate = [n for n in range(num_cols) if sheet.cell_value(1,n) == 'Total']
    index_estimate_pov = [n for n in range(num_cols) if sheet.cell_value(1,n) == 'Below poverty level']

    rownames_pov = ['Below poverty level', 'At or above poverty level']

    ### DEFINE MAIN FUNCTION
    def pov_characteristics(rownames,characteristic, location_id, rownames_pov, index_estimate, index_estimate_pov, dfs):
        rownames_index = [n for n in range(num_rows) if sheet.cell_value(n, 0) in rownames]
        dict = {'location_id': [], characteristic: [], 'poverty': [], 'people': []}
        for x in range(len(location_id)):
            for c in range(len(rownames)):
                for d in range(len(rownames_pov)):
                    dict['location_id'].append(location_id[x])
                    dict[characteristic].append(rownames[c])
                    if rownames_pov[d] == 'Below poverty level':
                        dict['poverty'].append(rownames_pov[d])
                        dict['people'].append(int(sheet.cell_value(rownames_index[c], index_estimate_pov[x]).replace(',', '')))
                    else:
                        dict['poverty'].append(rownames_pov[d])
                        not_pov = int(sheet.cell_value(rownames_index[c], index_estimate[x]).replace(',', '')) - \
                                  int(sheet.cell_value(rownames_index[c], index_estimate_pov[x]).replace(',', ''))
                        dict['people'].append(not_pov)
        dfs = dfs.append(pd.DataFrame(dict,columns=['location_id',characteristic, 'poverty','people']))

    # by age
    rownames_age = ['Under 5 years', '5 to 17 years', '18 to 34 years', '35 to 64 years', '65 years and over']
    pov_characteristics(rownames_age, 'age', location_id, rownames_pov, index_estimate, index_estimate_pov, dfs)

    # by sex
    rownames_sex = ['Male','Female']
    pov_characteristics(rownames_sex, 'sex', location_id, rownames_pov, index_estimate, index_estimate_pov, dfs)

    # poverty by race
    rownames_race = ['White alone', 'Black or African American alone', 'American Indian and Alaska Native alone','Asian alone',
                     'Native Hawaiian and Other Pacific Islander alone', 'Some other race alone', 'Two or more races']
    pov_characteristics(rownames_race, 'race', location_id, rownames_pov, index_estimate, index_estimate_pov, dfs)

    # by education
    rownames_edu = ['Less than high school graduate','High school graduate (includes equivalency)',"Some college, associate's degree",
                    "Bachelor's degree or higher"]
    pov_characteristics(rownames_edu, 'education', location_id, rownames_pov, index_estimate, index_estimate_pov, dfs)

    # by employment
    rownames_emp = ['Employed','Unemployed']
    pov_characteristics(rownames_emp, 'employment', location_id, rownames_pov, index_estimate, index_estimate_pov, dfs)

    # by work experience
    rownames_work = ['Worked full-time, year-round in the past 12 months','Worked part-time or part-year in the past 12 months','Did not work']
    pov_characteristics(rownames_work, 'work_experience', location_id, rownames_pov, index_estimate, index_estimate_pov, dfs)

    ### CREATE OUTPUT FILE
    excel_name, sheetnames = 'S1701_parsed.xlsx', ['PovertyByAge','PovertyBySex','PovertyByRace','PovertyByEducation',
                                                   'PovertyByEmployment','PovertyByWorkExperience']
    return dfs, excel_name, sheetnames