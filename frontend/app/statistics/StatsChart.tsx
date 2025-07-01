'use client';
import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid,
  TooltipProps,
} from 'recharts';
import { FaHeadphones, FaDownload } from 'react-icons/fa';
import { NameType, ValueType } from 'recharts/types/component/DefaultTooltipContent';
import { fetchChannelStats } from '@/lib/api';

interface ChannelStatPoint {
  date: string;
  listens: number;
  downloads: number;
}

const CustomTooltip = ({
  active,
  payload,
  label,
}: TooltipProps<ValueType, NameType>) => {
  if (active && payload && payload.length) {
    const listens = payload.find((p: any) => p.dataKey === 'listens');
    const downloads = payload.find((p: any) => p.dataKey === 'downloads');

    return (
      <div className="bg-white dark:bg-gray-800 text-sm text-gray-800 dark:text-gray-200 p-3 rounded-lg shadow-md">
        <p className="font-semibold mb-1">{label}</p>
        {listens && (
          <p className="flex items-center gap-2">
            <FaHeadphones className="text-indigo-500" />
            Listens: <span className="font-medium">{listens.value}</span>
          </p>
        )}
        {downloads && (
          <p className="flex items-center gap-2">
            <FaDownload className="text-green-400" />
            Downloads: <span className="font-medium">{downloads.value}</span>
          </p>
        )}
      </div>
    );
  }

  return null;
};

export default function StatsChart() {
  const [data, setData] = useState<ChannelStatPoint[]>([]);
  const [hiddenLines, setHiddenLines] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const response = await fetchChannelStats();
        console.log("Raw stats from API:", response);

        // Take only the most recent channel for now (or choose a specific one)
        const channel = response.data[0];

        // Convert day_1_count through day_7_count into time series
        const daysBack = 7;
        const today = new Date();

        const timeSeries: ChannelStatPoint[] = Array.from({ length: daysBack }, (_, i) => {
          const dayOffset = daysBack - i; // day_7_count → oldest
          const date = new Date(today);
          date.setDate(today.getDate() - dayOffset);
          const key = `day_${dayOffset}_count`;

          return {
            date: date.toISOString().split('T')[0], // YYYY-MM-DD
            listens: channel[key] || 0,
            downloads: Math.floor(channel[key] * 0.3), // mock downloads for now
          };
        });

        console.log("Transformed time series:", timeSeries);
        setData(timeSeries);
      } catch (err: any) {
        setError(err.message || 'Failed to load stats');
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  const toggleLine = (key: string) => {
    setHiddenLines(prev =>
      prev.includes(key) ? prev.filter(k => k !== key) : [...prev, key]
    );
  };

  const renderLegend = () => {
    const lines = [
      { key: 'listens', label: 'Listens', color: '#6366F1' },
      { key: 'downloads', label: 'Downloads', color: '#34D399' },
    ];

    return (
      <ul className="flex gap-4 mt-2 ml-4">
        {lines.map(({ key, label, color }) => {
          const isHidden = hiddenLines.includes(key);
          return (
            <li
              key={key}
              className={`cursor-pointer transition-all duration-200 ${
                isHidden ? 'opacity-40' : 'opacity-100'
              }`}
              onClick={() => toggleLine(key)}
            >
              <span
                className="inline-block w-3 h-3 rounded-full mr-2"
                style={{ backgroundColor: color }}
              ></span>
              <span className="text-sm">{label}</span>
            </li>
          );
        })}
      </ul>
    );
  };

  if (loading) {
    return <p className="text-gray-500 dark:text-gray-400">Loading chart data...</p>;
  }

  if (error) {
    return <p className="text-red-500">Error: {error}</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={320}>
      <LineChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 10 }}>
        <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.2} />
        <XAxis dataKey="date" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
        <YAxis tick={{ fill: '#9CA3AF', fontSize: 12 }} />
        <Tooltip content={<CustomTooltip />} />
        <Legend content={renderLegend as any} />
        {!hiddenLines.includes('listens') && (
          <Line
            type="monotone"
            dataKey="listens"
            stroke="#6366F1"
            strokeWidth={2.5}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
            name="Listens"
          />
        )}
        {!hiddenLines.includes('downloads') && (
          <Line
            type="monotone"
            dataKey="downloads"
            stroke="#34D399"
            strokeWidth={2.5}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
            name="Downloads"
          />
        )}
      </LineChart>
    </ResponsiveContainer>
  );
}
