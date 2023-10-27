## Angy Sanchez
# Importing basic libraries
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import scipy.stats as spst
import matplotlib.mlab as mlab
# library for dataframes
import pandas as pd
# library for solar position
import ephem
# library for date time format
from datetime import timedelta
# import functions
import StationData

# Main function
def days(df):
    df = [group[1] for group in df.groupby(df.index.date)]
    return df

def night(df):
    dfn =df[df['solar_radiation'] == 0]
    return dfn

def day(df):
    dfd =df[df['solar_radiation'] != 0]
    return dfd

def dfUHII_day(dfrom,dto):
    uhi =[]
    dfr = day(StationData.ref(dfrom, dto))
    for i in range(len(StationData.stations15(dfrom,dto))):
        s = day(StationData.stations15(dfrom,dto)[i])
        uhi.append(s.temperature - dfr['Tair'])  # .to_frame(name='UHI')
    # Create a dataframe of UHI for each station
    d = {'Station_1': uhi[0], 'Station_3': uhi[1], 'Station_4': uhi[2], 'Station_5': uhi[3], 'Station_6': uhi[4],
         'Station_7': uhi[5]}
    dfUHI = pd.DataFrame(data=d)
    dfUHI = dfUHI.asfreq(freq='15min')
    dfUHI = dfUHI.dropna(axis=0)
    return dfUHI

def dfUHII_night(dfrom,dto):
    uhi =[]
    dfr = night(StationData.ref(dfrom, dto))
    for i in range(len(StationData.stations15(dfrom,dto))):
        s = night(StationData.stations15(dfrom,dto)[i])
        uhi.append(s.temperature - dfr['Tair'])  # .to_frame(name='UHI')
    # Create a dataframe of UHI for each station
    d = {'Station_1': uhi[0], 'Station_3': uhi[1], 'Station_4': uhi[2], 'Station_5': uhi[3], 'Station_6': uhi[4],
         'Station_7': uhi[5]}
    dfUHI = pd.DataFrame(data=d)
    dfUHI = dfUHI.asfreq(freq='15min')
    dfUHI = dfUHI.dropna(axis=0)
    return dfUHI





# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


