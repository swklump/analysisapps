def advancedanalysis_func(cats_dict):
    import pandas as pd

    # Get state code
    web_path = 'https://www2.census.gov/geo/docs/reference/codes/files/national_county.txt'
    df_loccodes = pd.read_csv(web_path, dtype=str, usecols=[0,1])
    df_loccodes.columns = ['STATE', 'STATEFP']
    state_code = df_loccodes[df_loccodes['STATE']==cats_dict['state']]['STATEFP'].iloc[0]
    
    cats_dict['var_ind'] = cats_dict['var_ind'][0:cats_dict['var_ind'].find(':')]
    cats_dict['var_dep'] = cats_dict['var_dep'][0:cats_dict['var_dep'].find(':')]
    api_url_base = 'https://api.census.gov/data/' + cats_dict['year'] + '/acs/acs5/profile?get='
    api_key = '2d06b2407a7edc598608026ac92014c461d42dbb'

    ### GET INDPENDENT VARIABLE ARRAY
    api_url_ind = api_url_base + cats_dict['var_ind'] + '&for=tract:*&in=state:' + state_code + '&in=county:*&key='+api_key
    print(api_url_ind)
    df_ind = pd.read_json(str(api_url_ind))
    # promote first data row to header
    new_header = df_ind.iloc[0]
    df_ind = df_ind[1:]
    df_ind.columns = new_header

    ### GET DEPENDENT VARIABLE ARRAY
    api_url_ind = api_url_base + cats_dict['var_dep'] + '&for=tract:*&in=state:' + state_code + '&in=county:*&key='+api_key
    df_dep = pd.read_json(str(api_url_ind))
    # promote first data row to header
    new_header = df_dep.iloc[0]
    df_dep = df_dep[1:]
    df_dep.columns = new_header

    # create empty dataframe for quality checks
    df = pd.DataFrame()
    df['var_ind'] = pd.to_numeric(df_ind[cats_dict['var_ind']])
    df['var_dep'] = pd.to_numeric(df_dep[cats_dict['var_dep']])
    df = df[(df >= 0).all(1)]

    return df
    #https://www.census.gov/data/developers/data-sets/acs-5year.html
    #api key: 2d06b2407a7edc598608026ac92014c461d42dbb
    # df = pd.read_json('https://api.census.gov/data/2019/acs/acs5/profile?get=group(DP05)&for=tract:*&in=state:02&in=county:016&key=2d06b2407a7edc598608026ac92014c461d42dbb')
