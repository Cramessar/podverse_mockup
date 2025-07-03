"use client";
import React, { useState, useEffect } from "react";
import Sidebar from "../../components/Sidebar";
import {Feed, FeedLog, RecentLog} from "@/types/feed";


export default function AdminFeedsPage() {
  const [feeds, setFeeds] = useState<Feed[]>([]);
  const [expandedFeedId, setExpandedFeedId] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [logLoading, setLogLoading] = useState(false);
  const [logError, setLogError] = useState<string | null>(null);

  //updated with new API
  useEffect(() => {
  const loadFeeds = async () => {
    try {
      const response = await fetch("/api/feeds");
      if (!response.ok) throw new Error("Failed to load feeds");
      const data = await response.json();
      setFeeds(data); // assuming your API returns an array of feeds
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
    setLogError(null);
    return;
  }

  setLogLoading(true);
  setLogError(null);

  try {
    const response = await fetch(`/api/feeds/${feedId}`);
    if (!response.ok) throw new Error("Failed to fetch feed details");
    const feedData = await response.json();

    const updatedFeeds = feeds.map(f =>
      f.id === feedId ? { ...f, logs: feedData.recent_logs || [] } : f
    );
    setFeeds(updatedFeeds);
  } catch (err) {
    setLogError("FAILED to load");
  }

  setLogLoading(false);
  setExpandedFeedId(feedId);
};

  const handleCopyLogs = (logs: FeedLog[]) => {
    const text = logs.map((log) => `${log.created_at}: ${log.message}`).join("\n");
    navigator.clipboard.writeText(text);
    alert("Logs copied to clipboard!");
  };

  const handleDownloadLogs = (logs: FeedLog[], title: string) => {
    const text = logs.map((log) => `${log.created_at}: ${log.message}`).join("\n");
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
        <h1 className="text-2xl font-bold mb-4 text-podverse-text">
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
      <div>
        <h3 className="font-semibold text-sm text-podverse-text mb-2">
          Audit Log
        </h3>
        <div className="flex flex-col gap-2 mb-4 max-h-60 overflow-y-auto bg-gray-50 rounded p-2">
          {logLoading ? (
            <div className="text-podverse-muted">Loading logs...</div>
          ) : logError ? (
            <div className="text-red-500">{logError}</div>
          ) : !feed.recent_logs || feed.recent_logs.length === 0 ? (
            <div className="text-podverse-muted">No logs available</div>
          ) : (
            feed.recent_logs.map((log, i) => (
              <div key={i} className="text-xs border-b border-gray-200 py-2">
                <div>
                  <strong>Time:</strong>{" "}
                  {new Date(
                    log.last_finished_parse_time ||
                    log.last_good_http_status_time ||
                    ""
                  ).toLocaleString()}
                </div>
                <div>
                  <strong>Status:</strong>{" "}
                  <span className={log.parse_errors === 0 ? "text-green-600 font-semibold" : "text-red-600 font-semibold"}>
                    {log.parse_errors === 0 ? "Live" : "Error"}
                  </span>
                </div>
                  <div>
                    <strong>Message:</strong> {log.message}
                  </div>
              </div>
            ))
          )}
        </div>
        <div className="space-x-2">
          <button
            className="text-xs bg-podverse-surface px-2 py-1 rounded hover:bg-podverse-highlight text-podverse-accent"
            onClick={() => handleCopyLogs(feed.logs ?? [])}
            disabled={!feed.logs || feed.logs.length === 0}
          >
            Copy Log
          </button>
          <button
            className="text-xs bg-podverse-surface px-2 py-1 rounded hover:bg-podverse-highlight text-podverse-accent"
            onClick={() => handleDownloadLogs(feed.logs ?? [], feed.id.toString())}
            disabled={!feed.logs || feed.logs.length === 0}
          >
            Download Log
          </button>
        </div>
      </div>
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
