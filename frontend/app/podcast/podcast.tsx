import React from "react";
import Sidebar from "../../components/Sidebar";

export default function AdminPodcast() {
  return (
    <div className="flex min-h-screen bg-[#121214] text-white">
      <Sidebar />

      <main className="flex-1 p-8 space-y-8">
        <header className="bg-[#2a2a35] p-8 rounded mb-6">
          <h1 className="text-3xl font-bold">Podcast Name</h1>
          <p className="text-gray-400">Your go-to source for insightful discussions and engaging stories.</p>
          <button className="mt-4 bg-black text-white px-4 py-2 rounded hover:bg-[#3772ff] transition">
            Edit Podcast Info
          </button>
        </header>

        <section className="grid grid-cols-2 gap-8">
          {/* Podcast Metrics & Info */}
          <div className="bg-[#23232e] rounded p-6 shadow">
            <h2 className="text-xl font-semibold mb-4">Podcast Metrics & Info</h2>
            <button className="mb-4 bg-[#3772ff] text-white px-4 py-2 rounded hover:bg-[#1c57d1] transition">
              Download Report
            </button>
            <div className="grid grid-cols-2 gap-6 text-gray-300 mb-6">
              <div>
                <p>Total Episodes</p>
                <h3 className="text-2xl font-semibold">15</h3>
                <p className="text-sm text-gray-500">+2</p>
              </div>
              <div>
                <p>Average Listeners</p>
                <h3 className="text-2xl font-semibold">350</h3>
                <p className="text-sm text-gray-500">+50</p>
              </div>
              <div>
                <p>Total Downloads</p>
                <h3 className="text-2xl font-semibold">5000</h3>
                <p className="text-sm text-gray-500">+800</p>
              </div>
              <div>
                <p>Listener Ratings</p>
                <h3 className="text-2xl font-semibold">4.8</h3>
              </div>
            </div>

            {/* Monthly Downloads Chart placeholder */}
            <div className="bg-[#1f1f27] rounded p-4 text-gray-500 h-48 flex items-center justify-center">
              Monthly Downloads Chart Here
            </div>
          </div>

          {/* Audit Log */}
          <div className="bg-[#23232e] rounded p-6 shadow flex flex-col">
            <h2 className="text-xl font-semibold mb-4">Audit Log</h2>
            <div className="flex-1 overflow-y-auto space-y-3 text-gray-300">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className={`p-3 rounded ${i % 2 === 0 ? "bg-[#2a2a35]" : "bg-[#1f1f27]"}`}
                >
                  <p className="font-semibold">Logged Change</p>
                  <p className="text-sm text-[#7a7a8c]">Support Team Member</p>
                  <p className="text-xs text-[#52525b]">5/31/2025 24:00</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Listener Engagement */}
        <section>
          <h2 className="text-2xl font-bold mb-1">Listener Engagement</h2>
          <p className="text-gray-400 mb-6">Engagement stats for the last quarter.</p>

          <div className="grid grid-cols-2 gap-8">
            <div className="bg-[#23232e] rounded p-6 shadow text-gray-300 h-64 flex items-center justify-center">
              Listener Growth Chart Here
            </div>
            <div className="bg-[#23232e] rounded p-6 shadow text-gray-300 h-64 flex items-center justify-center">
              Age Distribution Chart Here
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
