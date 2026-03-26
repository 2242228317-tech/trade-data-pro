import { NextResponse } from 'next/server';
import { DataService } from '@/app/lib/data-service';

export async function GET() {
  try {
    const filterOptions = DataService.getFilterOptions();
    
    return NextResponse.json({
      success: true,
      data: filterOptions,
    });
  } catch (error) {
    console.error('Error fetching filter options:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch filter options' },
      { status: 500 }
    );
  }
}
