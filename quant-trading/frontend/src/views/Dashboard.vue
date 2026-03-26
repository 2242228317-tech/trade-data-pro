<template>
  <div class="dashboard">
    <!-- 市场概览卡片 -->
    <div class="overview-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-value up">{{ marketStats.upCount }}</div>
            <div class="stat-label">上涨家数</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-value down">{{ marketStats.downCount }}</div>
            <div class="stat-label">下跌家数</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-value">{{ marketStats.avgTurnover }}%</div>
            <div class="stat-label">平均换手率</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-value">{{ marketStats.totalAmount }}亿</div>
            <div class="stat-label">总成交额</div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 主要内容区 -->
    <el-row :gutter="20" class="main-section">
      <!-- 热门股票 -->
      <el-col :span="12">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>🔥 热门股票（高换手+上涨）</span>
              <el-button type="primary" size="small" @click="loadHotStocks">刷新</el-button>
            </div>
          </template>
          <el-table :data="hotStocks" style="width: 100%" height="400">
            <el-table-column prop="code" label="代码" width="100">
              <template #default="{ row }">
                <a @click="goToStock(row.code)" class="stock-link">{{ row.code }}</a>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="名称" width="120" />
            <el-table-column prop="price" label="现价">
              <template #default="{ row }">
                <span :class="getPriceClass(row.change_percent)">{{ row.price.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="change_percent" label="涨跌幅">
              <template #default="{ row }">
                <span :class="getPriceClass(row.change_percent)">{{ row.change_percent > 0 ? '+' : '' }}{{ row.change_percent.toFixed(2) }}%</span>
              </template>
            </el-table-column>
            <el-table-column prop="turnover_ratio" label="换手率">
              <template #default="{ row }">
                <span>{{ row.turnover_ratio.toFixed(2) }}%</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <!-- 买入信号 -->
      <el-col :span="12">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>📈 策略买入信号</span>
              <el-select v-model="signalStrategy" size="small" style="width: 120px">
                <el-option label="综合策略" value="combined" />
                <el-option label="MA交叉" value="ma_cross" />
                <el-option label="MACD" value="macd" />
                <el-option label="KDJ" value="kdj" />
              </el-select>
              <el-button type="success" size="small" @click="loadBuySignals">扫描</el-button>
            </div>
          </template>
          
          <div v-if="buySignals.length === 0" class="empty-state">
            暂无买入信号，点击扫描按钮查找机会
          </div>
          
          <el-table v-else :data="buySignals" style="width: 100%" height="400">
            <el-table-column prop="code" label="代码" width="100">
              <template #default="{ row }">
                <a @click="goToStock(row.code)" class="stock-link">{{ row.code }}</a>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="名称" width="120" />
            <el-table-column prop="price" label="现价">
              <template #default="{ row }">
                {{ row.price.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="change_percent" label="涨跌幅">
              <template #default="{ row }">
                <span :class="getPriceClass(row.change_percent)">{{ row.change_percent > 0 ? '+' : '' }}{{ row.change_percent.toFixed(2) }}%</span>
              </template>
            </el-table-column>
            <el-table-column prop="strength" label="信号强度">
              <template #default="{ row }">
                <el-progress 
                  :percentage="Math.min(row.strength, 100)" 
                  :color="getStrengthColor(row.strength)"
                  :stroke-width="8"
                />
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 高流动性股票池 -->
    <el-card class="data-card full-width">
      <template #header>
        <div class="card-header">
          <span>📊 高流动性股票池（成交额>1亿，换手率>3%）</span>
          <el-button type="primary" size="small" @click="loadFilteredStocks">刷新</el-button>
        </div>
      </template>
      
      <el-table :data="filteredStocks" style="width: 100%" v-loading="loading">
        <el-table-column prop="code" label="代码" width="100">
          <template #default="{ row }">
            <a @click="goToStock(row.code)" class="stock-link">{{ row.code }}</a>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" width="120" />
        <el-table-column prop="price" label="现价">
          <template #default="{ row }">
            <span :class="getPriceClass(row.change_percent)">{{ row.price.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="change_percent" label="涨跌幅">
          <template #default="{ row }">
            <span :class="getPriceClass(row.change_percent)">{{ row.change_percent > 0 ? '+' : '' }}{{ row.change_percent.toFixed(2) }}%</span>
          </template>
        </el-table-column>
        <el-table-column prop="volume" label="成交量">
          <template #default="{ row }">
            {{ formatVolume(row.volume) }}
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="成交额(亿)" />
        <el-table-column prop="turnover_ratio" label="换手率">
          <template #default="{ row }">
            <span>{{ row.turnover_ratio.toFixed(2) }}%</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="goToStock(row.code)">分析</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { stockApi, strategyApi } from '../api'

const router = useRouter()
const loading = ref(false)
const hotStocks = ref([])
const buySignals = ref([])
const filteredStocks = ref([])
const signalStrategy = ref('combined')

const marketStats = ref({
  upCount: 0,
  downCount: 0,
  avgTurnover: 0,
  totalAmount: 0
})

const loadHotStocks = async () => {
  try {
    const res = await strategyApi.getHotStocks(20)
    hotStocks.value = res.data.stocks || []
  } catch (error) {
    console.error('Failed to load hot stocks:', error)
  }
}

const loadBuySignals = async () => {
  loading.value = true
  try {
    const res = await strategyApi.scanBuySignals(signalStrategy.value, 20)
    buySignals.value = res.data.signals || []
  } catch (error) {
    console.error('Failed to load buy signals:', error)
  } finally {
    loading.value = false
  }
}

const loadFilteredStocks = async () => {
  loading.value = true
  try {
    const res = await stockApi.getFilteredStocks()
    filteredStocks.value = res.data.stocks || []
    
    // 计算市场统计
    if (filteredStocks.value.length > 0) {
      const upCount = filteredStocks.value.filter(s => s.change_percent > 0).length
      const downCount = filteredStocks.value.filter(s => s.change_percent < 0).length
      const avgTurnover = filteredStocks.value.reduce((sum, s) => sum + s.turnover_ratio, 0) / filteredStocks.value.length
      const totalAmount = filteredStocks.value.reduce((sum, s) => sum + s.amount, 0)
      
      marketStats.value = {
        upCount,
        downCount,
        avgTurnover: avgTurnover.toFixed(2),
        totalAmount: totalAmount.toFixed(2)
      }
    }
  } catch (error) {
    console.error('Failed to load filtered stocks:', error)
  } finally {
    loading.value = false
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

const getStrengthColor = (strength) => {
  if (strength >= 80) return '#67c23a'
  if (strength >= 60) return '#e6a23c'
  if (strength >= 40) return '#f56c6c'
  return '#909399'
}

const formatVolume = (volume) => {
  if (volume >= 100000000) {
    return (volume / 100000000).toFixed(2) + '亿'
  }
  if (volume >= 10000) {
    return (volume / 10000).toFixed(2) + '万'
  }
  return volume.toString()
}

onMounted(() => {
  loadHotStocks()
  loadFilteredStocks()
  loadBuySignals()
})
</script>

<style scoped>
.dashboard {
  padding: 10px;
}

.overview-cards {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  padding: 20px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 8px;
}

.stat-value.up {
  color: #f56c6c;
}

.stat-value.down {
  color: #67c23a;
}

.stat-label {
  color: #909399;
  font-size: 14px;
}

.main-section {
  margin-bottom: 20px;
}

.data-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}

.full-width {
  width: 100%;
}
</style>
