#! python 
# encoding: UTF-8
import time
import traceback
import csv
# import os

from datetime import datetime as dt
from typing import List

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains


'''
Get Danawa product infomations
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

            except Exception:
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

    detail_list = drv.find_elements(By.CLASS_NAME, 'category__list__row')
    print('parsing category list : {}'.format(len(detail_list)))

    # 컴퓨터 index 1 클릭 이벤트 추가
    detail_list[1].click()
    depth_list = detail_list[1].find_elements(By.CLASS_NAME, 'category__depth__row')
    print(f'depth count : {len(depth_list)}')

    for item in depth_list:
        category_code = item.get_attribute('category-code')
        # 753 is VGA code value
        #
        if category_code == 753:
            item.click()
    # Sleep for page changing
    time.sleep(10)

    '''
    mainClass: 대 분류
    midClass : 중 분류
    subClass : 소 분류
    '''
    categoryList = drv.find_elements(By.CLASS_NAME, 'dir_item')
    print(f'categoryList count : {len(categoryList)}')
    mainClass, midClass, subClass = categoryList[1], categoryList[2], categoryList[3]
    mainClass = mainClass.find_elements(By.TAG_NAME, 'span')[0].text
    midClass = midClass.find_elements(By.TAG_NAME, 'span')[0].text
    subClass = subClass.find_elements(By.TAG_NAME, 'span')[0].text
    
    cate = []
    print('{}->{}->{}'.format(mainClass, midClass, subClass))
    cate.append(mainClass)
    cate.append(midClass)
    cate.append(subClass)

    #product_list = drv.find_elements(By.CLASS_NAME, 'prod_main_info')
    #print('product count : {}'.format(len(product_list)))

    # Crawling product info
    # Maybe for-loop here
    resultList = getProductInfo(drv, cate)
    
    # Debug
    # for item in resultList:
    #    print(item)
    MakeCSV(today, resultList)

    # Move Tab
    # Maybe using click event
    numTab = drv.find_elements(By.CLASS_NAME, 'number_wrap')[0].find_elements(By.TAG_NAME, 'a')
    print("numTab: {}".format(len(numTab)))
        
except Exception:
    traceback.print_exc()

finally:
    # time.sleep(3)
    drv.quit()
    print('Quit crawling')
