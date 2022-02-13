import datetime as dt
from itertools import islice
import numpy as np
import io
import pandas as pan
import requests
    
def stats(url):

    r = requests.get(url, verify=False)
    data = pan.read_csv(io.StringIO(r.text), skiprows=[0], usecols=['Date','Symbol','Open','High','Low','Close','Volume USD'],
    na_values=['no info', '.'], delimiter=',')

    
    for col in data.columns:
        if col != 'Date' or 'Symbol':
            for count, i in enumerate(data[col]):
                if i == 0 and count !=0:
                    data[col][count] = data[col][count-1]
                elif i == 0 and count ==0:
                    data[col][count] = np.mean(data[col][count: count+100])
    
                    
    data['Date'] = [dt.datetime.strftime(dt.datetime.strptime(d, '%Y-%m-%d').date(),'%d-%m-%Y') for d in data['Date']]
    
    todays = [data['Close'][0], data['Date'][0]]
    Vol24H = [data['Volume USD'][0], data['Date'][0]]
    highestClose7 = [0, None]
    highestOpen7 = [0,None]
    highestLow7 = [0, None]
    lowestLow7 = [float('inf'), None]
    lowestOpen7 = [float('inf'),None]
    lowestClose7 = [float('inf'),None]
    lowestHigh7 = [float('inf'),None]
    lowestVol7 = [float('inf'),None]
    highestHigh7 = [0,None]
    highestVol7 = [0,None]
    highestClose14 = [0, None]
    highestOpen14 = [0,None]
    highestLow14 = [0, None]
    lowestLow14 = [float('inf'), None]
    lowestOpen14 = [float('inf'),None]
    lowestClose14 = [float('inf'),None]
    lowestHigh14 = [float('inf'),None]
    lowestVol14 = [float('inf'),None]
    highestHigh14 = [0,None]
    highestVol14 = [0,None]
    highestClose30 = [0, None]
    highestOpen30 = [0,None]
    highestLow30 = [0, None]
    lowestLow30 = [float('inf'), None]
    lowestOpen30 = [float('inf'),None]
    lowestClose30 = [float('inf'),None]
    lowestHigh30 = [float('inf'),None]
    lowestVol30 = [float('inf'),None]
    highestHigh30 = [0,None]
    highestVol30 = [0,None]
    highestClose90 = [0,None]
    highestHigh90 = [0,None]
    highestVol90 = [0,None]
    highestOpen90 = [0,None]
    highestLow90 = [0,None]
    lowestLow90 = [float('inf'),None]
    lowestOpen90 = [float('inf'),None]
    lowestClose90 = [float('inf'),None]
    lowestHigh90 = [float('inf'),None]
    lowestVol90 = [float('inf'),None]
    highestClose180 = [0,None]
    highestOpen180 = [0,None]
    highestLow180 = [0,None]
    lowestLow180 = [float('inf'),None]
    lowestOpen180 = [float('inf'),None]
    lowestClose180 = [float('inf'),None]
    lowestHigh180 = [float('inf'),None]
    lowestVol180 = [float('inf'),None]
    highestHigh180 = [0,None]
    highestVol180 = [0,None]
    highestOpen365 = [0,None]
    highestClose365 = [0,None]
    highestLow365 = [0,None]
    lowestLow365 = [float('inf'),None]
    lowestOpen365 = [float('inf'),None]
    lowestClose365 = [float('inf'),None]
    lowestHigh365 = [float('inf'),None]
    lowestVol365 = [float('inf'),None]
    highestHigh365 = [0,None]
    highestVol365 = [0,None]

    for row in islice(data.itertuples(), 7):
                
        if row[3]> highestOpen7[0]:
            highestOpen7[0] = row[3]
            highestOpen7[1] = row[1]
        if row[6] > highestClose7[0]:
            highestClose7[0] = row[6]
            highestClose7[1] = row[1]
        if row[3]< lowestOpen7[0]:
            lowestOpen7[0] = row[3]
            lowestOpen7[1] = row[1]
        if row[6] < lowestClose7[0]:
            lowestClose7[0] = row[6]
            lowestClose7[1] = row[1]
        if row[4]< lowestHigh7[0]:
            lowestHigh7[0] = row[4]
            lowestHigh7[1] = row[1]
        if row[7] < lowestVol7[0]:
            lowestVol7[0] = row[7]
            lowestVol7[1] = row[1]
        if row[5] < lowestLow7[0]:
            lowestLow7[0] = row[5]
            lowestLow7[1] = row[1]
        if row[5] > highestLow7[0]:
            highestLow7[0] = row[5]
            highestLow7[1] = row[1]
        if row[4] > highestHigh7[0]:
            highestHigh7[0] = row[4]
            highestHigh7[1] = row[1]
        if row[7] > highestVol7[0]:
            highestVol7[0] = row[7]
            highestVol7[1] = row[1]

    for row in islice(data.itertuples(), 14):
            
        if row[3]> highestOpen14[0]:
            highestOpen14[0] = row[3]
            highestOpen14[1] = row[1]
        if row[6] > highestClose14[0]:
            highestClose14[0] = row[6]
            highestClose14[1] = row[1]
        if row[3]< lowestOpen14[0]:
            lowestOpen14[0] = row[3]
            lowestOpen14[1] = row[1]
        if row[6] < lowestClose14[0]:
            lowestClose14[0] = row[6]
            lowestClose14[1] = row[1]
        if row[4]< lowestHigh14[0]:
            lowestHigh14[0] = row[4]
            lowestHigh14[1] = row[1]
        if row[7] < lowestVol14[0]:
            lowestVol14[0] = row[7]
            lowestVol14[1] = row[1]
        if row[5] < lowestLow14[0]:
            lowestLow14[0] = row[5]
            lowestLow14[1] = row[1]
        if row[5] > highestLow14[0]:
            highestLow14[0] = row[5]
            highestLow14[1] = row[1]
        if row[4] > highestHigh14[0]:
            highestHigh14[0] = row[4]
            highestHigh14[1] = row[1]
        if row[7] > highestVol14[0]:
            highestVol14[0] = row[7]
            highestVol14[1] = row[1]
 
   
    for row in islice(data.itertuples(), 30):
            
        if row[3]> highestOpen30[0]:
            highestOpen30[0] = row[3]
            highestOpen30[1] = row[1]
        if row[6] > highestClose30[0]:
            highestClose30[0] = row[6]
            highestClose30[1] = row[1]
        if row[3]< lowestOpen30[0]:
            lowestOpen30[0] = row[3]
            lowestOpen30[1] = row[1]
        if row[6] < lowestClose30[0]:
            lowestClose30[0] = row[6]
            lowestClose30[1] = row[1]
        if row[4]< lowestHigh30[0]:
            lowestHigh30[0] = row[4]
            lowestHigh30[1] = row[1]
        if row[7] < lowestVol30[0]:
            lowestVol30[0] = row[7]
            lowestVol30[1] = row[1]
        if row[5] < lowestLow30[0]:
            lowestLow30[0] = row[5]
            lowestLow30[1] = row[1]
        if row[5] > highestLow30[0]:
            highestLow30[0] = row[5]
            highestLow30[1] = row[1]
        if row[4] > highestHigh30[0]:
            highestHigh30[0] = row[4]
            highestHigh30[1] = row[1]
        if row[7] > highestVol30[0]:
            highestVol30[0] = row[7]
            highestVol30[1] = row[1]

    for row in islice(data.itertuples(), 90):
        if row[3]> highestOpen90[0]:
            highestOpen90[0] = row[3]
            highestOpen90[1] = row[1]
        if row[6] > highestClose90[0]:
            highestClose90[0] = row[6]
            highestClose90[1] = row[1]
        if row[3]< lowestOpen90[0]:
            lowestOpen90[0] = row[3]
            lowestOpen90[1] = row[1]
        if row[6] < lowestClose90[0]:
            lowestClose90[0] = row[6]
            lowestClose90[1] = row[1]
        if row[4]< lowestHigh90[0]:
            lowestHigh90[0] = row[4]
            lowestHigh90[1] = row[1]
        if row[7] < lowestVol90[0]:
            lowestVol90[0] = row[7]
            lowestVol90[1] = row[1]
        if row[5] < lowestLow90[0]:
            lowestLow90[0] = row[5]
            lowestLow90[1] = row[1]
        if row[5] > highestLow90[0]:
            highestLow90[0] = row[5]
            highestLow90[1] = row[1]
        if row[4] > highestHigh90[0]:
            highestHigh90[0] = row[4]
            highestHigh90[1] = row[1]
        if row[7] > highestVol90[0]:
            highestVol90[0] = row[7]
            highestVol90[1] = row[1]

    for row in islice(data.itertuples(), 180):
        if row[3] > highestOpen180[0]:
            highestOpen180[0] = row[3]
            highestOpen180[1] = row[1]
        if row[6] > highestClose180[0]:
            highestClose180[0] = row[6]
            highestClose180[1] = row[1]
        if row[3]< lowestOpen180[0]:
            lowestOpen180[0] = row[3]
            lowestOpen180[1] = row[1]
        if row[6] < lowestClose180[0]:
            lowestClose180[0] = row[6]
            lowestClose180[1] = row[1]
        if row[4]< lowestHigh180[0]:
            lowestHigh180[0] = row[4]
            lowestHigh180[1] = row[1]
        if row[7] < lowestVol180[0]:
            lowestVol180[0] = row[7]
            lowestVol180[1] = row[1]
        if row[5] < lowestLow180[0]:
            lowestLow180[0] = row[5]
            lowestLow180[1] = row[1]
        if row[5] > highestLow180[0]:
            highestLow180[0] = row[5]
            highestLow180[1] = row[1]
        if row[4] > highestHigh180[0]:
            highestHigh180[0] = row[4]
            highestHigh180[1] = row[1]
        if row[7] > highestVol180[0]:
            highestVol180[0] = row[7]
            highestVol180[1] = row[1]

    for row in islice(data.itertuples(), 365):
        if row[3] > highestOpen365[0]:
            highestOpen365[0] = row[3]
            highestOpen365[1] = row[1]
        if row[6] > highestClose365[0]:
            highestClose365[0] = row[6]
            highestClose365[1] = row[1]
        if row[3]< lowestOpen365[0]:
            lowestOpen365[0] = row[3]
            lowestOpen365[1] = row[1]
        if row[6] < lowestClose365[0]:
            lowestClose365[0] = row[6]
            lowestClose365[1] = row[1]
        if row[4]< lowestHigh365[0]:
            lowestHigh365[0] = row[4]
            lowestHigh365[1] = row[1]
        if row[7] < lowestVol365[0]:
            lowestVol365[0] = row[7]
            lowestVol365[1] = row[1]
        if row[5] < lowestLow365[0]:
            lowestLow365[0] = row[5]
            lowestLow365[1] = row[1]
        if row[5] > highestLow365[0]:
            highestLow365[0] = row[5]
            highestLow365[1] = row[1]
        if row[4] > highestHigh365[0]:
            highestHigh365[0] = row[4]
            highestHigh365[1] = row[1]
        if row[7] > highestVol365[0]:
            highestVol365[0] = row[7]
            highestVol365[1] = row[1]

    statistics = {'Latest Price':todays,'Volume 24 Hour':Vol24H,'Highest Daily Volume 7 Days': highestVol7,'Lowest Daily Volume 7 Days': lowestVol7,'Highest Opening Price 7 Days':highestOpen7,
    'Lowest Opening Price 7 Days': lowestOpen7,'Highest Closing Price 7 Days':highestClose7,'Lowest Closing Price 7 Days': lowestClose7,
    'Highest Daily Price 7 Days':highestHigh7,'Lowest Daily High 7 Days': lowestHigh7, 'Lowest Daily Price 7 Days':lowestLow7,'Highest Daily Low 7 Days': highestLow7,'Highest Daily Volume 14 Days': highestVol14,
    'Lowest Daily Volume 14 Days': lowestVol14,'Highest Daily Opening Price 14 Days':highestOpen14,'Lowest Daily Opening Price 14 Days': lowestOpen14,
    'Highest Daily Closing Price 14 Days':highestClose14,'Lowest Daily Closing Price 14 Days': lowestClose14,'Highest Daily Price 14 Days':highestHigh14,'Lowest Daily High 14 Days': lowestHigh14, 
    'Lowest Daily Price 14 Days':lowestLow14,'Highest Daily Low 14 Days': highestLow14,'Highest Daily Volume 30 Days': highestVol30,'Lowest Daily Volume 30 Days': lowestVol30,
     'Highest Opening Price 30 Days':highestOpen30,'Lowest Opening Price 30 Days': lowestOpen30,'Highest Closing Price 30 Days':highestClose30,'Lowest Closing Price 30 Days': lowestClose30,
      'Highest Daily Price 30 Days':highestHigh30,'Lowest Daily High 30 Days': lowestHigh30,'Lowest Daily Price 30 Days':lowestLow30,'Highest Daily Low 30 Days': highestLow30,
      'Highest Daily Volume 90 Days': highestVol90,'Lowest Daily Volume 90 Days': lowestVol90,'Highest Opening Price 90 Days':highestOpen90,
    'Lowest Opening Price 90 Days': lowestOpen90,'Highest Closing Price 90 Days':highestClose90,'Lowest Closing Price 90 Days': lowestClose90, 'Highest Daily Price 90 Days':highestHigh90,
    'Lowest Daily High 90 Days': lowestHigh90, 'Lowest Daily Price 90 Days':lowestLow90,'Highest Daily Low 90 Days': highestLow90,
    'Highest Daily Volume 180 Days': highestVol180,'Lowest Daily Volume 180 Days': lowestVol180,'Highest Opening Price 180 Days':highestOpen180,'Lowest Opening Price 180 Days': lowestOpen180,
    'Highest Closing Price 180 Days':highestClose180,'Lowest Closing Price 180 Days': lowestClose180,'Highest Daily Price 180 Days':highestHigh180,'Lowest Daily High 180 Days': lowestHigh180,
    'Lowest Daily Price 180 Days':lowestLow180,'Highest Daily Low 180 Days': highestLow180,'Highest Daily Volume Annual': highestVol365,'Lowest Daily Volume Annual': lowestVol365,
    'Highest Opening Price Annual':highestOpen365,'Lowest Opening Price Annual': lowestOpen365,'Highest Closing Price Annual':highestClose365,'Lowest Closing Price Annual': lowestClose365,
    'Highest Daily Price Annual':highestHigh365,'Lowest Daily High Annual': lowestHigh365,'Lowest Daily Price Annual':lowestLow365,'Highest Daily Low Annual': highestLow365}
    
    latest = {'Latest Price':todays,'Volume 24 Hour':Vol24H}

    opening = {'Highest Opening Price 7 Days':highestOpen7,'Lowest Opening Price 7 Days': lowestOpen7,'Highest Daily Opening Price 14 Days':highestOpen14,
    'Lowest Daily Opening Price 14 Days': lowestOpen14,'Highest Opening Price 30 Days':highestOpen30,
    'Lowest Opening Price 30 Days': lowestOpen30, 'Highest Opening Price 90 Days':highestOpen90,'Lowest Opening Price 90 Days': lowestOpen90, 
    'Highest Opening Price 180 Days':highestOpen180,'Lowest Opening Price 180 Days': lowestOpen180, 'Highest Opening Price Annual':highestOpen365,
    'Lowest Opening Price Annual': lowestOpen365}

    closing = {'Highest Closing Price 7 Days':highestClose7,'Lowest Closing Price 7 Days': lowestClose7,'Highest Daily Closing Price 14 Days':highestClose14,
    'Lowest Daily Closing Price 14 Days': lowestClose14,'Highest Closing Price 30 Days':highestClose30,
    'Lowest Closing Price 30 Days': lowestClose30, 'Highest Closing Price 90 Days':highestClose90,'Lowest Closing Price 90 Days': lowestClose90,
     'Highest Closing Price 180 Days':highestClose180,'Lowest Closing Price 180 Days': lowestClose180, 'Highest Closing Price Annual':highestClose365,'Lowest Closing Price Annual': lowestClose365}

    highs = {'Highest Daily Price 7 Days':highestHigh7,'Lowest Daily High 7 Days': lowestHigh7,'Highest Daily Price 14 Days':highestHigh14,'Lowest Daily High 14 Days': lowestHigh14,
    'Highest Daily Price 30 Days':highestHigh30,'Lowest Daily High 30 Days': lowestHigh30,
     'Highest Daily Price 90 Days':highestHigh90,'Lowest Daily High 90 Days': lowestHigh90,'Highest Daily Price 180 Days':highestHigh180,'Lowest Daily High 180 Days': lowestHigh180,
    'Highest Daily Price Annual':highestHigh365,'Lowest Daily High Annual': lowestHigh365}

    lows = {'Lowest Daily Price 7 Days':lowestLow7,'Highest Daily Low 7 Days': highestLow7,'Lowest Daily Price 14 Days':lowestLow14,'Highest Daily Low 14 Days': highestLow14,
    'Lowest Daily Price 30 Days':lowestLow30,'Highest Daily Low 30 Days': highestLow30,'Lowest Daily Price 90 Days':lowestLow90, 'Highest Daily Low 90 Days': highestLow90,
    'Lowest Daily Price 180 Days':lowestLow180,'Highest Daily Low 180 Days': highestLow180,'Lowest Daily Price Annual':lowestLow365,'Highest Daily Low Annual': highestLow365}

    volume = {'Volume 24 Hour':Vol24H,'Highest Daily Volume 7 Days': highestVol7,'Lowest Daily Volume 7 Days': lowestVol7,'Highest Daily Volume 14 Days': highestVol14,
    'Lowest Daily Volume 14 Days': lowestVol14,'Highest Daily Volume 30 Days':highestVol30,'Lowest Daily Volume 30 Days': lowestVol30,'Highest Daily Volume 90 Days':highestVol90,
    'Lowest Daily Volume 90 Days': lowestVol90,'Highest Daily Volume 180 Days':highestVol180,'Lowest Daily Volume 180 Days': lowestVol180, 'Highest Daily Volume Annual':highestVol365,
    'Lowest Daily Volume Annual': lowestVol365}

    seven = {'Highest Daily Volume 7 Days': highestVol7,'Lowest Daily Volume 7 Days': lowestVol7,'Highest Opening Price 7 Days':highestOpen7,
    'Lowest Opening Price 7 Days': lowestOpen7,'Highest Closing Price 7 Days':highestClose7,'Lowest Closing Price 7 Days': lowestClose7,
    'Highest Daily Price 7 Days':highestHigh7,'Lowest Daily High 7 Days': lowestHigh7, 'Lowest Daily Price 7 Days':lowestLow7,'Highest Daily Low 7 Days': highestLow7}

    fourteen = {'Highest Daily Volume 14 Days': highestVol14,'Lowest Daily Volume 14 Days': lowestVol14,'Highest Daily Opening Price 14 Days':highestOpen14,
    'Lowest Daily Opening Price 14 Days': lowestOpen14,'Highest Daily Closing Price 14 Days':highestClose14,'Lowest Daily Closing Price 14 Days': lowestClose14,
     'Highest Daily Price 14 Days':highestHigh14,'Lowest Daily High 14 Days': lowestHigh14, 'Lowest Daily Price 14 Days':lowestLow14,'Highest Daily Low 14 Days': highestLow14}

    thirty = {'Highest Daily Volume 30 Days': highestVol30,'Lowest Daily Volume 30 Days': lowestVol30, 'Highest Opening Price 30 Days':highestOpen30,'Lowest Opening Price 30 Days': lowestOpen30,
    'Highest Closing Price 30 Days':highestClose30,'Lowest Closing Price 30 Days': lowestClose30, 'Highest Daily Price 30 Days':highestHigh30,
    'Lowest Daily High 30 Days': lowestHigh30,'Lowest Daily Price 30 Days':lowestLow30,'Highest Daily Low 30 Days': highestLow30}

    ninety = {'Highest Daily Volume 90 Days': highestVol90,'Lowest Daily Volume 90 Days': lowestVol90,'Highest Opening Price 90 Days':highestOpen90,
    'Lowest Opening Price 90 Days': lowestOpen90,'Highest Closing Price 90 Days':highestClose90,'Lowest Closing Price 90 Days': lowestClose90, 'Highest Daily Price 90 Days':highestHigh90,
    'Lowest Daily High 90 Days': lowestHigh90, 'Lowest Daily Price 90 Days':lowestLow90,'Highest Daily Low 90 Days': highestLow90}

    oneeighty = {'Highest Daily Volume 180 Days': highestVol180,'Lowest Daily Volume 180 Days': lowestVol180,'Highest Opening Price 180 Days':highestOpen180,'Lowest Opening Price 180 Days': lowestOpen180,
    'Highest Closing Price 180 Days':highestClose180,'Lowest Closing Price 180 Days': lowestClose180,'Highest Daily Price 180 Days':highestHigh180,'Lowest Daily High 180 Days': lowestHigh180,
    'Lowest Daily Price 180 Days':lowestLow180,'Highest Daily Low 180 Days': highestLow180}

    annual = {'Highest Daily Volume Annual': highestVol365,'Lowest Daily Volume Annual': lowestVol365,'Highest Opening Price Annual':highestOpen365,'Lowest Opening Price Annual': lowestOpen365,
    'Highest Closing Price Annual':highestClose365,'Lowest Closing Price Annual': lowestClose365,'Highest Daily Price Annual':highestHigh365,'Lowest Daily High Annual': lowestHigh365,
    'Lowest Daily Price Annual':lowestLow365,'Highest Daily Low Annual': highestLow365}
    
    for key, value in thirty.items():
        print(key + ': '+str(value))
    for key, value in ninety.items():
        print(key + ': '+str(value))
    for key, value in oneeighty.items():
        print(key + ': '+str(value))
    return statistics, latest,opening,closing,highs,lows, volume, seven, fourteen, thirty,ninety,oneeighty,annual



