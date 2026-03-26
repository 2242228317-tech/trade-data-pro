import requests
import json
import simplejson
url ="http://api.quchaogu.com/dxwapp/lhb/funds?pagecount=20&lhsj=0&end_time=1500&RANKS_TAG=RANK_STRENGTH&day=20210420&start_time=930&filter_type=0&szjh=0&last_time=1500&KEY_ACTIVITY_TAB_PV=/sslhb&page=1&zg=1&kjjx=0&apiversion=8.9&backgroundcolor=white&vaid=&oaid=&device_id=a865166028641465%20HTTP/1.1"

r = requests.get(url)
if r.status_code==200:
    print(r.text)

import requests
import json
import simplejson
url ="http://api.quchaogu.com/dxwapp/lhb/funds?pagecount=20&lhsj=0&end_time=1500&RANKS_TAG=RANK_STRENGTH&day=20210420&start_time=930&filter_type=0&szjh=0&last_time=1500&KEY_ACTIVITY_TAB_PV=/sslhb&page=1&zg=1&kjjx=0&apiversion=8.9&backgroundcolor=white&vaid=&oaid=&device_id=a865166028641465%20HTTP/1.1"

r = requests.get(url)
if r.status_code==200:
    r=r.text.encode('utf-8').decode('unicode_escape')
    print(r)

import pandas as pd
import requests
from pandas.io.json import json_normalize
url ="http://api.quchaogu.com/dxwapp/lhb/funds?pagecount=20&lhsj=0&end_time=1500&RANKS_TAG=RANK_STRENGTH&day=20210420&start_time=930&filter_type=0&szjh=0&last_time=1500&KEY_ACTIVITY_TAB_PV=/sslhb&page=1&zg=1&kjjx=0&apiversion=8.9&backgroundcolor=white&vaid=&oaid=&device_id=a865166028641465%20HTTP/1.1"

r = requests.get(url)
if r.status_code==200:
    a=json.loads(r.text)
    b=pd.DataFrame.from_records(a['data']['stock_list']['list'])
    print(b)

df = (df["1"].apply(pd.Series).merge(df, left_index=True, right_index = True)

data_r= json.loads(r)
df = json_normalize(data_r)
df.head()

# 只深入到嵌套第4级
pd.json_normalize(r, record_path="code", max_level =4)

#print(json_normalize(data=b[0]))
print(json_normalize(data=b[0]).info())
