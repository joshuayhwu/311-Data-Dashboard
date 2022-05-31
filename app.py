import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "notebook_connected"

from design import apply_figure_style
from design import CONFIG_OPTIONS
from design import DISCRETE_COLORS
from design import LABELS
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, State
import dash_daq as daq
import dash.dependencies
from dash.exceptions import PreventUpdate

app = Dash(__name__)

# Attempt to load data with Local CSV file
# demo_df = pd.read_csv("venv\MyLA311_Service_Request_Data_2020.csv", engine='python')
# demo_df.head()

# Attempt to load data with 311 Data API 
import requests as re
results = re.get("https://data.lacity.org/resource/rq3b-xjk8.json")
data_json = results.json()
data_2020 = pd.json_normalize(data_json)


app.layout = html.Div([

    html.Div(children=[

        ## Neighborhood Council Dashboard
        html.Div(children=[
            html.H2("LA 311 Requests - Neighborhood Council Summary Dashboard", style={'vertical-align':'middle'} ),
            html.Div([daq.ToggleSwitch(id='dataQualitySwitch', value=True, style={'height':'vh'}, size = 35),
            html.Div(id='dataQualityOutput')], style={'font-family':'Open Sans'})
        ], style={'display':'flex', "justify-content": "space-between", 'vertical-align':'middle' , 'height':'9vh', 'width':'97.5vw'}),
    
        
        ## Summary Dropdown
        html.Div(children=[
            html.Div(dcc.Dropdown([n for n in set(data_2020['ncname'])], ' ', id='nc_dropdown', placeholder="Select a Neighborhood Council..."), style={'display': 'inline-block', 'width':'48.5vw'}),
            #html.Div(dcc.Dropdown([n for n in set(data_2020['requesttype'])], ' ', id='nc_dropdown2', placeholder="Select a Request Type..."), style={'display': 'inline-block', 'width':'32vw' }),
            # html.Div(dcc.Dropdown(id='nc_dropdown2', placeholder="Select a Request Type..."), style={'display': 'inline-block', 'width':'32vw' }),
            html.Div(dcc.Dropdown(id='nc_dropdown_filter', multi=True, placeholder="Remove a Request Type..."), style={'display': 'inline-block', 'width':'48.5vw'})
        ], style={'display':'flex' ,  "justify-content": "space-between", "width": "97.5vw"}),

        
        
        
        html.Div(html.Br(), style={"height":"1vh"}),
        html.Div(dcc.Graph(id='numReqLineChart', style={"height":"40vh", 'width':'97.4vw'}), style={"border":"0.5px black solid", "height":"40vh", 'width':'97.4vw'}),
        html.Div(html.Br(), style={"height":"1vh"}),
        html.Div(children=[
            html.Div(
                dcc.Graph(
                    id="reqTypePieChart", style={"height":"40vh", 'width':'48.5vw'}
                    ), style={'display': 'inline-block', 'width':'48.5vw', "border":"0.5px black solid", "height":"40vh"}), # for border-radius , add stuff later
            html.Div(
                dcc.Graph( 
                    id="timeCloseHist", style={"height":"40vh", 'width':'48vw'}
                    ), style={'display': 'inline-block', 'width':'48vw', "border":"0.5px black solid", "height":"40vh"})
        ], style={'display':'flex', "justify-content": "space-between", "width":'97.5vw'})
        
    ]),

    html.Div(html.Br(), style={"height":"5vh"}),
    # Neighborhood Council Summarization Dashboard
    html.Div(children=[
        html.H2("LA 311 Requests - Neighborhood Council Comparison Dashboard")
    ], style={'textAlign':'center'}),

    ## Comparison Dropdowns
    html.Div(children=[
        html.Div(dcc.Dropdown([n for n in set(data_2020['ncname'])], ' ', id='nc_comp_dropdown', placeholder="Select a Neighborhood Council..."), style={'display': 'inline-block', 'width':'48.5vw'}),
        html.Div(dcc.Dropdown([n for n in set(data_2020['ncname'])], ' ', id='nc_comp_dropdown2', placeholder="Select a Neighborhood Council..."), style={'display': 'inline-block', 'width':'48.5vw'}),
    ], style={'display':'flex' ,  "justify-content": "space-between", "width": "97.5vw"}),

        
    html.Div(html.Br(), style={"height":"1vh"}),

    ## NC Comparison - Indicator Visuals
    html.Div(children = [
        html.Div(children = [
        # html.Div(
        #     [
        #         dbc.Button("Open modal", id="open", n_clicks=0),
        #         dbc.Modal(
        #             [
        #                 dbc.ModalHeader(dbc.ModalTitle("Header")),
        #                 dbc.ModalBody("This is the content of the modal"),
        #                 dbc.ModalFooter(
        #                     dbc.Button(
        #                         "Close", id="close", className="ms-auto", n_clicks=0
        #                     )
        #                 ),
        #             ],
        #             id="modal",
        #             is_open=False,
        #         ),
        #     ]
        # ),
            html.Div([
                html.H6("Total Number of Requests", style={"text-align":'center'}), 
                html.H1(id='totalReqCard', style={"text-align":'center'})],  
                style={'display': 'inline-block', 'width':'24vw', 'height':'16vh', "border":"0.5px black solid"}),
            html.Div([
                html.H6("Number of Days", style={"text-align":'center'}), 
                html.H1(id='numDaysCard', style={"text-align":'center'})],  
                style={'display': 'inline-block', 'width':'24vw', 'height':'16vh', "border":"0.5px black solid"})
            
            #html.Div(dcc.Graph(id='totalReqCard', style={'width':'23vw', 'height':'16vh'}), style={'display': 'inline-block', 'width':'24vw', 'height':'16vh', "border":"0.5px black solid"}),
            #html.Div(dcc.Graph(id='numDaysCard', style={'width':'23vw', 'height':'16vh'}),  style={'display': 'inline-block', 'width':'24vw', 'height':'16vh', "border":"0.5px black solid"})
        ], style={'display':'flex' ,  "justify-content": "space-between", 'width':'48.5vw'}),
        html.Div(children=[ 
            html.Div([
                html.H6("Total Number of Requests", style={"text-align":'center'}), 
                html.H1(id='totalReqCard2', style={"text-align":'center'})],  
                style={'display': 'inline-block', 'width':'24vw', 'height':'16vh', "border":"0.5px black solid"}),
            html.Div([
                html.H6("Number of Days", style={"text-align":'center'}), 
                html.H1(id='numDaysCard2', style={"text-align":'center'})],  
                style={'display': 'inline-block', 'width':'24vw', 'height':'16vh', "border":"0.5px black solid"}) 
            # html.Div(dcc.Graph(id='totalReqCard2', style={'width':'23vw', 'height':'16vh'}), style={'display': 'inline-block', 'width':'24vw', 'height':'16vh', "border":"0.5px black solid"}),
            # html.Div(dcc.Graph(id='numDaysCard2', style={'width':'23vw', 'height':'16vh'}), style={'display': 'inline-block', 'width':'24vw', 'height':'16vh', "border":"0.5px black solid"})
        ], style={'display':'flex' ,  "justify-content": "space-between", 'width':'48.5vw'})
    ] , style={'display':'flex' ,  "justify-content": "space-between", "width": "97.5vw"}),

        
    html.Div(html.Br(), style={"height":"1vh"}),

    ## NC Comparison -  Request Source Bar Charts
    html.Div(children = [
        html.Div(dcc.Graph(id='reqSourceBarChart', style={"height":"30vh"}), style={'display': 'inline-block', 'width':'48.5vw', "border":"0.5px black solid",  "height":"30vh"}),
        html.Div(dcc.Graph(id='reqSourceBarChart2', style={"height":"30vh"}), style={'display': 'inline-block', 'width':'48.5vw', "border":"0.5px black solid", "margin-left": "10px",   "height":"30vh"})
    ] , style={'display':'flex' ,  "justify-content": "space-between", "width": "97.5vw"}),
    html.Div(html.Br(), style={"height":"1vh"}),
    
    ## NC Comparison - Number of Requests per day Overlapping line chart
    html.Div(dcc.Graph(id='overlayReqTimeLineChart', style={"height":"32vh", "width":"97.5vw"}), style={"border":"0.5px black solid", "height":"32vh", "width":"97.5vw"})
])

# @app.callback(
#     Output("modal", "is_open"),
#     [Input("open", "n_clicks"), Input("close", "n_clicks")],
#     [State("modal", "is_open")],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open





@app.callback(
    [dash.dependencies.Output('nc_dropdown_filter', 'options'),
     dash.dependencies.Output('nc_dropdown_filter', 'value')],
    dash.dependencies.Input('nc_dropdown', 'value')

)
def generate_dynamic_filter(nc_dropdown):
    if not nc_dropdown:
        df = data_2020
    else:
        df = data_2020[data_2020['ncname'] == nc_dropdown]
    
    rTypes = [n for n in set(df['requesttype'])]
    return rTypes, ' '



## Generate the charts and filters for NC Summary Dashboard
@app.callback(
    Output('reqTypePieChart', 'figure'),
    Output('timeCloseHist', 'figure'),
    Output('numReqLineChart', 'figure'),
    Output('dataQualityOutput', 'children'),
    Input('nc_dropdown', 'value'),
    [Input('nc_dropdown_filter', 'value')],
    Input('dataQualitySwitch', 'value')
)
def generate_nc_summary_charts(nc_dropdown, nc_dropdown_filter, dataQualitySwitch):
    # NC Dropdown
    if not nc_dropdown:
        df = data_2020
    else:
        df = data_2020[data_2020['ncname'] == nc_dropdown]
   
   # Remove Request Type Filter Dropdown
    if not nc_dropdown_filter:
        df = data_2020
    elif len(nc_dropdown_filter) > len(set(df['requesttype']))-1:
        raise PreventUpdate()
    elif nc_dropdown_filter is not None and nc_dropdown_filter != ' ' and len(nc_dropdown_filter) > 0:
        df = df[df['requesttype'].isin(nc_dropdown_filter) == False]
  
  # Pie Chart for the distribution of Request Types
    rtype = pd.DataFrame(df['requesttype'].value_counts())
    rtype = rtype.reset_index()
    reqTypePieChart = px.pie(rtype, values="requesttype", names="index", title="Share of each Request Type")
    reqTypePieChart.update_layout(margin=dict(l=50, r=50, b=50, t=50), legend_title = dict(font = dict(size = 10)), font=dict(size=9))





    # Distribution of Time to Close Date of each request
    ## Calculate the Time to Closed
    df.loc[:, 'createDateDT'] = pd.to_datetime(df.loc[:, 'createddate'].str[:-4].str.split("T").str.join(" "))
    df.loc[:, 'closeDateDT'] = pd.to_datetime(df.loc[:, 'closeddate'].str[:-4].str.split("T").str.join(" "))
    df.loc[:, 'timeToClose'] = (df.loc[:, 'closeDateDT'] - df.loc[:, 'createDateDT']).dt.days
    
    dataQualityOutput = None
    if dataQualitySwitch:
        df = df[(df['timeToClose'] > 1) & (df['timeToClose'] < 100)]
        dataQualityOutput = "Quality Filter: On"
    else:
        dataQualityOutput = "Quality Filter: Off"



    ## Calculate the Optimal number of bins based on Freedman-Diaconis Rule
    df.loc[:, "timeToClose"] = df.loc[:, "timeToClose"].fillna(0)
    q3, q1 = np.percentile(df.loc[:, "timeToClose"].astype(int), [75 ,25])
    iqr = q3 - q1
    if not iqr:
        numBins = 100
    else:
        numBins = int((2*iqr)/(df.shape[0]**(1/3)))

    timeCloseHist = px.histogram(df, x="timeToClose", title="Distribution of Time to Close Request", nbins= numBins, range_x=[min(df.loc[:, 'timeToClose']), max(df.loc[:, 'timeToClose'])], labels={"timeToClose":"Request Duration", "count":"Frequency"})
    timeCloseHist.update_layout(margin=dict(l=50, r=50, b=50, t=50), font=dict(size=9))

    ## Time Series for the Total Number of Requests
    # df.loc[:, 'createDateOnly'] = df.loc[:, 'createDateDT'].dt.date
    # rtime = pd.DataFrame(df.groupby('createDateOnly', as_index=False)['srnumber'].count())
    # fig3 = px.line(rtime, x="createDateOnly", y="srnumber", title="Trend for the Total Number of 311 Requests")
    rtime = pd.DataFrame(df.groupby('createDateDT', as_index=False)['srnumber'].count())
    numReqLineChart = px.line(rtime, x="createDateDT", y = 'srnumber', title="Total Number of 311 Requests Overtime", labels={"createDateDT":"DateTime", "srnumber":"Frequency"} )
    numReqLineChart.update_layout(margin=dict(l=25, r=25, b=25, t=50), font=dict(size=9))

    # apply_figure_style(reqTypePieChart)
    # apply_figure_style(timeCloseHist)
    # apply_figure_style(numReqLineChart)

    return reqTypePieChart, timeCloseHist, numReqLineChart, dataQualityOutput








## Generate the charts and filters for NC Comparison Dashboards
@app.callback(
    Output('reqSourceBarChart', 'figure'),
    Output('reqSourceBarChart2', 'figure'),
    Output('totalReqCard', 'children'),
    Output('totalReqCard2', 'children'),
    Output('numDaysCard', 'children'),
    Output('numDaysCard2', 'children'),
    Output('overlayReqTimeLineChart', 'figure'),
    Input('nc_comp_dropdown', 'value'),
    Input('nc_comp_dropdown2', 'value')
)
def generate_nc_comparison_charts(nc_comp_dropdown, nc_comp_dropdown2):
    if not nc_comp_dropdown:
        df_nc1 = data_2020
    else:
        df_nc1 = data_2020[data_2020['ncname'] == nc_comp_dropdown]

    if not nc_comp_dropdown2:
        df_nc2 = data_2020
    else:
        df_nc2 = data_2020[data_2020['ncname'] == nc_comp_dropdown2]
    
    
    df_nc1.loc[:, 'createDateDT'] = pd.to_datetime(df_nc1.loc[:, 'createddate'].str[:-4].str.split("T").str.join(" "))
    df_nc2.loc[:, 'createDateDT'] = pd.to_datetime(df_nc1.loc[:, 'createddate'].str[:-4].str.split("T").str.join(" "))



    # Bar chart of different Request Type Sources
    rSource = pd.DataFrame(df_nc1['requestsource'].value_counts())
    rSource = rSource.reset_index()
    reqSourceBarChart = px.bar(rSource, x="requestsource", y="index", orientation='h', title='Number of Requests by Source', labels={"index":"Request Source", "requestsource":"Frequency"})
    reqSourceBarChart.update_layout(margin=dict(l=25, r=25, b=25, t=50), font=dict(size=9))

    rSource2 = pd.DataFrame(df_nc2['requestsource'].value_counts())
    rSource2 = rSource2.reset_index()
    reqSourceBarChart2 = px.bar(rSource2, x="requestsource", y="index", orientation='h', title='Number of Requests by Source', labels={"index":"Request Source", "requestsource":"Frequency"})
    reqSourceBarChart2.update_layout(margin=dict(l=25, r=25, b=25, t=50) , font=dict(size=9))

    # Indicator Variables for Total Requests
    # totalReqCard = go.Figure()
    # totalReqCard.add_trace(go.Indicator(mode = "number+delta", value = df_nc1.shape[0], title = {'text': "Total Number of Requests"},domain = {'row': 0, 'column': 1}, number={"font":{"size":40}}))
    # totalReqCard.update_layout(margin=dict(l=25, r=25, b=35, t=70))
    totalReqCard = df_nc1.shape[0]

    # totalReqCard2 = go.Figure()
    # totalReqCard2.add_trace(go.Indicator( mode = "number+delta", value = df_nc2.shape[0], title = {'text': "Total Number of Requests"},domain = {'row': 0, 'column': 1},  number={"font":{"size":40}}))
    # totalReqCard2.update_layout(margin=dict(l=25, r=25, b=35, t=70))
    totalReqCard2 = df_nc2.shape[0]

    # Indicator Variables for Ignored Requests
    # ignoredReqCard = go.Figure()
    # ignoredReqCard.add_trace(go.Indicator(mode = "number+delta", value = df_nc1[df_nc1['timeToClose'] < 1].shape[0], title = {'text': "Ignored Requests"},domain = {'row': 0, 'column': 1}, number={"font":{"size":40}}))
    # ignoredReqCard.update_layout(margin=dict(l=25, r=25, b=35, t=70))

    # ignoredReqCard2 = go.Figure()
    # ignoredReqCard2.add_trace(go.Indicator( mode = "number+delta", value = df_nc2[df_nc2['timeToClose'] < 1].shape[0], title = {'text': "Ignored Requests"},domain = {'row': 0, 'column': 1}, number={"font":{"size":40}}))
    # ignoredReqCard2.update_layout(margin=dict(l=25, r=25, b=35, t=70))

    # Indicator Visuals for the Number of Days the dataset spans
    # numDaysCard = go.Figure()
    # numDaysCard.add_trace(go.Indicator(mode = "number+delta", value = np.max(df_nc1['createDateDT'].dt.day) - np.min(df_nc1['createDateDT'].dt.day) + 1, title = {'text': "Number of Days"},domain = {'row': 0, 'column': 1}, number={"font":{"size":40}}))
    # numDaysCard.update_layout(margin=dict(l=25, r=25, b=35, t=70))
    numDaysCard = np.max(df_nc1['createDateDT'].dt.day) - np.min(df_nc1['createDateDT'].dt.day) + 1

    # numDaysCard2 = go.Figure()
    # numDaysCard2.add_trace(go.Indicator( mode = "number+delta", value = np.max(df_nc2['createDateDT'].dt.day) - np.min(df_nc2['createDateDT'].dt.day) + 1, title = {'text': "Number of Days"},domain = {'row': 0, 'column': 1}, number={"font":{"size":40}}))
    # numDaysCard2.update_layout(margin=dict(l=25, r=25, b=35, t=70)) 
    numDaysCard2 = np.max(df_nc2['createDateDT'].dt.day) - np.min(df_nc2['createDateDT'].dt.day) + 1


    rTime = pd.DataFrame(df_nc1.groupby('createDateDT', as_index=False)['srnumber'].count())
    rTime2 = pd.DataFrame(df_nc2.groupby('createDateDT', as_index=False)['srnumber'].count())
    # overlayReqTimeLineChart = px.line(rtime, x="createDateDT", y = 'srnumber', title="Total Number of 311 Requests Overtime", labels={"createDateDT":"DateTime", "srnumber":"Frequency"} )
    # overlayReqTimeLineChart.update_layout(margin=dict(l=25, r=25, b=25, t=50), font=dict(size=9))
    #fig.add_scatter(x=df['Date'], y=df['AAPL.Low'], mode='lines') - usesomething like this to add lines
    overlayReqTimeLineChart = go.Figure()
    overlayReqTimeLineChart.add_trace(go.Scatter(x=rTime['createDateDT'], y=rTime['srnumber'], mode='lines', name='NC1'))
    overlayReqTimeLineChart.add_trace(go.Scatter(x=rTime2['createDateDT'], y=rTime2['srnumber'], mode='lines', name='NC2'))
    overlayReqTimeLineChart.update_layout(title='Number of Request Throughout the Day', margin=dict(l=25, r=25, b=35, t=50), xaxis_range=[min(min(rTime['createDateDT']), min(rTime2['createDateDT'])), max(max(rTime['createDateDT']), max(rTime2['createDateDT']))], font=dict(size=9))


    return reqSourceBarChart, reqSourceBarChart2, totalReqCard, totalReqCard2, numDaysCard, numDaysCard2, overlayReqTimeLineChart





app.run_server(debug=True)


