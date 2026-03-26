// Product types
export interface Product {
  id: string;
  name: string;
  description: string;
  category: string;
  subcategory: string;
  price: PriceRange;
  moq: number;
  supplier: Supplier;
  images: string[];
  specifications: Record<string, string>;
  rating: number;
  reviewCount: number;
  salesVolume: number;
  trend: 'up' | 'down' | 'stable';
  trendValue: number;
  region: string;
}

export interface PriceRange {
  min: number;
  max: number;
  currency: string;
  unit: string;
}

export interface Supplier {
  name: string;
  location: string;
  rating: number;
  yearsInBusiness: number;
  verified: boolean;
}

// Filter types
export interface FilterOptions {
  categories: string[];
  subcategories: Record<string, string[]>;
  regions: string[];
  priceRanges: { label: string; min?: number; max?: number }[];
  sortOptions: { value: string; label: string }[];
}

export interface SearchFilters {
  keyword?: string;
  category?: string;
  subcategory?: string;
  region?: string;
  minPrice?: number;
  maxPrice?: number;
  moq?: number;
  sortBy?: 'relevance' | 'price-asc' | 'price-desc' | 'sales' | 'rating' | 'newest';
  page: number;
  pageSize: number;
}

// Pagination
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// Dashboard
export interface DashboardStats {
  totalProducts: number;
  totalProductsChange: number;
  todayAdded: number;
  todayAddedChange: number;
  totalExportValue: number;
  totalExportChange: number;
  countriesCovered: number;
  countriesChange: number;
  topProducts: TrendingProduct[];
  recentTrades: TradeRecord[];
  categoryStats: CategoryStat[];
  regionStats: RegionStat[];
  monthlyTrend: TrendData;
}

export interface TrendingProduct {
  rank: number;
  name: string;
  value: string;
  growth: string;
  trend: 'up' | 'down';
}

export interface TradeRecord {
  time: string;
  product: string;
  category: string;
  price: string;
  quantity: string;
  region: string;
  status: '已发货' | '处理中' | '待发货';
}

export interface CategoryStat {
  name: string;
  value: number;
  color: string;
}

export interface RegionStat {
  name: string;
  value: number;
}

export interface TrendData {
  months: string[];
  values: number[];
  lastYearValues?: number[];
}

// Customs data
export interface CustomsData {
  year: number;
  month: number;
  hsCode: string;
  productName: string;
  exportValue: number;
  exportQuantity: number;
  destinationCountry: string;
  unit: string;
  yoyGrowth: number;
}

export interface ExportRecord {
  id: string;
  date: string;
  productName: string;
  hsCode: string;
  quantity: number;
  unit: string;
  value: number;
  currency: string;
  destination: string;
  province: string;
  companyType: string;
}

// Analytics
export interface ProfitAnalysis {
  productId: string;
  productName: string;
  costPrice: number;
  suggestedPrice: number;
  profitMargin: number;
  monthlyProfit: number;
  roi: number;
  paybackPeriod: number;
  breakEvenQuantity: number;
}

export interface CompetitionAnalysis {
  productId: string;
  competitorCount: number;
  averagePrice: number;
  priceRange: { min: number; max: number };
  marketShare: number;
  topCompetitors: Competitor[];
  barrierToEntry: 'low' | 'medium' | 'high';
  saturationLevel: 'low' | 'medium' | 'high';
}

export interface Competitor {
  name: string;
  location: string;
  price: number;
  sales: number;
  rating: number;
  marketShare: number;
}

// Export
export type ExportFormat = 'excel' | 'csv' | 'pdf';

export interface ExportOptions {
  format: ExportFormat;
  dataType: 'products' | 'customs' | 'analytics';
  filters?: SearchFilters;
  columns?: string[];
}

// Watchlist
export interface WatchlistItem {
  productId: string;
  addedAt: string;
  notes?: string;
  targetPrice?: number;
}
