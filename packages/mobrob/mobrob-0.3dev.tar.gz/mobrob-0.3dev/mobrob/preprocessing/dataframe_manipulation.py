import numpy as np
import pandas as pd

# todo: add time param (default 0.1sec)
def resample_df(df_orig, rule='100ms'):
    df = df_orig.copy()
    df['td'] = pd.to_timedelta(df['time'], 'ms')
    df.set_index(df['td'])
    df = df.resample(rule, on='td').mean().bfill()
    #df = df.drop(columns=['time'])
    return df
