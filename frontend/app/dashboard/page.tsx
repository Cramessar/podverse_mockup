"use client";
import React, { useState, useEffect } from "react";
import Sidebar from "../../components/Sidebar";
import { useRouter } from "next/navigation";
import { BellIcon } from "@heroicons/react/24/outline";
import { Feed, RecentLog } from "@/types/feed";

export default function DashboardPage() {
  const router = useRouter();
  const [feeds, setFeeds] = useState<Feed[]>([]);
  const [error, setError] = useState<string>("");
  const [selectedFeedId, setSelectedFeedId] = useState<number | null>(null);
  const [selectedFeedLogs, setSelectedFeedLogs] = useState<RecentLog[]>([]);
  const [logLoading, setLogLoading] = useState(false);
  const [logError, setLogError] = useState<string | null>(null);

  // Fetch feeds on mount
  useEffect(() => {
    const fetchFeeds = async () => {
      try {
        const response = await fetch("/api/feeds?limit=1000");
        if (!response.ok) throw new Error("Failed to load feeds");
        const data = await response.json();
        setFeeds(data);
      } catch (error) {
        setError("Failed to load feeds");
      }
    };
    fetchFeeds();
  }, []);

  // Show only most recent flagged or error feeds
  const handleRecentFlagged = (feeds: Feed[]) => {
    return feeds
      .filter(feed => feed.feed_flag_status_id === 2 || feed.feed_flag_status_id === 3)
      .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
      .slice(0, 6);
  };

  // Fetch logs for selected feed
  useEffect(() => {
    if (selectedFeedId == null) return;
    setLogLoading(true);
    setLogError(null);
    fetch(`/api/feeds/${selectedFeedId}`)
      .then(res => res.json())
      .then(data => setSelectedFeedLogs(data.recent_logs || []))
      .catch(() => setLogError("Failed to load logs"))
      .finally(() => setLogLoading(false));
  }, [selectedFeedId]);

  // Set default selected feed to first flagged/error feed
  useEffect(() => {
    if (selectedFeedId == null && feeds.length > 0) {
      const flagged = handleRecentFlagged(feeds);
      if (flagged.length > 0) {
        setSelectedFeedId(flagged[0].id);
      }
    }
  }, [feeds, selectedFeedId]);

  // Logout handler
  const handleLogout = () => {
    router.push("/auth/logout");
  };

  return (
    <div className="flex min-h-screen bg-gray-100 text-black">
      <Sidebar />

      <main className="flex-1  space-y-8">
        {/* Top bar */}
        <header className="flex justify-between p-2 pr-4 bg-podverse-surface items-center mb-8">
          <div className="flex-1 flex justify-center">
            <input
              type="search"
              placeholder="Search"
              className="rounded-full px-5 py-2 w-1/2 bg-white text-black placeholder-gray-400 focus:outline-none border border-gray-300"
            />
          </div>
          <div className="flex items-center space-x-4 ml-4">
            <button
              aria-label="Notifications"
              className="p-2 rounded hover:bg-gray-200 transition"
            >
              <BellIcon className="w-6 h-6 text-black" />
            </button>
            <button
              onClick={handleLogout}
              className="py-2 px-6 bg-podverse-accent hover:bg-podverse-accent text-white rounded-md transition"
            >
              Logout
            </button>
          </div>
        </header>

        {/* Show feed fetch error if any */}
        {error && (
          <div className="text-red-500 font-semibold mb-4">{error}</div>
        )}

        {/* RSS Feed and Audit Log */}
        <section className="grid grid-cols-2 gap-8">
          {/* Flagged Podcasts */}
          <div className="bg-white rounded-lg p-6 shadow-md flex flex-col h-[600px]">
            <h2 className="text-xl font-semibold mb-4 text-black">Recent Flagged Feeds</h2>
            <div className="flex-1 overflow-y-auto">
              {handleRecentFlagged(feeds).map((feed) => (
                <div
                  key={feed.id}
                  tabIndex={0}
                  role="button"
                  onClick={() => setSelectedFeedId(feed.id)}
                  className={`flex justify-between items-center p-3 rounded mb-3 cursor-pointer ${
                    feed.id === selectedFeedId
                      ? "bg-blue-100 border border-blue-400"
                      : feed.feed_flag_status_id === 2
                      ? "bg-yellow-100"
                      : "bg-red-100"
                  }`}
                >
                  <div>
                    <p className="font-semibold text-black">{feed.url}</p>
                    <p className="text-sm text-gray-500">Feed ID: {feed.id}</p>
                  </div>
                  <div className="flex items-center gap-2 ml-auto">
                    {/* Flag status oval, fixed width */}
                    <span
                      className={`flex items-center justify-center w-24 px-0 py-1 rounded-full shadow-md text-sm font-semibold select-none
                        ${
                          feed.feed_flag_status_id === 2
                            ? "bg-yellow-400 text-yellow-900"
                            : "bg-red-500 text-white"
                        }
                      `}
                    >
                      {feed.feed_flag_status_id === 2 ? "Flagged" : "Error"}
                    </span>
                    {/* Reparse button with Heroicon */}
                    <button
                      aria-label="Reparse"
                      className="ml-2 p-1 rounded-full bg-gradient-to-r from-podverse-accent to-blue-500 text-white shadow-md hover:from-blue-500 hover:to-podverse-accent transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 flex items-center justify-center"
                    >
                      {/* Heroicons ArrowPath (refresh) icon */}
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-5 h-5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12a7.5 7.5 0 0113.5-4.5M19.5 12a7.5 7.5 0 01-13.5 4.5m0 0V15m0 1.5H6m12-1.5v-1.5m0 0H18" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
              {handleRecentFlagged(feeds).length === 0 && (
                <div className="text-center text-gray-400 py-8">No flagged feeds found.</div>
              )}
            </div>
          </div>

          {/* Audit Log Table */}
          <div className="bg-white rounded-lg p-6 shadow-md flex flex-col h-[600px]">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-black">Audit Log</h2>
            </div>
            <div className="flex-1 space-y-3 overflow-auto min-w-0">
              {logLoading ? (
                <div className="text-podverse-muted">Loading logs...</div>
              ) : logError ? (
                <div className="text-red-500">{logError}</div>
              ) : selectedFeedLogs.length === 0 ? (
                <div className="text-podverse-muted">No logs available</div>
              ) : (
                selectedFeedLogs.map((log, i) => (
                  <div key={i} className="p-3 rounded bg-white border border-gray-200">
                    <p className="font-semibold text-black break-words">{log.message}</p>
                    <p className="text-xs text-gray-400">{new Date(
                      log.last_finished_parse_time ||
                      log.last_good_http_status_time ||
                      ""
                    ).toLocaleString()}</p>
                    <span className={log.parse_errors === 0 ? "text-green-600 font-semibold" : "text-red-600 font-semibold"}>
                      {log.parse_errors === 0 ? "Live" : "Error"}
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>
        </section>

        {/* Stats at the bottom */}
        <section className="mt-8">
          <div className="grid grid-cols-4 gap-6 mb-8">
            {[
              { title: "Podcasts", value: "1,250", change: "+5%" },
              { title: "New podcasts", value: "320", change: "+10%" },
              { title: "Views", value: "$12,500", change: "+15%" },
              { title: "Feedback Score", value: "4.8", change: "No Change" },
            ].map(({ title, value, change }) => (
              <div
                key={title}
                className="bg-white rounded p-6 flex flex-col justify-between"
              >
                <p className="text-gray-500">{title}</p>
                <h3 className="text-3xl font-semibold text-black">{value}</h3>
                <p className="text-gray-400">{change}</p>
              </div>
            ))}
          </div>
          {/* Chart placeholder */}
          <div className="bg-white rounded p-6 shadow-md">
            <h3 className="text-xl font-semibold mb-4 text-black">Monthly Sales</h3>
            <div className="h-48 bg-gray-100 flex items-center justify-center text-gray-400">
              Chart goes here
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}