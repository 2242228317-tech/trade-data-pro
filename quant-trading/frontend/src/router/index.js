import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import StockDetail from '../views/StockDetail.vue'
import Strategy from '../views/Strategy.vue'
import Backtest from '../views/Backtest.vue'
import Watchlist from '../views/Watchlist.vue'
import Signals from '../views/Signals.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/stock/:code',
    name: 'StockDetail',
    component: StockDetail,
    props: true
  },
  {
    path: '/strategy',
    name: 'Strategy',
    component: Strategy
  },
  {
    path: '/backtest',
    name: 'Backtest',
    component: Backtest
  },
  {
    path: '/watchlist',
    name: 'Watchlist',
    component: Watchlist
  },
  {
    path: '/signals',
    name: 'Signals',
    component: Signals
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
