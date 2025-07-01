"use client";
import React from "react";
import Sidebar from "../../components/Sidebar";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { BellIcon } from "@heroicons/react/24/outline";

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<"feeds" | "metrics">("metrics");
  const router = useRouter();

  const handleContinue = () => {
    router.push("/auth/logout");
  };

  return (
    <div className="flex min-h-screen bg-podverse-background text-podverse-text">
      <Sidebar />

      <main className="flex-1 p-8 space-y-8">
        {/* Top Bar */}
        <header className="flex justify-between items-center">
          <input
            type="search"
            placeholder="Search"
            className="rounded-full px-5 py-2 w-1/3 bg-podverse-surface text-podverse-text placeholder-podverse-muted focus:outline-none"
          />
          <div className="flex space-x-4">
            <button
              aria-label="Notifications"
              className="p-2 rounded hover:bg-podverse-surface transition"
            >
              <BellIcon className="w-6 h-6 text-black" />
            </button>
            <button
              onClick={handleContinue}
              className="p-2 rounded hover:bg-podverse-surface transition"
            >
              Logout
            </button>
          </div>
        </header>

        {/* Title & Tabs */}
        <section>
          <h1 className="text-3xl font-bold mb-1">Welcome to the Admin Panel</h1>
          <p className="text-podverse-muted mb-6">Manage your application effortlessly.</p>

          <div className="inline-flex rounded border border-podverse-border overflow-hidden">
            <button
              onClick={() => setActiveTab("feeds")}
              className={`px-6 py-3 font-semibold transition ${
                activeTab === "feeds"
                  ? "bg-podverse-primary text-white"
                  : "bg-podverse-surface text-podverse-muted hover:bg-podverse-border"
              }`}
            >
              Manage RSS Feeds
            </button>
            <button
              onClick={() => setActiveTab("metrics")}
              className={`px-6 py-3 font-semibold transition ${
                activeTab === "metrics"
                  ? "bg-podverse-primary text-white"
                  : "bg-podverse-surface text-podverse-muted hover:bg-podverse-border"
              }`}
            >
              Detailed Metrics
            </button>
          </div>

          {/* FEEDS TAB */}
          {activeTab === "feeds" && (
            <section className="grid grid-cols-2 gap-8 mt-8">
              {/* Flagged Podcasts */}
              <div className="bg-podverse-surface rounded-lg p-6 max-h-[420px] overflow-y-auto shadow-md">
                <h2 className="text-xl font-semibold mb-4">Flagged Podcasts</h2>
                {[...Array(6)].map((_, i) => (
                  <div
                    key={i}
                    className={`flex justify-between items-center p-3 rounded mb-3 ${
                      i % 2 === 0 ? "bg-podverse-background" : "bg-podverse-border"
                    }`}
                  >
                    <div>
                      <p className="font-semibold">Flagged Podcast {i + 1}</p>
                      <p className="text-sm text-podverse-muted">Podcast description</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button
                        className={`px-3 py-1 rounded text-sm ${
                          i % 2 === 0 ? "bg-podverse-warning" : "bg-podverse-error"
                        } text-black`}
                      >
                        Flag
                      </button>
                      <button
                        aria-label="Refresh"
                        className="p-1 rounded hover:bg-podverse-border transition"
                      >
                        🔄
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              {/* Audit Log */}
              <div className="bg-podverse-surface rounded-lg p-6 max-h-[420px] overflow-y-auto flex flex-col shadow-md">
                <h2 className="text-xl font-semibold mb-4">Audit Log</h2>
                <div className="flex-1 space-y-3">
                  {[...Array(6)].map((_, i) => (
                    <div
                      key={i}
                      className={`p-3 rounded ${
                        i % 2 === 0 ? "bg-podverse-background" : "bg-podverse-border"
                      }`}
                    >
                      <p className="font-semibold">Logged Change</p>
                      <p className="text-sm text-podverse-muted">Support Team Member</p>
                      <p className="text-xs text-podverse-border">5/31/2025 24:00</p>
                    </div>
                  ))}
                </div>
                <div className="mt-6 flex space-x-4">
                  <button className="flex-1 border border-podverse-border rounded py-3 hover:bg-podverse-border transition">
                    Reparse Feed
                  </button>
                  <button className="flex-1 bg-podverse-primary text-white rounded py-3">
                    Full Audit Log
                  </button>
                </div>
              </div>
            </section>
          )}

          {/* METRICS TAB */}
          {activeTab === "metrics" && (
            <section className="mt-8">
              <div className="flex justify-between items-center mb-6">
                <div>
                  <h2 className="text-xl font-semibold mb-1">Podverse</h2>
                  <p className="text-sm text-podverse-muted">
                    Overview of critical performance indicators.
                  </p>
                </div>
                <select
                  className="bg-podverse-surface rounded border border-podverse-border text-podverse-text px-4 py-2 focus:outline-none"
                  defaultValue="Monthly"
                >
                  <option>Monthly</option>
                  <option>Weekly</option>
                  <option>Yearly</option>
                </select>
              </div>

              <div className="flex space-x-6 mb-8">
                <button className="border border-podverse-border rounded px-6 py-3 hover:bg-podverse-border transition">
                  View Details
                </button>
                <button className="bg-podverse-primary text-white rounded px-6 py-3">
                  Download Report
                </button>
              </div>

              <div className="grid grid-cols-4 gap-6 mb-8">
                {[
                  { title: "Podcasts", value: "1,250", change: "+5%" },
                  { title: "New Podcasts", value: "320", change: "+10%" },
                  { title: "Views", value: "12,500", change: "+15%" },
                  { title: "Feedback Score", value: "4.8", change: "No Change" },
                ].map(({ title, value, change }) => (
                  <div
                    key={title}
                    className="bg-podverse-surface rounded p-6 flex flex-col justify-between"
                  >
                    <p className="text-podverse-muted">{title}</p>
                    <h3 className="text-3xl font-semibold">{value}</h3>
                    <p className="text-podverse-border">{change}</p>
                  </div>
                ))}
              </div>

              <div className="bg-podverse-surface rounded p-6 shadow-md">
                <h3 className="text-xl font-semibold mb-4">Monthly Sales</h3>
                <div className="h-48 bg-podverse-background flex items-center justify-center text-podverse-muted">
                  Chart goes here
                </div>
              </div>
            </section>
          )}
        </section>
      </main>
    </div>
  );
}