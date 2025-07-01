"use client";

import React, { useState, useEffect } from "react";
import Sidebar from "../../components/Sidebar";
import { fetchFeeds, fetchFeedLogs } from "@/lib/api";

interface FeedLog {
  time: string;
  message: string;
}

interface Feed {
  id: number;
  url: string;
  feed_flag_status_id: number;
  is_parsing: boolean;
  parsing_priority: number;
  last_parsed_file_hash: string;
  container_id: string;
  created_at: string;
  updated_at: string;
  logs?: FeedLog[];
}

export default function AdminFeedsPage() {
  const [feeds, setFeeds] = useState<Feed[]>([]);
  const [expandedFeedId, setExpandedFeedId] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const loadFeeds = async () => {
      try {
        const response = await fetchFeeds();
        setFeeds(response.data);
      } catch (err: any) {
        setError("Failed to load feeds");
        console.error(err);
      }
    };
    loadFeeds();
  }, []);

  const toggleExpand = async (feedId: number) => {
    if (expandedFeedId === feedId) {
      setExpandedFeedId(null);
      return;
    }

    const feed = feeds.find(f => f.id === feedId);
    if (feed && !feed.logs) {
      try {
        const logRes = await fetchFeedLogs(feedId);

        const parsedLogs: FeedLog[] = logRes.logs.map((log: any) => ({
          time: log.last_finished_parse_time || log.last_good_http_status_time || new Date().toISOString(),
          message: `${log.message || "No message available"}${log.last_http_status ? ` (HTTP ${log.last_http_status})` : ""}`
        }));

        const updatedFeeds = feeds.map(f =>
          f.id === feedId ? { ...f, logs: parsedLogs } : f
        );
        setFeeds(updatedFeeds);
      } catch (err) {
        console.error("Failed to fetch logs for feed", feedId);
      }
    }

    setExpandedFeedId(feedId);
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
    feed.url.toLowerCase().includes(searchTerm.toLowerCase())
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

        {error && (
          <div className="text-red-500 font-semibold mb-4">{error}</div>
        )}

        <div className="overflow-x-auto">
          <table className="min-w-full bg-podverse-surface rounded shadow text-podverse-text text-sm">
            <thead className="bg-podverse-accent text-black">
              <tr>
                {["ID", "URL", "Status", "Priority", "Created At", "Updated At", "Details", "Action"].map((header) => (
                  <th key={header} className="text-left px-4 py-2 font-semibold">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filteredFeeds.map((feed) => (
                <React.Fragment key={feed.id}>
                  <tr className="border-t border-podverse-border hover:bg-podverse-highlight transition">
                    <td className="px-4 py-2 font-medium">{feed.id}</td>
                    <td className="px-4 py-2 truncate max-w-xs">{feed.url}</td>
                    <td className="px-4 py-2">
                      <span
                        className={`text-xs px-2 py-1 rounded font-semibold ${
                          feed.feed_flag_status_id === 2
                            ? "bg-yellow-500 text-black"
                            : feed.feed_flag_status_id === 3
                            ? "bg-red-500 text-white"
                            : "bg-green-600 text-white"
                        }`}
                      >
                        {feed.feed_flag_status_id === 2
                          ? "Flagged"
                          : feed.feed_flag_status_id === 3
                          ? "Error"
                          : "Live"}
                      </span>
                    </td>
                    <td className="px-4 py-2">{feed.parsing_priority}</td>
                    <td className="px-4 py-2 text-xs">
                      {new Date(feed.created_at).toLocaleString()}
                    </td>
                    <td className="px-4 py-2 text-xs">
                      {new Date(feed.updated_at).toLocaleString()}
                    </td>
                    <td className="px-4 py-2 text-sm">
                      <button
                        className="text-podverse-accent hover:underline text-xs"
                        onClick={() => toggleExpand(feed.id)}
                      >
                        {expandedFeedId === feed.id ? "Hide Log" : "View Log"}
                      </button>
                    </td>
                    <td className="px-4 py-2">
                      <button
                        className="bg-podverse-primary hover:bg-podverse-accent text-white text-sm px-3 py-1 rounded"
                        onClick={() => alert(`Reparsing feed: ${feed.url}`)}
                      >
                        {feed.feed_flag_status_id === 3 ? "Retry" : "Reparse"}
                      </button>
                    </td>
                  </tr>
                  {expandedFeedId === feed.id && (
                    <tr className="bg-podverse-surface">
                      <td colSpan={8} className="px-6 py-3 border-t border-podverse-border">
                        <div className="flex justify-between items-center mb-2">
                          <h3 className="font-semibold text-sm text-podverse-text">
                            Audit Log
                          </h3>
                          <div className="space-x-2">
                            <button
                              className="text-xs bg-podverse-surface px-2 py-1 rounded hover:bg-podverse-highlight text-podverse-accent"
                              onClick={() => handleCopyLogs(feed.logs ?? [])}
                            >
                              Copy Log
                            </button>
                            <button
                              className="text-xs bg-podverse-surface px-2 py-1 rounded hover:bg-podverse-highlight text-podverse-accent"
                              onClick={() => handleDownloadLogs(feed.logs ?? [], feed.id.toString())}
                            >
                              Download Log
                            </button>
                          </div>
                        </div>
                        <ul className="text-xs text-podverse-muted list-disc ml-5">
                          {(feed.logs ?? []).map((log, i) => (
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
              {filteredFeeds.length === 0 && (
                <tr>
                  <td
                    colSpan={8}
                    className="text-center text-podverse-muted py-4"
                  >
                    No feeds found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
