// file: app/statistics/PodcastSelector.tsx
'use client';
import React, { useState } from 'react';

interface PodcastSelectorProps {
  onSelect: (podcastIndexId: number) => void;
}

export default function PodcastSelector({ onSelect }: PodcastSelectorProps) {
  const [input, setInput] = useState('');
  const [selected, setSelected] = useState<number | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const id = parseInt(input);
    if (!isNaN(id)) {
      setSelected(id);
      onSelect(id);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 items-center mb-4">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter podcast_index_id..."
        className="px-3 py-2 border rounded-md bg-white dark:bg-gray-800 text-sm w-64 text-black dark:text-white"
      />
      <button
        type="submit"
        className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition"
      >
        Load Stats
      </button>
    </form>
  );
}
