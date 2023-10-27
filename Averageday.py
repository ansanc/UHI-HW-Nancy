#####
# Angy Sanchez
# Importing libraries
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

# other files
import daydivision
import StationData

# Main general data

# date time format
dateFMT = '%Y-%m-%d %H:%M:%S'
# Stations
ref = 'MeteoCiel'
varref = ['utc', 'Tair', 'Rain', 'Nebulosity', 'WindSpeed', 'RH']
var = ['utc', 'legaltime', 'temperature', 'hygrometry', 'solar_radiation', 'wind_speed_min', 'wind_speed_max',
       'wind_speed_average', 'co2', 'voltage']
station_name = ['LRN', 'CharlesIII', 'GrandNancy', 'AvironClub', 'CollegeND', 'Aiguillage']

# a = input("Is the date range the same as the initial dates? Please write YES or NOT" )
# if a == 'NOT':
  #  dfrom = input("Insert new initial date")
   # dto = input("Insert new final date")
#####
# AVERAGE 24H
#####
# Temperature
def average15_24h_temperature(station_number, dfrom, dto):
    # ,fromDay,toDay):
    station = daydivision.days(StationData.stations15(dfrom,dto)[int(station_number)])
    # for i in range(fromDay,toDay):
    day_1 = station[1].temperature
    day_2 = station[2].temperature
    day_3 = station[3].temperature
    day_4 = station[4].temperature
    zippedList = list(zip(day_1, day_2, day_3, day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3', 'Day4'])
    # generation of timestamps
    n = len(df)
    df.index = pd.date_range('00:00', periods=n, freq='15min').strftime('%H:%M:%S')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    averageT = df['Average_day']
    return averageT
def averageRef_24h_temperature(dfrom, dto):  # ,fromDay,toDay):
    station = daydivision.days(StationData.ref(dfrom, dto))
    # for i in range(fromDay,toDay):
    day_1 = station[1].Tair
    day_2 = station[2].Tair
    day_3 = station[3].Tair
    day_4 = station[4].Tair
    zippedList = list(zip(day_1, day_2, day_3, day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3', 'Day4'])
    # generation of timestamps
    n = len(df)
    df.index = pd.date_range('00:00', periods=n, freq='15min').strftime('%H:%M:%S')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    refT_mean = df['Average_day']
    return refT_mean
#####
# Solar radiation
def average15_24h_radiation(station_number, dfrom, dto):  # ,fromDay,toDay):
    station = daydivision.days(StationData.stations15(dfrom,dto)[int(station_number)])
    # for i in range(fromDay,toDay):
    day_1 = station[1].solar_radiation
    day_2 = station[2].solar_radiation
    day_3 = station[3].solar_radiation
    day_4 = station[4].solar_radiation
    zippedList = list(zip(day_1, day_2, day_3, day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3','Day4'])
    # generation of timestamps
    n = len(df)
    df.index = pd.date_range('00:00', periods=n, freq='15min').strftime('%H:%M:%S')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    averageSun = df['Average_day']
    return averageSun
def averageRef_24h_radiation(dfrom, dto):  # ,fromDay,toDay):
    station = daydivision.days(StationData.ref(dfrom, dto))
    day_1 = station[1].solar_radiation
    day_2 = station[2].solar_radiation
    day_3 = station[3].solar_radiation
    day_4 = station[4].solar_radiation
    zippedList = list(zip(day_1, day_2, day_3, day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3','Day4'])
    # generation of timestamps
    n = len(df)
    df.index = pd.date_range('00:00', periods=n, freq='15min').strftime('%H:%M:%S')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    refmeanrad = df['Average_day']
    return refmeanrad
#####
# Wind
def average15_24h_wind(station_number, dfrom, dto):  # ,fromDay,toDay):
    station = daydivision.days(StationData.stations15(dfrom,dto)[int(station_number)])
    # for i in range(fromDay,toDay):
    day_1 = station[1].wind_speed_average
    day_2 = station[2].wind_speed_average
    day_3 = station[3].wind_speed_average
    day_4 = station[4].wind_speed_average
    zippedList = list(zip(day_1, day_2, day_3, day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3', 'Day4'])
    # generation of timestamps
    n = len(df)
    df.index = pd.date_range('00:00', periods=n, freq='15min').strftime('%H:%M:%S')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    averageWind = df['Average_day']
    return averageWind
def averageRef_24h_wind(dfrom, dto):  # ,fromDay,toDay):
    station = daydivision.days(StationData.ref(dfrom, dto))
    # for i in range(fromDay,toDay):
    day_1 = station[1].WindSpeed
    day_2 = station[2].WindSpeed
    day_3 = station[3].WindSpeed
    day_4 = station[4].WindSpeed
    zippedList = list(zip(day_1, day_2, day_3, day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3','Day4'])
    # generation of timestamps
    n = len(df)
    df.index = pd.date_range('00:00', periods=n, freq='15min').strftime('%H:%M:%S')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    refmeanWind = df['Average_day']
    return refmeanWind
#####
# UHII
# AVERAGE UHI
def meanUHI_24h(station_number, dfrom, dto):
    station = daydivision.days(StationData.dfUHII(dfrom, dto).iloc[:, station_number])
    # for i in range(fromDay,toDay):
    day_1 = station[1]
    day_2 = station[2]
    day_3 = station[3]
    day_4 = station[4]
    zippedList = list(zip(day_1, day_2, day_3, day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3', 'Day4'])
    # generation of timestamps
    n = len(df)
    df.index = pd.date_range('00:00:00 27/06/2019', periods=n, freq='15min')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    averageUHI = df['Average_day']
    return averageUHI
#####
# AVERAGE DAY
#####
#####
# Wind
def average15_day_wind(station_number, dfrom, dto):  # ,fromDay,toDay):
    dfday = daydivision.day(StationData.stations15(dfrom,dto)[int(station_number)])
    station = daydivision.days(dfday)
    # for i in range(fromDay,toDay):
    day_1 = station[1].wind_speed_average
    day_2 = station[2].wind_speed_average
    day_3 = station[3].wind_speed_average
    day_4 = station[4].wind_speed_average
    zippedList = list(zip(day_1, day_2, day_3,day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3','Day4'])
    # generation of timestamps
    n = len(df)
    dfday['utc'] = dfday.index
    df.index = pd.date_range(start=str(dfday.utc[0]), periods=n, freq= '15min')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    averageWind = df['Average_day']
    return averageWind
def averageRef_day_wind(dfrom, dto):  # ,fromDay,toDay):
    dfday = daydivision.day(StationData.ref(dfrom, dto))
    station = daydivision.days(dfday)
    # for i in range(fromDay,toDay):
    day_1 = station[1].WindSpeed
    day_2 = station[2].WindSpeed
    day_3 = station[3].WindSpeed
    day_4 = station[4].WindSpeed
    zippedList = list(zip(day_1, day_2, day_3, day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3','Day4'])
    # generation of timestamps
    n = len(df)
    dfday['utc'] = dfday.index
    df.index = pd.date_range(start=str(dfday.utc[0]), periods=n, freq= '15min')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    refmeanWind = df['Average_day']
    return refmeanWind
#####
# UHII
def meanUHI_day(station_number, dfrom, dto):
    dfd = daydivision.dfUHII_day(dfrom, dto)
    station = daydivision.days(daydivision.dfUHII_day(dfrom, dto).iloc[:, station_number])
    # for i in range(fromDay,toDay):
    day_1 = station[1]
    day_2 = station[2]
    day_3 = station[3]
    day_4 = station[4]
    zippedList = list(zip(day_1, day_2, day_3,day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3','Day4'])
    # generation of timestamps
    n = len(df)
    dfd['utc'] = dfd.index
    df.index = pd.date_range(start=str(dfd.utc[0]), periods=n, freq='15min')
    #df.index = pd.date_range('00:00:00 27/06/2019', periods=n, freq='15min')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    averageUHI = df['Average_day']
    return averageUHI
#####
# AVERAGE NIGHT
#####
def average15_night_wind(station_number, dfrom, dto):  # ,fromDay,toDay):
    dfnight = daydivision.night(StationData.stations15(dfrom,dto)[int(station_number)])
    station = daydivision.days(dfnight)
    # for i in range(fromDay,toDay):
    day_1 = station[1].wind_speed_average
    day_2 = station[2].wind_speed_average
    day_3 = station[3].wind_speed_average
    day_4 = station[4].wind_speed_average
    zippedList = list(zip(day_1, day_2, day_3,day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3','Day4'])
    # generation of timestamps
    n = len(df)
    df.index = pd.date_range(start=str(dfnight.utc[0]), periods=n, freq= '15min')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    averageWind = df['Average_day']
    return averageWind
def averageRef_night_wind(dfrom, dto):  # ,fromDay,toDay):
    dfnight = daydivision.night(StationData.ref(dfrom, dto))
    station = daydivision.days(dfnight)
    # for i in range(fromDay,toDay):
    day_1 = station[1].WindSpeed
    day_2 = station[2].WindSpeed
    day_3 = station[3].WindSpeed
    day_4 = station[4].WindSpeed
    zippedList = list(zip(day_1, day_2, day_3,day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3','Day4'])
    # generation of timestamps
    n = len(df)
    dfnight['utc'] = dfnight.index
    df.index = pd.date_range(start=str(dfnight.utc[0]), periods=n, freq= '15min')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    refmeanWind = df['Average_day']
    return refmeanWind
def meanUHI_night(station_number, dfrom, dto):
    dfn = daydivision.dfUHII_night(dfrom, dto)
    station = daydivision.days(daydivision.dfUHII_night(dfrom, dto).iloc[:, station_number])
    # for i in range(fromDay,toDay):
    day_1 = station[1]
    day_2 = station[2]
    day_3 = station[3]
    day_4 = station[4]
    zippedList = list(zip(day_1, day_2, day_3,day_4))
    df = pd.DataFrame(zippedList, columns=['Day1', 'Day2', 'Day3','Day4'])
    # generation of timestamps
    n = len(df)
    dfn['utc'] = dfn.index
    df.index = pd.date_range(start=str(dfn.utc[0]), periods=n, freq='15min')
    col = df.loc[:, "Day1":"Day4"]
    df['Average_day'] = col.mean(axis=1)
    averageUHI = df['Average_day']
    return averageUHI
