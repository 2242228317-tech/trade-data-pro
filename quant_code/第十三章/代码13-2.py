import time
from funcat import *
from datetime import datetime, date,timedelta
def difenxing _today(code): 
    code=code
    T("20210520")
    S("{}".format(code))
    today_high=csv_data.loc[csv_data['code'] =="{}".format(code), "trade"]  
    today_high =today_high.item()
    print(code,today_high,H[1],HIGH)
for i in csv_data.code:
    difenxing(i)

from funcat import *
def difenxing_today(code): 
    code=code
    T("20210520")
    # 设置关注股票为耀皮玻璃
    S("{}".format(code))
    today_high=csv_data.loc[csv_data['code'] =="{}".format(code), "trade"]  
    today_high =today_high.item()
    try:
        if today_high>H[1]>HIGH and today_low>L[1]>L:
            print(code,today_high,H[1],HIGH)
    except:
        print(None)
csv_data=csv_data.sort_values(by="turnoverratio", ascending=False)
for i in csv_data.code:
    print(i)
    difenxing_today(i)
