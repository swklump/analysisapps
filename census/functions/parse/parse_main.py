
def parse_func(wbs, table_ids, years):
    import xlrd, io, zipfile
    xlrd.xlsx.ensure_elementtree_imported(False, None)
    xlrd.xlsx.Element_has_iter = True
    import pandas as pd
    from datetime import datetime
    from ._helperfunctions import get_location_id

    # Import tract modules
    from .tracts.DP04_housing_parser import DP04_parse_housing
    from .tracts.DP05_demographics_parser import DP05_parse_demo
    from .tracts.S0801_commute_parser import S0801_parse_commute
    from .tracts.S1501_education_parser import S1501_parse_education
    from .tracts.S1701_poverty_parser import S1701_parse_poverty
    from .tracts.S1810_disability_parser import S1810_parse_disab
    from .tracts.S1901_income_parser import S1901_parse_income

    # Import blockgroup modules
    from .blockgroups.B01001_age_parser import B01001_parse_age
    from .blockgroups.B03002_race_parser import B03002_parse_race
    from .blockgroups.B08134_commute_parser import B08134_parse_commute
    from .blockgroups.B15002_education_parser import B15002_parse_edu
    from .blockgroups.B17017_poverty_parser import B17017_parse_poverty
    from .blockgroups.B19001_income_parser import B19001_parse_income
    from .blockgroups.B25008_housingtenure_parser import B25008_parse_housingtenure
    from .blockgroups.B25034_houseage_parser import B25034_parse_houseage
    from .blockgroups.B25075_housingvalue_parser import B25075_parse_housingvalue
    from .blockgroups.C17002_incomepovratio_parser import C17002_parse_incomepovratio
    from .blockgroups.C21007_disability_parser import C21007_parse_disab

    # Create zipped stream to add spreadsheet to
    buf = io.BytesIO()
    zs = zipfile.ZipFile(buf, mode='w')

    for x in range(len(wbs)):

        # Get data tab to parse
        sheet = wbs[x].sheet_by_name('Data')
        num_cols, num_rows = sheet.ncols, sheet.nrows

        #Now run parse functions
        locations_indexes = get_location_id(sheet, num_cols)
        location_id = locations_indexes[0]
        index_estimate = locations_indexes[1]
        # states, counties, tracts = locations_indexes[2], locations_indexes[3], locations_indexes[4]

        module_dict = {'DP04': DP04_parse_housing, 'DP05':DP05_parse_demo, 'S0801':S0801_parse_commute, 'S1501':S1501_parse_education,
                       'S1701':S1701_parse_poverty, 'S1810':S1810_parse_disab, 'S1901':S1901_parse_income}

        module_dict_bg = {
            'B01001':B01001_parse_age,  'B03002':B03002_parse_race,
            'B08134':B08134_parse_commute,'B15002':B15002_parse_edu,'B17017':B17017_parse_poverty,
            'B19001':B19001_parse_income,'B25008':B25008_parse_housingtenure,'B25034':B25034_parse_houseage,'B25075':B25075_parse_housingvalue,
            'C17002':C17002_parse_incomepovratio, 'C21007':C21007_parse_disab}
        
        module_dict = dict(module_dict.items() | module_dict_bg.items())

        results = module_dict[table_ids[x]](sheet, num_cols, num_rows, location_id, index_estimate)
        dfs, excel_name, sheetnames = results[0], results[1], results[2]

        # dfs = add_location_details(dfs)

        # Create zipped stream to add spreadsheet to
        zfm = zs.open(excel_name[:-12]+'_'+str(years[x])+'_parsed.xlsx', 'w')
        with pd.ExcelWriter(zfm, engine='xlsxwriter') as writer:
            for d in range(len(dfs)):
                dfs[d].insert(loc=1, column='year', value=years[x])
                dfs[d].to_excel(writer, sheet_name=sheetnames[d], index=False)
                if d == len(dfs)-1:
                    df_detail = pd.DataFrame({'Detail':['Census Table ID','Year','File Parsed at Datetime'],
                                              'Value':[table_ids[x],years[x],datetime.now()]},
                                             columns=['Detail','Value'])
                    df_detail.to_excel(writer, sheet_name='FileDetails', index=False)
        zfm.close()


    ### Combine files with same name but different years
    # get list of files in zipped folder, create unique set, create dictionary with count of each unique
    # files = zs.namelist()
    # unique_files = []
    # for f in files:
    #     unique_files.append(f[:-17])
    # unique_files = set(unique_files)
    #
    # dict_files = {}
    # for u in unique_files:
    #     dict_files[u] = pd.DataFrame()
    #
    # for u in unique_files:
    #     for f in files:
    #         if u == f[:-17]:
    #             if len(dict_files[u]) == 0:
    #                 dict_files[u] = pd.read_excel(zs.open(f, 'r').read())
    #             else:
    #                 dict_files[u] = pd.concat([dict_files[u],pd.read_excel(zs.open(f, 'r').read())])
    #
    #     zfm1 = zs.open('test.xlsx', 'w')
    #     with pd.ExcelWriter(zfm1, engine='xlsxwriter') as writer:
    #         for k in dict_files.keys():
    #             dict_files[k].to_excel(writer, sheet_name='test', index=False)
    #     zfm1.close()
    zs.close()

    return buf