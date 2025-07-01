'use client';
import React, { useState } from 'react';
import StatsChart from './StatsChart';
import StatsChannel from './StatsChannel';
import Sidebar from '../../components/Sidebar';
import ChannelSelector from './ChannelSelector';

export default function StatsDashboard() {
  const [selectedPodcastId, setSelectedPodcastId] = useState<number | null>(null);

  return (
    <div className="flex min-h-screen bg-gray-50 dark:bg-gray-950">
      <Sidebar />

      <main className="flex-1 p-6 space-y-6">
        <h1 className="text-2xl font-bold">📊 Stats Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-300">
          Monitor podcast performance across time.
        </p>

        {/* Global Chart */}
        <div className="bg-white dark:bg-gray-900 rounded-2xl shadow p-4">
          <StatsChart />
        </div>

        {/* Channel Selector */}
        <div className="bg-white dark:bg-gray-900 rounded-2xl shadow p-4">
          <ChannelSelector onSelect={(id) => setSelectedPodcastId(id)} />
        </div>

        {/* Channel Stats */}
        {selectedPodcastId && (
          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow p-4">
            <StatsChannel channelId={selectedPodcastId} />
          </div>
        )}
      </main>
    </div>
  );
}
