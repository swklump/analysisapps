
def compile_years(folderlocation, savelocation):

    # Imports
    import xlrd
    import xlsxwriter
    import pandas as pd
    import glob


    files = glob.glob(folderlocation + '//' + '*.*')
    dict_dfs = {}
  
    for x in range(len(files)):
        df = pd.read_excel(files[x], dtype={'tract_blckgrp':object})
        year = files[x].replace('.xlsx','')[-4:]
        dict_dfs[year] = df
        dict_dfs[year]['year'] = int(year)
    
    df_allyears = pd.DataFrame()
    for k in dict_dfs.keys():
        df_allyears = pd.concat([df_allyears,dict_dfs[k]])
    
    second_column = df_allyears.pop('year')
    df_allyears.insert(1,'year',second_column)
    #Create output file
    outputname = savelocation + '\\' + 'censusdata_allyears.xlsx'
    writer = (outputname)
    with pd.ExcelWriter(writer, engine='xlsxwriter') as writer:
        df_allyears.to_excel(writer, sheet_name='Data', index=False)

folderlocation = r'\\dowl.com\j\Projects\38\63026-01\40Study\Environmental\B10.12_Social Groups Map\CensusData\2. Processed Data\2. Compiled Data'
savelocation = r'\\dowl.com\j\Projects\38\63026-01\40Study\Environmental\B10.12_Social Groups Map\CensusData\3. Analysis'
compile_years(folderlocation, savelocation)




    