import React, { useState } from "react";
import Sidebar from "@/components/Sidebar";

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState<"feeds" | "metrics">("metrics");

    return (
    <div className="flex min-h-screen bg-[#121214] text-white">
      <Sidebar />

      {/* Main content */}
      <main className="flex-1 p-8 space-y-8">
        {/* Top bar */}
        <header className="flex justify-between items-center">
          <input
            type="search"
            placeholder="Search"
            className="rounded-full px-5 py-2 w-1/3 bg-[#2a2a35] text-white placeholder-[#7a7a8c] focus:outline-none"
          />
          <div className="flex space-x-4">
            <button
              aria-label="Notifications"
              className="p-2 rounded hover:bg-[#2a2a35] transition"
            >
              🔔
            </button>
            <button
              aria-label="Profile"
              className="p-2 rounded hover:bg-[#2a2a35] transition"
            >
              👤
            </button>
          </div>
        </header>

        {/* Title and tabs */}
        <section>
          <h1 className="text-3xl font-bold mb-1">Welcome to the Admin Panel</h1>
          <p className="text-gray-400 mb-6">Manage your application effortlessly.</p>
          <div className="inline-flex rounded border border-[#2a2a35] overflow-hidden">
            <button
              onClick={() => setActiveTab("feeds")}
              className={`px-6 py-3 font-semibold transition ${activeTab === "feeds"
                  ? "bg-[#3772ff] text-white"
                  : "bg-[#23232e] text-[#7a7a8c] hover:bg-[#2a2a35]"
                }`}
            >
              Manage RSS Feeds
            </button>
            <button
              onClick={() => setActiveTab("metrics")}
              className={`px-6 py-3 font-semibold transition ${activeTab === "metrics"
                  ? "bg-[#3772ff] text-white"
                  : "bg-[#23232e] text-[#7a7a8c] hover:bg-[#2a2a35]"
                }`}
            >
              Detailed Metrics
            </button>
          </div>

          {activeTab === "feeds" && (
            <section className="grid grid-cols-2 gap-8 mt-8">
              {/* Flagged Podcasts */}
              <div className="bg-[#23232e] rounded-lg p-6 max-h-[420px] overflow-y-auto shadow-md">
                <h2 className="text-xl font-semibold mb-4">Flagged Podcasts</h2>
                {[...Array(6)].map((_, i) => (
                  <div
                    key={i}
                    className={`flex justify-between items-center p-3 rounded mb-3 ${i % 2 === 0 ? "bg-[#2a2a35]" : "bg-[#1f1f27]"
                      }`}
                  >
                    <div>
                      <p className="font-semibold">Flagged Podcast {i + 1}</p>
                      <p className="text-sm text-[#7a7a8c]">Podcast description</p>
                    </div>
                    <button
                      className={`px-3 py-1 rounded text-sm ${i % 2 === 0 ? "bg-yellow-500" : "bg-red-600"
                        }`}
                    >
                      Flag
                    </button>
                    <button
                      aria-label="Refresh"
                      className="ml-2 p-1 rounded hover:bg-[#2a2a35] transition"
                    >
                      🔄
                    </button>
                  </div>
                ))}
              </div>

              {/* Audit Log */}
              <div className="bg-[#23232e] rounded-lg p-6 max-h-[420px] overflow-y-auto flex flex-col shadow-md">
                <h2 className="text-xl font-semibold mb-4">Audit Log</h2>
                <div className="flex-1 overflow-y-auto space-y-3">
                  {[...Array(6)].map((_, i) => (
                    <div
                      key={i}
                      className={`p-3 rounded ${i % 2 === 0 ? "bg-[#2a2a35]" : "bg-[#1f1f27]"
                        }`}
                    >
                      <p className="font-semibold">Logged Change</p>
                      <p className="text-sm text-[#7a7a8c]">Support Team Member</p>
                      <p className="text-xs text-[#52525b]">5/31/2025 24:00</p>
                    </div>
                  ))}
                </div>
                <div className="mt-6 flex space-x-4">
                  <button className="flex-1 border border-[#2a2a35] rounded py-3 hover:bg-[#2a2a35] transition">
                    Reparse Feed
                  </button>
                  <button className="flex-1 bg-[#3772ff] text-white rounded py-3">
                    Full Audit Log
                  </button>
                </div>
              </div>
            </section>
          )}

          {activeTab === "metrics" && (
            <section className="mt-8">
              {/* Metrics header */}
              <div className="flex justify-between items-center mb-6">
                <div>
                  <h2 className="text-xl font-semibold mb-1">Podverse</h2>
                  <p className="text-sm text-[#7a7a8c] mb-4">
                    Overview of critical performance indicators.
                  </p>
                </div>
                <select
                  className="bg-[#23232e] rounded border border-[#2a2a35] text-white px-4 py-2 focus:outline-none"
                  defaultValue="Monthly"
                >
                  <option>Monthly</option>
                  <option>Weekly</option>
                  <option>Yearly</option>
                </select>
              </div>

              <div className="flex space-x-6 mb-8">
                <button className="border border-[#2a2a35] rounded px-6 py-3 hover:bg-[#2a2a35] transition">
                  View Details
                </button>
                <button className="bg-[#3772ff] text-white rounded px-6 py-3">
                  Download Report
                </button>
              </div>

              <div className="grid grid-cols-4 gap-6 mb-8">
                {[
                  { title: "Podcasts", value: "1,250", change: "+5%" },
                  { title: "New podcasts", value: "320", change: "+10%" },
                  { title: "Views", value: "$12,500", change: "+15%" },
                  { title: "Feedback Score", value: "4.8", change: "No Change" },
                ].map(({ title, value, change }) => (
                  <div
                    key={title}
                    className="bg-[#23232e] rounded p-6 flex flex-col justify-between"
                  >
                    <p className="text-[#7a7a8c]">{title}</p>
                    <h3 className="text-3xl font-semibold">{value}</h3>
                    <p className="text-[#52525b]">{change}</p>
                  </div>
                ))}
              </div>

              {/* Chart placeholder */}
              <div className="bg-[#23232e] rounded p-6 shadow-md">
                <h3 className="text-xl font-semibold mb-4">Monthly Sales</h3>
                <div className="h-48 bg-[#1f1f27] flex items-center justify-center text-[#7a7a8c]">
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
