# 超级无敌大韭菜 - A 股投资分析技能

## 📦 技能包结构

```
chaoji-wudi-da-jiucai/
├── SKILL.md                    # 技能说明（核心）
├── scripts/
│   ├── get_stock_data.py       # 行情数据获取
│   ├── technical_analysis.py   # 技术指标分析
│   ├── fundamental_analysis.py # 基本面分析
│   └── risk_checker.py         # 风险评估
├── references/
│   ├── indicators.md           # 技术指标详解
│   ├── strategies.md           # 投资策略库
│   ├── financial_reports.md    # 财报解读指南
│   └── risk_management.md      # 风险管理手册
└── assets/
    └── report_template.md      # 分析报告模板
```

---

## 🚀 使用方法

### 方式一：直接使用（无需 Python）

技能的核心功能（行情获取、技术分析、基本面分析、风险评估）可以通过 Python 脚本实现，但**即使没有 Python，你也可以直接使用本技能的分析框架和参考文档**。

在对话中触发：
- 发送股票代码（如"600519"、"贵州茅台"）
- 询问分析（如"分析宁德时代"、"看看茅台的技术面"）

---

### 方式二：完整功能（需要 Python）

#### 1. 安装 Python

下载地址：https://www.python.org/downloads/

安装时勾选 **"Add Python to PATH"**

#### 2. 安装依赖

```bash
pip install requests
```

#### 3. 运行脚本

```bash
# 获取行情
python scripts/get_stock_data.py 600519 quote

# 获取 K 线
python scripts/get_stock_data.py 600519 kline

# 技术分析（演示模式）
python scripts/technical_analysis.py --demo

# 基本面分析
python scripts/fundamental_analysis.py 600519

# 风险评估（演示模式）
python scripts/risk_checker.py --demo
```

---

## 📊 功能说明

### 1. 行情数据获取 (`get_stock_data.py`)

**数据源：** 新浪财经、腾讯财经（免费）

**支持：**
- 实时行情（开盘、收盘、最高、最低、成交量）
- 历史 K 线（日 K、周 K、月 K）
- 股票基本信息

**注意：** 免费数据可能有 15 分钟延迟

---

### 2. 技术指标分析 (`technical_analysis.py`)

**支持指标：**
- 均线（MA5/10/20/60）
- MACD（金叉/死叉/背离）
- KDJ（超买/超卖）
- RSI（相对强弱）
- BOLL（布林带）

**输出：**
- 指标数值
- 买卖信号
- 趋势判断

---

### 3. 基本面分析 (`fundamental_analysis.py`)

**分析维度：**
- 估值（PE、PB、历史分位）
- 成长（营收增长、利润增长）
- 盈利（ROE、毛利率、净利率）
- 财务健康（负债率、现金流）

**输出：**
- 综合评分（0-100）
- 星级评级（1-5 星）
- 投资建议

---

### 4. 风险评估 (`risk_checker.py`)

**风险因素：**
- 高位风险（52 周分位）
- 波动率风险
- 回撤风险
- 估值风险
- 技术破位风险

**输出：**
- 风险等级（低/中/高）
- 止盈止损建议
- 仓位建议

---

## ⚠️ 重要提示

### 数据限制
- 免费 API 有延迟，盘中交易请以券商软件为准
- 财务数据需要付费 API（如东方财富 Choice、同花顺 iFinD）
- 当前脚本使用模拟数据或免费数据源

### 投资风险
- **本技能不构成投资建议**
- 所有分析仅供参考
- 决策由用户自行负责
- 建议分散投资、设置止损

### 建议配置
如需完整功能，建议：
1. 开通付费数据 API（东方财富/同花顺）
2. 接入券商交易接口（需合规）
3. 定期更新脚本和数据源

---

## 📚 参考文档

- **技术指标** → `references/indicators.md`
- **投资策略** → `references/strategies.md`
- **财报解读** → `references/financial_reports.md`
- **风险管理** → `references/risk_management.md`

---

## 🔄 后续优化

### 待实现功能
- [ ] 接入付费数据 API
- [ ] 资金流向分析
- [ ] 龙虎榜数据
- [ ] 北向资金追踪
- [ ] 行业对比分析
- [ ] 自动报告生成
- [ ] 回测功能

### 欢迎贡献
如有改进建议或新功能，欢迎提交！

---

**祝投资顺利，账户长红！📈**

*市场有风险，投资需谨慎*
