'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Search, Filter, TrendingUp, DollarSign, Globe, Package,
  Star, ArrowUpRight, Download, Heart, BarChart3, Lightbulb,
  ChevronRight, Sparkles, Target, Clock
} from 'lucide-react';
import { Navbar } from '@/app/components/Navbar';
import { api } from '@/app/lib/api';
import { Product } from '@/app/types';

// ===== 选品卡片 =====
function ProductResearchCard({ product, onFavorite, isFavorite }: { 
  product: Product; 
  onFavorite: (id: string) => void;
  isFavorite: boolean;
}) {
  const [showDetails, setShowDetails] = useState(false);
  
  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-600 bg-green-100';
    if (score >= 6) return 'text-blue-600 bg-blue-100';
    if (score >= 4) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };
  
  const researchScore = Math.floor(Math.random() * 5) + 5; // Mock score 5-10
  
  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow"
    >
      <div className="p-4">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getScoreColor(researchScore)}`}>
              选品评分 {researchScore}/10
            </span>
            {product.trend === 'up' && (
              <span className="px-2 py-1 rounded-full text-xs font-medium text-green-600 bg-green-100">
                趋势上升
              </span>
            )}
          </div>
          <button
            onClick={() => onFavorite(product.id)}
            className="p-1.5 rounded-full hover:bg-gray-100 transition-colors"
          >
            <Heart className={`w-5 h-5 ${isFavorite ? 'fill-red-500 text-red-500' : 'text-gray-400'}`} />
          </button>
        </div>
        
        <div className="mb-3">
          <h3 className="font-bold text-gray-900 line-clamp-2">{product.name}</h3>
          <p className="text-sm text-gray-500">{product.category} · {product.subcategory}</p>
        </div>
        
        <div className="grid grid-cols-2 gap-2 mb-3">
          <div className="bg-gray-50 rounded-lg p-2">
            <p className="text-xs text-gray-500">价格区间</p>
            <p className="font-bold text-gray-900">¥{product.price.min}-{product.price.max}</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-2">
            <p className="text-xs text-gray-500">MOQ</p>
            <p className="font-bold text-gray-900">{product.moq} 件</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-2">
            <p className="text-xs text-gray-500">月销量</p>
            <p className="font-bold text-gray-900">{product.salesVolume.toLocaleString()}</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-2">
            <p className="text-xs text-gray-500">供应商</p>
            <p className="font-bold text-gray-900 truncate">{product.supplier.name.slice(0, 6)}...</p>
          </div>
        </div>
        
        {showDetails && (
          <motion.div 
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="border-t border-gray-100 pt-3 mt-3"
          >
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">供应商评分</span>
                <span className="font-medium">{product.supplier.rating}/5.0 {product.supplier.verified && '✓ 已认证'}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">产品评分</span>
                <span className="font-medium">{product.rating}/5.0 ({product.reviewCount} 评价)</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">产地</span>
                <span className="font-medium">{product.region}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">趋势</span>
                <span className={`font-medium ${product.trendValue > 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {product.trendValue > 0 ? '+' : ''}{product.trendValue}%
                </span>
              </div>
            </div>
          </motion.div>
        )}
        
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="w-full mt-3 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
        >
          {showDetails ? '收起详情' : '查看详情'}
        </button>
      </div>
    </motion.div>
  );
}

// ===== 筛选面板 =====
function FilterPanel({ filters, onChange }: { 
  filters: any; 
  onChange: (filters: any) => void;
}) {
  const categories = ['全部', '电子产品', '机械设备', '纺织服装', '化工产品', '农产品', '家居用品'];
  const priceRanges = [
    { label: '全部', min: undefined, max: undefined },
    { label: '¥0-100', min: 0, max: 100 },
    { label: '¥100-500', min: 100, max: 500 },
    { label: '¥500-1000', min: 500, max: 1000 },
    { label: '¥1000+', min: 1000, max: undefined },
  ];
  const sortOptions = [
    { value: 'score', label: '选品评分' },
    { value: 'sales', label: '销量' },
    { value: 'profit', label: '利润潜力' },
    { value: 'trend', label: '趋势' },
    { value: 'newest', label: '最新' },
  ];
  
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
      <div className="flex items-center gap-2 mb-4">
        <Filter className="w-5 h-5 text-blue-600" />
        <h3 className="font-bold text-gray-900">筛选条件</h3>
      </div>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">品类</label>
          <div className="flex flex-wrap gap-2">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => onChange({ ...filters, category: cat === '全部' ? '' : cat })}
                className={`px-3 py-1.5 rounded-full text-sm transition-colors ${
                  filters.category === cat || (cat === '全部' && !filters.category)
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">价格区间</label>
          <div className="flex flex-wrap gap-2">
            {priceRanges.map((range) => (
              <button
                key={range.label}
                onClick={() => onChange({ ...filters, priceRange: range.label })}
                className={`px-3 py-1.5 rounded-full text-sm transition-colors ${
                  filters.priceRange === range.label
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {range.label}
              </button>
            ))}
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">排序</label>
          <select
            value={filters.sortBy}
            onChange={(e) => onChange({ ...filters, sortBy: e.target.value })}
            className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            {sortOptions.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>
        
        <div className="flex items-center gap-2 pt-2 border-t border-gray-100">
          <input
            type="checkbox"
            id="verified-only"
            checked={filters.verifiedOnly}
            onChange={(e) => onChange({ ...filters, verifiedOnly: e.target.checked })}
            className="rounded text-blue-600"
          />
          <label htmlFor="verified-only" className="text-sm text-gray-700">
            仅显示认证供应商
          </label>
        </div>
      </div>
    </div>
  );
}

// ===== 主页面 =====
export default function ProductResearchPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [favorites, setFavorites] = useState<Set<string>>(new Set());
  const [filters, setFilters] = useState({
    category: '',
    priceRange: '全部',
    sortBy: 'score',
    verifiedOnly: false,
  });
  
  useEffect(() => {
    loadProducts();
  }, [filters]);
  
  const loadProducts = async () => {
    setLoading(true);
    try {
      const data = await api.searchProducts({
        category: filters.category,
        sortBy: filters.sortBy as any,
        page: 1,
        pageSize: 12,
      });
      setProducts(data.data);
    } catch (error) {
      console.error('Failed to load products:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const toggleFavorite = (id: string) => {
    setFavorites((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };
  
  const tips = [
    {
      icon: Lightbulb,
      color: 'yellow',
      title: '选品黄金法则',
      content: '高需求 + 低竞争 + 高利润 = 理想产品',
    },
    {
      icon: Target,
      color: 'blue',
      title: '关注长尾品类',
      content: '细分领域往往竞争更小，利润空间更大',
    },
    {
      icon: TrendingUp,
      color: 'green',
      title: '把握趋势',
      content: '上升趋势的产品更容易获得成功',
    },
    {
      icon: Clock,
      color: 'purple',
      title: '季节性考量',
      content: '注意产品的季节性特征，提前布局',
    },
  ];
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* 标题区 */}
        <div className="mb-6">
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-yellow-500" />
            <h1 className="text-2xl font-bold text-gray-900">智能选品工具</h1>
          </div>
          <p className="mt-1 text-sm text-gray-500">
            基于大数据分析的选品推荐系统，助你发现潜力产品
          </p>
        </div>
        
        {/* 选品技巧 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {tips.map((tip, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-xl p-4 shadow-sm border border-gray-100"
            >
              <div className={`w-10 h-10 rounded-lg bg-${tip.color}-100 flex items-center justify-center mb-3`}>
                <tip.icon className={`w-5 h-5 text-${tip.color}-600`} />
              </div>
              <h3 className="font-bold text-gray-900 mb-1">{tip.title}</h3>
              <p className="text-sm text-gray-600">{tip.content}</p>
            </motion.div>
          ))}
        </div>
        
        {/* 主要内容 */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* 侧边栏筛选 */}
          <div className="lg:col-span-1">
            <FilterPanel filters={filters} onChange={setFilters} />
            
            <div className="mt-4 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl p-4 text-white">
              <h4 className="font-bold mb-2">专业版功能</h4>
              <ul className="text-sm space-y-1 opacity-90">
                <li>• 竞品监控</li>
                <li>• 价格追踪</li>
                <li>• 供应商评级</li>
                <li>• 市场预测</li>
              </ul>
              <button className="mt-3 w-full py-2 bg-white text-blue-600 rounded-lg text-sm font-medium hover:bg-blue-50 transition-colors">
                升级专业版
              </button>
            </div>
          </div>
          
          {/* 产品列表 */}
          <div className="lg:col-span-3">
            <div className="flex items-center justify-between mb-4">
              <p className="text-sm text-gray-500">
                找到 <span className="font-medium text-gray-900">{products.length}</span> 个潜力产品
              </p>
              <div className="flex items-center gap-2">
                <button
                  onClick={loadProducts}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <Clock className="w-4 h-4" />
                  刷新
                </button>
                <button className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
                >
                  <Download className="w-4 h-4" />
                  导出
                </button>
              </div>
            </div>
            
            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Array.from({ length: 6 }).map((_, i) => (
                  <div key={i} className="bg-white rounded-xl h-64 animate-pulse" />
                ))}
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {products.map((product) => (
                  <ProductResearchCard
                    key={product.id}
                    product={product}
                    onFavorite={toggleFavorite}
                    isFavorite={favorites.has(product.id)}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
