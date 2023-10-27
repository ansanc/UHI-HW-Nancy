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
import daydivision
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
def daily_graphs(dfrom,dto,day):

    # Establishing station of reference
    dfref = StationData.ref(dfrom, dto)
    # Importing station data in 15 min gap
    stations_15 = StationData.stations15(dfrom, dto)
    # Importing station data in 15 min gap
    stations_60 = StationData.stations60(dfrom, dto)
    # Importing UHI dataframe to divided in days
    dfUHI = StationData.dfUHII(dfrom,dto)
    # Separating my data in an specific date that I want to observe
    # ref station in day x
    dfref_date = daydivision.days(dfref)[day]
    # 15 min gap station information in x day
    stations_dayx_15min = []
    for i in range(len(stations_15)):
        stations_dayx_15min.append(daydivision.days(stations_15[i])[day])
    # 60 min gap station information in x day
    stations_dayx_60min = []
    for i in range(len(stations_60)):
        stations_dayx_60min.append(daydivision.days(stations_60[i])[day])

    # UHI information for each station in x dat
    UHI_dayx= []
    for i in range(len(dfUHI)):
        UHI_dayx.append(daydivision.days(dfUHI[i])[day])
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Compute Day events (sun): noon, sunrise, sunset
    # See https://rhodesmill.org/pyephem/tutorial.html
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

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    (ylim0, ylim1) = plt.gca().get_ylim()
    dfDayEvents = getDayEvents(dfref_date)
    # Radiation
    fig, ax1 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    fig.autofmt_xdate()
    #plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Day')
    if dfref['Solar_Radiation'].isnull().values.all() == True:
        for i in range(0, 6):
            ax1.plot(stations_dayx_15min.index, stations_dayx_15min[i].solar_radiation, label=station_name[i])
        ax1.set_ylabel(' Solar radiation (W/$m^2$)')
        ax1.grid()
        ax1.legend()
        ax1.set_title('Solar radiation at day' + str(day))
        # Plot lines for each daily events
        ax1.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')  # , label='Sunset')
        ax1.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')  # , label='Noon')
        ax1.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey',
                 ls='-.')  # , label='Sunrise')
        # Plot text labels of 'sunrise', 'noon' and 'sunset'
        ax1.text(dfDayEvents.sunrise[0], ylim1 * 0.9, 'Sunrise', ha='right', rotation=90, fontsize=14)
        ax1.text(dfDayEvents.noon[0], ylim1 * 0.9, 'Noon', ha='right', rotation=90, fontsize=14)
        ax1.text(dfDayEvents.sunset[0], ylim1 * 0.9, 'Sunset', ha='right', rotation=90, fontsize=14)
        plt.savefig('SolarRadiation_day' + str(day) + '.png')

    else:
        for i in range(len(stations_dayx_60min)):
            ax1.plot(stations_dayx_60min[i].index, stations_dayx_60min[i].solar_radiation, label=station_name[i])
        ax1.plot(dfref_date.index, dfref_date.Solar_Radiation, label=ref_file)
        ax1.set_ylabel(' Solar radiation (W/$m^2$)')
        ax1.grid()
        ax1.legend()
        ax1.set_title('Solar radiation at day' + str(day))
        # Plot lines for each daily events
        ax1.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')  # , label='Sunset')
        ax1.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')  # , label='Noon')
        ax1.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey', ls='-.')  # , label='Sunrise')
        # Plot text labels of 'sunrise', 'noon' and 'sunset'
        ax1.text(dfDayEvents.sunrise[0], ylim1 * 0.9, 'Sunrise', ha='right', rotation=90, fontsize=14)
        ax1.text(dfDayEvents.noon[0], ylim1 * 0.9, 'Noon', ha='right', rotation=90, fontsize=14)
        ax1.text(dfDayEvents.sunset[0], ylim1 * 0.9, 'Sunset', ha='right', rotation=90, fontsize=14)
        plt.savefig('SolarRadiation_day' + str(day)+'.png')

    # Rain
    if dfref_date['Rain'].isnull().values.all() == False:
        fig, ax2 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
        fig.set_size_inches(12.5, 5.5)
        fig.autofmt_xdate()
        #plt.xticks(fontname='DaxOT', rotation=45)
        plt.xlabel('Day')
        ax2.plot(dfref_date.index, dfref_date.Rain, label="Rain")
        ax2.set_ylabel('Rain (mm/h))')
        ax2.grid()
        #ax2.set_ylim(0, 27)
        ax2.legend()
        ax2.set_title('Rain in day' + str(day))
        fig.savefig('Rain_day' + str(day)+'.png')

    # Cloudiness
    if dfref_date['Nebulosity'].isnull().values.all() == False:
        fig, ax3 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
        fig.set_size_inches(12.5, 5.5)
        fig.autofmt_xdate()
        #plt.xticks(fontname='DaxOT', rotation=45)
        plt.xlabel('Day')
        ax3.plot(dfref_date.index, dfref_date.Nebulosity, label="Cloudiness")
        ax3.set_ylabel('Cloudiness(Octa))')
        ax3.grid()
        ax3.set_ylim(0, 8)
        ax3.legend()
        ax3.set_title('Cloudiness day' + str(day) )

        # Plot lines for each daily events
        ax3.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')  # , label='Sunset')
        ax3.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')  # , label='Noon')
        ax3.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey', ls='-.')  # , label='Sunrise')
        # Plot text labels of 'sunrise', 'noon' and 'sunset'
        ax3.text(dfDayEvents.sunrise[0], ylim1 * 0.9, 'Sunrise', ha='right', rotation=90, fontsize=14)
        ax3.text(dfDayEvents.noon[0], ylim1 * 0.9, 'Noon', ha='right', rotation=90, fontsize=14)
        ax3.text(dfDayEvents.sunset[0], ylim1 * 0.9, 'Sunset', ha='right', rotation=90, fontsize=14)
        fig.savefig('Cloudiness_day'+ str(day) +'.png')

    # Wind
    fig, ax4 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    fig.autofmt_xdate()
    #plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Hour')
    for i in range(len(stations_dayx_60min)):
        ax4.plot(stations_dayx_60min[i].index, stations_dayx_60min[i].wind_speed_average, label=station_name[i])
    ax4.plot(dfref_date.index, dfref_date.WindSpeed, label='MeteoCiel')
    ax4.set_ylabel('Wind speed (m/s))')
    ax4.grid()
    ax4.set_ylim(0, 15)
    ax4.legend()
    ax4.set_title('Average wind speed at day ' + str(day))
    # Plot lines for each daily events
    ax4.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')  # , label='Sunset')
    ax4.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')  # , label='Noon')
    ax4.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey', ls='-.')  # , label='Sunrise')
    # Plot text labels of 'sunrise', 'noon' and 'sunset'
    ax4.text(dfDayEvents.sunrise[0], ylim1 * 0.9, 'Sunrise', ha='right', rotation=90, fontsize=14)
    ax4.text(dfDayEvents.noon[0], ylim1 * 0.9, 'Noon', ha='right', rotation=90, fontsize=14)
    ax4.text(dfDayEvents.sunset[0], ylim1 * 0.9, 'Sunset', ha='right', rotation=90, fontsize=14)
    fig.savefig('Wind_day'+ str(day) +'.png')
    # Air temperature

    fig, ax5 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    #fig.autofmt_xdate()
    #plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Hour')
    for i in range(len(stations_dayx_60min)):
        ax5.plot(stations_dayx_60min[i].index, stations_dayx_60min[i].temperature, label=station_name[i])
    ax5.plot(dfref_date.index, dfref_date.Tair, label='MeteoCiel')
    ax5.set_ylabel('Temperature (°C)')
    ax5.grid()
    ax5.set_ylim(15, 45)
    ax5.legend()
    ax5.set_title('Air Temperature at day' + str(day))
    # Plot lines for each daily events
    ax5.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')  # , label='Sunset')
    ax5.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')  # , label='Noon')
    ax5.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey', ls='-.')  # , label='Sunrise')
    # Plot text labels of 'sunrise', 'noon' and 'sunset'
    ax5.text(dfDayEvents.sunrise[0], ylim1 * 0.9, 'Sunrise', ha='right', rotation=90, fontsize=14)
    ax5.text(dfDayEvents.noon[0], ylim1 * 0.9, 'Noon', ha='right', rotation=90, fontsize=14)
    ax5.text(dfDayEvents.sunset[0], ylim1 * 0.9, 'Sunset', ha='right', rotation=90, fontsize=14)
    fig.savefig('Temperature_day' + str(day) + '.png')

    # UHII
    fig, ax6 = plt.subplots()  # figsize=(11, 7),gridspec_kw={'height_ratios': [1, 1]} )
    fig.set_size_inches(12.5, 5.5)
    #fig.autofmt_xdate()
    #plt.xticks(fontname='DaxOT', rotation=45)
    plt.xlabel('Hour')
    for i in range(len(stations_dayx_60min)):
        ax6.plot(UHI_dayx[i], label=station_name[i])
    ax6.set_ylim(-4, 8)
    ax6.set_ylabel('$\Delta_{ur}$ T (°C)')
    ax6.grid()
    ax6.legend(loc='upper right')
    ax6.set_title('UHII at day'+ str(day))
    # Plot lines for each daily events
    ax6.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')  # , label='Sunset')
    ax6.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')  # , label='Noon')
    ax6.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey', ls='-.')  # , label='Sunrise')
    # Plot text labels of 'sunrise', 'noon' and 'sunset'
    ax6.text(dfDayEvents.sunrise[0], ylim1 * 0.9, 'Sunrise', ha='right', rotation=90, fontsize=14)
    ax6.text(dfDayEvents.noon[0], ylim1 * 0.9, 'Noon', ha='right', rotation=90, fontsize=14)
    ax6.text(dfDayEvents.sunset[0], ylim1 * 0.9, 'Sunset', ha='right', rotation=90, fontsize=14)
    fig.tight_layout()
    fig.savefig('UHI_day'+ str(day) +'.png')
