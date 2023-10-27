#####
# Angy Sanchez
#Importing libraries
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
import Averageday

# Main general data

# date time format
dateFMT = '%Y-%m-%d %H:%M:%S'
# Stations
ref_file = 'MeteoCiel'
varref = ['utc', 'Tair', 'Rain', 'Nebulosity', 'WindSpeed', 'RH']
var = ['utc', 'legaltime', 'temperature', 'hygrometry', 'solar_radiation', 'wind_speed_min', 'wind_speed_max',
       'wind_speed_average', 'co2', 'voltage']
station_name = ['LRN', 'CharlesIII', 'GrandNancy', 'AvironClub', 'CollegeND', 'Aiguillage']

# Colors depending of the stations
# LRN = blue
# Charles III = green
# GrandNancy = pink
# AvironClub = brown
# CollegeND = purple
# Aiguillaje = red
# MeteoCiel = magenta
def getDayEvents(df):
    Tomblaine = ephem.Observer()
    # Coordonnées GPS du Labo : 48.688, 6.22, elev = 200m
    Tomblaine.lat = '48.688'
    Tomblaine.lon = '6.22'
    Tomblaine.elevation = 200
    sun = ephem.Sun()

    # New list declarations
    sunrise_hour = []
    sunset_hour = []
    noon_hour = []

    date = df.index  # Get the date/hour from the dafatrame index
    date = date.strftime('%Y-%m-%d').tolist()  # Only extract the date
    date = list(dict.fromkeys(date))  # Remove duplicate dates

    for d in date:
        Tomblaine.date = d
        # Get the sunrise, sunset and noon (in the Ephem.Date format)
        sunrise = Tomblaine.next_rising(sun)
        sunset = Tomblaine.next_setting(sun)
        noon = Tomblaine.next_transit(sun)

        # Convert to datetime and append them to a list
        sunrise_hour.append(sunrise.datetime())
        noon_hour.append(noon.datetime())
        sunset_hour.append(sunset.datetime())

    # Create and return a DataFrame
    dfEvents = pd.DataFrame(index=date, data={'sunrise': sunrise_hour, 'noon': noon_hour, 'sunset': sunset_hour})
    return dfEvents

# main Function
def average_plot(dfrom,dto):
    dfDayEvents =getDayEvents(daydivision.days(StationData.ref(dfrom,dto))[0])
    # Radiation
    fig, ax1 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    fig.autofmt_xdate()
    plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(0, 6):
        ax1.plot(Averageday.average15_24h_radiation(i, dfrom, dto), label=station_name[i])
    ax1.plot(Averageday.averageRef_24h_radiation(dfrom, dto), label='MeteoCiel')
    ax1.set_ylabel(' Solar radiation (W/$m^2$)')
    # get the Y limits of the figure
    (ylim0, ylim1) = plt.gca().get_ylim()
    # Plot lines for each daily events
    ax1.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')  # , label='Sunset')
    ax1.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')  # , label='Noon')
    ax1.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey', ls='-.')  # , label='Sunrise')
    # plt.grid()
    # Plot text labels of 'sunrise', 'noon' and 'sunset'
    ax1.text(dfDayEvents.sunrise, ylim1 * 0.9, 'Sunrise -' + ' 03:33', ha='right', rotation=90, fontsize=14)
    ax1.text(dfDayEvents.noon, ylim1 * 0.9, 'Noon -' + ' 11:38', ha='right', rotation=90, fontsize=14)
    ax1.text(dfDayEvents.sunset, ylim1 * 0.9, 'Sunset - ' + ' 19:42', ha='right', rotation=90, fontsize=14)
    ax1.grid()
    ax1.legend()
    ax1.set_title('Average 24h: Solar radiation')
    fig.savefig("SolarRadiation_average.png")

    # Wind
    fig, ax4 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    fig.autofmt_xdate()
    plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(0, 6):
        ax4.plot(Averageday.average15_24h_wind(i, dfrom, dto), label=station_name[i])
    ax4.plot(Averageday.averageRef_24h_wind(dfrom, dto), label='MeteoCiel')
    ax4.set_ylabel('Wind speed (m/s))')
    # get the Y limits of the figure
    (ylim0, ylim1) = plt.gca().get_ylim()
    # Plot lines for each daily events
    plt.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')  # , label='Sunset')
    plt.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')  # , label='Noon')
    plt.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey', ls='-.')  # , label='Sunrise')
    # plt.grid()
    # Plot text labels of 'sunrise', 'noon' and 'sunset'
    ax4.text(dfDayEvents.sunrise, ylim1 * 0.9, 'Sunrise -' + ' 03:33', ha='right', rotation=90, fontsize=14)
    ax4.text(dfDayEvents.noon, ylim1 * 0.9, 'Noon -' + ' 11:38', ha='right', rotation=90, fontsize=14)
    ax4.text(dfDayEvents.sunset, ylim1 * 0.9, 'Sunset - ' + ' 19:42', ha='right', rotation=90, fontsize=14)
    ax4.grid()
    ax4.set_ylim(0, 10)
    ax4.legend()
    ax4.set_title('Average 24h: Mean wind speed')
    fig.savefig('Wind_average.png')


    # Air temperature
    fig, ax5 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    # fig.autofmt_xdate()
    # plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(0, 6):
        ax5.plot(Averageday.average15_24h_temperature(i, dfrom, dto), label=station_name[i])
    ax5.plot(Averageday.averageRef_24h_temperature(dfrom, dto), label='MeteoCiel')
    # get the Y limits of the figure
    (ylim0, ylim1) = plt.gca().get_ylim()
    # Plot lines for each daily events
    plt.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')  # , label='Sunset')
    plt.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')  # , label='Noon')
    plt.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey', ls='-.')  # , label='Sunrise')
    # plt.grid()
    # Plot text labels of 'sunrise', 'noon' and 'sunset'
    ax5.text(dfDayEvents.sunrise, ylim1 * 0.9, 'Sunrise -' + ' 03:33', ha='right', rotation=90, fontsize=14)
    ax5.text(dfDayEvents.noon, ylim1 * 0.9, 'Noon -' + ' 11:38', ha='right', rotation=90, fontsize=14)
    ax5.text(dfDayEvents.sunset, ylim1 * 0.9, 'Sunset - ' + ' 19:42', ha='right', rotation=90, fontsize=14)
    ax5.set_ylabel('Temperature (°C)')
    ax5.grid()
    ax5.set_ylim(15, 45)
    ax5.legend()
    ax5.set_title('Average 24h: Air Temperature')
    fig.savefig('Temperature_average.png')

    # UHI

    fig, ax6 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    # fig.autofmt_xdate()
    # plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(0, 6):
        ax6.plot(Averageday.meanUHI_24h(i, dfrom, dto), label=station_name[i])
    #ax6.set_ylim(-4, 8)
    ax6.set_ylabel('$\Delta_{ur}$ T (°C)')
    # get the Y limits of the figure
    (ylim0, ylim1) = plt.gca().get_ylim()
    # Plot lines for each daily events
    plt.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')  # , label='Sunset')
    plt.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')  # , label='Noon')
    plt.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey', ls='-.')  # , label='Sunrise')
    # plt.grid()
    # Plot text labels of 'sunrise', 'noon' and 'sunset'
    ax6.text(dfDayEvents.sunrise, ylim1 * 0.9, 'Sunrise -' + ' 03:33', ha='right', rotation=90, fontsize=14)
    ax6.text(dfDayEvents.noon, ylim1 * 0.9, 'Noon -' + ' 11:38', ha='right', rotation=90, fontsize=14)
    ax6.text(dfDayEvents.sunset, ylim1 * 0.9, 'Sunset - ' + ' 19:42', ha='right', rotation=90, fontsize=14)
    ax6.grid()
    ax6.legend(loc='upper right')
    ax6.set_title('Average 24h: UHII')
    fig.tight_layout()
    fig.savefig('UHI_average.png')

def averageDay_plot(dfrom,dto):
    dfDayEvents =getDayEvents(daydivision.days(StationData.ref(dfrom,dto))[0])
    # Wind
    fig, ax4 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    fig.autofmt_xdate()
    plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(0, 6):
        ax4.plot(Averageday.average15_day_wind(i, dfrom, dto), label=station_name[i])
    ax4.plot(Averageday.averageRef_day_wind(dfrom, dto), label='MeteoCiel')
    ax4.set_ylabel('Wind speed (m/s))')
    # get the Y limits of the figure
    (ylim0, ylim1) = plt.gca().get_ylim()
    # Plot lines for each daily events
    plt.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')  # , label='Sunset')
    plt.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')  # , label='Noon')
    plt.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey', ls='-.')  # , label='Sunrise')
    # plt.grid()
    # Plot text labels of 'sunrise', 'noon' and 'sunset'
    ax4.text(dfDayEvents.sunrise, ylim1 * 0.9, 'Sunrise -' + ' 03:33', ha='right', rotation=90, fontsize=14)
    ax4.text(dfDayEvents.noon, ylim1 * 0.9, 'Noon -' + ' 11:38', ha='right', rotation=90, fontsize=14)
    ax4.text(dfDayEvents.sunset, ylim1 * 0.9, 'Sunset - ' + ' 19:42', ha='right', rotation=90, fontsize=14)
    ax4.grid()
    #ax4.set_ylim(0, 10)
    ax4.legend()
    ax4.set_title('Average Day: Mean wind speed')
    fig.savefig('Wind_average_day.png')
    # UHI

    fig, ax6 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    # fig.autofmt_xdate()
    # plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(len(station_name)):
        ax6.plot(Averageday.meanUHI_day(i, dfrom, dto), label=station_name[i])
    #ax6.set_ylim(-4, 8)
    # get the Y limits of the figure
    (ylim0, ylim1) = plt.gca().get_ylim()
    # Plot lines for each daily events
    plt.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')  # , label='Sunset')
    plt.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')  # , label='Noon')
    plt.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey', ls='-.')  # , label='Sunrise')
    # plt.grid()
    # Plot text labels of 'sunrise', 'noon' and 'sunset'
    ax6.text(dfDayEvents.sunrise, ylim1 * 0.9, 'Sunrise -' + ' 03:33', ha='right', rotation=90, fontsize=14)
    ax6.text(dfDayEvents.noon, ylim1 * 0.9, 'Noon -' + ' 11:38', ha='right', rotation=90, fontsize=14)
    ax6.text(dfDayEvents.sunset, ylim1 * 0.9, 'Sunset - ' + ' 19:42', ha='right', rotation=90, fontsize=14)
    ax6.set_ylabel('$\Delta_{ur}$ T (°C)')
    ax6.grid()
    ax6.legend(loc='upper right')
    ax6.set_title('Average day: UHII')
    fig.tight_layout()
    fig.savefig('UHI_average_day.png')

def averageNight_plot(dfrom,dto):

    # Wind
    fig, ax4 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    fig.autofmt_xdate()
    plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(0, 6):
        ax4.plot(Averageday.average15_night_wind(i, dfrom, dto), label=station_name[i])
    ax4.plot(Averageday.averageRef_night_wind(dfrom, dto), label='MeteoCiel')
    ax4.set_ylabel('Wind speed (m/s))')
    ax4.grid()
    #ax4.set_ylim(0, 10)
    ax4.legend()
    ax4.set_title('Average night: Mean wind speed')
    fig.savefig('Wind_average_night.png')

    # UHI

    fig, ax6 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    # fig.autofmt_xdate()
    # plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Date')
    for i in range(0, 6):
        ax6.plot(Averageday.meanUHI_night(i, dfrom, dto), label=station_name[i])
    #ax6.set_ylim(-4, 8)
    ax6.set_ylabel('$\Delta_{ur}$ T (°C)')
    ax6.grid()
    ax6.legend(loc='upper right')
    ax6.set_title('Average night: UHII')
    fig.tight_layout()
    fig.savefig('UHI_average_night.png')