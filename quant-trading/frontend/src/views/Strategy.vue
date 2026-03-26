<template>
  <div class="strategy">
    <el-row :gutter="20">
      <!-- 策略选择 -->
      <el-col :span="8">
        <el-card class="strategy-list">
          <template #header>
            <span>🎯 选择策略</span>
          </template>
          
          <el-menu
            :default-active="activeStrategy"
            @select="handleStrategySelect"
            class="strategy-menu"
          >
            <el-menu-item index="ma_cross">
              <div class="strategy-item">
                <div class="strategy-name">MA交叉策略</div>
                <div class="strategy-desc">双均线金叉买入，死叉卖出</div>
              </div>
            </el-menu-item>
            
            <el-menu-item index="macd">
              <div class="strategy-item">
                <div class="strategy-name">MACD策略</div>
                <div class="strategy-desc">DIFF上穿DEA买入，下穿卖出</div>
              </div>
            </el-menu-item>
            
            <el-menu-item index="kdj">
              <div class="strategy-item">
                <div class="strategy-name">KDJ策略</div>
                <div class="strategy-desc">KDJ金叉且J<80买入</div>
              </div>
            </el-menu-item>
            
            <el-menu-item index="boll">
              <div class="strategy-item">
                <div class="strategy-name">布林带策略</div>
                <div class="strategy-desc">下轨反弹买入，上轨回落卖出</div>
              </div>
            </el-menu-item>
            
            <el-menu-item index="rsi">
              <div class="strategy-item">
                <div class="strategy-name">RSI策略</div>
                <div class="strategy-desc">RSI超卖(<20)买入，超买(>80)卖出</div>
              </div>
            </el-menu-item>
            
            <el-menu-item index="combined">
              <div class="strategy-item">
                <div class="strategy-name">综合策略 ⭐</div>
                <div class="strategy-desc">多指标共振，3个以上信号确认</div>
              </div>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>

      <!-- 策略详情 -->
      <el-col :span="16">
        <el-card class="strategy-detail">
          <template #header>
            <span>📖 {{ currentStrategy.name }} - 详情</span>
          </template>
          
          <div class="strategy-info">
            <h3>策略逻辑</h3>
            <p>{{ currentStrategy.logic }}</p>
            
            <h3>买入条件</h3>
            <ul>
              <li v-for="(condition, index) in currentStrategy.buyConditions" :key="index">
                {{ condition }}
              </li>
            </ul>
            
            <h3>卖出条件</h3>
            <ul>
              <li v-for="(condition, index) in currentStrategy.sellConditions" :key="index">
                {{ condition }}
              </li>
            </ul>
            
            <h3>风险提示</h3>
            <el-alert
              :title="currentStrategy.risk"
              type="warning"
              :closable="false"
              show-icon
            />
          </div>
        </el-card>

        <!-- 快速回测 -->
        <el-card class="quick-backtest">
          <template #header>
            <span>⚡ 快速回测</span>
          </template>
          
          <el-form :model="backtestForm" label-width="100px">
            <el-form-item label="股票代码">
              <el-input v-model="backtestForm.code" placeholder="如: 000001" />
            </el-form-item>
            
            <el-form-item label="回测周期">
              <el-select v-model="backtestForm.days">
                <el-option label="6个月" :value="180" />
                <el-option label="1年" :value="365" />
                <el-option label="2年" :value="730" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="初始资金">
              <el-input-number v-model="backtestForm.capital" :min="10000" :step="10000" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="runQuickBacktest" :loading="loading">运行回测</el-button>
            </el-form-item>
          </el-form>

          <!-- 回测结果 -->
          <div v-if="backtestResult" class="backtest-result">
            <el-divider />
            <el-row :gutter="20">
              <el-col :span="6">
                <div class="result-item">
                  <div class="result-label">总收益率</div>
                  <div class="result-value" :class="backtestResult.total_return_pct >= 0 ? 'up' : 'down'">
                    {{ backtestResult.total_return_pct >= 0 ? '+' : '' }}{{ backtestResult.total_return_pct.toFixed(2) }}%
                  </div>
                </div>
              </el-col>
              
              <el-col :span="6">
                <div class="result-item">
                  <div class="result-label">胜率</div>
                  <div class="result-value">{{ backtestResult.win_rate.toFixed(2) }}%</div>
                </div>
              </el-col>
              
              <el-col :span="6">
                <div class="result-item">
                  <div class="result-label">最大回撤</div>
                  <div class="result-value down">{{ backtestResult.max_drawdown_pct.toFixed(2) }}%</div>
                </div>
              </el-col>
              
              <el-col :span="6">
                <div class="result-item">
                  <div class="result-label">夏普比率</div>
                  <div class="result-value">{{ backtestResult.sharpe_ratio.toFixed(2) }}</div>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { backtestApi } from '../api'

const router = useRouter()
const activeStrategy = ref('combined')
const loading = ref(false)
const backtestResult = ref(null)

const backtestForm = ref({
  code: '000001',
  days: 365,
  capital: 100000
})

const strategies = {
  ma_cross: {
    name: 'MA交叉策略',
    logic: '使用两条不同周期的移动平均线，当短期均线上穿长期均线时产生买入信号（金叉），当短期均线下穿长期均线时产生卖出信号（死叉）。',
    buyConditions: [
      '短期均线（如MA5）上穿长期均线（如MA20）',
      '交叉点在零轴上方表示强势买入',
      '成交量配合放大更佳'
    ],
    sellConditions: [
      '短期均线下穿长期均线（死叉）',
      '跌破支撑位确认卖出'
    ],
    risk: '震荡行情中可能产生频繁的假信号，建议结合其他指标使用。'
  },
  macd: {
    name: 'MACD策略',
    logic: 'MACD（指数平滑异同平均线）通过计算快速线与慢速线的差值，判断价格趋势的强度和方向。',
    buyConditions: [
      'DIFF线上穿DEA线（金叉）',
      'MACD柱状线在零轴上方翻红',
      '零轴上方的金叉信号更强'
    ],
    sellConditions: [
      'DIFF线下穿DEA线（死叉）',
      'MACD柱状线在零轴下方翻绿'
    ],
    risk: 'MACD是滞后指标，在快速行情中可能错过最佳买卖点。'
  },
  kdj: {
    name: 'KDJ策略',
    logic: 'KDJ随机指标通过比较收盘价与一定周期内价格范围的关系，判断超买超卖状态。',
    buyConditions: [
      'K线上穿D线（金叉）',
      'J值小于80（非超买区）',
      'J值从超卖区（<20）回升时信号更强'
    ],
    sellConditions: [
      'K线下穿D线（死叉）',
      'J值大于100（严重超买）'
    ],
    risk: 'KDJ在单边行情中容易过早发出反向信号，需结合趋势判断。'
  },
  boll: {
    name: '布林带策略',
    logic: '布林带由上轨、中轨、下轨组成，价格通常在通道内运行，触及上下轨可能产生反弹或回调。',
    buyConditions: [
      '股价触及或跌破下轨后反弹',
      '股价突破中轨向上',
      '通道收窄后向上突破'
    ],
    sellConditions: [
      '股价触及或突破上轨后回落',
      '股价跌破中轨向下',
      '通道收窄后向下突破'
    ],
    risk: '强势行情中价格可能持续沿上轨或下轨运行，产生误判。'
  },
  rsi: {
    name: 'RSI策略',
    logic: 'RSI相对强弱指标通过比较一段时期内价格上涨和下跌的幅度，判断超买超卖状态。',
    buyConditions: [
      'RSI6值小于20（超卖区）',
      'RSI从超卖区回升上穿20'
    ],
    sellConditions: [
      'RSI6值大于80（超买区）',
      'RSI从超买区回落下穿80'
    ],
    risk: 'RSI在趋势行情中可能在超买超卖区长期运行，产生过早信号。'
  },
  combined: {
    name: '综合策略',
    logic: '综合多个技术指标，当3个及以上指标同时发出买入或卖出信号时才产生交易信号，提高信号可靠性。',
    buyConditions: [
      '3个及以上指标发出买入信号（强烈买入）',
      '2个指标发出买入信号（弱买入）'
    ],
    sellConditions: [
      '3个及以上指标发出卖出信号（强烈卖出）',
      '2个指标发出卖出信号（弱卖出）'
    ],
    risk: '信号出现频率较低，可能错过部分机会，但胜率相对较高。'
  }
}

const currentStrategy = computed(() => strategies[activeStrategy.value])

const handleStrategySelect = (index) => {
  activeStrategy.value = index
  backtestResult.value = null
}

const runQuickBacktest = async () => {
  loading.value = true
  try {
    const res = await backtestApi.runBacktest({
      code: backtestForm.value.code,
      strategy_type: activeStrategy.value,
      initial_capital: backtestForm.value.capital
    })
    backtestResult.value = res.data
  } catch (error) {
    console.error('Backtest failed:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.strategy {
  padding: 10px;
}

.strategy-list, .strategy-detail, .quick-backtest {
  margin-bottom: 20px;
}

.strategy-item {
  padding: 5px 0;
}

.strategy-name {
  font-weight: bold;
  color: #fff;
}

.strategy-desc {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.strategy-menu {
  background: transparent;
  border-right: none;
}

.strategy-info h3 {
  color: #00d4aa;
  margin: 20px 0 10px 0;
}

.strategy-info h3:first-child {
  margin-top: 0;
}

.strategy-info p {
  color: #ccc;
  line-height: 1.8;
}

.strategy-info ul {
  color: #ccc;
  padding-left: 20px;
}

.strategy-info li {
  margin: 8px 0;
}

.backtest-result {
  margin-top: 20px;
}

.result-item {
  text-align: center;
  padding: 15px;
  background: #0f0f1e;
  border-radius: 8px;
}

.result-label {
  color: #909399;
  margin-bottom: 8px;
}

.result-value {
  font-size: 24px;
  font-weight: bold;
  color: #fff;
}

.result-value.up {
  color: #f56c6c;
}

.result-value.down {
  color: #67c23a;
}
</style>
