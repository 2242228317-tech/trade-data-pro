import { NextResponse } from 'next/server';
import { DataService } from '@/app/lib/data-service';

export async function GET() {
  try {
    const stats = DataService.getDashboardStats();
    const categoryStats = DataService.getCategoryStats();
    const regionStats = DataService.getRegionStats();
    const trending = DataService.getTrendingProducts(6);
    
    return NextResponse.json({
      success: true,
      data: {
        stats,
        categories: categoryStats,
        regions: regionStats,
        trending,
      },
    });
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch dashboard data' },
      { status: 500 }
    );
  }
}
