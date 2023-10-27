#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import ephem
from datetime import timedelta

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Read the data from the 'data-meteo' directory. skip the tow with the units
dfLRN = pd.read_csv( 'LRN.csv', skiprows=[1] )
dfLRN.index = pd.to_datetime(dfLRN['utc'], format='%Y-%m-%d %H:%M:%S')

dfGN = pd.read_csv( 'GrandNancy.csv', skiprows=[1] )
dfGN.index = pd.to_datetime(dfGN['utc'], format='%Y-%m-%d %H:%M:%S')

dfMC = pd.read_csv('MeteoCiel.csv', skiprows=[1] )
dfMC.index = pd.to_datetime(dfMC['utc'], format='%Y-%m-%d %H:%M:%S')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Filtering the datetime to get DataFrame only from 'dateFrom' to 'dateTo'
#dateFrom = "2019-06-23 00:00:00"; dateTo = "2019-06-29 23:59:59" # June Heatwave
dateFrom = "2019-07-23 00:00:00"; dateTo = "2019-07-23 23:59:59" # July Heatwave

dfLRN = dfLRN[ dateFrom : dateTo ]
dfGN = dfGN[ dateFrom : dateTo ]
dfMC = dfMC[ dateFrom : dateTo ]
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Compute Day events (sun): noon, sunrise, sunset
# See https://rhodesmill.org/pyephem/tutorial.html
def getDayEvents(df):
    Tomblaine=ephem.Observer()
    # Coordonnées GPS du Labo : 48.688, 6.22, elev = 200m
    Tomblaine.lat='48.688'  
    Tomblaine.lon='6.22'
    Tomblaine.elevation = 200     
    sun = ephem.Sun()
    
    # New list declarations
    sunrise_hour = []
    sunset_hour = []
    noon_hour = []
    
    date = df.index                             # Get the date/hour from the dafatrame index
    date = date.strftime( '%Y-%m-%d' ).tolist() # Only extract the date
    date = list ( dict.fromkeys( date ) )       # Remove duplicate dates
    
    for d in date:
        Tomblaine.date = d
        # Get the sunrise, sunset and noon (in the Ephem.Date format)
        sunrise = Tomblaine.next_rising(sun) 
        sunset = Tomblaine.next_setting(sun)
        noon = Tomblaine.next_transit(sun)
        
        # Convert to datetime and append them to a list      
        sunrise_hour.append( sunrise.datetime() )
        noon_hour.append( noon.datetime() )
        sunset_hour.append( sunset.datetime() )
    
    # Create and return a DataFrame
    dfEvents = pd.DataFrame( index=date, data={'sunrise':sunrise_hour, 'noon':noon_hour, 'sunset':sunset_hour} )
    return dfEvents
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    

dfDayEvents = getDayEvents(dfLRN)

fig = plt.figure(figsize=(9,6))
fig.autofmt_xdate()
plt.xticks(fontname = 'DaxOT', rotation=45 )
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')

# Plot the temperature of the LRN Station and the MeteoCiel Station
plt.plot(dfLRN.index, dfLRN.temperature, label='LRN data')
plt.plot(dfGN.index, dfGN.temperature, label='GN data')
plt.plot(dfMC.index, dfMC.Tair, label='MeteoCiel data')

# get the Y limits of the figure
(ylim0, ylim1) =  plt.gca().get_ylim()

# Plot lines for each daily events
plt.plot([dfDayEvents.sunset, dfDayEvents.sunset], [ylim0, ylim1], color='grey', ls='-')#, label='Sunset')
plt.plot([dfDayEvents.noon, dfDayEvents.noon], [ylim0, ylim1], ls='--', color='grey')#, label='Noon')
plt.plot([dfDayEvents.sunrise, dfDayEvents.sunrise], [ylim0, ylim1], color='grey', ls='-.')#, label='Sunrise')
#plt.grid()

# Plot text labels of 'sunrise', 'noon' and 'sunset'
plt.text( dfDayEvents.sunrise[0], ylim1*0.9, 'Sunrise', ha='right', rotation=90, fontsize=14)
plt.text( dfDayEvents.noon[0], ylim1*0.9, 'Noon', ha='right', rotation=90, fontsize=14)
plt.text( dfDayEvents.sunset[0], ylim1*0.9, 'Sunset', ha='right', rotation=90, fontsize=14)
plt.legend()
plt.tight_layout()
plt.show()
