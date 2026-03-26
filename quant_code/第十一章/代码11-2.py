import tushare  as  ts
csv_data=ts.get_today_all()
csv_data[~csv_data.name.str.contains('ST')]

import tushare  as  ts
csv_data=ts.get_today_all()
csv_data=csv_data[~csv_data.name.str.contains('ST')]
csv_data[csv_data["volume"]>15000000]#15万手

import tushare  as  ts
csv_data=ts.get_today_all()
csv_data=csv_data[~csv_data.name.str.contains('ST')]
csv_data=csv_data[csv_data["volume"]>15000000]#15万手
csv_data["amount"]=round(csv_data["amount"]/100000000,2)#一亿，保留2位
csv_data[(csv_data["amount"]>1)]

import  tushare  as  ts
csv_data=ts.get_today_all()
csv_data=csv_data[~csv_data.name.str.contains('ST')]
csv_data=csv_data[csv_data["volume"]>15000000]#15万手
csv_data["amount"]=round(csv_data["amount"]/100000000,2)#一亿，保留2位
csv_data=csv_data[(csv_data["amount"]>1)]
csv_data["liutongliang"]=csv_data["nmc"]/csv_data["trade"]#增加流通盘的列
csv_data["turnoverratio"]=round(csv_data["turnoverratio"],2)#换手率保留2位
csv_data[csv_data["turnoverratio"]>3]

impor t tushare as ts
def  today_data():
    csv_data=ts.get_today_all()
    csv_data=csv_data[~csv_data.name.str.contains('ST')]
    csv_data=csv_data[csv_data["volume"]>15000000]#15万手
    csv_data["amount"]=round(csv_data["amount"]/100000000,2)#一亿，保留2位
    csv_data=csv_data[(csv_data["amount"]>1)]
    csv_data["liutongliang"]=csv_data["nmc"]/csv_data["trade"]#增加流通盘的列
    csv_data["turnoverratio"]=round(csv_data["turnoverratio"],2)#换手率保留2位
    csv_data=csv_data[csv_data["turnoverratio"]>3]
    csv_data=csv_data.sort_values(by="turnoverratio", ascending=False)
return csv_data

