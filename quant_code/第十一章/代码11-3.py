impor t get_data
csv_data=get_data.today_data()
for code in  csv_data.code:
	print(code )

import  get_data
from  datetime  import  datetime, date,timedelta
import re
import time
import tushare as ts

global pro  #在使用前初次声明
ts.set_token('b31e0ac207a5a45e0f7503aff25bf6bd929b88fe1d017a034ee0d530')
pro = ts.pro_api()

def gu_zhengze_sz(code):
    if re.match(r'^6.*',code):
        i_code_temp=code+'.SH'
    if re.match(r'^(0|3).*',code):
        i_code_temp=code+'.SZ'
    return i_code_temp
def len_fangzhi_szcode(szcode,start_time,today_time):
    time_=pro.daily(ts_code=szcode,start_date=start_time,end_date=today_time)['trade_date']
    return len(time_)
def len_fangzhi(start_time,today_time):
time_=pro.daily(ts_code='000001.SZ',start_date=start_time, end_date=today_time)
['trade_date']
    print("{}到{}一共{}天".format(start_time,today_time,len(time_)))#两时间间距15天
    return len(time_),time_[0],time_[1]
def time_jg():
    len_time,time_0,time_1=len_fangzhi(start_time,today_time)
    if str(datetime.now())[11:13]<=str(15):
        time_t=time_0
    else:
        time_t=time_1
    #print(str(datetime.now())[11:13]==time_t) #False
    print("fc时间",time_t)#fc时间 20200408
    return time_t,len_time
def time_start():
    """今天时间today_time 格式20200307"""
    today_time=str(datetime.now())[:11]
    start_time=str(datetime.now() - timedelta(days=20))[:11]
    today_time= re.sub(r'\D', "",today_time)
    start_time= re.sub(r'\D', "",start_time)
    #('20200731', '20200820', '16:12')
return start_time,today_time,str(datetime.now())[11:16]

csv_data=get.get_data()
start_time,today_time,today_hour=time_start()#时间('20200731', '20200820', '16:12')
time_t,len_time=time_jg()
for code in  csv_data.code:
    szcode=gu_zhengze_sz(code)
    len_time_sz=len_fangzhi_szcode(szcode,start_time,today_time)
    print(code,’ , 该股票在近20日中成交日{}天’.format(len_time_sz))

def main():
    csv_data=get.get_data()
    start_time,today_time,today_hour=time_start()#时间('20200731', '20200820', '16:12')
    time_t,len_time=time_jg()
    for code in  csv_data.code:
        szcode=gu_zhengze_sz(code)
        len_time_sz=len_fangzhi_szcode(szcode,start_time,today_time)
        print(code,’ , 该股票在近20日中成交日{}天’.format(len_time_sz))
        if len_time_sz<=len_time-1:#追加判断语句，去掉停牌股票
        continue

```
## 单股票研究
``` python
from funcat import *
from funcat.data.tushare_backend import TushareDataBackend

set_data_backend(TushareDataBackend())

# 设置目前天数为2017年1月4日
T("20170104")
# 设置关注股票为上证指数
S("000001.XSHG")

# 打印 Open High Low Close
>>> print(O, H, L, C)
3133.79 3160.1 3130.11 3158.79

# 当天涨幅
>>> C / C[1] - 1
0.0072929156356

# 打印60日均线
>>> MA(C, 60)
3154.78333333

# 判断收盘价是否大于60日均线
>>> C > MA(C, 60)
True

# 30日最高价
>>> HHV(H, 30)
3301.21

# 最近30日，收盘价 Close 大于60日均线的天数
>>> COUNT(C > MA(C, 60), 30)
17

# 10日均线上穿
>>> CROSS(MA(C, 10), MA(C, 20))
False
```

## DataBackend
默认实现了一个从 tushare 上面实时拉数据选股的 Backend。

为了更高的性能，可以自定义Backend使用本地数据。这样可以极大地提高运行速度。

## TODO
- EMA
- MACD
- KDJ
- BOLL

def fc_get(code,start_time,time_0,time_1):
    if str(datetime.now())[11:13]<=str(15):
        time_t=time_0
    else:
        time_t=time_1
    S(code)
    T(time_t)
    try:
        #print(HHV(H,10),":::::,日期报错,funcat hhv的问题。")
        print(code[:6],"fc时间{}".format(time_t),str(CLOSE),str(100*MA(V,5)),str(100*MA(V,30)),str(100*MA(V,120)),HHV(H,10),LLV(L,10),MA(CLOSE,50))
        return (code[:6],"fc时间{}".format(time_t),str(CLOSE),str(100*MA(V,5)),str(100*MA(V,30)),str(100*MA(V,120)),HHV(H,10),LLV(L,10),MA(CLOSE,50))
    except:
        return

if len_time_sz<=len_time-1: 
    continue
if today_time!=time_0 or (str(datetime.now())[11:13]>str(15)): 
    listr=other.fc_get(szcode[:6],start_time,time_0,time_1)
list_collect.append(listr)
df_mongo=pd.DataFrame(list_collect)
df_mongo.to_csv("data_gp/get_ma120.txt",encoding = "utf-8")
    columns_name=["code","time","close_yestday","MA_5","MA_30","MA_120","H_10","L_10","MA_C_50"]
if len(df_mongo.columns)==len(columns_name):
    df_mongo=pd.DataFrame(list_collect,columns=columns_name)
    df_mongo.to_csv("data_gp/get_ma120.txt",encoding = "utf-8")

def get_ma50():
    hour_start=datetime.now()#--》用时
    
    start_time,today_time,today_hour=other.time_start()#('20201128', '20201218', '22:11')
    len_time,time_0,time_1=other.len_fangzhi(start_time,today_time)#(15, '20201218', '20201217')
    data_get_ts = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date').rename(columns={'symbol':'code'})

    list_collect=[]
    for szcode in data_get_ts.ts_code[:]:
        ##接口限制访问500次/分钟
        #time.sleep(0.121)
        len_time_sz=other.len_fangzhi_szcode(szcode,start_time,today_time)
        if len_time_sz<=len_time-1:#防止出错
            continue
        if today_time!=time_0 or (str(datetime.now())[11:13]>str(15)):#第二天 or 当日15点以后（）
            listr=other.fc_get(szcode[:6],start_time,time_0,time_1)#['代码', '603992.XSHG', 'fc时间20200325', 20.09, '成交量', 86524.0]
        list_collect.append(listr)
    df_mongo=pd.DataFrame(list_collect)
    df_mongo.to_csv("data_gp/get_ma120.txt",encoding = "utf-8")
    columns_name=["code","time","close_yestday","MA_5","MA_30","MA_120","H_10","L_10","MA_C_50"]
    if len(df_mongo.columns)==len(columns_name):
        df_mongo=pd.DataFrame(list_collect,columns=columns_name)
        df_mongo.to_csv("data_gp/get_ma120.txt",encoding = "utf-8")
        
    #--》检查错误2020.12.18
    if len(df_mongo.columns)!=len(columns_name):
        print("--->请检查:列数")
    if len(df_mongo)<3000:
        print("--->请检查:股票数量是否正确")
    arr=data_get_ts.columns.str.contains('^ts_code')#[False False False False False False False False False False False False False False False False]
    #     print('True个数：',np.sum(arr!=0))
    #     print('False个数：',np.sum(arr==0))
    if np.sum(arr!=0)==0:
        print("--->请检查:获取数量为空")
        data_get_ts = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date').rename(columns={'symbol':'code'})
        print(data_get_ts)
    #--》用时
    hour_end=datetime.now()
    print("MA120用时{}".format((hour_end-hour_start)))
    return df_mongo
