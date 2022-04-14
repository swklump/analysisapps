# This function cleans up the data in the tables
def clean_tables(dict):
    import pandas as pd
    for k in dict.keys():

        ### ALL TABLES
        # reset index after combining dfs
        dict[k].reset_index(drop=True, inplace=True)

        # convert station columns to numeric, take out rows with 'Total' or 'Average'
        dict[k] = dict[k].replace('\+', '', regex=True)
        for a in dict[k].columns.tolist():
            dict[k] = dict[k][~dict[k][a].isin(['Total', 'Average', 'All Segments', 'All Intersections'])]
            if 'Location' in str(a) or str(a) in ['Seg. No.', 'Year']:
                dict[k][a] = pd.to_numeric(dict[k][a])

        # rename the median type columns
        dict[k] = dict[k].rename(columns={'Type.1': 'Median Type'})

        ### SUMMARY TABLES
        if 'FreqSumm' in k:
            # get unique values in columns
            elements = dict[k].drop_duplicates(['Element Name'], keep='last')['Element Name'].values.tolist()
            indices = [dict[k][dict[k]['Element Name'] == e].index[0] for e in elements]
            columns = dict[k].drop_duplicates([0], keep='last')[0].values.tolist()
            columns.insert(0, 'Element Name')

            # create list of lists with data
            data_list = []
            for e in range(len(elements)):
                if e != len(elements) - 1:
                    temp_list = [elements[e]]
                    for i in range(indices[e], indices[e + 1]):
                        temp_list.append(dict[k][1][i])
                    data_list.append(temp_list)
                else:
                    temp_list = [elements[e]]
                    for i in range(indices[e], len(dict[k]['Element Name'])):
                        temp_list.append(dict[k][1][i])
                    data_list.append(temp_list)
            # replace dataframe
            drop_columns = ['Predicted Crashes', 'Percent of Total Predicted Crashes', 'Predicted Travel Crash Rate', 'Predicted Crash Rate']
            drop_columns = [d for d in drop_columns if d in columns]

            df_temp = pd.DataFrame(data_list, columns=columns).drop(drop_columns, axis=1)
            for d in df_temp.columns.tolist()[1:]:
                df_temp[d] = pd.to_numeric(df_temp[d])
            dict[k] = df_temp

        ### CRASH TYPE TABLES
        if 'TypeDistribution' in k:
            column_names = ['Element Name', 'Element Type', 'Crash Type', 'Fatal and Injury Crashes',
                            'Property Damage Only Crashes']
            call_names = ['Element Name', ('Element Type', 'Element Type'), ('Crash Type', 'Crash Type'),
                          ('Fatal and Injury', 'Crashes'), ('Property Damage Only', 'Crashes')]
            dict_temp = {}
            for x in range(len(column_names)):
                dict_temp[column_names[x]] = dict[k][call_names[x]].values.tolist()
            df_temp = pd.DataFrame(dict_temp, columns=column_names)
            dict[k] = df_temp[
                ~df_temp['Crash Type'].isin(['Total Single Vehicle Crashes', 'Total Multiple Vehicle Crashes',
                                             'Total Highway Segment Crashes', 'Total Crashes'])]

    return dict
