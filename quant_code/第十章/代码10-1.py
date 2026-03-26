import requests
import json
from bs4 import BeautifulSoup
header={
    'Host': 'basic.10jqka.com.cn',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G9730 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Hexin_Gphone/10.24.03 (Royal Flush) hxtheme/0 innerversion/G037.08.490.1.32 followPhoneSystemTheme/0 userid/80738749 hxNewFont/1 isVip/0',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Cookie': 'user=MDpsdHNqaW06Ok5vbmU6NTAwOjkwNzM4NzQ5OjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI3Ojo6ODA3Mzg3NDk6MTYxOTE3ODcxODo6OjEyNjc2MjMwMDA6NDAwMDgyOjA6MWZiNThkNTI2OGE3NmY3MTFlOGM0NjI4OWQ5NGJlZTQzOjow; userid=80738749; u_name=ltsjim; escapename=ltsjim; ticket=eecee652c32fbde00d9ca32153f06c95; user_status=0; hxmPid=free_stock_paihangbang_601816; v=Aw1XFqaAMew7zvW_6Viar6WaFSKH6kG8yx6lkE-SSaQTRiZYFzpRjFtutWHc',
    'X-Requested-With': 'com.hexin.plat.android'
    }
url='http://basic.10jqka.com.cn/api/stockph/focusday.php?code={}'.format("000858")
r = requests.get(url,headers=header)
r_text=r.text.encode('utf-8')#r_text=r.text.encode('utf-8').decode('unicode_escape')
soup = BeautifulSoup(r_text, "lxml")
json.loads(soup.text)["data"]["history"]["rank"][-1]

import requests
import json
from bs4 import BeautifulSoup
import time
import pandas as pd
import shiyan
def ths_renqi(code):
    header={
    'Host': 'basic.10jqka.com.cn',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G9730 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Hexin_Gphone/10.24.03 (Royal Flush) hxtheme/0 innerversion/G037.08.490.1.32 followPhoneSystemTheme/0 userid/80738749 hxNewFont/1 isVip/0',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.8',
    'Cookie': 'user=MDpsdHNqaW06Ok5vbmU6NTAwOjkwNzM4NzQ5OjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI3Ojo6ODA3Mzg3NDk6MTYxOTE3ODcxODo6OjEyNjc2MjMwMDA6NDAwMDgyOjA6MWZiNThkNTI2OGE3NmY3MTFlOGM0NjI4OWQ5NGJlZTQzOjow; userid=80738749; u_name=ltsjim; escapename=ltsjim; ticket=eecee652c32fbde00d9ca32153f06c95; user_status=0; hxmPid=free_stock_paihangbang_601816; v=Aw1XFqaAMew7zvW_6Viar6WaFSKH6kG8yx6lkE-SSaQTRiZYFzpRjFtutWHc',
    'X-Requested-With': 'com.hexin.plat.android'
    }
    url='http://basic.10jqka.com.cn/api/stockph/focusday.php?code={}'.format(code)
    r = requests.get(url,headers=header)
    r_text=r.text.encode('utf-8')#r_text=r.text.encode('utf-8').decode('unicode_escape')
    soup = BeautifulSoup(r_text, "lxml")
    return json.loads(soup.text)["data"]["history"]["rank"][-1]
def url_today_zhenghe(numb=20):
    #资金流
    pd.set_option('display.max_rows', None)
    url_today=shiyan.url_get_main()
    url_today=url_today.reset_index()#去index()
    renqi_list=[]
    url_today=url_today[:numb]
    print("{}秒后显示，请耐心等待".format(numb))
    for i in url_today.code.tolist():
        renqi_=ths_renqi(i)
        renqi_list.append(renqi_)
        time.sleep(0.9)
    url_today["ths_rq"]=renqi_list
    return url_today

import requests
import json
from bs4 import BeautifulSoup
headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'v=A_nOCr7EvcWz-mFRdDTuBY8ICG7QBu241_oRTBsudSCfohOYY1b9iGdKIR2o',
'Host': 'basic.10jqka.com.cn',
'If-Modified-Since': 'Thu, 18 Feb 2021 05:46:40 GMT',
'sec-ch-ua': '"\\Not;A\"Brand";v="99", "Google Chrome";v="85", "Chromium";v="85"',
'sec-ch-ua-mobile': '?0',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'none',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4168.2 Safari/537.36'

}
url = "https://basic.10jqka.com.cn/api/stockph/popularity/top/"
r = requests.get(url, headers = headers)
result_=pd.DataFrame(json.loads(r.text)['data']["list"])

a=result_#增加内容
a.rename(columns={"change":"涨幅","change_reason":"行业","change_section":"几天","change_days":"几板","hot_rank_chg":"增长","circulate_market_value":"市值"}, inplace = True)
a["市值"]=pd.to_numeric(a["市值"])
a["市值"]=round(a["市值"]/100000000,2)#一亿，保留2位
result_=a[["name","涨幅","行业","几天","几板","市值","price","增长","code","hot_rank"]]

a=url_today_zhenghe(numb=40)
result_=shiyan.ths_top100()[["行业",'市值',"增长","code","hot_rank"]]
b=pd.merge(a, result_, how='outer', on=['code'])
print(b)

import  tushare  as  ts
csv_data=ts.get_today_all()
csv_data["turnoverratio"]=round(csv_data["turnoverratio"],2)#换手率保留2位
csv_data=csv_data[csv_data["turnoverratio"]>3]
csv_data=csv_data.sort_values(by="turnoverratio", ascending=False)
