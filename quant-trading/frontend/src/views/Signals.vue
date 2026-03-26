<template>
  <div class="signals">
    <el-row :gutter="20">
      <!-- 买入信号 -->
      <el-col :span="12">
        <el-card class="signal-card">
          <template #header>
            <div class="card-header">
              <span class="buy-title">📈 买入信号</span>
              <el-select v-model="buyStrategy" size="small" style="width: 120px">
                <el-option label="综合策略" value="combined" />
                <el-option label="MA交叉" value="ma_cross" />
                <el-option label="MACD" value="macd" />
                <el-option label="KDJ" value="kdj" />
                <el-option label="布林带" value="boll" />
                <el-option label="RSI" value="rsi" />
              </el-select>
              <el-button type="success" size="small" @click="scanBuySignals" :loading="loadingBuy">
                扫描
              </el-button>
            </div>
          </template>
          
          <div v-if="buySignals.length === 0" class="empty-state">
            <el-empty description="暂无买入信号，点击扫描查找机会" />
          </div>
          
          <div v-else class="signal-list">
            <div v-for="signal in buySignals" :key="signal.code" 
                 class="signal-item buy"
                 @click="goToStock(signal.code)">
              <div class="signal-main">
                <div class="stock-info">
                  <div class="stock-name">{{ signal.name }}</div>
                  <div class="stock-code">{{ signal.code }}</div>
                </div>
                
                <div class="price-info">
                  <div class="current-price">{{ signal.price.toFixed(2) }}</div>
                  <div class="change" :class="signal.change_percent >= 0 ? 'up' : 'down'">
                    {{ signal.change_percent >= 0 ? '+' : '' }}{{ signal.change_percent.toFixed(2) }}%
                  </div>
                </div>
              </div>
              
              <div class="signal-detail">
                <div class="signal-type">{{ signal.signal === 'BUY' ? '强烈买入' : '弱买入' }}</div>
                <div class="signal-reason">{{ signal.reason }}</div>
                
                <div class="signal-strength">
                  <span>信号强度</span>
                  <el-progress 
                    :percentage="Math.min(signal.strength, 100)"
                    :color="getStrengthColor"
                    :stroke-width="6"
                  />
                </div>
                
                <div class="turnover">换手率: {{ signal.turnover_ratio.toFixed(2) }}%</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 卖出信号 -->
      <el-col :span="12">
        <el-card class="signal-card">
          <template #header>
            <div class="card-header">
              <span class="sell-title">📉 卖出信号</span>
              <el-select v-model="sellStrategy" size="small" style="width: 120px">
                <el-option label="综合策略" value="combined" />
                <el-option label="MA交叉" value="ma_cross" />
                <el-option label="MACD" value="macd" />
                <el-option label="KDJ" value="kdj" />
                <el-option label="布林带" value="boll" />
                <el-option label="RSI" value="rsi" />
              </el-select>
              <el-button type="danger" size="small" @click="scanSellSignals" :loading="loadingSell">
                扫描
              </el-button>
            </div>
          </template>
          
          <div v-if="sellSignals.length === 0" class="empty-state">
            <el-empty description="暂无卖出信号" />
          </div>
          
          <div v-else class="signal-list">
            <div v-for="signal in sellSignals" :key="signal.code" 
                 class="signal-item sell"
                 @click="goToStock(signal.code)">
              <div class="signal-main">
                <div class="stock-info">
                  <div class="stock-name">{{ signal.name }}</div>
                  <div class="stock-code">{{ signal.code }}</div>
                </div>
                
                <div class="price-info">
                  <div class="current-price">{{ signal.price.toFixed(2) }}</div>
                  <div class="change" :class="signal.change_percent >= 0 ? 'up' : 'down'">
                    {{ signal.change_percent >= 0 ? '+' : '' }}{{ signal.change_percent.toFixed(2) }}%
                  </div>
                </div>
              </div>
              
              <div class="signal-detail">
                <div class="signal-type">{{ signal.signal === 'SELL' ? '强烈卖出' : '弱卖出' }}</div>
                <div class="signal-reason">{{ signal.reason }}</div>
                
                <div class="signal-strength">
                  <span>信号强度</span>
                  <el-progress 
                    :percentage="Math.min(signal.strength, 100)"
                    :color="getStrengthColor"
                    :stroke-width="6"
                  />
                </div>
                
                <div class="turnover">换手率: {{ signal.turnover_ratio.toFixed(2) }}%</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 自动刷新设置 -->
    <el-card class="settings-card">
      <template #header>
        <span>⚙️ 自动扫描设置</span>
      </template>
      
      <el-form inline>
        <el-form-item label="自动刷新">
          <el-switch v-model="autoRefresh" @change="handleAutoRefresh" />
        </el-form-item>
        
        <el-form-item label="刷新间隔">
          <el-select v-model="refreshInterval" :disabled="!autoRefresh">
            <el-option label="5分钟" :value="300000" />
            <el-option label="15分钟" :value="900000" />
            <el-option label="30分钟" :value="1800000" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="scanAll">立即扫描全部</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { strategyApi } from '../api'

const router = useRouter()

const buySignals = ref([])
const sellSignals = ref([])
const buyStrategy = ref('combined')
const sellStrategy = ref('combined')
const loadingBuy = ref(false)
const loadingSell = ref(false)
const autoRefresh = ref(false)
const refreshInterval = ref(300000)
let refreshTimer = null

const scanBuySignals = async () => {
  loadingBuy.value = true
  try {
    const res = await strategyApi.scanBuySignals(buyStrategy.value, 20)
    buySignals.value = res.data.signals || []
  } catch (error) {
    console.error('Failed to scan buy signals:', error)
  } finally {
    loadingBuy.value = false
  }
}

const scanSellSignals = async () => {
  loadingSell.value = true
  try {
    const res = await strategyApi.scanSellSignals(sellStrategy.value, 20)
    sellSignals.value = res.data.signals || []
  } catch (error) {
    console.error('Failed to scan sell signals:', error)
  } finally {
    loadingSell.value = false
  }
}

const scanAll = () => {
  scanBuySignals()
  scanSellSignals()
}

const handleAutoRefresh = (enabled) => {
  if (enabled) {
    refreshTimer = setInterval(() => {
      scanAll()
    }, refreshInterval.value)
  } else {
    if (refreshTimer) {
      clearInterval(refreshTimer)
      refreshTimer = null
    }
  }
}

const goToStock = (code) => {
  router.push(`/stock/${code}`)
}

const getStrengthColor = (percentage) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 60) return '#e6a23c'
  if (percentage >= 40) return '#f56c6c'
  return '#909399'
}

onMounted(() => {
  scanAll()
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped>
.signals {
  padding: 10px;
}

.signal-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.buy-title {
  color: #67c23a;
  font-weight: bold;
}

.sell-title {
  color: #f56c6c;
  font-weight: bold;
}

.empty-state {
  padding: 40px;
}

.signal-list {
  max-height: 600px;
  overflow-y: auto;
}

.signal-item {
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.signal-item:hover {
  transform: translateX(5px);
}

.signal-item.buy {
  background: #67c23a11;
  border-left: 4px solid #67c23a;
}

.signal-item.sell {
  background: #f56c6c11;
  border-left: 4px solid #f56c6c;
}

.signal-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.stock-name {
  font-size: 16px;
  font-weight: bold;
  color: #fff;
}

.stock-code {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.current-price {
  font-size: 20px;
  font-weight: bold;
  color: #fff;
  text-align: right;
}

.change {
  font-size: 12px;
  text-align: right;
  margin-top: 4px;
}

.up {
  color: #f56c6c;
}

.down {
  color: #67c23a;
}

.signal-detail {
  padding-top: 10px;
  border-top: 1px solid #2a2a3e;
}

.signal-type {
  font-weight: bold;
  margin-bottom: 5px;
}

.signal-item.buy .signal-type {
  color: #67c23a;
}

.signal-item.sell .signal-type {
  color: #f56c6c;
}

.signal-reason {
  font-size: 12px;
  color: #ccc;
  margin-bottom: 8px;
}

.signal-strength {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 5px;
}

.signal-strength span {
  font-size: 12px;
  color: #909399;
  white-space: nowrap;
}

.turnover {
  font-size: 12px;
  color: #909399;
}

.settings-card {
  margin-top: 20px;
}
</style>
