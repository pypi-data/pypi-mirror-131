import traceback
import os
import pandas as pd
# ========
from yflib._common import _writeCSVFile, _readCSVFile, _pathlized
from yflib.indicators._EMA import EMAcalculation
from yflib._dayEnd import _load_YF
# ========

def MACDcalcution(dayendcsv):
    ema12 = EMAcalculation(dayendcsv,'Close',12)
    ema26 = EMAcalculation(dayendcsv,'Close',26)
    dayendcsv['MACD'] = ema12 - ema26
    ema9 = EMAcalculation(dayendcsv,'MACD',9)
    dayendcsv['MACD_Signal'] = ema9
    dayendcsv["MACD_Hist"] = dayendcsv["MACD"]-dayendcsv["MACD_Signal"]
    return dayendcsv

def _MACD(stockList, verbose):
    if stockList and isinstance(stockList, list):
        try:
            for stock in stockList:
                FileName = stock+"_MACD"
                path = _pathlized(stock,"_dayEnd")
                if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
                    _load_YF([stock],verbose)
                dayendcsv = _readCSVFile(stock,"_dayEnd", verbose)
                MACD = MACDcalcution(dayendcsv)
                returncsv = pd.concat([MACD['MACD'], MACD['MACD_Signal'], MACD['MACD_Hist']], axis=1)
                _writeCSVFile(FileName, returncsv, verbose)
        except:
            print(stock+"|MACD - Load Failed")
            if verbose == True:
                traceback.print_exc()
    else:
        print("StockList Invalid")
        return None

def _read_MACD(stock, verbose):
    path = _pathlized(stock,"_MACD")
    try:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
            _MACD([stock], verbose)
        stockData = _readCSVFile(stock,"_MACD", verbose)
        return stockData
    except:
        print(stock+"|MACD - Read Failed")
        if verbose==True:
            traceback.print_exc()
        return None
