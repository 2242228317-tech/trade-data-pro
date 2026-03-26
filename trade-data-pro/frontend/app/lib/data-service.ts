import fs from 'fs';
import path from 'path';
import {
  Product,
  ExportRecord,
  CustomsData,
  ProfitAnalysis,
  CompetitionAnalysis,
  TrendData,
  FilterOptions,
  SearchFilters,
  PaginatedResponse,
  DashboardStats,
  CategoryStat,
  RegionStat,
  Competitor,
  TrendingProduct,
  TradeRecord,
} from '../types';

// 数据文件路径
const DATA_DIR = path.join(process.cwd(), 'data');
const PRODUCTS_FILE = path.join(DATA_DIR, 'all-products.json');
const CUSTOMS_FILE = path.join(DATA_DIR, 'customs-data.json');

// 缓存
let productsCache: Product[] | null = null;
let customsCache: CustomsData[] | null = null;

// 从文件加载产品数据
function loadProducts(): Product[] {
  if (productsCache) return productsCache;
  
  try {
    if (fs.existsSync(PRODUCTS_FILE)) {
      const data = fs.readFileSync(PRODUCTS_FILE, 'utf-8');
      productsCache = JSON.parse(data);
      console.log(`[DataService] 加载了 ${productsCache?.length} 个产品`);
      return productsCache || [];
    }
  } catch (error) {
    console.error('[DataService] 加载产品数据失败:', error);
  }
  
  return [];
}

// 从文件加载海关数据
function loadCustomsData(): CustomsData[] {
  if (customsCache) return customsCache;
  
  try {
    if (fs.existsSync(CUSTOMS_FILE)) {
      const data = fs.readFileSync(CUSTOMS_FILE, 'utf-8');
      customsCache = JSON.parse(data);
      console.log(`[DataService] 加载了 ${customsCache?.length} 条海关记录`);
      return customsCache || [];
    }
  } catch (error) {
    console.error('[DataService] 加载海关数据失败:', error);
  }
  
  return [];
}

// 获取筛选选项
export function getFilterOptions(): FilterOptions {
  const products = loadProducts();
  
  const categories = [...new Set(products.map(p => p.category))];
  const subcategories: Record<string, string[]> = {};
  
  categories.forEach(cat => {
    const subs = [...new Set(products.filter(p => p.category === cat).map(p => p.subcategory))];
    subcategories[cat] = subs;
  });
  
  const regions = [...new Set(products.map(p => p.region))];
  
  return {
    categories,
    subcategories,
    regions,
    priceRanges: [
      { label: '¥0-50', min: 0, max: 50 },
      { label: '¥50-100', min: 50, max: 100 },
      { label: '¥100-500', min: 100, max: 500 },
      { label: '¥500-1000', min: 500, max: 1000 },
      { label: '¥1000+', min: 1000 },
    ],
    sortOptions: [
      { value: 'relevance', label: '相关度' },
      { value: 'price-asc', label: '价格从低到高' },
      { value: 'price-desc', label: '价格从高到低' },
      { value: 'sales', label: '销量' },
      { value: 'rating', label: '评分' },
      { value: 'newest', label: '最新' },
    ],
  };
}

// 搜索产品
export function searchProducts(filters: SearchFilters): PaginatedResponse<Product> {
  let products = loadProducts();
  
  // 关键词筛选
  if (filters.keyword) {
    const keyword = filters.keyword.toLowerCase();
    products = products.filter(p =>
      p.name.toLowerCase().includes(keyword) ||
      p.category.toLowerCase().includes(keyword) ||
      p.subcategory.toLowerCase().includes(keyword) ||
      p.description?.toLowerCase().includes(keyword)
    );
  }
  
  // 分类筛选
  if (filters.category) {
    products = products.filter(p => p.category === filters.category);
  }
  
  if (filters.subcategory) {
    products = products.filter(p => p.subcategory === filters.subcategory);
  }
  
  // 地区筛选
  if (filters.region) {
    products = products.filter(p => p.region === filters.region);
  }
  
  // 价格筛选
  if (filters.minPrice !== undefined) {
    products = products.filter(p => p.price.max >= filters.minPrice!);
  }
  if (filters.maxPrice !== undefined) {
    products = products.filter(p => p.price.min <= filters.maxPrice!);
  }
  
  // MOQ筛选
  if (filters.moq !== undefined) {
    products = products.filter(p => p.moq <= filters.moq!);
  }
  
  // 排序
  switch (filters.sortBy) {
    case 'price-asc':
      products.sort((a, b) => a.price.min - b.price.min);
      break;
    case 'price-desc':
      products.sort((a, b) => b.price.max - a.price.max);
      break;
    case 'sales':
      products.sort((a, b) => b.salesVolume - a.salesVolume);
      break;
    case 'rating':
      products.sort((a, b) => b.rating - a.rating);
      break;
    case 'newest':
      products.sort((a, b) => b.id.localeCompare(a.id));
      break;
    default:
      // 默认按相关度（销量+评分）
      products.sort((a, b) => (b.salesVolume * b.rating) - (a.salesVolume * a.rating));
  }
  
  const total = products.length;
  const page = filters.page || 1;
  const pageSize = filters.pageSize || 20;
  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  
  return {
    data: products.slice(start, end),
    total,
    page,
    pageSize,
    totalPages: Math.ceil(total / pageSize),
  };
}

// 获取单个产品
export function getProductById(id: string): Product | null {
  const products = loadProducts();
  return products.find(p => p.id === id) || null;
}

// 获取热门产品
export function getTrendingProducts(limit: number = 10): TrendingProduct[] {
  const products = loadProducts();
  
  return products
    .filter(p => p.trend === 'up')
    .sort((a, b) => b.trendValue - a.trendValue)
    .slice(0, limit)
    .map((p, index) => ({
      rank: index + 1,
      name: p.name.slice(0, 30) + (p.name.length > 30 ? '...' : ''),
      value: `¥${(p.salesVolume * p.price.min / 10000).toFixed(1)}万`,
      growth: `+${p.trendValue}%`,
      trend: 'up' as const,
    }));
}

// 获取海关数据
export function getCustomsData(filters?: { destination?: string; category?: string }): CustomsData[] {
  let data = loadCustomsData();
  
  if (filters?.destination) {
    data = data.filter(d => d.destination === filters.destination);
  }
  
  if (filters?.category) {
    data = data.filter(d => d.productName.includes(filters.category!));
  }
  
  return data;
}

// 获取仪表盘统计数据
export function getDashboardStats(): DashboardStats {
  const products = loadProducts();
  const customs = loadCustomsData();
  
  const totalProducts = products.length;
  const todayAdded = Math.floor(Math.random() * 100) + 50;
  const totalExportValue = customs.reduce((sum, c) => sum + c.exportValue, 0);
  const countriesCovered = new Set(customs.map(c => c.destination)).size;
  
  // 品类统计
  const categoryMap = new Map<string, number>();
  products.forEach(p => {
    categoryMap.set(p.category, (categoryMap.get(p.category) || 0) + 1);
  });
  
  const categoryStats: CategoryStat[] = Array.from(categoryMap.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6)
    .map(([name, value], index) => ({
      name,
      value,
      color: ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444', '#6b7280'][index],
    }));
  
  // 地区统计
  const regionMap = new Map<string, number>();
  products.forEach(p => {
    regionMap.set(p.region, (regionMap.get(p.region) || 0) + 1);
  });
  
  const regionStats: RegionStat[] = Array.from(regionMap.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([name, value]) => ({ name, value }));
  
  // 月度趋势
  const monthlyTrend: TrendData = {
    months: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
    values: [295, 278, 315, 328, 318, 335, 352, 361, 348, 365, 382, 395],
    lastYearValues: [280, 265, 298, 312, 305, 320, 335, 342, 338, 355, 368, 380],
  };
  
  // 实时交易
  const recentTrades: TradeRecord[] = products
    .slice(0, 5)
    .map((p, i) => ({
      time: `${10 + i}:0${i * 2}`,
      product: p.name.slice(0, 15) + '...',
      category: p.category,
      price: `¥${p.price.min}`,
      quantity: `${Math.floor(Math.random() * 2000 + 100)}`,
      region: p.region,
      status: ['已发货', '处理中', '待发货'][Math.floor(Math.random() * 3)] as any,
    }));
  
  return {
    totalProducts,
    totalProductsChange: 12.5,
    todayAdded,
    todayAddedChange: 8.2,
    totalExportValue,
    totalExportChange: 4.6,
    countriesCovered: countriesCovered || 50,
    countriesChange: 2.1,
    topProducts: getTrendingProducts(6),
    recentTrades,
    categoryStats,
    regionStats,
    monthlyTrend,
  };
}

// 获取利润分析
export function getProfitAnalysis(productId: string): ProfitAnalysis {
  const product = getProductById(productId);
  if (!product) throw new Error('Product not found');
  
  const costPrice = product.price.min * 0.6; // 假设成本为60%
  const suggestedPrice = product.price.max * 1.3; // 建议售价
  const profitPerUnit = suggestedPrice - costPrice;
  const profitMargin = (profitPerUnit / suggestedPrice) * 100;
  const monthlyVolume = Math.floor(product.salesVolume / 12);
  const monthlyProfit = profitPerUnit * monthlyVolume;
  const roi = (profitPerUnit / costPrice) * 100;
  
  return {
    productId,
    productName: product.name,
    costPrice: Math.floor(costPrice),
    suggestedPrice: Math.floor(suggestedPrice),
    profitMargin: Number(profitMargin.toFixed(1)),
    monthlyProfit: Math.floor(monthlyProfit),
    roi: Number(roi.toFixed(1)),
    paybackPeriod: Math.floor(costPrice / profitPerUnit),
    breakEvenQuantity: Math.ceil(costPrice / profitPerUnit),
  };
}

// 获取竞争分析
export function getCompetitionAnalysis(productId: string): CompetitionAnalysis {
  const product = getProductById(productId);
  if (!product) throw new Error('Product not found');
  
  const products = loadProducts().filter(p => 
    p.category === product.category && p.id !== productId
  );
  
  const prices = products.map(p => (p.price.min + p.price.max) / 2);
  const avgPrice = prices.reduce((a, b) => a + b, 0) / prices.length || product.price.min;
  
  const topCompetitors: Competitor[] = products
    .sort((a, b) => b.salesVolume - a.salesVolume)
    .slice(0, 5)
    .map(p => ({
      name: p.supplier.name.slice(0, 20),
      location: p.region,
      price: (p.price.min + p.price.max) / 2,
      sales: p.salesVolume,
      rating: p.rating,
      marketShare: Math.floor(Math.random() * 20) + 5,
    }));
  
  return {
    productId,
    competitorCount: products.length,
    averagePrice: Math.floor(avgPrice),
    priceRange: {
      min: Math.min(...prices, product.price.min),
      max: Math.max(...prices, product.price.max),
    },
    marketShare: Math.floor(Math.random() * 15) + 3,
    topCompetitors,
    barrierToEntry: products.length > 50 ? 'high' : products.length > 20 ? 'medium' : 'low',
    saturationLevel: products.length > 100 ? 'high' : products.length > 50 ? 'medium' : 'low',
  };
}

// 导出数据
export function exportData(type: string, format: string, filters?: SearchFilters): any {
  if (type === 'products') {
    const { data } = searchProducts(filters || { page: 1, pageSize: 1000 });
    return data;
  }
  
  if (type === 'customs') {
    return getCustomsData();
  }
  
  return [];
}

// 刷新数据
export function refreshData(): void {
  productsCache = null;
  customsCache = null;
  loadProducts();
  loadCustomsData();
}
