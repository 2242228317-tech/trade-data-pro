import { NextRequest, NextResponse } from 'next/server';
import { DataService } from '@/app/lib/data-service';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = Number(searchParams.get('limit')) || 10;
    
    const trendingProducts = DataService.getTrendingProducts(limit);
    
    return NextResponse.json({
      success: true,
      data: trendingProducts,
    });
  } catch (error) {
    console.error('Error fetching trending products:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch trending products' },
      { status: 500 }
    );
  }
}
