# coding=utf-8
import requests
r = requests.get("https://www.baidu.com/img/dong_528d34b686d4889666f77c62b9a65857.gif")
with open("baidu.png","wb") as f:
    f.write(r.content)

# coding=utf-8
import requests
r = requests.get("https://www.baidu.com ")
r.text

from selenium import webdriver

# 创建 WebDriver 对象，指明使用chrome浏览器驱动
wd = webdriver.Chrome(r'd:\webdrivers\chromedriver.exe')
# 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
wd.get('https://www.baidu.com')
elements = wd.find_element_by_id('s_lg_img')
print(elements)
print(wd.page_source)#打印网页源代码

from bs4 import BeautifulSoup
html=wd.page_source
bs = BeautifulSoup(html, "html.parser")
title = bs.find('div', id='lg').img
print(title.get("src")[2:])