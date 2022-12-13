import pandas as pd
import os
def Savedf2CSV(df:pd.DataFrame, name:str):
    df.to_csv('Files' + os.sep + name + '.csv')
def ReadfCSV(name: str):
    df = pd.read_csv('Files' + os.sep + name + '.csv', index_col=0)
    return df
def ReadfPARQUET(name: str):
    df = pd.read_parquet('Files' + os.sep + name + '.parquet')
    return df
def Savedf2PARQUET(df:pd.DataFrame, name:str):
    df.to_parquet('Files' + os.sep + name + '.csv')