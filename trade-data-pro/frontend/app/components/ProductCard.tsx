// Product Card component
'use client';

import Link from 'next/link';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { Heart, TrendingUp, TrendingDown, Minus, MapPin, Star, Package } from 'lucide-react';
import { Product } from '@/app/types';
import { cn, formatCurrency, formatNumber, getTrendColor, getTrendBgColor } from '@/app/lib/utils';

interface ProductCardProps {
  product: Product;
  className?: string;
  onCompare?: (product: Product) => void;
  isCompared?: boolean;
  showActions?: boolean;
}

export function ProductCard({
  product,
  className,
  onCompare,
  isCompared,
  showActions = true,
}: ProductCardProps) {
  const TrendIcon = product.trend === 'up' ? TrendingUp : product.trend === 'down' ? TrendingDown : Minus;
  
  return (
    <motion.div
      whileHover={{ y: -4 }}
      className={cn(
        "bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-lg transition-all",
        className
      )}
    >
      <Link href={`/products/${product.id}`}>
        <div className="relative aspect-square bg-gray-100">
          <div className="absolute inset-0 flex items-center justify-center text-gray-400">
            <Package className="w-12 h-12" />
          </div>
          
          {product.trend === 'up' && product.trendValue > 20 && (
            <div className="absolute top-2 left-2 px-2 py-1 bg-red-500 text-white text-xs font-bold rounded">
              热销
            </div>
          )}
          
          {product.supplier.verified && (
            <div className="absolute top-2 right-2 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
              <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            </div>
          )}
        </div>
      </Link>
      
      <div className="p-4">
        <Link href={`/products/${product.id}`}>
          <h3 className="font-medium text-gray-900 line-clamp-2 hover:text-blue-600 transition-colors">
            {product.name}
          </h3>
        </Link>
        
        <div className="flex items-center gap-1 mt-2">
          <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
          <span className="text-sm font-medium">{product.rating}</span>
          <span className="text-sm text-gray-400">({formatNumber(product.reviewCount)}评价)</span>
        </div>
        
        <div className="flex items-baseline gap-2 mt-2">
          <span className="text-lg font-bold text-red-600">
            {formatCurrency(product.price.min, product.price.currency)}
          </span>
          <span className="text-sm text-gray-400">
            - {formatCurrency(product.price.max, product.price.currency)}
          </span>
        </div>
        
        <div className="flex items-center gap-2 mt-2 text-sm text-gray-500">
          <span className="px-2 py-0.5 bg-gray-100 rounded">MOQ: {product.moq}件</span>
          <span className="flex items-center gap-1">
            <MapPin className="w-3 h-3" />
            {product.region}
          </span>
        </div>
        
        <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
          <div className="flex items-center gap-1">
            <div className={cn("px-2 py-0.5 rounded flex items-center gap-1 text-xs", getTrendBgColor(product.trend))}>
              <TrendIcon className={cn("w-3 h-3", getTrendColor(product.trend))} />
              <span className={getTrendColor(product.trend)}>
                {product.trendValue > 0 ? '+' : ''}{product.trendValue}%
              </span>
            </div>
          </div>
          
          {showActions && (
            <div className="flex items-center gap-2">
              <button
                onClick={() => onCompare?.(product)}
                className={cn(
                  "px-2 py-1 text-xs font-medium rounded transition-colors",
                  isCompared
                    ? "bg-blue-100 text-blue-600"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                )}
              >
                {isCompared ? '已对比' : '对比'}
              </button>
              
              <button className="p-1.5 text-gray-400 hover:text-red-500 transition-colors">
                <Heart className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
