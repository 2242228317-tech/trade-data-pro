import { NextRequest, NextResponse } from 'next/server';
import { DataService } from '@/app/lib/data-service';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { type, format, filters, dateRange } = body;
    
    if (!type || !format) {
      return NextResponse.json(
        { success: false, error: 'Missing required fields: type, format' },
        { status: 400 }
      );
    }
    
    // Generate export data
    const exportData = DataService.exportData(type, filters || {});
    
    // Create response based on format
    let contentType: string;
    let filename: string;
    let data: string;
    
    const timestamp = new Date().toISOString().slice(0, 10);
    
    switch (format) {
      case 'csv':
        contentType = 'text/csv';
        filename = `trade-data-${type}-${timestamp}.csv`;
        data = convertToCSV(JSON.parse(exportData));
        break;
      case 'excel':
        contentType = 'application/json';
        filename = `trade-data-${type}-${timestamp}.json`;
        data = exportData;
        break;
      case 'pdf':
        contentType = 'application/json';
        filename = `trade-data-${type}-${timestamp}.json`;
        data = exportData;
        break;
      default:
        contentType = 'application/json';
        filename = `trade-data-${type}-${timestamp}.json`;
        data = exportData;
    }
    
    return NextResponse.json({
      success: true,
      data: {
        content: data,
        filename,
        contentType,
        recordCount: JSON.parse(exportData).length,
        generatedAt: new Date().toISOString(),
      },
    });
  } catch (error) {
    console.error('Error exporting data:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to export data' },
      { status: 500 }
    );
  }
}

function convertToCSV(data: any[]): string {
  if (data.length === 0) return '';
  
  const headers = Object.keys(data[0]);
  const csvRows = [headers.join(',')];
  
  for (const row of data) {
    const values = headers.map(header => {
      const value = row[header];
      if (typeof value === 'object') {
        return `"${JSON.stringify(value).replace(/"/g, '""')}"`;
      }
      return `"${String(value).replace(/"/g, '""')}"`;
    });
    csvRows.push(values.join(','));
  }
  
  return csvRows.join('\n');
}
