import traceback
import os
import pandas as pd
# ========
from yflib._common import _writeCSVFile, _readCSVFile, _pathlized
from yflib._dayEnd import _load_YF
# ========

def BBANDSCalculation(TPdataframe):
    BBanddataframe = TPdataframe["TP"].rolling(20).mean()
    BBanddataframe = BBanddataframe.rename("BB_Real_Middle_Band")
    BBanddataframe = pd.DataFrame(BBanddataframe)
    TPstd = TPdataframe["TP"].rolling(20).std()
    BBanddataframe["BB_Real_Upper_Band"] = BBanddataframe["BB_Real_Middle_Band"] + 2 * TPstd
    BBanddataframe["BB_Real_Lower_Band"] = BBanddataframe["BB_Real_Middle_Band"] - 2 * TPstd
    return BBanddataframe

def TPCalculation(dataframe):
    TPdataframe = (dataframe['Close']+dataframe['High']+dataframe['Low'])/3
    TPdataframe = TPdataframe.rename("TP")
    return pd.DataFrame(TPdataframe)

def _BBANDS(stockList, verbose):
    if stockList and isinstance(stockList, list):
        try:
            for stock in stockList:
                FileName = stock + "_BBANDS"
                path = _pathlized(stock,"_dayend")
                if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), path)):
                    _load_YF([stock], verbose)
                dayendcsv = _readCSVFile(stock, "_dayEnd", verbose)
                tp = TPCalculation(dayendcsv)
                bbands = BBANDSCalculation(tp)
                _writeCSVFile(FileName, bbands, verbose)
        except:
            print(stock+"|BBANDS - Load Failed")
            if verbose == True:
                traceback.print_exc()
    else:
        print("StockList Invalid")

def _read_BBANDS(stock, verbose):
    path = _pathlized(stock,"_BBANDS")
    try:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
            _BBANDS([stock] ,verbose)
        stockData = _readCSVFile(stock, "_BBANDS" ,verbose)
        return stockData
    except:
        print(stock+"|BBANDS - Read Failed")
        if verbose==True:
            traceback.print_exc()
        return None
