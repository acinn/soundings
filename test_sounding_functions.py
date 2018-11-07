#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 11:29:29 2018

Tests for sounding download functions

@author: Zora Schirmeister
"""
import pandas as pd
import csv
import numpy as np
import datetime
from urllib.request import Request, urlopen

from sounding_functions_10 import create_url, from_day_time, check_todays_sounding, write_csvfile, create_dataframe, download_sounding

def test_create_url():
    d = create_url(station_id='11120', year='2018', month='09', from_date='1700', to_date='1712', region='europe')
    assert type(d) == str
    e = create_url(station_id=None, year=None, month=None, from_date=None, to_date=None, region=None)
    assert type(e) == str


def test_from_day_time():
    d = from_day_time()
    possible_hours = ['00','01', '02', '03', '04','05', '06', '07', '08', '09',
                      '10', '11', '12', '13', '14','15', '16', '17', '18', 
                      '19', '20', '21', '22', '23']
    possible_days = ['00','01', '02', '03', '04','05', '06', '07', '08', '09',
                      '10', '11', '12', '13', '14','15', '16', '17', '18', 
                      '19', '20', '21', '22', '23', '24', '25', '26', '27', 
                      '28', '29', '30', '31']
    assert type(d) == str
    assert len(d) == 4
    assert d[-2:] in possible_hours
    assert d[0:2] in possible_days
    day = '{:%d}'.format(datetime.datetime.now())
    yesterday = datetime.date.today() - datetime.timedelta(1)
    yesterday = yesterday.strftime('%d')
    assert d[0:2] == day or yesterday


def test_check_todays_sounding():
    lines = ['<HTML>',
 '<TITLE>University of Wyoming - Radiosonde Data</TITLE>',
 '<LINK REL="StyleSheet" HREF="/resources/select.css" TYPE="text/css">',
 '<BODY BGCOLOR="white">',
 '<H2>11120 LOWI Innsbruck-Flughafen Observations at 03Z 17 Sep 2018</H2>',
 '<PRE>',
 '-----------------------------------------------------------------------------',
 '   PRES   HGHT   TEMP   DWPT   RELH   MIXR   DRCT   SKNT   THTA   THTE   THTV',
 '    hPa     m      C      C      %    g/kg    deg   knot     K      K      K ',
 '-----------------------------------------------------------------------------',
 ' 1000.0    188                                                               ',
 '  956.0    593   15.8   14.8     94  11.19    280      4  292.7  324.7  294.7',
 '</PRE><H3>Station information and sounding indices</H3><PRE>']
    badlines = ['<HTML>',
 '<TITLE>University of Wyoming - Radiosonde Data</TITLE>',
 '<LINK REL="StyleSheet" HREF="/resources/select.css" TYPE="text/css">',
 '<BODY BGCOLOR="white">',
 '<P>Description of the ',
 '-----------------------------------------------------------------------------']
    d = check_todays_sounding(lines)
    e = check_todays_sounding(badlines)
    assert d == True
    assert e == False


def test_write_csvfile():
    lines = ['<HTML>',
 '<TITLE>University of Wyoming - Radiosonde Data</TITLE>',
 '<LINK REL="StyleSheet" HREF="/resources/select.css" TYPE="text/css">',
 '<BODY BGCOLOR="white">',
 '<H2>11120 LOWI Innsbruck-Flughafen Observations at 03Z 17 Sep 2018</H2>',
 '<PRE>',
 '-----------------------------------------------------------------------------',
 '   PRES   HGHT   TEMP   DWPT   RELH   MIXR   DRCT   SKNT   THTA   THTE   THTV',
 '    hPa     m      C      C      %    g/kg    deg   knot     K      K      K ',
 '-----------------------------------------------------------------------------',
 ' 1000.0    188                                                               ',
 '  956.0    593   15.8   14.8     94  11.19    280      4  292.7  324.7  294.7',
 '776.0 2277 4.2 0.9 79 5.29 331 6 298.2 314.1 299.1',
 '752.0 2533 5.0 -18.0 17 1.24 351 7 301.8 305.9 302.0',
 '700.0 3114 1.8 -9.2 44 2.73 35 8 304.4 313.2 304.9',
 '650.0 3706 -2.3 -9.8 56 2.81 15 11 306.3 315.4 306.8',
 '643.0 3792 -2.9 -9.9 59 2.82 8 11 306.6 315.7 307.1',
 '</PRE><H3>Station information and sounding indices</H3><PRE>']
    d = write_csvfile(lines)
    assert type(d[0]) == list
    assert type(d[1]) == list

def test_create_dataframe():
    d = create_dataframe()
    assert type(d) == pd.core.frame.DataFrame

def test_download_sounding():
    d = download_sounding()
    # station_id='11120', year='2018', month='09', from_date='1700', to_date='1712', region='europe'
    assert type(d) == pd.core.frame.DataFrame