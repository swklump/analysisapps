from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from django.contrib import messages

from .functions.aktrafficvolume.akdata_main import akdata_script
from .functions.ihsdm.ihsdm_parse_main import ihsdm_parse_func
from .functions.tam.tam import tam_func

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

email_master = 'sam.klump@outlook.com'
email_href = 'mailto:' + email_master

@csrf_exempt
def traffic(request):
    return render(request, 'traffic.html', context={'email':email_master, 'email_link':email_href})

@csrf_exempt
def aktrafficdata(request):
    if request.method == "POST":
        try:
            # Step 2
            zipped_folder = request.FILES["zip_file"]
            unzipped = zipfile.ZipFile(zipped_folder)

            # Step 3
            convert_zeros = request.POST.getlist('zeros')
            # Run module
            buf, report_type = akdata_script(unzipped, convert_zeros)
            buf.seek(0)
            response = StreamingHttpResponse(buf,content_type="application/zip")
            if report_type == 'combined_speeds.xlsx':
                response['Content-Disposition'] = 'attachment; filename="combined_speeds.zip"'
                return response
            elif report_type == 'combined_volumes.xlsx':
                response['Content-Disposition'] = 'attachment; filename="combined_volumes.zip"'
                return response
        except Exception:
            return render(request, 'aktrafficdata/aktrafficdata-error.html')
    return render(request, 'aktrafficdata/aktrafficdata.html', context={'email':email_master, 'email_link':email_href})


### IHSDM
@csrf_exempt
def ihsdm(request):

    if request.method == "POST":

        ### STEP 1
        zipped_folder = request.FILES["zip_file"]
        if zipped_folder.name[-4:] != '.zip':
            messages.error(request, f'Please upload a zipped folder (.zip).')
            return render(request, 'ihsdm/ihsdm-error.html')
        unzipped = zipfile.ZipFile(zipped_folder)
        fnames = unzipped.namelist()

        for html_file in fnames:
            # Check if file is an Excel file
            if html_file[-5:] != '.html' and html_file[-4:] != '.htm':
                messages.error(request, f'Please upload a zipped folder only containing HTML (.html or .htm) files.')
                return render(request, 'ihsdm/ihsdm-error.html')

        # Set up zipped folder output
        buf = io.BytesIO()
        zs = zipfile.ZipFile(buf, mode='w')

        # get file names, beautiful soup files, html dfs, and highway names
        fnames = unzipped.namelist()
        bs_files = [bs(unzipped.open(fnames[h], 'r'), 'html.parser') for h in range(len(fnames))]

        # check if any tables in html
        try:
            html_dfs = [pd.read_html(unzipped.open(fnames[h], 'r')) for h in range(len(fnames))]
        except ValueError:
            messages.error(request, f'Please upload a zipped folder of IHSDM evaluation HTML files. No tables were found.')
            return render(request, 'ihsdm/ihsdm-error.html')

        # get highway names, check that not empty
        highwaynames = []
        for h in range(len(bs_files)):
            bs_text = bs_files[h].find_all('font')
            for f in bs_text:
                check_text = f.text.replace("\t", "").replace("\r", "").replace("\n", "")
                if 'Highway Title' in check_text or 'Intersection Title' in check_text:
                    index = check_text.find(':')
                    highwaynames.append(check_text[index+2:])
        if len(highwaynames) == 0:
            messages.error(request, f'Please upload a zipped folder of IHSDM evaluation HTML files. No element names '
                                    f'were found in the file.')
            return render(request, 'ihsdm/ihsdm-error.html')

        # general error exception
        try:
            ihsdm_parse_func(bs_files, html_dfs, highwaynames, zs)
        except Exception:
            messages.error(request, f'Please make sure that standard HTML output files from IHSDM are uploaded in a zipped folder.'
                                    f' If the error persists, please send an email to Sam Klump at '
                                    f'sam.klump@outlook.com.')
            return render(request, 'ihsdm/ihsdm-error.html')

        zs.close()
        buf.seek(0)
        response = StreamingHttpResponse(buf,content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename="ihsdm_parsed_files.zip"'
        return response
    return render(request, 'ihsdm/ihsdm.html', context={'email':email_master, 'email_link':email_href})


### TRIP ASSIGNMENT MODEL
@csrf_exempt
def tam(request):
    # dummy variables for map
    # dict_lines = {'link_num':['','','','',''],'lat':['','','','',''], 'lon':['','','','',''],'trips':['','','','',''], 'cat':['1','2','3','4','5']}
    # df = pd.DataFrame(dict_lines)
    # plot_div = return_graph_tam(df)

    if request.method == "POST":

        outputtype = request.POST['outputtype']
        # try:
        uploaded_file = request.FILES["excel_file"]
        if uploaded_file.name[-5:] != '.xlsx':
            messages.error(request, f'Please upload an Excel (.xlsx) file.')
            return render(request, 'tam/tam-error.html')
        func_results = tam_func(uploaded_file)
        buf, df_map = func_results[0], func_results[1]
        buf.seek(0)

        if outputtype == 'table':
            response = StreamingHttpResponse(buf,content_type="application/zip")
            response['Content-Disposition'] = 'attachment; filename="tam_outputtables.zip"'
            return response
        elif outputtype == 'map':
            plot_div = return_graph_tam(df_map)
            return render(request, 'tam/tam.html', context={'plot_div': plot_div, 'email':email_master, 'email_link':email_href})

        # except Exception:
        #     return render(request, 'tam/tam-error.html')

    return render(request, 'tam/tam.html', context={'email':email_master, 'email_link':email_href})


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

#For tam app
def return_graph_tam(df):
    plotly.express.set_mapbox_access_token('pk.eyJ1Ijoic3drbHVtcCIsImEiOiJja3Z4MGk0aTYwaGlrMnBubzYyeXA2bW91In0.UmjBh9eSwNC8BJ0p5MRF-w')
    df = df.sort_values(['trips'],ascending=True)
    uniquevals = df['cat'].unique()
    fig = px.line_mapbox(df, lat="lat", lon="lon", color="cat",line_group="link_num",
    color_discrete_map = {uniquevals[0]:'green',uniquevals[1]:'yellow',uniquevals[2]:'orange',uniquevals[3]:'red',uniquevals[4]:'black',},
    center = {"lat":  61.565, "lon":-149.52}, zoom=10.5,
    mapbox_style="open-street-map",
    labels={'trips_perday':'Volumes'},
    hover_data=['link_num','cat']
    )

    fig.update_traces(line={'width':5})
    fig.update_layout(
        font=dict(
            family="Calibri",
            size=24,
            color="Gray"
        )
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.08,
        xanchor="left",
        x=0,
        title=dict(text="Modeled Trips (quintiles)")
    ))

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(height=700)


    plot_div = plot(fig,output_type='div',include_plotlyjs=False, show_link=False, link_text="")
    return plot_div