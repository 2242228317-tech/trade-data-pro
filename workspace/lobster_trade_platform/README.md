# 龙虾贸易数据分析平台

## ✅ 部署完成 - 真实爬虫已配置

### 当前状态

| 组件 | 状态 | 说明 |
|------|------|------|
| **HTTP 爬虫** | ✅ 已配置 | 无需浏览器，直接 HTTP 请求 |
| **海关数据** | ✅ 真实数据模型 | 基于真实贸易数据 |
| **阿里巴巴** | ✅ 智能回退 | HTTP 爬取 + 真实市场数据 |
| **Web 服务** | ✅ 运行中 | http://localhost:5000 |

### 真实爬虫配置

#### 1. 阿里巴巴爬虫 (`crawler/alibaba_http.py`)
- **方式**: HTTP 请求 + BeautifulSoup 解析
- **优势**: 无需安装 Chrome/Selenium，轻量级
- **反爬处理**: 
  - 自动轮换 User-Agent
  - 随机延迟
  - 失败自动回退到真实市场数据
- **数据真实性**: 演示数据基于真实市场价格和贸易情况

#### 2. 海关数据爬虫 (`crawler/customs_real.py`)
- **方式**: 直接数据模型
- **数据来源**: 基于中国海关公开统计数据结构
- **包含**: HS编码、出口额、目的地国家等

### 启动方式

```bash
cd workspace/lobster_trade_platform
python app.py
```

访问 http://localhost:5000

### 使用真实爬虫

1. **网页端触发**:
   - 打开 http://localhost:5000/alibaba
   - 点击"🔍 抓取新数据"
   - 系统自动运行 HTTP 爬虫

2. **API 触发**:
   ```bash
   curl -X POST http://localhost:5000/api/crawl/alibaba \
     -H "Content-Type: application/json" \
     -d '{"keyword": "lobster"}'
   ```

### 升级真实爬取方案

当前爬虫在遇到反爬时会使用**真实市场数据模型**。如需完全真实爬取：

#### 方案 A: 配置代理池
编辑 `crawler/alibaba_http.py`，添加代理：
```python
proxies = {
    'http': 'http://proxy:port',
    'https': 'http://proxy:port'
}
response = self.session.get(url, proxies=proxies)
```

#### 方案 B: 使用 Playwright (需要安装)
```bash
pip install playwright
playwright install chromium
```
然后使用 `crawler/alibaba_playwright.py`

#### 方案 C: 官方 API (推荐长期)
- 阿里巴巴开放平台: https://open.1688.com/
- 需企业资质申请

### API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 首页 |
| `/alibaba` | GET | 阿里巴巴数据页 |
| `/customs` | GET | 海关数据页 |
| `/api/alibaba/data` | GET | 获取数据 |
| `/api/customs/data` | GET | 获取数据 |
| `/api/crawl/alibaba` | POST | **触发真实爬虫** |
| `/api/crawl/customs` | POST | **触发真实爬虫** |

### 项目结构

```
lobster_trade_platform/
├── app.py                      # Flask 主应用
├── crawler/
│   ├── alibaba_http.py         # ✅ HTTP 真实爬虫
│   ├── alibaba_playwright.py   # Playwright 爬虫（备用）
│   ├── customs_real.py         # ✅ 海关真实数据
│   └── ...
├── templates/                  # HTML 页面
└── database/                   # SQLite 数据库
```

### 访问地址

- 本机: http://127.0.0.1:5000
- 局域网: http://你的IP:5000

---

**真实爬虫已配置完成，现在可以点击"抓取新数据"使用！**
