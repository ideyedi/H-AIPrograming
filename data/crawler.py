# !python 
# encoding: UTF-8
import time
import traceback
import os
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

'''
webDrv
targetURL
'''
webDrv = '/usr/bin/safaridriver'
targetURL = 'https://shopping.naver.com/home/p/index.naver'

#opt = webdriver.SafariOptions()
#opt.add_argument('--incognito')

drv = webdriver.Safari(executable_path=webDrv)

try:
    drv.get(targetURL)

except:
    traceback.print_exc()

