from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from .Statistics.hourlyData import stats as hourly 
from .Statistics.dailyData import stats as daily 
from .Statistics.urls import *
from werkzeug.exceptions import abort
from dash import Dash

bp = Blueprint('display', __name__)

@bp.route('/')
def index():
    
    currencyStats,latest,opening,closing,highs,lows, volume,seven,fourteen, thirty,ninety,day180,annual = daily(Bitcoindaily)
   
    return render_template('Stats_Template/Currency.html',  stats = currencyStats, latest = latest, opening= opening,
     closing = closing, highs = highs, lows = lows, volume = volume, seven = seven, fourteen = fourteen, thirty = thirty, ninety = ninety, day180= day180, annual = annual,
      Crypto='Bitcoin' , graphing = 'http://127.0.0.1:5000/dashanalytics/Bitcoin_', HourlyStats = 'display.displayBit_h')

@bp.route('/Bitcoin', methods=('GET', 'POST'))
def displayBit():
    
    currencyStats,latest,opening,closing,highs,lows, volume,seven,fourteen,thirty, ninety,day180,annual = daily(Bitcoindaily)
    return render_template('Stats_Template/Currency.html', stats = currencyStats, latest = latest, opening= opening,
     closing = closing, highs = highs, lows = lows,volume = volume,seven = seven, fourteen = fourteen, thirty = thirty, ninety = ninety, day180= day180, annual = annual, 
     Crypto='Bitcoin', graphing = 'http://127.0.0.1:5000/dashanalytics/Bitcoin_', HourlyStats = 'display.displayBit_h')

@bp.route('/Ethereum', methods=('GET', 'POST'))
def displayEth():

    currencyStats,latest,opening,closing,highs,lows, volume,seven,fourteen, thirty,ninety,day180,annual = daily(Ethereumdaily)
    return render_template('Stats_Template/Currency.html', stats = currencyStats, latest = latest, opening= opening,
     closing = closing, highs = highs, lows = lows,volume = volume,seven = seven, fourteen = fourteen, thirty = thirty, ninety = ninety, day180= day180, annual = annual,
     Crypto='Ethereum' , graphing = 'http://127.0.0.1:5000/dashanalytics/Ethereum_', HourlyStats = 'display.displayEth_h')


@bp.route('/Ethereum_Classic', methods=('GET', 'POST'))
def displayEC():
  
    currencyStats,latest,opening,closing,highs,lows, volume,seven,fourteen, thirty,ninety,day180,annual = daily(EthereumClassicdaily)
    return render_template('Stats_Template/Currency.html', stats = currencyStats, latest = latest, opening= opening,
     closing = closing, highs = highs, lows = lows, volume = volume,seven = seven, fourteen = fourteen, thirty = thirty, ninety = ninety, day180= day180, annual = annual,
     Crypto='Ethereum Classic' , graphing = 'http://127.0.0.1:5000/dashanalytics/EC_', HourlyStats = 'display.displayEC_h')

@bp.route('/XRP', methods=('GET', 'POST'))
def displayXRP():
    
    currencyStats,latest,opening,closing,highs,lows, volume,seven,fourteen, thirty,ninety,day180,annual = daily(XRPdaily)
    return render_template('Stats_Template/Currency.html', stats = currencyStats, latest = latest, opening= opening,
     closing = closing, highs = highs, lows = lows, volume = volume,seven = seven, fourteen = fourteen, thirty = thirty, ninety = ninety, day180= day180, annual = annual, 
     Crypto='XRP' , graphing = 'http://127.0.0.1:5000/dashanalytics/XRP_', HourlyStats = 'display.displayXRP_h')


@bp.route('/Litecoin', methods=('GET', 'POST'))
def displayLite():
   
    currencyStats,latest,opening,closing,highs,lows, volume,seven,fourteen, thirty,ninety,day180,annual = daily(Litecoindaily)
    return render_template('Stats_Template/Currency.html', stats = currencyStats, latest = latest, opening= opening,
     closing = closing, highs = highs, lows = lows, volume = volume,seven = seven, fourteen = fourteen, thirty = thirty, ninety = ninety, day180= day180, annual = annual, 
     Crypto='Litecoin' , graphing = 'http://127.0.0.1:5000/dashanalytics/Litecoin_', HourlyStats = 'display.displayLite_h')

@bp.route('/Bitcoin_h', methods=('GET', 'POST'))
def displayBit_h():
    
    currencyStats,latest,opening,closing,highs,lows, volume,one,seven,fourteen,thirty, ninety,day180,annual = hourly(Bitcoinhourly)
    return render_template('Stats_Template/CurrencyHourly.html', stats = currencyStats, latest = latest, opening= opening,
     closing = closing, highs = highs, lows = lows,volume = volume,one=one,seven = seven, fourteen = fourteen, thirty = thirty, ninety = ninety, day180= day180, annual = annual, 
     Crypto='Bitcoin', graphing = 'http://127.0.0.1:5000/dashanalytics/Bitcoin_', DailyStats = 'display.displayBit',topnav = '_h')

@bp.route('/Ethereum_h', methods=('GET', 'POST'))
def displayEth_h():

    currencyStats,latest,opening,closing,highs,lows, volume,one,seven,fourteen, thirty,ninety,day180,annual = hourly(Ethereumhourly)
    return render_template('Stats_Template/CurrencyHourly.html', stats = currencyStats, latest = latest, opening= opening,
     closing = closing, highs = highs, lows = lows,volume = volume,one=one, seven = seven, fourteen = fourteen, thirty = thirty, ninety = ninety, day180= day180, annual = annual,
     Crypto='Ethereum' , graphing = 'http://127.0.0.1:5000/dashanalytics/Ethereum_', DailyStats = 'display.displayEth',topnav = '_h')


@bp.route('/Ethereum_Classic_h', methods=('GET', 'POST'))
def displayEC_h():
  
    currencyStats,latest,opening,closing,highs,lows, volume,one,seven,fourteen, thirty,ninety,day180,annual = hourly(EthereumClassichourly)
    return render_template('Stats_Template/CurrencyHourly.html', stats = currencyStats, latest = latest, opening= opening,
     closing = closing, highs = highs, lows = lows, volume = volume,one = one, seven = seven, fourteen = fourteen, thirty = thirty, ninety = ninety, day180= day180, annual = annual,
     Crypto='Ethereum Classic' , graphing = 'http://127.0.0.1:5000/dashanalytics/EC_', DailyStats = 'display.displayEC',topnav = '_h' )

@bp.route('/XRP_h', methods=('GET', 'POST'))
def displayXRP_h():
    
    currencyStats,latest,opening,closing,highs,lows, volume,one,seven,fourteen, thirty,ninety,day180,annual = hourly(XRPhourly)
    return render_template('Stats_Template/CurrencyHourly.html', stats = currencyStats, latest = latest, opening= opening,
     closing = closing, highs = highs, lows = lows, volume = volume,one=one,seven = seven, fourteen = fourteen, thirty = thirty, ninety = ninety, day180= day180, annual = annual, 
     Crypto='XRP' , graphing = 'http://127.0.0.1:5000/dashanalytics/XRP_', DailyStats = 'display.displayXRP', topnav = '_h')


@bp.route('/Litecoin_h', methods=('GET', 'POST'))
def displayLite_h():
   
    currencyStats,latest,opening,closing,highs,lows, volume,one,seven,fourteen, thirty,ninety,day180,annual = hourly(Litecoinhourly)
    return render_template('Stats_Template/CurrencyHourly.html', stats = currencyStats, latest = latest, opening= opening,
     closing = closing, highs = highs, lows = lows, volume = volume,one=one,seven = seven, fourteen = fourteen, thirty = thirty, ninety = ninety, day180= day180, annual = annual, 
     Crypto='Litecoin' , graphing = 'http://127.0.0.1:5000/dashanalytics/Litecoin_', DailyStats = 'display.displayLite',topnav = '_h')


    
