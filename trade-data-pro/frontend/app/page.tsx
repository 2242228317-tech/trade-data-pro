'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { 
  TrendingUp, Package, Globe, DollarSign, ArrowUpRight,
  BarChart3, PieChart, Activity, ExternalLink
} from 'lucide-react';

// 统计卡片
function StatCard({ title, value, change, icon: Icon, color }: any) {
  const [displayValue, setDisplayValue] = useState(0);
  const numValue = parseInt(value.replace(/[^0-9]/g, ''));
  
  useEffect(() => {
    const step = numValue / 30;
    let current = 0;
    const timer = setInterval(() => {
      current += step;
      if (current >= numValue) {
        setDisplayValue(numValue);
        clearInterval(timer);
      } else {
        setDisplayValue(Math.floor(current));
      }
    }, 50);
    return () => clearInterval(timer);
  }, [numValue]);
  
  const colorClasses: any = {
    blue: 'bg-blue-500',
    green: 'bg-emerald-500',
    purple: 'bg-violet-500',
    orange: 'bg-orange-500',
  };
  
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className={`${colorClasses[color]} p-3 rounded-lg`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <div className="flex items-center text-green-600 text-sm font-medium">
          <ArrowUpRight className="w-4 h-4 mr-1" />
          {change}
        </div>
      </div>
      <div className="mt-4">
        <p className="text-gray-500 text-sm">{title}</p>
        <p className="text-2xl font-bold text-gray-900 mt-1">
          {displayValue.toLocaleString()}
        </p>
      </div>
    </div>
  );
}

// 图表区域
function TrendChart() {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-blue-600" />
          <h3 className="font-bold text-gray-900">出口趋势分析</h3>
        </div>
        <select className="text-sm border border-gray-200 rounded-lg px-3 py-1">
          <option>近12个月</option>
          <option>近6个月</option>
        </select>
      </div>
      <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <div className="flex items-end justify-center gap-2 h-40">
            {[280, 265, 298, 312, 305, 320, 335, 342, 338, 355, 368, 395].map((v, i) => (
              <div key={i} className="flex flex-col items-center">
                <div 
                  className="w-6 bg-blue-500 rounded-t" 
                  style={{ height: `${(v/400)*120}px` }}
                />
                <span className="text-xs text-gray-400 mt-1">{i+1}月</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// 品类分布
function CategoryChart() {
  const categories = [
    { name: '电子产品', value: 35, color: '#3b82f6' },
    { name: '机械设备', value: 25, color: '#10b981' },
    { name: '纺织服装', value: 15, color: '#f59e0b' },
    { name: '化工产品', value: 12, color: '#8b5cf6' },
    { name: '其他', value: 13, color: '#6b7280' },
  ];
  
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-center gap-2 mb-6">
        <PieChart className="w-5 h-5 text-purple-600" />
        <h3 className="font-bold text-gray-900">品类分布</h3>
      </div>
      <div className="space-y-3">
        {categories.map((cat) => (
          <div key={cat.name} className="flex items-center">
            <div 
              className="w-3 h-3 rounded-full mr-3" 
              style={{ backgroundColor: cat.color }}
            />
            <span className="flex-1 text-sm text-gray-600">{cat.name}</span>
            <span className="font-medium text-gray-900">{cat.value}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// 实时动态
function RealtimeUpdates() {
  const updates = [
    { icon: '📱', text: '深圳某供应商上传了500+款电子产品', time: '刚刚' },
    { icon: '📈', text: '义乌小商品价格指数上涨 2.3%', time: '2分钟前' },
    { icon: '🚢', text: '海关总署2月最新统计数据已同步', time: '5分钟前' },
    { icon: '☀️', text: '太阳能电池板出口量激增 45%', time: '8分钟前' },
    { icon: '🔋', text: '锂电池原材料成本下降 8%', time: '12分钟前' },
  ];
  
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-center gap-2 mb-6">
        <Activity className="w-5 h-5 text-green-600" />
        <h3 className="font-bold text-gray-900">实时动态</h3>
        <span className="ml-auto flex items-center gap-1 text-xs text-green-600">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          实时更新中
        </span>
      </div>
      <div className="space-y-4">
        {updates.map((u, i) => (
          <div key={i} className="flex items-start gap-3">
            <span className="text-lg">{u.icon}</span>
            <div className="flex-1">
              <p className="text-sm text-gray-700">{u.text}</p>
              <p className="text-xs text-gray-400 mt-0.5">{u.time}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// 出口目的地
function RegionRanking() {
  const regions = [
    { name: '美国', value: '$120.5B', growth: '+8.2%' },
    { name: '欧盟', value: '$98.3B', growth: '+5.1%' },
    { name: '东盟', value: '$62.1B', growth: '+12.3%' },
    { name: '日本', value: '$34.7B', growth: '+3.8%' },
    { name: '韩国', value: '$28.9B', growth: '+6.5%' },
  ];
  
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <h3 className="font-bold text-gray-900 mb-6">出口目的地排行</h3>
      <div className="space-y-4">
        {regions.map((r, i) => (
          <div key={r.name} className="flex items-center">
            <span className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-bold mr-3">
              {i + 1}
            </span>
            <span className="flex-1 font-medium text-gray-900">{r.name}</span>
            <span className="text-gray-600 mr-3">{r.value}</span>
            <span className="text-green-600 text-sm">{r.growth}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// 快速入口
function QuickLinks() {
  const links = [
    { 
      title: '商品数据库', 
      desc: '浏览 1688 和海关商品数据', 
      href: '/products',
      icon: Package,
      color: 'blue',
      stats: '246个产品'
    },
    { 
      title: '海关统计', 
      desc: '官方进出口数据查询', 
      href: '/customs',
      icon: Globe,
      color: 'purple',
      stats: '月度更新'
    },
    { 
      title: '数据洞察', 
      desc: '价格趋势、竞品分析', 
      href: '/analytics',
      icon: TrendingUp,
      color: 'orange',
      stats: 'AI分析'
    },
  ];
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {links.map((link) => (
        <Link
          key={link.title}
          href={link.href}
          className="group bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-lg transition-all"
        >
          <div className="flex items-start justify-between mb-4">
            <div className={`p-3 bg-${link.color}-50 rounded-lg`}>
              <link.icon className={`w-6 h-6 text-${link.color}-600`} />
            </div>
            <span className="text-xs text-gray-400 bg-gray-50 px-2 py-1 rounded">
              {link.stats}
            </span>
          </div>
          <h4 className="font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
            {link.title}
          </h4>
          <p className="text-sm text-gray-500 mt-1">{link.desc}</p>
          <div className="mt-4 flex items-center text-sm text-blue-600">
            查看详情
            <ExternalLink className="w-4 h-4 ml-1" />
          </div>
        </Link>
      ))}
    </div>
  );
}

// 导航栏
function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="text-xl font-bold text-gray-900">TradeData Pro</span>
              <span className="hidden sm:inline text-xs text-gray-400 ml-2">专业出口数据分析</span>
            </div>
          </Link>
          
          <div className="flex items-center gap-1">
            <Link href="/" className="px-4 py-2 rounded-lg text-sm font-medium bg-blue-50 text-blue-600">
              首页
            </Link>
            <Link href="/products" className="px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
              商品数据
            </Link>
            <Link href="/customs" className="px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
              海关统计
            </Link>
            <Link href="/analytics" className="px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
              数据分析
            </Link>
            <Link href="/pricing" className="px-4 py-2 rounded-lg text-sm font-medium bg-gradient-to-r from-amber-100 to-orange-100 text-amber-700 hover:from-amber-200 hover:to-orange-200 transition-colors">
              升级会员
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

// 主页面
export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 标题 */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">中国出口商品数据概览</h1>
          <p className="mt-2 text-gray-500">实时追踪阿里巴巴1688和海关总署出口数据</p>
        </div>
        
        {/* 统计卡片 */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard title="商品总数" value="2,847,392" change="+12.5%" icon={Package} color="blue" />
          <StatCard title="今日新增" value="3,847" change="+8.2%" icon={Activity} color="green" />
          <StatCard title="出口总额" value="3,380" change="+4.6%" icon={DollarSign} color="purple" />
          <StatCard title="覆盖国家" value="200" change="+2.1%" icon={Globe} color="orange" />
        </div>
        
        {/* 图表区域 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2">
            <TrendChart />
          </div>
          <div>
            <CategoryChart />
          </div>
        </div>
        
        {/* 动态和排行 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <RealtimeUpdates />
          <RegionRanking />
        </div>
        
        {/* 快速入口 */}
        <QuickLinks />
      </main>
      
      {/* 页脚 */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-gray-900">TradeData Pro</span>
            </div>
            <p className="text-sm text-gray-500">2024 TradeData Pro. 专业出口数据分析平台</p>
            <div className="flex items-center gap-4 text-sm text-gray-500">
              <span>数据来源: 阿里巴巴1688 | 海关总署</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
