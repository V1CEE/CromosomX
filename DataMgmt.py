import pandas as pd
import os
def Savedf2CSV(df:pd.DataFrame, name:str):
    df.to_csv('Files' + os.sep + name + '.csv', index=False)
def ReadfCSV(name: str):
    df = pd.read_csv('Files' + os.sep + name + '.csv')
    return df
def ReadfPARQUET(name: str):
    df = pd.read_parquet('Files' + os.sep + name + '.parquet')
    return df
