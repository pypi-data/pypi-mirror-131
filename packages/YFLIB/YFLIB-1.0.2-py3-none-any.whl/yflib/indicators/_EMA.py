import traceback
import os
# ========
from yflib._common import _writeCSVFile, _readCSVFile, _pathlized
from yflib._dayEnd import _load_YF
# ========

def EMAcalculation(df, type, period):
    EMA_Period = 'EMA_' + str(period)
    df[EMA_Period] = df[type].ewm(span=period, adjust=False, min_periods = period).mean()
    # ema = []
    # for i in range(period-1):
    #     ema.append(0)
    # ema.append(sum(df[type][:period]) / period)
    # for price in df[type][period:]:
    #     ema.append((price * (2 / (1 + period))) + ema[-1] * (1 - (2 / (1 + period))))
    # df[EMA_Period] = ema
    return df[EMA_Period]

def _EMA(stockList, period, verbose):
    if stockList and isinstance(stockList, list):
        try:
            for stock in stockList:
                FileName = stock+"_EMA"+str(period)
                path = _pathlized(stock,"_dayEnd")
                if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
                    _load_YF([stock],verbose)
                dayendcsv = _readCSVFile(stock,"_dayEnd", verbose)
                ema = EMAcalculation(dayendcsv, 'Close',period)
                ema[0:period-1] = None
                _writeCSVFile(FileName, ema, verbose)
        except:
            print(stock+"|EMA - Load Failed")
            if verbose == True:
                traceback.print_exc()
    else:
        print("StockList Invalid")

def _read_EMA(stock, period, verbose):
    path = _pathlized(stock,"_EMA"+str(period))
    try:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
            _EMA([stock], period,verbose)
        stockData = _readCSVFile(stock,"_EMA"+str(period), verbose)
        return stockData
    except:
        print(stock+"|EMA - Read Failed")
        if verbose==True:
            traceback.print_exc()
        return None