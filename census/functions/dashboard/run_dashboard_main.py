def run_dashboard():
    import dash
    from dash import dcc
    from dash import html
    from dash.dependencies import Input, Output
    import plotly.express as px
    import pandas as pd
    import json

    df = pd.read_json('https://api.census.gov/data/2019/acs/acs5/profile?get=DP05_0001E&for=tract:*&in=state:02&key=2d06b2407a7edc598608026ac92014c461d42dbb')
    # Promote header row
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header

    df['GEOID'] = df['state'] + df['county'] + df['tract']

    with open("WebApp/census/dashboard/cb_2019_02_tract_500k.json") as fp:
        geojson = json.load(fp)
    result = len(geojson['features'])
    counties = list(set(df['county'].values.tolist()))
    counties.insert(0,'All')
    df['DP05_0001E'] = df['DP05_0001E'].astype(int)

    return result

    # app = dash.Dash(__name__)

    # app.layout = html.Div([
    #     html.H1("Census Data Dashboard", style={'text-align': 'center'}),

    #     dcc.Dropdown(
    #         id='slct_county', 
    #         options=[{'value': x, 'label': x} 
    #                  for x in counties],
    #         multi=False,
    #         value=counties[0],
    #         style={'width': "40%"}
    #     ),
    #     dcc.Graph(id="choropleth"),
    # ])

    # @app.callback(
    #     Output("choropleth", "figure"), 
    #     [Input("slct_county", "value")])


    # def display_choropleth(option_slctd):
        
    #     dff = df
    #     if option_slctd=='All':
    #         pass
    #     else:
    #         dff = dff[dff['county']==option_slctd]
    #     # dff_copy = dff_copy[dff_copy['county']=='170']
    #     fig = px.choropleth_mapbox(dff, geojson=geojson, locations='GEOID', featureidkey="properties.GEOID", color='DP05_0001E',
    #                            color_continuous_scale='Viridis',height=750,width=1000,zoom=3,
    #                            center={'lat':62.673634, 'lon':-155.647922},
    #                            mapbox_style="open-street-map",
    #                            opacity=0.5,
    #                           )

    #     fig.update_layout(
    #     font=dict(
    #         family="Calibri",
    #         size=12,
    #         color="Black"
    #         )
    #     )
    #     # fig.update_geos(fitbounds="geojson", visible=False)
    #     # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    #     return fig

    # app.run_server(debug=True)