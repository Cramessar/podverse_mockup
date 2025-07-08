"use client";
import React from "react";
import Sidebar from "../../components/Sidebar";

export default function AdminPodcast() {
  return (
    <div className="flex min-h-screen bg-podverse-background text-podverse-text">
      <Sidebar />

      <main className="flex-1 p-8 space-y-8">
        {/* Podcast Header */}
        <header className="bg-podverse-surface p-8 rounded mb-6">
          <h1 className="text-3xl font-bold">Podcast Name</h1>
          <p className="text-podverse-muted">
            Your go-to source for insightful discussions and engaging stories.
          </p>
          <button className="mt-4 bg-podverse-primary text-white px-4 py-2 rounded hover:bg-podverse-accent transition">
            Edit Podcast Info
          </button>
        </header>

        {/* Metrics + Audit Log */}
        <section className="grid grid-cols-2 gap-8">
          {/* Podcast Metrics */}
          <div className="bg-podverse-surface rounded p-6 shadow">
            <h2 className="text-xl font-semibold mb-4">Podcast Metrics & Info</h2>
            <button className="mb-4 bg-podverse-primary text-white px-4 py-2 rounded hover:bg-podverse-accent transition">
              Download Report
            </button>

            <div className="grid grid-cols-2 gap-6 text-podverse-muted mb-6">
              {[
                { label: "Total Episodes", value: "15", change: "+2" },
                { label: "Average Listeners", value: "350", change: "+50" },
                { label: "Total Downloads", value: "5000", change: "+800" },
                { label: "Listener Ratings", value: "4.8", change: null },
              ].map(({ label, value, change }) => (
                <div key={label}>
                  <p>{label}</p>
                  <h3 className="text-2xl font-semibold text-podverse-text">{value}</h3>
                  {change && (
                    <p className="text-sm text-podverse-border">{change}</p>
                  )}
                </div>
              ))}
            </div>

            {/* Chart Placeholder */}
            <div className="bg-podverse-background rounded p-4 text-podverse-muted h-48 flex items-center justify-center">
              Monthly Downloads Chart Here
            </div>
          </div>

          {/* Audit Log */}
          <div className="bg-podverse-surface rounded p-6 shadow flex flex-col">
            <h2 className="text-xl font-semibold mb-4">Audit Log</h2>
            <div className="flex-1 overflow-y-auto space-y-3">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className={`p-3 rounded ${
                    i % 2 === 0 ? "bg-podverse-background" : "bg-podverse-border"
                  }`}
                >
                  <p className="font-semibold text-podverse-text">Logged Change</p>
                  <p className="text-sm text-podverse-muted">Support Team Member</p>
                  <p className="text-xs text-podverse-border">5/31/2025 24:00</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Listener Engagement */}
        <section>
          <h2 className="text-2xl font-bold mb-1">Listener Engagement</h2>
          <p className="text-podverse-muted mb-6">
            Engagement stats for the last quarter.
          </p>

          <div className="grid grid-cols-2 gap-8">
            <div className="bg-podverse-surface rounded p-6 shadow text-podverse-muted h-64 flex items-center justify-center">
              Listener Growth Chart Here
            </div>
            <div className="bg-podverse-surface rounded p-6 shadow text-podverse-muted h-64 flex items-center justify-center">
              Age Distribution Chart Here
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
