import traceback
import os
import pandas as pd
# ========
from yflib._common import _writeCSVFile, _readCSVFile, _pathlized
from yflib._dayEnd import _load_YF
# ========

def SMACalculation(dataframe, period):
    sma = dataframe.rolling(window = period).mean()
    sma = sma.rename("SMA")
    sma = pd.DataFrame(sma)
    return sma

def _SMA(stockList, period, verbose):
    if stockList and isinstance(stockList, list):
        try:
            for stock in stockList:
                FileName = stock+"_SMA"+str(period)
                path = _pathlized(stock,"_dayEnd")
                if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
                    _load_YF([stock],verbose)
                dayendcsv = _readCSVFile(stock,"_dayEnd", verbose)
                sma = SMACalculation(dayendcsv["Close"], period)
                _writeCSVFile(FileName, sma, verbose)
        except:
            print(stock+"|SMA - Load Failed")
            if verbose == True:
                traceback.print_exc()
    else:
        print("StockList Invalid")

def _read_SMA(stock, period, verbose):
    path = _pathlized(stock,"_SMA"+str(period))
    try:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
            _SMA([stock], period, verbose)
        stockData = _readCSVFile(stock,"_SMA"+str(period),verbose)
        return stockData
    except:
        print(stock+"|SMA - Read Failed")
        if verbose==True:
            traceback.print_exc()
        return None
