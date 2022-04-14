
def analyze_blockgroup(unzipped, cats_dict, checks_groups, checks_calcs, zs, tablenames_blockgroups, fnames):

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
    all_location_id = []
    for b in range(len(tablenames_blockgroups)):
        df = pd.read_excel(unzipped.open(fnames[b], 'r'), dtype={'location_id': object})
        dict_dfs[tablenames_blockgroups[b]] = df
        [all_location_id.append(x) for x in df['location_id'].tolist()]
    df_compiled['location_id'] = sorted(list(set(all_location_id)))

    # Define table analysis functions
    def analyze_B01001(c):
        if cats_dict['elderly'] != "dontinclude":

            df_B01001 = dict_dfs[b][dict_dfs[b]['location_id']==df_compiled['location_id'][c]]

            # Total population
            df_compiled.at[c,'pop_tot']= df_B01001['people'].sum()

            # Elderly people
            cats_elderly = ['60 and 61 years', '62 to 64 years', '65 and 66 years', '67 to 69 years', '70 to 74 years',
                            '75 to 79 years', '80 to 84 years','85 years and over']

            if cats_dict['elderly'] == '60yr':
                pass
            elif cats_dict['elderly'] == '65yr':
                cats_elderly = list(set(cats_elderly) - set(['60 and 61 years', '62 to 64 years']))
            elif cats_dict['elderly'] == '75yr':
                cats_elderly = list(set(cats_elderly) - set(['60 and 61 years', '62 to 64 years', '65 and 66 years', '67 to 69 years','70 to 74 years']))

            df_compiled.at[c,'pop_elderly'] = df_B01001[df_B01001['age'].isin(cats_elderly)]['people'].sum()
            df_compiled.at[c,'pop_elderly_%'] = (df_compiled['pop_elderly'][c] / df_compiled['pop_tot'][c]).round(3)
        
    def analyze_B03002(c):
        if 'poc' in checks_groups:
            df_B03002 = dict_dfs[b][dict_dfs[b]['location_id']==df_compiled['location_id'][c]]

            # Total population
            df_compiled.at[c, 'pop_tot'] = df_B03002['people'].sum()

            # People of Color
            #num of poc
            non_hispwhite = df_B03002[(df_B03002['hisp_latino'] == 'Not Hispanic or Latino')&(df_B03002['race'] == 'White alone')]['people'].sum()
            df_compiled.at[c,'pop_poc'] = (df_compiled['pop_tot'][c] - non_hispwhite).round(3)
            df_compiled.at[c,'pop_poc_%'] = (df_compiled['pop_poc'][c] / df_compiled['pop_tot'][c]).round(3)
        
    def analyze_B08134(c):
        if cats_dict['nondriver'] != "dontinclude":
            df_B08134 = dict_dfs[b][dict_dfs[b]['location_id']==df_compiled['location_id'][c]]

            # Workers age 16 and older and that do not work from home
            df_compiled.at[c,'workers_16_nothome_tot'] = df_B08134['workers_16_nothome'].sum()

            # Nondrivers to work
            if cats_dict['nondriver'] == 'nondriver':
                df_compiled.at[c, 'pop_nondriver'] = df_B08134[df_B08134['commute_mode'] != 'Car, truck, or van']['workers_16_nothome'].sum()
            elif cats_dict['nondriver'] == 'carpool':
                df_compiled.at[c, 'pop_nondriver'] = df_B08134[df_B08134['commute_mode_sub'].isin(['Carpooled','-'])]['workers_16_nothome'].sum()

            df_compiled.at[c,'pop_nondriver_%'] = (df_compiled['pop_nondriver'][c] / df_compiled['workers_16_nothome_tot'][c]).round(3)

    def analyze_B15002(c):
        if 'edu' in checks_groups:

            df_B15002 = dict_dfs[b][dict_dfs[b]['location_id']==df_compiled['location_id'][c]]

            # People over 25 years old
            df_compiled.at[c,'pop_25_tot'] =df_B15002['people_25'].sum()

            # Low education people
            cats_education = ['No schooling completed', 'Nursery school', 'Kindergarten','1st grade','2nd grade',
                              '3rd grade','4th grade','5th grade','6th grade','7th grade','8th grade','9th grade',
                              '10th grade','11th grade','12th grade, no diploma']
            df_compiled.at[c,'pop_loweducation'] = df_B15002[df_B15002['education'].isin(cats_education)]['people_25'].sum()
            df_compiled.at[c,'pop_loweducation_%'] = (df_compiled['pop_loweducation'][c] / df_compiled['pop_25_tot'][c]).round(3)

    def analyze_C17002(c):
        if 'lowincome' in checks_groups:
            df_C17002 = dict_dfs[b][dict_dfs[b]['location_id']==df_compiled['location_id'][c]]

            # Total households
            df_compiled.at[c,'pop_pov_tot'] = df_C17002['people'].sum()
            # Low income people
            df_compiled.at[c,'pop_lowincome'] = df_C17002[df_C17002['income_pov_ratio']!='2.00 and over']['people'].sum()
            df_compiled.at[c,'pop_lowincome_%'] = (df_compiled['pop_lowincome'][c] / df_compiled['pop_pov_tot'][c]).round(3)
    
    def analyze_B25008(c):
        if 'renter' in checks_groups:
            df_B25008 = dict_dfs[b][dict_dfs[b]['location_id']==df_compiled['location_id'][c]]

            # People in occupied households
            df_compiled.at[c,'pop_inhouse_tot'] = df_B25008['people'].sum()

            # Renters
            df_compiled.at[c,'pop_renter'] = df_B25008[df_B25008['owner_renter']=='Renter occupied']['people'].sum()
            df_compiled.at[c,'pop_renter_%'] = (df_compiled['pop_renter'][c] / df_compiled['pop_inhouse_tot'][c]).round(3)

    def analyze_B25034(c):
        if 'lead' in checks_groups:
            df_B25034 = dict_dfs[b][dict_dfs[b]['location_id']==df_compiled['location_id'][c]]

            # People in occupied households
            df_compiled.at[c,'house_tot'] = df_B25034['houses'].sum()

            # Lead paint indicator
            cats_houseage = ['Built 1950 to 1959','Built 1940 to 1949','Built 1939 or earlier']
            df_compiled.at[c,'house_leadindicator'] = df_B25034[df_B25034['house_age'].isin(cats_houseage)]['houses'].sum()
            df_compiled.at[c,'house_leadindicator_%'] = (df_compiled['house_leadindicator'][c] / df_compiled['house_tot'][c]).round(3)
        
    def analyze_B25075(c):
        if cats_dict['lowhousevalue'] != "dontinclude":
            df_B25075 = dict_dfs[b][dict_dfs[b]['location_id']==df_compiled['location_id'][c]]

            # Housing Value
            if cats_dict['lowhousevalue'] != "dontinclude":
                # Total households
                df_compiled.at[c, 'house_tot'] = df_B25075['households'].sum()
                cats_housevalue = ['Less than $10,000', '$10,000 to $14,999', '$15,000 to $19,999','$20,000 to $24,999',
                                   '$25,000 to $29,999', '$30,000 to $34,999', '$35,000 to $39,999','$40,000 to $49,999',
                                   '$50,000 to $59,999', '$60,000 to $69,999', '$70,000 to $79,999','$80,000 to $89,999',
                                   '$90,000 to $99,99']
                if cats_dict['lowhousevalue'] == '50k':
                    cats_housevalue = list(set(cats_housevalue) - set(['$50,000 to $59,999', '$60,000 to $69,999',
                                                                       '$70,000 to $79,999','$80,000 to $89,999','$90,000 to $99,99']))
                    df_compiled.at[c, 'house_lowhousevalue'] = df_B25075[df_B25075['housevalue_range'].isin(cats_housevalue)]['households'].sum()
                elif cats_dict['lowhousevalue'] == '100k':
                    df_compiled.at[c,'house_lowhousevalue'] = df_B25075[df_B25075['housevalue_range'].isin(cats_housevalue)]['households'].sum()
                df_compiled.at[c,'house_lowhousevalue_%'] = (df_compiled['house_lowhousevalue'][c] / df_compiled['house_tot'][c]).round(3)
        
    def analyze_C21007(c):
        if 'disab' in checks_groups:
            df_C21007 = dict_dfs[b][dict_dfs[b]['location_id']==df_compiled['location_id'][c]]

            # People 18 years and older
            df_compiled.at[c,'pop_18_tot'] = df_C21007['people_18'].sum()

            # Disabled people
            df_compiled.at[c,'pop_disabled'] = df_C21007[df_C21007['disability']=='With a disability']['people_18'].sum()
            df_compiled.at[c,'pop_disabled_%'] = (df_compiled['pop_disabled'][c] / df_compiled['pop_18_tot'][c]).round(3)
    
    # Put analysis functions in a dictionary
    dict_functions = {'B01001':analyze_B01001, 'B03002':analyze_B03002, 'B08134':analyze_B08134, 'B15002':analyze_B15002, 'C17002':analyze_C17002,
    'B25008':analyze_B25008, 'B25034':analyze_B25034, 'B25075':analyze_B25075, 'C21007':analyze_C21007}
    
    #### GET RAW NUMBERS OF ATTRIBUTES
    for c in range(len(df_compiled['location_id'])):
        for b in tablenames_blockgroups:
            try:
                dict_functions[b](c)
            except Exception:
                pass

    #### GET PERCENTILE RANKS
    column_names = df_compiled.columns.values.tolist()
    for c in column_names:
        if c == 'pop_lowincome_%':
            df_compiled['pop_lowincome_%rank'] = df_compiled['pop_lowincome_%'].rank(pct=True).round(3)
        elif c == 'pop_elderly_%':
            df_compiled['pop_elderly_%rank'] = df_compiled['pop_elderly_%'].rank(pct=True).round(3)
        elif c == 'pop_disabled_%':
            df_compiled['pop_disabled_%rank'] = df_compiled['pop_disabled_%'].rank(pct=True).round(3)
        elif c == 'pop_poc_%':
            df_compiled['pop_poc_%rank'] = df_compiled['pop_poc_%'].rank(pct=True).round(3)
        elif c == 'pop_nondriver_%':
            df_compiled['pop_nondriver_%rank'] = df_compiled['pop_nondriver_%'].rank(pct=True).round(3)
        elif c == 'pop_renter_%':
            df_compiled['pop_renter_%rank'] = df_compiled['pop_renter_%'].rank(pct=True).round(3)
        elif c == 'house_leadindicator_%':
            df_compiled['house_leadindicator_%rank'] = df_compiled['house_leadindicator_%'].rank(pct=True).round(3)
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
        if c[-4:] == "_tot" and c not in ['pop_tot','house_tot']:
            cnames_totals.append(c)
    cnames_totals = sorted(cnames_totals)
    
    if 'pop_tot' in column_names:
        cnames_totals.insert(0,'pop_tot')
        if 'house_tot' in column_names:
            cnames_totals.insert(1,'house_tot')
    elif 'house_tot' in column_names:
        cnames_totals.insert(0,'house_tot')
    
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
    cnames_all.insert(0,'location_id')
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
    dfs.insert(0,df_compiled)
    keep_index.insert(0,False)
    sheetnames.insert(0,'Data')

    ###Create output file
    return dfs, sheetnames, keep_index