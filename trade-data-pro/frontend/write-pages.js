const fs = require('fs');

// Write all page files with proper UTF-8 encoding
const files = {
  'app/page.tsx': `'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import {
  TrendingUp, Package, Globe, DollarSign,
  Activity, Search, Filter, Download, MapPin, Award, Zap,
  BarChart3, ArrowRight, Star
} from 'lucide-react';
import { Navbar } from '@/app/components/Navbar';
import { StatCard } from '@/app/components/StatCard';
import { ProductCard } from '@/app/components/ProductCard';
import { LoadingSpinner } from '@/app/components/Loading';
import { TrendLineChart, TrendBarChart, TrendPieChart } from '@/app/components/Charts';
import { api } from '@/app/lib/api';

export default function Home() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [trending, setTrending] = useState([]);
  const [categories, setCategories] = useState([]);
  const [regions, setRegions] = useState([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const data = await api.getDashboard();
      setStats(data.stats);
      setTrending(data.trending);
      setCategories(data.categories);
      setRegions(data.regions);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
  const trendData = months.map((month, i) => ({
    month,
    value: 295 + i * 8 + Math.random() * 20,
  }));

  const categoryChartData = categories.slice(0, 6).map(cat => ({
    name: cat.name,
    value: cat.value / 10000,
  }));

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex items-center justify-center py-20">
          <LoadingSpinner size="lg" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6"
        >
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-yellow-100 rounded-lg">
              <Activity className="w-4 h-4 text-yellow-600" />
            </div>
            <h1 className="text-xl font-bold text-gray-900">中国出口商品数据概览</h1>
          </div>
          <p className="mt-1 text-sm text-gray-500">实时追踪阿里巴巴1688和海关总署出口数据</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6"
        >
          <StatCard
            title="商品总数"
            value={stats?.totalProducts || 0}
            change={12.5}
            changeType="up"
            icon={Package}
            format="number"
          />
          <StatCard
            title="今日新增"
            value={stats?.dailyNewProducts || 0}
            change={8.2}
            changeType="up"
            icon={Activity}
            format="number"
          />
          <StatCard
            title="出口总额"
            value={stats?.totalExportValue || 0}
            change={4.6}
            changeType="up"
            icon={DollarSign}
            format="currency"
            valuePrefix="$"
            valueSuffix="B"
          />
          <StatCard
            title="覆盖国家"
            value={stats?.coveredCountries || 0}
            change={2.1}
            changeType="up"
            icon={Globe}
            format="number"
            valueSuffix="+"
          />
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 h-full">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Globe className="w-4 h-4 text-blue-600" />
                  <h3 className="text-sm font-bold">全球出口热力图</h3>
                </div>
                <span className="text-xs text-gray-400">单位：亿美元</span>
              </div>

              <div className="h-80 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <Globe className="w-16 h-16 mx-auto mb-3 text-blue-300" />
                  <p className="text-gray-500">全球出口热力图</p>
                  <div className="mt-4 grid grid-cols-2 gap-x-8 gap-y-2 text-sm">
                    {regions.slice(0, 6).map((region) => (
                      <div key={region.name} className="flex items-center justify-between">
                        <span className="text-gray-600">{region.name}</span>
                        <span className="font-medium text-blue-600">${(region.exportValue / 1000000000).toFixed(1)}B</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <TrendLineChart
              data={trendData}
              xKey="month"
              yKey="value"
              title="2024年出口趋势"
              height={220}
            />

            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
              <div className="flex items-center gap-2 mb-2">
                <BarChart3 className="w-4 h-4 text-purple-600" />
                <h3 className="text-sm font-bold">品类分布</h3>
              </div>
              <TrendPieChart
                data={categoryChartData}
                nameKey="name"
                valueKey="value"
                height={200}
              />
            </div>
          </div>

          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Award className="w-4 h-4 text-orange-600" />
                  <h3 className="text-sm font-bold">热门出口商品</h3>
                </div>
                <Link href="/products" className="text-xs text-blue-600 hover:underline">
                  查看全部
                </Link>
              </div>

              <div className="space-y-2">
                {trending.slice(0, 6).map((product, index) => (
                  <Link
                    key={product.id}
                    href={'/products/' + product.id}
                    className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <div className={'w-6 h-6 rounded flex items-center justify-center text-xs font-bold ' + (index < 3 ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600')}>
                      {index + 1}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">{product.name}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-bold">{product.trendValue}%</p>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>

          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4 text-green-600" />
                  <h3 className="text-sm font-bold">精选推荐</h3>
                </div>
                <Link href="/analytics" className="text-xs text-blue-600 hover:underline">
                  查看更多
                </Link>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {trending.slice(0, 4).map((product) => (
                  <ProductCard key={product.id} product={product} showActions={false} />
                ))}
              </div>
            </div>
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-6 bg-gradient-to-r from-slate-800 to-slate-900 rounded-xl p-6 text-white"
        >
          <h3 className="font-bold mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-400" />
            快速开始
          </h3>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { icon: Search, label: '商品搜索', href: '/products', color: 'bg-blue-500' },
              { icon: Filter, label: '高级筛选', href: '/products', color: 'bg-emerald-500' },
              { icon: BarChart3, label: '数据分析', href: '/analytics', color: 'bg-violet-500' },
              { icon: Download, label: '导出报表', href: '/customs', color: 'bg-orange-500' },
            ].map((action) => (
              <Link
                key={action.label}
                href={action.href}
                className="flex items-center gap-3 p-3 bg-white/10 hover:bg-white/20 rounded-lg transition-colors"
              >
                <div className={action.color + ' p-2 rounded'}>
                  <action.icon className="w-4 h-4" />
                </div>
                <span className="font-medium">{action.label}</span>
              </Link>
            ))}
          </div>
        </motion.div>
      </main>

      <footer className="bg-white border-t border-gray-200 mt-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-2 text-sm text-gray-500">
            <p>2024 TradeData Pro. 专业出口数据分析平台</p>
            <p>数据来源：阿里巴巴1688 | 海关总署</p>
          </div>
        </div>
      </footer>
    </div>
  );
}`
};

Object.entries(files).forEach(([path, content]) => {
  fs.writeFileSync(path, content, { encoding: 'utf8' });
  console.log('Written:', path);
});

console.log('All files written successfully!');
