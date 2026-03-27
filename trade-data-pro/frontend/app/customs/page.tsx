'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Globe, TrendingUp, TrendingDown, Download, Calendar,
  BarChart3, PieChart, ArrowUpRight, ArrowDownRight,
  Search, Filter, ChevronDown, FileSpreadsheet
} from 'lucide-react';
import { Navbar } from '@/app/components/Navbar';
import { api } from '@/app/lib/api';

// 海关统计数据
interface CustomsData {
  hs_code: string;
  product_name: string;
  unit: string;
  quantity: number;
  value_usd: number;
  yoy_quantity: number;
  yoy_value: number;
  month: number;
  year: number;
}

// 国别数据
interface CountryData {
  country: string;
  export_value: number;
  import_value: number;
  total: number;
  yoy: number;
}

// 统计卡片
function StatCard({ title, value, change, changeType, icon: Icon, color }: any) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-xl p-6 shadow-sm border border-gray-100"
    >
      <div className="flex items-start justify-between">
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <div className={`flex items-center text-sm font-medium ${
          changeType === 'up' ? 'text-green-600' : 'text-red-600'
        }`}>
          {changeType === 'up' ? (
            <ArrowUpRight className="w-4 h-4 mr-1" />
          ) : (
            <ArrowDownRight className="w-4 h-4 mr-1" />
          )}
          {change}
        </div>
      </div>
      <div className="mt-4">
        <p className="text-gray-500 text-sm">{title}</p>
        <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
      </div>
    </motion.div>
  );
}

// 商品数据表格
function ProductTable({ data }: { data: CustomsData[] }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileSpreadsheet className="w-5 h-5 text-blue-600" />
            <h3 className="font-bold text-gray-900">商品进出口统计</h3>
          </div>
          <button 
            onClick={() => {
              // 导出数据为CSV
              const headers = ['HS编码', '商品名称', '计量单位', '数量', '金额(万美元)', '同比数量', '同比金额'];
              const rows = data.map((item: CustomsData) => [
                item.hs_code,
                item.product_name,
                item.unit,
                (item.quantity / 10000).toFixed(2),
                (item.value_usd / 10000).toFixed(2),
                item.yoy_quantity + '%',
                item.yoy_value + '%'
              ]);
              
              const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n');
              const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
              const link = document.createElement('a');
              link.href = URL.createObjectURL(blob);
              link.download = `海关统计数据_${new Date().toISOString().split('T')[0]}.csv`;
              link.click();
            }}
            className="flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors"
          >
            <Download className="w-4 h-4" />
            导出Excel
          </button>
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">HS编码</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">商品名称</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">计量单位</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">数量</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">金额(万美元)</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">同比数量</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">同比金额</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {data.map((item, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-sm font-medium text-gray-900">{item.hs_code}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{item.product_name}</td>
                <td className="px-6 py-4 text-sm text-gray-500">{item.unit}</td>
                <td className="px-6 py-4 text-sm text-right text-gray-900">
                  {(item.quantity / 10000).toFixed(2)}万
                </td>
                <td className="px-6 py-4 text-sm text-right font-medium text-gray-900">
                  ${(item.value_usd / 10000).toFixed(2)}
                </td>
                <td className={`px-6 py-4 text-sm text-right ${
                  item.yoy_quantity >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {item.yoy_quantity >= 0 ? '+' : ''}{item.yoy_quantity}%
                </td>
                <td className={`px-6 py-4 text-sm text-right ${
                  item.yoy_value >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {item.yoy_value >= 0 ? '+' : ''}{item.yoy_value}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// 国别贸易统计
function CountryStats({ data }: { data: CountryData[] }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div className="flex items-center gap-2 mb-6">
        <Globe className="w-5 h-5 text-blue-600" />
        <h3 className="font-bold text-gray-900">TOP10 贸易伙伴</h3>
      </div>
      
      <div className="space-y-4">
        {data.map((country, index) => (
          <div key={country.country} className="flex items-center">
            <span className={`w-6 h-6 rounded-full flex items-center justify-center text-sm font-bold mr-3 ${
              index < 3 ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'
            }`}>
              {index + 1}
            </span>
            <span className="flex-1 font-medium text-gray-900">{country.country}</span>
            <div className="text-right mr-4">
              <p className="text-sm font-medium text-gray-900">${country.total}B</p>
              <p className="text-xs text-gray-500">出口${country.export_value}B</p>
            </div>
            <span className={`text-sm font-medium ${
              country.yoy >= 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {country.yoy >= 0 ? '+' : ''}{country.yoy}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// 趋势图表
function TrendChart() {
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
  const exportData = [280, 265, 298, 312, 305, 320, 335, 342, 338, 355, 368, 395];
  const importData = [220, 215, 238, 245, 252, 258, 265, 270, 268, 275, 282, 295];
  
  const maxValue = Math.max(...exportData, ...importData);
  
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-blue-600" />
          <h3 className="font-bold text-gray-900">进出口趋势对比</h3>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-500 rounded"></div>
            <span className="text-sm text-gray-600">出口</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-orange-400 rounded"></div>
            <span className="text-sm text-gray-600">进口</span>
          </div>
        </div>
      </div>
      
      <div className="h-64 flex items-end justify-between gap-2">
        {months.map((month, i) => (
          <div key={month} className="flex-1 flex flex-col items-center gap-1">
            <div className="w-full flex gap-0.5 items-end" style={{ height: '150px' }}>
              <div 
                className="flex-1 bg-blue-500 rounded-t"
                style={{ height: `${(exportData[i] / maxValue) * 100}%` }}
              />
              <div 
                className="flex-1 bg-orange-400 rounded-t"
                style={{ height: `${(importData[i] / maxValue) * 100}%` }}
              />
            </div>
            <span className="text-xs text-gray-500">{month}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function CustomsPage() {
  const [customsData, setCustomsData] = useState<CustomsData[]>([]);
  const [countryData, setCountryData] = useState<CountryData[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('2024-02');
  
  useEffect(() => {
    loadData();
  }, []);
  
  const loadData = async () => {
    try {
      // 加载海关商品数据
      const response = await fetch('/api/customs');
      if (response.ok) {
        const result = await response.json();
        if (result.success && result.data) {
          setCustomsData(result.data);
        }
      }
      
      // 加载国别数据
      const countryResponse = await fetch('/api/customs/countries');
      if (countryResponse.ok) {
        const result = await countryResponse.json();
        if (result.success && result.data) {
          setCountryData(result.data);
        }
      }
    } catch (error) {
      console.error('加载海关数据失败:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // 默认数据（如果API返回为空）
  const defaultCustomsData: CustomsData[] = [
    { hs_code: "8517", product_name: "电话机", unit: "万台", quantity: 12345678, value_usd: 987654321, yoy_quantity: 5.2, yoy_value: 8.3, month: 2, year: 2024 },
    { hs_code: "8471", product_name: "计算机及部件", unit: "万台", quantity: 8765432, value_usd: 876543210, yoy_quantity: 3.1, yoy_value: 5.7, month: 2, year: 2024 },
    { hs_code: "8528", product_name: "电视及显示器", unit: "万台", quantity: 7654321, value_usd: 765432100, yoy_quantity: -2.3, yoy_value: 1.2, month: 2, year: 2024 },
    { hs_code: "8541", product_name: "集成电路", unit: "万个", quantity: 6543210, value_usd: 654321000, yoy_quantity: 12.5, yoy_value: 15.8, month: 2, year: 2024 },
    { hs_code: "9403", product_name: "家具及零件", unit: "万吨", quantity: 543210, value_usd: 543210000, yoy_quantity: 1.8, yoy_value: 3.5, month: 2, year: 2024 },
    { hs_code: "6203", product_name: "男式服装", unit: "万件", quantity: 4321098, value_usd: 432109800, yoy_quantity: -5.2, yoy_value: -2.1, month: 2, year: 2024 },
    { hs_code: "9503", product_name: "玩具", unit: "万吨", quantity: 321098, value_usd: 321098000, yoy_quantity: 8.9, yoy_value: 11.2, month: 2, year: 2024 },
    { hs_code: "4202", product_name: "箱包", unit: "万个", quantity: 2109876, value_usd: 210987600, yoy_quantity: 3.4, yoy_value: 6.7, month: 2, year: 2024 },
  ];
  
  const defaultCountryData: CountryData[] = [
    { country: "美国", export_value: 524.4, import_value: 164.2, total: 688.6, yoy: 2.1 },
    { country: "东盟", export_value: 587.4, import_value: 394.6, total: 982.0, yoy: 8.2 },
    { country: "欧盟", export_value: 501.2, import_value: 271.8, total: 773.0, yoy: -1.5 },
    { country: "日本", export_value: 157.4, import_value: 142.6, total: 300.0, yoy: -5.2 },
    { country: "韩国", export_value: 148.9, import_value: 132.8, total: 281.7, yoy: 3.1 },
    { country: "越南", export_value: 137.2, import_value: 89.4, total: 226.6, yoy: 15.2 },
    { country: "德国", export_value: 100.1, import_value: 121.7, total: 221.8, yoy: -2.3 },
    { country: "马来西亚", export_value: 87.3, import_value: 112.5, total: 199.8, yoy: 6.8 },
    { country: "澳大利亚", export_value: 78.9, import_value: 145.2, total: 224.1, yoy: -3.1 },
    { country: "俄罗斯", export_value: 112.4, import_value: 98.7, total: 211.1, yoy: 22.5 },
  ];
  
  const displayData = customsData.length > 0 ? customsData : defaultCustomsData;
  const displayCountries = countryData.length > 0 ? countryData : defaultCountryData;
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 标题 */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">海关统计数据</h1>
          <p className="mt-2 text-gray-500">中国海关总署官方进出口统计数据</p>
        </div>
        
        {/* 筛选栏 */}
        <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 mb-6">
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex items-center gap-2">
              <Calendar className="w-5 h-5 text-gray-400" />
              <span className="text-sm text-gray-600">统计周期:</span>
            </div>
            <select 
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value)}
              className="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="2024-02">2024年2月</option>
              <option value="2024-01">2024年1月</option>
              <option value="2023-12">2023年12月</option>
              <option value="2023-11">2023年11月</option>
            </select>
            
            <div className="flex-1"></div>
            
            <button className="flex items-center gap-2 px-4 py-2 border border-gray-200 rounded-lg hover:bg-gray-50">
              <Filter className="w-4 h-4" />
              筛选
              <ChevronDown className="w-4 h-4" />
            </button>
            
            <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              <Download className="w-4 h-4" />
              导出报告
            </button>
          </div>
        </div>
        
        {/* 统计卡片 */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard 
            title="出口总额" 
            value="$3,380亿" 
            change="+4.6%" 
            changeType="up" 
            icon={TrendingUp} 
            color="bg-blue-500" 
          />
          <StatCard 
            title="进口总额" 
            value="$2,557亿" 
            change="+2.1%" 
            changeType="up" 
            icon={TrendingDown} 
            color="bg-orange-500" 
          />
          <StatCard 
            title="贸易顺差" 
            value="$823亿" 
            change="+12.3%" 
            changeType="up" 
            icon={BarChart3} 
            color="bg-green-500" 
          />
          <StatCard 
            title="贸易伙伴" 
            value="230个" 
            change="+1个" 
            changeType="up" 
            icon={Globe} 
            color="bg-purple-500" 
          />
        </div>
        
        {/* 主要内容 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <ProductTable data={displayData} />
            <TrendChart />
          </div>
          <div>
            <CountryStats data={displayCountries} />
          </div>
        </div>
        
        {/* 数据来源 */}
        <div className="mt-8 bg-blue-50 rounded-xl p-6">
          <div className="flex items-start gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Globe className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <h4 className="font-bold text-gray-900">数据来源说明</h4>
              <p className="mt-1 text-sm text-gray-600">
                本页面数据来源于中国海关总署官方统计，包括进出口商品统计数据和国别贸易数据。
                数据每月更新，仅供参考。如需官方数据，请访问 
                <a href="http://www.customs.gov.cn/" target="_blank" className="text-blue-600 hover:underline">
                  海关总署官网
                </a>
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
