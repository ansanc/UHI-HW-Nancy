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
#import other functions
import StationData
# date time format
dateFMT = '%Y-%m-%d %H:%M:%S'
# Stations
ref_file = 'MeteoCiel'
rad_file = 'ref_radiation'
varref = ['utc', 'Tair', 'Rain', 'Nebulosity', 'WindSpeed', 'RH']
var = ['utc', 'legaltime', 'temperature', 'hygrometry', 'solar_radiation', 'wind_speed_min', 'wind_speed_max',
       'wind_speed_average', 'co2', 'voltage']
station_name = ['LRN', 'CharlesIII', 'GrandNancy', 'AvironClub', 'CollegeND', 'Aiguillage']

# main Function
def week_graphs(dfrom,dto):

    #reference station
    dfref = StationData.ref(dfrom, dto)
    stations_15 = StationData.stations15(dfrom, dto)
    # Radiation
    fig, ax1 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    fig.autofmt_xdate()
    plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    # cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    if dfref['solar_radiation'].isnull().values.all() == True:
        for i in range(len(stations_15)):
            ax1.plot(stations_15[i].index, stations_15[i].solar_radiation, label=station_name[i])
        ax1.set_ylabel(' Solar radiation (W/$m^2$)')
        ax1.grid()
        ax1.legend()
        ax1.set_title('Solar radiation')
        plt.savefig("SolarRadiation.png")
    else:
        for i in range(len(station_name)):
            ax1.plot(stations_15[i].index,stations_15[i].solar_radiation, label=station_name[i])
        ax1.plot(dfref.index, dfref.solar_radiation, label=ref_file)
        ax1.set_ylabel(' Solar radiation (W/$m^2$)')
        ax1.grid()
        ax1.legend()
        ax1.set_title('Solar radiation')
        fig.savefig("SolarRadiation.png")

    # Rain
    if dfref['Rain'].isnull().values.all() == False:
        fig, ax2 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
        fig.set_size_inches(12.5, 5.5)
        fig.autofmt_xdate()
        plt.xticks(fontname='DaxOT', rotation=45)
        plt.xlabel('Date')
        ax2.bar(dfref.index, dfref.Rain, label="Rain", width=0.05)
        ax2.set_ylabel('Rain (mm/h))')
        ax2.grid()
        #ax2.set_ylim(0, 27)
        ax2.legend()
        ax2.set_title('Rain')
        fig.savefig('Rain.png')

    # Cloudiness
    if dfref['Nebulosity'].isnull().values.all() == False:
        fig, ax3 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
        fig.set_size_inches(12.5, 5.5)
        fig.autofmt_xdate()
        plt.xticks(fontname='DaxOT', rotation=45)
        plt.xlabel('Date')
        ax3.plot(dfref.index, dfref.Nebulosity, label="Cloudiness")
        ax3.set_ylabel('Cloudiness(Octa))')
        ax3.grid()
        ax3.set_ylim(0, 8)
        ax3.legend()
        ax3.set_title('Cloudiness')
        fig.savefig('Cloudiness.png')

    # Wind
    fig, ax4 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    fig.autofmt_xdate()
    plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(len(station_name)):
        ax4.plot(stations_15[i].index, stations_15[i].wind_speed_average, label=station_name[i])
    ax4.plot(dfref.index, dfref.WindSpeed, label='MeteoCiel')
    ax4.set_ylabel('Wind speed (m/s))')
    ax4.grid()
    ax4.set_ylim(0, 10)
    ax4.legend()
    ax4.set_title('Average wind speed')
    fig.savefig('Wind.png')

    # Air temperature
    fig, ax5 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    #fig.autofmt_xdate()
    #plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(len(station_name)):
        ax5.plot(stations_15[i].index, stations_15[i].temperature, label=station_name[i])
    ax5.plot(dfref.index, dfref.Tair, label='MeteoCiel')
    ax5.set_ylabel('Temperature (°C)')
    ax5.grid()
    ax5.set_ylim(15, 45)
    ax5.legend()
    ax5.set_title('Air Temperature')
    fig.savefig('Temperature.png')

    # UHI

    fig, ax6 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    # fig.autofmt_xdate()
    # plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(len(station_name)):
        ax6.plot(StationData.UHII(stations_15[i],dfref), label=station_name[i])
    #ax6.set_ylim(-4, 8)
    ax6.set_ylabel('$\Delta_{ur}$ T (°C)')
    ax6.grid()
    ax6.legend(loc='upper right')
    ax6.set_title('UHII')
    fig.tight_layout()
    fig.savefig('UHI.png')
