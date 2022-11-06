import pandas as pd
import os
def Savedf2CSV(df:pd.DataFrame, name:str):
    df.to_csv('Files' + os.sep + name + '.csv')
def Readf2CSV(name: str):
    df = pd.read_csv('Files' + os.sep + name + '.csv')
    return df