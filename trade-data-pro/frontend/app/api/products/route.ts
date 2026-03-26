import { NextRequest, NextResponse } from 'next/server';
import { searchProducts, getFilterOptions } from '@/app/lib/data-service';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    
    const filters = {
      keyword: searchParams.get('keyword') || undefined,
      category: searchParams.get('category') || undefined,
      subcategory: searchParams.get('subcategory') || undefined,
      minPrice: searchParams.has('minPrice') ? Number(searchParams.get('minPrice')) : undefined,
      maxPrice: searchParams.has('maxPrice') ? Number(searchParams.get('maxPrice')) : undefined,
      moq: searchParams.has('moq') ? Number(searchParams.get('moq')) : undefined,
      region: searchParams.get('region') || undefined,
      sortBy: (searchParams.get('sortBy') as any) || 'relevance',
      page: Number(searchParams.get('page')) || 1,
      pageSize: Number(searchParams.get('pageSize')) || 20,
    };
    
    const result = searchProducts(filters);
    
    return NextResponse.json({
      success: true,
      ...result,
    });
  } catch (error) {
    console.error('Error fetching products:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch products' },
      { status: 500 }
    );
  }
}
