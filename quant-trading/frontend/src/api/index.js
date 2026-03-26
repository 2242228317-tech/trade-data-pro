import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 股票数据API
export const stockApi = {
  // 获取实时股票数据
  getRealtimeStocks: (limit = 50, minTurnover = 0) => 
    api.get(`/api/stocks/realtime?limit=${limit}&min_turnover=${minTurnover}`),
  
  // 获取筛选后的股票
  getFilteredStocks: (params = {}) => 
    api.get('/api/stocks/filtered', { params }),
  
  // 获取股票历史数据
  getStockHistory: (code, days = 365) => 
    api.get(`/api/stocks/${code}/history?days=${days}`),
  
  // 获取股票基本信息
  getStockInfo: (code) => 
    api.get(`/api/stocks/${code}/info`),
  
  // 获取资金流向
  getMoneyFlow: (code) => 
    api.get(`/api/stocks/${code}/moneyflow`)
}

// 技术指标API
export const indicatorApi = {
  // 获取所有技术指标
  getAllIndicators: (code, days = 365) => 
    api.get(`/api/indicators/${code}/all?days=${days}`),
  
  // 获取最新信号
  getLatestSignals: (code) => 
    api.get(`/api/indicators/${code}/signals`)
}

// 策略API
export const strategyApi = {
  // 获取策略信号
  getStrategySignal: (code, strategyType = 'combined') => 
    api.get(`/api/strategy/${code}/signal?strategy_type=${strategyType}`),
  
  // 获取所有策略信号对比
  getAllSignals: (code) => 
    api.get(`/api/strategy/${code}/all-signals`),
  
  // 扫描买入信号
  scanBuySignals: (strategyType = 'combined', limit = 20) => 
    api.get(`/api/strategy/scan/buy-signals?strategy_type=${strategyType}&limit=${limit}`),
  
  // 扫描卖出信号
  scanSellSignals: (strategyType = 'combined', limit = 20) => 
    api.get(`/api/strategy/scan/sell-signals?strategy_type=${strategyType}&limit=${limit}`),
  
  // 获取热门股票
  getHotStocks: (limit = 20) => 
    api.get(`/api/strategy/hot-stocks?limit=${limit}`)
}

// 回测API
export const backtestApi = {
  // 运行回测
  runBacktest: (data) => 
    api.post('/api/backtest/run', data),
  
  // 对比策略
  compareStrategies: (code, days = 365) => 
    api.get(`/api/backtest/compare/${code}?days=${days}`),
  
  // 蒙特卡洛模拟
  monteCarlo: (code, strategyType = 'ma_cross', runs = 100) => 
    api.get(`/api/backtest/monte-carlo/${code}?strategy_type=${strategyType}&runs=${runs}`),
  
  // 参数优化
  optimizeParams: (code, strategyType = 'ma_cross') => 
    api.get(`/api/backtest/optimize/${code}?strategy_type=${strategyType}`)
}

export default api
