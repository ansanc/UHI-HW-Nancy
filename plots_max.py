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
import maxx

# date time format
dateFMT = '%Y-%m-%d %H:%M:%S'
# Stations
ref_file = 'MeteoCiel'
rad_file = 'ref_radiation'
varref = ['utc', 'Tair', 'Rain', 'Nebulosity', 'WindSpeed', 'RH']
var = ['utc', 'legaltime', 'temperature', 'hygrometry', 'solar_radiation', 'wind_speed_min', 'wind_speed_max',
       'wind_speed_average', 'co2', 'voltage']
station_name = ['LRN', 'CharlesIII', 'GrandNancy', 'AvironClub', 'CollegeND', 'Aiguillage']

def max_plots(dfrom,dto):
    # Radiation
    fig, ax1 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    fig.autofmt_xdate()
    plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(0, 6):
        ax1.plot(maxx.max_rad(i, dfrom, dto), label=station_name[i])
    ax1.plot(maxx.maxRef_rad(dfrom, dto), label='MeteoCiel')
    ax1.set_ylabel(' Solar radiation (W/$m^2$)')
    ax1.grid()
    ax1.legend()
    ax1.set_title('Average 24h: Solar radiation')
    fig.savefig("SolarRadiation_max.png")

    # Air temperature
    fig, ax5 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    # fig.autofmt_xdate()
    # plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(0, 6):
        ax5.plot(maxx.max_T(i, dfrom, dto), label=station_name[i])
    ax5.plot(maxx.max_T(dfrom, dto), label='MeteoCiel')
    ax5.set_ylabel('Temperature (°C)')
    ax5.grid()
    #ax5.set_ylim(15, 45)
    ax5.legend()
    ax5.set_title('Average 24h: Air Temperature')
    fig.savefig('Temperature_max.png')

    # UHI
    fig, ax6 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    # fig.autofmt_xdate()
    # plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(0, 6):
        ax6.plot(maxx.max_uhi(i, dfrom, dto), label=station_name[i])
    #ax6.set_ylim(-4, 8)
    ax6.set_ylabel('$\Delta_{ur}$ T (°C)')
    ax6.grid()
    ax6.legend(loc='upper right')
    ax6.set_title('Average 24h: UHII')
    fig.tight_layout()
    fig.savefig('UHI_max.png')

def max_dayplots(dfrom,dto):

    # Air temperature
    fig, ax5 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    # fig.autofmt_xdate()
    # plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(0, 6):
        ax5.bar(maxx.max_T_day(i, dfrom, dto), label=station_name[i])
    ax5.bar(maxx.max_T_day(dfrom, dto), label='MeteoCiel')
    ax5.set_ylabel('Temperature (°C)')
    ax5.grid()
    #ax5.set_ylim(15, 45)
    ax5.legend()
    ax5.set_title('Average 24h: Air Temperature')
    fig.savefig('Temperature_max_day.png')

    # UHI
    fig, ax6 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    # fig.autofmt_xdate()
    # plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(0, 6):
        ax6.bar(maxx.max_uhi_day(i, dfrom, dto), label=station_name[i])
    #ax6.set_ylim(-4, 8)
    ax6.set_ylabel('$\Delta_{ur}$ T (°C)')
    ax6.grid()
    ax6.legend(loc='upper right')
    ax6.set_title('Average 24h: UHII')
    fig.tight_layout()
    fig.savefig('UHI_max_day.png')

