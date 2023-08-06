import traceback
import os
import numpy as np
# ========
from yflib._common import _writeCSVFile, _readCSVFile, _pathlized
from yflib._dayEnd import _load_YF
# ========

def OBVCalculation(dataframe):
    dataframe["OBV"] = (np.sign(dataframe['Close'].diff()) * dataframe['Volume']).fillna(0).cumsum()
    return dataframe["OBV"]

def _OBV(stockList, verbose):
    if stockList and isinstance(stockList, list):
        try:
            for stock in stockList:
                FileName = stock+"_OBV"
                path = _pathlized(stock,"_dayEnd")
                if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), path)):
                    _load_YF([stock], verbose)
                dayendcsv = _readCSVFile(stock, "_dayEnd", verbose)
                obv = OBVCalculation(dayendcsv)
                _writeCSVFile(FileName, obv, verbose)
        except:
            print(stock+"|OBV - Load Failed")
            if verbose == True:
                traceback.print_exc()
    else:
        print("StockList Invalid")

def _read_OBV(stock, verbose):
    path = _pathlized(stock,"_OBV")
    try:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
            _OBV([stock] ,verbose)
        stockData = _readCSVFile(stock, "_OBV" ,verbose)
        return stockData
    except:
        print(stock+"|OBV - Read Failed")
        if verbose==True:
            traceback.print_exc()
        return None
        