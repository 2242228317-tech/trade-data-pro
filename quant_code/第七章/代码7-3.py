from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def get_pop_rank(code):
# 启动浏览器，获取网页源代码
    browser = webdriver.Chrome()
    mainUrl = "http://guba.eastmoney.com/list,{}.html".format(code)
    browser.get(mainUrl)
    #print(f"browser text = {browser.page_source}")
    element = browser.find_element_by_id('popularity_rank')
    print(code,element.text)
    browser.close()

s = time.time()
for i in csv_li[10:20]:
    get_pop_rank(i)
e = time.time()
print('总用时：',e-s)

get_pop_rank(code)内部，所有时间会不会有改变呢。爱动手的读者可以先自行编写代码，然后继续读书，跟着我的思路继续往下研究。
	For循环在get_pop_rank(code)内部，详见如下代码。
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def get_pop_rank(code_list):
# 启动浏览器，获取网页源代码
    browser = webdriver.Chrome()
    for code in code_list:
        mainUrl = "http://guba.eastmoney.com/list,{}.html".format(code)
        browser.get(mainUrl)
        #print(f"browser text = {browser.page_source}")
        element = browser.find_element_by_id('popularity_rank')
        print(code,element.text)
    browser.quit()

s = time.time()
get_pop_rank(csv_li[10:20])
e = time.time()
print('总用时：',e-s)

from selenium import webdriver
import time
from threading import Thread
import pandas as pd
def process(code_list,num):
    browser = webdriver.Chrome()
    browser.set_page_load_timeout(20)
    for code in code_list:

        mainUrl = "http://guba.eastmoney.com/list,{}.html".format(code)
        browser.get(mainUrl)
        element = browser.find_element_by_id('popularity_rank')
        print(code,element.text)
    browser.quit()
def process2(code_list,num):
    browser = webdriver.Chrome()
    browser.set_page_load_timeout(20)
    for code in code_list:

        mainUrl = "http://guba.eastmoney.com/list,{}.html".format(code)
        browser.get(mainUrl)
        element = browser.find_element_by_id('popularity_rank')
        print(code,element.text)
    browser.quit()

def main():
    thead_list = []
    csv_data=data_get()
    #多线程
    t1 = Thread(target=process, args=(csv_li[10:15],1))
    t1.start()
    t2 = Thread(target=process2, args=(csv_li[15:20],1))
    t2.start()
    thead_list.append(t1)
    t1.join()
    t2.join()
if __name__ == '__main__':
    s = time.time()
    main()
    e = time.time()
    print('总用时：',e-s)

