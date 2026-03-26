// API client for making requests to the backend

const API_BASE = '/api';

async function fetchWithErrorHandling(url: string, options?: RequestInit) {
  const response = await fetch(url, options);
  const data = await response.json();
  
  if (!response.ok || !data.success) {
    throw new Error(data.error || `HTTP error! status: ${response.status}`);
  }
  
  return data.data;
}

export const api = {
  // Products
  getProducts: (filters?: Record<string, any>) => {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, String(value));
        }
      });
    }
    return fetchWithErrorHandling(`${API_BASE}/products?${params}`);
  },
  
  getProduct: (id: string) => {
    return fetchWithErrorHandling(`${API_BASE}/products/${id}`);
  },
  
  getTrendingProducts: (limit?: number) => {
    const params = limit ? `?limit=${limit}` : '';
    return fetchWithErrorHandling(`${API_BASE}/products/trending${params}`);
  },
  
  getFilterOptions: () => {
    return fetchWithErrorHandling(`${API_BASE}/products/filters`);
  },
  
  // Customs
  getCustomsData: (filters?: Record<string, any>) => {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, String(value));
        }
      });
    }
    return fetchWithErrorHandling(`${API_BASE}/customs?${params}`);
  },
  
  // Analytics
  getAnalytics: (productId?: string) => {
    const params = productId ? `?productId=${productId}` : '';
    return fetchWithErrorHandling(`${API_BASE}/analytics${params}`);
  },
  
  // Dashboard
  getDashboard: () => {
    return fetchWithErrorHandling(`${API_BASE}/dashboard`);
  },
  
  // Export
  exportData: (type: string, format: string, filters?: Record<string, any>) => {
    return fetchWithErrorHandling(`${API_BASE}/export`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, format, filters }),
    });
  },
  
  // Compare
  compareProducts: (productIds: string[]) => {
    const params = new URLSearchParams();
    productIds.forEach(id => params.append('ids', id));
    return fetchWithErrorHandling(`${API_BASE}/products/compare?${params}`);
  },
};
