// Stat Card component
'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowUpRight, ArrowDownRight, LucideIcon } from 'lucide-react';
import { cn, formatNumber, formatCurrency } from '@/app/lib/utils';

interface StatCardProps {
  title: string;
  value: number;
  valuePrefix?: string;
  valueSuffix?: string;
  change?: number;
  changeType?: 'up' | 'down' | 'neutral';
  icon: LucideIcon;
  subtitle?: string;
  format?: 'number' | 'currency' | 'percent';
  currency?: string;
  className?: string;
}

export function StatCard({
  title,
  value,
  valuePrefix = '',
  valueSuffix = '',
  change,
  changeType = 'up',
  icon: Icon,
  subtitle,
  format = 'number',
  currency = 'CNY',
  className,
}: StatCardProps) {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    const duration = 1000;
    const steps = 30;
    const stepValue = value / steps;
    const stepDuration = duration / steps;
    
    let current = 0;
    let step = 0;
    
    const timer = setInterval(() => {
      step++;
      current = Math.min(step * stepValue, value);
      setDisplayValue(Math.floor(current));
      
      if (step >= steps) {
        setDisplayValue(value);
        clearInterval(timer);
      }
    }, stepDuration);
    
    return () => clearInterval(timer);
  }, [value]);

  const formattedValue = format === 'currency' 
    ? formatCurrency(displayValue, currency)
    : format === 'percent'
    ? `${displayValue}%`
    : formatNumber(displayValue);

  return (
    <motion.div
      whileHover={{ y: -2 }}
      className={cn(
        "bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-all",
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div className="p-2 bg-blue-50 rounded-lg">
          <Icon className="w-5 h-5 text-blue-600" />
        </div>
        {change !== undefined && (
          <div
            className={cn(
              "flex items-center gap-0.5 text-xs font-medium px-2 py-1 rounded-full",
              changeType === 'up' && "bg-green-50 text-green-600",
              changeType === 'down' && "bg-red-50 text-red-600",
              changeType === 'neutral' && "bg-gray-50 text-gray-600"
            )}
          >
            {changeType === 'up' ? (
              <ArrowUpRight className="w-3 h-3" />
            ) : changeType === 'down' ? (
              <ArrowDownRight className="w-3 h-3" />
            ) : null}
            {change > 0 ? '+' : ''}{change}%
          </div>
        )}
      </div>
      
      <div className="mt-3">
        <p className="text-gray-500 text-xs">{title}</p>
        <p className="text-xl font-bold text-gray-900 mt-0.5">
          {valuePrefix}{formattedValue}{valueSuffix}
        </p>
        {subtitle && (
          <p className="text-gray-400 text-xs mt-1">{subtitle}</p>
        )}
      </div>
    </motion.div>
  );
}
