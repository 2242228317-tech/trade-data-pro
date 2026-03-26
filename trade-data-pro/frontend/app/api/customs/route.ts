import { NextRequest, NextResponse } from 'next/server';
import { DataService } from '@/app/lib/data-service';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    
    const filters = {
      category: searchParams.get('category') || undefined,
      country: searchParams.get('country') || undefined,
      year: searchParams.has('year') ? Number(searchParams.get('year')) : undefined,
      month: searchParams.has('month') ? Number(searchParams.get('month')) : undefined,
      region: searchParams.get('region') || undefined,
    };
    
    const customsData = DataService.getCustomsData(filters);
    
    // Aggregate data by category
    const categoryStats = customsData.reduce((acc, item) => {
      if (!acc[item.category]) {
        acc[item.category] = { value: 0, quantity: 0, count: 0 };
      }
      acc[item.category].value += item.exportValue;
      acc[item.category].quantity += item.exportQuantity;
      acc[item.category].count += 1;
      return acc;
    }, {} as Record<string, { value: number; quantity: number; count: number }>);
    
    // Aggregate by country
    const countryStats = customsData.reduce((acc, item) => {
      if (!acc[item.destinationCountry]) {
        acc[item.destinationCountry] = { value: 0, quantity: 0, region: item.destinationRegion };
      }
      acc[item.destinationCountry].value += item.exportValue;
      acc[item.destinationCountry].quantity += item.exportQuantity;
      return acc;
    }, {} as Record<string, { value: number; quantity: number; region: string }>);
    
    // Aggregate by month
    const monthlyStats = customsData.reduce((acc, item) => {
      const key = `${item.year}-${item.month.toString().padStart(2, '0')}`;
      if (!acc[key]) {
        acc[key] = { value: 0, quantity: 0, growth: 0 };
      }
      acc[key].value += item.exportValue;
      acc[key].quantity += item.exportQuantity;
      return acc;
    }, {} as Record<string, { value: number; quantity: number; growth: number }>);
    
    return NextResponse.json({
      success: true,
      data: {
        records: customsData.slice(0, 100),
        summary: {
          totalValue: customsData.reduce((sum, d) => sum + d.exportValue, 0),
          totalQuantity: customsData.reduce((sum, d) => sum + d.exportQuantity, 0),
          recordCount: customsData.length,
        },
        byCategory: Object.entries(categoryStats).map(([name, stats]) => ({
          name,
          exportValue: stats.value,
          exportQuantity: stats.quantity,
          avgUnitPrice: stats.value / stats.quantity,
        })),
        byCountry: Object.entries(countryStats)
          .map(([name, stats]) => ({
            name,
            exportValue: stats.value,
            exportQuantity: stats.quantity,
            region: stats.region,
          }))
          .sort((a, b) => b.exportValue - a.exportValue)
          .slice(0, 20),
        byMonth: Object.entries(monthlyStats)
          .map(([month, stats]) => ({
            month,
            exportValue: stats.value,
            exportQuantity: stats.quantity,
          }))
          .sort((a, b) => a.month.localeCompare(b.month)),
      },
    });
  } catch (error) {
    console.error('Error fetching customs data:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch customs data' },
      { status: 500 }
    );
  }
}
