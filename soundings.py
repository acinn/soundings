#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sounding functions

@author: Zora
Created on Fri Oct 19 10:35:40 2018
"""

import pandas as pd
import csv
import datetime
import sys
from urllib.request import Request, urlopen


def create_url(station_id='11120', year=None, month=None, from_date=None,
               to_date=None, region='europe'):
    """Returns the url for the sounding data of the chosen date and location.

    Default: The last sounding at Innsbruck Airport.

    Parameters
    ----------
    station_id : str
        The id of the station.
    year : str
        A four character string indicating the year. Default: now
    month
    from_date
    to_date
    region

    Returns
    -------
    The url of the data homepage as string.
    """
    
    if year is None:
        year = '{:%Y}'.format(datetime.datetime.now())

    if month is None:
        month = '{:%m}'.format(datetime.datetime.now())
        
    if from_date is None:
        from_date = from_day_time()
                
    if to_date is None:
        to_date = '{:%d%H}'.format(datetime.datetime.now())

    return ('http://weather.uwyo.edu/cgi-bin/sounding?region=' + region +
            '&TYPE=TEXT%3ALIST&YEAR=' + year + '&MONTH=' + month + '&FROM=' +
            from_date + '&TO=' + to_date + '&STNM=' + station_id)


def from_day_time(station_id=None):
    """Used for create_url(). Returns the keyword argument for from_date if 
    it is set to None. Returns the day and hour of the last sounding 
    (for Innsbruck Airport: sounding in the last 24 hours, 
    all other stations: sounding in the last 12 hours).
    
    Returns
    -------
    a string of the format: ddhh.
    """
    hour_now = int('{:%H}'.format(datetime.datetime.now()))
    
    if station_id == None or station_id == '11120':
        # if there was a sounding today (and now is later than 3 a.m.) today is
        # chosen, else yesterday for the day (as the first sounding in
        # Innsbruck takes place at 3 o'clock)
        if hour_now >= 3:
            day = '{:%d}'.format(datetime.datetime.now())
        else:
            yesterday = datetime.date.today() - datetime.timedelta(1)
            day = yesterday.strftime('%d')
        # since there is only one sounding per day, hour con be set to '00'
        hour = '00'
    else:
        # at different stations, there are 2 soundings per day
        hour_start = hour_now - 12
        if hour_start < 0:
            hour_start += 24
            yesterday = datetime.date.today() - datetime.timedelta(1)
            day = yesterday.strftime('%d')
        else:
            day = '{:%d}'.format(datetime.datetime.now())
        hour = str(hour_start)
        
    # check if digit number is right (two digits)    
    if len(day) < 2:
        day = '0' + day
    if len(hour) < 2:
        hour = '0' + hour
        
    from_date = day + hour
    return from_date


def check_todays_sounding(lines):
    """ Checks if there is data of the current sounding available. If not an 
    an advice is given.
    
    Parameters:
    -----------
    lines:  string
            data downloaded and split into rows like in table
            
    Returns:
    --------
    boolean: if False: The data file does not have data of a sounding.
                       comment: that says that there is not data of the last 
                       sounding available.
             if True: Data of the last sounding or chosen date is available.
    """
    # If there is not available data the 5th line in the downloaded stuff will 
    # be '<P>Description of the ', this is tested.
    bad_text = '<P>Description of the '
    if lines[4] == bad_text:
        text = 'Sorry, there is no data of this sounding available. You '\
             'can try to downlaod the data of a different sounding (e.g. '\
             'yesterday). For example fill in the keyword arguments as it is'\
             ' described in the following:\ndownload_sounding(year=\'2018\','\
             'month=\'10\', from_date=\'1703\', to_date=\'1704\') \n'\
             'That will download the data of the 17th of October 2018 for '\
             'the first sounding which took place at 03 o\'clock at Innsbruck'\
             ' Airport.'
        print(text)
        return False
    else:
        return True


def write_csvfile(data):
    """Preprocesses the downloaded data and writes it in a csv-file called 
    'rawdata.csv'. First only rows with data for the table are selected. Rows
    which do not contain all parameters are deleted. Then the csv-file will be 
    created.
    
    Parameters
    ----------
    data : list
            downloaded data, already separated in rows in a list
    
    Returns
    -------
    a csv-file called rawdata.csv, which contains a table of the sounding
    data.
    """
    # find the first row of interest, which is the head of the table
    for element in data:
        if element == '-----------------------------------------------------------------------------':
            cut1 = 4 + data.index(element)
            break    
    
    # find the first row which does not contain data of the table
    for element in data:
        if element == '</PRE><H3>Station information and sounding indices</H3><PRE>':
            cut2 = data.index(element)
            break

    # cut the table from the string and delete the 2. row which only contains 
    # '----'
    cut = data[cut1:cut2]
    del cut[2]
    
    # save the string as a list, with each row being a list with elements for 
    # each entry in a row of the table
    pretable = []
    for element in cut:
        a = element.split()
        pretable.append(a)
    
    # remove rows which do not contain entries for all columns
    for element in pretable:
        if len(element) < 11:
            pretable.remove(element)

    # create a csv-file called rawdata.csv which contains the table
    with open('rawdata.csv', mode='w') as file:
        csv_writer = csv.writer(file, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for line in pretable:
            csv_writer.writerow(line)
            
    return cut, pretable


def create_dataframe():
    """Creates a pandas dataframe from the data saved in 'rawdata.csv'.
    
    Returns
    -------
    pandas dataframe
    """
    col_names = ['pres', 'hght', 'temp', 'dwpt', 'relh', 'mixr', 'drct',
                 'speed', 'thta', 'thte', 'thtv']

    df = pd.read_csv('rawdata.csv', sep=' ', names=col_names)
    
    return df


def download_sounding(station_id='11120', year=None, month=None, from_date=None,
                      to_date=None, region='europe'):
    """Returns a dataframe with the data of the last sounding at 
    Innsbruck-Flughafen, (or when selected, of a specific sounding at a 
    specific location).
    
    
    Parameters
    ----------
    station_id: string
            ID of the station: e.g. Innsbruck-Flughafen (default): 11120
            
    year: string
            Format: four-digit number (e.g. 2018)
            Default: None returns the current year.

            
    month: string
            Format: two-digit number (e.g. 01, 02, 03, ... 12)
            Default: None returns the current month.
            
    from_date: string
            (Builds a time period with to_date in which the sounding took
            place. The ealiest sounding in the period will be chosen.)
            day and hour of the sounding of interest is needed
            best: dd00 for 00:00 as start time
            default: None returns the last sounding
            Format: ddhh
                
    to_date: string
            End of time period in which sounding took place.
            hour of the end of period of interest is needed:
            e.g. dd12 for until 12 o'clock
            default: None returns the last sounding
            Format: ddhh
    
    region: string
            default: europe
            other regions are possible, but not implemented yet
            Format: lowercase letters
    
    Returns
    -------
    a pandas dataframe with the sounding data and the link to the homepage of 
    the sounding.
    """

    url = create_url(station_id=station_id, year=year, month=month,
                     from_date=from_date, to_date=to_date, region=region)
    
    req = urlopen(Request(url)).read()
    data = req.decode('utf-8')

    # separate the string into rows, each row is an element in a list
    data = data.split('\n')
    
    # check if the data is available 
    datacheck = check_todays_sounding(data)
    if datacheck == False:
            # when there is no data, only a message and en exception appears
            sys.exit()
        
    write_csvfile(data)
    df = create_dataframe()
    print('On this homepage you can find the data:\n' + url)

    return df
