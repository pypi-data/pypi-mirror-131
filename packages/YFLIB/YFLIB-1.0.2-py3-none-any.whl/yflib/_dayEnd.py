import yfinance as yf
import traceback
import pandas as pd
import os
# -------------------

from yflib._common import _writeCSVFile,_readCSVFile,_commonDateFilter
#---------------------

def _load_YF(stockList,verbose):
    if stockList and isinstance(stockList,list):
        try:
            for stock in stockList:

                stockTicker = yf.Ticker(stock)
                div = stockTicker.dividends.to_dict()
                splits = stockTicker.splits.to_dict()

                stockData = yf.download(stock)
                stockData = __consolid(stockData,div,splits)
                
                _writeCSVFile(stock+"_dayEnd",stockData,verbose)
        except:
            print(stock+"|dayEnd - Load Failed")
            if verbose == True:
                traceback.print_exc()
    else:
        print("StockList Invalid")

def _read_dayEnd(stock,startDate,endDate,usecols,verbose):
    try:
        path = "cache/"+ stock + "_dayEnd"+".csv" 
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),path)):
            _load_YF([stock],verbose)
            
        stockData = _readCSVFile(stock,"_dayEnd",verbose)
        

        if usecols is not None:
            stockData = stockData.filter(items=usecols, axis=1)
            
        stockData = _commonDateFilter(stockData,startDate,endDate)
        return stockData
    except:
        print(stock+"|dayEnd - Read Failed")
        if verbose==True:
            traceback.print_exc()
        return None

def __consolid(stockData,div,splits):
    divArray = []
    splitsArray = []
    for date,value in stockData.iterrows():
        if date in div:
            divArray.append(div[date])
        else:
            divArray.append(0)

        if date in splits:
            splitsArray.append(splits[date])
        else:
            splitsArray.append(0)
    divDF = pd.DataFrame(divArray,index=stockData.index,columns=["dividend_amount"])
    splitsDF = pd.DataFrame(splitsArray,index=stockData.index,columns=["split_coefficient"])
    stockData = pd.concat([stockData,divDF,splitsDF],axis=1)
    return stockData

# def __dateModify(date):
#     array = []
#     for d in date:
#         array.append(d.strftime("%Y-%m-%d"))
#     return array