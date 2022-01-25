# !python 
# encoding: UTF-8
import traceback

from selenium import webdriver

'''
webDrv
targetURL
'''
webDrv = '/usr/bin/safaridriver'
targetURL = 'https://shopping.naver.com/home/p/index.naver'

drv = webdriver.Safari(executable_path=webDrv)

try:
    print('test')

except Exception:
    traceback.print_exc()
