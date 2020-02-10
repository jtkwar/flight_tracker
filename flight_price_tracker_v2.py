# -*- coding: utf-8 -*-
"""
Jeffrey Kwarsick, Ph.D.
January 2020

Python Script to scrap Google Flights
And find the cheapest flights to a region of specific city
SFO to Europe Area

Project Guided from Python Machine Learning Blueprints
by Alexander Combs and Michael Roman
packt.com
"""


# import the relevant libraries for the task
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ability to scrap the webpage and access chrome automatically
from bs4 import BeautifulSoup
from selenium import webdriver

import re
import requests
import scipy
from PyAstronomy import pyasl
from datetime import date, timedelta, datetime
import time
from time import sleep
import schedule

import smtplib

def check_flights(dest, dept, rtn):
    # replace the path for the web driver
    # might need to download a more updated version of the chromedriver
    chrome_path = 'C:\\Users\\stark\\Downloads\\chromedriver'
    browser     = webdriver.Chrome(chrome_path)
    
    #start_date = dept
    #rtn_date   = rtn
    
    # initialize lists to store retrieved information
    dept_date, rtn_date, destination, price, stops, flttime = [], [], [], [], [], []
    
    start_sat_date = datetime.strptime(dept, '%Y-%m-%d')
    end_sat_date = datetime.strptime(rtn, '%Y-%m-%d')
    
    for i in range(60):
        sat_start = str(start_sat_date).split()[0]
        sat_end   = str(end_sat_date).split()[0]
        satz = "https://www.google.com/flights#f=0&flt=/m/0d6lp.r/m/02j9z." + sat_start + "*r/m/02j9z./m/0d6lp." + sat_end + ";c:USD;e:1;sd:1;t:e"
    
        #print(satz)
        browser.get(satz)
        # have the programl sleep for random time
        sleep(np.random.randint(3,7))
        # call BeautifulSoup to extract the data from the html webpage
        soupit = BeautifulSoup(browser.page_source, "html5lib")
        cardz = soupit.select('div[class*=tsAU4e ]')
        #print(len(cardz))
        for card in cardz:
            # Extract the data and appends to a list
            # Destination
            # Price of the Flight
            # Number of Stops
            # Duration of the Flight
            dest = card.select('h3[class*="W6bZuc YMlIz"]')[0].text
            prc  = card.select('div[class*=MJg7fb]')[0].text
            stp = card.select('span[class*=nx0jzf]')[0].text
            flt = card.select('span[class*=Xq1DAb]')[0].text
            destination.append(dest)
            price.append(prc)
            # append the departure and return dates
            dept_date.append(start_sat_date.strftime('%Y-%m-%d'))
            rtn_date.append(end_sat_date.strftime('%Y-%m-%d'))
            stops.append(stp)
            flttime.append(flt)
        
    
        # update the departure and return dates
        start_sat_date = start_sat_date + timedelta(days=4)
        end_sat_date   = end_sat_date + timedelta(days=4)
    
    # regex for grabbing number of stops
    re_stops = r'[0-9]{1}'
    
    # processing of the data to remove ','
    # 'Great Value'
    # '$'-sign
    prices = [price[i].replace(',', '') for i in range(len(price))]
    prices1 = [prices[i].replace('Great value', '') for i in range(len(prices))]
    prices2 = [int(prices1[i].replace('$', '')) for i in range(len(prices))]
    stops1 =  [re.findall(re_stops, stops[i]) for i in range(len(stops))]
    stops_flat = [item for sublist in stops1 for item in sublist]
    df_flts = pd.DataFrame(list(zip(dept_date, rtn_date, destination, prices2, stops_flat, flttime)), columns =['DepartureDate', 'ReturnDate', 'Destination', 'PriceUSD', 'Stops', 'TravelTime'])
    
    my_city = dest
    # sub-select dataframe for destination of interest
    temp = df_flts.query("Destination=='{0}'".format(my_city))
    
    # generalizedESD for outlier determination
    r = pyasl.generalizedESD(temp['PriceUSD'], 3, 0.025, fullOutput=True)
    print('Total Outliers:', r[0])
    out_dates = []
    for i in sorted(r[1]):
        out_dates.append(temp['DepartureDate'][i])
        print(out_dates)
        print('       R      Lambda')
    for i in range(len(r[2])):
        print('%2d %8.5f %8.5f' % ((i+1), r[2][i], r[3][i]))
    
    # find the minimum price of the dataframe
    my_min = min(temp['PriceUSD'])
    # subselect destination dataframe with minimum price
    df_lowest = temp.query("PriceUSD=='{0}'".format(my_min))
    # save all instances of the cheap flight to a list of strings
    my_strings = []
    for i in range(len(df_lowest)):
        ugh = "To " + dest + " on " + df_lowest['DepartureDate'].iloc[i] + " for $" + str(df_lowest['PriceUSD'].iloc[i])
        my_strings.append(ugh)
    # concentate strings together to send as text message
    new = '\n'.join(my_strings)
    
    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)
    
    # log into server with credentials
    server.starttls()
    server.login( 'Your Email', "Your Password" )
    
    # save the message
    message = "ALERT!!! To " + dest + "\n" + new

    # Send text message through SMS gateway of destination number
    server.sendmail( 'Flight Updater', '##########@mms.att.net', message)
    
# set up the scheduler to run our code every 60 min
schedule.every(60).minutes.do(check_flights('London', '2020-03-01', '2020-03-08'))
while 1:
    schedule.run_pending()
    sleep(1)
    
    
        
    
    