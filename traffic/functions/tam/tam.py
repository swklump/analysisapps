def tam_func(uploaded_file):

    import pandas as pd
    pd.options.mode.chained_assignment = None
    import numpy as np
    import io, zipfile
    from .calc_dist_points import calc_dist
    from datetime import datetime

    now0 = datetime.now()

    # ----------------------------------------------------------------------------------------------------------
    # READ IN DATA

    # Read in nodes tab
    df_nodes = pd.read_excel(uploaded_file, sheet_name='Nodes')
    df_nodes.dropna(subset=['node_number'], inplace=True)
    df_nodes['node_number'] = df_nodes['node_number'].astype(int)
    num_nodes = df_nodes.shape[0]

    # Read in the links tab
    df_links = pd.read_excel(uploaded_file, sheet_name='Links', dtype={'link_num':object})
    df_links.dropna(subset=['link_num'], inplace=True)
    df_links['from_node'] = df_links['from_node'].astype(int)
    df_links['to_node'] = df_links['to_node'].astype(int)

    # Merge node types, determine link type
    df_links = pd.merge(df_links,df_nodes[['node_number','node_type']],how="left",left_on='from_node',right_on='node_number').drop(columns=['node_number'])
    df_links.rename(columns = {'node_type':'from_node_type'}, inplace = True)
    df_links = pd.merge(df_links,df_nodes[['node_number','node_type']],how="left",left_on='to_node',right_on='node_number').drop(columns=['node_number'])
    df_links.rename(columns = {'node_type':'to_node_type'}, inplace = True)
    df_links.loc[(df_links['from_node_type'] == 'zone')|(df_links['to_node_type'] == 'zone'), 'link_type'] = 'zone'
    df_links.loc[(df_links['from_node_type'] != 'zone')&(df_links['to_node_type'] != 'zone'), 'link_type'] = 'network'

    # Merge lat/lons for nodes
    df_links = pd.merge(df_links,df_nodes[['node_number','centroid_lat','centroid_lon']],how="left",left_on='from_node',right_on='node_number').drop(columns=['node_number'])
    df_links.rename(columns = {'centroid_lat':'from_lat','centroid_lon':'from_lon'}, inplace = True)
    df_links = pd.merge(df_links,df_nodes[['node_number','centroid_lat','centroid_lon']],how="left",left_on='to_node',right_on='node_number').drop(columns=['node_number'])
    df_links.rename(columns = {'centroid_lat':'to_lat','centroid_lon':'to_lon'}, inplace = True)


    # Compute link length with haversine formula, compute cost
    df_links = calc_dist(df_links)
    df_links['cost'] = df_links['dist'] * 60 / df_links['speed']
    

    # ----------------------------------------------------------------------------------------------------------
    # CREATE MATRICES

    # Create pointer, cost, and distance matrices
    nodaldelay_matrix = np.zeros([num_nodes,num_nodes],dtype='float')
    pointer_matrix = np.zeros([num_nodes,num_nodes],dtype=object)
    cost_matrix = np.zeros([num_nodes,num_nodes],dtype='float')

    # match up from the data source
    for x in range(len(df_links)):
        from_node = df_links['from_node'].loc[x]
        to_node = df_links['to_node'].loc[x]
        nodaldelay_matrix[from_node-1][to_node-1] = str(df_links['node_delay'].loc[x])
        pointer_matrix[from_node-1][to_node-1] = str(df_links['link_num'].loc[x])
        cost_matrix[from_node-1][to_node-1] = df_links['cost'].loc[x]

    # Assign large costs for od that aren't possible
    cost_matrix[cost_matrix==0] = 999999999
    
    # Solve F-W algorithm for all least cost paths
    for m in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                node_delay = nodaldelay_matrix[m][j]
                if cost_matrix[i][m] + cost_matrix[m][j] + node_delay < cost_matrix[i][j]:
                    cost_matrix[i][j] = cost_matrix[i][m] + cost_matrix[m][j] + node_delay
                    pointer_matrix[i][j] = str(pointer_matrix[i][m]) + ',' + str(pointer_matrix[m][j])
    now2 = datetime.now()
    
    # ----------------------------------------------------------------------------------------------------------
    # REFORMAT MATRICES TO DATAFRAMES

    # Reformat cost to a dataframe
    cost_dict = {'from_node':[],'to_node':[],'cost':[]}
    for x in range(len(cost_matrix)):
        cost_dict['from_node']+=[x+1]*len(cost_matrix)
        cost_dict['to_node']+=list(np.arange(1,num_nodes+1,1))
        cost_dict['cost']+=list(cost_matrix[x])
    df_cost = pd.DataFrame(cost_dict,columns=['from_node','to_node','cost'])

    # Reformat pointer to a dataframe
    pointer_dict = {'from_node':[],'to_node':[],'link_num':[]}
    for x in range(len(pointer_matrix)):
        pointer_dict['from_node']+=[x+1]*len(pointer_matrix)
        pointer_dict['to_node']+=list(np.arange(1,num_nodes+1,1))
        pointer_dict['link_num']+=list(pointer_matrix[x])

    # Separate out multiple link numbers into own row
    # Define the function for getting indices of comma
    def find(my_str, my_char):
        return [i for i, ltr in enumerate(my_str) if ltr == my_char]
    # create a new dict to add values to
    pointer_dict_new = {'from_node':[],'to_node':[],'link_num':[]}
    for x in range(len(pointer_dict['from_node'])):
        indices = find(pointer_dict['link_num'][x],',')
        # if only one link, just add values to new dict
        if len(indices) == 0:
            pointer_dict_new['from_node'].append(pointer_dict['from_node'][x])
            pointer_dict_new['to_node'].append(pointer_dict['to_node'][x])
            pointer_dict_new['link_num'].append(pointer_dict['link_num'][x])
        # else loop through each index
        else:
            for z in range(len(indices)+1):
                pointer_dict_new['from_node'].append(pointer_dict['from_node'][x])
                pointer_dict_new['to_node'].append(pointer_dict['to_node'][x])
                if z == 0:
                    link_num = pointer_dict['link_num'][x][:indices[0]]
                elif z == len(indices):
                    link_num = pointer_dict['link_num'][x][indices[z-1]+1:]
                else:
                    link_num = pointer_dict['link_num'][x][indices[z-1]+1:indices[z]]
                pointer_dict_new['link_num'].append(link_num)

    df_pointer = pd.DataFrame(pointer_dict_new,columns=['from_node','to_node','link_num'])
    change_to_ints = ['from_node','to_node','link_num']
    for x in change_to_ints:
        df_pointer[x] = df_pointer[x].astype(int)

    
   
    # ----------------------------------------------------------------------------------------------------------
    # ASSIGN VOLUMES TO LINKS

    # filter to only zone to zone ods
    zone_nums = df_nodes[df_nodes['node_type']=='zone']['node_number'].values.tolist()
    df_cost = df_cost[(df_cost['from_node'].isin(zone_nums))&(df_cost['to_node'].isin(zone_nums))]
    df_pointer = df_pointer[(df_pointer['from_node'].isin(zone_nums))&(df_pointer['to_node'].isin(zone_nums))]

    # filter out same origin and destination
    df_cost = df_cost[~(df_cost['from_node']==df_cost['to_node'])]
    df_pointer = df_pointer[~(df_pointer['from_node']==df_pointer['to_node'])]

    # get trips from od spreadsheet tab
    df_od = pd.read_excel(uploaded_file, sheet_name='OD', dtype={'from_node':int, 'to_node':int})
    df_odsummed = df_od.groupby(['from_node','to_node'])[['trips_allhours','trips_pmpeak']].sum() #in case there are duplicates in spreadsheet
    df_pointer = pd.merge(df_pointer,df_odsummed,how="left",on=['from_node','to_node'])

    # filter out zero trip od pairs (direction wrong)
    df_pointer = df_pointer[df_pointer['trips_allhours']!=0]

    # aggregate and filter out feeder links
    link_vols = df_pointer.groupby('link_num').agg({'trips_allhours':'sum', 'trips_pmpeak':'sum'}).reset_index()
    network_links = df_links[df_links['link_type']=='network']['link_num'].values.tolist()
    link_vols = link_vols[link_vols['link_num'].isin(network_links)]
    
    

    # ----------------------------------------------------------------------------------------------------------
    # Get data in format for mapping
    dict_map = {}
    df_links['link_num'] = df_links['link_num'].astype(str)
    dict_map['link_num'] =  [str(ele) for ele in link_vols['link_num'] for i in range(2)]
    dict_map['trips'] =  [int(ele) for ele in link_vols['trips_allhours'] for i in range(2)]
    dict_map['lat'], dict_map['lon'], dict_map['cat']= [], [], []

    # Categorize trips by quintiles
    min_val = int(min(link_vols['trips_allhours']))
    first = int(np.quantile(link_vols['trips_allhours'],0.2))
    second = int(np.quantile(link_vols['trips_allhours'],0.4))
    third = int(np.quantile(link_vols['trips_allhours'],0.6))
    fourth = int(np.quantile(link_vols['trips_allhours'],0.8))
    max_val = int(max(link_vols['trips_allhours']))
    for x in range(len(dict_map['trips'])):
        if dict_map['trips'][x] < first:
            dict_map['cat'].append(str(min_val)+'-'+str(first))
        elif dict_map['trips'][x] < second:
            dict_map['cat'].append(str(first)+'-'+str(second))
        elif dict_map['trips'][x] < third:
            dict_map['cat'].append(str(second)+'-'+str(third))
        elif dict_map['trips'][x] < fourth:
            dict_map['cat'].append(str(third)+'-'+str(fourth))
        else:
            dict_map['cat'].append(str(fourth)+'-'+str(max_val))

    # reformat to have each line point as own row
    for x in range(len(dict_map['link_num'])):
        if (x+1) % 2 != 0:
            lat = df_links[df_links['link_num']==dict_map['link_num'][x]]['from_lat'].values.tolist()[0]
            lon = df_links[df_links['link_num']==dict_map['link_num'][x]]['from_lon'].values.tolist()[0]
        else:
            lat = df_links[df_links['link_num']==dict_map['link_num'][x]]['to_lat'].values.tolist()[0]
            lon = df_links[df_links['link_num']==dict_map['link_num'][x]]['to_lon'].values.tolist()[0]
        dict_map['lat'].append(lat)
        dict_map['lon'].append(lon)
    

    df_map = pd.DataFrame(dict_map)


    # ----------------------------------------------------------------------------------------------------------
    # WRITE TO FILE

    # Send to zipped folder
    buf = io.BytesIO()
    zs = zipfile.ZipFile(buf, mode='w')
    zfm1 = zs.open("tam_outputtables.xlsx", 'w')
    with pd.ExcelWriter(zfm1, engine='xlsxwriter') as writer:
        df_cost.to_excel(writer,sheet_name='cost_table',index=False)
        df_pointer.to_excel(writer,sheet_name='pointer_table',index=False)
        link_vols.to_excel(writer,sheet_name='link_vols',index=False)
        df_map.to_excel(writer,sheet_name='map_format',index=False)

    zfm1.close()
    zs.close()

    return buf, df_map