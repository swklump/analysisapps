
def S0801_parse_commute(sheet, num_cols, num_rows, location_id, index_estimate):
    import pandas as pd
    from decimal import Decimal
    from ._helperfunctions import get_rowindex, get_rownameindex

    # Get indices of male and female
    male_indices = []
    female_indices = []
    for n in range(num_cols):
        if 'Male' in sheet.cell_value(1,n):
            male_indices.append(n)
        elif 'Female' in sheet.cell_value(1,n):
            female_indices.append(n)

    ####MEANS OF TRANSPORTATION TO WORK
    rownames_mode = ['Car, truck, or van', 'Public transportation (excluding taxicab)', 'Walked', 'Bicycle', 'Taxicab, motorcycle, or other means', 'Worked from home']
    rownames_mode_index = get_rowindex(sheet, num_rows, rownames_mode)
    rownames_car = ['Drove alone', 'Carpooled']
    rownames_car_index = get_rowindex(sheet, num_rows, rownames_car)
    rownames_carpool = ['In 2-person carpool', 'In 3-person carpool', 'In 4-or-more person carpool']
    rownames_carpool_index = get_rowindex(sheet, num_rows, rownames_carpool)

    #Get number of workers
    for n in range(num_rows):
        if sheet.cell_value(n,0) == 'Workers 16 years and over':
            num_workers_index = n

    #Create table
    dict_transpo = {'location_id':[], 'transpo_mode':[], 'transpo_mode_sub':[], 'transpo_mode_sub1':[],'sex':[], 'workers_16_nothome':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_mode)):
            if rownames_mode[c] == 'Car, truck, or van':
                for d in range(len(rownames_car)):
                    if rownames_car[d] == 'Carpooled':
                        for e in range(len(rownames_carpool)):
                            for s in range(0,2):
                                dict_transpo['location_id'].append(location_id[x])
                                dict_transpo['transpo_mode'].append(rownames_mode[c])
                                dict_transpo['transpo_mode_sub'].append(rownames_car[d])
                                dict_transpo['transpo_mode_sub1'].append(rownames_carpool[e])
                                if s == 0:
                                    dict_transpo['sex'].append('Male')
                                    if sheet.cell_value(rownames_carpool_index[e], male_indices[x]) == '-':
                                        dict_transpo['workers_16_nothome'].append(0)
                                    else:
                                        dict_transpo['workers_16_nothome'].append(Decimal(sheet.cell_value(rownames_carpool_index[e], male_indices[x]).replace('%', '')) * \
                                            int(sheet.cell_value(num_workers_index, male_indices[x]).replace(',', '')))
                                else:
                                    dict_transpo['sex'].append('Female')
                                    if sheet.cell_value(rownames_carpool_index[e], female_indices[x]) == '-':
                                        dict_transpo['workers_16_nothome'].append(0)
                                    else:
                                        dict_transpo['workers_16_nothome'].append(Decimal(
                                            sheet.cell_value(rownames_carpool_index[e], female_indices[x]).replace('%','')) * int(sheet.cell_value(num_workers_index, female_indices[x]).replace(',','')))
                    else:
                        for s in range(0, 2):
                            dict_transpo['location_id'].append(location_id[x])
                            dict_transpo['transpo_mode'].append(rownames_mode[c])
                            dict_transpo['transpo_mode_sub'].append(rownames_car[d])
                            dict_transpo['transpo_mode_sub1'].append('-')
                            if s == 0:
                                dict_transpo['sex'].append('Male')
                                if sheet.cell_value(rownames_car_index[d], male_indices[x]) == '-':
                                    dict_transpo['workers_16_nothome'].append(0)
                                else:
                                    dict_transpo['workers_16_nothome'].append(
                                        Decimal(sheet.cell_value(rownames_car_index[d], male_indices[x]).replace('%', '')) * \
                                        int(sheet.cell_value(num_workers_index, male_indices[x]).replace(',', '')))
                            else:
                                dict_transpo['sex'].append('Female')
                                if sheet.cell_value(rownames_car_index[d], female_indices[x]) == '-':
                                    dict_transpo['workers_16_nothome'].append(0)
                                else:
                                    dict_transpo['workers_16_nothome'].append(Decimal(
                                        sheet.cell_value(rownames_car_index[d], female_indices[x]).replace('%', '')) * int(
                                        sheet.cell_value(num_workers_index, female_indices[x]).replace(',', '')))

            else:
                for s in range(0, 2):
                    dict_transpo['location_id'].append(location_id[x])
                    dict_transpo['transpo_mode'].append(rownames_mode[c])
                    dict_transpo['transpo_mode_sub'].append('-')
                    dict_transpo['transpo_mode_sub1'].append('-')
                    if s == 0:
                        dict_transpo['sex'].append('Male')
                        if sheet.cell_value(rownames_mode_index[c], male_indices[x]) == '-':
                            dict_transpo['workers_16_nothome'].append(0)
                        else:
                            dict_transpo['workers_16_nothome'].append(
                                Decimal(sheet.cell_value(rownames_mode_index[c], male_indices[x]).replace('%', '')) * \
                                int(sheet.cell_value(num_workers_index, male_indices[x]).replace(',', '')))
                    else:
                        dict_transpo['sex'].append('Female')
                        if sheet.cell_value(rownames_mode_index[c], female_indices[x]) == '-':
                            dict_transpo['workers_16_nothome'].append(0)
                        else:
                            dict_transpo['workers_16_nothome'].append(Decimal(
                                sheet.cell_value(rownames_mode_index[c], female_indices[x]).replace('%', '')) * int(
                                sheet.cell_value(num_workers_index, female_indices[x]).replace(',', '')))

    ####PLACE OF WORK
    #Get rows
    rownames_work = ['Worked in state of residence', 'Worked outside state of residence']
    rownames_work_index = get_rowindex(sheet, num_rows, rownames_work)

    rownames_work_sub= ['Worked in county of residence', 'Worked outside county of residence']
    rownames_work_sub_index = get_rowindex(sheet, num_rows, rownames_work_sub)

    #Create table
    dict_work = {'location_id':[],'work_location':[], 'work_location_sub':[], 'sex':[],'workers_16':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_work)):
            if rownames_work[c] == 'Worked in state of residence':
                for d in range(len(rownames_work_sub)):
                    for s in range(0, 2):
                        dict_work['location_id'].append(location_id[x])
                        dict_work['work_location'].append(rownames_work[c])
                        dict_work['work_location_sub'].append(rownames_work_sub[d])
                        if s == 0:
                            dict_work['sex'].append('Male')
                            if sheet.cell_value(rownames_work_sub_index[d], male_indices[x]) == '-':
                                dict_work['workers_16'].append(0)
                            else:
                                dict_work['workers_16'].append(Decimal(sheet.cell_value(rownames_work_sub_index[d], male_indices[x]).replace('%', '')) * int(sheet.cell_value(num_workers_index, male_indices[x]).replace(',', '')))
                        else:
                            dict_work['sex'].append('Female')
                            if sheet.cell_value(rownames_work_sub_index[d], female_indices[x]) == '-':
                                dict_work['workers_16'].append(0)
                            else:
                                dict_work['workers_16'].append(Decimal(sheet.cell_value(rownames_work_sub_index[d], female_indices[x]).replace('%', '')) * int(sheet.cell_value(num_workers_index,female_indices[x]).replace(',', '')))

            else:
                for s in range(0, 2):
                    dict_work['location_id'].append(location_id[x])
                    dict_work['work_location'].append(rownames_work[c])
                    dict_work['work_location_sub'].append('-')
                    if s == 0:
                        dict_work['sex'].append('Male')
                        if sheet.cell_value(rownames_work_index[c], male_indices[x]) == '-':
                            dict_work['workers_16'].append(0)
                        else:
                            dict_work['workers_16'].append(Decimal(sheet.cell_value(rownames_work_index[c],male_indices[x]).replace('%',''))*int(sheet.cell_value(num_workers_index,male_indices[x]).replace(',','')))
                    else:
                        dict_work['sex'].append('Female')
                        if sheet.cell_value(rownames_work_index[c], female_indices[x]) == '-':
                            dict_work['workers_16'].append(0)
                        else:
                            dict_work['workers_16'].append(Decimal(sheet.cell_value(rownames_work_index[c], female_indices[x]).replace('%', '')) * int(sheet.cell_value(num_workers_index, female_indices[x]).replace(',', '')))


    ####TIME OF DEPARTURE TO GO TO WORK
    #Get rows
    result = get_rownameindex(sheet, num_rows, 'TIME OF DEPARTURE TO GO TO WORK', 'TRAVEL TIME TO WORK')
    rownames_depart = result[0]
    rownames_depart_index = result[1]

    #Get number of workers don't work from home
    for n in range(num_rows):
        if sheet.cell_value(n,0) == 'Workers 16 years and over who did not work from home':
            num_workers_nothome_index = n

    #Create table
    dict_depart = {'location_id':[],'depart_time':[], 'sex':[], 'workers_16_nothome':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_depart)):
            for s in range(0, 2):
                dict_depart['location_id'].append(location_id[x])
                dict_depart['depart_time'].append(rownames_depart[c])
                if s == 0:
                    dict_depart['sex'].append('Male')
                    if sheet.cell_value(rownames_depart_index[c], male_indices[x]) == '-':
                        dict_depart['workers_16_nothome'].append(0)
                    else:
                        dict_depart['workers_16_nothome'].append(Decimal(sheet.cell_value(rownames_depart_index[c],male_indices[x]).replace('%',''))*\
                        int(sheet.cell_value(num_workers_nothome_index,male_indices[x]).replace(',','')))
                else:
                    dict_depart['sex'].append('Female')
                    if sheet.cell_value(rownames_depart_index[c], female_indices[x]) == '-':
                        dict_depart['workers_16_nothome'].append(0)
                    else:
                        dict_depart['workers_16_nothome'].append(Decimal(sheet.cell_value(rownames_depart_index[c],female_indices[x]).replace('%',''))*\
                        int(sheet.cell_value(num_workers_nothome_index,female_indices[x]).replace(',','')))


    ####TRAVEL TIME TO WORK
    #Get rows
    result = get_rownameindex(sheet, num_rows, 'TRAVEL TIME TO WORK', 'Mean travel time to work (minutes)')
    rownames_time = result[0]
    rownames_time_index = result[1]

    #Create table
    dict_time = {'location_id':[],'travel_time':[], 'sex':[], 'workers_16_nothome':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_time)):
            for s in range(0, 2):
                dict_time['location_id'].append(location_id[x])
                dict_time['travel_time'].append(rownames_time[c])
                if s == 0:
                    dict_time['sex'].append('Male')
                    if sheet.cell_value(rownames_time_index[c], male_indices[x]) == '-':
                        dict_time['workers_16_nothome'].append(0)
                    else:
                        dict_time['workers_16_nothome'].append(Decimal(sheet.cell_value(rownames_time_index[c],male_indices[x]).replace('%',''))*int(sheet.cell_value(num_workers_nothome_index,male_indices[x]).replace(',','')))
                else:
                    dict_time['sex'].append('Female')
                    if sheet.cell_value(rownames_time_index[c], female_indices[x]) == '-':
                        dict_time['workers_16_nothome'].append(0)
                    else:
                        dict_time['workers_16_nothome'].append(Decimal(sheet.cell_value(rownames_time_index[c], female_indices[x]).replace('%', '')) * int(sheet.cell_value(num_workers_nothome_index, female_indices[x]).replace(',', '')))

    ####VEHICLES AVAILABLE
    #Get rows
    result = get_rownameindex(sheet, num_rows, 'Workers 16 years and over in households', 'PERCENT ALLOCATED')
    rownames_veh = result[0]
    rownames_veh_index = result[1]

    #Get number of workers in household
    for n in range(num_rows):
        if sheet.cell_value(n,0) == 'Workers 16 years and over in households':
            num_workers_house_index = n

    #Create table
    dict_veh = {'location_id':[],'num_veh':[], 'sex':[], 'households':[]}
    for x in range(len(location_id)):
        for c in range(len(rownames_veh)):
            for s in range(0, 2):
                dict_veh['location_id'].append(location_id[x])
                dict_veh['num_veh'].append(rownames_veh[c])
                if s == 0:
                    dict_veh['sex'].append('Male')
                    if sheet.cell_value(rownames_veh_index[c],male_indices[x]) == '-':
                        dict_veh['households'].append(0)
                    else:
                        dict_veh['households'].append(Decimal(sheet.cell_value(rownames_veh_index[c],male_indices[x]).replace('%',''))*\
                        int(sheet.cell_value(num_workers_house_index,male_indices[x]).replace(',','')))
                else:
                    dict_veh['sex'].append('Female')
                    if sheet.cell_value(rownames_veh_index[c],female_indices[x]) == '-':
                        dict_veh['households'].append(0)
                    else:
                        dict_veh['households'].append(Decimal(sheet.cell_value(rownames_veh_index[c],female_indices[x]).replace('%',''))*\
                        int(sheet.cell_value(num_workers_house_index,female_indices[x]).replace(',','')))

    ####Create output file
    df_transpo = pd.DataFrame(dict_transpo,columns=['location_id', 'transpo_mode', 'transpo_mode_sub', 'transpo_mode_sub1', 'sex','workers_16_nothome'])
    df_transpo["workers_16_nothome"] = pd.to_numeric(df_transpo["workers_16_nothome"]).div(100)
    df_work = pd.DataFrame(dict_work,columns=['location_id','work_location','work_location_sub','sex','workers_16'])
    df_work["workers_16"] = pd.to_numeric(df_work["workers_16"]).div(100)
    df_depart = pd.DataFrame(dict_depart,columns=['location_id','depart_time','sex','workers_16_nothome'])
    df_depart["workers_16_nothome"] = pd.to_numeric(df_depart["workers_16_nothome"]).div(100)
    df_time = pd.DataFrame(dict_time,columns=['location_id','travel_time','sex','workers_16_nothome'])
    df_time["workers_16_nothome"] = pd.to_numeric(df_time["workers_16_nothome"]).div(100)
    df_veh = pd.DataFrame(dict_veh,columns=['location_id','num_veh','sex','households'])
    df_veh["households"] = pd.to_numeric(df_veh["households"]).div(100)

    dfs = [df_transpo, df_work, df_depart, df_time, df_veh]
    excelname, sheetnames = 'S0801_parsed.xlsx', ['TransportationMode', 'WorkLocation', 'DepartureTime', 'TravelTime','Vehicles','Summary']
    return dfs, excelname, sheetnames







