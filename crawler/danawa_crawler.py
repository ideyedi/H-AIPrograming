#! python 
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

def getProductInfo():
    print('hello')

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

    '''
    mainClass: 대 분류
    midClass : 중 분류
    subClass : 소 분류
    '''
    #mainClass = drv.find_elements(By.CLASS_NAME, 'f dir_home')
    #print('mainClass : {}'.format(len(mainClass)))
    #print('mainClass : {}'.format(mainClass.find_elements(By.CLASS_NAME, 'a')[0].text))
    categoryList = drv.find_elements(By.CLASS_NAME, 'dir_item')
    mainClass, midClass, subClass = categoryList[1], categoryList[2], categoryList[3]
    #print(mainClass.dtype, midClass.dtype)
    mainClass = mainClass.find_elements(By.TAG_NAME, 'span')[0].text
    midClass = midClass.find_elements(By.TAG_NAME, 'span')[0].text
    subClass = subClass.find_elements(By.TAG_NAME, 'span')[0].text
    print('{}->{}->{}'.format(mainClass, midClass, subClass))

    # Crawling product info
    getProductInfo()
        
except:
    traceback.print_exc()

finally:
    time.sleep(3)
    drv.quit()
    print('Quit crawlering')
