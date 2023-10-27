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
import Weekgraphs
import StationData
# import Daygraph
import daydivision
import Averageday
import plots_average
import hw2
import maxx
# import average
# Main function
def main():

    # station_name =['LRN', 'Pepiniere', 'CharlesIII', 'GrandNancy', 'AvironClub', 'CollegeND', 'Aiguillage']
    # Function for asking the station and date wanted
    print("Hello, please make sure that all the data files are in the same folder as all the files of this program")
    # 2015 : (1) 2015-06-30 00:00:00 - 2015-07-07 23:45:00
    #        (2) 2015-07-15 00:00:00 - 2015-07-22 23:45:00
    # 2016 :     2016-06-23 00:00:00 - 2016-06-27 23:45:00
    # 2017 : (1) 2017-06-18 00:00:00 - 2017-06-22 23:45:00
    #        (2) 2017-07-05 00:00:00 - 2017-07-06 23:45:00
    #        (3) 2017-08-26 00:00:00 - 2017-08-29 23:45:00
    # 2018 :     2018-07-24 00:00:00 - 2018-08-08 23:45:00
    # 2019 : (1) 2019-06-25 00:00:00 - 2019-06-30 23:45:00
    #        (2) 2019-07-21 00:00:00 - 2019-07-26 23:45:00
    date_from = input("Please enter the date FROM in the next format Y-m-d H:M:S: ")
    date_to = input('Please enter the date TO in the next format Y-m-d H:M:S: ')

    Weekgraphs.week_graphs(date_from,date_to)
    # SecondHeatwave average plots
    #hw2.average_plot(date_from,date_to)
    #hw2.averageDay_plot(date_from,date_to)
    #hw2.averageNight_plot(date_from,date_to)
    #First heatwave average plots
    #plots_average.average_plot(date_from,date_to)
    plots_average.averageDay_plot(date_from,date_to)
    plots_average.averageNight_plot(date_from,date_to)
    #print(maxx.maxUHI_24h(date_from,date_to))
    #print(maxx.maxUHI_day(date_from, date_to))
    #print(maxx.maxUHI_night(date_from,date_to))
    # for i in range(len(daydivision.days(StationData.ref(date_from, date_to)))):
    #    Daygraph.daily_graphs(date_from,date_to,i)
    # dfaverage = averageday(df)
    # return df

if __name__ == '__main__':
    main()
