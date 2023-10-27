## Angy Sanchez
# Importing basic libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
# library for dataframes
import pandas as pd
# library for date time format
from datetime import timedelta
#import other functions
import StationData
import Averageday
# date time format
dateFMT = '%Y-%m-%d %H:%M:%S'
# Stations
ref_file = 'MeteoCiel'
rad_file = 'ref_radiation'
varref = ['utc', 'Tair', 'Rain', 'Nebulosity', 'WindSpeed', 'RH']
var = ['utc', 'legaltime', 'temperature', 'hygrometry', 'solar_radiation', 'wind_speed_min', 'wind_speed_max',
       'wind_speed_average', 'co2', 'voltage']
station_name = ['LRN', 'CharlesIII', 'GrandNancy', 'AvironClub', 'CollegeND', 'Aiguillage']

# Max temperature
def maxT24h_15(dfrom,dto):
    lstmax=[]
    for i in range(len(station_name)):
        lstmax.append(Averageday.average15_24h_temperature(i,dfrom,dto).max())
    lstidmax=[]
    for i in range(len(station_name)):
        lstidmax.append(Averageday.average15_24h_temperature(i,dfrom,dto).idxmax())
    df = pd.DataFrame(lstmax,lstidmax)
    return df
def maxTday_15(dfrom,dto):
    lstmax=[]
    for i in range(len(station_name)):
        lstmax.append(Averageday.average15_day_temperature(i,dfrom,dto).max())
    lstidmax=[]
    for i in range(len(station_name)):
        lstidmax.append(Averageday.average15_day_temperature(i,dfrom,dto).idxmax())
    df = pd.DataFrame(lstmax,lstidmax)
    return df
def maxTnight_15(dfrom,dto):
    lstmax=[]
    for i in range(len(station_name)):
        lstmax.append(Averageday.average15_night_temperature(i,dfrom,dto).max())
    lstidmax=[]
    for i in range(len(station_name)):
        lstidmax.append(Averageday.average15_night_temperature(i,dfrom,dto).idxmax())
    df = pd.DataFrame(lstmax,lstidmax)
    return df
def maxT24h_Ref(dfrom,dto):
    lstmax=Averageday.averageRef_24h_temperature(dfrom,dto).max()
    lstidmax=Averageday.averageRef_24h_temperature(dfrom,dto).idxmax()
    df = (lstmax,lstidmax)
    return df
def maxTday_Ref(dfrom,dto):
    lstmax=Averageday.averageRef_day_temperature(dfrom,dto).max()
    lstidmax=Averageday.averageRef_day_temperature(dfrom,dto).idxmax()
    df = (lstmax,lstidmax)
    return df
def maxTnight_Ref(dfrom,dto):
    lstmax=Averageday.averageRef_night_temperature(dfrom,dto).max()
    lstidmax=Averageday.averageRef_night_temperature(dfrom,dto).idxmax()
    df = (lstmax,lstidmax)
    return df

# Max solar radiation
def maxRad_15(dfrom,dto):
    lstmax=[]
    for i in range(len(station_name)):
        lstmax.append(Averageday.average15_24h_radiation(i,dfrom,dto).max())
    lstidmax=[]
    for i in range(len(station_name)):
        lstidmax.append(Averageday.average15_24h_radiation(i,dfrom,dto).idxmax())
    df = pd.DataFrame(lstmax,lstidmax)
    return df
def maxRad_Ref(dfrom,dto):
    lstmax=Averageday.averageRef_24h_radiation(dfrom,dto).max()
    lstidmax=Averageday.averageRef_24h_radiation(dfrom,dto).idxmax()
    df = (lstmax,lstidmax)
    return df

# Max UHII mean day
def maxUHI_24h(dfrom,dto):
    lstmax=[]
    for i in range(len(station_name)):
        lstmax.append(Averageday.meanUHI_24h(i,dfrom,dto).max())
    lstidmax=[]
    for i in range(len(station_name)):
        lstidmax.append(Averageday.meanUHI_24h(i,dfrom,dto).idxmax())
    df = pd.DataFrame(lstmax,lstidmax)
    return df
def maxUHI_day(dfrom,dto):
    lstmax=[]
    for i in range(0,6):
        lstmax.append(Averageday.meanUHI_day(i,dfrom,dto).max())
    lstidmax=[]
    for i in range(0,6):
        lstidmax.append(Averageday.meanUHI_day(i,dfrom,dto).idxmax())
    df = pd.DataFrame(lstmax,lstidmax)
    return df
def maxUHI_night(dfrom,dto):
    lstmax=[]
    for i in range(len(station_name)):
        lstmax.append(Averageday.meanUHI_night(i,dfrom,dto).max())
    lstidmax=[]
    for i in range(len(station_name)):
        lstidmax.append(Averageday.meanUHI_night(i,dfrom,dto).idxmax())
    df = pd.DataFrame(lstmax,lstidmax)
    return df

#### Max UHI all days at day
def maxUHI_allst_day(dfrom,dto):
    def dayUHI_st(station_number, dfrom, dto):
        dfd = daydivision.dfUHII_day(dfrom, dto)
        station = daydivision.days(daydivision.dfUHII_day(dfrom, dto).iloc[:, station_number])
        df1 = pd.DataFrame(station)
        n = len(df1)
        dfd['utc'] = dfd.index
        df1.index = pd.date_range(start=str(dfd.utc[0]), periods=n, freq='15min')
        return df1
    lstmax=[]
    lstidmax = []
    for i in range(len(station_name)):
        lstmax.append(dayUHI_st(i,dfrom,dto).max())
        lstidmax.append(dayUHI_st(i,dfrom,dto).idxmax())
    df = pd.DataFrame(lstmax,lstidmax)
    return df

#### Min UHI all days
def minUHI_allst_day(dfrom,dto):
    dfd = daydivision.dfUHII_day(dfrom, dto)
    def dayUHI_st(station_number, dfrom, dto):
        station = daydivision.days(daydivision.dfUHII_day(dfrom, dto).iloc[:, station_number])
        df1 = pd.DataFrame(station)
        n = len(df1)
        dfd['utc'] = dfd.index
        df1.index = pd.date_range(start=str(dfd.utc[0]), periods=n, freq='15min')
        return df1
    lstmin=[]
    lstidmin = []
    for i in range(len(station_name)):
        lstmin.append(dayUHI_st(i,dfrom,dto).min())
        lstidmin.append(dayUHI_st(i,dfrom,dto).idxmin())
    df = pd.DataFrame(lstmin,lstidmin)
    return df

### Max UHI all days at night
def maxUHI_allst_night(dfrom,dto):
    def nightUHI_st(station_number, dfrom, dto):
        dfn = daydivision.dfUHII_night(dfrom, dto)
        station = daydivision.days(daydivision.dfUHII_night(dfrom, dto).iloc[:, station_number])
        df1 = pd.DataFrame(station)
        n = len(df1)
        dfn['utc'] = dfn.index
        df1.index = pd.date_range(start=str(dfn.utc[0]), periods=n, freq='15min')
        return df1
    lstmax=[]
    lstidmax = []
    for i in range(len(station_name)):
        lstmax.append(nightUHI_st(i,dfrom,dto).max())
        lstidmax.append(nightUHI_st(i,dfrom,dto).idxmax())
    df = pd.DataFrame(lstmax,lstidmax)
    return df

#### Min UHI all days at night
def minUHI_allst_night(dfrom,dto):

    def nightUHI_st(station_number, dfrom, dto):
        dfn = daydivision.dfUHII_night(dfrom, dto)
        station = daydivision.days(daydivision.dfUHII_night(dfrom, dto).iloc[:, station_number])
        df1 = pd.DataFrame(station)
        n = len(df1)
        dfn['utc'] = dfn.index
        df1.index = pd.date_range(start=str(dfn.utc[0]), periods=n, freq='15min')
        return df1
    lstmin=[]
    lstidmin = []
    for i in range(len(station_name)):
        lstmin.append(nightUHI_st(i,dfrom,dto).min())
        lstidmin.append(nightUHI_st(i,dfrom,dto).idxmin())
    df = pd.DataFrame(lstmin,lstidmin)
    return df

