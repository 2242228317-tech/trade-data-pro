# A 股量化选股系统 - 使用指南

## 🚀 快速开始

### 1. 安装依赖

```bash
cd quant_stock
pip install -r requirements.txt
```

### 2. 基本使用

#### 执行突破策略选股（默认）
```bash
python main.py --strategy breakout --top 10
```

#### 分析单只股票
```bash
python main.py --analyze 000001
```

#### 交互模式
```bash
python main.py --interactive
```

### 3. 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| --strategy | -s | 选股策略 (breakout/trend/value) | breakout |
| --top | -t | 返回股票数量 | 10 |
| --analyze | -a | 分析单只股票代码 | - |
| --interactive | -i | 进入交互模式 | False |

## 📊 策略说明

### 突破策略 (breakout)
适合短线交易，关注:
- ✅ 当日涨幅 > 3%
- ✅ 成交量放大 > 1.5 倍
- ✅ 突破 20 日高点
- ✅ 均线多头排列
- ✅ MACD/KDJ金叉

**评分标准**: 满足条件越多，得分越高（满分 10 分）

### 趋势策略 (trend)
适合中线持有，关注:
- ✅ 20 日均线向上倾斜
- ✅ 股价在均线上方
- ✅ 成交量温和放大

### 价值策略 (value)
适合长线投资，关注:
- ✅ 低市盈率 (PE < 20)
- ✅ 高 ROE (> 10%)
- ✅ 基本面良好

## 💡 交互模式命令

```
>>> analyze 000001      # 分析平安银行
>>> screen breakout     # 执行突破选股
>>> screen trend        # 执行趋势选股
>>> help                # 显示帮助
>>> quit                # 退出
```

## 📈 技术指标说明

### 均线系统 (MA)
- **MA5**: 5 日均线，超短期趋势
- **MA10**: 10 日均线，短期趋势
- **MA20**: 20 日均线，月线级别
- **MA60**: 60 日均线，季线级别

**多头排列**: MA5 > MA10 > MA20 > MA60 (看涨)
**空头排列**: MA5 < MA10 < MA20 < MA60 (看跌)

### MACD
- **DIF**: 快线
- **DEA**: 慢线
- **金叉**: DIF 上穿 DEA (买入信号)
- **死叉**: DIF 下穿 DEA (卖出信号)

### KDJ
- **K > 80**: 超买区 (谨慎)
- **K < 20**: 超卖区 (关注)
- **K 上穿 D**: 金叉 (买入)

### RSI
- **RSI > 70**: 超买
- **RSI < 30**: 超卖

### 布林带 (BOLL)
- **上轨**: 压力位
- **中轨**: 20 日均线
- **下轨**: 支撑位

## ⚠️ 风险提示

1. **本程序仅供学习研究**，不构成投资建议
2. 股市有风险，入市需谨慎
3. 短期交易风险极高，请控制仓位
4. 建议设置止损位（如 -5%）
5. 不要把所有资金投入单只股票
6. 历史表现不代表未来收益

## 🛠️ 扩展开发

### 添加新策略

在 `strategies/` 目录下创建新的选股器类:

```python
from strategies.selector import StockSelector

class MyStrategy(StockSelector):
    def select(self, stock_codes, **kwargs):
        # 实现你的选股逻辑
        results = []
        for code in stock_codes:
            df = self.fetcher.get_daily_data(code)
            # ... 分析逻辑
            if 符合条件:
                results.append({...})
        return pd.DataFrame(results)
```

然后在 `get_selector()` 函数中注册:

```python
selectors['my_strategy'] = MyStrategy
```

### 添加新指标

在 `indicators/technical.py` 中添加:

```python
@staticmethod
def MY_INDICATOR(df, **kwargs):
    df = df.copy()
    # 计算逻辑
    df['NEW_COLUMN'] = ...
    return df
```

## 📁 目录结构

```
quant_stock/
├── main.py              # 主程序入口
├── requirements.txt     # 依赖列表
├── README.md           # 项目说明
├── USAGE.md            # 使用指南
├── data/
│   └── data_fetcher.py # 数据获取模块
├── indicators/
│   └── technical.py    # 技术指标模块
├── strategies/
│   └── selector.py     # 选股策略模块
└── output/             # 选股结果输出目录
```

## 🔧 常见问题

### Q: 获取数据失败怎么办？
A: 检查网络连接，akshare 需要访问东方财富网站。也可以考虑使用 tushare 等替代数据源。

### Q: 选股结果为空？
A: 可能是市场整体表现不佳，没有股票满足条件。可以尝试降低筛选条件。

### Q: 如何回测策略？
A: 当前版本主要提供选股功能，回测功能正在开发中。可以手动记录选股结果，后续跟踪验证。

---

**祝投资顺利！📈**
