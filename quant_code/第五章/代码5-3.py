# coding=utf-8
import requests
url=” http://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112309073354919152763_1617455258436&fid=f62&po=1&pz=50&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124”
r = requests.get(url)

r_text=r.text.split("{}".format("jQuery112309073354919152763_1617455258436"))[1]
r_text

r_text_qu=r_text.rstrip(';')
r_text_json=json.loads(r_text_qu[1:-1])['data']['diff']
dfcf_code={"f12":"code","f2":"价格","f3":"涨幅","f14":"name","f62":"主净入√","f66":"超净入","f69":"超占比",
                   "f72":"大净入","f75":"大占比","f78":"中净入","f81":"中占比","f84":"小净入","f87":"小占比","f124":"不知道","f184":"主占比√"}
result_=pd.DataFrame(r_text_json).rename(columns=dfcf_code)
result_["主净入√"]=round(result_["主净入√"]/100000000,2)#一亿，保留2位
result_=result_[result_["主净入√"]>0]
result_["超净入"]=round(result_["超净入"]/100000000,2)#一亿，保留2位
result_["大净入"]=round(result_["大净入"]/100000000,2)#一亿，保留2位
result_["中净入"]=round(result_["中净入"]/100000000,2)#一亿，保留2位
result_["小净入"]=round(result_["小净入"]/100000000,2)#一亿，保留2位
result_
