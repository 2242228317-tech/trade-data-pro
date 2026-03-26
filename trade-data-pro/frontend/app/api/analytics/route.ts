import { NextRequest, NextResponse } from 'next/server';
import { DataService } from '@/app/lib/data-service';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const productId = searchParams.get('productId');
    
    if (productId) {
      // Get analytics for specific product
      const analytics = DataService.getProductAnalytics(productId);
      
      if (!analytics) {
        return NextResponse.json(
          { success: false, error: 'Product not found' },
          { status: 404 }
        );
      }
      
      return NextResponse.json({
        success: true,
        data: analytics,
      });
    }
    
    // Get overall analytics
    const categoryStats = DataService.getCategoryStats();
    const regionStats = DataService.getRegionStats();
    const dashboardStats = DataService.getDashboardStats();
    
    // Get top trending products
    const trendingProducts = DataService.getTrendingProducts(10);
    
    return NextResponse.json({
      success: true,
      data: {
        overview: dashboardStats,
        categories: categoryStats,
        regions: regionStats,
        trending: trendingProducts,
      },
    });
  } catch (error) {
    console.error('Error fetching analytics:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch analytics' },
      { status: 500 }
    );
  }
}
