// file: frontend/app/statistics/ChannelStatsChart.tsx
'use client';
import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { fetchChannelStatsById } from '@/lib/api';

interface ChannelStatsChartProps {
  channelId: number;
}

export default function ChannelStatsChart({ channelId }: ChannelStatsChartProps) {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetchChannelStatsById(channelId);
        const channel = res.data;

        const daysBack = 7;
        const today = new Date();

        const series = Array.from({ length: daysBack }, (_, i) => {
          const dayOffset = daysBack - i;
          const date = new Date(today);
          date.setDate(today.getDate() - dayOffset);
          const key = `day_${dayOffset}_count`;

          return {
            date: date.toISOString().split('T')[0],
            listens: channel[key] || 0,
          };
        });

        setData(series);
      } catch (err) {
        console.error('Failed to load channel stats chart', err);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [channelId]);

  if (loading) return <p className="text-sm text-gray-500 dark:text-gray-400">Loading chart...</p>;

  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold mb-2">📈 7-Day Listen Trend</h3>
      <ResponsiveContainer width="100%" height={260}>
        <LineChart data={data} margin={{ top: 10, right: 30, bottom: 0, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.15} />
          <XAxis dataKey="date" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip />
          <Line type="monotone" dataKey="listens" stroke="#6366F1" strokeWidth={2.5} dot={{ r: 4 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
