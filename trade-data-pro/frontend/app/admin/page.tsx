'use client';

import { useState } from 'react';
import { CheckCircle, XCircle, Clock, DollarSign, Users, RefreshCw, AlertCircle } from 'lucide-react';

const MOCK_ORDERS = [
  { order_id: "TD20250322A1B2C3", amount: 99, plan_name: "专业版", duration_months: 1, payment_method: "manual_alipay", user: { email: "user1@example.com" }, note: "TradeData-TD20250322A1B2C3" },
  { order_id: "TD20250322D4E5F6", amount: 29, plan_name: "基础版", duration_months: 3, payment_method: "manual_wechat", user: { email: "user2@example.com" }, note: "TradeData-TD20250322D4E5F6" }
];

const MOCK_STATS = { total_users: 15, total_payments: 8, pending_payments: 2, total_revenue: 586 };

export default function AdminPage() {
  const [adminKey, setAdminKey] = useState('');
  const [isAuth, setIsAuth] = useState(false);
  const [orders, setOrders] = useState(MOCK_ORDERS);
  const [stats] = useState(MOCK_STATS);

  const login = () => {
    if (adminKey === 'trade888') setIsAuth(true);
    else alert('密码错误');
  };

  const confirm = (orderId: string, ok: boolean) => {
    if (ok) {
      setOrders(orders.filter(o => o.order_id !== orderId));
      alert('已确认收款，会员已开通');
    } else {
      setOrders(orders.filter(o => o.order_id !== orderId));
      alert('已拒绝订单');
    }
  };

  if (!isAuth) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md text-center">
          <div className="w-16 h-16 bg-blue-600 rounded-xl mx-auto mb-4 flex items-center justify-center">
            <DollarSign className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">管理后台</h1>
          <p className="text-gray-500 mt-2 mb-6">请输入密码</p>
          <input type="password" value={adminKey} onChange={(e) => setAdminKey(e.target.value)} placeholder="输入密码" className="w-full px-4 py-3 border border-gray-200 rounded-xl mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button onClick={login} className="w-full py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700">登录</button>
          <p className="text-gray-400 text-sm mt-4">密码: trade888</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <DollarSign className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">TradeData 管理后台</span>
          </div>
          <button onClick={() => setIsAuth(false)} className="text-gray-500">退出</button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatCard title="总用户数" value={stats.total_users} icon={Users} color="blue" />
          <StatCard title="总订单数" value={stats.total_payments} icon={CheckCircle} color="green" />
          <div className="bg-white rounded-xl p-6 shadow-sm border-2 border-amber-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-amber-600 text-sm">待确认订单</p>
                <p className="text-2xl font-bold text-amber-700">{stats.pending_payments}</p>
              </div>
              <div className="w-12 h-12 bg-amber-100 rounded-lg flex items-center justify-center">
                <Clock className="w-6 h-6 text-amber-600" />
              </div>
            </div>
          </div>
          <StatCard title="总收入" value={`¥${stats.total_revenue}`} icon={DollarSign} color="purple" />
        </div>

        <div className="bg-white rounded-xl shadow-sm">
          <div className="p-6 border-b border-gray-200 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-amber-600" />
              <h2 className="text-lg font-bold text-gray-900">待确认订单</h2>
              <span className="px-2 py-1 bg-amber-100 text-amber-700 rounded-full text-sm">{orders.length}</span>
            </div>
            <button className="flex items-center gap-2 text-gray-500"><RefreshCw className="w-4 h-4" />刷新</button>
          </div>

          <div className="divide-y divide-gray-100">
            {orders.length === 0 ? (
              <div className="p-12 text-center">
                <CheckCircle className="w-12 h-12 text-gray-300 mx-auto mb-2" />
                <p className="text-gray-500">暂无待确认订单</p>
              </div>
            ) : (
              orders.map((order) => (
                <div key={order.order_id} className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="font-mono text-sm bg-gray-100 px-2 py-1 rounded">{order.order_id}</span>
                        <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded-full text-xs">{order.plan_name}</span>
                        <span className="text-gray-400 text-sm">{order.duration_months}个月</span>
                      </div>
                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div><p className="text-gray-500">用户邮箱</p><p className="font-medium">{order.user.email}</p></div>
                        <div><p className="text-gray-500">支付方式</p><p className="font-medium">{order.payment_method.includes('alipay') ? '支付宝' : '微信'}</p></div>
                        <div><p className="text-gray-500">付款备注</p><p className="font-mono text-amber-700 bg-amber-50 px-2 py-1 rounded inline-block">{order.note}</p></div>
                      </div>
                    </div>
                    <div className="text-right ml-6">
                      <p className="text-2xl font-bold text-gray-900 mb-2">¥{order.amount}</p>
                      <div className="flex gap-2">
                        <button onClick={() => confirm(order.order_id, false)} className="px-4 py-2 border border-red-200 text-red-600 rounded-lg hover:bg-red-50 flex items-center gap-1">
                          <XCircle className="w-4 h-4" />拒绝
                        </button>
                        <button onClick={() => confirm(order.order_id, true)} className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-1">
                          <CheckCircle className="w-4 h-4" />确认收款
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="mt-8 bg-blue-50 rounded-xl p-6">
          <h3 className="font-bold text-blue-900 mb-3">操作说明</h3>
          <ul className="space-y-1 text-blue-800 text-sm">
            <li>1. 在支付宝/微信中查看是否有对应金额和备注的收款</li>
            <li>2. 核对金额和备注是否匹配（TradeData-订单号）</li>
            <li>3. 确认无误后点击「确认收款」，系统自动开通会员</li>
          </ul>
        </div>
      </main>
    </div>
  );
}

function StatCard({ title, value, icon: Icon, color }: { title: string; value: number | string; icon: any; color: string }) {
  const colors: Record<string, string> = { blue: 'bg-blue-100 text-blue-600', green: 'bg-green-100 text-green-600', purple: 'bg-purple-100 text-purple-600' };
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${colors[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
}
