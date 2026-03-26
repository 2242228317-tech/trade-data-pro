'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface CompareContextType {
  compareList: string[];
  addToCompare: (id: string) => boolean;
  removeFromCompare: (id: string) => void;
  clearCompare: () => void;
  isInCompare: (id: string) => boolean;
  canAddMore: () => boolean;
  maxItems: number;
}

const CompareContext = createContext<CompareContextType | undefined>(undefined);

const MAX_COMPARE_ITEMS = 5; // 免费版限制，专业版可更多

export function CompareProvider({ children }: { children: ReactNode }) {
  const [compareList, setCompareList] = useState<string[]>([]);

  // 从localStorage加载
  useEffect(() => {
    const saved = localStorage.getItem('trade_data_compare');
    if (saved) {
      setCompareList(JSON.parse(saved));
    }
  }, []);

  // 保存到localStorage
  useEffect(() => {
    localStorage.setItem('trade_data_compare', JSON.stringify(compareList));
  }, [compareList]);

  const addToCompare = (id: string): boolean => {
    if (compareList.includes(id)) return true;
    if (compareList.length >= MAX_COMPARE_ITEMS) return false;
    
    setCompareList(prev => [...prev, id]);
    return true;
  };

  const removeFromCompare = (id: string) => {
    setCompareList(prev => prev.filter(item => item !== id));
  };

  const clearCompare = () => {
    setCompareList([]);
  };

  const isInCompare = (id: string) => {
    return compareList.includes(id);
  };

  const canAddMore = () => {
    return compareList.length < MAX_COMPARE_ITEMS;
  };

  return (
    <CompareContext.Provider value={{
      compareList,
      addToCompare,
      removeFromCompare,
      clearCompare,
      isInCompare,
      canAddMore,
      maxItems: MAX_COMPARE_ITEMS
    }}>
      {children}
    </CompareContext.Provider>
  );
}

export function useCompare() {
  const context = useContext(CompareContext);
  if (context === undefined) {
    throw new Error('useCompare must be used within a CompareProvider');
  }
  return context;
}
