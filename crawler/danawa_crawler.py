#! python 
# encoding: UTF-8
import time
import traceback
import csv
import os

from datetime import datetime as dt
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


'''
Get Danawa product infomation
for my research
'''


def getProductInfo(drv, cate) -> List:
    resultList = []
    linkList = []
    # resultList.append(drv)
    productList = drv.find_elements(By.CLASS_NAME, 'prod_layer') 
    # print("count: {}".format(len(productList)))
    
    for product in productList:
        div = product.find_elements(By.CLASS_NAME, 'thumb_image')
        # print("div count : {}".format(len(div)))
        linkList.append(div[0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href'))

    # Save parents URL
    parents = drv.current_url
    # print(parents)

    for idx, url in enumerate(linkList):
        drv.get(url)
        diff_items = drv.find_elements(By.CLASS_NAME, 'diff_item')

        if idx >= len(linkList) - 1:
            print('last product is skipped')
            break

        # Get name
        prod_name = drv.find_elements(By.CLASS_NAME, 'prod_tit')[0].text
        print('product_name : {}'.format(prod_name))
                
        for item in diff_items:
            # product list
            tmp = []
            tmp += cate

            try:
                # Get url
                link = item.find_elements(By.CLASS_NAME, 'prc_line')
                link = link[0].find_elements(By.CLASS_NAME, 'priceCompareBuyLink')
                link = link[0].get_attribute('href')

                # Mall info
                d_mall = item.find_elements(By.CLASS_NAME, 'd_mall')[0].find_elements(By.TAG_NAME, 'img')[0]
                d_mall = d_mall.get_attribute('alt')

                # price, ship fee
                price = item.find_elements(By.CLASS_NAME, 'prc_c')[0].text
                ship = item.find_elements(By.CLASS_NAME, 'ship')[0].text
               
                # print(d_mall, price, ship)
                # print(link)
                # print('-'*10)

                # product List
                tmp.append(prod_name)
                tmp.append(price)
                tmp.append(ship)
                tmp.append(d_mall)
                tmp.append(link)

            except:
                print('skip')
                continue

            # Products List
            resultList.append(tmp)

    # Return parents Page
    drv.get(parents)
    
    return resultList


'''
function description 
Save List to csv
'''
def MakeCSV(today, productsList):
    ret = True
    headers = ['main', 'mid', 'sub', 'name', 'price', 'ship', 'platform', 'link', 'label']
    rows = productsList
    
    with open('./data/' + today+'.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(headers)
        ret = w.writerows(productsList)

    print("writerResult: {}".format(ret))
    return ret


'''
webDrv
targetURL
'''
webDrv = '/usr/bin/safaridriver'
targetURL = 'http://www.danawa.com'
# opt = webdriver.SafariOptions()
# opt.add_argument('--incognito')

drv = webdriver.Safari(executable_path=webDrv)
herf_list = []

try:
    today = dt.now()
    today = today.strftime("%y%m%d.%H%M")
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
        # print('len {}'.format(len(get_items)))

    print('Link count : {}'.format(len(herf_list)))
    # Access to fisrt link 
    # 일단 하나씩 올려보면서 직접 크롤링 해보는 방향으로
    # 가전 index : 6
    drv.get(herf_list[8])
    
    product_list = drv.find_elements(By.CLASS_NAME, 'prod_main_info')
    print('product count : {}'.format(len(product_list)))

    '''
    mainClass: 대 분류
    midClass : 중 분류
    subClass : 소 분류
    '''
    # mainClass = drv.find_elements(By.CLASS_NAME, 'f dir_home')
    # print('mainClass : {}'.format(len(mainClass)))
    # print('mainClass : {}'.format(mainClass.find_elements(By.CLASS_NAME, 'a')[0].text))
    categoryList = drv.find_elements(By.CLASS_NAME, 'dir_item')
    mainClass, midClass, subClass = categoryList[1], categoryList[2], categoryList[3]
    # print(mainClass.dtype, midClass.dtype)
    mainClass = mainClass.find_elements(By.TAG_NAME, 'span')[0].text
    midClass = midClass.find_elements(By.TAG_NAME, 'span')[0].text
    subClass = subClass.find_elements(By.TAG_NAME, 'span')[0].text
    
    cate = []
    print('{}->{}->{}'.format(mainClass, midClass, subClass))
    cate.append(mainClass)
    cate.append(midClass)
    cate.append(subClass)

    # Crawling product info
    # Maybe for-loop here
    resultList = []
    resultList = getProductInfo(drv, cate)
    
    # Debug
    # for item in resultList:
    #    print(item)
    MakeCSV(today, resultList)

    # Move Tab
    # Maybe using click event
    numTab = drv.find_elements(By.CLASS_NAME, 'number_wrap')[0].find_elements(By.TAG_NAME, 'a')
    print("numTab: {}".format(len(numTab)))
        
except:
    traceback.print_exc()

finally:
    # time.sleep(3)
    drv.quit()
    print('Quit crawlering')
