# A 股量化选股系统

专业的 A 股量化分析工具，支持技术指标分析、选股策略、回测等功能。

## 功能特性

- 📊 **数据获取**: 支持 akshare/tushare 数据源
- 📈 **技术指标**: MA、MACD、KDJ、RSI、BOLL 等
- 🎯 **选股策略**: 多因子选股、技术面选股、突破策略等
- 📉 **回测系统**: 策略历史表现回测
- 📱 **信号提醒**: 买卖点自动生成

## 安装依赖

```bash
pip install akshare pandas numpy ta-lib matplotlib tqdm
```

## 快速开始

```bash
python main.py --strategy breakout --top 10
```

## 目录结构

```
quant_stock/
├── main.py           # 主入口
├── data/            # 数据模块
├── indicators/      # 技术指标
├── strategies/      # 选股策略
├── backtest/        # 回测系统
└── utils/           # 工具函数
```

## 风险提示

⚠️ 本程序仅供学习研究使用，不构成投资建议。股市有风险，投资需谨慎。
