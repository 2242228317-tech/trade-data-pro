<template>
  <div class="watchlist">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>⭐ 我的自选股</span>
          <el-button type="primary" size="small" @click="showAddDialog = true">添加股票</el-button>
        </div>
      </template>
      
      <div v-if="watchlist.length === 0" class="empty-state">
        <el-empty description="暂无自选股，点击添加股票" />
        <el-button type="primary" @click="showAddDialog = true">添加股票</el-button>
      </div>
      
      <el-table v-else :data="watchlistData" style="width: 100%" v-loading="loading">
        <el-table-column prop="code" label="代码" width="100">
          <template #default="{ row }">
            <a @click="goToStock(row.code)" class="stock-link">{{ row.code }}</a>
          </template>
        </el-table-column>
        
        <el-table-column prop="name" label="名称" width="120" />
        
        <el-table-column prop="price" label="现价">
          <template #default="{ row }">
            <span :class="getPriceClass(row.change_percent)">{{ row.price?.toFixed(2) || '-' }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="change_percent" label="涨跌幅">
          <template #default="{ row }">
            <span :class="getPriceClass(row.change_percent)">{{ row.change_percent > 0 ? '+' : '' }}{{ row.change_percent?.toFixed(2) || '-' }}%</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="signal" label="策略信号">
          <template #default="{ row }">
            <el-tag v-if="row.signal" :type="getSignalType(row.signal)" size="small">
              {{ getSignalText(row.signal) }}
            </el-tag>
            <span v-else class="no-signal">--</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="strength" label="信号强度">
          <template #default="{ row }">
            <el-progress 
              v-if="row.strength"
              :percentage="Math.min(row.strength, 100)"
              :color="getStrengthColor"
              :stroke-width="6"
            />
            <span v-else class="no-signal">--</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="goToStock(row.code)">分析</el-button>
            <el-button type="danger" size="small" @click="removeStock(row.code)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加股票对话框 -->
    <el-dialog v-model="showAddDialog" title="添加自选股" width="400px">
      <el-form :model="addForm">
        <el-form-item label="股票代码">
          <el-input v-model="addForm.code" placeholder="输入6位股票代码" maxlength="6" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="addStock">添加</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { stockApi, strategyApi } from '../api'

const router = useRouter()
const loading = ref(false)
const showAddDialog = ref(false)
const watchlist = ref([])
const stockData = ref({})
const signals = ref({})

const addForm = ref({
  code: ''
})

const watchlistData = computed(() => {
  return watchlist.value.map(code => {
    const data = stockData.value[code] || {}
    const signal = signals.value[code] || {}
    return {
      code,
      name: data.name || '--',
      price: data.price,
      change_percent: data.change_percent,
      signal: signal.signal,
      strength: signal.strength
    }
  })
})

const loadWatchlist = async () => {
  // 从localStorage加载
  const saved = localStorage.getItem('quant_watchlist')
  if (saved) {
    watchlist.value = JSON.parse(saved)
    await loadStockData()
  }
}

const loadStockData = async () => {
  if (watchlist.value.length === 0) return
  
  loading.value = true
  try {
    // 获取实时数据
    const realtimeRes = await stockApi.getRealtimeStocks(500)
    const stocks = realtimeRes.data || []
    
    // 获取策略信号
    for (const code of watchlist.value) {
      try {
        const signalRes = await strategyApi.getStrategySignal(code, 'combined')
        signals.value[code] = signalRes.data
      } catch (e) {
        signals.value[code] = {}
      }
    }
    
    // 匹配数据
    for (const stock of stocks) {
      if (watchlist.value.includes(stock.code)) {
        stockData.value[stock.code] = stock
      }
    }
  } catch (error) {
    console.error('Failed to load stock data:', error)
  } finally {
    loading.value = false
  }
}

const addStock = () => {
  const code = addForm.value.code.trim()
  if (!code) {
    return
  }
  
  if (!watchlist.value.includes(code)) {
    watchlist.value.push(code)
    localStorage.setItem('quant_watchlist', JSON.stringify(watchlist.value))
    loadStockData()
  }
  
  showAddDialog.value = false
  addForm.value.code = ''
}

const removeStock = (code) => {
  const index = watchlist.value.indexOf(code)
  if (index > -1) {
    watchlist.value.splice(index, 1)
    localStorage.setItem('quant_watchlist', JSON.stringify(watchlist.value))
    delete stockData.value[code]
    delete signals.value[code]
  }
}

const goToStock = (code) => {
  router.push(`/stock/${code}`)
}

const getPriceClass = (change) => {
  if (change > 0) return 'up'
  if (change < 0) return 'down'
  return ''
}

const getSignalType = (signal) => {
  if (signal === 'BUY') return 'success'
  if (signal === 'SELL') return 'danger'
  if (signal === 'WEAK_BUY') return 'warning'
  if (signal === 'WEAK_SELL') return 'warning'
  return 'info'
}

const getSignalText = (signal) => {
  const map = {
    'BUY': '买入',
    'SELL': '卖出',
    'HOLD': '持有',
    'WEAK_BUY': '弱买',
    'WEAK_SELL': '弱卖'
  }
  return map[signal] || signal
}

const getStrengthColor = (percentage) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 60) return '#e6a23c'
  if (percentage >= 40) return '#f56c6c'
  return '#909399'
}

onMounted(() => {
  loadWatchlist()
  // 定时刷新
  setInterval(loadStockData, 30000)
})
</script>

<style scoped>
.watchlist {
  padding: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-state {
  text-align: center;
  padding: 60px;
}

.stock-link {
  color: #409eff;
  cursor: pointer;
  text-decoration: none;
}

.stock-link:hover {
  text-decoration: underline;
}

.up {
  color: #f56c6c;
}

.down {
  color: #67c23a;
}

.no-signal {
  color: #909399;
}
</style>
