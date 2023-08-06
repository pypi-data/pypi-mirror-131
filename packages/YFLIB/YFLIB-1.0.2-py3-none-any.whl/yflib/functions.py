from yflib._dayEnd import _read_dayEnd

from yflib.indicators._BBANDS import _read_BBANDS
from yflib.indicators._CCI import _read_CCI
from yflib.indicators._EMA import _read_EMA
from yflib.indicators._MACD import _read_MACD
from yflib.indicators._OBV import _read_OBV
from yflib.indicators._RSI import _read_RSI
from yflib.indicators._SMA import _read_SMA
from yflib.indicators._STOCH import _read_STOCH
from yflib.indicators._STOCHRSI import _read_STOCHRSI

from yflib._common import _commonDateFilter

def read_dayEnd(stock,startDate=None,endDate=None,usecols=None,verbose=False):
    return _read_dayEnd(stock,startDate,endDate,usecols,verbose)

def read_indicator(stock,indicator,period=None,startDate=None,endDate=None,verbose=False):
    if indicator == "BBANDS":
        stockData = _read_BBANDS(stock,verbose)
    elif indicator == "CCI":
        stockData =_read_CCI(stock,period,verbose)
    elif indicator == "EMA":
        stockData = _read_EMA(stock,period,verbose)
    elif indicator == "MACD":
        stockData = _read_MACD(stock,verbose)
    elif indicator == "OBV":
        stockData = _read_OBV(stock,verbose)
    elif indicator == "RSI":
        stockData = _read_RSI(stock,period,verbose)
    elif indicator == "SMA":
        stockData = _read_SMA(stock,period,verbose)
    elif indicator == "STOCH":
        stockData = _read_STOCH(stock,verbose)
    elif indicator == "STOCHRSI":
        stockData = _read_STOCHRSI(stock,period,verbose)
    else: # Exception
        return None
    stockData = _commonDateFilter(stockData, startDate, endDate)
    return stockData
    

