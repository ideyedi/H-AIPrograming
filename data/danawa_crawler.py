# !python 
# encoding: UTF-8
import time
import traceback
import os
import csv
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

'''
webDrv
targetURL
'''
webDrv = '/usr/bin/safaridriver'
targetURL = 'http://www.danawa.com'
#opt = webdriver.SafariOptions()
#opt.add_argument('--incognito')

drv = webdriver.Safari(executable_path=webDrv)
herf_list = []

try:
    today = date.today()
    print('Today {}'.format(today))
    
    drv.get(targetURL)
    category = drv.find_elements(By.CLASS_NAME, 'btn_cate_all')
    category[0].click()

    # Sleep click event
    time.sleep(3)
    detail_list = drv.find_elements(By.CLASS_NAME, 'category-all__detail__list')
    print('parsing category list : {}'.format(len(detail_list)))

    # Get link list
    for items in detail_list:
        get_items = items.find_elements(By.CLASS_NAME, 'item')
        a_tag = get_items[0].find_elements(By.TAG_NAME, 'a')
        herf_list.append(a_tag[0].get_attribute('href'))
        #print('len {}'.format(len(get_items)))

    print('Link count : {}'.format(len(herf_list)))
# Access to fisrt link 
# 일단 하나씩 올려보면서 직접 크롤링 해보는 방향으로
    drv.get(herf_list[0])
    product_list = drv.find_elements(By.CLASS_NAME, 'prod_main_info')
    print('product count : {}'.format(len(product_list)))

except:
    traceback.print_exc()

finally:
    time.sleep(3)
    drv.quit()
    print('Quit crawlering')