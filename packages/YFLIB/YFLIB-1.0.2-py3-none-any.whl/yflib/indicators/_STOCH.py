import pandas as pd
import traceback
import os 
#==========
from yflib._common import _writeCSVFile, _readCSVFile, _pathlized
from yflib._dayEnd import _load_YF
#==========

def stochastics( dataframe, low, high, close, k, d ):

    df = dataframe.copy()

    # Set minimum low and maximum high of the k stoch
    low_min  = df[low].rolling( window = k ).min()
    high_max = df[high].rolling( window = k ).max()

    # Fast Stochastic
    df['k_fast'] = 100 * (df[close] - low_min)/(high_max - low_min)
    df['d_fast'] = df['k_fast'].rolling(window = d).mean()

    # Slow Stochastic
    df['k_slow'] = df["d_fast"]
    df['d_slow'] = df['k_slow'].rolling(window = d).mean()

    stoch = pd.concat([df['k_slow'], df['d_slow']], axis=1)
    stoch = stoch.rename(columns={'k_slow': 'STOCH_SlowK', 'd_slow':'STOCH_SlowD'})

    return stoch

def _STOCH(stockList, verbose):
    if stockList and isinstance(stockList,list):
        try:
            for stock in stockList:
                FileName = stock+"_STOCH"
                path = _pathlized(stock,"_dayEnd")
                if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
                    _load_YF([stock], verbose)
                dayendcsv = _readCSVFile(stock,"_dayEnd",verbose)
                stochs = stochastics(dayendcsv, 'Low', 'High', 'Close', 5, 3)
                _writeCSVFile(FileName, stochs, verbose)
        except:
            print(stock+"|STOCH - Load Failed")
            if verbose == True:
                traceback.print_exc()
    else:
        print("StockList Invalid")

def _read_STOCH(stock,verbose):
    path = _pathlized(stock,"_STOCH")
    try:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
            _STOCH([stock], verbose)
        stockData = _readCSVFile(stock,"_STOCH",verbose)
        return stockData
    except:
        print(stock+"|STOCH - Read Failed")
        if verbose==True:
            traceback.print_exc()
        return None

