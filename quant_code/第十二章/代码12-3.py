import tushare as ts
import pandas as pd
import numpy as np
from talib import *

df=ts.get_k_data('600600')
print(df.info())
df["real"] = talib.MA(df.close, timeperiod=30)
df['MA10_rolling'] = df['close'].rolling(30).mean()
print(df[["real",'MA10_rolling']])

