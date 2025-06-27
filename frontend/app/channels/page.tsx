"use client";

import React from "react";
import Sidebar from "@/components/Sidebar";
import { useRouter } from "next/navigation";
import ChannelTable from "./ChannelTable";

export default function ChannelsPage() {
  const router = useRouter();

  const handleLogout = () => {
    router.push("/auth/logout");
  };

  return (
    <div className="flex min-h-screen bg-podverse-background text-black">
      <Sidebar />

      {/* Main Content */}
      <main className="flex-1 p-8 space-y-8">
        {/* Topbar */}
        <header className="flex justify-between items-center">
          <input
            type="search"
            placeholder="Search Channels"
            className="rounded-full px-5 py-2 w-1/3 bg-[#2a2a35] text-black placeholder-[#7a7a8c] focus:outline-none"
          />
          <div className="flex space-x-4">
            <button
              aria-label="Notifications"
              className="p-2 rounded hover:bg-[#2a2a35] transition"
            >
              🔔
            </button>
            <button
              onClick={handleLogout}
              aria-label="Logout"
              className="p-2 rounded hover:bg-[#2a2a35] transition"
            >
              Logout
            </button>
          </div>
        </header>

        {/* Channel Management */}
        <section>
          <h1 className="text-3xl font-bold text-podverse-secondary mb-2">
            Channel Management
          </h1>
          <p className="text-black mb-6">
            Manage your podcast channels below. Sort, review, or remove entries as needed.
          </p>

          <div className="bg-white rounded-lg p-6 shadow-md">
            <ChannelTable />
          </div>
        </section>
      </main>
    </div>
  );
}
