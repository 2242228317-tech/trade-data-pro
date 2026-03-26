'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface FavoriteItem {
  id: string;
  name: string;
  price: { min: number; max: number };
  category: string;
  supplier: { name: string; location: string };
  addedAt: string;
}

interface SearchHistoryItem {
  keyword: string;
  filters: Record<string, any>;
  timestamp: string;
}

interface UserDataContextType {
  favorites: FavoriteItem[];
  searchHistory: SearchHistoryItem[];
  addFavorite: (product: any) => void;
  removeFavorite: (id: string) => void;
  isFavorite: (id: string) => boolean;
  addSearchHistory: (keyword: string, filters?: Record<string, any>) => void;
  clearSearchHistory: () => void;
}

const UserDataContext = createContext<UserDataContextType | undefined>(undefined);

export function UserDataProvider({ children }: { children: ReactNode }) {
  const [favorites, setFavorites] = useState<FavoriteItem[]>([]);
  const [searchHistory, setSearchHistory] = useState<SearchHistoryItem[]>([]);

  // 从localStorage加载
  useEffect(() => {
    const savedFavorites = localStorage.getItem('trade_data_favorites');
    const savedHistory = localStorage.getItem('trade_data_search_history');
    
    if (savedFavorites) setFavorites(JSON.parse(savedFavorites));
    if (savedHistory) setSearchHistory(JSON.parse(savedHistory));
  }, []);

  // 保存到localStorage
  useEffect(() => {
    localStorage.setItem('trade_data_favorites', JSON.stringify(favorites));
  }, [favorites]);

  useEffect(() => {
    localStorage.setItem('trade_data_search_history', JSON.stringify(searchHistory));
  }, [searchHistory]);

  const addFavorite = (product: any) => {
    if (favorites.some(f => f.id === product.id)) return;
    
    const newFavorite: FavoriteItem = {
      id: product.id,
      name: product.name,
      price: product.price,
      category: product.category,
      supplier: product.supplier,
      addedAt: new Date().toISOString()
    };
    
    setFavorites(prev => [newFavorite, ...prev]);
  };

  const removeFavorite = (id: string) => {
    setFavorites(prev => prev.filter(f => f.id !== id));
  };

  const isFavorite = (id: string) => {
    return favorites.some(f => f.id === id);
  };

  const addSearchHistory = (keyword: string, filters?: Record<string, any>) => {
    if (!keyword.trim()) return;
    
    const newItem: SearchHistoryItem = {
      keyword: keyword.trim(),
      filters: filters || {},
      timestamp: new Date().toISOString()
    };
    
    setSearchHistory(prev => {
      // 去重并保留最近20条
      const filtered = prev.filter(item => item.keyword !== keyword);
      return [newItem, ...filtered].slice(0, 20);
    });
  };

  const clearSearchHistory = () => {
    setSearchHistory([]);
  };

  return (
    <UserDataContext.Provider value={{
      favorites,
      searchHistory,
      addFavorite,
      removeFavorite,
      isFavorite,
      addSearchHistory,
      clearSearchHistory
    }}>
      {children}
    </UserDataContext.Provider>
  );
}

export function useUserData() {
  const context = useContext(UserDataContext);
  if (context === undefined) {
    throw new Error('useUserData must be used within a UserDataProvider');
  }
  return context;
}
