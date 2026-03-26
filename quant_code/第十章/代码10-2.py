import pandas as pd
import tushare as ts
import numpy as np
import talib as tb
import warnings
import numpy as np
warnings.filterwarnings('ignore')
df_30min=pd.DataFrame(ts.get_hist_data("002701", ktype='30'))[:200] #获取30分钟k线数据
df_30min=df_30min[::-1]
df_30min["tdate"]=pd.to_datetime(df_30min.index)#转换成datetime格式化
# df_30min["month"]=df_30min.tdate.apply(lambda x: x.month)
df=df_30min[["open","high","low","close"]]
df["ma5"]=df.close.rolling(window=5).mean()
df["ma30"]=df.close.rolling(window=30).mean()
con=df.ma5>df.ma30#计算
df["position"]=con#覆盖到列中
df["cross"]=df.position.rolling(window=2).sum()
con_cross=df[df.cross==1]
df["cross"]=df[df.cross==1]

print(con_cross,con_cross.shift(-1))

con_cross=(df.cross==1)
df.loc[con_cross,"cross"]=df.loc[con_cross].ma5
df["cross"]=df["cross"].replace(0,np.nan).replace(2,np.nan)
#构造时间

all_cross=df.loc[con_cross]
all_cross["end_date"]=df.loc[con_cross].shift(-1).tdate
#print(all_cross)
#阶段最高最低点
df.loc[:,"mark"]=pd.np.nan
for i in all_cross.itertuples():
    #print(i.tdate,i.end_date,i.position)
    con_dur=(df.tdate>=i.tdate)&(df.tdate<=i.end_date)
    #print(con_dur)
    df_con_dur=df.loc[con_dur]
    #print(df_con_dur.info())
    #position 为TRUE，MA5>MA30,有最高点。FALSE有最低点。
    if df_con_dur.empty:
        continue
    if i.position==True:
        max_price=df_con_dur.high.max()
        df.loc[con_dur,"mark"]=max_price
        max_price_date=df_con_dur.loc[df_con_dur.high==max_price].tdate.iloc[0]
        #print(max_price_date)
        all_cross.loc[all_cross.tdate==i.tdate,"maxmin_price"]=max_price
        all_cross.loc[all_cross.tdate==i.tdate,"maxmin_price_date"]=max_price_date
    else:  
        min_price=df_con_dur.low.min()
        df.loc[con_dur,"mark"]=min_price
        min_price_date=df_con_dur.loc[df_con_dur.low==min_price].tdate.iloc[0]
        #print(min_price_date)
        all_cross.loc[all_cross.tdate==i.tdate,"maxmin_price"]=min_price
        all_cross.loc[all_cross.tdate==i.tdate,"maxmin_price_date"]=min_price_date
df.loc[:,"beenline"]=pd.np.nan
for i in range(0,all_cross.tdate.count()-1) :
    #print(i,i+1)
    pre=all_cross.iloc[i][["maxmin_price","maxmin_price_date","position"]]
    nex=all_cross.iloc[i+1][["maxmin_price","maxmin_price_date"]]
    pre_date=pre.maxmin_price_date
    pre_price=pre.maxmin_price
    nex_date=nex.maxmin_price_date
    nex_price=nex.maxmin_price
    if pre.position==True:
        con_pre_nex_date=(df.tdate>=pre_date)&(df.tdate<=nex_date)
        lenth=df.loc[con_pre_nex_date].tdate.count()
        diff_line=pd.np.linspace(pre_price,nex_price,lenth)
        df.loc[con_pre_nex_date,"beenline"]=diff_line
    else:
        con_pre_nex_date=(df.tdate>=pre_date)&(df.tdate<=nex_date)
        lenth=df.loc[con_pre_nex_date].tdate.count()
        diff_line=pd.np.linspace(pre_price,nex_price,lenth)
        df.loc[con_pre_nex_date,"beenline"]=diff_line
#print(df)
        
fig, ax = plt.subplots(figsize=(15, 15)) ## 创建图片和坐标轴
#mpf.candlestick2_ohlc(ax,df.open,df.high,df.low,df.close,width=1.0,colorup='r',colordown='green', alpha=1)
l=[i for i in range(df.tdate.count())]
ax.plot(l,df.ma5,"g-")
ax.plot(l,df.ma30,"b-")
ax.plot(l,df.cross,"k.")
ax.plot(l,df.mark,"b.")
ax.plot(l,df.beenline,"k-")

import seaborn as sns
sns.set(style="whitegrid")
sns.boxplot(x="industry", y="amount_predict", data=data_df[2], palette="Set3")

a.style.\
        bar(width=100,subset=['涨幅','主占比√'],color='lightpink').\
        background_gradient(subset=['ths_rq'], cmap='spring') # 指定色系#background_gradient(cmap='Reds',axis = 0,low = 0,high = 1,subset = ['ths_rq'])

