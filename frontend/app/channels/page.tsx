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
    <div className="flex min-h-screen bg-podverse-background text-podverse-text">
      <Sidebar />

      {/* Main Content */}
      <main className="flex-1 p-8 space-y-8">
        {/* Topbar */}
        <header className="flex justify-end items-center">
          <div className="flex space-x-4">
            <button
              aria-label="Notifications"
              className="p-2 rounded hover:bg-podverse-border transition"
            >
              🔔
            </button>
            <button
              onClick={handleLogout}
              aria-label="Logout"
              className="p-2 rounded hover:bg-podverse-border transition"
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
          <p className="text-podverse-muted mb-6">
            Manage your podcast channels below. Sort, review, or remove entries as needed.
          </p>

          <div className="bg-podverse-surface rounded-lg p-6 shadow-md">
            <ChannelTable />
          </div>
        </section>
      </main>
    </div>
  );
}
