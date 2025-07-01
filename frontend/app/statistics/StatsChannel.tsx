'use client';
import React, { useEffect, useState } from 'react';
import { fetchChannelStatsById } from '@/lib/api';

interface StatsChannelProps {
  channelId: number;
}

export default function StatsChannel({ channelId }: StatsChannelProps) {
  const [channelData, setChannelData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadChannelStats = async () => {
      try {
        const response = await fetchChannelStatsById(channelId);
        console.log('Detailed channel stats:', response);
        setChannelData(response.data);
      } catch (err: any) {
        setError('Failed to load channel stats');
      } finally {
        setLoading(false);
      }
    };

    loadChannelStats();
  }, [channelId]);

  if (loading) return <p className="text-gray-500 dark:text-gray-400">Loading...</p>;
  if (error) return <p className="text-red-500">{error}</p>;
  if (!channelData) return null;

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">📡 Channel Stats</h1>
      <p className="text-gray-600 dark:text-gray-300">
        Viewing detailed stats for: <span className="font-semibold">{channelData.title}</span>
      </p>

      <div className="bg-white dark:bg-gray-900 rounded-2xl shadow p-4">
        <h2 className="text-xl font-semibold mb-2">Metadata</h2>
        <ul className="text-sm text-gray-700 dark:text-gray-300 space-y-1">
          <li><strong>ID:</strong> {channelData.id}</li>
          <li><strong>Slug:</strong> {channelData.slug}</li>
          <li><strong>ID Text:</strong> {channelData.id_text}</li>
          <li><strong>Podcast GUID:</strong> {channelData.podcast_guid}</li>
          <li><strong>Has Value Splits:</strong> {channelData.has_value_time_splits ? 'Yes' : 'No'}</li>
        </ul>
      </div>

      {/* Placeholder for future graph or related item stats */}
      <div className="bg-white dark:bg-gray-900 rounded-2xl shadow p-4 mt-4">
        <h2 className="text-xl font-semibold mb-2">Related Stats</h2>
        <p>Stats ID(s): {channelData.stats?.join(', ') || 'None'}</p>
        <p>Item ID(s): {channelData.items?.join(', ') || 'None'}</p>
      </div>
    </div>
  );
}
