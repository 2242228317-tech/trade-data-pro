import tushare as ts
csv_data=ts.get_today_all()
csv_data["turnoverratio"]=round(csv_data["turnoverratio"],2)#换手率保留2位
csv_data["liutongliang"]=csv_data["nmc"]/csv_data["trade"]#增加流通盘的列
csv_data["turnover_jisuan"]=csv_data["volume"]/csv_data["liutongliang"]/100#股/100=手  csv_data["volume"]>20000000 20万手
print(csv_data[["turnover_jisuan","turnoverratio"]])

