<template>
  <div class="app">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="200px" class="sidebar">
        <div class="logo">
          <el-icon><TrendCharts /></el-icon>
          <span>量化交易系统</span>
        </div>
        <el-menu
          :default-active="$route.path"
          router
          class="nav-menu"
          background-color="#1a1a2e"
          text-color="#fff"
          active-text-color="#00d4aa"
        >
          <el-menu-item index="/">
            <el-icon><Odometer /></el-icon>
            <span>行情大盘</span>
          </el-menu-item>
          <el-menu-item index="/signals">
            <el-icon><Bell /></el-icon>
            <span>交易信号</span>
          </el-menu-item>
          <el-menu-item index="/strategy">
            <el-icon><Cpu /></el-icon>
            <span>策略中心</span>
          </el-menu-item>
          <el-menu-item index="/backtest">
            <el-icon><TrendCharts /></el-icon>
            <span>策略回测</span>
          </el-menu-item>
          <el-menu-item index="/watchlist">
            <el-icon><Star /></el-icon>
            <span>自选股</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-container>
        <el-header class="header">
          <div class="header-left">
            <h2>{{ $route.name }}</h2>
          </div>
          <div class="header-right">
            <el-input
              v-model="searchCode"
              placeholder="输入股票代码"
              class="search-input"
              @keyup.enter="searchStock"
            >
              <template #append>
                <el-button @click="searchStock">
                  <el-icon><Search /></el-icon>
                </el-button>
              </template>
            </el-input>
          </div>
        </el-header>
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const searchCode = ref('')

const searchStock = () => {
  if (searchCode.value) {
    router.push(`/stock/${searchCode.value}`)
    searchCode.value = ''
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #0f0f1e;
  color: #fff;
}

.app {
  height: 100vh;
}

.sidebar {
  background: #1a1a2e;
  border-right: 1px solid #2a2a3e;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 18px;
  font-weight: bold;
  color: #00d4aa;
  border-bottom: 1px solid #2a2a3e;
}

.logo .el-icon {
  font-size: 24px;
}

.nav-menu {
  border-right: none;
}

.header {
  background: #1a1a2e;
  border-bottom: 1px solid #2a2a3e;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header h2 {
  color: #fff;
  font-size: 20px;
}

.search-input {
  width: 250px;
}

.main-content {
  background: #0f0f1e;
  padding: 20px;
  overflow-y: auto;
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #1a1a2e;
}

::-webkit-scrollbar-thumb {
  background: #3a3a4e;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #4a4a5e;
}

/* Element Plus 深色主题覆盖 */
.el-card {
  background: #1a1a2e;
  border: 1px solid #2a2a3e;
  color: #fff;
}

.el-table {
  background: transparent;
}

.el-table th,
.el-table tr {
  background: #1a1a2e;
  color: #fff;
}

.el-table td {
  border-bottom: 1px solid #2a2a3e;
}

.el-table--enable-row-hover .el-table__body tr:hover > td {
  background: #2a2a3e;
}

.el-input__wrapper {
  background: #2a2a3e;
  box-shadow: 0 0 0 1px #3a3a4e inset;
}

.el-input__inner {
  color: #fff;
}
</style>
