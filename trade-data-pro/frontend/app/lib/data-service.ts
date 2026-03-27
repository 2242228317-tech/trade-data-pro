// 简单的数据服务导出
export const DataService = {
  getProducts: async () => {
    const res = await fetch('/api/products');
    return res.json();
  },
  getProduct: async (id: string) => {
    const res = await fetch(`/api/products/${id}`);
    return res.json();
  },
  getCustomsData: async () => {
    const res = await fetch('/api/customs');
    return res.json();
  },
  getDashboardStats: async () => {
    const res = await fetch('/api/dashboard');
    return res.json();
  },
};

export default DataService;
