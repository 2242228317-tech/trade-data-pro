'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  ArrowLeft, Heart, Share2, Star, MapPin, Package, TrendingUp, TrendingDown,
  CheckCircle, Building2, Calendar, Users, BarChart3, DollarSign, Target,
  AlertTriangle, Lightbulb, ChevronRight
} from 'lucide-react';
import { Navbar } from '@/app/components/Navbar';
import { LoadingSpinner, Skeleton } from '@/app/components/Loading';
import { TrendLineChart, TrendBarChart } from '@/app/components/Charts';
import { api } from '@/app/lib/api';
import { Product } from '@/app/types';
import {
  formatCurrency, formatNumber, formatPercent, cn,
  getTrendColor, getTrendBgColor, getRiskLevelColor, getRiskLevelText
} from '@/app/lib/utils';

export default function ProductDetailPage() {
  const params = useParams();
  const productId = params.id as string;
  
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    loadProduct();
  }, [productId]);

  const loadProduct = async () => {
    setLoading(true);
    try {
      const data = await api.getProduct(productId);
      setProduct(data);
    } catch (error) {
      console.error('Error loading product:', error);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'overview', name: '概览' },
    { id: 'profit', name: '利润分析' },
    { id: 'competition', name: '竞争分析' },
    { id: 'export', name: '出口数据' },
  ];

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

  if (!product) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 py-20 text-center">
          <h1 className="text-2xl font-bold text-gray-900">商品未找到</h1>
          <Link href="/products" className="text-blue-600 hover:underline mt-4 inline-block">
            返回商品列表
          </Link>
        </div>
      </div>
    );
  }

  const TrendIcon = product.trend === 'up' ? TrendingUp : product.trend === 'down' ? TrendingDown : null;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-sm text-gray-500 mb-6">
          <Link href="/" className="hover:text-gray-900">首页</Link>
          <ChevronRight className="w-4 h-4" />
          <Link href="/products" className="hover:text-gray-900">商品搜索</Link>
          <ChevronRight className="w-4 h-4" />
          <span className="text-gray-900">{product.name}</span>
        </div>

        {/* Product Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-6"
        >
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-6">
            {/* Product Image */}
            <div className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
              <Package className="w-24 h-24 text-gray-300" />
            </div>

            {/* Product Info */}
            <div className="lg:col-span-2">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs font-medium rounded">
                      {product.category}
                    </span>
                    <span className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs font-medium rounded">
                      {product.subcategory}
                    </span>
                  </div>
                  
                  <h1 className="text-2xl font-bold text-gray-900 mb-2">{product.name}</h1>
                  
                  <p className="text-gray-600 mb-4">{product.description}</p>
                  
                  <div className="flex items-center gap-4 mb-4">
                    <div className="flex items-center gap-1">
                      <Star className="w-5 h-5 text-yellow-400 fill-yellow-400" />
                      <span className="font-bold">{product.rating}</span>
                      <span className="text-gray-400">({formatNumber(product.reviewCount)}评价)</span>
                    </div>
                    
                    <div className={cn("flex items-center gap-1 px-2 py-1 rounded", getTrendBgColor(product.trend))}>
                      {TrendIcon && <TrendIcon className={cn("w-4 h-4", getTrendColor(product.trend))} />}
                      <span className={cn("font-medium text-sm", getTrendColor(product.trend))}>
                        {formatPercent(product.trendValue)}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setIsFavorite(!isFavorite)}
                    className={cn(
                      "p-2 rounded-lg transition-colors",
                      isFavorite ? "bg-red-50 text-red-500" : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                    )}
                  >
                    <Heart className={cn("w-5 h-5", isFavorite && "fill-current")} />
                  </button>
                  <button className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors">
                    <Share2 className="w-5 h-5" />
                  </button>
                </div>
              </div>

              {/* Price */}
              <div className="flex items-baseline gap-2 mb-4">
                <span className="text-3xl font-bold text-red-600">
                  {formatCurrency(product.price.min, product.price.currency)}
                </span>
                <span className="text-lg text-gray-400">
                  - {formatCurrency(product.price.max, product.price.currency)}
                </span>
                <span className="text-gray-400">/ {product.price.unit}</span>
              </div>

              {/* MOQ */}
              <div className="flex items-center gap-2 mb-4">
                <span className="text-gray-500">起订量:</span>
                <span className="font-medium">{product.moq} {product.price.unit}</span>
              </div>

              {/* Supplier Info */}
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                      <Building2 className="w-5 h-5 text-blue-600" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{product.supplier.name}</span>
                        {product.supplier.verified && (
                          <CheckCircle className="w-4 h-4 text-blue-500" />
                        )}
                      </div>
                      <div className="flex items-center gap-3 text-sm text-gray-500">
                        <span className="flex items-center gap-1">
                          <MapPin className="w-3 h-3" />
                          {product.supplier.location}
                        </span>
                        <span>{product.supplier.yearsInBusiness}年经验</span>
                        <span>评分 {product.supplier.rating}</span>
                      </div>
                    </div>
                  </div>
                  
                  <button className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors">
                    联系供应商
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="border-t border-gray-200">
            <div className="flex">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={cn(
                    "px-6 py-3 text-sm font-medium border-b-2 transition-colors",
                    activeTab === tab.id
                      ? "border-blue-600 text-blue-600"
                      : "border-transparent text-gray-500 hover:text-gray-700"
                  )}
                >
                  {tab.name}
                </button>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Tab Content */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
        >
          {activeTab === 'overview' && <OverviewTab product={product} />}
          {activeTab === 'profit' && product.profitAnalysis && <ProfitTab analysis={product.profitAnalysis} />}
          {activeTab === 'competition' && product.competitionAnalysis && <CompetitionTab analysis={product.competitionAnalysis} />}
          {activeTab === 'export' && product.exportData && <ExportTab data={product.exportData} />}
        </motion.div>
      </main>
    </div>
  );
}

function OverviewTab({ product }: { product: Product }) {
  const monthlyData = product.exportData?.slice(-12).map(d => ({
    month: d.month,
    value: d.exportValue / 10000,
    quantity: d.exportQuantity,
  })) || [];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4">产品规格</h3>
        <div className="grid grid-cols-2 gap-4">
          {Object.entries(product.specifications).map(([key, value]) => (
            <div key={key} className="flex justify-between py-2 border-b border-gray-100">
              <span className="text-gray-500">{key}</span>
              <span className="font-medium">{value}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4">销量趋势</h3>
        <TrendLineChart
          data={monthlyData}
          xKey="month"
          yKey="value"
          height={250}
        />
      </div>

      {product.profitAnalysis && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">利润概览</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-green-600">预估利润率</p>
              <p className="text-2xl font-bold text-green-700">{product.profitAnalysis.profitMargin}%</p>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-600">投资回报率</p>
              <p className="text-2xl font-bold text-blue-700">{product.profitAnalysis.roi}%</p>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg">
              <p className="text-sm text-purple-600">预估年利润</p>
              <p className="text-2xl font-bold text-purple-700">{formatCurrency(product.profitAnalysis.yearlyProfit)}</p>
            </div>
            <div className="p-4 bg-orange-50 rounded-lg">
              <p className="text-sm text-orange-600">风险评估</p>
              <p className={cn("text-2xl font-bold", getRiskLevelColor(product.profitAnalysis.riskLevel))}>
                {getRiskLevelText(product.profitAnalysis.riskLevel)}
              </p>
            </div>
          </div>
        </div>
      )}

      {product.competitionAnalysis && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">竞争概况</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-500">竞争对手数量</span>
              <span className="font-medium">{product.competitionAnalysis.competitorCount}家</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-500">市场集中度</span>
              <span className="font-medium">{product.competitionAnalysis.marketConcentration === 'high' ? '高' : product.competitionAnalysis.marketConcentration === 'medium' ? '中' : '低'}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-500">市场份额</span>
              <span className="font-medium">{product.competitionAnalysis.marketShare}%</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-500">进入壁垒</span>
              <span className={cn(
                "font-medium",
                product.competitionAnalysis.entryBarrier === 'high' ? 'text-red-600' :
                product.competitionAnalysis.entryBarrier === 'medium' ? 'text-yellow-600' : 'text-green-600'
              )}>
                {product.competitionAnalysis.entryBarrier === 'high' ? '高' : product.competitionAnalysis.entryBarrier === 'medium' ? '中' : '低'}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function ProfitTab({ analysis }: { analysis: NonNullable<Product['profitAnalysis']> }) {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <DollarSign className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">预估成本</p>
              <p className="text-xl font-bold">{formatCurrency(analysis.estimatedCost)}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <DollarSign className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">建议售价</p>
              <p className="text-xl font-bold">{formatCurrency(analysis.estimatedSellingPrice)}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <Target className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">单件利润</p>
              <p className="text-xl font-bold text-green-600">
                {formatCurrency(analysis.estimatedSellingPrice - analysis.estimatedCost)}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">利润分析详情</h3>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center py-3 border-b border-gray-100">
              <span className="text-gray-600">利润率</span>
              <span className="text-xl font-bold text-green-600">{analysis.profitMargin}%</span>
            </div>
            
            <div className="flex justify-between items-center py-3 border-b border-gray-100">
              <span className="text-gray-600">投资回报率 (ROI)</span>
              <span className="font-medium">{analysis.roi}%</span>
            </div>
            
            <div className="flex justify-between items-center py-3 border-b border-gray-100">
              <span className="text-gray-600">盈亏平衡数量</span>
              <span className="font-medium">{formatNumber(analysis.breakEvenQuantity)} 件</span>
            </div>
            
            <div className="flex justify-between items-center py-3 border-b border-gray-100">
              <span className="text-gray-600">回本周期</span>
              <span className="font-medium">{analysis.paybackPeriod} 个月</span>
            </div>
            
            <div className="flex justify-between items-center py-3">
              <span className="text-gray-600">风险评估</span>
              <span className={cn("px-3 py-1 rounded-full text-sm font-medium", getRiskLevelColor(analysis.riskLevel))}>
                {getRiskLevelText(analysis.riskLevel)}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">收益预测</h3>
          
          <div className="space-y-4">
            <div className="p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-green-600">预计月利润</p>
                  <p className="text-2xl font-bold text-green-700">{formatCurrency(analysis.monthlyProfit)}</p>
                </div>
                <DollarSign className="w-10 h-10 text-green-200" />
              </div>
            </div>
            
            <div className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-blue-600">预计年利润</p>
                  <p className="text-2xl font-bold text-blue-700">{formatCurrency(analysis.yearlyProfit)}</p>
                </div>
                <BarChart3 className="w-10 h-10 text-blue-200" />
              </div>
            </div>
          </div>
          
          <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
            <div className="flex items-start gap-3">
              <Lightbulb className="w-5 h-5 text-yellow-600 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-yellow-800">选品建议</p>
                <p className="text-sm text-yellow-700 mt-1">
                  {analysis.profitMargin > 40 
                    ? '该产品利润率优秀，建议重点关注。'
                    : analysis.profitMargin > 25
                    ? '该产品利润率良好，具备投资价值。'
                    : '该产品利润率一般，建议谨慎评估。'}
                  {analysis.riskLevel === 'low' 
                    ? '风险较低，适合新手入行。'
                    : analysis.riskLevel === 'medium'
                    ? '风险适中，需要一定的运营经验。'
                    : '风险较高，建议有丰富经验的卖家操作。'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function CompetitionTab({ analysis }: { analysis: NonNullable<Product['competitionAnalysis']> }) {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-500">竞争对手</p>
          <p className="text-2xl font-bold">{analysis.competitorCount}</p>
          <p className="text-xs text-gray-400 mt-1">家供应商</p>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-500">市场份额</p>
          <p className="text-2xl font-bold text-blue-600">{analysis.marketShare}%</p>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-500">平均价格</p>
          <p className="text-2xl font-bold">{formatCurrency(analysis.priceRange.average)}</p>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-500">进入壁垒</p>
          <p className={cn(
            "text-2xl font-bold",
            analysis.entryBarrier === 'high' ? 'text-red-600' :
            analysis.entryBarrier === 'medium' ? 'text-yellow-600' : 'text-green-600'
          )}>
            {analysis.entryBarrier === 'high' ? '高' : analysis.entryBarrier === 'medium' ? '中' : '低'}
          </p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4">主要竞争对手</h3>
        
        <div className="space-y-4">
          {analysis.topCompetitors.map((competitor, index) => (
            <div key={competitor.id} className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
              <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                {index + 1}
              </div>
              
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-medium">{competitor.name}</span>
                  <span className={cn(
                    "px-2 py-0.5 text-xs rounded",
                    competitor.priceLevel === 'premium' ? 'bg-purple-100 text-purple-700' :
                    competitor.priceLevel === 'medium' ? 'bg-blue-100 text-blue-700' :
                    'bg-green-100 text-green-700'
                  )}>
                    {competitor.priceLevel === 'premium' ? '高端' : competitor.priceLevel === 'medium' ? '中端' : '低端'}
                  </span>
                </div>
                
                <div className="flex items-center gap-4 mt-1 text-sm">
                  <span className="text-gray-500">市场份额: {competitor.marketShare}%</span>
                </div>
              </div>
              
              <div className="text-right text-sm">
                <p className="text-green-600">优势: {competitor.strength}</p>
                <p className="text-red-600">劣势: {competitor.weakness}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">价格分布</h3>
          
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">最低价格</span>
              <span className="font-medium">{formatCurrency(analysis.priceRange.min)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">最高价格</span>
              <span className="font-medium">{formatCurrency(analysis.priceRange.max)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">平均价格</span>
              <span className="font-medium">{formatCurrency(analysis.priceRange.average)}</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">市场分析</h3>
          
          <div className="space-y-4">
            <div className="p-3 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-800">
                <strong>市场集中度:</strong> {analysis.marketConcentration === 'high' ? '高 - 头部效应明显' : analysis.marketConcentration === 'medium' ? '中 - 竞争较为均衡' : '低 - 市场分散'}
              </p>
            </div>
            
            <div className="p-3 bg-yellow-50 rounded-lg">
              <p className="text-sm text-yellow-800">
                <strong>竞争建议:</strong> {' '}
                {analysis.marketConcentration === 'high' 
                  ? '市场已被头部占据，建议寻找细分市场或差异化竞争。'
                  : analysis.marketConcentration === 'medium'
                  ? '市场竞争均衡，通过优化产品和服务可以获取份额。'
                  : '市场较为分散，是进入的好时机，建议快速建立品牌。'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ExportTab({ data }: { data: NonNullable<Product['exportData']> }) {
  const chartData = data.slice(-12).map(d => ({
    month: d.month,
    value: d.exportValue / 10000,
    quantity: d.exportQuantity,
    growth: d.growthRate,
  }));

  const countryData = data.reduce((acc, item) => {
    if (!acc[item.destinationCountry]) {
      acc[item.destinationCountry] = { value: 0, count: 0 };
    }
    acc[item.destinationCountry].value += item.exportValue;
    acc[item.destinationCountry].count += 1;
    return acc;
  }, {} as Record<string, { value: number; count: number }>);

  const topCountries = Object.entries(countryData)
    .map(([name, stats]) => ({ name, value: stats.value / 10000 }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 10);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-500">年度出口额</p>
          <p className="text-2xl font-bold">{formatCurrency(data.reduce((sum, d) => sum + d.exportValue, 0))}</p>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-500">出口总量</p>
          <p className="text-2xl font-bold">{formatNumber(data.reduce((sum, d) => sum + d.exportQuantity, 0))} 件</p>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <p className="text-sm text-gray-500">平均单价</p>
          <p className="text-2xl font-bold">
            {formatCurrency(data.reduce((sum, d) => sum + d.unitPrice, 0) / data.length)}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">出口趋势</h3>
          <TrendLineChart
            data={chartData}
            xKey="month"
            yKey="value"
            height={300}
          />
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">出口目的地 TOP10</h3>
          <TrendBarChart
            data={topCountries}
            xKey="name"
            yKey="value"
            height={300}
          />
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-bold text-gray-900">出口明细</h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">月份</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">目的地</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">出口额</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">数量</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">增长率</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {data.slice(0, 20).map((record) => (
                <tr key={record.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm">{record.year}年{record.month}</td>
                  <td className="px-6 py-4 text-sm">{record.destinationCountry}</td>
                  <td className="px-6 py-4 text-sm text-right">{formatCurrency(record.exportValue)}</td>
                  <td className="px-6 py-4 text-sm text-right">{formatNumber(record.exportQuantity)}</td>
                  <td className={cn(
                    "px-6 py-4 text-sm text-right font-medium",
                    record.growthRate > 0 ? 'text-green-600' : record.growthRate < 0 ? 'text-red-600' : 'text-gray-600'
                  )}>
                    {record.growthRate > 0 ? '+' : ''}{record.growthRate}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
