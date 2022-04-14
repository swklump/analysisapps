def html_to_excel(bs_files,html_dfs,highwaynames, zs, output_name):
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    from .clean_tables import clean_tables

    if len(bs_files) < 1:
        return

    # Create dictionary, add data for each table
    dict = {}

    ### GET ALL TABLE NAMES FROM HTML
    # for each html file
    for a in range(len(bs_files)):
        dict_temp = {}

        # remove dfs with one row
        dfs = html_dfs[a][3:]

        tbl = bs_files[a].find_all('table', {'class': 'Base'})
        # for each table in html file
        for t in range(len(tbl)):
            table_title = str(tbl[t].find('span', {'class': 'TableCaption'}).text)
            # clean up text
            table_title = table_title.replace("\t", "").replace("\r", "").replace("\n", "")
            table_title = table_title.replace('   ',' ').replace('  ', ' ').replace("  ", "").replace(' ','')
            table_title = table_title[table_title.find('.')+1:]
            if table_title.find('(') != -1:
                table_title = table_title[:table_title.find('(')]
            replace_words = {'Evaluation':'','Predicted':'','SpeedChangeLane':'SCL','Homogeneous':'Homog','Freeway':'Frwy',
                             'Crash':'','Summary':'Summ','Segment':'Seg','Frequencies':'Freq','Intersection':'Int','/':'_',
                             'Horizontal':'Horiz','and':'+','Element':''}
            for k,v in replace_words.items():
                table_title = table_title.replace(k,v)

            dict_temp[table_title] = dfs[t]
            dict_temp[table_title]['Element Name'] = highwaynames[a]
            first_col = dict_temp[table_title].pop('Element Name')
            dict_temp[table_title].insert(0, 'Element Name', first_col)

        # check if table already in dictionary, if is concat with existing, else add
        for k_temp in dict_temp.keys():
            if k_temp in dict.keys():
                dict[k_temp] = pd.concat([dict[k_temp], dict_temp[k_temp]])
            else:
                dict[k_temp] = dict_temp[k_temp]

    dict = clean_tables(dict)

    # Write to file
    zfm1 = zs.open(output_name, 'w')
    with pd.ExcelWriter(zfm1, engine='xlsxwriter') as writer:
        for k in dict.keys():
            dict[k].to_excel(writer, sheet_name=k, index=False)
    zfm1.close
    return
