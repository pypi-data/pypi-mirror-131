import traceback
import os
import numpy as np
import pandas as pd
# ========
from yflib._common import _writeCSVFile, _readCSVFile, _pathlized
from yflib._dayEnd import _load_YF
# ========

def CCICalculation(dataframe, period):
    high = dataframe["High"].array
    low = dataframe["Low"].array
    close = dataframe["Close"].array
    total = len(close)

    tp = (high+low+close)/3 # typical price
    atp = np.zeros(total) # average typical price
    md = np.zeros(total) # mean deviation
    result = np.zeros(total)

    for i in range(period-1,total):
        atp[i] = np.sum(tp[i-(period-1):i+1])/period
        md[i] = np.sum(np.fabs(atp[i]-tp[i-(period-1):i+1]))/period
        result[i] = (tp[i]-atp[i])/(0.015*md[i])

    return pd.DataFrame(data=result,index=dataframe.index,columns=["CCI"])

def _CCI(stockList, period, verbose):
    if stockList and isinstance(stockList, list):
        try:
            for stock in stockList:
                FileName = stock+"_CCI"+str(period)
                path = _pathlized(stock,"_dayend")
                if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
                    _load_YF([stock],verbose)
                dayendcsv = _readCSVFile(stock,"_dayEnd", verbose)
                cci = CCICalculation(dayendcsv, period)
                _writeCSVFile(FileName, cci, verbose)
        except:
            print(stock+"|CCI - Load Failed")
            if verbose == True:
                traceback.print_exc()
    else:
        print("StockList Invalid")

def _read_CCI(stock, period,verbose):
    path = _pathlized(stock,"_CCI"+str(period))
    try:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
            _CCI([stock], period, verbose)
        stockData = _readCSVFile(stock,"_CCI"+str(period),verbose)
        return stockData
    except:
        print(stock+"|CCI - Load Failed")
        if verbose==True:
            traceback.print_exc()
        return None
