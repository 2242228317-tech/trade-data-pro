'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Crown, ArrowRight, X } from 'lucide-react';

// 会员浮动入口组件
export function MembershipFloatButton() {
  const [isExpanded, setIsExpanded] = useState(false);
  
  return (
    <div className="fixed bottom-6 right-6 z-40">
      {isExpanded ? (
        <div className="bg-white rounded-2xl shadow-2xl p-4 w-72 animate-in slide-in-from-bottom-2 fade-in">
          <div className="flex items-start justify-between mb-3">
            <div>
              <h4 className="font-bold text-gray-900">解锁更多功能</h4>
              <p className="text-sm text-gray-500">升级会员获取无限查询</p>
            </div>
            <button 
              onClick={() => setIsExpanded(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          
          <div className="space-y-2 mb-4">
            <div className="flex items-center gap-2 text-sm">
              <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
              <span className="text-gray-600">查看 5 年历史数据</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
              <span className="text-gray-600">Excel 数据导出</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
              <span className="text-gray-600">API 接口访问</span>
            </div>
          </div>
          
          <Link
            href="/pricing"
            className="block w-full py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-medium text-center hover:shadow-lg transition-all"
          >
            查看定价方案
          </Link>
        </div>
      ) : (
        <button
          onClick={() => setIsExpanded(true)}
          className="w-14 h-14 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full shadow-lg hover:shadow-xl flex items-center justify-center text-white transition-all hover:scale-105"
        >
          <Crown className="w-6 h-6" />
        </button>
      )}
    </div>
  );
}

// 导航栏会员入口
export function NavbarMembershipEntry() {
  return (
    <Link
      href="/pricing"
      className="hidden md:flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-amber-100 to-orange-100 text-amber-700 rounded-lg text-sm font-medium hover:from-amber-200 hover:to-orange-200 transition-colors"
    >
      <Crown className="w-4 h-4" />
      升级会员
    </Link>
  );
}

// 受限功能遮罩
export function PremiumOverlay({ 
  children, 
  requiredPlan = 'basic',
  feature 
}: { 
  children: React.ReactNode; 
  requiredPlan?: 'basic' | 'pro' | 'enterprise';
  feature: string;
}) {
  const planNames = {
    basic: '基础版',
    pro: '专业版', 
    enterprise: '企业版'
  };
  
  return (
    <div className="relative">
      <div className="blur-sm pointer-events-none select-none">
        {children}
      </div>
      
      <div className="absolute inset-0 flex items-center justify-center bg-white/80 backdrop-blur-sm rounded-xl">
        <div className="text-center p-6">
          <div className="w-12 h-12 bg-purple-100 rounded-full mx-auto mb-3 flex items-center justify-center">
            <Crown className="w-6 h-6 text-purple-600" />
          </div>
          <p className="text-gray-600 mb-4">
            {feature} 需要 {planNames[requiredPlan]} 会员
          </p>
          
          <Link
            href="/pricing"
            className="inline-flex items-center gap-1 text-purple-600 font-medium hover:gap-2 transition-all"
          >
            立即升级
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  );
}
