def analyze_tract(unzipped, cats_dict, checks_groups, checks_calcs, zs, tablenames_tracts, fnames):

    # Imports
    import xlrd, xlsxwriter, glob
    import pandas as pd
    from pandas.plotting import scatter_matrix
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    dfs, sheetnames = [], []
    keep_index = []

    # Create empty final data frame
    df_compiled = pd.DataFrame()
    # Create dictionary of source file data frames
    dict_dfs = {}

    # Gets all tract-block groups from each file
    all_tract = []
    for b in range(len(tablenames_tracts)):
        df = pd.read_excel(unzipped.open(fnames[b], 'r'), dtype={'location_id': object}, sheet_name=None)
        dict_dfs[tablenames_tracts[b]] = df
        for x in df.keys():
            if x == 'FileDetails':
                pass
            else:
                for y in df[x]['location_id']:
                    all_tract.append(y)
    df_compiled['location_id'] = sorted(list(set(all_tract)))

    # Define table analysis functions
    def analyze_DP04(c):
        df_DP04_value = dict_dfs[b]['HousingValue'][dict_dfs[b]['HousingValue']['location_id'] == df_compiled['location_id'][c]]
        df_DP04_tenure = dict_dfs[b]['HousingTenure'][dict_dfs[b]['HousingTenure']['location_id'] == df_compiled['location_id'][c]]

        # Housing Value
        if cats_dict['lowhousevalue'] != "dontinclude":
            # Total households
            df_compiled.at[c, 'house_tot'] = df_DP04_tenure['houses'].sum()
            cats_housevalue = ['Less than $50,000','$50,000 to $99,999']
            if cats_dict['lowhousevalue'] != "dontinclude":
                if cats_dict['lowhousevalue'] == '50k':
                    cats_housevalue = list(set(cats_housevalue) - set(['$50,000 to $99,999']))
                    df_compiled.at[c, 'house_lowhousevalue'] = df_DP04_value[df_DP04_value['value'].isin(cats_housevalue)]['houses'].sum()
                elif cats_dict['lowhousevalue'] == '100k':
                    df_compiled.at[c, 'house_lowhousevalue'] = df_DP04_value[df_DP04_value['value'].isin(cats_housevalue)]['houses'].sum()
                df_compiled.at[c, 'house_lowhousevalue_%'] = (df_compiled['house_lowhousevalue'][c] / df_compiled['house_tot'][c]).round(3)

        # Renter
        if 'renter' in checks_groups:
            # Total households
            df_compiled.at[c, 'house_tot'] = df_DP04_tenure['houses'].sum()
            df_compiled.at[c, 'house_renter'] = df_DP04_tenure[df_DP04_tenure['housing_tenure']=='Renter-occupied']['houses'].sum()
            df_compiled.at[c, 'house_renter_%'] = (df_compiled['house_renter'][c] / df_compiled['house_tot'][c]).round(3)

    def analyze_DP05(c):
        if cats_dict['elderly'] != "dontinclude":
            df_DP05_age = dict_dfs[b]['Age'][dict_dfs[b]['Age']['location_id'] == df_compiled['location_id'][c]]
            df_DP05_race = dict_dfs[b]['Race'][dict_dfs[b]['Race']['location_id'] == df_compiled['location_id'][c]]

            # Total population
            df_compiled.at[c, 'pop_tot'] = df_DP05_age['people'].sum()

            # Elderly
            cats_elderly = ['60 to 64 years','65 to 74 years','75 to 84 years','85 years and over']

            if cats_dict['elderly'] == '60yr':
                pass
            elif cats_dict['elderly'] == '65yr':
                cats_elderly = list(set(cats_elderly) - set(['60 to 64 years']))
            elif cats_dict['elderly'] == '75yr':
                cats_elderly = list(set(cats_elderly) - set(['60 to 64 years', '65 to 74 years']))
            df_compiled.at[c, 'pop_elderly'] = df_DP05_age[df_DP05_age['age_range'].isin(cats_elderly)]['people'].sum()
            df_compiled.at[c, 'pop_elderly_%'] = (df_compiled['pop_elderly'][c] / df_compiled['pop_tot'][c]).round(3)

        # People of Color
        if 'poc' in checks_groups:
            df_compiled.at[c, 'pop_poc'] = df_DP05_race[df_DP05_race['race'] != 'White']['people'].sum()
            df_compiled.at[c, 'pop_poc_%'] = (df_compiled['pop_poc'][c] / df_compiled['pop_tot'][c]).round(3)

    def analyze_S0801(c):
        if cats_dict['nondriver'] != "dontinclude":
            df_S0801_transmode = dict_dfs[b]['TransportationMode'][dict_dfs[b]['TransportationMode']['location_id'] == df_compiled['location_id'][c]]

            # Workers age 16 and older and that do not work from home
            df_compiled.at[c, 'workers_16_nothome_tot'] = df_S0801_transmode['workers_16_nothome'].sum()

            # Nondrivers to work
            if cats_dict['nondriver'] == 'nondriver':
                df_compiled.at[c, 'pop_nondriver'] = df_S0801_transmode[df_S0801_transmode['transpo_mode'] != 'Car, truck, or van']['workers_16_nothome'].sum()
            elif cats_dict['nondriver'] == 'carpool':
                df_compiled.at[c, 'pop_nondriver'] = df_S0801_transmode[df_S0801_transmode['transpo_mode_sub'].isin(['Carpooled', '-'])]['workers_16_nothome'].sum()

            df_compiled.at[c, 'pop_nondriver_%'] = (df_compiled['pop_nondriver'][c] / df_compiled['workers_16_nothome_tot'][c]).round(3)

    def analyze_S1501(c):
        if 'edu' in checks_groups:
            df_S1501_eduage = dict_dfs[b]['EducationByAge'][dict_dfs[b]['EducationByAge']['location_id'] == df_compiled['location_id'][c]]

            # People over 25 years old
            df_compiled.at[c, 'pop_18_tot'] = df_S1501_eduage['people'].sum()

            # Low education people
            df_compiled.at[c, 'pop_loweducation'] = df_S1501_eduage[df_S1501_eduage['education']=='Less than high school graduate']['people'].sum()
            df_compiled.at[c, 'pop_loweducation_%'] = (df_compiled['pop_loweducation'][c] / df_compiled['pop_18_tot'][c]).round(3)

    def analyze_S1701(c):
        if 'pov' in checks_groups:
            df_S1701_povage = dict_dfs[b]['PovertyByAge'][dict_dfs[b]['PovertyByAge']['location_id'] == df_compiled['location_id'][c]]

            # Total households
            df_compiled.at[c, 'pop_povcalculated_tot'] = df_S1701_povage['people'].sum()

            # Low income people
            df_compiled.at[c, 'pop_poverty'] = df_S1701_povage[df_S1701_povage['poverty'] == 'Below poverty level']['people'].sum()
            df_compiled.at[c, 'pop_poverty_%'] = (df_compiled['pop_poverty'][c] / df_compiled['pop_povcalculated_tot'][c]).round(3)

    def analyze_S1810(c):
        if 'disab' in checks_groups:
            df_S1810_disabage = dict_dfs[b]['DisabilitiesByAge'][dict_dfs[b]['DisabilitiesByAge']['location_id'] == df_compiled['location_id'][c]]

            # People 18 years and older
            df_compiled.at[c, 'pop_disabcalculated_tot'] = df_S1810_disabage['people'].sum()

            # Disabled people
            df_compiled.at[c, 'pop_disabled'] = df_S1810_disabage[df_S1810_disabage['disability'] == 'With a disability']['people'].sum()
            df_compiled.at[c, 'pop_disabled_%'] = (df_compiled['pop_disabled'][c] / df_compiled['pop_disabcalculated_tot'][c]).round(3)

    # Put analysis functions in a dictionary
    dict_functions = {'DP04': analyze_DP04, 'DP05': analyze_DP05, 'S0801': analyze_S0801, 'S1501': analyze_S1501,
                      'S1701': analyze_S1701, 'S1810': analyze_S1810}

    #### GET RAW NUMBERS OF ATTRIBUTES
    for c in range(len(df_compiled['location_id'])):
        for b in tablenames_tracts:
            try:
                dict_functions[b](c)
            except Exception:
                pass

    #### GET PERCENTILE RANKS
    column_names = df_compiled.columns.values.tolist()
    for c in column_names:
        if c == 'pop_poverty_%':
            df_compiled['pop_poverty_%rank'] = df_compiled['pop_poverty_%'].rank(pct=True).round(3)
        elif c == 'pop_elderly_%':
            df_compiled['pop_elderly_%rank'] = df_compiled['pop_elderly_%'].rank(pct=True).round(3)
        elif c == 'pop_disabled_%':
            df_compiled['pop_disabled_%rank'] = df_compiled['pop_disabled_%'].rank(pct=True).round(3)
        elif c == 'pop_poc_%':
            df_compiled['pop_poc_%rank'] = df_compiled['pop_poc_%'].rank(pct=True).round(3)
        elif c == 'pop_nondriver_%':
            df_compiled['pop_nondriver_%rank'] = df_compiled['pop_nondriver_%'].rank(pct=True).round(3)
        elif c == 'house_renter_%':
            df_compiled['house_renter_%rank'] = df_compiled['house_renter_%'].rank(pct=True).round(3)
        elif c == 'house_lowhousevalue_%':
            df_compiled['house_lowhousevalue_%rank'] = df_compiled['house_lowhousevalue_%'].rank(pct=True).round(3)
        elif c == 'pop_loweducation_%':
            df_compiled['pop_loweducation_%rank'] = df_compiled['pop_loweducation_%'].rank(pct=True).round(3)

    # Sort list of absolute columns
    column_names = df_compiled.columns.values.tolist()
    column_names.remove('location_id')
    cname_abs = []
    for c in column_names:
        if c[-2:] != "_%" and c[-6:] != "_%rank" and c[-4:] != "_tot":
            cname_abs.append(c)
    cname_abs = sorted(cname_abs)

    # Sort list of totals
    cnames_totals = []
    for c in column_names:
        if c[-4:] == "_tot" and c not in ['pop_tot', 'house_tot']:
            cnames_totals.append(c)
    cnames_totals = sorted(cnames_totals)

    if 'pop_tot' in column_names:
        cnames_totals.insert(0, 'pop_tot')
        if 'house_tot' in column_names:
            cnames_totals.insert(1, 'house_tot')
    elif 'house_tot' in column_names:
        cnames_totals.insert(0, 'house_tot')

    # Sort list of % columns
    cnames_perc = []
    for c in column_names:
        if c[-2:] == "_%":
            cnames_perc.append(c)
    cnames_perc = sorted(cnames_perc)

    # Sort list of % rank columns
    cnames_percrank = []
    for c in column_names:
        if c[-6:] == "_%rank":
            cnames_percrank.append(c)
    cnames_percrank = sorted(cnames_percrank)

    # Combine lists
    cnames_all = cnames_totals + cname_abs + cnames_perc + cnames_percrank
    cnames_all.insert(0, 'location_id')
    df_compiled = df_compiled[cnames_all]

    # Add correlation matrix and scatter plots if box checked
    if "matrix" in checks_calcs:
        corr_matrix = df_compiled[cnames_perc].corr().round(2)
        dfs.append(corr_matrix)
        keep_index.append(True)
        sheetnames.append('Correlation Matrix')

        # Scatter plots
        df_scatter = df_compiled[cnames_perc]
        df_scatter.columns = df_scatter.columns.str.replace('pop_', '')
        df_scatter.columns = df_scatter.columns.str.replace('_', ' ')
        sns.set(font_scale=1.25)
        sns.pairplot(df_scatter)
        zfm_scatter = zs.open("scatter_matrix.png", 'w')
        plt.savefig(zfm_scatter)
        zfm_scatter.close()

        # make sorted correlation matrix
        upper_corr_mat = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

        # Convert to 1-D series and drop Null values
        unique_corr_pairs = upper_corr_mat.unstack().dropna()

        # Sort correlation pairs
        sorted_mat = unique_corr_pairs.sort_values(ascending=False)
        dfs.append(sorted_mat)
        keep_index.append(True)
        sheetnames.append('Sorted Correlation Matrix')

    # Add summary statistics and create boxplots if box checked
    if "summ" in checks_calcs:
        df_summ = df_compiled.describe().round(2)
        dfs.append(df_summ)
        keep_index.append(True)
        sheetnames.append('Summary Statistics')

    # Remove percentages and percentage ranks if boxes not checked
    if "perc" not in checks_calcs:
        for c in column_names:
            if c[-2:] == "_%":
                del df_compiled[c]

    if "percrank" not in checks_calcs:
        for c in column_names:
            if c[-6:] == "_%rank":
                del df_compiled[c]
    dfs.insert(0, df_compiled)
    keep_index.insert(0, False)
    sheetnames.insert(0, 'Data')

    ###Create output file
    return dfs, sheetnames, keep_index