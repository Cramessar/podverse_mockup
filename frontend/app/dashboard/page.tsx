"use client";
import React from "react";
import Sidebar from "../../components/Sidebar";
import { useRouter } from "next/navigation";
import { BellIcon } from "@heroicons/react/24/outline";

export default function DashboardPage() {
  const router = useRouter();

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

        {/* RSS Feed and Audit Log */}
        <section className="grid grid-cols-2 gap-8">
          {/* Flagged Podcasts */}
          <div className="bg-white rounded-lg p-6 shadow-md flex flex-col h-[600px]">
            <h2 className="text-xl font-semibold mb-4 text-black">Recent Flagged Feeds</h2>
            <div className="flex-1 overflow-y-auto">
              {[...Array(6)].map((_, i) => (
                <div
                  key={i}
                  className={`flex justify-between items-center p-3 rounded mb-3 ${i === 0 ? "bg-blue-100 border border-blue-400" : i % 2 === 0 ? "bg-gray-100" : "bg-gray-200"}`}
                >
                  <div>
                    <p className="font-semibold text-black">Flagged Podcast {i + 1}</p>
                    <p className="text-sm text-gray-500">Podcast name</p>
                  </div>
                  <div className="flex items-center gap-2 ml-auto">
                    {/* Flag status oval, fixed width */}
                    <span
                      className={`flex items-center justify-center w-24 px-0 py-1 rounded-full shadow-md text-sm font-semibold select-none
                        ${i % 2 === 0 ? "bg-yellow-400 text-yellow-900" : "bg-red-500 text-white"}
                      `}
                    >
                      {i % 2 === 0 ? "Flagged" : "Error"}
                    </span>
                    {/* Close button */}
                    <button
                      aria-label="Remove flag"
                      className="ml-2 p-1 rounded-full hover:bg-gray-200 transition flex items-center justify-center shadow"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
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
            </div>
          </div>

          {/* Audit Log */}
          <div className="bg-white rounded-lg p-6 shadow-md flex flex-col h-[600px]">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-black">Audit Log</h2>
              <button className="bg-podverse-accent text-white rounded px-4 py-2 font-semibold shadow hover:bg-blue-600 transition-all">
                Full Audit Log
              </button>
            </div>
            <div className="flex-1 space-y-3 overflow-auto min-w-0">
              {[...Array(6)].map((_, i) => (
                <div
                  key={i}
                  className={`p-3 rounded break-words truncate max-w-full bg-white border border-gray-200 cursor-pointer`}
                >
                  <p className="font-semibold text-black break-words truncate max-w-full">Logged Change</p>
                  <p className="text-sm text-gray-500 break-words truncate max-w-full">Support Team Member</p>
                  <p className="text-xs text-gray-400 break-words truncate max-w-full">5/31/2025 24:00</p>
                </div>
              ))}
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