"use client";
import React, { useState } from "react";
import Sidebar from "../../components/Sidebar";
import { ChevronDownIcon } from "@heroicons/react/24/outline";

export default function ReportsPage() {
  const [selectedPodcast, setSelectedPodcast] = useState("Podcast Name");

  // Dummy list for dropdown – replace with real data
  const podcasts = ["Podcast Name", "Another Podcast", "Tech Talk", "Daily Recap"];

  return (
    <div className="flex min-h-screen bg-podverse-background text-white">
      <Sidebar />
      <main className="flex-1 p-6 space-y-6 overflow-y-auto">
        {/* Podcast Selector */}
        <div className="flex items-center justify-between">
          <div>
            <label className="text-lg font-semibold">Select Podcast:</label>
            <div className="relative inline-block ml-4">
              <select
                value={selectedPodcast}
                onChange={(e) => setSelectedPodcast(e.target.value)}
                className="bg-podverse-surface border border-gray-700 rounded px-4 py-2 pr-8 text-white"
              >
                {podcasts.map((podcast) => (
                  <option key={podcast} value={podcast}>
                    {podcast}
                  </option>
                ))}
              </select>
              <ChevronDownIcon className="absolute right-2 top-2 w-5 h-5 pointer-events-none" />
            </div>
          </div>
          <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Download Report
          </button>
        </div>

        {/* Podcast Info */}
        <section className="bg-podverse-surface p-6 rounded shadow">
          <h2 className="text-2xl font-semibold mb-2">{selectedPodcast}</h2>
          <p className="text-gray-300">
            Your go-to source for insightful discussions and engaging stories.
          </p>
        </section>

        {/* Metrics Grid */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard label="Total Episodes" value="15" delta="+2" />
          <MetricCard label="Avg. Listeners" value="350" delta="+50" />
          <MetricCard label="Total Downloads" value="5000" delta="+800" />
          <MetricCard label="Listener Ratings" value="4.8" />
        </section>

        {/* Monthly Chart Placeholder */}
        <section className="bg-podverse-surface p-6 rounded shadow h-64 flex items-center justify-center">
          <span className="text-gray-400">[ Monthly Downloads Chart Here ]</span>
        </section>

        {/* Audit Log */}
        <section className="bg-podverse-surface p-6 rounded shadow">
          <h3 className="text-xl font-semibold mb-4">Audit Log</h3>
          <div className="space-y-2">
            {[...Array(5)].map((_, i) => (
              <div
                key={i}
                className="bg-gray-800 hover:bg-gray-700 transition p-3 rounded"
              >
                <p className="font-semibold">Logged Change</p>
                <p className="text-sm text-gray-400">Support Team Member - 6/1/2025 12:00 AM</p>
              </div>
            ))}
          </div>
        </section>

        {/* Listener Engagement */}
        <section className="bg-podverse-surface p-6 rounded shadow">
          <h3 className="text-xl font-semibold mb-2">Listener Engagement</h3>
          <p className="text-gray-300 mb-4">
            Engagement stats for the last quarter.
          </p>
          <div className="h-40 bg-gray-900 flex items-center justify-center rounded">
            <span className="text-gray-500">[ Engagement Chart Placeholder ]</span>
          </div>
        </section>
      </main>
    </div>
  );
}

// Simple reusable metric card
function MetricCard({
  label,
  value,
  delta,
}: {
  label: string;
  value: string | number;
  delta?: string;
}) {
  return (
    <div className="bg-podverse-surface p-4 rounded shadow space-y-1">
      <p className="text-sm text-gray-400">{label}</p>
      <p className="text-2xl font-bold">{value}</p>
      {delta && <p className="text-green-400 text-sm">{delta}</p>}
    </div>
  );
}
