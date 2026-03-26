<template>
  <div class="stock-detail" v-loading="loading">
    <!-- 股票头部信息 -->
    <div class="stock-header" v-if="stockInfo">
      <div class="stock-title">
        <h1>{{ stockInfo.name }} <span class="stock-code">{{ code }}</span></h1>
        <div class="stock-industry" v-if="stockInfo.industry">
          {{ stockInfo.industry }} | {{ stockInfo.area }}
        </div>
      </div>
      
      <div class="stock-price" v-if="currentData">
        <div class="price" :class="getPriceClass(currentData.change_percent)">
          {{ currentData.price.toFixed(2) }}
        </div>
        <div class="change" :class="getPriceClass(currentData.change_percent)">
          {{ currentData.change_percent > 0 ? '+' : '' }}{{ currentData.change_percent.toFixed(2) }}%
        </div>
      </div>
    </div>

    <!-- 策略信号 -->
    <el-card class="signal-card" v-if="strategySignal">
      <template #header>
        <span>🎯 策略信号 - {{ getStrategyName(strategyType) }}</span>
      </template>
      
      <div class="signal-content">
        <div class="signal-badge" :class="strategySignal.signal.toLowerCase()">
          {{ getSignalText(strategySignal.signal) }}
        </div>
        <div class="signal-info">
          <p>{{ strategySignal.reason }}</p>
          <el-progress 
            v-if="strategySignal.strength"
            :percentage="Math.min(strategySignal.strength, 100)"
            :color="getStrengthColor"
            :stroke-width="12"
          />
        </div>
      </div>
    </el-card>

    <!-- 技术指标信号 -->
    <el-card class="indicators-card" v-if="indicatorSignals">
      <template #header>
        <span>📊 技术指标信号</span>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="indicator-item">
            <div class="indicator-name">均线信号</div>
            <el-tag :type="indicatorSignals.ma_golden_cross ? 'success' : (indicatorSignals.ma_death_cross ? 'danger' : 'info')">
              {{ indicatorSignals.ma_golden_cross ? '金叉' : (indicatorSignals.ma_death_cross ? '死叉' : '无信号') }}
            </el-tag>
          </div>
        </el-col>
        
        <el-col :span="8">
          <div class="indicator-item">
            <div class="indicator-name">MACD信号</div>
            <el-tag :type="indicatorSignals.macd_golden_cross ? 'success' : (indicatorSignals.macd_death_cross ? 'danger' : 'info')">
              {{ indicatorSignals.macd_golden_cross ? '金叉' : (indicatorSignals.macd_death_cross ? '死叉' : '无信号') }}
            </el-tag>
          </div>
        </el-col>
        
        <el-col :span="8">
          <div class="indicator-item">
            <div class="indicator-name">KDJ信号</div>
            <el-tag :type="indicatorSignals.kdj_golden_cross ? 'success' : (indicatorSignals.kdj_overbought ? 'danger' : (indicatorSignals.kdj_oversold ? 'success' : 'info'))">
              {{ indicatorSignals.kdj_golden_cross ? '金叉' : (indicatorSignals.kdj_overbought ? '超买' : (indicatorSignals.kdj_oversold ? '超卖' : '无信号')) }}
            </el-tag>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- K线图 -->
    <el-card class="chart-card">
      <template #header>
        <div class="chart-header">
          <span>📈 K线图与技术指标</span>
          <el-radio-group v-model="chartPeriod" size="small" @change="loadData">
            <el-radio-button label="6m">6个月</el-radio-button>
            <el-radio-button label="1y">1年</el-radio-button>
            <el-radio-button label="2y">2年</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      
      <div ref="klineChart" class="kline-chart"></div>
    </el-card>

    <!-- 指标数值 -->
    <el-card class="values-card" v-if="indicatorValues">
      <template #header>
        <span>📋 最新指标数值</span>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="value-section">
            <h4>移动平均线</h4>
            <div class="value-item">
              <span class="label">MA5:</span>
              <span class="value">{{ indicatorValues.ma5?.toFixed(2) || '-' }}</span>
            </div>
            <div class="value-item">
              <span class="label">MA10:</span>
              <span class="value">{{ indicatorValues.ma10?.toFixed(2) || '-' }}</span>
            </div>
            <div class="value-item">
              <span class="label">MA20:</span>
              <span class="value">{{ indicatorValues.ma20?.toFixed(2) || '-' }}</span>
            </div>
            <div class="value-item">
              <span class="label">MA60:</span>
              <span class="value">{{ indicatorValues.ma60?.toFixed(2) || '-' }}</span>
            </div>
          </div>
        </el-col>
        
        <el-col :span="6">
          <div class="value-section">
            <h4>MACD</h4>
            <div class="value-item">
              <span class="label">DIFF:</span>
              <span class="value" :class="getValueClass(indicatorValues.macd_diff)">{{ indicatorValues.macd_diff?.toFixed(3) || '-' }}</span>
            </div>
            <div class="value-item">
              <span class="label">DEA:</span>
              <span class="value">{{ indicatorValues.macd_dea?.toFixed(3) || '-' }}</span>
            </div>
            <div class="value-item">
              <span class="label">MACD:</span>
              <span class="value" :class="getValueClass(indicatorValues.macd)">{{ indicatorValues.macd?.toFixed(3) || '-' }}</span>
            </div>
          </div>
        </el-col>
        
        <el-col :span="6">
          <div class="value-section">
            <h4>KDJ</h4>
            <div class="value-item">
              <span class="label">K:</span>
              <span class="value">{{ indicatorValues.kdj_k?.toFixed(2) || '-' }}</span>
            </div>
            <div class="value-item">
              <span class="label">D:</span>
              <span class="value">{{ indicatorValues.kdj_d?.toFixed(2) || '-' }}</span>
            </div>
            <div class="value-item">
              <span class="label">J:</span>
              <span class="value" :class="getKDJClass(indicatorValues.kdj_j)">{{ indicatorValues.kdj_j?.toFixed(2) || '-' }}</span>
            </div>
          </div>
        </el-col>
        
        <el-col :span="6">
          <div class="value-section">
            <h4>布林带/RSI</h4>
            <div class="value-item">
              <span class="label">上轨:</span>
              <span class="value">{{ indicatorValues.boll_upper?.toFixed(2) || '-' }}</span>
            </div>
            <div class="value-item">
              <span class="label">中轨:</span>
              <span class="value">{{ indicatorValues.boll_mid?.toFixed(2) || '-' }}</span>
            </div>
            <div class="value-item">
              <span class="label">下轨:</span>
              <span class="value">{{ indicatorValues.boll_lower?.toFixed(2) || '-' }}</span>
            </div>
            <div class="value-item">
              <span class="label">RSI6:</span>
              <span class="value" :class="getRSIClass(indicatorValues.rsi6)">{{ indicatorValues.rsi6?.toFixed(2) || '-' }}</span>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 操作按钮 -->
    <div class="actions">
      <el-button type="primary" size="large" @click="goToBacktest">
        <el-icon><TrendCharts /></el-icon> 策略回测
      </el-button>
      
      <el-button type="success" size="large" @click="addToWatchlist">
        <el-icon><Star /></el-icon> 加入自选
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import * as echarts from 'echarts'
import { stockApi, indicatorApi, strategyApi } from '../api'

const route = useRoute()
const router = useRouter()
const props = defineProps(['code'])

const loading = ref(false)
const chartPeriod = ref('1y')
const klineChart = ref(null)
let chartInstance = null

const stockInfo = ref(null)
const currentData = ref(null)
const strategySignal = ref(null)
const indicatorSignals = ref(null)
const indicatorValues = ref(null)
const chartData = ref([])

const strategyType = ref('combined')

const loadData = async () => {
  loading.value = true
  try {
    const days = chartPeriod.value === '6m' ? 180 : (chartPeriod.value === '1y' ? 365 : 730)
    
    // 并行加载数据
    const [infoRes, signalsRes, indicatorsRes, strategyRes] = await Promise.all([
      stockApi.getStockInfo(props.code).catch(() => ({ data: {} })),
      indicatorApi.getLatestSignals(props.code).catch(() => ({ data: {} })),
      indicatorApi.getAllIndicators(props.code, days).catch(() => ({ data: { data: [] } })),
      strategyApi.getStrategySignal(props.code, strategyType.value).catch(() => ({ data: {} }))
    ])
    
    stockInfo.value = infoRes.data
    currentData.value = {
      price: signalsRes.data.price,
      change_percent: 0
    }
    indicatorSignals.value = signalsRes.data.signals
    indicatorValues.value = signalsRes.data.indicators
    strategySignal.value = strategyRes.data
    chartData.value = indicatorsRes.data.data || []
    
    renderChart()
  } catch (error) {
    console.error('Failed to load stock data:', error)
  } finally {
    loading.value = false
  }
}

const renderChart = () => {
  if (!klineChart.value || chartData.value.length === 0) return
  
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(klineChart.value)
  
  const dates = chartData.value.map(d => d.date)
  const klineData = chartData.value.map(d => [d.open, d.close, d.low, d.high])
  const ma5 = chartData.value.map(d => d.ma5)
  const ma20 = chartData.value.map(d => d.ma20)
  const ma60 = chartData.value.map(d => d.ma60)
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['K线', 'MA5', 'MA20', 'MA60'],
      textStyle: { color: '#fff' }
    },
    grid: {
      left: '3%',
      right: '3%',
      bottom: '10%'
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#666' } }
    },
    yAxis: {
      scale: true,
      axisLine: { lineStyle: { color: '#666' } },
      splitLine: { lineStyle: { color: '#333' } }
    },
    dataZoom: [
      { type: 'inside' },
      { type: 'slider', bottom: '2%' }
    ],
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        data: klineData,
        itemStyle: {
          color: '#f56c6c',
          color0: '#67c23a',
          borderColor: '#f56c6c',
          borderColor0: '#67c23a'
        }
      },
      {
        name: 'MA5',
        type: 'line',
        data: ma5,
        smooth: true,
        lineStyle: { color: '#ffd700', width: 1 }
      },
      {
        name: 'MA20',
        type: 'line',
        data: ma20,
        smooth: true,
        lineStyle: { color: '#00ced1', width: 1 }
      },
      {
        name: 'MA60',
        type: 'line',
        data: ma60,
        smooth: true,
        lineStyle: { color: '#ff69b4', width: 1 }
      }
    ]
  }
  
  chartInstance.setOption(option)
}

const goToBacktest = () => {
  router.push({
    path: '/backtest',
    query: { code: props.code }
  })
}

const addToWatchlist = () => {
  // 实现添加自选逻辑
}

const getPriceClass = (change) => {
  if (change > 0) return 'up'
  if (change < 0) return 'down'
  return ''
}

const getValueClass = (val) => {
  if (val > 0) return 'up'
  if (val < 0) return 'down'
  return ''
}

const getKDJClass = (val) => {
  if (val > 80) return 'overbought'
  if (val < 20) return 'oversold'
  return ''
}

const getRSIClass = (val) => {
  if (val > 80) return 'overbought'
  if (val < 20) return 'oversold'
  return ''
}

const getSignalText = (signal) => {
  const map = {
    'BUY': '买入',
    'SELL': '卖出',
    'HOLD': '持有',
    'WEAK_BUY': '弱买入',
    'WEAK_SELL': '弱卖出'
  }
  return map[signal] || signal
}

const getStrategyName = (type) => {
  const map = {
    'ma_cross': 'MA交叉',
    'macd': 'MACD',
    'kdj': 'KDJ',
    'boll': '布林带',
    'rsi': 'RSI',
    'combined': '综合策略'
  }
  return map[type] || type
}

const getStrengthColor = (percentage) => {
  if (percentage < 40) return '#909399'
  if (percentage < 60) return '#e6a23c'
  if (percentage < 80) return '#67c23a'
  return '#00d4aa'
}

watch(() => props.code, loadData)

onMounted(() => {
  loadData()
  window.addEventListener('resize', () => chartInstance?.resize())
})
</script>

<style scoped>
.stock-detail {
  padding: 10px;
}

.stock-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 20px;
  background: #1a1a2e;
  border-radius: 8px;
}

.stock-title h1 {
  margin: 0;
  color: #fff;
}

.stock-code {
  font-size: 18px;
  color: #909399;
  font-weight: normal;
}

.stock-industry {
  margin-top: 8px;
  color: #909399;
}

.stock-price {
  text-align: right;
}

.price {
  font-size: 36px;
  font-weight: bold;
}

.change {
  font-size: 18px;
  margin-top: 5px;
}

.up {
  color: #f56c6c;
}

.down {
  color: #67c23a;
}

.overbought {
  color: #f56c6c;
}

.oversold {
  color: #67c23a;
}

.signal-card, .indicators-card, .chart-card, .values-card {
  margin-bottom: 20px;
}

.signal-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.signal-badge {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 24px;
  font-weight: bold;
}

.signal-badge.buy {
  background: #67c23a33;
  color: #67c23a;
  border: 2px solid #67c23a;
}

.signal-badge.sell {
  background: #f56c6c33;
  color: #f56c6c;
  border: 2px solid #f56c6c;
}

.signal-badge.hold {
  background: #90939933;
  color: #909399;
  border: 2px solid #909399;
}

.signal-badge.weak_buy {
  background: #e6a23c33;
  color: #e6a23c;
  border: 2px solid #e6a23c;
}

.signal-info {
  flex: 1;
}

.signal-info p {
  margin: 0 0 10px 0;
  color: #fff;
}

.indicator-item {
  text-align: center;
  padding: 15px;
  background: #0f0f1e;
  border-radius: 8px;
}

.indicator-name {
  margin-bottom: 10px;
  color: #909399;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.kline-chart {
  height: 400px;
}

.values-card h4 {
  margin: 0 0 15px 0;
  color: #00d4aa;
}

.value-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #2a2a3e;
}

.value-item:last-child {
  border-bottom: none;
}

.label {
  color: #909399;
}

.value {
  font-weight: bold;
  color: #fff;
}

.actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 30px;
}
</style>
