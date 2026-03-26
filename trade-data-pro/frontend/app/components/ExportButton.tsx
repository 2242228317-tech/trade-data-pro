'use client';

import { useState } from 'react';
import { Download, FileSpreadsheet, FileJson, X, Check } from 'lucide-react';
import { cn } from '@/app/lib/utils';

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: any[];
  filename?: string;
}

export function ExportModal({ isOpen, onClose, data, filename = 'export' }: ExportModalProps) {
  const [format, setFormat] = useState<'csv' | 'json' | 'excel'>('csv');
  const [exporting, setExporting] = useState(false);
  const [success, setSuccess] = useState(false);

  if (!isOpen) return null;

  const handleExport = async () => {
    setExporting(true);
    
    try {
      let content: string;
      let mimeType: string;
      let extension: string;

      switch (format) {
        case 'json':
          content = JSON.stringify(data, null, 2);
          mimeType = 'application/json';
          extension = 'json';
          break;
        case 'csv':
          content = convertToCSV(data);
          mimeType = 'text/csv;charset=utf-8;';
          extension = 'csv';
          break;
        case 'excel':
          // Excel需要额外库，先用CSV代替
          content = convertToCSV(data);
          mimeType = 'text/csv;charset=utf-8;';
          extension = 'csv';
          break;
      }

      // 创建下载链接
      const blob = new Blob([content], { type: mimeType });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `${filename}_${new Date().toISOString().split('T')[0]}.${extension}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      setSuccess(true);
      setTimeout(() => {
        setSuccess(false);
        onClose();
      }, 1500);
    } catch (error) {
      console.error('Export failed:', error);
    } finally {
      setExporting(false);
    }
  };

  const convertToCSV = (data: any[]): string => {
    if (data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const rows = data.map(item => 
      headers.map(header => {
        const value = item[header];
        // 处理嵌套对象和数组
        if (typeof value === 'object' && value !== null) {
          return JSON.stringify(value).replace(/,/g, ';');
        }
        return value;
      }).join(',')
    );
    
    return [headers.join(','), ...rows].join('\n');
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-full max-w-md mx-4">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-bold text-gray-900">导出数据</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-4 mb-6">
          <p className="text-sm text-gray-600">
            共 {data.length} 条数据，选择导出格式：
          </p>

          <div className="grid grid-cols-3 gap-3">
            <button
              onClick={() => setFormat('csv')}
              className={cn(
                "flex flex-col items-center gap-2 p-4 rounded-lg border-2 transition-all",
                format === 'csv'
                  ? "border-blue-500 bg-blue-50"
                  : "border-gray-200 hover:border-gray-300"
              )}
            >
              <FileSpreadsheet className="w-8 h-8 text-green-600" />
              <span className="text-sm font-medium">CSV</span>
            </button>

            <button
              onClick={() => setFormat('json')}
              className={cn(
                "flex flex-col items-center gap-2 p-4 rounded-lg border-2 transition-all",
                format === 'json'
                  ? "border-blue-500 bg-blue-50"
                  : "border-gray-200 hover:border-gray-300"
              )}
            >
              <FileJson className="w-8 h-8 text-orange-600" />
              <span className="text-sm font-medium">JSON</span>
            </button>

            <button
              onClick={() => setFormat('excel')}
              className={cn(
                "flex flex-col items-center gap-2 p-4 rounded-lg border-2 transition-all",
                format === 'excel'
                  ? "border-blue-500 bg-blue-50"
                  : "border-gray-200 hover:border-gray-300"
              )}
            >
              <FileSpreadsheet className="w-8 h-8 text-blue-600" />
              <span className="text-sm font-medium">Excel</span>
            </button>
          </div>
        </div>

        <button
          onClick={handleExport}
          disabled={exporting || success}
          className={cn(
            "w-full flex items-center justify-center gap-2 py-3 rounded-lg font-medium transition-all",
            success
              ? "bg-green-500 text-white"
              : "bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
          )}
        >
          {exporting ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : success ? (
            <>
              <Check className="w-5 h-5" />
              导出成功
            </>
          ) : (
            <>
              <Download className="w-5 h-5" />
              立即导出
            </>
          )}
        </button>
      </div>
    </div>
  );
}

// 导出按钮组件
export function ExportButton({ 
  data, 
  filename,
  className 
}: { 
  data: any[]; 
  filename?: string;
  className?: string;
}) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className={cn(
          "flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors",
          className
        )}
      >
        <Download className="w-4 h-4" />
        导出
      </button>

      <ExportModal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        data={data}
        filename={filename}
      />
    </>
  );
}
