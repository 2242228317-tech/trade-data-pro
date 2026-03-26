// Local storage utilities for watchlist and favorites

import { WatchlistItem, Product } from '../types';

const WATCHLIST_KEY = 'tradepro_watchlist';

export const WatchlistStorage = {
  getAll(): WatchlistItem[] {
    if (typeof window === 'undefined') return [];
    const data = localStorage.getItem(WATCHLIST_KEY);
    return data ? JSON.parse(data) : [];
  },

  add(product: Product): WatchlistItem {
    const items = this.getAll();
    const existing = items.find(item => item.productId === product.id);
    
    if (existing) {
      return existing;
    }

    const newItem: WatchlistItem = {
      id: `watch-${Date.now()}`,
      productId: product.id,
      product,
      addedAt: new Date().toISOString(),
    };

    items.push(newItem);
    localStorage.setItem(WATCHLIST_KEY, JSON.stringify(items));
    return newItem;
  },

  remove(productId: string): void {
    const items = this.getAll().filter(item => item.productId !== productId);
    localStorage.setItem(WATCHLIST_KEY, JSON.stringify(items));
  },

  isInWatchlist(productId: string): boolean {
    return this.getAll().some(item => item.productId === productId);
  },

  update(productId: string, updates: Partial<Omit<WatchlistItem, 'id' | 'productId' | 'product'>>): void {
    const items = this.getAll();
    const index = items.findIndex(item => item.productId === productId);
    
    if (index !== -1) {
      items[index] = { ...items[index], ...updates };
      localStorage.setItem(WATCHLIST_KEY, JSON.stringify(items));
    }
  },

  clear(): void {
    localStorage.removeItem(WATCHLIST_KEY);
  },
};

// Export comparison utility
export const ComparisonStorage = {
  getAll(): string[] {
    if (typeof window === 'undefined') return [];
    const data = localStorage.getItem('tradepro_compare');
    return data ? JSON.parse(data) : [];
  },

  add(productId: string): void {
    const items = this.getAll();
    if (!items.includes(productId) && items.length < 4) {
      items.push(productId);
      localStorage.setItem('tradepro_compare', JSON.stringify(items));
    }
  },

  remove(productId: string): void {
    const items = this.getAll().filter(id => id !== productId);
    localStorage.setItem('tradepro_compare', JSON.stringify(items));
  },

  clear(): void {
    localStorage.removeItem('tradepro_compare');
  },

  isInComparison(productId: string): boolean {
    return this.getAll().includes(productId);
  },
};
