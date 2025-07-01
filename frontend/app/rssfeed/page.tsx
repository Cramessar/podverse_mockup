// File: frontend/app/rssfeed/page.tsx
"use client";

import React, { useState, useEffect } from "react";
import Sidebar from "../../components/Sidebar";

interface FeedLog {
  time: string;
  message: string;
}

interface FeedResult {
  new: number;
  updated: number;
  unchanged: number;
  errors: string[];
}

interface Feed {
  id: number;
  title: string;
  status: "live" | "flagged" | "error";
  lastUpdated: string;
  episodeCount: number;
  lastResult: FeedResult;
  logs: FeedLog[];
}

const mockFeeds: Feed[] = [
  {
    id: 1,
    title: "Tech News Weekly",
    status: "flagged",
    lastUpdated: "2025-06-30T09:14:12Z",
    episodeCount: 50,
    lastResult: { new: 3, updated: 1, unchanged: 46, errors: [] },
    logs: [
      { time: "2025-06-30T09:14:12Z", message: "3 new, 1 updated" },
      { time: "2025-06-28T07:02:00Z", message: "No changes" },
    ],
  },
  {
    id: 2,
    title: "Sports Daily",
    status: "live",
    lastUpdated: "2025-06-30T11:00:00Z",
    episodeCount: 120,
    lastResult: { new: 0, updated: 0, unchanged: 120, errors: [] },
    logs: [{ time: "2025-06-30T11:00:00Z", message: "No changes" }],
  },
  {
    id: 3,
    title: "True Crime Central",
    status: "error",
    lastUpdated: "2025-06-30T10:30:00Z",
    episodeCount: 0,
    lastResult: {
      new: 0,
      updated: 0,
      unchanged: 0,
      errors: ["Failed to parse XML"],
    },
    logs: [
      { time: "2025-06-30T10:30:00Z", message: "Error: Failed to parse XML" },
    ],
  },
];

export default function AdminFeedsPage() {
  const [feeds, setFeeds] = useState<Feed[]>([]);
  const [expandedFeedId, setExpandedFeedId] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>("");

  useEffect(() => {
    setFeeds(mockFeeds);
  }, []);

  const toggleExpand = (feedId: number) => {
    setExpandedFeedId(expandedFeedId === feedId ? null : feedId);
  };

  const handleCopyLogs = (logs: FeedLog[]) => {
    const text = logs.map((log) => `${log.time}: ${log.message}`).join("\n");
    navigator.clipboard.writeText(text);
    alert("Logs copied to clipboard!");
  };

  const handleDownloadLogs = (logs: FeedLog[], title: string) => {
    const text = logs.map((log) => `${log.time}: ${log.message}`).join("\n");
    const blob = new Blob([text], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${title}_logs.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const filteredFeeds = feeds.filter((feed) =>
    feed.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="flex min-h-screen bg-podverse-background text-podverse-text">
      <Sidebar />
      <div className="flex-1 p-6">
        <h1 className="text-2xl font-bold mb-4 text-podverse-secondary">
          RSS Feed Dashboard
        </h1>

        <input
          type="text"
          placeholder="Search feeds..."
          className="border border-podverse-border px-3 py-2 rounded mb-4 w-full max-w-md bg-podverse-surface text-podverse-text placeholder-podverse-muted"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />

        <div className="overflow-x-auto">
          <table className="min-w-full bg-podverse-surface rounded shadow text-podverse-text text-sm">
            <thead className="bg-podverse-accent text-black">
              <tr>
                {[
                  "Title",
                  "Status",
                  "Last Updated",
                  "Episodes",
                  "Details",
                  "Action",
                ].map((header) => (
                  <th key={header} className="text-left px-4 py-2 font-semibold">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filteredFeeds.map((feed) => (
                <React.Fragment key={feed.id}>
                  <tr className="border-t border-podverse-border">
                    <td className="px-4 py-2 font-medium">{feed.title}</td>
                    <td className="px-4 py-2">
                      <span
                        className={`text-xs px-2 py-1 rounded font-semibold ${
                          feed.status === "flagged"
                            ? "bg-podverse-accent text-white"
                            : feed.status === "live"
                            ? "bg-green-600 text-white"
                            : "bg-yellow-500 text-black"
                        }`}
                      >
                        {feed.status}
                      </span>
                    </td>
                    <td className="px-4 py-2 text-sm" title={feed.lastUpdated}>
                      {new Date(feed.lastUpdated).toLocaleString()}
                    </td>
                    <td className="px-4 py-2">{feed.episodeCount}</td>
                    <td className="px-4 py-2 text-sm">
                      {feed.status === "error" ? (
                        <span className="text-podverse-danger">{feed.lastResult.errors[0]}</span>
                      ) : (
                        <div className="text-podverse-muted">
                          ✔ {feed.lastResult.new} new, 🔁 {feed.lastResult.updated} updated, ➖ {feed.lastResult.unchanged} unchanged
                        </div>
                      )}
                      <button
                        className="ml-2 text-podverse-accent hover:underline text-xs"
                        onClick={() => toggleExpand(feed.id)}
                      >
                        {expandedFeedId === feed.id ? "Hide Log" : "View Log"}
                      </button>
                    </td>
                    <td className="px-4 py-2">
                      <button
                        className="bg-podverse-primary hover:bg-podverse-accent text-white text-sm px-3 py-1 rounded"
                        onClick={() => alert(`Reparsing feed: ${feed.title}`)}
                      >
                        {feed.status === "error" ? "Retry" : "Reparse"}
                      </button>
                    </td>
                  </tr>
                  {expandedFeedId === feed.id && (
                    <tr className="bg-podverse-surface">
                      <td colSpan={6} className="px-6 py-3 border-t border-podverse-border">
                        <div className="flex justify-between items-center mb-2">
                          <h3 className="font-semibold text-sm text-podverse-text">Audit Log</h3>
                          <div className="space-x-2">
                            <button
                              className="text-xs bg-podverse-surface px-2 py-1 rounded hover:bg-podverse-highlight text-podverse-accent"
                              onClick={() => handleCopyLogs(feed.logs)}
                            >
                              Copy Log
                            </button>
                            <button
                              className="text-xs bg-podverse-surface px-2 py-1 rounded hover:bg-podverse-highlight text-podverse-accent"
                              onClick={() => handleDownloadLogs(feed.logs, feed.title)}
                            >
                              Download Log
                            </button>
                          </div>
                        </div>
                        <ul className="text-xs text-podverse-muted list-disc ml-5">
                          {feed.logs.map((log, i) => (
                            <li key={i}>
                              <strong>{new Date(log.time).toLocaleString()}:</strong> {log.message}
                            </li>
                          ))}
                        </ul>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}