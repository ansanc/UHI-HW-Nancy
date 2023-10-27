## Angy Sanchez
# Importing basic libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
# library for dataframes
import pandas as pd
# library for solar position
import ephem
# library for date time format
from datetime import timedelta

# Main general data

# date time format
dateFMT = '%Y-%m-%d %H:%M:%S'
# Stations
ref_file = 'MeteoCiel'
rad_file = 'ref_radiation'
varref = ['utc', 'Tair', 'Rain', 'Nebulosity', 'WindSpeed', 'RH']
var = ['utc', 'legaltime', 'temperature', 'hygrometry', 'solar_radiation', 'wind_speed_min', 'wind_speed_max',
       'wind_speed_average', 'co2', 'voltage']
# first filter for changing the frequency and filling missing days
# just change de year
gapfrom = '2015-01-01 00:00:00'
gapto = '2019-12-31 23:45:00'
# creation of dataframe of data of reference for the first heatwave

def ref(dfrom, dto):
    dfref = pd.read_csv(ref_file + '.csv', skiprows=[1])  # , nrows=200 )
    dfref.index = pd.to_datetime(dfref['utc'], format='%Y-%m-%d %H:%M:%S')
    dfref.sort_index(inplace=True)
    radreffile = pd.read_csv(rad_file + '.csv', skiprows=[1])  # , nrows=200 )
    radreffile.index = pd.to_datetime(radreffile['utc'], format='%Y-%m-%d %H:%M:%S')
    radreffile.sort_index(inplace=True)
    dfref = dfref[dfref.utc.between(gapfrom, gapto)]
    dfref1 = dfref[dfref.utc.between(dfrom, dto)]
    dfref1 = dfref1.drop('utc', axis=1)
    dfref1 = dfref1.asfreq(freq='15min')
    dfref1 = dfref1.interpolate(method='linear')
    radreffile = radreffile[radreffile.utc.between(gapfrom, gapto)]
    radref1 = radreffile[radreffile.utc.between(dfrom, dto)]
    radref1 = radref1.asfreq(freq='15min')
    radref1 = radref1.drop('utc', axis=1)
    radref1 = radref1.interpolate(method='linear')
    r = radref1['GLO'] * 277.778 * 0.01
    dfref1['solar_radiation'] = r.tolist()
    dfref1['Nebulosity'] = dfref1['Nebulosity'].replace('/8', '', regex=True)
    dfref1['Nebulosity'] = dfref1['Nebulosity'].astype(float)
    dfref1['WindSpeed'] = dfref1['WindSpeed'] * (1 / 3.6)
    dfref1['solar_radiation'] * 277.778 * 0.01
    #dfref1['solar_radiation'] * 277.778 *  0.01
    # dfref = dfref.drop('utc', axis=1)
    return dfref1
def importbasedata15(station, dfr, dt):  # , filterdfrom, filterdto):
    df = pd.read_csv(station + '.csv', skiprows=[1])  # , nrows=200 )
# selecting index as utc
    df.index = pd.to_datetime(df['utc'], format='%Y-%m-%d %H:%M:%S')
    cols = df.columns[2:]
    df[cols] = df[cols].apply(pd.to_numeric)
# Dividing data
    df = df[df.utc.between(gapfrom, gapto)]
# filling spaces were the data is not spaced every 15 minutes
    df = df.asfreq(freq='15min')
    # organizing index in case the file is not organized
        # df.sort_index(inplace=True)
        # Selecting range of interes
    df = df[df.utc.between(dfr, dt)]
    return df

    # freq of 1h, good for comparison with MeteoCiel data
def out_range(df):
    srmin = 0 <= df['solar_radiation']
    srmax = 1500 >= df['solar_radiation']
    df['solar_radiation'].where(srmin & srmax, inplace=True)
    Tmin = -35 <= df['temperature']  # -24.8 mix reported by meteofrance
    Tmax = 50 >= df['temperature']  # 40.1 max reported by meteofrance
    df['temperature'].where(Tmin & Tmax, inplace=True)
    hmin = 0 <= df['hygrometry']
    hmax = 100 >= df['hygrometry']  # Hygrometry: [0, 100]
    df['hygrometry'].where(hmin & hmax, inplace=True)
    wmin = 0 <= df['wind_speed_average']
    wmax = 49 >= df['wind_speed_average']  # 40 max reported by meteofrance
    df['wind_speed_average'].where(wmin & wmax, inplace=True)
    cmin = 250 <= df['co2']  # CO2: [250, 4000]
    cmax = 4000 >= df['co2']
    df['co2'].where(cmin & cmax, inplace=True)
    voltmin = 8 <= df['voltage']
    voltmax = 15 >= df['voltage']  # Voltage: [8, 15]
    df['voltage'].where(voltmin & voltmax, inplace=True)
    return df
def percentmissing(df):
    percentage_missing = df.isna().mean() * 100
    return percentage_missing
# definition station
def station_15min(station,dfrom,dto):
    df = importbasedata15(station, dfrom, dto)
    df = out_range(df)
    return df
# List of the stations: list of dataframes
def stations15(dfrom,dto):
    station_name = ['LRN', 'CharlesIII', 'GrandNancy', 'AvironClub', 'CollegeND', 'Aiguillage']
    lst = []
    for i in range(len(station_name)):
        lst.append(station_15min(station_name[i], dfrom, dto))
    return lst
# Quantification of UHI
def UHII(df, dfr):
    i = df['temperature'] - dfr['Tair']
    return i
# List of UHII
def dfUHII(dfrom,dto):
    uhi =[]
    dfr = ref(dfrom, dto)
    for i in range(len(stations15(dfrom,dto))):
        uhi.append(stations15(dfrom, dto)[i].temperature - dfr['Tair'])  # .to_frame(name='UHI')
    # Create a dataframe of UHI for each station
    d = {'Station_1': uhi[0], 'Station_3': uhi[1], 'Station_4': uhi[2], 'Station_5': uhi[3], 'Station_6': uhi[4],
         'Station_7': uhi[5]}
    dfUHI = pd.DataFrame(data=d)
    dfUHI = dfUHI.asfreq(freq='15min')
    return dfUHI



