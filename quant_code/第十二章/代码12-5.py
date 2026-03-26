from funcat import *
from funcat.data.tushare_backend import TushareDataBackend

set_data_backend(TushareDataBackend())

T("20210512")
# 设置关注股票为耀皮玻璃
S("600819.XSHG")
print(O, H, L, C)
TR = MAX(MAX(HIGH - LOW, ABS(HIGH - REF(CLOSE, 1))), ABS(LOW - REF(CLOSE, 1)))
SUM(TR,10)/10

import tushare as ts
import pandas as pd
from funcat import *
from datetime import datetime, date,timedelta
import numpy as np

global pro  #在使用前初次声明
ts.set_token('b31e0ac207a5a45e0f7503aff25bf6bd929b88fe1d017a034ee0d530')
pro = ts.pro_api()
csv_data=ts.get_today_all()

today_high=csv_data.loc[csv_data['code'] =="600819", "high"]
today_low=csv_data.loc[csv_data['code'] =="600819", "low"]
tr_today=MAX(MAX((today_high-today_low),ABS(CLOSE-today_high)),ABS(CLOSE-today_low))
atr_today=(SUM(TR,9)+tr_today)/10
atr_today

from funcat import *
from funcat.data.tushare_backend import TushareDataBackend

set_data_backend(TushareDataBackend())

T("20210512")
# 设置关注股票为耀皮玻璃
S("600819.XSHG")
DI1, DI2, ADX, ADXR=DMI(M1=10, M2=6)
print(DI1, DI2, ADX, ADXR)

import tushare as ts
import pandas as pd
from funcat import *
from datetime import datetime, date,timedelta
import numpy as np

global pro  #在使用前初次声明
ts.set_token('b31e0ac207a5a45e0f7503aff25bf6bd929b88fe1d017a034ee0d530')
pro = ts.pro_api()
csv_data=ts.get_today_all()
T("20210512")
# 设置关注股票为耀皮玻璃
S("600819.XSHG")
print(O, H, L, C)

today_high=csv_data.loc[csv_data['code'] =="600819", "high"]
today_low=csv_data.loc[csv_data['code'] =="600819", "low"]
today_high =today_high.item()
today_low = today_low.item()
TR = MAX(MAX(HIGH - LOW, ABS(HIGH - REF(CLOSE, 1))), ABS(LOW - REF(CLOSE, 1)))
HD = HIGH - REF(HIGH, 1)
LD = REF(LOW, 1) - LOW
tr_today=MAX(MAX((today_high-today_low),ABS(CLOSE-today_high)),ABS(CLOSE-today_low))
hd=today_high-HIGH
ld=LOW-today_low
tr_toal_today_2=(tr_today+TR)
dmp_today = IF((HD > 0) & (HD > LD), HD, 0)+IF((hd > 0) & (hd > ld),hd, 0)
dmm_today = IF((LD > 0) & (LD > HD), LD, 0)+IF((ld > 0) & (ld > hd),ld, 0)
di1 = dmp_today * 100 / tr_toal_today_2
di2 = dmm_today * 100 / tr_toal_today_2
print(di1,di2)

from funcat import *
from funcat.data.tushare_backend import TushareDataBackend

set_data_backend(TushareDataBackend())

T("20210512")
# 设置关注股票为耀皮玻璃
S("600819.XSHG")
for i in range(0,12):
    print(i,CLOSE[i])

today_price=csv_data.loc[csv_data['code'] =="600819", "trade"]  
today_price =today_price.item()
std_today_list=[]
std_today_list.append(today_price )
for i in range(0,12):
    std_today_list.append(float(str(CLOSE[i])))
print(std_today_list)

