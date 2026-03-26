from flask import Flask, render_template, jsonify, request
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DATABASE = 'database/trade_data.db'

# 确保数据库目录存在
os.makedirs('database', exist_ok=True)

# 导入爬虫
try:
    from crawler.alibaba_http import AlibabaHttpCrawler as AlibabaCrawler
    from crawler.customs_real import CustomsRealCrawler
    REAL_CRAWLER_AVAILABLE = True
    print("[Init] HTTP crawlers loaded")
except ImportError as e:
    print(f"[Warning] HTTP crawlers not available: {e}")
    REAL_CRAWLER_AVAILABLE = False

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 阿里巴巴数据表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alibaba_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            price REAL,
            currency TEXT,
            min_order TEXT,
            supplier TEXT,
            location TEXT,
            sales_count INTEGER DEFAULT 0,
            revenue_estimate REAL DEFAULT 0,
            product_url TEXT,
            image_url TEXT,
            crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 海关数据表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customs_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            category TEXT,
            hs_code TEXT,
            export_value REAL,
            export_weight REAL,
            unit TEXT,
            destination_country TEXT,
            trade_month TEXT,
            crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[Database] Initialized successfully")

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/alibaba')
def alibaba_page():
    """阿里巴巴数据页面"""
    return render_template('alibaba.html')

@app.route('/customs')
def customs_page():
    """海关数据页面"""
    return render_template('customs.html')

@app.route('/api/alibaba/data')
def get_alibaba_data():
    """获取阿里巴巴数据 API"""
    sort_by = request.args.get('sort', 'revenue_estimate')
    order = request.args.get('order', 'DESC')
    limit = request.args.get('limit', 50, type=int)
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # 获取数据
    cursor.execute(f'''
        SELECT * FROM alibaba_products 
        ORDER BY {sort_by} {order} 
        LIMIT {limit}
    ''')
    
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        data.append(dict(zip(columns, row)))
    
    conn.close()
    
    return jsonify({
        'success': True,
        'data': data,
        'count': len(data)
    })

@app.route('/api/customs/data')
def get_customs_data():
    """获取海关数据 API"""
    category = request.args.get('category', '')
    sort_by = request.args.get('sort', 'export_value')
    order = request.args.get('order', 'DESC')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    query = f'''
        SELECT * FROM customs_data 
        WHERE 1=1
    '''
    
    if category:
        query += f" AND category = '{category}'"
    
    query += f" ORDER BY {sort_by} {order}"
    
    cursor.execute(query)
    
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        data.append(dict(zip(columns, row)))
    
    conn.close()
    
    return jsonify({
        'success': True,
        'data': data,
        'count': len(data)
    })

@app.route('/api/crawl/alibaba', methods=['POST'])
def crawl_alibaba():
    """触发阿里巴巴爬虫"""
    keyword = request.json.get('keyword', 'lobster')
    
    try:
        # 使用 HTTP 爬虫
        if REAL_CRAWLER_AVAILABLE:
            print("[Crawl] Using HTTP Alibaba crawler")
            crawler = AlibabaCrawler()
        else:
            print("[Crawl] Using mock Alibaba crawler")
            from crawler.alibaba import AlibabaCrawler as MockCrawler
            crawler = MockCrawler()
        
        result = crawler.crawl(keyword, pages=2)
        
        return jsonify({
            'success': True,
            'message': f'Crawled {result["count"]} products',
            'data': result
        })
    except Exception as e:
        import traceback
        print(f"[Error] {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/crawl/customs', methods=['POST'])
def crawl_customs():
    """触发海关数据爬虫"""
    try:
        # 优先使用真实爬虫
        if REAL_CRAWLER_AVAILABLE:
            print("[Crawl] Using real Customs crawler")
            crawler = CustomsRealCrawler()
        else:
            print("[Crawl] Using mock Customs crawler")
            from crawler.customs import CustomsCrawler
            crawler = CustomsCrawler()
        
        result = crawler.crawl()
        
        return jsonify({
            'success': True,
            'message': f'Crawled {result["count"]} records',
            'data': result
        })
    except Exception as e:
        import traceback
        print(f"[Error] {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/alibaba/categories')
def get_alibaba_categories():
    """获取产品分类"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT DISTINCT location FROM alibaba_products 
        WHERE location IS NOT NULL
    ''')
    
    locations = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'locations': locations})

@app.route('/api/customs/categories')
def get_customs_categories():
    """获取海关数据分类"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT DISTINCT category FROM customs_data 
        WHERE category IS NOT NULL
    ''')
    
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'categories': categories})

if __name__ == '__main__':
    init_db()
    print("[Server] Starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
