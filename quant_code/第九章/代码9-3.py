import pandas as pd
import requests
import json
import simplejson
from pandas.io.json import json_normalize
url ="http://api.quchaogu.com/dxwapp/lhb/funds?pagecount=20&lhsj=0&end_time=1500&RANKS_TAG=RANK_STRENGTH&day=20210422&start_time=930&filter_type=0&szjh=0&last_time=1500&KEY_ACTIVITY_TAB_PV=/sslhb&page=1&zg=1&kjjx=0&apiversion=8.9&backgroundcolor=white&vaid=&oaid=&device_id=a865166028641465"

r = requests.get(url)
if r.status_code==200:
    a=json.loads(r.text)
    b=pd.DataFrame.from_records(a['data']['stock_list']['list'])
    print(json_normalize(data=b[0])[["param.code","text","remark"]])
