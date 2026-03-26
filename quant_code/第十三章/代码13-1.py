def boll_today(code): 
    code=code
    T("20210512")
    # 设置关注股票为耀皮玻璃
    S("{}".format(code))
    today_price=csv_data.loc[csv_data['code'] =="{}".format(code), "trade"]  
    today_price =today_price.item()
    std_today_list=[]
    std_today_list.append(today_price )
    for i in range(0,12):
        #print(i,CLOSE[i])
        std_today_list.append(float(str(CLOSE[i])))
    print("{}".format(code),std_today_list,round(np.std(std_today_list),2))#
for i in csv_data.code[:10]:
    boll_today(i)

def boll_today(code): 
    code=code
    T("20210512")
    # 设置关注股票为耀皮玻璃
    S("{}".format(code))
    today_price=csv_data.loc[csv_data['code'] =="{}".format(code), "trade"]  
    today_price =today_price.item()
    std_today_list=[]
    std_today_list.append(today_price )
    for i in range(0,12):
        #print(i,CLOSE[i])
        std_today_list.append(float(str(CLOSE[i])))
    if round(np.std(std_today_list),2)>float(str(STD(CLOSE,13))):
        print("{}".format(code),std_today_list,round(np.std(std_today_list),2),STD(CLOSE,13))#

hour_start=datetime.now()
for i in csv_data.code[:100]:
    try:
        boll_today(i)
        hour_end=datetime.now()
        print("用时{}".format((hour_end-hour_start)))
    except:
        pass

