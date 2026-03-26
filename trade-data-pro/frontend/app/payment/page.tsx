'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
  ArrowLeft, Copy, CheckCircle, Clock, AlertCircle,
  MessageCircle, RefreshCw
} from 'lucide-react';

interface PaymentPageProps {
  searchParams: { order?: string };
}

// 模拟数据 - 实际应该从API获取
const MOCK_ORDER = {
  order_id: "TD20250322A1B2C3",
  amount: 99,
  plan_name: "专业版",
  duration_months: 1,
  payment_method: "alipay",
  qr_code_url: "https://via.placeholder.com/300x300?text=Alipay+QR",
  account: "138****8888",
  note: "TradeData-TD20250322A1B2C3",
  status: "pending",
  expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
};

export default function PaymentPage({ searchParams }: PaymentPageProps) {
  const [copied, setCopied] = useState(false);
  const [checking, setChecking] = useState(false);
  const [status, setStatus] = useState(MOCK_ORDER.status);

  const copyNote = () => {
    navigator.clipboard.writeText(MOCK_ORDER.note);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const checkStatus = () => {
    setChecking(true);
    // 模拟查询
    setTimeout(() => {
      setChecking(false);
      // 实际应该调用API查询状态
    }, 1500);
  };

  const formatTime = (isoString: string) => {
    const date = new Date(isoString);
    return date.toLocaleString('zh-CN', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 顶部导航 */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-2xl mx-auto px-4 py-4">
          <Link 
            href="/pricing" 
            className="inline-flex items-center text-gray-600 hover:text-gray-900"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            返回定价
          </Link>
        </div>
      </div>

      <div className="max-w-2xl mx-auto px-4 py-8">
        {/* 订单信息卡片 */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-xl font-bold text-gray-900">订单支付</h1>
            <span className="px-3 py-1 bg-yellow-100 text-yellow-700 rounded-full text-sm font-medium">
              等待付款
            </span>
          </div>

          <div className="bg-gray-50 rounded-xl p-4 mb-6">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-500">订单编号</span>
              <span className="font-mono text-sm">{MOCK_ORDER.order_id}</span>
            </div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-500">套餐</span>
              <span className="font-medium">{MOCK_ORDER.plan_name} × {MOCK_ORDER.duration_months}个月</span>
            </div>
            <div className="flex justify-between items-center pt-2 border-t border-gray-200">
              <span className="text-gray-900 font-medium">应付金额</span>
              <span className="text-3xl font-bold text-blue-600">¥{MOCK_ORDER.amount}</span>
            </div>
          </div>

          {/* 支付步骤 */}
          <div className="space-y-6">
            {/* 步骤1：扫码支付 */}
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                1
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-gray-900 mb-2">扫码支付</h3>
                <p className="text-gray-500 text-sm mb-4">
                  使用{MOCK_ORDER.payment_method === 'alipay' ? '支付宝' : '微信'}扫描二维码付款
                </p>

                {/* 收款码 */}
                <div className="bg-white border-2 border-dashed border-gray-300 rounded-xl p-8 text-center max-w-xs mx-auto">
                  <div className="w-48 h-48 bg-gray-100 rounded-lg mx-auto mb-4 flex items-center justify-center">
                    {/* 这里放你的真实收款码 */}
                    <div className="text-center">
                      <div className="text-4xl mb-2">📱</div>
                      <div className="text-xs text-gray-400">收款码位置</div>
                      <div className="text-xs text-gray-400 mt-1">请替换为真实二维码</div>
                    </div>
                  </div>
                  <p className="text-sm text-gray-500">收款账号：{MOCK_ORDER.account}</p>
                </div>

                {/* 或者转账方式 */}
                <div className="mt-4 p-4 bg-blue-50 rounded-xl">
                  <p className="text-sm text-blue-700 mb-2">或者通过转账支付：</p>
                  <div className="flex items-center justify-between bg-white rounded-lg p-3">
                    <span className="font-mono text-sm">{MOCK_ORDER.account}</span>
                    <button className="text-blue-600 text-sm font-medium">
                      复制账号
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* 步骤2：备注订单号 */}
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                2
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-gray-900 mb-2">添加付款备注</h3>
                <p className="text-gray-500 text-sm mb-3">
                  付款时请务必添加以下备注，方便确认您的订单
                </p>

                <div className="flex items-center gap-2 bg-amber-50 border border-amber-200 rounded-xl p-4">
                  <code className="flex-1 font-mono text-lg text-amber-800">
                    {MOCK_ORDER.note}
                  </code>
                  <button
                    onClick={copyNote}
                    className="flex items-center gap-1 px-3 py-2 bg-white border border-amber-300 rounded-lg text-amber-700 hover:bg-amber-100 transition-colors"
                  >
                    {copied ? (
                      <>
                        <CheckCircle className="w-4 h-4" />
                        <span className="text-sm">已复制</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-4 h-4" />
                        <span className="text-sm">复制</span>
                      </>
                    )}
                  </button>
                </div>

                <div className="mt-3 flex items-start gap-2 text-amber-700 text-sm">
                  <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                  <p>忘记备注可能导致无法自动开通，需要联系客服手动处理</p>
                </div>
              </div>
            </div>

            {/* 步骤3：等待确认 */}
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-gray-200 text-gray-600 rounded-full flex items-center justify-center font-bold">
                3
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-gray-900 mb-2">等待确认</h3>
                <p className="text-gray-500 text-sm mb-4">
                  付款完成后，我们会在24小时内确认并开通会员
                </p>

                <div className="bg-gray-100 rounded-xl p-4 text-center">
                  <Clock className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-gray-600 text-sm">订单有效期至</p>
                  <p className="text-gray-900 font-medium">{formatTime(MOCK_ORDER.expires_at)}</p>
                </div>

                {/* 刷新状态按钮 */}
                <button
                  onClick={checkStatus}
                  disabled={checking}
                  className="w-full mt-4 py-3 bg-white border border-gray-200 rounded-xl font-medium text-gray-700 hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
                >
                  <RefreshCw className={`w-4 h-4 ${checking ? 'animate-spin' : ''}`} />
                  {checking ? '查询中...' : '刷新支付状态'}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* 联系客服 */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-start gap-4">
            <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
              <MessageCircle className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <h3 className="font-bold text-gray-900 mb-1">遇到问题？</h3>
              <p className="text-gray-500 text-sm mb-3">
                付款后如果长时间未开通，请通过微信联系管理员
              </p>
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">管理员微信：</span>
                <code className="bg-gray-100 px-2 py-1 rounded text-sm">your-wechat-id</code>
                <span className="text-gray-400">|</span>
                <span className="text-sm text-gray-600">备注订单号：</span>
                <code className="bg-gray-100 px-2 py-1 rounded text-sm font-mono">{MOCK_ORDER.order_id}</code>
              </div>
            </div>
          </div>
        </div>

        {/* 提示 */}
        <p className="text-center text-gray-400 text-sm mt-6">
          此订单为手动确认支付，仅限内部测试使用
        </p>
      </div>
    </div>
  );
}
