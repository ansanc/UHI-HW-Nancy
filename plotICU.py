#!/usr/bin/python3
# 
# Resampling file without modyfing data value
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

dfLRN = pd.read_csv( 'LRN.csv', skiprows=[1] )
dfLRN.index = pd.to_datetime(dfLRN['utc'], format='%Y-%m-%d %H:%M:%S')

dfGrandNancy = pd.read_csv( 'GrandNancy.csv', skiprows=[1] )
dfGrandNancy.index = pd.to_datetime(dfGrandNancy['utc'], format='%Y-%m-%d %H:%M:%S')

dfMC = pd.read_csv('MeteoCiel.csv', skiprows=[1] )
dfMC.index = pd.to_datetime(dfMC['utc'], format='%Y-%m-%d %H:%M:%S')

# Data Filtering between 2 dates
dateFrom = "2019-07-23 00:00:00"; dateTo = "2019-07-29 05:00:00" # July Heatwave
dateFrom = "2019-06-23 00:00:00"; dateTo = "2019-06-29 05:00:00" # June Heatwave
dfLRN = dfLRN[dateFrom:dateTo]
dfMC = dfMC[dateFrom:dateTo]

# Set the frequency of the data to every hour.
# NOW, THE DATA ARE HOURLY DATA !
dfLRN = dfLRN.asfreq(freq='60min')

dfLRN['ICU_LRN'] = dfMC['Tair'] - dfLRN['temperature']
dfLRN['ICU_GN'] = dfMC['Tair'] - dfGrandNancy['temperature']
fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(12, 8),gridspec_kw={'height_ratios': [1, 1]} )

fig.autofmt_xdate()
plt.xticks(fontname = 'DaxOT', rotation=45 )
ax1.set_ylabel('Temperature (°C)')
ax1.plot(dfLRN.index, dfLRN.temperature, label='LRN data')
ax1.plot(dfMC.index, dfMC.Tair, label='MeteoCiel data')
ax1.grid()

ax2.set_ylabel(r'$\Delta_{ur}$ T (°C)')
ax2.plot(dfLRN.index, dfLRN.ICU_LRN, label='LRN data', color='green' )
ax2.plot(dfLRN.index, dfLRN.ICU_GN, label='GN data', color='purple')
ax2.grid()
ax1.legend()
plt.tight_layout()
plt.show()
