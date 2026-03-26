'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, Package, TrendingUp } from 'lucide-react';
import { Navbar } from '@/app/components/Navbar';
import Link from 'next/link';

export default function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetch('/api/products?pageSize=20')
      .then(r => r.json())
      .then(data => {
        setProducts(data.data || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const categories = ['all', '电子产品', '家居用品', '纺织服装', '新能源', '运动户外'];
  
  const filteredProducts = filter === 'all' 
    ? products 
    : products.filter((p: any) => p.category === filter);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">商品数据库</h1>
          <p className="mt-2 text-gray-500">基于1688和海关数据的真实产品信息</p>
        </div>

        {/* 筛选 */}
        <div className="flex flex-wrap gap-2 mb-6">
          {categories.map(cat => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                filter === cat 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              {cat === 'all' ? '全部' : cat}
            </button>
          ))}
        </div>

        {/* 产品网格 */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {Array.from({length: 8}).map((_, i) => (
              <div key={i} className="bg-white rounded-xl h-80 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {filteredProducts.map((product: any) => (
              <Link 
                key={product.id} 
                href={`/products/${product.id}`}
                className="group bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition-all"
              >
                <div className="p-4">
                  <div className="flex items-center justify-between mb-3">
                    <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                      {product.category}
                    </span>
                    {product.trend === 'up' && (
                      <span className="flex items-center text-xs text-green-600">
                        <TrendingUp className="w-3 h-3 mr-1" />
                        +{product.trendValue}%
                      </span>
                    )}
                  </div>
                  
                  <h3 className="font-bold text-gray-900 line-clamp-2 mb-2 group-hover:text-blue-600 transition-colors">
                    {product.name}
                  </h3>
                  
                  <p className="text-sm text-gray-500 mb-3">{product.subcategory}</p>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs text-gray-400">价格区间</p>
                      <p className="font-bold text-gray-900">¥{product.price?.min}-{product.price?.max}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-gray-400">MOQ</p>
                      <p className="font-medium text-gray-700">{product.moq} 件</p>
                    </div>
                  </div>
                  
                  <div className="mt-3 pt-3 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500">
                    <span>{product.supplier?.location}</span>
                    <span>月销 {product.salesVolume?.toLocaleString()}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {!loading && filteredProducts.length === 0 && (
          <div className="text-center py-20">
            <Package className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <p className="text-gray-500">暂无产品数据</p>
          </div>
        )}
      </main>
    </div>
  );
}
