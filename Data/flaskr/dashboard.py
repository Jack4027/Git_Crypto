import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go 
from .Statistics.urls import *
from .Graphs.dailyGraph import drawGraph as daily
from .Graphs.hourlyGraph import drawGraph as hourly
from .Graphs.model import modelPrediction as prediction
import dash_bootstrap_components as dbc
import requests 
import datetime as dt
import io 
import pandas as pd
import dash_table
import numpy as np

"""
dcc.Location(id='url'),
children= dcc.Graph(
    id = 'Bitcoin Graph',
    figure=bitcoin
)
)
"""

bitcoin = daily(Bitcoindaily,'gold','Bitcoin')
bh = hourly(Bitcoinhourly,'gold','Bitcoin')
bp,bitcoinPredictionTable = prediction(Bitcoindaily,'gold','Bitcoin')

ethereum = daily(Ethereumdaily,'purple','Ethereum')
eh = hourly(Ethereumhourly, 'purple', 'Ethereum')
ep,ethereumPredictionTable = prediction(Ethereumdaily,'purple','Ethereum')

EC = daily(EthereumClassicdaily,'grey','Ethereum Classic')
ech = hourly(EthereumClassichourly,'grey', 'Ethereum Classic')
ecp,ECPredictionTable = prediction(EthereumClassicdaily,'grey','Ethereum Classic')

litecoin = daily(Litecoindaily,'yellow','Litecoin')
lth = hourly(Litecoinhourly,'yellow','Litecoin')
ltp,litecoinPredictionTable = prediction(Litecoindaily,'yellow','Litecoin')

XRP = daily(XRPdaily,'black','XRP')
xrph = hourly(XRPhourly, 'black', 'XRP')
xrpp,XRPPredictionTable = prediction(XRPdaily,'black','XRP')

def datatodataframe(url):
    r = requests.get(url, verify=False)


    data = pd.read_csv(io.StringIO(r.text), skiprows=[0],usecols=['Date','Symbol','Open','High','Low','Close','Volume USD'],
                        na_values=['no info', '.'], delimiter=',')
      
    for col in data.columns:
        if col != 'Date' or 'Symbol':
            for count, i in enumerate(data[col]):
                if i == 0 and count !=0:
                    data[col][count] = data[col][count-1]
                elif i == 0 and count ==0:
                    data[col][count] = np.mean(data[col][count: count+100])
    
    if '_1h' in url:
        data['Date'] = [dt.datetime.strftime(dt.datetime.strptime(d, '%Y-%m-%d %I-%p'),'%d-%m-%Y %X') for d in data['Date']]
    else:
        data['Date'] = [dt.datetime.strftime(dt.datetime.strptime(d, '%Y-%m-%d').date(),'%d-%m-%Y') for d in data['Date']]
    data = data.round(decimals = 4)

    
    columns = ['Open', 'Close', 'Low', 'High', 'Volume USD']

       
    for i in columns:
        data[i] = data.apply(lambda x: "{} USD".format(x[i]),axis = 1)
        
    return data

def predictiontodataframe(read):

    """
    for col in read.columns:
        if col != 'Date' or 'Symbol':
            for count, i in enumerate(read[col]):
                if i == 0:
                    read[col][count] = read[col][count-1]
    """

    read = read.round(decimals = 4)
    for i in ['Real Close', 'Model Prediction']:
        read[i] = read.apply(lambda x: "{} USD".format(x[i]),axis = 1)
        
    return read

"""
def predictiontotable(read):
    
    table = go.Figure(data=[go.Table(
    header=dict(
        values=["<b>Date</b>", "Real Close", "Model Prediction"],
        line_color='white', fill_color='white',
        align='center', font=dict(color='black', size=12)
    ),
    cells=dict(
        values=[read.Date, read['Real Close'],read['Model Prediction']],
        align='center', font=dict(color='black', size=11)
    ))
    ])

    return table
"""
def create_table(file):
    table = dash_table.DataTable(
        id = 'Data-History',
        columns=[{"name": i, "id": i} for i in file.columns],
        data= file.to_dict('records'),
        sort_action="native",
        sort_mode='native',
        style_header={ 'backgroundColor': 'skyblue' },
        style_cell={ 'backgroundColor': 'lightblue' },
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'white'
        }
    ],

        page_size=50
    )

    return table

def create(server):

    app = dash.Dash(
        __name__,
        server = server,
        routes_pathname_prefix='/dashanalytics/',
        external_stylesheets=[
            'templates/Bitcoin/bit.css', dbc.themes.BOOTSTRAP]
    )

    app.layout = html.Div([
        dcc.Location(id='url'),
        dbc.Nav( 
        [   
            dbc.NavItem(dbc.NavLink('Bitcoin Statistics',style = {'color':'limegreen'}, href='http://127.0.0.1:5000/'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
            dbc.NavItem(dbc.NavLink('Ethereum Statistics',style = {'color':'limegreen'},  href='http://127.0.0.1:5000/Ethereum'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
            dbc.NavItem(dbc.NavLink('Ethereum Classic Statistics',style = {'color':'limegreen'}, href='http://127.0.0.1:5000/Ethereum_Classic'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
            dbc.NavItem(dbc.NavLink('Litecoin Statistics',style = {'color':'limegreen'}, href='http://127.0.0.1:5000/Litecoin'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
            dbc.NavItem(dbc.NavLink('XRP Statistics',style = {'color':'limegreen'}, href='http://127.0.0.1:5000/XRP'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
     ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'},
        
    ),
    html.Div(id='page-content'),
    ] 
    )
    

    
    bit_daily=html.Div([

        dcc.Graph(
            id='Bitcoin Daily Time Series',
            figure=bitcoin
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
      
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum Classic',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Litecoin',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('XRP',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),


    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(datatodataframe(Bitcoindaily)),
        dcc.Link(dbc.Button("Download CSV", color="primary", className="ml-4 mt-3"), href=Bitcoindaily, target='_blank')
    ])
    eth_daily=html.Div([
        dcc.Graph(
        id='Ethereum Daily Time Series',
        figure=ethereum
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Bitcoin',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum Classic',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Litecoin',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('XRP',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),



    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(datatodataframe(Ethereumdaily)),
        dcc.Link(dbc.Button("Download CSV", color="primary", className="ml-4 mt-3"), href=Ethereumdaily, target='_blank')
    ])
    EC_daily=html.Div([
        dcc.Graph(
        id='Ethereum Classic Daily Time Series',
        figure=EC
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/EC_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/EC_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Bitcoin',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Litecoin',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('XRP',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),


    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(datatodataframe(EthereumClassicdaily)),
        dcc.Link(dbc.Button("Download CSV", color="primary", className="ml-4 mt-3"), href=EthereumClassicdaily, target='_blank')
    ])
    lite_daily=html.Div([
        dcc.Graph(
            id='Litecoin Daily Time Series',
            figure=litecoin
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
       
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Bitcoin',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum Classic',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('XRP',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),


    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(datatodataframe(Litecoindaily)),
        dcc.Link(dbc.Button("Download CSV", color="primary", className="ml-4 mt-3"), href=Litecoindaily, target='_blank')
    ])
    XRP_daily=html.Div([
        dcc.Graph(
            id='XRP Daily Time Series',
            figure=XRP
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/XRP_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/XRP_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Bitcoin',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum Classic',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Litecoin',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),


    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(datatodataframe(XRPdaily)),
        dcc.Link(dbc.Button("Download CSV", color="primary", className="ml-4 mt-3"), href=XRPdaily, target='_blank')

    ])
    bit_hourly=html.Div([

        dcc.Graph(
            id='Bitcoin Hourly Time Series',
            figure=bh
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
      
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum Classic',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Litecoin',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('XRP',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),


    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(datatodataframe(Bitcoinhourly)),
        dcc.Link(dbc.Button("Download CSV", color="primary", className="ml-4 mt-3"), href=Bitcoinhourly, target='_blank')
    ])
    eth_hourly=html.Div([
        dcc.Graph(
        id='Ethereum Hourly Time Series',
        figure=eh
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Bitcoin',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum Classic',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Litecoin',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('XRP',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),



    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(datatodataframe(Ethereumhourly)),
        dcc.Link(dbc.Button("Download CSV", color="primary", className="ml-4 mt-3"), href=Ethereumhourly, target='_blank')
    ])
    EC_hourly=html.Div([
        dcc.Graph(
        id='Ethereum Classic Hourly Time Series',
        figure=ech
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/EC_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/EC_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Bitcoin',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Litecoin',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('XRP',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),


    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(datatodataframe(EthereumClassichourly)),
        dcc.Link(dbc.Button("Download CSV", color="primary", className="ml-4 mt-3"), href=EthereumClassichourly, target='_blank')
    ])
    lite_hourly=html.Div([
        dcc.Graph(
            id='Litecoin Hourly Time Series',
            figure= lth
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
       
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Bitcoin',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum Classic',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('XRP',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),


    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(datatodataframe(Litecoinhourly)),
        dcc.Link(dbc.Button("Download CSV", color="primary", className="ml-4 mt-3"), href=Litecoinhourly, target='_blank')
    ])

    XRP_hourly=html.Div([
        dcc.Graph(
            id='XRP Hourly Time Series',
            figure= xrph
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/XRP_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/XRP_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Bitcoin',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum Classic',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Litecoin',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),


    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(datatodataframe(XRPhourly)),
        dcc.Link(dbc.Button("Download CSV", color="primary", className="ml-4 mt-3"), href=XRPhourly, target='_blank')
    ])

    bit_prediction=html.Div([

        dcc.Graph(
            id='Bitcoin Model Prediction',
            figure=bp
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
      
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum Classic',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Litecoin',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('XRP',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),


    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(predictiontodataframe(bitcoinPredictionTable)),
        

    ])
    eth_prediction=html.Div([
        dcc.Graph(
        id='Ethereum Model Prediction',
        figure=ep
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Bitcoin',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum Classic',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Litecoin',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('XRP',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),



    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(predictiontodataframe(ethereumPredictionTable)),
        

    ])
    EC_prediction=html.Div([
        dcc.Graph(
        id='Ethereum Classic Hourly Time Series',
        figure=ecp
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/EC_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/EC_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Bitcoin',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Litecoin',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('XRP',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),


    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(predictiontodataframe(ECPredictionTable)),

    ])
    lite_prediction=html.Div([
        dcc.Graph(
            id='Litecoin Model Prediction',
            figure= ltp
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
       
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Bitcoin',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum Classic',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('XRP',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),


    ],
        pills=True,
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(predictiontodataframe(litecoinPredictionTable)),

    ])

    XRP_Prediction=html.Div([
        dcc.Graph(
            id='XRP Model Prediction',
            figure= xrpp
        ),
                dbc.Nav( 
        [   
        dbc.NavItem(dbc.NavLink('Daily',style = {'color':'limegreen'}, href='/dashanalytics/XRP_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Hourly',style = {'color':'limegreen'}, href='/dashanalytics/XRP_h'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Prediction',style = {'color':'limegreen'}, href='/dashanalytics/XRP_p'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Bitcoin',style = {'color':'limegreen'}, href='/dashanalytics/Bitcoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum',style = {'color':'limegreen'}, href='/dashanalytics/Ethereum_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Ethereum Classic',style = {'color':'limegreen'}, href='/dashanalytics/EC_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),
        
        dbc.NavItem(dbc.NavLink('Litecoin',style = {'color':'limegreen'}, href='/dashanalytics/Litecoin_g'), style={'background-color':'lightgreen','border-radius':'3em', 'margin-left': '3em'}),


    ],
        pills=True, 
        style = {'padding-top':'20px', 'padding-left':'20px','padding-bottom':'20px', 'background-color':'lightblue'}),
        create_table(predictiontodataframe(XRPPredictionTable)),
        
    ])
    
    @ app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/dashanalytics/Bitcoin_g':
            return bit_daily
        elif pathname == '/dashanalytics/Ethereum_g':
            return eth_daily
        elif pathname == '/dashanalytics/EC_g':
            return EC_daily
        elif pathname == '/dashanalytics/Litecoin_g':
            return lite_daily
        elif pathname == '/dashanalytics/XRP_g':
            return XRP_daily
        elif pathname == '/dashanalytics/Bitcoin_h':
            return bit_hourly
        elif pathname == '/dashanalytics/Ethereum_h':
            return eth_hourly
        elif pathname == '/dashanalytics/EC_h':
            return EC_hourly
        elif pathname == '/dashanalytics/Litecoin_h':
            return lite_hourly
        elif pathname == '/dashanalytics/XRP_h':
            return XRP_hourly
        elif pathname == '/dashanalytics/Bitcoin_p':
            return bit_prediction
        elif pathname == '/dashanalytics/Ethereum_p':
            return eth_prediction
        elif pathname == '/dashanalytics/EC_p':
            return EC_prediction
        elif pathname == '/dashanalytics/Litecoin_p':
            return lite_prediction
        elif pathname == '/dashanalytics/XRP_p':
            return XRP_Prediction
            
    if __name__ == '__main__':
        app.run_server(debug=True)

    return app.server
