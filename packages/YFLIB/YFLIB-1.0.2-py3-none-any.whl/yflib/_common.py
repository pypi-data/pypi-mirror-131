import os
import pandas as pd

__current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

def _writeCSVFile(fileName, dataFrame,verbose):
    try:
        path = __current_path+"/cache/"+fileName+".csv"
        dataFrame.to_csv(path,index=True)
    except:
        if verbose == True:
            print("Unable to write files. Please check if root permission granted or not.")

def _readCSVFile(stock,metaData,verbose):
    try:
        path = __current_path+"/cache/"+stock+metaData+".csv"
        return pd.read_csv(path,index_col=[0])
    except:
        if verbose == True:
            print("File not found. Please run load before read")
        return None

# --- Date are inclusive ---
def _commonDateFilter(dataframe,startDate,endDate):
    if startDate:
        dataframe = dataframe[(dataframe.index>=startDate)]
    if endDate:
        dataframe = dataframe[(dataframe.index<=endDate)]
    return dataframe
# --------------------------

def _pathlized(stock,metaName):
    return "cache/"+stock+metaName+".csv"