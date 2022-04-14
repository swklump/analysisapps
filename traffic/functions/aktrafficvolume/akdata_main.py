
def akdata_script(unzipped, convert_zeros):
    import pandas as pd
    import io, zipfile
    import numpy as np
    from datetime import datetime, timedelta
    from .helperfunctions import excel_date

    # Create empty dataframe
    fnames = unzipped.namelist()
    df_final = pd.DataFrame()

    for f in fnames:

        # Read in file, get report type, get site name
        df_og = pd.read_excel(unzipped.open(f))
        report_type = df_og.columns.tolist()[0]
        if 'Speed' in report_type:
            report_type = 'combined_speeds.xlsx'
        elif 'Volume' in  report_type:
            report_type = 'combined_volumes.xlsx'
        site_name = df_og.iloc[0, 1]

        # Find rows with "All" in first column
        index_all = df_og.index[df_og.iloc[:,0].isin(['All Northbound','All Southbound','All Eastbound','All Westbound'])].tolist()
        for i in index_all:
            df_temp = pd.DataFrame()
            # Reassign header rows for first direction
            direction = df_og.iloc[i, 0].replace('All ','')
            new_header = df_og.iloc[i+2]
            df = df_og[i+3:]

            df.columns = new_header
            if "Workday" in df.columns.tolist():
                del df["Workday"]
            if "7 Day" in df.columns.tolist():
                del df["7 Day"]
            if "Count" in df.columns.tolist():
                del df["Count"]
            df.columns.values[0] = "time"
            df = df.loc[:, pd.notnull(df.columns)]
            df = df[:24]

            # Make column of repeating times
            df_temp['time'] = pd.concat([df['time']] * (len(df.columns.tolist())-1))

            # Make column of repeating dates
            dates_list = []
            for d in df.columns.tolist()[1:]:
                dates_list += ([d] * 24)
            df_temp['date'] = dates_list

            if report_type == 'combined_speeds.xlsx':
                speeds_list = []
                for d in df.columns.tolist()[1:]:
                    speeds_list += df[d].values.tolist()
                df_temp['speeds'] = speeds_list
            elif report_type == 'combined_volumes.xlsx':
                volumes_list = []
                for d in df.columns.tolist()[1:]:
                    volumes_list += df[d].values.tolist()
                df_temp['volumes'] = volumes_list

            # Make column of repeating site names and direction
            df_temp.insert(loc=0, column='site', value=[site_name] * ((len(df.columns.tolist())-1)*24))
            df_temp.insert(loc=1, column='direction', value=[direction] * ((len(df.columns.tolist()) - 1) * 24))

            df_final = pd.concat([df_final,df_temp])

    # Convert to datetime
    excel_dates = []
    df_final.reset_index(drop=True, inplace=True)
    for x in range(len(df_final['date'].values.tolist())):
        hour = df_final['time'].iloc[x][0:2]
        year = df_final['date'].iloc[x][0:4]
        month = df_final['date'].iloc[x][5:7]
        day = df_final['date'].iloc[x][8:10]
        date = datetime(year=int(year), month=int(month), day=int(day))
        excel_dates.append(excel_date(date + timedelta(hours=int(hour))))
    df_final.insert(loc=4, column='excel_datetime', value=excel_dates)

    # replace zeros
    if len(convert_zeros) > 0:
        df_final = df_final.replace(0,'')

    # Send to zipped folder
    buf = io.BytesIO()
    zs = zipfile.ZipFile(buf, mode='w')
    zfm1 = zs.open(report_type, 'w')
    with pd.ExcelWriter(zfm1, engine='xlsxwriter') as writer:
        df_final.to_excel(writer, sheet_name='Data', index=False)
    zfm1.close()
    zs.close()

    return buf, report_type

