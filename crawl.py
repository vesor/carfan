#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import re
import tinydb

MODE_NORMAL, MODE_HIGHTEMP, MODE_DRIVE = range(3)
def keyOfMode(key, mode):
    # keys xpath is '//*[@id="JiaQuanGj"]'
    modes = ['Gj', 'Sw', 'Qd']
    return '//*[@id="{}{}"]'.format(key, modes[mode])



options = webdriver.ChromeOptions()

# tell selenium to use the dev channel version of chrome
# NOTE: only do this if you have a good reason to
# options.binary_location = '/usr/bin/google-chrome-unstable'  # path to google Chrome bin

options.add_argument('headless')

# set the window size
options.add_argument('window-size=1200x600')

# with proxy
proxy_url = 'ip:port'
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': proxy_url,
    'sslProxy': proxy_url  # 需要信任代理服务器CA证书
})

desired_capabilities = options.to_capabilities()
proxy.add_to_capabilities(desired_capabilities)

# initialize the driver
# driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome(chrome_options=options, desired_capabilities=desired_capabilities)

db = tinydb.TinyDB('tinydb.json')

def get_value_for(key):
    elem = driver.find_element_by_xpath(key)
    text = re.sub("[^0-9.\-]","", elem.text)
    if len(text) == 0:
        return 0 # 未检出
    else:
        return float(text)

def get_items_in_mode(switch_tab, mode):
    #switch_tab.click()
    driver.execute_script("arguments[0].click();", switch_tab)
    items = {}
    items['C6H6'] = get_value_for(keyOfMode('Ben', mode))
    items['C6H5CH3'] = get_value_for(keyOfMode('JiaBen', mode))
    items['C6H5CH2CH3'] = get_value_for(keyOfMode('YiBen', mode))
    items['C6H4CH3CH3'] = get_value_for(keyOfMode('ErJiaBen', mode))
    items['C6H5CHCH2'] = get_value_for(keyOfMode('BenYiXi', mode))
    items['HCHO'] = get_value_for(keyOfMode('JiaQuan', mode))
    items['CH3CHO'] = get_value_for(keyOfMode('YiQuan', mode))
    items['CH2CHCHO'] = get_value_for(keyOfMode('BinXiQuan', mode))
    return items  

def scrap_page(url):
    driver.get(url)

    # wait up to 10 seconds for the elements to become available
    driver.implicitly_wait(10)
    #driver.get_screenshot_as_file('1.png')

    # use css selectors to grab the search inputs
    # text = driver.find_element_by_css_selector('#kw')
    # search = driver.find_element_by_css_selector('#su')

    # text.send_keys('headless chrome')

    # driver.get_screenshot_as_file('2.png')


    # # search
    # search.click()
    # driver.get_screenshot_as_file('search-result.png')

    # results = driver.find_elements_by_xpath('//div[@class="result c-container "]')

    # for result in results:
    #     res = result.find_element_by_css_selector('a')
    #     title = res.text
    #     link = res.get_attribute('href')
    #     print ('Title: %s \nLink: %s\n' % (title, link))

    result = {}

    head_title = driver.find_elements_by_xpath('/html/head/title')
    head_title = head_title[0].get_attribute("textContent")
    matchObj = re.match( u'(.*)油耗及环保评测_(.*)油耗及环保评测_怎么样', head_title)
    if matchObj:
        result['car_name'] = matchObj.group(1)
        result['car_model'] = matchObj.group(2)
    else:
        return None

    aq_label = driver.find_elements_by_xpath('//*[@id="targetId"]/div/div[1]/div[1]/div[1]/div[1]')
    #print (aq_label[0].text)
    if len(aq_label) == 0:
        return None # No title, page not found, or test not finished
    
    
    
    aq_score = driver.find_elements_by_xpath('//*[@id="targetId"]/div/div[1]/div[1]/div[1]/div[2]/span')
    #print (aq_score[0].text)
    result['score'] = int(aq_score[0].text)

    # hcho_value = driver.find_elements_by_xpath('//*[@id="JiaQuanGj"]')
    # print (hcho_value[0].text)

    # evaluation_container = driver.find_elements_by_class_name('evaluation-center')
    # assert len(evaluation_container) == 1
    # evaluation_container = evaluation_container[0]

    chart_container = driver.find_elements_by_class_name('md-qualityChart')
    assert len(chart_container) == 1
    chart_container = chart_container[0]

    switch_container = chart_container.find_elements_by_class_name('switch-tab')

    switch_tabs = switch_container[0].find_elements_by_xpath('.//div')
    assert len(switch_tabs) == 3

    result['normal_mode'] = get_items_in_mode(switch_tabs[0], MODE_NORMAL)
    result['hightemp_mode'] = get_items_in_mode(switch_tabs[1], MODE_HIGHTEMP)
    result['drive_mode'] = get_items_in_mode(switch_tabs[2], MODE_DRIVE)


    # click to avoid auto scrolling
    active_swipers = driver.find_elements_by_class_name('swiper-pagination-switch swiper-visible-switch swiper-active-switch')
    for sw in active_swipers:
        sw.click()

    report_images_container = driver.find_elements_by_class_name('md-picShow-swiper')
    if len(report_images_container) > 0:
        assert len(report_images_container) == 1
        image_urls = []
        report_images_container = report_images_container[0]
        image_elems = report_images_container.find_elements_by_xpath('.//div[1]/div[1]/div')
        for elem in image_elems:
            src = elem.find_element_by_tag_name('img').get_attribute('src')
            image_urls.append(src)
        result['report_scans'] = image_urls

    return result


for i in range(200):
    id = 800 + i
    url = 'http://pingce.m.yiche.com/details/{:d}-7-2.html'.format(id)
    print ('url', url)
    result = scrap_page(url)

    if result is not None:
        result['id'] = id
        print (result['car_name']) 
        qr = tinydb.Query()
        db.upsert(result, qr.id == id)
