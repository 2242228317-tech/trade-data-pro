const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');

// 数据存储路径
const DATA_DIR = path.join(process.cwd(), 'data');
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 生成真实的模拟数据 - 基于2024年实际外贸趋势
function generateRealisticData() {
  console.log('正在生成基于2024年外贸趋势的模拟数据...\n');
  
  // 2024年热销产品数据（基于真实市场趋势）
  const hotProducts = [
    // 新能源产品（2024年最火）
    { name: '太阳能电池板 100W-500W', category: '新能源', sub: '太阳能', price: 280, moq: 50, trend: 45.2, region: '江苏' },
    { name: '锂电池组 48V 100Ah', category: '新能源', sub: '储能电池', price: 1200, moq: 20, trend: 38.7, region: '广东' },
    { name: '便携式储能电源 1000W', category: '新能源', sub: '储能设备', price: 650, moq: 30, trend: 52.3, region: '浙江' },
    { name: '新能源汽车充电桩', category: '新能源', sub: '充电设备', price: 890, moq: 10, trend: 41.5, region: '广东' },
    
    // 电子产品
    { name: '无线蓝牙耳机 TWS降噪', category: '电子产品', sub: '耳机音响', price: 45, moq: 100, trend: 15.8, region: '广东' },
    { name: '智能手表 运动健康监测', category: '电子产品', sub: '智能穿戴', price: 128, moq: 50, trend: 22.4, region: '深圳' },
    { name: '快充充电器 65W氮化镓', category: '电子产品', sub: '充电设备', price: 35, moq: 200, trend: 28.6, region: '东莞' },
    { name: '手机支架 磁吸无线充', category: '电子产品', sub: '手机配件', price: 28, moq: 150, trend: 18.9, region: '深圳' },
    { name: '平板电脑 10.1英寸', category: '电子产品', sub: '平板电脑', price: 480, moq: 30, trend: 12.3, region: '深圳' },
    { name: '智能家居中控面板', category: '电子产品', sub: '智能家居', price: 180, moq: 40, trend: 35.7, region: '杭州' },
    
    // 家居用品
    { name: '真空压缩收纳袋套装', category: '家居用品', sub: '收纳用品', price: 15, moq: 300, trend: 8.5, region: '义乌' },
    { name: 'LED护眼台灯 智能调光', category: '家居用品', sub: '灯具照明', price: 68, moq: 80, trend: 16.2, region: '中山' },
    { name: '厨房置物架 多层不锈钢', category: '家居用品', sub: '厨房用品', price: 45, moq: 100, trend: 11.4, region: '揭阳' },
    { name: '智能门锁 指纹密码', category: '家居用品', sub: '安防设备', price: 320, moq: 20, trend: 42.8, region: '深圳' },
    { name: '扫地机器人 自动回充', category: '家居用品', sub: '清洁电器', price: 680, moq: 15, trend: 31.5, region: '苏州' },
    { name: '床上四件套 纯棉', category: '家居用品', sub: '床上用品', price: 85, moq: 60, trend: 6.8, region: '南通' },
    
    // 纺织服装
    { name: '瑜伽服套装 速干面料', category: '纺织服装', sub: '运动服装', price: 38, moq: 100, trend: 24.6, region: '泉州' },
    { name: '防晒衣 UPF50+', category: '纺织服装', sub: '户外服装', price: 35, moq: 120, trend: 32.1, region: '石狮' },
    { name: '纯棉T恤 定制印花', category: '纺织服装', sub: 'T恤', price: 18, moq: 200, trend: 9.3, region: '广州' },
    { name: '保暖内衣套装 德绒', category: '纺织服装', sub: '内衣', price: 42, moq: 80, trend: 15.7, region: '义乌' },
    { name: '冲锋衣 三合一可拆卸', category: '纺织服装', sub: '外套', price: 128, moq: 50, trend: 21.4, region: '泉州' },
    
    // 运动户外
    { name: '露营帐篷 3-4人全自动', category: '运动户外', sub: '露营装备', price: 168, moq: 30, trend: 48.9, region: '厦门' },
    { name: '折叠自行车 20寸', category: '运动户外', sub: '自行车', price: 380, moq: 15, trend: 19.2, region: '天津' },
    { name: '登山包 40L防水', category: '运动户外', sub: '户外背包', price: 95, moq: 50, trend: 14.6, region: '泉州' },
    { name: '瑜伽垫 TPE防滑', category: '运动户外', sub: '瑜伽用品', price: 25, moq: 150, trend: 12.8, region: '东莞' },
    { name: '筋膜枪 深层按摩', category: '运动户外', sub: '健身器材', price: 88, moq: 60, trend: 8.4, region: '永康' },
    
    // 美妆个护
    { name: '电动牙刷 声波震动', category: '美妆个护', sub: '口腔护理', price: 55, moq: 80, trend: 18.7, region: '宁波' },
    { name: '洁面仪 硅胶刷头', category: '美妆个护', sub: '面部护理', price: 42, moq: 100, trend: 11.3, region: '深圳' },
    { name: '吹风机 负离子护发', category: '美妆个护', sub: '美发工具', price: 78, moq: 50, trend: 16.5, region: '东莞' },
    { name: '美甲灯 LED速干', category: '美妆个护', sub: '美甲工具', price: 22, moq: 200, trend: 7.9, region: '义乌' },
    
    // 汽车配件
    { name: '车载充电器 快充', category: '汽车配件', sub: '车载电子', price: 18, moq: 150, trend: 13.4, region: '深圳' },
    { name: '行车记录仪 4K高清', category: '汽车配件', sub: '安防设备', price: 168, moq: 30, trend: 9.8, region: '东莞' },
    { name: '汽车脚垫 全包围', category: '汽车配件', sub: '内饰用品', price: 85, moq: 40, trend: 6.2, region: '台州' },
    { name: '车载吸尘器 无线充电', category: '汽车配件', sub: '清洁用品', price: 48, moq: 80, trend: 15.1, region: '宁波' },
    
    // 机械设备
    { name: '激光切割机 小型', category: '机械设备', sub: '工业设备', price: 2800, moq: 5, trend: 22.7, region: '济南' },
    { name: '3D打印机 FDM', category: '机械设备', sub: '打印设备', price: 680, moq: 10, trend: 17.3, region: '深圳' },
    { name: '电动螺丝刀套装', category: '机械设备', sub: '工具', price: 35, moq: 100, trend: 8.6, region: '永康' },
    { name: '小型挖掘机 1吨', category: '机械设备', sub: '工程机械', price: 8500, moq: 3, trend: 31.2, region: '济宁' },
    
    // 医疗器械
    { name: '电子血压计 上臂式', category: '医疗器械', sub: '检测仪器', price: 68, moq: 50, trend: 14.8, region: '深圳' },
    { name: '血氧仪 指夹式', category: '医疗器械', sub: '检测仪器', price: 25, moq: 100, trend: 6.5, region: '深圳' },
    { name: '体温计 红外额温', category: '医疗器械', sub: '检测仪器', price: 18, moq: 200, trend: 4.2, region: '东莞' },
    { name: '按摩椅 全身自动', category: '医疗器械', sub: '康复设备', price: 2800, moq: 5, trend: 19.6, region: '宁德' },
    
    // 玩具礼品
    { name: '益智积木 1000片', category: '玩具礼品', sub: '益智玩具', price: 32, moq: 80, trend: 10.3, region: '汕头' },
    { name: '遥控无人机 4K航拍', category: '玩具礼品', sub: '遥控玩具', price: 268, moq: 20, trend: 25.7, region: '深圳' },
    { name: '毛绒玩具 大号公仔', category: '玩具礼品', sub: '毛绒玩具', price: 28, moq: 100, trend: 7.4, region: '扬州' },
    { name: '创意礼品 定制logo', category: '玩具礼品', sub: '礼品', price: 15, moq: 200, trend: 12.1, region: '义乌' },
  ];

  const suppliers = [
    '深圳市科技创新有限公司', '义乌市小商品批发中心', '广州市服装制造厂',
    '宁波市五金工具厂', '苏州市电子科技有限公司', '佛山市家居用品厂',
    '温州市眼镜制造厂', '东莞市玩具礼品厂', '上海市医疗器械公司',
    '青岛市化工有限公司', '杭州市智能家居厂', '厦门市户外用品公司',
    '泉州市运动器材厂', '天津市自行车厂', '中山市灯具厂',
  ];

  const products = hotProducts.map((item, index) => {
    const supplier = suppliers[index % suppliers.length];
    const salesVolume = Math.floor(Math.random() * 80000) + 5000;
    
    return {
      id: `real-${index + 1}`,
      name: `${item.name} 厂家直销`,
      description: `热销${item.sub}产品，${item.region}产地，品质保证`,
      category: item.category,
      subcategory: item.sub,
      price: {
        min: Math.floor(item.price * 0.85),
        max: Math.floor(item.price * 1.15),
        currency: 'CNY',
        unit: '件',
      },
      moq: item.moq,
      supplier: {
        name: supplier,
        location: item.region,
        rating: Number((3.8 + Math.random() * 1.2).toFixed(1)),
        yearsInBusiness: Math.floor(Math.random() * 15) + 2,
        verified: Math.random() > 0.2,
      },
      images: [],
      specifications: {
        '产地': item.region,
        '材质': '优质材料',
        '认证': 'CE, FCC, ROHS',
      },
      rating: Number((4 + Math.random()).toFixed(1)),
      reviewCount: Math.floor(Math.random() * 3000) + 50,
      salesVolume,
      trend: item.trend > 15 ? 'up' : item.trend > 5 ? 'stable' : 'down',
      trendValue: item.trend,
      region: item.region,
    };
  });

  // 生成更多随机产品
  for (let i = 0; i < 200; i++) {
    const baseProduct = hotProducts[i % hotProducts.length];
    const priceVariation = 0.8 + Math.random() * 0.4;
    
    products.push({
      id: `real-${hotProducts.length + i + 1}`,
      name: `热销${baseProduct.sub} ${['批发', '定制', '代工', '贴牌'][Math.floor(Math.random() * 4)]}`,
      description: `${baseProduct.region}产地，${['一件代发', '量大从优', '品质保证', '现货供应'][Math.floor(Math.random() * 4)]}`,
      category: baseProduct.category,
      subcategory: baseProduct.sub,
      price: {
        min: Math.floor(baseProduct.price * priceVariation * 0.9),
        max: Math.floor(baseProduct.price * priceVariation * 1.1),
        currency: 'CNY',
        unit: '件',
      },
      moq: Math.floor(baseProduct.moq * (0.5 + Math.random())),
      supplier: {
        name: suppliers[Math.floor(Math.random() * suppliers.length)],
        location: baseProduct.region,
        rating: Number((3.5 + Math.random() * 1.5).toFixed(1)),
        yearsInBusiness: Math.floor(Math.random() * 15) + 1,
        verified: Math.random() > 0.3,
      },
      images: [],
      specifications: {},
      rating: Number((3.5 + Math.random() * 1.5).toFixed(1)),
      reviewCount: Math.floor(Math.random() * 2000),
      salesVolume: Math.floor(Math.random() * 50000),
      trend: Math.random() > 0.5 ? 'up' : Math.random() > 0.3 ? 'stable' : 'down',
      trendValue: Number((Math.random() * 40 - 10).toFixed(1)),
      region: baseProduct.region,
    });
  }

  // 生成海关数据
  const customsData = [];
  const destinations = ['美国', '德国', '日本', '韩国', '越南', '英国', '荷兰', '澳大利亚', '俄罗斯', '印度', '巴西', '阿联酋'];
  const hsCodePrefix = ['85', '84', '62', '61', '94', '39', '73', '87', '90', '95'];
  
  for (const product of hotProducts.slice(0, 15)) {
    for (const dest of destinations) {
      const baseValue = Math.floor(Math.random() * 40000) + 5000;
      const yoyGrowth = Number((Math.random() * 50 - 15).toFixed(1));
      
      customsData.push({
        date: '2024-02',
        productName: product.category,
        hsCode: `${hsCodePrefix[Math.floor(Math.random() * hsCodePrefix.length)]}.${Math.floor(Math.random() * 99)}.${Math.floor(Math.random() * 99)}`,
        exportValue: baseValue,
        exportQuantity: Math.floor(baseValue * (10 + Math.random() * 20)),
        destination: dest,
        yoyGrowth,
        momGrowth: Number((Math.random() * 20 - 5).toFixed(1)),
      });
    }
  }

  // 保存数据
  fs.writeFileSync(
    path.join(DATA_DIR, 'all-products.json'),
    JSON.stringify(products, null, 2)
  );
  
  fs.writeFileSync(
    path.join(DATA_DIR, 'customs-data.json'),
    JSON.stringify(customsData, null, 2)
  );

  console.log(`✅ 成功生成 ${products.length} 个产品数据`);
  console.log(`✅ 成功生成 ${customsData.length} 条海关数据`);
  console.log(`📁 数据已保存到: ${DATA_DIR}\n`);
  
  // 打印数据摘要
  console.log('=== 数据摘要 ===');
  const categoryCount = {};
  products.forEach(p => {
    categoryCount[p.category] = (categoryCount[p.category] || 0) + 1;
  });
  
  console.log('\n按品类分布:');
  Object.entries(categoryCount)
    .sort((a, b) => b[1] - a[1])
    .forEach(([cat, count]) => {
      console.log(`  ${cat}: ${count} 个产品`);
    });
  
  console.log('\n按地区分布:');
  const regionCount = {};
  products.forEach(p => {
    regionCount[p.region] = (regionCount[p.region] || 0) + 1;
  });
  Object.entries(regionCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .forEach(([reg, count]) => {
      console.log(`  ${reg}: ${count} 个产品`);
    });
  
  console.log('\n按趋势分布:');
  const upCount = products.filter(p => p.trend === 'up').length;
  const stableCount = products.filter(p => p.trend === 'stable').length;
  const downCount = products.filter(p => p.trend === 'down').length;
  console.log(`  上升: ${upCount} (${(upCount/products.length*100).toFixed(1)}%)`);
  console.log(`  平稳: ${stableCount} (${(stableCount/products.length*100).toFixed(1)}%)`);
  console.log(`  下降: ${downCount} (${(downCount/products.length*100).toFixed(1)}%)`);
  
  console.log('\n增长最快的产品 (TOP 5):');
  products
    .sort((a, b) => b.trendValue - a.trendValue)
    .slice(0, 5)
    .forEach((p, i) => {
      console.log(`  ${i+1}. ${p.name} - +${p.trendValue}%`);
    });
  
  return { products, customs: customsData };
}

// 执行
generateRealisticData();
