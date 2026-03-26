pip install selenium

from selenium import webdriver

# 创建 WebDriver 对象，指明使用chrome浏览器驱动
wd = webdriver.Chrome(r'd:\webdrivers\chromedriver.exe')

# 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
wd.get('https://www.baidu.com')

from selenium import webdriver

# 创建 WebDriver 对象，指明使用chrome浏览器驱动
wd = webdriver.Chrome()

# 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
wd.get('https://www.baidu.com')

driver.find_element_by_link_text("新闻").click()

driver.find_element_by_link_text("新").click()
driver.find_element_by_link_text("闻").click()

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
    #browser.close()
get_pop_rank("002639")

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

list_stock=["300059","603316","000001","002639","000001","000002","000003"]
for i in list_stock:
    get_pop_rank(i)

def get_pop_rank(code,browser):
# 启动浏览器，获取网页源代码

    try:
        mainUrl = http://guba.eastmoney.com/list,{}.html".format(code)
        browser.get(mainUrl)
        element = browser.find_element_by_id('popularity_rank')
        
        print(code,element.text)
        return code,element.text
    except:
        
        print(code,'timeout')
        return code,'timeout'
