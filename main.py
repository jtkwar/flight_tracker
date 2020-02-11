# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 14:58:38 2020

@author: stark
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
import os


__author__ = "Jeffrey Kwarsick, Ph.D."
__version__ = "0.1.0"
__license__ = "MIT"

os.chdir('C:\\Users\\stark\\Desktop')
from flight_price_tracker.py import check_flights

def main():
    check_flights('London', '2020-03-01', '2020-03-08')    
    # set up the scheduler to run our code every 60 min
    schedule.every(60).minutes.do(check_flights('London', '2020-03-01', '2020-03-08'))
    while 1:
        schedule.run_pending()
        sleep(1)
        
if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()

