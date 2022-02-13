import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd
from pylab import rcParams
from matplotlib import rc
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import requests
import io

url = 'https://www.cryptodatadownload.com/cdd/Bittrex_BTCUSD_d.csv'  
def modelPrediction(dailydata, colour, crypto):
 
    model = tf.keras.models.load_model('models/MinMaxModel')
    RANDOM_SEED = 42
    np.random.seed(RANDOM_SEED)

    url = dailydata
    r = requests.get(url, verify=False)
    read = pd.read_csv(io.StringIO(r.text), skiprows=[0],
                            na_values=['no info', '.'], delimiter=',')

    read = read.iloc[::-1]
    read = read.sort_values('Date')
    for col in read.columns:
        if col != 'Date' or 'Symbol':
            for count, i in enumerate(read[col]):
                if i == 0:
                    read[col][count] = read[col][count-1]
    #print(read.head())

    def to_sequences(data, seq_len):
        d = []

        for index in range(len(data) - seq_len):
            d.append(data[index: index + seq_len])

        return np.array(d)

    def preprocess(data_raw, seq_len, train_split):

        data = to_sequences(data_raw, seq_len)

        num_train = int(train_split * data.shape[0])

        X_train = data[:num_train, :-1, :]
        y_train = data[:num_train, -1, :]

        X_test = data[num_train:, :-1, :]
        y_test = data[num_train:, -1, :]

        return X_train, y_train, X_test, y_test
    
    scaler = MinMaxScaler()
    close_price = read.Close.values.reshape(-1,1)
    scaled_close = scaler.fit_transform(close_price)
    #print(scaled_close.shape)
    #print(np.isnan(scaled_close).any())
    scaled_close = scaled_close[~np.isnan(scaled_close)]
    scaled_close = scaled_close.reshape(-1, 1)
    #print(np.isnan(scaled_close).any())
    SEQ_LEN = 100
    X_train, y_train, X_test, y_test = preprocess(scaled_close, SEQ_LEN, train_split = 0.95)
    #print(X_train.shape)
    #print(X_test.shape)


    BATCH_SIZE = 64

    model.evaluate(X_test, y_test)

    y_hat = model.predict(X_test)

    y_test_inverse = scaler.inverse_transform(y_test)
    y_hat_inverse = scaler.inverse_transform(y_hat)
    #read['Original'] = y_test_inverse
    #read['Prediction'] = y_hat_inverse
    #print(y_hat_inverse)
    y_hat_inverse = y_hat_inverse.flatten()
    dr = len(y_hat_inverse)
    #print(y_hat_inverse.shape)

    fig = make_subplots()
        
    fig.add_trace(go.Scatter(x=read['Date'][-dr:], y=read['Close'][-dr: ], name = 'Real Close (USD)', line_color=colour),
    )
    fig.add_trace(go.Scatter(x=read['Date'][-dr: ], y=y_hat_inverse, name = 'Model Prediction (USD)', line_color='red'),
    )
    predData = {'Date': read['Date'][-dr: ],'Symbol': read['Symbol'][-dr: ],'Real Close': read['Close'][-dr:],'Model Prediction': y_hat_inverse }
    predictionTable = pd.DataFrame(predData)
    predictionTable = predictionTable.iloc[::-1]
    #print(predictionTable.head())
    fig.update_layout(
        title={'text':f'{crypto} Price Prediction',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
        font=dict(
        family="Courier New, monospace",
        size=18,
        color= colour
    ), height=700
        )


    fig.update_xaxes(rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                
                dict(step="all")
            ]),
        ),title_text='Date', tickmode = 'auto',nticks =20, color = colour
    )
    fig.update_yaxes(title_text='Closing Price (USD)',
    color= colour
    )


    return fig, predictionTable

