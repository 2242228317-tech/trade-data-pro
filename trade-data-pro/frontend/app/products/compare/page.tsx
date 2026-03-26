'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  ArrowLeft, X, Check, Star, TrendingUp, TrendingDown, DollarSign,
  Package, MapPin, Building2, ChevronRight, Download
} from 'lucide-react';
import { Navbar } from '@/app/components/Navbar';
import { LoadingSpinner } from '@/app/components/Loading';
import { api } from '@/app/lib/api';
import { Product } from '@/app/types';
import {
  formatCurrency, formatNumber, formatPercent, cn,
  getTrendColor, getTrendBgColor, getRiskLevelColor, getRiskLevelText
} from '@/app/lib/utils';

export default function ComparePage() {
  const searchParams = useSearchParams();
  const ids = searchParams.get('ids')?.split(',') || [];
  
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    if (ids.length === 0) return;
    
    setLoading(true);
    try {
      const loaded = await Promise.all(
        ids.map(id => api.getProduct(id))
      );
      setProducts(loaded.filter(Boolean));
    } catch (error) {
      console.error('Error loading products:', error);
    } finally {
      setLoading(false);
    }
  };

  const removeProduct = (id: string) => {
    setProducts(prev => prev.filter(p => p.id !== id));
  };

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

  if (products.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 py-20 text-center">
          <h1 className="text-2xl font-bold text-gray-900">没有可对比的商品</h1>
          <Link href="/products" className="text-blue-600 hover:underline mt-4 inline-block">
            去添加商�?          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-6"
        >
          <div className="flex items-center gap-4">
            <Link
              href="/products"
              className="flex items-center gap-1 text-gray-500 hover:text-gray-900"
            >
              <ArrowLeft className="w-4 h-4" />
              返回
            </Link>
            
            <h1 className="text-2xl font-bold">商品对比</h1>
          </div>
          
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700">
            <Download className="w-4 h-4" />
            导出对比
          </button>
        </motion.div>

        {/* Comparison Table */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
        >
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr>
                  <th className="px-6 py-4 text-left bg-gray-50 sticky left-0 z-10 min-w-[150px]">对比�?/th>
                  {products.map((product) => (
                    <th key={product.id} className="px-4 py-4 text-center bg-gray-50 min-w-[200px]">
                      <div className="relative">
                        <button
                          onClick={() => removeProduct(product.id)}
                          className="absolute -top-2 -right-2 w-6 h-6 bg-red-100 text-red-600 rounded-full flex items-center justify-center hover:bg-red-200"
                        >
                          <X className="w-3 h-3" />
                        </button>
                        
                        <div className="aspect-square bg-gray-100 rounded-lg mb-2 flex items-center justify-center">
                          <Package className="w-8 h-8 text-gray-300" />
                        </div>
                        
                        <Link
                          href={`/products/${product.id}`}
                          className="font-medium text-blue-600 hover:underline line-clamp-2"
                        >
                          {product.name}
                        </Link>
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              
              <tbody className="divide-y divide-gray-200">
                {/* Price */}
                <tr>
                  <td className="px-6 py-4 font-medium bg-white sticky left-0 z-10">价格区间</td>
                  {products.map((product) => (
                    <td key={product.id} className="px-4 py-4 text-center">
                      <div className="text-lg font-bold text-red-600">
                        {formatCurrency(product.price.min, product.price.currency)}
                      </div>
                      <div className="text-sm text-gray-400">
                        - {formatCurrency(product.price.max, product.price.currency)}
                      </div>
                    </td>
                  ))}
                </tr>

                {/* MOQ */}
                <tr className="bg-gray-50/50">
                  <td className="px-6 py-4 font-medium bg-gray-50/50 sticky left-0 z-10">起订�?/td>
                  {products.map((product) => (
                    <td key={product.id} className="px-4 py-4 text-center">
                      {product.moq} {product.price.unit}
                    </td>
                  ))}
                </tr>

                {/* Rating */}
                <tr>
                  <td className="px-6 py-4 font-medium bg-white sticky left-0 z-10">评分</td>
                  {products.map((product) => (
                    <td key={product.id} className="px-4 py-4 text-center">
                      <div className="flex items-center justify-center gap-1">
                        <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                        <span className="font-bold">{product.rating}</span>
                      </div>
                      <div className="text-sm text-gray-400">({formatNumber(product.reviewCount)}评价)</div>
                    </td>
                  ))}
                </tr>

                {/* Sales */}
                <tr className="bg-gray-50/50">
                  <td className="px-6 py-4 font-medium bg-gray-50/50 sticky left-0 z-10">销�?/td>
                  {products.map((product) => (
                    <td key={product.id} className="px-4 py-4 text-center">
                      {formatNumber(product.salesVolume)}
                    </td>
                  ))}
                </tr>

                {/* Trend */}
                <tr>
                  <td className="px-6 py-4 font-medium bg-white sticky left-0 z-10">趋势</td>
                  {products.map((product) => {
                    const TrendIcon = product.trend === 'up' ? TrendingUp : TrendingDown;
                    return (
                      <td key={product.id} className="px-4 py-4 text-center">
                        <div className={cn(
                          "inline-flex items-center gap-1 px-2 py-1 rounded",
                          getTrendBgColor(product.trend)
                        )}>
                          <TrendIcon className={cn("w-4 h-4", getTrendColor(product.trend))} />
                          <span className={getTrendColor(product.trend)}>
                            {formatPercent(product.trendValue)}
                          </span>
                        </div>
                      </td>
                    );
                  })}
                </tr>

                {/* Profit */}
                {products.some(p => p.profitAnalysis) && (
                  <>
                    <tr className="bg-gray-50/50">
                      <td className="px-6 py-4 font-medium bg-gray-50/50 sticky left-0 z-10">利润�?/td>
                      {products.map((product) => (
                        <td key={product.id} className="px-4 py-4 text-center">
                          {product.profitAnalysis ? (
                            <span className={cn(
                              "font-bold",
                              product.profitAnalysis.profitMargin >= 30 ? 'text-green-600' : 'text-yellow-600'
                            )}>
                              {product.profitAnalysis.profitMargin}%
                            </span>
                          ) : (
                            '-'
                          )}
                        </td>
                      ))}
                    </tr>

                    <tr>
                      <td className="px-6 py-4 font-medium bg-white sticky left-0 z-10">预估年利�?/td>
                      {products.map((product) => (
                        <td key={product.id} className="px-4 py-4 text-center">
                          {product.profitAnalysis ? (
                            <span className="font-bold text-blue-600">
                              {formatCurrency(product.profitAnalysis.yearlyProfit)}
                            </span>
                          ) : (
                            '-'
                          )}
                        </td>
                      ))}
                    </tr>

                    <tr className="bg-gray-50/50">
                      <td className="px-6 py-4 font-medium bg-gray-50/50 sticky left-0 z-10">风险等级</td>
                      {products.map((product) => (
                        <td key={product.id} className="px-4 py-4 text-center">
                          {product.profitAnalysis ? (
                            <span className={cn(
                              "px-2 py-1 rounded text-sm font-medium",
                              getRiskLevelColor(product.profitAnalysis.riskLevel)
                            )}>
                              {getRiskLevelText(product.profitAnalysis.riskLevel)}
                            </span>
                          ) : (
                            '-'
                          )}
                        </td>
                      ))}
                    </tr>
                  </>
                )}

                {/* Competition */}
                {products.some(p => p.competitionAnalysis) && (
                  <>
                    <tr>
                      <td className="px-6 py-4 font-medium bg-white sticky left-0 z-10">竞争对手</td>
                      {products.map((product) => (
                        <td key={product.id} className="px-4 py-4 text-center">
                          {product.competitionAnalysis ? (
                            <span>{product.competitionAnalysis.competitorCount} �?/span>
                          ) : (
                            '-'
                          )}
                        </td>
                      ))}
                    </tr>

                    <tr className="bg-gray-50/50">
                      <td className="px-6 py-4 font-medium bg-gray-50/50 sticky left-0 z-10">市场份额</td>
                      {products.map((product) => (
                        <td key={product.id} className="px-4 py-4 text-center">
                          {product.competitionAnalysis ? (
                            <span>{product.competitionAnalysis.marketShare}%</span>
                          ) : (
                            '-'
                          )}
                        </td>
                      ))}
                    </tr>
                  </>
                )}

                {/* Supplier */}
                <tr>
                  <td className="px-6 py-4 font-medium bg-white sticky left-0 z-10">供应�?/td>
                  {products.map((product) => (
                    <td key={product.id} className="px-4 py-4 text-center">
                      <div className="flex items-center justify-center gap-1">
                        <Building2 className="w-4 h-4 text-gray-400" />
                        <span>{product.supplier.name.slice(0, 10)}...</span>
                      </div>
                      <div className="text-sm text-gray-400">
                        <MapPin className="w-3 h-3 inline" /> {product.supplier.location}
                      </div>
                    </td>
                  ))}
                </tr>

                {/* Actions */}
                <tr className="bg-gray-50/50">
                  <td className="px-6 py-4 font-medium bg-gray-50/50 sticky left-0 z-10">操作</td>
                  {products.map((product) => (
                    <td key={product.id} className="px-4 py-4 text-center">
                      <Link
                        href={`/products/${product.id}`}
                        className="inline-flex items-center gap-1 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700"
                      >
                        查看详情
                        <ChevronRight className="w-4 h-4" />
                      </Link>
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        </motion.div>

        {/* Summary */}
        {products.length >= 2 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mt-6 bg-blue-50 rounded-xl p-6"
          >
            <h3 className="text-lg font-bold text-blue-900 mb-4">对比结论</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-blue-600 mb-1">最佳利润率</p>
                {(() => {
                  const best = products
                    .filter(p => p.profitAnalysis)
                    .sort((a, b) => (b.profitAnalysis?.profitMargin || 0) - (a.profitAnalysis?.profitMargin || 0))[0];
                  return best ? (
                    <p className="font-medium text-blue-900">{best.name.slice(0, 20)}...</p>
                  ) : (
                    <p className="text-gray-400">暂无数据</p>
                  );
                })()}
              </div>
              
              <div>
                <p className="text-sm text-blue-600 mb-1">最佳趋�?/p>
                {(() => {
                  const best = products.sort((a, b) => b.trendValue - a.trendValue)[0];
                  return (
                    <p className="font-medium text-blue-900">{best.name.slice(0, 20)}...</p>
                  );
                })()}
              </div>
              
              <div>
                <p className="text-sm text-blue-600 mb-1">最低竞�?/p>
                {(() => {
                  const best = products
                    .filter(p => p.competitionAnalysis)
                    .sort((a, b) => (a.competitionAnalysis?.competitorCount || 0) - (b.competitionAnalysis?.competitorCount || 0))[0];
                  return best ? (
                    <p className="font-medium text-blue-900">{best.name.slice(0, 20)}...</p>
                  ) : (
                    <p className="text-gray-400">暂无数据</p>
                  );
                })()}
              </div>
            </div>
          </motion.div>
        )}
      </main>
    </div>
  );
}
