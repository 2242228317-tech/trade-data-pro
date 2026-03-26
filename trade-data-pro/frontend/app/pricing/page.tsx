'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { 
  Check, X, Zap, Crown, Building2, 
  Copy, CheckCircle, AlertCircle, Loader2
} from 'lucide-react';
import { apiRequest, MEMBERSHIP_PLANS, PAYMENT_CONFIG, API_URL } from '@/app/config';

// 颜色配置
const colorClasses: Record<string, { bg: string; border: string; button: string; buttonHover: string; text: string }> = {
  gray: { 
    bg: 'bg-gray-50', 
    border: 'border-gray-200', 
    button: 'bg-gray-900', 
    buttonHover: 'hover:bg-gray-800',
    text: 'text-gray-600'
  },
  blue: { 
    bg: 'bg-blue-50', 
    border: 'border-blue-200', 
    button: 'bg-blue-600', 
    buttonHover: 'hover:bg-blue-700',
    text: 'text-blue-600'
  },
  purple: { 
    bg: 'bg-purple-50', 
    border: 'border-purple-200', 
    button: 'bg-purple-600', 
    buttonHover: 'hover:bg-purple-700',
    text: 'text-purple-600'
  },
  orange: { 
    bg: 'bg-orange-50', 
    border: 'border-orange-200', 
    button: 'bg-orange-600', 
    buttonHover: 'hover:bg-orange-700',
    text: 'text-orange-600'
  },
};

// 图标映射
const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  Zap,
  Crown,
  Building2,
};

function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">TradeData Pro</span>
          </Link>
          
          <div className="flex items-center gap-4">
            <Link href="/" className="text-gray-600 hover:text-gray-900">首页</Link>
            <Link href="/login" className="text-gray-600 hover:text-gray-900">登录</Link>
            <Link href="/register" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              免费注册
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

function PlanCard({ plan, currentPlan, onSelect }: { 
  plan: typeof MEMBERSHIP_PLANS[0]; 
  currentPlan?: string; 
  onSelect: (plan: typeof MEMBERSHIP_PLANS[0]) => void;
}) {
  const isCurrent = currentPlan === plan.role;
  const Icon = iconMap[plan.icon] || Zap;
  const colors = colorClasses[plan.color] || colorClasses.gray;
  
  return (
    <div className={`relative bg-white rounded-2xl border-2 ${plan.popular ? 'border-purple-500 shadow-xl scale-105' : `border-gray-100 ${colors.border}`} p-8 transition-all hover:shadow-lg`}>
      {plan.popular && (
        <div className="absolute -top-4 left-1/2 -translate-x-1/2">
          <span className="bg-gradient-to-r from-purple-600 to-pink-600 text-white text-sm font-bold px-4 py-1 rounded-full">
            最受欢迎
          </span>
        </div>
      )}
      
      <div className={`w-14 h-14 ${colors.bg} rounded-xl flex items-center justify-center mb-6`}>
        <Icon className={`w-7 h-7 ${colors.text}`} />
      </div>
      
      <h3 className="text-xl font-bold text-gray-900">{plan.name}</h3>
      <p className="text-gray-500 text-sm mt-1">{plan.description}</p>
      
      <div className="mt-6 mb-8">
        <span className="text-4xl font-bold text-gray-900">¥{plan.price}</span>
        <span className="text-gray-500">{plan.period}</span>
      </div>
      
      <ul className="space-y-4 mb-8">
        {plan.features.map((f, i) => (
          <li key={i} className="flex items-start gap-3">
            {f.included ? (
              <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
            ) : (
              <X className="w-5 h-5 text-gray-300 flex-shrink-0 mt-0.5" />
            )}
            <span className={f.included ? 'text-gray-700' : 'text-gray-400'}>{f.text}</span>
          </li>
        ))}
      </ul>
      
      <button
        onClick={() => onSelect(plan)}
        disabled={isCurrent}
        className={`w-full py-3 px-4 rounded-xl font-medium transition-all ${
          isCurrent 
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
            : `${colors.button} text-white ${colors.buttonHover} shadow-lg hover:shadow-xl`
        }`}
      >
        {isCurrent ? '当前方案' : plan.price === 0 ? '免费使用' : '立即升级'}
      </button>
    </div>
  );
}

// 支付弹窗组件
function PaymentModal({ plan, onClose }: { plan: typeof MEMBERSHIP_PLANS[0]; onClose: () => void }) {
  const router = useRouter();
  const [step, setStep] = useState<'select' | 'pay' | 'done'>('select');
  const [method, setMethod] = useState<'alipay' | 'wechat'>('alipay');
  const [months, setMonths] = useState(1);
  const [orderId, setOrderId] = useState('');
  const [amount, setAmount] = useState(0);
  const [copied, setCopied] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const totalPrice = plan.price * months;
  const discount = months === 12 ? Math.round(totalPrice * 0.2) : 0;
  const finalPrice = totalPrice - discount;
  
  const createOrder = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      const data = await apiRequest('/manual/membership/payment/manual/create', {
        method: 'POST',
        body: JSON.stringify({
          plan: plan.role,
          duration_months: months,
          payment_method: method,
        }),
      });
      
      setOrderId(data.order_id);
      setAmount(data.amount);
      setStep('pay');
    } catch (err: any) {
      if (err.message.includes('请先登录') || err.message.includes('Unauthorized')) {
        router.push('/login?redirect=/pricing');
        return;
      }
      setError(err.message || '创建订单失败');
    } finally {
      setIsLoading(false);
    }
  };
  
  const copyNote = () => {
    navigator.clipboard.writeText(`TradeData-${orderId}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  
  if (step === 'select') {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-2xl max-w-md w-full p-6 relative max-h-[90vh] overflow-y-auto">
          <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600">
            <X className="w-6 h-6" />
          </button>
          
          <h3 className="text-xl font-bold text-gray-900 mb-2">升级到 {plan.name}</h3>
          <p className="text-gray-500 mb-6">选择订阅时长和支付方式</p>
          
          {/* 时长选择 */}
          <div className="mb-6">
            <label className="text-sm font-medium text-gray-700 mb-3 block">订阅时长</label>
            <div className="grid grid-cols-3 gap-3">
              {PAYMENT_CONFIG.durations.map((d) => (
                <button 
                  key={d.months} 
                  onClick={() => setMonths(d.months)} 
                  className={`py-3 px-4 rounded-xl border-2 text-center transition-all ${
                    months === d.months 
                      ? 'border-blue-500 bg-blue-50 text-blue-700' 
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="font-bold">{d.label}</div>
                  {d.discount > 0 && (
                    <div className="text-xs text-green-600 mt-1">省{d.discount * 100}%</div>
                  )}
                </button>
              ))}
            </div>
          </div>
          
          {/* 支付方式 */}
          <div className="mb-6">
            <label className="text-sm font-medium text-gray-700 mb-3 block">支付方式</label>
            <div className="grid grid-cols-2 gap-3">
              {PAYMENT_CONFIG.methods.map((m) => (
                <button 
                  key={m.id}
                  onClick={() => setMethod(m.id as 'alipay' | 'wechat')} 
                  className={`py-3 px-4 rounded-xl border-2 flex items-center justify-center gap-2 transition-all ${
                    method === m.id 
                      ? `border-[${m.color}] bg-opacity-10` 
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  style={method === m.id ? { borderColor: m.color, backgroundColor: `${m.color}10` } : {}}
                >
                  <span className="text-lg">{m.icon}</span>
                  <span className="font-medium">{m.name}</span>
                </button>
              ))}
            </div>
          </div>
          
          {/* 价格汇总 */}
          <div className="bg-gray-50 rounded-xl p-4 mb-6">
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-600">{plan.name} × {months}个月</span>
              <span className="font-medium">¥{totalPrice}</span>
            </div>
            {discount > 0 && (
              <div className="flex justify-between text-sm text-green-600 mb-2">
                <span>年度优惠</span>
                <span>-¥{discount}</span>
              </div>
            )}
            <div className="border-t border-gray-200 pt-2 flex justify-between">
              <span className="font-bold text-gray-900">应付总额</span>
              <span className="text-2xl font-bold text-blue-600">¥{finalPrice}</span>
            </div>
          </div>
          
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm">
              {error}
            </div>
          )}
          
          <button 
            onClick={createOrder} 
            disabled={isLoading}
            className="w-full py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                创建订单中...
              </>
            ) : (
              '确认支付'
            )}
          </button>
        </div>
      </div>
    );
  }
  
  if (step === 'pay') {
    const paymentMethod = PAYMENT_CONFIG.methods.find(m => m.id === method);
    
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-2xl max-w-md w-full p-6 relative max-h-[90vh] overflow-y-auto">
          <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600">
            <X className="w-6 h-6" />
          </button>
          
          <div className="text-center mb-6">
            <h3 className="text-xl font-bold text-gray-900">扫码支付</h3>
            <p className="text-gray-500 text-sm">订单号: <span className="font-mono">{orderId}</span></p>
          </div>
          
          {/* 收款码 */}
          <div className="bg-white border-2 border-dashed border-gray-300 rounded-xl p-6 text-center mb-6">
            <div className="w-48 h-48 bg-gray-100 rounded-lg mx-auto mb-4 flex items-center justify-center overflow-hidden">
              <img 
                src={method === 'alipay' ? '/images/alipay-qr.png' : '/images/wechat-qr.png'} 
                alt="收款码"
                className="w-full h-full object-contain"
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.style.display = 'none';
                  const parent = target.parentElement;
                  if (parent) {
                    parent.innerHTML = `
                      <div class="text-center p-4">
                        <div class="text-4xl mb-2">⚠️</div>
                        <div class="text-sm text-amber-700 font-medium">收款码未配置</div>
                        <div class="text-xs text-gray-500 mt-1">请联系管理员</div>
                      </div>
                    `;
                  }
                }}
              />
            </div>
            <div className="flex items-center justify-center gap-2">
              <div 
                className="w-2 h-2 rounded-full" 
                style={{ backgroundColor: paymentMethod?.color }}
              />
              <p className="text-sm text-gray-600 font-medium">
                {paymentMethod?.name}收款码
              </p>
            </div>
          </div>
          
          {/* 金额 */}
          <div className="bg-amber-50 rounded-xl p-4 mb-6 text-center">
            <p className="text-gray-600 text-sm mb-1">应付金额</p>
            <p className="text-3xl font-bold text-gray-900">¥{finalPrice}</p>
          </div>
          
          {/* 付款备注 */}
          <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
            <div className="flex items-start gap-2 mb-2">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-bold text-red-900">付款时必须添加备注！</p>
                <p className="text-red-700 text-sm">否则无法确认您的订单</p>
              </div>
            </div>
            
            <div className="flex items-center gap-2 bg-white rounded-lg p-3 mt-3">
              <code className="flex-1 font-mono text-lg text-red-800">TradeData-{orderId}</code>
              <button 
                onClick={copyNote} 
                className="flex items-center gap-1 px-3 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors"
              >
                {copied ? (
                  <><CheckCircle className="w-4 h-4" /><span className="text-sm">已复制</span></>
                ) : (
                  <><Copy className="w-4 h-4" /><span className="text-sm">复制</span></>
                )}
              </button>
            </div>
          </div>
          
          {/* 步骤说明 */}
          <div className="space-y-3 text-sm">
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 bg-green-600 text-white rounded-full flex items-center justify-center text-xs font-bold">1</div>
              <span className="text-gray-700">扫码付款 ¥{finalPrice}</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 bg-green-600 text-white rounded-full flex items-center justify-center text-xs font-bold">2</div>
              <span className="text-gray-700">添加备注：<code className="bg-gray-100 px-1 rounded">TradeData-{orderId}</code></span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 bg-amber-500 text-white rounded-full flex items-center justify-center text-xs font-bold">3</div>
              <span className="text-gray-700">等待管理员确认（24小时内）</span>
            </div>
          </div>
          
          {/* 联系 */}
          <div className="mt-6 pt-4 border-t border-gray-200">
            <p className="text-sm text-gray-500 text-center">
              付款后长时间未开通？请联系管理员微信并提供订单号
            </p>
          </div>
        </div>
      </div>
    );
  }
  
  return null;
}

export default function PricingPage() {
  const [currentPlan] = useState<string>('free');
  const [showPayment, setShowPayment] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<typeof MEMBERSHIP_PLANS[0] | null>(null);
  
  const handleSelect = (plan: typeof MEMBERSHIP_PLANS[0]) => {
    if (plan.price === 0) {
      window.location.href = '/';
      return;
    }
    setSelectedPlan(plan);
    setShowPayment(true);
  };
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="bg-gradient-to-b from-blue-600 to-blue-700 text-white py-20">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">选择适合您的方案</h1>
          <p className="text-xl text-blue-100 max-w-2xl mx-auto">
            从免费版开始，随时升级解锁更多专业数据功能
          </p>
        </div>
      </div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10 pb-20">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {MEMBERSHIP_PLANS.map((plan) => (
            <PlanCard 
              key={plan.role} 
              plan={plan} 
              currentPlan={currentPlan} 
              onSelect={handleSelect} 
            />
          ))}
        </div>
      </div>
      
      {showPayment && selectedPlan && (
        <PaymentModal 
          plan={selectedPlan} 
          onClose={() => setShowPayment(false)} 
        />
      )}
    </div>
  );
}
