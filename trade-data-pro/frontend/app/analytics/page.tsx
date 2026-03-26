'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  TrendingUp, DollarSign, Users, Target, BarChart3, 
  PieChart, ArrowUpRight, ArrowDownRight, Calculator,
  Download, Filter, Search, Lightbulb, AlertCircle
} from 'lucide-react';
import { Navbar } from '@/app/components/Navbar';
import { StatCard } from '@/app/components/StatCard';
import { api } from '@/app/lib/api';
import { Product, ProfitAnalysis, CompetitionAnalysis } from '@/app/types';

// ===== 利润率计算器 =====
function ProfitCalculator() {
  const [costPrice, setCostPrice] = useState('');
  const [sellingPrice, setSellingPrice] = useState('');
  const [shippingCost, setShippingCost] = useState('');
  const [platformFee, setPlatformFee] = useState('5');
  const [monthlyVolume, setMonthlyVolume] = useState('');
  
  const calculate = () => {
    const cost = parseFloat(costPrice) || 0;
    const sell = parseFloat(sellingPrice) || 0;
    const ship = parseFloat(shippingCost) || 0;
    const fee = parseFloat(platformFee) || 0;
    const volume = parseInt(monthlyVolume) || 0;
    
    const profitPerUnit = sell - cost - ship - (sell * fee / 100);
    const profitMargin = sell > 0 ? (profitPerUnit / sell) * 100 : 0;
    const monthlyProfit = profitPerUnit * volume;
    const roi = cost > 0 ? (profitPerUnit / cost) * 100 : 0;
    
    return { profitPerUnit, profitMargin, monthlyProfit, roi };
  };
  
  const result = calculate();
  
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <Calculator className="w-5 h-5 text-blue-600" />
        <h3 className="text-lg font-bold text-gray-900">利润率计算器</h3>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">采购成本 (¥)</label>
          <input
            type="number"
            value={costPrice}
            onChange={(e) => setCostPrice(e.target.value)}
            className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="0.00"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">销售价 (¥)</label>
          <input
            type="number"
            value={sellingPrice}
            onChange={(e) => setSellingPrice(e.target.value)}
            className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="0.00"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">物流成本 (¥)</label>
          <input
            type="number"
            value={shippingCost}
            onChange={(e) => setShippingCost(e.target.value)}
            className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="0.00"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">平台费率 (%)</label>
          <input
            type="number"
            value={platformFee}
            onChange={(e) => setPlatformFee(e.target.value)}
            className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">预计月销量</label>
          <input
            type="number"
            value={monthlyVolume}
            onChange={(e) => setMonthlyVolume(e.target.value)}
            className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="100"
          />
        </div>
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-blue-50 rounded-lg p-4">
          <p className="text-sm text-gray-600">单品利润</p>
          <p className="text-xl font-bold text-blue-600">¥{result.profitPerUnit.toFixed(2)}</p>
        </div>
        <div className="bg-green-50 rounded-lg p-4">
          <p className="text-sm text-gray-600">利润率</p>
          <p className="text-xl font-bold text-green-600">{result.profitMargin.toFixed(1)}%</p>
        </div>
        <div className="bg-purple-50 rounded-lg p-4">
          <p className="text-sm text-gray-600">月利润</p>
          <p className="text-xl font-bold text-purple-600">¥{result.monthlyProfit.toLocaleString()}</p>
        </div>
        <div className="bg-orange-50 rounded-lg p-4">
          <p className="text-sm text-gray-600">ROI</p>
          <p className="text-xl font-bold text-orange-600">{result.roi.toFixed(1)}%</p>
        </div>
      </div>
    </motion.div>
  );
}

// ===== 选品评估工具 =====
function ProductEvaluator() {
  const [scores, setScores] = useState({
    demand: 7,
    competition: 5,
    profit: 7,
    trend: 6,
    logistics: 8,
  });
  
  const totalScore = Object.values(scores).reduce((a, b) => a + b, 0);
  const maxScore = 50;
  const percentage = (totalScore / maxScore) * 100;
  
  const getRating = (score: number) => {
    if (score >= 40) return { label: '强烈推荐', color: 'text-green-600', bg: 'bg-green-100' };
    if (score >= 30) return { label: '值得尝试', color: 'text-blue-600', bg: 'bg-blue-100' };
    if (score >= 20) return { label: '谨慎考虑', color: 'text-yellow-600', bg: 'bg-yellow-100' };
    return { label: '不建议', color: 'text-red-600', bg: 'bg-red-100' };
  };
  
  const rating = getRating(totalScore);
  
  const factors = [
    { key: 'demand', label: '市场需求', description: '市场容量和需求量' },
    { key: 'competition', label: '竞争程度', description: '低分=竞争激烈，高分=蓝海' },
    { key: 'profit', label: '利润空间', description: '毛利率和净利润' },
    { key: 'trend', label: '增长趋势', description: '市场增长趋势' },
    { key: 'logistics', label: '物流便利', description: '运输便利性和成本' },
  ];
  
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      className="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <Target className="w-5 h-5 text-purple-600" />
        <h3 className="text-lg font-bold text-gray-900">选品评估工具</h3>
      </div>
      
      <div className="mb-6">
        {factors.map((factor) => (
          <div key={factor.key} className="mb-4">
            <div className="flex justify-between items-center mb-1">
              <div>
                <span className="font-medium text-gray-900">{factor.label}</span>
                <span className="text-xs text-gray-400 ml-2">{factor.description}</span>
              </div>
              <span className="font-bold text-blue-600">{scores[factor.key as keyof typeof scores]}/10</span>
            </div>
            <input
              type="range"
              min="1"
              max="10"
              value={scores[factor.key as keyof typeof scores]}
              onChange={(e) => setScores({ ...scores, [factor.key]: parseInt(e.target.value) })}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
            />
          </div>
        ))}
      </div>
      
      <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
        <div>
          <p className="text-sm text-gray-600">综合评分</p>
          <p className="text-3xl font-bold text-gray-900">{totalScore}/{maxScore}</p>
        </div>
        <div className={`px-4 py-2 rounded-full ${rating.bg}`}>
          <span className={`font-bold ${rating.color}`}>{rating.label}</span>
        </div>
      </div>
    </motion.div>
  );
}

// ===== 市场洞察 =====
function MarketInsights() {
  const insights = [
    {
      type: 'trend',
      icon: TrendingUp,
      color: 'blue',
      title: '新能源产品持续火爆',
      description: '太阳能电池、锂电池、储能设备等新能源产品出口增长超过40%，建议重点关注。',
    },
    {
      type: 'alert',
      icon: AlertCircle,
      color: 'red',
      title: '传统纺织竞争加剧',
      description: '东南亚纺织产品竞争加剧，建议转向高附加值产品或寻找新的细分市场。',
    },
    {
      type: 'opportunity',
      icon: Lightbulb,
      color: 'yellow',
      title: '智能家居出口良机',
      description: '欧美市场对智能家居产品需求激增，智能门锁、智能照明、扫地机器人等产品机会大。',
    },
  ];
  
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <BarChart3 className="w-5 h-5 text-green-600" />
        <h3 className="text-lg font-bold text-gray-900">市场洞察</h3>
      </div>
      
      <div className="space-y-4">
        {insights.map((insight, index) => (
          <div key={index} className="flex gap-3 p-3 bg-gray-50 rounded-lg">
            <div className={`p-2 rounded-lg bg-${insight.color}-100`}>
              <insight.icon className={`w-5 h-5 text-${insight.color}-600`} />
            </div>
            <div>
              <h4 className="font-medium text-gray-900">{insight.title}</h4>
              <p className="text-sm text-gray-600 mt-1">{insight.description}</p>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

// ===== 主页面 =====
export default function AnalyticsPage() {
  const [stats, setStats] = useState({
    avgProfitMargin: 32.5,
    topCategory: '电子产品',
    growthLeader: '新能源',
    avgOrderValue: 2847,
  });
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* 标题 */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">数据分析中心</h1>
          <p className="mt-1 text-sm text-gray-500">专业的选品分析工具和市场洞察</p>
        </div>
        
        {/* 统计卡片 */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <StatCard 
            title="平均利润率" 
            value={`${stats.avgProfitMargin}%`} 
            change="+2.3%" 
            changeType="up" 
            icon={DollarSign} 
          />
          <StatCard 
            title="热门品类" 
            value={stats.topCategory} 
            change="稳定" 
            changeType="up" 
            icon={PieChart} 
          />
          <StatCard 
            title="增长冠军" 
            value={stats.growthLeader} 
            change="+45.6%" 
            changeType="up" 
            icon={TrendingUp} 
          />
          <StatCard 
            title="平均客单价" 
            value={`¥${stats.avgOrderValue}`} 
            change="+8.2%" 
            changeType="up" 
            icon={Users} 
          />
        </div>
        
        {/* 主要内容区 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ProfitCalculator />
          <ProductEvaluator />
          <div className="lg:col-span-2">
            <MarketInsights />
          </div>
        </div>
      </main>
    </div>
  );
}
