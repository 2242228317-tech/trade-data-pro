<template>
  <div class="backtest">
    <!-- 回测配置 -->
    <el-card class="config-card">
      <template #header>
        <span>⚙️ 回测配置</span>
      </template>
      
      <el-form :model="config" label-width="120px" inline>
        <el-form-item label="股票代码">
          <el-input v-model="config.code" placeholder="000001" style="width: 120px" />
        </el-form-item>
        
        <el-form-item label="策略类型">
          <el-select v-model="config.strategy" style="width: 150px">
            <el-option label="MA交叉" value="ma_cross" />
            <el-option label="MACD" value="macd" />
            <el-option label="KDJ" value="kdj" />
            <el-option label="布林带" value="boll" />
            <el-option label="RSI" value="rsi" />
            <el-option label="综合策略" value="combined" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="回测周期">
          <el-select v-model="config.days" style="width: 120px">
            <el-option label="6个月" :value="180" />
            <el-option label="1年" :value="365" />
            <el-option label="2年" :value="730" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="初始资金">
          <el-input-number v-model="config.capital" :min="10000" :step="50000" style="width: 150px" />
        </el-form-item>
        
        <el-form-item label="止损比例">
          <el-input-number v-model="config.stopLoss" :min="0.02" :max="0.2" :step="0.01" style="width: 100px" />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="runBacktest" :loading="loading" size="large">开始回测</el-button>
          <el-button @click="compareStrategies" :loading="comparing">策略对比</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 回测结果 -->
    <div v-if="result">
      <!-- 关键指标 -->
      <el-row :gutter="20" class="metrics-row">
        <el-col :span="4">
          <el-card class="metric-card">
            <div class="metric-value" :class="result.total_return_pct >= 0 ? 'up' : 'down'">
              {{ result.total_return_pct >= 0 ? '+' : '' }}{{ result.total_return_pct.toFixed(2) }}%
            </div>
            <div class="metric-label">总收益率</div>
          </el-card>
        </el-col>
        
        <el-col :span="4">
          <el-card class="metric-card">
            <div class="metric-value">{{ result.final_capital.toLocaleString() }}</div>
            <div class="metric-label">期末资金</div>
          </el-card>
        </el-col>
        
        <el-col :span="4">
          <el-card class="metric-card">
            <div class="metric-value">{{ result.total_trades }}</div>
            <div class="metric-label">交易次数</div>
          </el-card>
        </el-col>
        
        <el-col :span="4">
          <el-card class="metric-card">
            <div class="metric-value">{{ result.win_rate.toFixed(1) }}%</div>
            <div class="metric-label">胜率</div>
          </el-card>
        </el-col>
        
        <el-col :span="4">
          <el-card class="metric-card">
            <div class="metric-value down">{{ result.max_drawdown_pct.toFixed(2) }}%</div>
            <div class="metric-label">最大回撤</div>
          </el-card>
        </el-col>
        
        <el-col :span="4">
          <el-card class="metric-card">
            <div class="metric-value">{{ result.sharpe_ratio.toFixed(2) }}</div>
            <div class="metric-label">夏普比率</div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 图表 -->
      <el-row :gutter="20">
        <el-col :span="16">
          <el-card class="chart-card">
            <template #header>
              <span>📈 权益曲线</span>
            </template>
            <div ref="equityChart" class="chart"></div>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card class="trades-card">
            <template #header>
              <span>📝 交易记录</span>
            </template>
            
            <el-table :data="result.trades" height="400" size="small">
              <el-table-column prop="date" label="日期" width="100" />
              <el-table-column prop="action" label="操作" width="80">
                <template #default="{ row }">
                  <el-tag :type="row.action === 'BUY' ? 'success' : 'danger'" size="small">
                    {{ row.action === 'BUY' ? '买入' : '卖出' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="price" label="价格">
                <template #default="{ row }">
                  {{ row.price.toFixed(2) }}
                </template>
              </el-table-column>
              <el-table-column prop="shares" label="数量" />
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 策略对比结果 -->
    <el-card v-if="comparisonResult" class="comparison-card">
      <template #header>
        <span>📊 策略对比分析</span>
      </template>
      
      <el-table :data="comparisonData" style="width: 100%">
        <el-table-column prop="strategy" label="策略" />
        <el-table-column prop="total_return_pct" label="总收益率">
          <template #default="{ row }">
            <span :class="row.total_return_pct >= 0 ? 'up' : 'down'">
              {{ row.total_return_pct >= 0 ? '+' : '' }}{{ row.total_return_pct.toFixed(2) }}%
            </span>
          </template>
        </el-table-column>
        
        <el-table-column prop="win_rate" label="胜率">
          <template #default="{ row }">
            {{ row.win_rate.toFixed(1) }}%
          </template>
        </el-table-column>
        
        <el-table-column prop="max_drawdown_pct" label="最大回撤">
          <template #default="{ row }">
            <span class="down">{{ row.max_drawdown_pct.toFixed(2) }}%</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="sharpe_ratio" label="夏普比率" />
        
        <el-table-column prop="total_trades" label="交易次数" />
        
        <el-table-column prop="final_capital" label="期末资金">
          <template #default="{ row }">
            {{ row.final_capital.toLocaleString() }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'
import { backtestApi } from '../api'

const route = useRoute()

const config = ref({
  code: route.query.code || '000001',
  strategy: 'ma_cross',
  days: 365,
  capital: 100000,
  stopLoss: 0.08
})

const loading = ref(false)
const comparing = ref(false)
const result = ref(null)
const comparisonResult = ref(null)
const equityChart = ref(null)
let chartInstance = null

const comparisonData = computed(() => {
  if (!comparisonResult.value) return []
  return Object.entries(comparisonResult.value.comparison).map(([name, data]) => ({
    strategy: name,
    ...data
  }))
})

const runBacktest = async () => {
  loading.value = true
  comparisonResult.value = null
  try {
    const res = await backtestApi.runBacktest({
      code: config.value.code,
      strategy_type: config.value.strategy,
      initial_capital: config.value.capital,
      stop_loss: config.value.stopLoss
    })
    result.value = res.data
    
    setTimeout(() => {
      renderEquityChart()
    }, 100)
  } catch (error) {
    console.error('Backtest failed:', error)
  } finally {
    loading.value = false
  }
}

const compareStrategies = async () => {
  comparing.value = true
  result.value = null
  try {
    const res = await backtestApi.compareStrategies(config.value.code, config.value.days)
    comparisonResult.value = res.data
  } catch (error) {
    console.error('Comparison failed:', error)
  } finally {
    comparing.value = false
  }
}

const renderEquityChart = () => {
  if (!equityChart.value || !result.value) return
  
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(equityChart.value)
  
  const dates = result.value.equity_curve.map(d => d.date)
  const equities = result.value.equity_curve.map(d => d.equity)
  const prices = result.value.equity_curve.map(d => d.price)
  
  // 标记买卖点
  const buyPoints = []
  const sellPoints = []
  result.value.trades.forEach((trade, index) => {
    const dataIndex = dates.indexOf(trade.date)
    if (dataIndex >= 0) {
      const point = {
        xAxis: trade.date,
        yAxis: trade.action === 'BUY' ? prices[dataIndex] : prices[dataIndex],
        value: trade.action
      }
      if (trade.action === 'BUY') {
        buyPoints.push(point)
      } else {
        sellPoints.push(point)
      }
    }
  })
  
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['权益', '股价'],
      textStyle: { color: '#fff' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#666' } }
    },
    yAxis: [
      {
        type: 'value',
        name: '权益',
        position: 'left',
        axisLine: { lineStyle: { color: '#666' } },
        splitLine: { lineStyle: { color: '#333' } }
      },
      {
        type: 'value',
        name: '股价',
        position: 'right',
        axisLine: { lineStyle: { color: '#666' } },
        splitLine: { show: false }
      }
    ],
    dataZoom: [
      { type: 'inside' },
      { type: 'slider', bottom: '2%' }
    ],
    series: [
      {
        name: '权益',
        type: 'line',
        data: equities,
        smooth: true,
        lineStyle: { color: '#00d4aa', width: 2 },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: '#00d4aa66' },
              { offset: 1, color: '#00d4aa00' }
            ]
          }
        }
      },
      {
        name: '股价',
        type: 'line',
        yAxisIndex: 1,
        data: prices,
        smooth: true,
        lineStyle: { color: '#ffd700', width: 1 },
        markPoint: {
          data: [
            ...buyPoints.map(p => ({ ...p, itemStyle: { color: '#67c23a' } })),
            ...sellPoints.map(p => ({ ...p, itemStyle: { color: '#f56c6c' } }))
          ]
        }
      }
    ]
  }
  
  chartInstance.setOption(option)
}

onMounted(() => {
  window.addEventListener('resize', () => chartInstance?.resize())
  if (route.query.code) {
    runBacktest()
  }
})
</script>

<style scoped>
.backtest {
  padding: 10px;
}

.config-card {
  margin-bottom: 20px;
}

.metrics-row {
  margin-bottom: 20px;
}

.metric-card {
  text-align: center;
  padding: 15px;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 8px;
}

.metric-value.up {
  color: #f56c6c;
}

.metric-value.down {
  color: #67c23a;
}

.metric-label {
  color: #909399;
  font-size: 12px;
}

.chart-card, .trades-card, .comparison-card {
  margin-bottom: 20px;
}

.chart {
  height: 400px;
}

.up {
  color: #f56c6c;
}

.down {
  color: #67c23a;
}
</style>
