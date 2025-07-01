// file: frontend/app/statistics/ChannelSelector.tsx
'use client';
import React, { useEffect, useState } from 'react';
import { fetchChannels } from '@/lib/api';

interface ChannelSelectorProps {
  onSelect: (channelId: number) => void;
}

export default function ChannelSelector({ onSelect }: ChannelSelectorProps) {
  const [channels, setChannels] = useState<any[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadChannels = async () => {
      try {
        const res = await fetchChannels();
        setChannels(res.data); // assumes { data: [...] }
      } catch (err) {
        console.error('Failed to load channels');
      } finally {
        setLoading(false);
      }
    };

    loadChannels();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const id = parseInt(e.target.value);
    setSelectedId(id);
    onSelect(id);
  };

  return (
    <div className="mb-4">
      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
        Select a Podcast Channel
      </label>
      <select
        value={selectedId ?? ''}
        onChange={handleChange}
        className="w-full px-3 py-2 rounded-md border bg-white dark:bg-gray-800 text-black dark:text-white"
      >
        <option value="" disabled>Select a channel...</option>
        {loading ? (
          <option>Loading...</option>
        ) : (
          channels.map((channel) => (
            <option key={channel.id} value={channel.id}>
              {channel.title || `Untitled (${channel.id})`}
            </option>
          ))
        )}
      </select>
    </div>
  );
}
