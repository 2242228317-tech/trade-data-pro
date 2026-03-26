// API 配置 - 从环境变量读取
export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// 应用配置
export const APP_NAME = process.env.NEXT_PUBLIC_APP_NAME || 'TradeData Pro';
export const APP_URL = process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000';

// 支付配置
export const PAYMENT_CONFIG = {
  // 支持的支付方式
  methods: [
    { id: 'alipay', name: '支付宝', icon: '💙', color: '#1677FF' },
    { id: 'wechat', name: '微信支付', icon: '💚', color: '#07C160' },
  ] as const,
  
  // 订阅时长选项
  durations: [
    { months: 1, label: '1个月', discount: 0 },
    { months: 3, label: '3个月', discount: 0 },
    { months: 12, label: '12个月', discount: 0.2 }, // 年付8折
  ],
};

// 会员配置
export const MEMBERSHIP_PLANS = [
  {
    role: 'free',
    name: '免费版',
    price: 0,
    period: '永久免费',
    description: '适合个人体验',
    features: [
      { text: '每日 10 次查询', included: true },
      { text: '查看最近 3 个月数据', included: true },
      { text: '基础数据图表', included: true },
      { text: '数据导出', included: false },
      { text: 'API 接口访问', included: false },
    ]
  },
  {
    role: 'basic',
    name: '基础版',
    price: 29,
    period: '/月',
    description: '适合个人研究者',
    features: [
      { text: '每日 100 次查询', included: true },
      { text: '查看最近 12 个月数据', included: true },
      { text: '高级数据图表', included: true },
      { text: 'CSV 数据导出', included: true },
      { text: 'API 接口访问', included: false },
    ]
  },
  {
    role: 'pro',
    name: '专业版',
    price: 99,
    period: '/月',
    description: '适合专业分析师',
    popular: true,
    features: [
      { text: '无限次查询', included: true },
      { text: '查看最近 5 年历史数据', included: true },
      { text: '专业数据分析报告', included: true },
      { text: 'Excel + CSV 导出', included: true },
      { text: '完整 API 接口访问', included: true },
    ]
  },
  {
    role: 'enterprise',
    name: '企业版',
    price: 299,
    period: '/月',
    description: '适合企业数据部门',
    features: [
      { text: '无限次查询', included: true },
      { text: '查看最近 10 年历史数据', included: true },
      { text: '定制化数据报告', included: true },
      { text: '批量数据导出', included: true },
      { text: 'API + 数据推送', included: true },
    ]
  }
];

// 请求封装
export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const url = `${API_URL}${endpoint}`;
  
  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  // 添加认证token
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    if (token) {
      defaultHeaders['Authorization'] = `Bearer ${token}`;
    }
  }
  
  const response = await fetch(url, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '请求失败' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  
  return response.json();
}
