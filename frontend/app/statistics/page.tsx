'use client';
import React from 'react';
import StatsChart from './StatsChart';
import StatsChannel from './StatsChannel'; // 👈 import the new component
import Sidebar from '../../components/Sidebar';

export default function StatsDashboard() {
  const channelId = 4; // 🔧 You can make this dynamic later

  return (
    <div className="flex min-h-screen bg-gray-50 dark:bg-gray-950">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <main className="flex-1 p-6 space-y-6">
        <h1 className="text-2xl font-bold">📊 Stats Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-300">
          Monitor podcast performance across time.
        </p>

        {/* Chart */}
        <div className="bg-white dark:bg-gray-900 rounded-2xl shadow p-4">
          <StatsChart />
        </div>

        {/* Channel-specific metadata */}
        <div className="bg-white dark:bg-gray-900 rounded-2xl shadow p-4">
          <StatsChannel channelId={channelId} />
        </div>
      </main>
    </div>
  );
}
