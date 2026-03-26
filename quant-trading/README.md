# 量化交易系统

基于Python的量化交易平台，集成了多种技术指标和交易策略。

## 功能特性

- 📊 **实时行情**：获取A股实时数据
- 📈 **技术指标**：MACD、KDJ、BOLL、RSI、MA等
- 🎯 **交易策略**：双均线、MACD、KDJ、布林带、RSI、综合策略
- 📉 **策略回测**：完整的回测系统，支持夏普比率、最大回撤等分析
- 🔍 **信号扫描**：自动扫描全市场买卖信号
- ⭐ **自选股管理**：本地保存自选股，自动跟踪信号

## 项目结构

```
quant-trading/
├── backend/              # FastAPI后端
│   ├── app/
│   │   ├── main.py      # 入口文件
│   │   ├── models.py    # 数据库模型
│   │   ├── routers/     # API路由
│   │   │   ├── stock.py
│   │   │   ├── indicators.py
│   │   │   ├── strategy.py
│   │   │   └── backtest.py
│   │   └── services/    # 业务逻辑
│   │       ├── data_service.py
│   │       ├── indicator_service.py
│   │       ├── strategy_service.py
│   │       └── backtest_service.py
│   └── requirements.txt
├── frontend/            # Vue3前端
│   ├── src/
│   │   ├── views/       # 页面组件
│   │   ├── api/         # API接口
│   │   └── App.vue
│   └── package.json
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
# 后端
cd backend
pip install -r requirements.txt

# 前端
cd frontend
npm install
```

### 2. 配置Tushare Token

编辑 `backend/app/services/data_service.py`，修改 `TS_TOKEN` 为你自己的Tushare API Token。

获取Token：https://tushare.pro/register

### 3. 启动服务

```bash
# 启动后端 (端口8000)
cd backend
python -m app.main

# 启动前端 (端口3000)
cd frontend
npm run dev
```

### 4. 访问系统

打开浏览器访问：http://localhost:3000

## API文档

启动后端后访问：http://localhost:8000/docs

## 策略说明

### MA交叉策略
- **买入**：短期均线上穿长期均线（金叉）
- **卖出**：短期均线下穿长期均线（死叉）

### MACD策略
- **买入**：DIFF线上穿DEA线
- **卖出**：DIFF线下穿DEA线

### KDJ策略
- **买入**：K线上穿D线且J<80
- **卖出**：K线下穿D线或J>100

### 布林带策略
- **买入**：股价触及下轨反弹或突破中轨
- **卖出**：股价触及上轨回落或跌破中轨

### 综合策略
- 3个及以上指标共振时产生交易信号

## 免责声明

本系统仅供学习研究使用，不构成投资建议。股市有风险，投资需谨慎。
