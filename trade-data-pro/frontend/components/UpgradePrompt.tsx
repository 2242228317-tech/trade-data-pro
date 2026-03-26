'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
  Lock, X, Crown, ArrowRight, Zap, Shield
} from 'lucide-react';

interface UpgradePromptProps {
  feature: string;
  description: string;
  requiredPlan: 'basic' | 'pro' | 'enterprise';
  currentPlan?: string;
  onClose?: () => void;
}

const PLAN_INFO = {
  basic: { name: '基础版', price: 29, icon: Shield, color: 'blue' },
  pro: { name: '专业版', price: 99, icon: Crown, color: 'purple' },
  enterprise: { name: '企业版', price: 299, icon: Zap, color: 'orange' }
};

// 小型升级提示（用于功能受限时的内联提示）
export function UpgradeBadge({ requiredPlan }: { requiredPlan: 'basic' | 'pro' | 'enterprise' }) {
  const info = PLAN_INFO[requiredPlan];
  
  return (
    <Link 
      href="/pricing"
      className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs font-medium hover:shadow-md transition-shadow"
    >
      <Crown className="w-3 h-3" />
      {info.name}
    </Link>
  );
}

// 中等升级卡片（用于页面内的功能限制提示）
export function UpgradeCard({ 
  feature, 
  description, 
  requiredPlan,
  currentPlan = 'free'
}: UpgradePromptProps) {
  const info = PLAN_INFO[requiredPlan];
  const Icon = info.icon;
  
  return (
    <div className="bg-gradient-to-br from-gray-50 to-gray-100 border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center">
      <div className={`w-16 h-16 bg-${info.color}-100 rounded-full mx-auto mb-4 flex items-center justify-center`}>
        <Lock className={`w-8 h-8 text-${info.color}-600`} />
      </div>
      
      <h3 className="text-lg font-bold text-gray-900 mb-2">
        {feature} 需要 {info.name}
      </h3>
      
      <p className="text-gray-500 mb-6 max-w-sm mx-auto">
        {description}
      </p>
      
      <div className="flex items-center justify-center gap-4">
        <Link
          href="/pricing"
          className={`inline-flex items-center gap-2 px-6 py-3 bg-${info.color}-600 text-white rounded-xl font-medium hover:bg-${info.color}-700 transition-colors`}
        >
          升级到 {info.name}
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
      
      <p className="text-sm text-gray-400 mt-4">
        仅需 ¥{info.price}/月，随时可取消
      </p>
    </div>
  );
}

// 全屏升级弹窗（用于操作时的拦截提示）
export function UpgradeModal({ 
  feature, 
  description, 
  requiredPlan,
  currentPlan = 'free',
  onClose 
}: UpgradePromptProps & { onClose: () => void }) {
  const info = PLAN_INFO[requiredPlan];
  const Icon = info.icon;
  
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-md w-full p-8 relative animate-in fade-in zoom-in duration-200">
        {onClose && (
          <button 
            onClick={onClose}
            className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        )}
        
        <div className="text-center">
          <div className={`w-20 h-20 bg-gradient-to-br from-${info.color}-100 to-${info.color}-200 rounded-full mx-auto mb-6 flex items-center justify-center`}>
            <Icon className={`w-10 h-10 text-${info.color}-600`} />
          </div>
          
          <h3 className="text-2xl font-bold text-gray-900 mb-2">
            解锁 {feature}
          </h3>
          
          <p className="text-gray-500 mb-6">
            {description}
          </p>
          
          {/* 当前 vs 目标方案对比 */}
          <div className="bg-gray-50 rounded-xl p-4 mb-6 text-left">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm text-gray-500">当前方案</span>
              <span className="text-sm font-medium text-gray-900">免费版</span>
            </div>
            <div className="w-full h-px bg-gray-200 mb-3" />
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-500">升级后</span>
              <span className={`text-sm font-bold text-${info.color}-600`}>{info.name}</span>
            </div>
          </div>
          
          <div className="flex gap-3">
            <button
              onClick={onClose}
              className="flex-1 py-3 px-4 border border-gray-200 text-gray-700 rounded-xl font-medium hover:bg-gray-50 transition-colors"
            >
              稍后再说
            </button>
            <Link
              href="/pricing"
              className={`flex-1 py-3 px-4 bg-${info.color}-600 text-white rounded-xl font-medium hover:bg-${info.color}-700 transition-colors inline-flex items-center justify-center gap-2`}
            >
              立即升级
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

// 查询配额提示（用于显示剩余次数）
export function QuotaIndicator({ 
  used, 
  limit, 
  resetAt 
}: { 
  used: number; 
  limit: number; 
  resetAt?: string;
}) {
  const percentage = (used / limit) * 100;
  const isLow = percentage >= 80;
  const isExhausted = used >= limit;
  
  return (
    <div className="flex items-center gap-3 text-sm">
      <div className="flex items-center gap-2">
        <span className="text-gray-500">今日查询</span>
        <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
          <div 
            className={`h-full rounded-full transition-all ${
              isExhausted ? 'bg-red-500' : isLow ? 'bg-orange-500' : 'bg-green-500'
            }`}
            style={{ width: `${Math.min(percentage, 100)}%` }}
          />
        </div>
        <span className={`font-medium ${isExhausted ? 'text-red-600' : isLow ? 'text-orange-600' : 'text-gray-700'}`}>
          {used}/{limit}
        </span>
      </div>
      
      {isExhausted ? (
        <Link 
          href="/pricing"
          className="text-blue-600 hover:text-blue-700 font-medium"
        >
          升级获取更多
        </Link>
      ) : isLow ? (
        <Link 
          href="/pricing"
          className="text-blue-600 hover:text-blue-700 text-xs"
        >
          即将用完
        </Link>
      ) : null}
    </div>
  );
}

// 导出按钮（带权限检查）
export function ExportButton({ 
  onClick, 
  hasPermission = false,
  requiredPlan = 'basic' as const
}: { 
  onClick?: () => void; 
  hasPermission?: boolean;
  requiredPlan?: 'basic' | 'pro' | 'enterprise';
}) {
  const [showModal, setShowModal] = useState(false);
  
  if (hasPermission) {
    return (
      <button
        onClick={onClick}
        className="inline-flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        导出数据
      </button>
    );
  }
  
  return (
    <>
      <button
        onClick={() => setShowModal(true)}
        className="inline-flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-500 rounded-lg font-medium hover:bg-gray-200 transition-colors group"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
        导出数据
        <span className="ml-1 px-1.5 py-0.5 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs rounded">
          PRO
        </span>
      </button>
      
      {showModal && (
        <UpgradeModal
          feature="数据导出"
          description="导出功能允许您将查询结果保存为 Excel 或 CSV 格式，方便离线分析和报告制作。"
          requiredPlan={requiredPlan}
          onClose={() => setShowModal(false)}
        />
      )}
    </>
  );
}

// API 访问提示
export function ApiAccessCard() {
  return (
    <div className="bg-gradient-to-br from-purple-600 to-pink-600 rounded-2xl p-6 text-white">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-bold mb-1">需要 API 访问？</h3>
          <p className="text-purple-100 text-sm">
            将我们的数据集成到您的系统中
          </p>
        </div>
        <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
        </div>
      </div>
      
      <ul className="space-y-2 mb-6 text-sm">
        <li className="flex items-center gap-2">
          <svg className="w-4 h-4 text-green-300" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          RESTful API 接口
        </li>
        <li className="flex items-center gap-2">
          <svg className="w-4 h-4 text-green-300" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          每日 10,000 次调用
        </li>
        <li className="flex items-center gap-2">
          <svg className="w-4 h-4 text-green-300" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          详细文档支持
        </li>
      </ul>
      
      <Link
        href="/pricing"
        className="block w-full py-3 bg-white text-purple-600 rounded-xl font-medium text-center hover:bg-purple-50 transition-colors"
      >
        查看专业版方案
      </Link>
    </div>
  );
}
