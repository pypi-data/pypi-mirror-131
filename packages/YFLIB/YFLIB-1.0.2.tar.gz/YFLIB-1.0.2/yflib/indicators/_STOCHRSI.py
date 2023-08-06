import pandas as pd
import traceback
import os
#==========
from yflib._common import _writeCSVFile, _readCSVFile, _pathlized
from yflib.indicators._RSI import _RSI
#==========

def rsistochastics(stock, period):
    k_period = 3
    RSI_period = "RSI_"+str(period)
    path = _pathlized(stock,RSI_period)

    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
        _RSI([stock],period, False)
    rsi_period=_readCSVFile(stock, "_RSI"+str(period), False)

    low_min  = rsi_period[RSI_period].rolling( window = k_period ).min()
    high_max = rsi_period[RSI_period].rolling( window = k_period ).max()

    stochrsi_K = (rsi_period[RSI_period]-low_min)/(high_max-low_min)*100
    stochrsi_K = stochrsi_K.rename("STOCHRSI_"+str(period)+"_FastK", inplace=True)
    stochrsi_D = stochrsi_K.rolling(k_period).mean()
    stochrsi_D = stochrsi_D.rename("STOCHRSI_"+str(period)+"_FastD", inplace=True)
    stochrsi = pd.concat([stochrsi_D,stochrsi_K], axis=1)
    return stochrsi

def _STOCHRSI(stockList, period, verbose):
    if stockList and isinstance(stockList,list):
        try:
            for stock in stockList:
                FileName = stock+"_STOCHRSI"+str(period)
                returncsv = rsistochastics(stock, period)
                _writeCSVFile(FileName,returncsv, verbose)
        except:
            print(stock+"|RSI - Load Failed")
            if verbose == True:
                traceback.print_exc()
    else:
        print("StockList Invalid")

def _read_STOCHRSI(stock, period, verbose):
    path = _pathlized(stock,"_STOCHRSI"+str(period))
    try:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
            _STOCHRSI([stock],period, verbose)
        stockData = _readCSVFile(stock,"_STOCHRSI"+str(period),verbose)
        return stockData
    except:
        print(stock+"|RSI - Read Failed")
        if verbose==True:
            traceback.print_exc()
        return None

