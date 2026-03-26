// Loading spinner component
'use client';

import { cn } from '@/app/lib/utils';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function LoadingSpinner({ size = 'md', className }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4',
  };

  return (
    <div
      className={cn(
        "inline-block rounded-full border-blue-600 border-t-transparent animate-spin",
        sizeClasses[size],
        className
      )}
    />
  );
}

// Skeleton loading component
interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={cn(
        "animate-pulse bg-gray-200 rounded",
        className
      )}
    />
  );
}

// Loading overlay component
interface LoadingOverlayProps {
  children: React.ReactNode;
  loading: boolean;
  className?: string;
}

export function LoadingOverlay({ children, loading, className }: LoadingOverlayProps) {
  return (
    <div className={cn("relative", className)}>
      {children}
      {loading && (
        <div className="absolute inset-0 bg-white/80 flex items-center justify-center z-10">
          <LoadingSpinner size="lg" />
        </div>
      )}
    </div>
  );
}
