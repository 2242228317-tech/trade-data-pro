import requests
url='http://www.iwencai.com/stockpick/search?typed=1&preParams=2&ts=2&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E4%BA%BA%E6%B0%94'
r = requests.get(url)
print(r.text)
print(r.status_code)

import requests
headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie':'PHPSESSID=09577a6ece656917a4c43358873b7ae6; cid=09577a6ece656917a4c43358873b7ae61617717486; ComputerID=09577a6ece656917a4c43358873b7ae61617717486; WafStatus=0; v=A7qdyFvvjlmHcQK1nT3B0UKnC-vfaz5vsO-y6cSzZs0Yt1RdrPuOVYB_AvSX',
'Host': 'www.iwencai.com',
'Referer': 'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E4%BA%BA%E6%B0%94',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
url='http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E4%BA%BA%E6%B0%94'
r = requests.get(url,headers = headers)
print(r.text)
print(r.status_code)

import requests
from bs4 import BeautifulSoup
headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie':'PHPSESSID=09577a6ece656917a4c43358873b7ae6; cid=09577a6ece656917a4c43358873b7ae61617717486; ComputerID=09577a6ece656917a4c43358873b7ae61617717488; WafStatus=0; user_status=0; other_uid=Ths_iwencai_Xuangu_ckirvbpw79oikwk4n56xv71mwnjy1wbz; v=A3QK7FAaqMovLzyGG4vnAzjpRTnlTZg32nEsew7VAP-CeRpvNl1oxyqB_Ald',
'Host': 'www.iwencai.com',
'Referer': 'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E4%BA%BA%E6%B0%94',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
data={'typed': '1',
'preParams': '2',
'ts': '2',
'f': '',
'qs': '',
'selfsectsn': '',
'querytype': '',
'searchfilter':'' ,
'tid': 'stockpick',
'w': '人气'}
url='http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=1&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%E4%BA%BA%E6%B0%94'
r = requests.get(url,headers = headers,params=data)
soup = BeautifulSoup(r.text, "lxml")
soup.find_all('a',target="_blank")[2:]
