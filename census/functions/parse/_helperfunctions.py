
def get_location_id(sheet, num_cols):

    # Get columns with estimate values (not percent error)
    locations_unprocessed = []
    index_estimate = []
    for n in range(num_cols):
        if sheet.cell_value(0, n) == '':
            pass
        else:
            locations_unprocessed.append(sheet.cell_value(0, n))
            index_estimate.append(n)

    # Import lookup table as df
    import pandas as pd
    web_path = 'https://www2.census.gov/geo/docs/reference/codes/files/national_county.txt'
    df_loccodes = pd.read_csv(web_path)
    df_loccodes.columns = ['STATE', 'STATEFP', 'COUNTYFP', 'COUNTYNAME', 'CLASSFP']

    locations = []
    states = []
    counties = []
    tracts = []
    for location in locations_unprocessed:
        num_commas = location.count(',')
        dict_location = {'blockgroup':'','tract':'','county':'','state':''}
        if num_commas == 0:
            dict_location['state'] = location
        elif num_commas == 1:
            comma_index = location.find(',')
            dict_location['state'] = location[comma_index+2:]
            dict_location['county'] = location[:comma_index]
        elif num_commas == 2:
            comma_index_first = location.find(',')
            comma_index_second = location.find(',', comma_index_first+1)
            dict_location['state'] = location[comma_index_second+2:]
            dict_location['county'] = location[comma_index_first+2:comma_index_second]
            dict_location['tract'] = location[:comma_index_first]
        elif num_commas == 3:
            comma_index_first = location.find(',')
            comma_index_second = location.find(',', comma_index_first + 1)
            comma_index_third = location.find(',', comma_index_second + 2)
            dict_location['state'] = location[comma_index_third + 2:]
            dict_location['county'] = location[comma_index_second + 2:comma_index_third]
            dict_location['tract'] = location[comma_index_first+2:comma_index_second]
            dict_location['blockgroup'] = location[:comma_index_first]

        # convert to number ID
        location_code = ''

        # Convert state to code
        state_dict = {"Alabama": "AL","Alaska": "AK","Arizona": "AZ", "Arkansas": "AR","California": "CA","Colorado": "CO",
                      "Connecticut": "CT","Delaware": "DE","Florida": "FL","Georgia": "GA","Hawaii": "HI","Idaho": "ID",
                      "Illinois": "IL","Indiana": "IN","Iowa": "IA","Kansas": "KS","Kentucky": "KY","Louisiana": "LA","Maine": "ME",
                      "Maryland": "MD","Massachusetts": "MA","Michigan": "MI","Minnesota": "MN","Mississippi": "MS","Missouri": "MO",
                      "Montana": "MT","Nebraska": "NE","Nevada": "NV","New Hampshire": "NH","New Jersey": "NJ","New Mexico": "NM",
                      "New York": "NY","North Carolina": "NC", "North Dakota": "ND","Ohio": "OH","Oklahoma": "OK","Oregon": "OR",
                      "Pennsylvania": "PA","Rhode Island": "RI","South Carolina": "SC","South Dakota": "SD","Tennessee": "TN",
                      "Texas": "TX","Utah": "UT","Vermont": "VT","Virginia": "VA","Washington": "WA","West Virginia": "WV",
                      "Wisconsin": "WI","Wyoming": "WY","District of Columbia": "DC","American Samoa": "AS","Guam": "GU",
                      "Northern Mariana Islands": "MP","Puerto Rico": "PR","United States Minor Outlying Islands": "UM","U.S. Virgin Islands": "VI",}
        if dict_location['state'] != '':
            # Convert state name to 2 letter code
            for k, v in state_dict.items():
                if dict_location['state'] == k:
                    dict_location['state'] = v
            state_code = str(df_loccodes[df_loccodes['STATE']==dict_location['state']]['STATEFP'].tolist()[0])
            if len(state_code) == 1:
                state_code = '0' + state_code
            location_code += (state_code + '_')

        # Convert county to code
        if dict_location['county'] != '':
            county_codes = df_loccodes[df_loccodes['COUNTYNAME']==dict_location['county']]['COUNTYFP'].tolist()
            if len(county_codes) == 0:
                county_code = '??'
            else:
                county_code = str(county_codes[0])
            if county_code == '??':
                pass
            elif len(county_code) == 1:
                county_code = '00' + county_code
            elif len(county_code) == 2:
                county_code = '0' + county_code
            location_code += (county_code + '_')

        # Convert tract to code
        if dict_location['tract'] != '':
            c = dict_location['tract']
            if c.find('.') != -1:
                val = c.replace('Census Tract ', '').replace('.', '')
            else:
                val = c.replace('Census Tract ', '') + '00'
            location_code += (val.rjust(6, '0') + '_')

        # Convert blockgroup to code
        if dict_location['blockgroup'] != '':
            location_code += (dict_location['blockgroup'].replace('Block Group ',''))

        if location_code[-1:] == '_':
            locations.append(location_code[:-1])
        else:
            locations.append(location_code)
        # states.append(dict_location['state'])
        # counties.append(dict_location['county'])
        # tracts.append(dict_location['tract'])

    return locations, index_estimate