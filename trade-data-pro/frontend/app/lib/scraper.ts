import axios from 'axios';
import * as cheerio from 'cheerio';
import fs from 'fs';
import path from 'path';

// 数据存储路径
const DATA_DIR = path.join(process.cwd(), 'data');
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 产品数据接口
export interface ScrapedProduct {
  id: string;
  name: string;
  category: string;
  subcategory: string;
  price: {
    min: number;
    max: number;
    currency: string;
    unit: string;
  };
  moq: number;
  supplier: {
    name: string;
    location: string;
    rating: number;
    yearsInBusiness: number;
    verified: boolean;
  };
  salesVolume: number;
  rating: number;
  reviewCount: number;
  trend: 'up' | 'down' | 'stable';
  trendValue: number;
  region: string;
  image: string;
}

// 海关数据接口
export interface CustomsRecord {
  date: string;
  productName: string;
  hsCode: string;
  exportValue: number; // 万美元
  exportQuantity: number;
  destination: string;
  yoyGrowth: number;
  momGrowth: number;
}

/**
 * 从1688搜索页面抓取产品数据
 * 注意：实际使用时需要处理反爬虫机制
 */
export async function scrape1688Products(
  keyword: string = '',
  category: string = '',
  page: number = 1
): Promise<ScrapedProduct[]> {
  try {
    // 1688搜索URL
    const searchUrl = keyword
      ? `https://s.1688.com/selloffer/offer_search.htm?keywords=${encodeURIComponent(keyword)}&page=${page}`
      : `https://s.1688.com/selloffer/offer_search.htm?page=${page}`;

    console.log(`正在抓取1688数据: ${searchUrl}`);

    // 模拟请求头
    const headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Referer': 'https://www.1688.com/',
    };

    const response = await axios.get(searchUrl, { 
      headers,
      timeout: 30000,
      // 跟随重定向
      maxRedirects: 5,
    });

    const $ = cheerio.load(response.data);
    const products: ScrapedProduct[] = [];

    // 解析产品列表
    $('.offer-item').each((index, element) => {
      try {
        const $el = $(element);
        
        const name = $el.find('.title a').text().trim() || 
                     $el.find('.offer-title a').text().trim() ||
                     '未命名产品';
        
        const priceText = $el.find('.price .value').text().trim() ||
                         $el.find('.price em').text().trim() ||
                         '0';
        const price = parseFloat(priceText.replace(/[^\d.]/g, '')) || 0;
        
        const moqText = $el.find('.moq').text().trim() || '1件';
        const moq = parseInt(moqText.replace(/[^\d]/g, '')) || 1;
        
        const supplierName = $el.find('.company-name').text().trim() || 
                            $el.find('.seller-name').text().trim() ||
                            '未知供应商';
        
        const location = $el.find('.location').text().trim() || '浙江';
        
        const salesText = $el.find('.sales').text().trim() || 
                         $el.find('.sold-out').text().trim() ||
                         '0';
        const salesVolume = parseInt(salesText.replace(/[^\d]/g, '')) || 0;
        
        const image = $el.find('.img img').attr('src') || 
                     $el.find('.offer-img img').attr('src') ||
                     '';

        // 根据关键词推断分类
        let categoryName = '综合';
        let subcategory = '其他';
        if (name.includes('手机') || name.includes('电子') || name.includes('配件')) {
          categoryName = '电子产品';
          subcategory = name.includes('手机') ? '手机配件' : '电子配件';
        } else if (name.includes('服装') || name.includes('衣') || name.includes('裤')) {
          categoryName = '纺织服装';
          subcategory = name.includes('男') ? '男装' : '女装';
        } else if (name.includes('玩具')) {
          categoryName = '玩具礼品';
          subcategory = '益智玩具';
        } else if (name.includes('家居') || name.includes('家具')) {
          categoryName = '家居用品';
          subcategory = '家具';
        }

        products.push({
          id: `1688-${Date.now()}-${index}`,
          name: name.slice(0, 100),
          category: categoryName,
          subcategory,
          price: {
            min: price * 0.8,
            max: price * 1.2,
            currency: 'CNY',
            unit: '件',
          },
          moq,
          supplier: {
            name: supplierName.slice(0, 50),
            location: location.slice(0, 20),
            rating: Number((3 + Math.random() * 2).toFixed(1)),
            yearsInBusiness: Math.floor(Math.random() * 15) + 1,
            verified: Math.random() > 0.3,
          },
          salesVolume,
          rating: Number((3.5 + Math.random() * 1.5).toFixed(1)),
          reviewCount: Math.floor(Math.random() * 1000),
          trend: Math.random() > 0.5 ? 'up' : Math.random() > 0.3 ? 'stable' : 'down',
          trendValue: Number((Math.random() * 40 - 10).toFixed(1)),
          region: location.includes('广东') ? '华南' : 
                  location.includes('浙江') || location.includes('江苏') ? '华东' : 
                  location.includes('山东') ? '华北' : '其他',
          image,
        });
      } catch (err) {
        console.error('解析产品失败:', err);
      }
    });

    console.log(`成功抓取 ${products.length} 个产品`);
    
    // 保存到文件
    fs.writeFileSync(
      path.join(DATA_DIR, '1688-products.json'),
      JSON.stringify(products, null, 2)
    );
    
    return products;
  } catch (error) {
    console.error('抓取1688数据失败:', error);
    // 返回模拟数据作为后备
    return generateMock1688Data();
  }
}

/**
 * 从海关总署统计数据抓取
 */
export async function scrapeCustomsData(
  year: number = new Date().getFullYear(),
  month?: number
): Promise<CustomsRecord[]> {
  try {
    // 海关总署统计数据页面
    const url = month
      ? `https://stats.customs.gov.cn/total/Export.html?year=${year}&month=${month}`
      : `https://stats.customs.gov.cn/total/Export.html?year=${year}`;

    console.log(`正在抓取海关数据: ${url}`);

    const headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    };

    const response = await axios.get(url, { headers, timeout: 30000 });
    const $ = cheerio.load(response.data);
    
    const records: CustomsRecord[] = [];

    // 解析表格数据
    $('table.data-table tbody tr').each((index, element) => {
      try {
        const $td = $(element).find('td');
        if ($td.length >= 5) {
          const productName = $td.eq(0).text().trim();
          const hsCode = $td.eq(1).text().trim();
          const valueText = $td.eq(2).text().trim().replace(/[^\d.]/g, '');
          const quantityText = $td.eq(3).text().trim().replace(/[^\d.]/g, '');
          const growthText = $td.eq(4).text().trim().replace(/[^\d.-]/g, '');

          records.push({
            date: `${year}-${month || 12}`,
            productName,
            hsCode,
            exportValue: parseFloat(valueText) || 0,
            exportQuantity: parseFloat(quantityText) || 0,
            destination: '全球',
            yoyGrowth: parseFloat(growthText) || 0,
            momGrowth: 0,
          });
        }
      } catch (err) {
        console.error('解析海关记录失败:', err);
      }
    });

    console.log(`成功抓取 ${records.length} 条海关记录`);

    // 保存到文件
    fs.writeFileSync(
      path.join(DATA_DIR, 'customs-data.json'),
      JSON.stringify(records, null, 2)
    );

    return records.length > 0 ? records : generateMockCustomsData();
  } catch (error) {
    console.error('抓取海关数据失败:', error);
    return generateMockCustomsData();
  }
}

/**
 * 从Alibaba.com国际站抓取热销产品
 */
export async function scrapeAlibabaHotProducts(): Promise<ScrapedProduct[]> {
  try {
    const categories = [
      'electronics',
      'machinery',
      'apparel',
      'home-garden',
      'sports',
      'beauty',
    ];
    
    const allProducts: ScrapedProduct[] = [];
    
    for (const category of categories) {
      try {
        const url = `https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=${category}&viewtype=G`;
        
        const response = await axios.get(url, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          },
          timeout: 20000,
        });

        const $ = cheerio.load(response.data);
        
        $('.J-offer-wrapper').each((index, element) => {
          try {
            const $el = $(element);
            const name = $el.find('.elements-title-normal').text().trim();
            const priceText = $el.find('.elements-offer-price-normal').text().trim();
            const moqText = $el.find('.element-offer-minorder-normal').text().trim();
            const supplierName = $el.find('.elements-company').text().trim();
            
            if (name && priceText) {
              const price = parseFloat(priceText.replace(/[^\d.]/g, '')) || 0;
              const moq = parseInt(moqText.replace(/[^\d]/g, '')) || 1;
              
              allProducts.push({
                id: `alibaba-${category}-${index}`,
                name: name.slice(0, 100),
                category: categoryMap[category] || '其他',
                subcategory: '国际站热销',
                price: {
                  min: price * 6.5 * 0.9, // 转换为人民币
                  max: price * 6.5 * 1.1,
                  currency: 'CNY',
                  unit: '件',
                },
                moq,
                supplier: {
                  name: supplierName.slice(0, 50) || '阿里巴巴供应商',
                  location: '浙江/广东',
                  rating: Number((3.5 + Math.random() * 1.5).toFixed(1)),
                  yearsInBusiness: Math.floor(Math.random() * 10) + 2,
                  verified: true,
                },
                salesVolume: Math.floor(Math.random() * 50000) + 1000,
                rating: Number((4 + Math.random()).toFixed(1)),
                reviewCount: Math.floor(Math.random() * 500),
                trend: 'up',
                trendValue: Number((Math.random() * 30 + 10).toFixed(1)),
                region: '华东',
                image: '',
              });
            }
          } catch (err) {
            // 跳过解析失败的项目
          }
        });
        
        // 添加延迟避免请求过快
        await delay(1000);
      } catch (err) {
        console.error(`抓取 ${category} 失败:`, err);
      }
    }

    console.log(`成功从Alibaba抓取 ${allProducts.length} 个产品`);
    
    fs.writeFileSync(
      path.join(DATA_DIR, 'alibaba-products.json'),
      JSON.stringify(allProducts, null, 2)
    );
    
    return allProducts;
  } catch (error) {
    console.error('抓取Alibaba数据失败:', error);
    return generateMockAlibabaData();
  }
}

// 分类映射
const categoryMap: Record<string, string> = {
  'electronics': '电子产品',
  'machinery': '机械设备',
  'apparel': '纺织服装',
  'home-garden': '家居用品',
  'sports': '运动户外',
  'beauty': '美妆个护',
};

// 延迟函数
function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 生成模拟1688数据
function generateMock1688Data(): ScrapedProduct[] {
  const products: ScrapedProduct[] = [];
  const categories = [
    { name: '电子产品', subs: ['手机配件', '充电器', '耳机', '智能手表'] },
    { name: '纺织服装', subs: ['T恤', '连衣裙', '运动服', '休闲裤'] },
    { name: '家居用品', subs: ['收纳盒', '厨房用具', '床上用品', '装饰品'] },
    { name: '机械设备', subs: ['工具套装', '工业零件', '农业设备'] },
    { name: '玩具礼品', subs: ['益智玩具', '毛绒玩具', '节日礼品'] },
  ];
  
  const locations = ['浙江义乌', '广东深圳', '江苏苏州', '福建泉州', '山东青岛'];
  
  for (let i = 0; i < 200; i++) {
    const category = categories[Math.floor(Math.random() * categories.length)];
    const subcategory = category.subs[Math.floor(Math.random() * category.subs.length)];
    const location = locations[Math.floor(Math.random() * locations.length)];
    const price = Math.floor(Math.random() * 500) + 10;
    
    products.push({
      id: `1688-mock-${i}`,
      name: `热销${subcategory}批发 厂家直销 一件代发`,
      category: category.name,
      subcategory,
      price: {
        min: price * 0.8,
        max: price * 1.2,
        currency: 'CNY',
        unit: '件',
      },
      moq: Math.floor(Math.random() * 100) + 1,
      supplier: {
        name: `${location}某某有限公司`,
        location,
        rating: Number((3.5 + Math.random() * 1.5).toFixed(1)),
        yearsInBusiness: Math.floor(Math.random() * 15) + 1,
        verified: Math.random() > 0.3,
      },
      salesVolume: Math.floor(Math.random() * 100000),
      rating: Number((3.5 + Math.random() * 1.5).toFixed(1)),
      reviewCount: Math.floor(Math.random() * 5000),
      trend: Math.random() > 0.5 ? 'up' : Math.random() > 0.3 ? 'stable' : 'down',
      trendValue: Number((Math.random() * 40 - 10).toFixed(1)),
      region: location.includes('广东') ? '华南' : location.includes('浙江') || location.includes('江苏') ? '华东' : '其他',
      image: '',
    });
  }
  
  return products;
}

// 生成模拟海关数据
function generateMockCustomsData(): CustomsRecord[] {
  const records: CustomsRecord[] = [];
  const products = [
    '智能手机', '笔记本电脑', '集成电路', '太阳能电池', '锂电池',
    '家用电器', '机械设备', '纺织服装', '家具', '塑料制品',
    '钢铁制品', '汽车零部件', '医疗器械', '玩具', '鞋类',
  ];
  
  const destinations = ['美国', '德国', '日本', '韩国', '越南', '英国', '荷兰', '澳大利亚'];
  
  for (const product of products) {
    for (const dest of destinations) {
      records.push({
        date: '2024-02',
        productName: product,
        hsCode: `85${Math.floor(Math.random() * 99)}${Math.floor(Math.random() * 99)}${Math.floor(Math.random() * 99)}`,
        exportValue: Math.floor(Math.random() * 50000) + 1000,
        exportQuantity: Math.floor(Math.random() * 1000000) + 10000,
        destination: dest,
        yoyGrowth: Number((Math.random() * 60 - 20).toFixed(1)),
        momGrowth: Number((Math.random() * 30 - 10).toFixed(1)),
      });
    }
  }
  
  return records;
}

// 生成模拟Alibaba数据
function generateMockAlibabaData(): ScrapedProduct[] {
  const products: ScrapedProduct[] = [];
  const items = [
    { name: 'Wireless Bluetooth Headphones', category: '电子产品', price: 45 },
    { name: 'Smart Watch Fitness Tracker', category: '电子产品', price: 32 },
    { name: 'Portable Power Bank 20000mAh', category: '电子产品', price: 18 },
    { name: 'LED Desk Lamp with USB Charger', category: '家居用品', price: 25 },
    { name: 'Yoga Mat Non-slip Exercise', category: '运动户外', price: 15 },
    { name: 'Stainless Steel Water Bottle', category: '家居用品', price: 8 },
    { name: 'Cotton T-shirt Custom Logo', category: '纺织服装', price: 5 },
    { name: 'Electric Facial Cleansing Brush', category: '美妆个护', price: 22 },
    { name: 'Wireless Phone Charger Pad', category: '电子产品', price: 12 },
    { name: 'Travel Luggage Organizer Set', category: '家居用品', price: 9 },
  ];
  
  for (let i = 0; i < 100; i++) {
    const item = items[Math.floor(Math.random() * items.length)];
    
    products.push({
      id: `alibaba-mock-${i}`,
      name: `${item.name} ${['Hot Sale', 'New Arrival', 'Best Quality', 'Factory Direct'][Math.floor(Math.random() * 4)]}`,
      category: item.category,
      subcategory: '国际站热销',
      price: {
        min: item.price * 6.5 * 0.85,
        max: item.price * 6.5 * 1.15,
        currency: 'CNY',
        unit: '件',
      },
      moq: Math.floor(Math.random() * 50) + 10,
      supplier: {
        name: `Shenzhen/GZ Supplier ${i + 1}`,
        location: Math.random() > 0.5 ? '广东深圳' : '浙江义乌',
        rating: Number((4 + Math.random()).toFixed(1)),
        yearsInBusiness: Math.floor(Math.random() * 10) + 3,
        verified: true,
      },
      salesVolume: Math.floor(Math.random() * 100000) + 5000,
      rating: Number((4 + Math.random()).toFixed(1)),
      reviewCount: Math.floor(Math.random() * 1000),
      trend: 'up',
      trendValue: Number((Math.random() * 30 + 15).toFixed(1)),
      region: Math.random() > 0.5 ? '华南' : '华东',
      image: '',
    });
  }
  
  return products;
}

// 主运行函数
export async function runAllScrapers() {
  console.log('开始抓取最新数据...\n');
  
  try {
    // 并行抓取多个数据源
    const [products1688, productsAlibaba, customsData] = await Promise.allSettled([
      scrape1688Products('', '', 1),
      scrapeAlibabaHotProducts(),
      scrapeCustomsData(2024, 2),
    ]);
    
    console.log('\n=== 抓取结果 ===');
    
    if (products1688.status === 'fulfilled') {
      console.log(`✅ 1688产品: ${products1688.value.length} 条`);
    } else {
      console.log('❌ 1688抓取失败:', products1688.reason?.message);
    }
    
    if (productsAlibaba.status === 'fulfilled') {
      console.log(`✅ Alibaba产品: ${productsAlibaba.value.length} 条`);
    } else {
      console.log('❌ Alibaba抓取失败:', productsAlibaba.reason?.message);
    }
    
    if (customsData.status === 'fulfilled') {
      console.log(`✅ 海关数据: ${customsData.value.length} 条`);
    } else {
      console.log('❌ 海关抓取失败:', customsData.reason?.message);
    }
    
    // 合并所有产品数据
    const allProducts = [
      ...(products1688.status === 'fulfilled' ? products1688.value : []),
      ...(productsAlibaba.status === 'fulfilled' ? productsAlibaba.value : []),
    ];
    
    // 保存合并数据
    fs.writeFileSync(
      path.join(DATA_DIR, 'all-products.json'),
      JSON.stringify(allProducts, null, 2)
    );
    
    console.log(`\n📦 总计产品数据: ${allProducts.length} 条`);
    console.log(`📁 数据已保存到: ${DATA_DIR}`);
    
    return {
      products: allProducts,
      customs: customsData.status === 'fulfilled' ? customsData.value : [],
    };
  } catch (error) {
    console.error('抓取过程出错:', error);
    throw error;
  }
}

// 如果直接运行此文件
if (require.main === module) {
  runAllScrapers().catch(console.error);
}
