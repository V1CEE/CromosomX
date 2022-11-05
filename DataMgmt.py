import pandas as pd

def Savedf2CSV(df:pd.DataFrame, name:str):
    df.to_csv(name + '.csv')
def Readf2CSV(df:pd.DataFrame):
    df.read_csv('main_df.csv')