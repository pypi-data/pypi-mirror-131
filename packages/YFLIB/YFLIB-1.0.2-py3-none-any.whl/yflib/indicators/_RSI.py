import traceback
import os
# ========
from yflib._common import _writeCSVFile, _readCSVFile, _pathlized
from yflib._dayEnd import _load_YF
# ========

def RSICalculation(dataframe, period, ema = True):
    RSI_period = "RSI_"+str(period)
    close_delta = dataframe['Close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    # Use exponential moving average
        dataframe['ma_up'] = up.ewm(com = period - 1, adjust=True, min_periods = period).mean()
        dataframe['ma_down'] = down.ewm(com = period - 1, adjust=True, min_periods = period).mean()
    else:
        # Use simple moving average
        dataframe['ma_up'] = up.rolling(window = period, adjust=False).mean()
        dataframe['ma_down'] = down.rolling(window = period, adjust=False).mean()
        
    rsi = dataframe['ma_up'] / dataframe['ma_down']
    dataframe[RSI_period] = 100 - (100/(1 + rsi))
    return dataframe[RSI_period]

def _RSI(stockList, period, verbose):
    if stockList and isinstance(stockList, list):
        try:
            for stock in stockList:
                FileName = stock+"_RSI"+str(period)
                path = _pathlized(stock,"_dayEnd")
                if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
                    _load_YF([stock],verbose)
                dayendcsv = _readCSVFile(stock,"_dayEnd", verbose)
                rsi = RSICalculation(dayendcsv, period)
                _writeCSVFile(FileName, rsi, verbose)
        except:
            print(stock+"|RSI - Load Failed")
            if verbose == True:
                traceback.print_exc()
    else:
        print("StockList Invalid")

def _read_RSI(stock, period, verbose):
    path = _pathlized(stock,"_EMA"+str(period))
    try:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
            _RSI([stock], period, verbose)
        stockData = _readCSVFile(stock,"_RSI"+str(period),verbose)
        return stockData
    except:
        print(stock+"|RSI - Read Failed")
        if verbose==True:
            traceback.print_exc()
        return None
