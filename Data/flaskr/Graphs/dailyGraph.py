import numpy as np
import pandas as pan
import datetime as dt
import io
import requests
import plotly.io._json as json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

    
url = "https://www.cryptodatadownload.com/cdd/Bittrex_BTCUSD_d.csv"

   
def drawGraph(url, colour, crypto):

    r = requests.get(url, verify=False)
    read = pan.read_csv(io.StringIO(r.text), skiprows=[0],
                        na_values=['no info', '.'], delimiter=',')

    
    for col in read.columns:
        if col != 'Date' or 'Symbol':
            for count, i in enumerate(read[col]):
                if i == 0 and count!=0:
                    read[col][count] = read[col][count-1]
                elif i == 0 and count==0:
                    read[col][count] = np.mean(read[col][count:count+10])
    
    #print(read.head())

    fig = make_subplots(specs=[[{'secondary_y':True}]])
    
    fig.add_trace(go.Scatter(x=read['Date'], y=read['Close'], name = 'Closing Price (USD)', line_color=colour),
    secondary_y=True,)
    fig.add_trace(go.Scatter(x=read['Date'], y=read['Volume USD'], name = 'Volume (USD)', line_color='lightgreen', opacity=0.6),
    secondary_y=False,)

    fig.update_layout(
        title={'text':f'{crypto} Time Series',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    ), height=700
        )
    
    
    fig.update_xaxes(rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ]),
    ),title_text='Date'
    )
    fig.update_yaxes(title_text='Closing Price (USD)',
    color=colour,
    secondary_y=True,)

    fig.update_yaxes(title_text='Volume (USD)',
    color='lightgreen',
    secondary_y=False,)
    
    return fig


