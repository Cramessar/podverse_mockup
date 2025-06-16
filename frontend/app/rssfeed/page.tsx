"use client";
import React, { useState } from "react";
import Sidebar from "../../components/Sidebar";

export default function AdminFeeds() {
  const [selectedFeed, setSelectedFeed] = useState<number | null>(null);

  // Sample feeds data (replace with real data)
  const feeds = [
    {
      id: 1,
      category: "Tech News",
      status: "flagged",
      statusColor: "bg-red-500",
      flaggedStatus: "1 Hour",
      lastUpdated: "2 days ago",
      views: 500,
      shares: 50,
      duration: "2 days",
      contact: "admin@technews.com",
      auditLogs: [
        { date: "5/31/2025", description: "Logged Change", user: "Support Team" },
        { date: "5/25/2025", description: "Logged Change", user: "Support Team" },
      ],
    },
    {
      id: 2,
      category: "Sports Updates",
      status: "live",
      statusColor: "bg-green-500",
      flaggedStatus: "30 Days",
      lastUpdated: "1 hour ago",
      views: 1500,
      shares: 150,
      duration: "30 days",
      contact: "admin@sportsupdates.com",
      auditLogs: [
        { date: "5/31/2025", description: "Logged Change", user: "Support Team" },
      ],
    },
  ];

  return (
    <div className="flex min-h-screen bg-[#121214] text-white">
      <Sidebar />

      <main className="flex-1 p-8 space-y-8">
        <h1 className="text-3xl font-bold mb-6">Manage RSS Feeds</h1>

        {/* Filters */}
        <section className="flex space-x-4 mb-6">
          {["Category", "Status", "Time", "Sort By"].map((filter) => (
            <select
              key={filter}
              className="bg-[#23232e] border border-[#2a2a35] rounded px-4 py-2 text-white focus:outline-none"
              defaultValue={filter}
              aria-label={filter}
            >
              <option disabled>{filter}</option>
              <option>Option 1</option>
              <option>Option 2</option>
            </select>
          ))}

          {/* Action buttons */}
          <button
            className="ml-auto p-2 border border-[#2a2a35] rounded hover:bg-[#2a2a35] transition"
            title="Reparse"
          >
            🔄
          </button>
          <button
            className="p-2 border border-[#2a2a35] rounded hover:bg-[#2a2a35] transition"
            title="Flag"
          >
            🚩
          </button>
          <button
            className="p-2 border border-[#2a2a35] rounded hover:bg-[#2a2a35] transition"
            title="Delete"
          >
            🗑️
          </button>
        </section>

        {/* Feeds List */}
        <section>
          {feeds.map((feed) => (
            <div
              key={feed.id}
              className={`p-4 rounded mb-4 border cursor-pointer ${
                selectedFeed === feed.id ? "bg-[#2a2a35]" : "bg-[#23232e]"
              }`}
              onClick={() => setSelectedFeed(selectedFeed === feed.id ? null : feed.id)}
            >
              <div className="flex items-center space-x-4">
                <input
                  type="checkbox"
                  checked={selectedFeed === feed.id}
                  onChange={() =>
                    setSelectedFeed(selectedFeed === feed.id ? null : feed.id)
                  }
                />
                <div
                  className={`w-4 h-4 rounded-full ${feed.statusColor}`}
                  aria-label={feed.status}
                />
                <div>
                  <p className="font-semibold">{feed.category}</p>
                  <p className="text-sm text-[#7a7a8c] capitalize">{feed.status}</p>
                </div>
                <div className="ml-auto space-x-6 text-sm text-[#7a7a8c]">
                  <span>
                    {feed.status.charAt(0).toUpperCase() + feed.status.slice(1)} Status:{" "}
                    {feed.flaggedStatus}
                  </span>
                  <span>Last Updated: {feed.lastUpdated}</span>
                </div>
                <button
                  title="Refresh Feed"
                  className="ml-6 p-2 rounded hover:bg-[#2a2a35] transition"
                  onClick={() => alert(`Refresh feed ${feed.category}`)}
                >
                  🔄
                </button>
              </div>

              {/* Detailed info if selected */}
              {selectedFeed === feed.id && (
                <div className="mt-4 grid grid-cols-2 gap-8 border-t pt-4 text-sm text-[#7a7a8c]">
                  <div>
                    <h3 className="font-semibold mb-2">Performance Metrics</h3>
                    <p>Views: {feed.views}</p>
                    <p>Shares: {feed.shares}</p>
                    <p>Status Duration: {feed.duration}</p>
                    <p>Contact Info: {feed.contact}</p>
                  </div>
                  <div>
                    <h3 className="font-semibold mb-2">Audit Log</h3>
                    {feed.auditLogs.map((log, idx) => (
                      <div
                        key={idx}
                        className="mb-2 border-b border-[#2a2a35] last:border-none"
                      >
                        <p>{log.description}</p>
                        <p className="text-xs">{log.user}</p>
                        <p className="text-xs text-[#52525b]">{log.date}</p>
                      </div>
                    ))}
                    <button className="mt-2 bg-[#3772ff] text-white px-3 py-1 rounded hover:bg-[#1c57d1] transition">
                      Full Audit Log
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}
