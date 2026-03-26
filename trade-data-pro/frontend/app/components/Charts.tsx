// Chart components using Recharts
'use client';

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
} from 'recharts';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16'];

interface LineChartProps {
  data: any[];
  xKey: string;
  yKey: string;
  title?: string;
  height?: number;
}

export function TrendLineChart({ data, xKey, yKey, title, height = 300 }: LineChartProps) {
  return (
    <div style={{ width: '100%', height }} className="bg-white rounded-xl p-4 border border-gray-100">
      {title && <h3 className="text-sm font-bold text-gray-900 mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height={height - (title ? 40 : 0)}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
          <XAxis dataKey={xKey} tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              fontSize: '12px',
            }}
          />
          <Area
            type="monotone"
            dataKey={yKey}
            stroke="#3b82f6"
            strokeWidth={2}
            fillOpacity={1}
            fill="url(#colorValue)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

interface BarChartProps {
  data: any[];
  xKey: string;
  yKey: string;
  title?: string;
  color?: string;
  height?: number;
}

export function TrendBarChart({ data, xKey, yKey, title, color = '#3b82f6', height = 300 }: BarChartProps) {
  return (
    <div style={{ width: '100%', height }} className="bg-white rounded-xl p-4 border border-gray-100">
      {title && <h3 className="text-sm font-bold text-gray-900 mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height={height - (title ? 40 : 0)}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
          <XAxis dataKey={xKey} tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              fontSize: '12px',
            }}
          />
          <Bar dataKey={yKey} fill={color} radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

interface PieChartProps {
  data: any[];
  nameKey: string;
  valueKey: string;
  title?: string;
  height?: number;
}

export function TrendPieChart({ data, nameKey, valueKey, title, height = 300 }: PieChartProps) {
  return (
    <div style={{ width: '100%', height }} className="bg-white rounded-xl p-4 border border-gray-100">
      {title && <h3 className="text-sm font-bold text-gray-900 mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height={height - (title ? 40 : 0)}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            paddingAngle={2}
            dataKey={valueKey}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              fontSize: '12px',
            }}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

interface MultiLineChartProps {
  data: any[];
  xKey: string;
  lines: { key: string; name: string; color: string }[];
  title?: string;
  height?: number;
}

export function MultiLineChart({ data, xKey, lines, title, height = 300 }: MultiLineChartProps) {
  return (
    <div style={{ width: '100%', height }} className="bg-white rounded-xl p-4 border border-gray-100">
      {title && <h3 className="text-sm font-bold text-gray-900 mb-4">{title}</h3>}
      <ResponsiveContainer width="100%" height={height - (title ? 40 : 0)}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
          <XAxis dataKey={xKey} tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              fontSize: '12px',
            }}
          />
          <Legend />
          {lines.map((line) => (
            <Line
              key={line.key}
              type="monotone"
              dataKey={line.key}
              name={line.name}
              stroke={line.color}
              strokeWidth={2}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
