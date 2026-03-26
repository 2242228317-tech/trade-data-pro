def init(context):
    # cash_limit的属性是根据用户需求自己定义的，你可以定义无限多种自己随后需要的属性，ricequant的系统默认只是会占用context.portfolio的关键字来调用策略的投资组合信息
context.cash_limit = 5000
# 在context中保存全局变量
    context.s1 = "000001.XSHE"
# 实时打印日志
    logger.info("RunInfo: {}".format(context.run_info))

def handle_bar(context, bar_dict):
    # put all your algorithm main logic here.
    # ...
    order_shares('000001.XSHE', 500)
    # ...
def before_trading(context, bar_dict):
    logger.info("This is before trading")

def before_trading(context):
fundamentals_df=get_fundamentals(
query(
fundamentals.eod_derivative_indicator.market_cap_2))
S1=list(fundamentals_df.columns.values)

def filter_paused(stock_list):
    return [stock for stock in stock_list if not is_suspended(stock)]

def filter_st(stock_list):
    return [stock for stock in stock_list if not is_st_stock(stock)]

def filter_new(stock_list):
    return [stock for stock in stock_list if instruments(stock).days_from_listed() >= 180]

# before_trading此函数会在每天策略交易开始前被调用，当天只会被调用一次
def before_trading(context):
    fundamentals_df=get_fundamentals(
    query(
    fundamentals.eod_derivative_indicator.market_cap_2)) 
    S1=list(fundamentals_df.columns.values)
    stocks = filter_paused(S1)
    stocks = filter_st(stocks)
    context.stocks = filter_new(stocks)
    #logger.info("context.stocks"+str(context.stocks))
    print('股票总数：',len(S1))
print('------')
def filter_paused(stock_list):
    return [stock for stock in stock_list if not is_suspended(stock)] 

def filter_st(stock_list):
    return [stock for stock in stock_list if not is_st_stock(stock)]
    
def filter_new(stock_list):
    return [stock for stock in stock_list if instruments(stock).days_from_listed() >= 180]

def KDJ(N=9, M1=3, M2=3):
    """
    KDJ 随机指标
    """
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA(RSV, (M1 * 2 - 1))
    D = EMA(K, (M2 * 2 - 1))
    J = K * 3 - D * 2
    return K, D, J
    
def MACD(SHORT=12, LONG=26, M=9):
    """
    MACD 指数平滑移动平均线
    """
    DIFF = EMA(CLOSE, SHORT) - EMA(CLOSE, LONG)
    DEA = EMA(DIFF, M)
    MACD = (DIFF - DEA) * 2
return DIFF,DEA,MACD

def BOLL(N=20, P=2):
    """
    BOLL 布林带
    """
    MID = MA(CLOSE, N)
    UPPER = MID + STD(CLOSE, N) * P
    LOWER = MID - STD(CLOSE, N) * P
return UPPER, MID, LOWER

def Kinko Hyo (M1=7, M2=22,M3=44):
    """
    Ichimoku Kinko Hyo
    """
    zk=(HHV(HIGH,M1)+LLV(LOW,M1))/2
    zd=(HHV(HIGH,M2)+LLV(LOW,M2))/2
    hy=REF(C,M2)
    za=REF((zk+zd)/2,M2)
    zb=REF((HHV(HIGH,M3)+LLV(LOW,M3))/2,M2)
    za_f=(zk+zd)/2
    zb_f=(HHV(HIGH,M3)+LLV(LOW,M3))/2
return zk,zd,za,zb,za_f,zb_f
