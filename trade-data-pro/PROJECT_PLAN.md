# 外贸数据分析平台项目规划

## 项目名称
**TradeData Pro** - 中国出口商品数据分析平台

## 技术架构

### 前端
- **框架**: Next.js 14 + TypeScript + Tailwind CSS
- **UI 组件**: shadcn/ui + Framer Motion
- **图表**: ECharts / Recharts
- **地图**: 高德地图 API / ECharts 地图

### 后端
- **API**: FastAPI (Python)
- **数据库**: PostgreSQL (主库) + Redis (缓存)
- **爬虫**: Scrapy + Playwright (处理动态页面)
- **任务调度**: Celery + Redis
- **搜索**: Elasticsearch (可选)

### 数据源
1. **1688/阿里巴巴**: 商品信息、价格、销量
2. **海关总署**: 官方出口统计数据
3. **国家统计局**: 宏观经济数据
4. **世界银行**: 国际贸易数据

## 核心功能模块

### 1. 数据采集模块
- **1688 爬虫**: 商品详情、价格走势、销量统计
- **海关数据爬虫**: 进出口商品分类统计
- **定时任务**: 每日/每周自动更新
- **数据清洗**: 去重、标准化、补全

### 2. 数据存储设计

#### 商品信息表 (products)
```sql
- id: UUID
- source: ENUM ('1688', 'customs', 'manual')
- category_id: UUID (分类ID)
- name: VARCHAR (产品名称)
- description: TEXT (产品描述)
- price: DECIMAL (价格)
- cost: DECIMAL (成本)
- currency: VARCHAR (币种)
- quantity: INTEGER (销量)
- unit: VARCHAR (单位)
- export_region: VARCHAR[] (出口地区)
- hs_code: VARCHAR (海关编码)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

#### 海关统计数据表 (customs_stats)
```sql
- id: UUID
- year: INTEGER
- month: INTEGER
- hs_code: VARCHAR (海关编码)
- product_name: VARCHAR
- export_value: DECIMAL (出口金额 USD)
- export_quantity: DECIMAL (出口数量)
- unit: VARCHAR
- destination_country: VARCHAR (目的国)
- growth_rate: DECIMAL (增长率)
```

#### 分类表 (categories)
```sql
- id: UUID
- parent_id: UUID (父分类)
- name: VARCHAR (分类名)
- hs_code_prefix: VARCHAR (海关编码前缀)
- icon: VARCHAR
```

### 3. 前端页面设计

#### 首页 (Dashboard)
- 核心指标卡片（今日出口额、TOP 商品、增长趋势）
- 实时数据滚动展示
- 热门品类云图
- 出口目的地地图

#### 数据洞察页
- 多维度筛选（时间、品类、地区）
- 趋势图表（折线图、柱状图）
- 排行榜（TOP 10 商品/地区）
- 对比分析

#### 商品详情页
- 价格走势曲线
- 销量统计
- 竞争分析
- 相似商品推荐

#### 海关数据页
- HS 编码查询
- 官方统计数据
- 月度/年度报告

#### 管理后台
- 爬虫任务管理
- 数据质量监控
- 用户权限管理

## 爬虫策略

### 1688 爬虫
```python
# 主要抓取字段
- 商品标题、详情
- 价格区间、起批量
- 30天销量、累计成交
- 供应商信息
- 产品参数
```

### 海关总署爬虫
```python
# 数据来源: http://www.customs.gov.cn/
# 抓取内容:
- 进出口商品类章总值表
- 主要出口商品量值表
- 进出口贸易方式总值表
- 进出口商品贸易方式企业性质总值表
```

## 项目目录结构
```
trade-data-pro/
├── frontend/              # Next.js 前端
│   ├── app/              # App Router
│   ├── components/       # 组件
│   ├── lib/              # 工具函数
│   └── types/            # TypeScript 类型
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── models/       # 数据模型
│   │   ├── services/     # 业务逻辑
│   │   └── tasks/        # 异步任务
│   ├── crawler/          # 爬虫模块
│   └── config/           # 配置文件
├── database/             # 数据库迁移
├── docker-compose.yml    # 部署配置
└── README.md
```

## 开发计划

### Phase 1: 基础架构 (1周)
- [ ] 项目初始化
- [ ] 数据库设计
- [ ] Docker 配置
- [ ] 基础 API

### Phase 2: 数据采集 (1-2周)
- [ ] 1688 爬虫
- [ ] 海关数据爬虫
- [ ] 数据清洗入库
- [ ] 定时任务

### Phase 3: 前端开发 (2周)
- [ ] Dashboard 首页
- [ ] 数据可视化
- [ ] 搜索/筛选功能
- [ ] 响应式设计

### Phase 4: 高级功能 (1周)
- [ ] 用户系统
- [ ] 数据导出
- [ ] 邮件订阅
- [ ] API 限流

### Phase 5: 部署优化 (1周)
- [ ] 服务器部署
- [ ] 性能优化
- [ ] 监控告警

## 技术要求
- 数据实时性: T+1 更新
- 并发量: 支持 1000+ 并发
- 响应时间: API < 200ms
- 可用性: 99.5%

## 注意事项
⚠️ **法律合规**
- 遵守 robots.txt
- 控制爬虫频率
- 不涉及个人隐私数据
- 数据来源标注

⚠️ **反爬策略**
- IP 代理池
- 请求间隔随机化
- User-Agent 轮换
- 验证码处理

---

**确认后开始 Phase 1 开发？**
