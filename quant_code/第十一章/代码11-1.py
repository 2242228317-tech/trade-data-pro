Import  requests
url = "http://hq.sinajs.cn/list=sz000001"
r = requests.get(url)
if r.status_code==200:
    print(r.text)

%pip install tushare

import tushare
print("tushare版本号{}".format(tushare.__version__))

Import  tushare  as  ts
ts.get_hist_data('000001') #一次性获取全部日k线数据
’’’ 
参数说明：
code：股票代码，即6位数字代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
start：开始日期，格式YYYY-MM-DD
end：结束日期，格式YYYY-MM-DD
ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
retry_count：当网络异常后重试次数，默认为3
pause:重试时停顿秒数，默认为0
例如：
ts.get_hist_data('000001', ktype='W') #获取周k线数据
ts.get_hist_data('000001', ktype='M') #获取月k线数据
ts.get_hist_data('000001', ktype='5') #获取5分钟k线数据
ts.get_hist_data('000001', ktype='15') #获取15分钟k线数据
ts.get_hist_data('000001', ktype='30') #获取30分钟k线数据
ts.get_hist_data('000001', ktype='60') #获取60分钟k线数据
ts.get_hist_data('sh'）#获取上证指数k线数据
ts.get_hist_data('sz'）#获取深圳成指k线数据
ts.get_hist_data('hs300'）#获取沪深300指数k线数据
ts.get_hist_data('000001',start='2021-01-01',end='2021-03-20') #获取”000001”从2021-01-01到2021-03-20的k线数据
’’’

Import  tushare  as  ts
ts.get_today_all()
