from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from django.contrib import messages

from .functions.parse.parse_main import parse_func
from .functions.descriptiveanalysis.data_analysis_tract import analyze_tract
from .functions.descriptiveanalysis.data_analysis_blockgroup import analyze_blockgroup
from .functions.advancedanalysis.advancedanalysis_main import advancedanalysis_func
from .functions.advancedanalysis.test import test_func
from .functions.dashboard.run_dashboard_main import run_dashboard

import zipfile, xlrd, io
from bs4 import BeautifulSoup as bs
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True
import pandas as pd
import plotly
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import textwrap
import psycopg2

email_master = 'sam.klump@outlook.com'
email_href = 'mailto:' + email_master

available_tables = {'tracts': ['DP04', 'DP05', 'S0801', 'S1501','S1701','S1810', 'S1901'],
                                'block_groups': ['B01001','B03002', 'B08134','B15002', 'B17017', 'B19001',
                                                 'B25003', 'B25008', 'B25034','B25075','C17002','C21007']}


# --------------------------------------------------------------------------------------------------------------------------------------------
### CENSUS APP
@csrf_exempt
def census(request):
    return render(request, 'census.html', context={'email':email_master, 'email_link':email_href})

@csrf_exempt
def parse(request):

    if request.method == "POST":
        uploaded_file = request.FILES["excel_file"]
        if uploaded_file.name[-4:] != '.zip' and uploaded_file.name[-5:] != '.xlsx':
            messages.error(request, f'Please upload an Excel (.xlsx) file or zipped folder (.zip).')
            return render(request, 'parse-error.html')

        ex_yn = ''
        if uploaded_file.name[-5:] == '.xlsx':
            ex_yn='excel'
            fnames = [uploaded_file.name]
        elif uploaded_file.name[-4:] == '.zip':
            unzipped = zipfile.ZipFile(uploaded_file)
            fnames = unzipped.namelist()
        wbs = []
        table_ids = []
        years = []
        for census_file in fnames:

            # Check if file is an Excel file
            if census_file[-5:] != '.xlsx':
                messages.error(request, f'Please upload an Excel (.xlsx) file or a zipped folder containing only Excel files.')
                return render(request, 'parse-error.html')
            if ex_yn == 'excel':
                wb = xlrd.open_workbook(file_contents=uploaded_file.read())
            else:
                wb = xlrd.open_workbook(file_contents=unzipped.open(census_file, 'r').read())

            # Check if file is in right format
            if 'Information' not in wb.sheet_names() or 'Data' not in wb.sheet_names():
                messages.error(request, f'The uploaded file is not in the correct format. The file must be downloaded from the data.census.gov website '
                                        f'in the standard Excel format with an "Information" and "Data" tabs in the workbook file.')
                return render(request, 'parse-error.html')

            # Need to check if (1) a table ID can be found and (2) if the table id is available
            sheet = wb.sheet_by_name('Information')
            num_rows_info = sheet.nrows

            # Get table ID from spreadsheet
            table_id = ''
            year = ''
            for n in range(num_rows_info):
                if sheet.cell_value(n, 0) == 'TABLE ID:':
                    table_id = sheet.cell_value(n, 1)
                elif sheet.cell_value(n, 0) == 'VINTAGE:':
                    year = int(sheet.cell_value(n, 1))

            # Check if table ID available and is available for parsing
            if table_id == '' or year == '':
                messages.error(request,
                               f'The uploaded file is not in the correct format. The file must have a "TABLE ID:" and "VINTAGE" cell in the '
                               f'"Information" tab. Please download a table file from the Census data website.')
                return render(request, 'parse-error.html')

            if table_id not in available_tables['tracts'] and table_id not in available_tables['block_groups']:
                messages.error(request,
                               f'The uploaded table ID ' + table_id + ' is not currently available for parsing. If you would like this table '
                               f'to be added to the app, please send an email to Sam Klump at sam.klump@outlook.com.')
                return render(request, 'parse-error.html')

            wbs.append(wb)
            table_ids.append(table_id)
            years.append(year)

        # General exception error
        try:
            buf = parse_func(wbs, table_ids, years)
            buf.seek(0)
        except Exception:
            messages.error(request, f'Please check that the uploaded file(s) were not edited after downloading from the '
                                    f'US Census website. If the error persists, please send an email to Sam Klump at '
                                    f'sam.klump@outlook.com.')
            return render(request, 'parse-error.html')

        response = StreamingHttpResponse(buf,content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename="census_parsed_files.zip"'
        return response
    return render(request, 'parse.html', context={'email':email_master, 'email_link':email_href})


@csrf_exempt
def descriptiveanalysis(request):
    # plot_div = return_graph()
    if request.method == "POST":

        ### STEP 1
        zipped_folder = request.FILES["zip_file"]
        if zipped_folder.name[-4:] != '.zip':
            messages.error(request, f'Please upload a zipped folder (.zip).')
            return render(request, 'descriptiveanalysis-error.html')
        unzipped = zipfile.ZipFile(zipped_folder)
        fnames = unzipped.namelist()
        for census_file in fnames:
            # Check if file is an Excel file
            if census_file[-5:] != '.xlsx':
                messages.error(request, f'Please upload a zipped folder only containing Excel (.xlsx) files.')
                return render(request, 'descriptiveanalysis-error.html')

        # Get table names
        tablenames = []
        for x in range(len(fnames)):
            try:
                df_detail = pd.read_excel(unzipped.open(fnames[x], 'r'), sheet_name='FileDetails')
                tablenames.append(df_detail.loc[df_detail['Detail'] == 'Census Table ID', 'Value'].values[0])
            except Exception:
                messages.error(request, f'Upload a zipped folder of Excel files outputted from the "Parse Census Data" '
                                        f'module. Do not delete or edit the "FileDetails" sheet in the Excel files.')
                return render(request, 'descriptiveanalysis-error.html')

        # Put applicable table names into tracts list and block groups list
        tablenames_tracts = []
        tablenames_blockgroups = []
        for x in range(len(tablenames)):
            if tablenames[x] in available_tables['tracts']:
                tablenames_tracts.append(tablenames[x])
            if tablenames[x] in available_tables['block_groups']:
                tablenames_blockgroups.append(tablenames[x])

        # Check that table IDs are available
        if len(tablenames_tracts) == 0 and len(tablenames_blockgroups) == 0:
            messages.error(request, f'Upload a zipped folder of Excel files outputted from the "Parse Census Data" '
                                    f'module.')
            return render(request, 'descriptiveanalysis-error.html')

        ### STEP 2
        cats_dict = {'elderly':request.POST['old'], 'nondriver':request.POST['nondriver'],'lowhousevalue':request.POST['housevalue']}
        checks_groups = request.POST.getlist('checks')

        ### STEP 3
        checks_calcs = request.POST.getlist('calcs')
        if "matrix" in checks_calcs:
            if len(fnames) < 2:
                messages.error(request, f'Please uncheck the "Correlation Matrix" checkbox or upload a zipped folder '
                                        f'with at least two parsed Excel files.')
                return render(request, 'descriptiveanalysis-error.html')
        graphset_list = ['test']

        # Check that something is checked
        val = 0
        for v in cats_dict.values():
            if v == 'dontinclude':
                pass
            else:
                val += 1
        val += len(checks_groups)
        if val == 0:
            messages.error(request, f'You must include at least one selection from Step 2.')
            return render(request, 'descriptiveanalysis-error.html')
        if "matrix" in checks_calcs:
            if val < 2:
                messages.error(request, f'Please uncheck the "Correlation Matrix" checkbox or make at least two applicable '
                                        f'selections in Step 2.')
                return render(request, 'descriptiveanalysis-error.html')
        # Run module
        # Set up zipped folder output
        buf = io.BytesIO()
        zs = zipfile.ZipFile(buf, mode='w')

        try:
            if len(tablenames_tracts) != 0:
                # Run module
                results = analyze_tract(unzipped, cats_dict, checks_groups, checks_calcs, zs, tablenames_tracts, fnames)
                dfs, sheetnames, keep_index = results[0], results[1], results[2]

            elif len(tablenames_blockgroups) != 0:
                results = analyze_blockgroup(unzipped, cats_dict, checks_groups, checks_calcs, zs,tablenames_blockgroups, fnames)
                dfs, sheetnames, keep_index = results[0], results[1], results[2]

            # Create zipped stream to add spreadsheet to
            zfm1 = zs.open('censusdata_analyzed.xlsx', 'w')
            with pd.ExcelWriter(zfm1, engine='xlsxwriter') as writer:
                for d in range(len(dfs)):
                    dfs[d].to_excel(writer, sheet_name=sheetnames[d], index=keep_index[d])

        except Exception:
            messages.error(request, f'Please check that no column or sheet names were changed within each file '
                                    f'outputted from the "Parse Census Data" module. Check that the selections made in '
                                    f'Step 2 have the corresponding Table ID in the zipped folder. If this error persists, please '
                                    f'send an email to Sam Klump at sam.klump@outlook.com.')
            return render(request, 'descriptiveanalysis-error.html')

        zfm1.close()
        zs.close()
        buf.seek(0)
        response = StreamingHttpResponse(buf,content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename="census_analysis_files.zip"'
        return response
    return render(request, 'descriptiveanalysis.html', context={'email':email_master, 'email_link':email_href})


@csrf_exempt
def advancedanalysis(request):
    # dummy variables for plot
    plot_results = return_graph(pd.DataFrame({},columns=['x','y']),'x', 'y','x','y',0)
    plot_div, model_results, pred_val = plot_results[0], plot_results[1], plot_results[2]

    cols = """'DP05_0001PE', 'DP05_0002PE', 'DP05_0003PE', 'DP05_0004PE', 'DP05_0005PE', 'DP05_0006PE', 'DP05_0007PE', 'DP05_0008PE', 'DP05_0009PE', 'DP05_0010PE', 'DP05_0011PE', 'DP05_0012PE',
        'DP05_0013PE', 'DP05_0014PE', 'DP05_0015PE', 'DP05_0016PE', 'DP05_0017PE', 'DP05_0018PE', 'DP05_0019PE', 'DP05_0020PE', 'DP05_0021PE', 'DP05_0022PE', 'DP05_0023PE', 'DP05_0024PE', 'DP05_0025PE',
        'DP05_0026PE', 'DP05_0027PE', 'DP05_0028PE', 'DP05_0029PE', 'DP05_0030PE', 'DP05_0031PE', 'DP05_0032PE', 'DP05_0033PE', 'DP05_0034PE', 'DP05_0035PE', 'DP05_0036PE', 'DP05_0037PE', 'DP05_0038PE',
        'DP05_0039PE', 'DP05_0040PE', 'DP05_0041PE', 'DP05_0042PE', 'DP05_0043PE', 'DP05_0044PE', 'DP05_0045PE', 'DP05_0046PE', 'DP05_0047PE', 'DP05_0048PE', 'DP05_0049PE', 'DP05_0050PE', 'DP05_0051PE',
        'DP05_0052PE', 'DP05_0053PE', 'DP05_0054PE', 'DP05_0055PE', 'DP05_0056PE', 'DP05_0057PE', 'DP05_0058PE', 'DP05_0059PE', 'DP05_0060PE', 'DP05_0061PE', 'DP05_0062PE', 'DP05_0063PE', 'DP05_0064PE',
        'DP05_0065PE', 'DP05_0066PE', 'DP05_0067PE', 'DP05_0068PE', 'DP05_0069PE', 'DP05_0070PE', 'DP05_0071PE', 'DP05_0072PE', 'DP05_0073PE', 'DP05_0074PE', 'DP05_0075PE', 'DP05_0076PE', 'DP05_0077PE',
        'DP05_0078PE', 'DP05_0079PE', 'DP05_0080PE', 'DP05_0081PE', 'DP05_0082PE', 'DP05_0083PE', 'DP05_0084PE', 'DP05_0085PE', 'DP05_0086PE', 'DP05_0087PE', 'DP05_0088PE', 'DP05_0089PE',
        'GEO_ID', 'NAME', 'state', 'county', 'tract'"""

    if request.method == "POST":
        cats_dict = {'table_ind': request.POST['table_ind'], 'var_ind': request.POST['var_ind'],
                     'table_dep': request.POST['table_dep'], 'var_dep': request.POST['var_dep'],
                     'ind_var_val': request.POST['ind_var_val'], 'year': request.POST['year'],
                     'state': request.POST['state']}

        xlab = cats_dict['var_ind'][cats_dict['var_ind'].find(':')+1:]
        ylab = cats_dict['var_dep'][cats_dict['var_dep'].find(':')+1:]
        # try:
            # df = advancedanalysis_func(cats_dict)
        # val = test_func(cats_dict, cur)
        val = ''
        #     plot_results = return_graph(df, 'var_ind', 'var_dep', '% "'+xlab+'"', '% "'+ylab+'"', cats_dict['ind_var_val'])
        #     plot_div, model_results, pred_val = plot_results[0], plot_results[1], round(plot_results[2],1)
        # except Exception:
        #     pass


        return render(request, 'advancedanalysis.html', context={'plot_div': plot_div, 'model_results':val,'cols':cols})
        # return render(request, 'advancedanalysis.html', context={'plot_div': plot_div, 'model_results':model_results,
        # 'input_val':int(cats_dict['ind_var_val']), 'input_var': xlab, 'pred_val':pred_val, 'pred_var':ylab})
    return render(request, 'advancedanalysis.html', context={'plot_div': plot_div, 'model_results':model_results,'cols':cols})

#For census advanced analysis app
def return_graph(df, var_ind, var_dep, xlab, ylab, ind_var_val):
    if var_ind == 'x':
        fig = px.scatter(df, x = var_ind, y=var_dep,trendline="ols",
        labels={var_ind:xlab, var_dep:ylab}).update_layout(title_x=0.5)

    else:
        split_text = textwrap.wrap(ylab + ' by ') + textwrap.wrap(xlab)
        fig = px.scatter(df, x = var_ind, y=var_dep,trendline="ols",
        labels={var_ind:xlab, var_dep:ylab}, title= '<br>'.join(split_text)).update_layout(title_x=0.5)

    fig.update_layout(
    title_font_family="Arial",
    )
    fig.update_layout(
    title={
        'xanchor': 'center',
        'yanchor': 'top'})

    results = px.get_trendline_results(fig)
    if len(results) > 0:
        results = results.px_fit_results.iloc[0].summary()

        fig.update_layout(showlegend=True)
        fig.update_layout(
            legend=dict(
                x=0,y=1,
                traceorder="normal",
                font=dict(
                    family="sans-serif",
                    size=12,
                    color="Black"
                ),
                bgcolor="LightSteelBlue",
                bordercolor="dimgray",
                borderwidth=2
            ))

        # retrieve model estimates
        model = px.get_trendline_results(fig)
        alpha = model.iloc[0]["px_fit_results"].params[0]
        beta = model.iloc[0]["px_fit_results"].params[1]

        # restyle figure
        fig.data[0].name = 'Tracts/Block Groups'
        fig.data[0].showlegend = True
        fig.data[1].name = fig.data[1].name  + ' y = ' + str(round(alpha, 2)) + ' + ' + str(round(beta, 2)) + 'x'
        fig.data[1].showlegend = True
        pred_val = alpha + beta*int(ind_var_val)
        # addition for r-squared
        rsq = model.iloc[0]["px_fit_results"].rsquared
        fig.add_trace(go.Scatter(x=[max(var_ind)], y=[max(var_ind)],
                                name = "R-squared" + ' = ' + str(round(rsq, 2)),
                                showlegend=True,
                                mode='markers',
                                marker=dict(color='rgba(0,0,0,0)')
                                ))

    else:
        results = ''
        pred_val = 0
    plot_div = plot(fig,output_type='div',include_plotlyjs=False, show_link=False, link_text="")
    return plot_div, results, pred_val


@csrf_exempt
def parse_tableids(request):
    return render(request, 'parse-tableids.html')

