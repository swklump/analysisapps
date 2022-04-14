def S1501_parse_education(sheet, num_cols, num_rows, location_id, index_estimate):
    import pandas as pd

    # Get indexes for male and female
    index_estimate_male = [n for n in range(num_cols) if sheet.cell_value(1, n) == 'Male']
    index_estimate_female = [n for n in range(num_cols) if sheet.cell_value(1, n) == 'Female']

    dfs = []
    # Define rownames
    rownames_age = ['Population 18 to 24 years','Population 25 to 34 years','Population 35 to 44 years',
                    'Population 45 to 64 years','Population 65 years and over']
    rownames_race = ['White alone','White alone, not Hispanic or Latino','Black alone','American Indian or Alaska Native alone','Asian alone',
                     'Native Hawaiian and Other Pacific Islander alone','Some other race alone','Two or more races']
    rownames_edu = ['High school graduate or higher',"Bachelor's degree or higher"]

    ### DEFINE MAIN FUNCTION
    def education_characteristics(rownames, characteristic, location_id, index_estimate, index_estimate_male, dfs, rownames_edu):
        rownames_index = [n for n in range(num_rows) if sheet.cell_value(n, 0) in rownames]
        dict = {'location_id': [], characteristic: [], 'education': [], 'sex':[],'people': []}
        for x in range(len(location_id)):
            for c in range(len(rownames)):
                if rownames[c] == 'Population 18 to 24 years':
                    for f in range(1,5):
                        for g in range(0,2):
                            dict['location_id'].append(location_id[x])
                            dict[characteristic].append(rownames[c])
                            dict['education'].append(sheet.cell_value(rownames_index[c]+f, 0))
                            if g == 0:
                                dict['sex'].append('Male')
                                dict['people'].append(int(sheet.cell_value(rownames_index[c]+f, index_estimate_male[x]).replace(',', '')))
                            else:
                                dict['sex'].append('Female')
                                dict['people'].append(int(sheet.cell_value(rownames_index[c] + f, index_estimate_female[x]).replace(',','')))

                elif rownames[c] == 'White alone':
                    for d in range(0, 3):
                        for h in range(0, 2):
                            dict['location_id'].append(location_id[x])
                            dict[characteristic].append('White alone, Hispanic or Latino')

                            if h == 0:
                                dict['sex'].append('Male')
                                # all white
                                total_cat_all_white = int(sheet.cell_value(rownames_index[c], index_estimate_male[x]).replace(',', ''))
                                hs_all_white = int(sheet.cell_value(rownames_index[c] + 1, index_estimate_male[x]).replace(',', ''))
                                bachelors_all_white = int(sheet.cell_value(rownames_index[c] + 2, index_estimate_male[x]).replace(',', ''))

                                # non hispanic white
                                total_cat_nonhisp = int(sheet.cell_value(rownames_index[c+1], index_estimate_male[x]).replace(',', ''))
                                hs_nonhisp = int(sheet.cell_value(rownames_index[c+1] + 1, index_estimate_male[x]).replace(',', ''))
                                bachelors_nonhisp = int(sheet.cell_value(rownames_index[c+1] + 2, index_estimate_male[x]).replace(',', ''))

                            else:
                                dict['sex'].append('Female')
                                # all white
                                total_cat_all_white = int(sheet.cell_value(rownames_index[c], index_estimate_female[x]).replace(',', ''))
                                hs_all_white = int(sheet.cell_value(rownames_index[c] + 1, index_estimate_female[x]).replace(',', ''))
                                bachelors_all_white = int(sheet.cell_value(rownames_index[c] + 2, index_estimate_female[x]).replace(',', ''))

                                # non hispanic white
                                total_cat_nonhisp = int(sheet.cell_value(rownames_index[c + 1], index_estimate_female[x]).replace(',', ''))
                                hs_nonhisp = int(sheet.cell_value(rownames_index[c + 1] + 1, index_estimate_female[x]).replace(',',''))
                                bachelors_nonhisp = int(sheet.cell_value(rownames_index[c + 1] + 2, index_estimate_female[x]).replace(',',''))

                            # hispanic white
                            total_cat = total_cat_all_white - total_cat_nonhisp
                            hs = hs_all_white - hs_nonhisp
                            bachelors = bachelors_all_white - bachelors_nonhisp
                            if d == 0:
                                dict['education'].append('Less than high school graduate')
                                dict['people'].append(total_cat - hs)
                            elif d == 1:
                                dict['education'].append("Between high school graduate and bachelor's degree")
                                dict['people'].append(hs - bachelors)
                            elif d == 2:
                                dict['education'].append("Bachelor's degree or higher")
                                dict['people'].append(bachelors)

                else:
                    for d in range(0,3):
                        for h in range(0,2):
                            dict['location_id'].append(location_id[x])
                            dict[characteristic].append(rownames[c])
                            if h == 0:
                                total_cat = int(sheet.cell_value(rownames_index[c], index_estimate_male[x]).replace(',', ''))
                                hs = int(sheet.cell_value(rownames_index[c]+1, index_estimate_male[x]).replace(',', ''))
                                bachelors = int(sheet.cell_value(rownames_index[c]+2, index_estimate_male[x]).replace(',', ''))
                                dict['sex'].append('Male')
                            else:
                                total_cat = int(sheet.cell_value(rownames_index[c], index_estimate_female[x]).replace(',', ''))
                                hs = int(sheet.cell_value(rownames_index[c] + 1, index_estimate_female[x]).replace(',', ''))
                                bachelors = int(sheet.cell_value(rownames_index[c] + 2, index_estimate_female[x]).replace(',', ''))
                                dict['sex'].append('Female')
                            if d == 0:
                                dict['education'].append('Less than high school graduate')
                                dict['people'].append(total_cat - hs)
                            elif d == 1:
                                dict['education'].append("Between high school graduate and bachelor's degree")
                                dict['people'].append(hs - bachelors)
                            elif d == 2:
                                dict['education'].append("Bachelor's degree or higher")
                                dict['people'].append(bachelors)

        dfs = dfs.append(pd.DataFrame(dict, columns=['location_id', characteristic, 'education', 'sex','people']))

    # by age
    education_characteristics(rownames_age, 'age', location_id, index_estimate,index_estimate_male, dfs, rownames_edu)

    # by race
    education_characteristics(rownames_race, 'race', location_id,index_estimate,index_estimate_male, dfs, rownames_edu)

    # median earnings
    rowname_startindex = [n for n in range(num_rows) if sheet.cell_value(n, 0) == 'MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)']
    rownames_index = list(range(rowname_startindex[0]+2,num_rows))
    dict = {'location_id': [], 'education': [], 'sex':[], 'median_earnings': []}
    for x in range(len(location_id)):
        for c in range(len(rownames_index)):
            for d in range(0,3):
                dict['location_id'].append(location_id[x])
                dict['education'].append(sheet.cell_value(rownames_index[c], 0))
                if d == 0:
                    dict['sex'].append('Male')
                    if sheet.cell_value(rownames_index[c], index_estimate_male[x]) == '-':
                        dict['median_earnings'].append('')
                    elif '-' in sheet.cell_value(rownames_index[c], index_estimate_male[x]):
                        dict['median_earnings'].append(int(sheet.cell_value(rownames_index[c], index_estimate_male[x]).replace('-','').replace(',', '')))
                    else:
                        dict['median_earnings'].append(int(sheet.cell_value(rownames_index[c], index_estimate_male[x]).replace(',', '')))
                elif d == 1:
                    dict['sex'].append('Female')
                    if sheet.cell_value(rownames_index[c], index_estimate_female[x]) == '-':
                        dict['median_earnings'].append('')
                    elif '-' in sheet.cell_value(rownames_index[c], index_estimate_female[x]):
                        dict['median_earnings'].append(int(sheet.cell_value(rownames_index[c], index_estimate_female[x]).replace('-','').replace(',', '')))
                    else:
                        dict['median_earnings'].append(int(sheet.cell_value(rownames_index[c], index_estimate_female[x]).replace(',', '')))
                else:
                    dict['sex'].append('All')
                    if sheet.cell_value(rownames_index[c], index_estimate[x]) == '-':
                        dict['median_earnings'].append('')
                    elif '-' in sheet.cell_value(rownames_index[c], index_estimate[x]):
                        dict['median_earnings'].append(int(sheet.cell_value(rownames_index[c], index_estimate[x]).replace('-','').replace(',', '')))
                    else:
                        dict['median_earnings'].append(int(sheet.cell_value(rownames_index[c], index_estimate[x]).replace(',', '')))
    dfs.append(pd.DataFrame(dict, columns=['location_id', 'education', 'sex','median_earnings']))


    ### CREATE OUTPUT FILE
    excel_name, sheetnames = 'S1501_parsed.xlsx', ['EducationByAge','EducationByRace','MedianEarningsByEducation']
    return dfs, excel_name, sheetnames