"use client";

import { useEffect, useState } from "react";

export interface Channel {
  id: number;
  id_text: string;
  podcast_index_id: number;
  title?: string | null;
}

export default function ChannelTable() {
  const [channels, setChannels] = useState<Channel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [sortKey, setSortKey] = useState<keyof Channel>("id");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  useEffect(() => {
    fetch("http://localhost:8000/admin/channels")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch channels");
        return res.json();
      })
      .then((data) => setChannels(data.data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const sortedChannels = [...channels].sort((a, b) => {
    const aVal = a[sortKey];
    const bVal = b[sortKey];
    if (aVal == null || bVal == null) return 0;
    if (sortOrder === "asc") return aVal > bVal ? 1 : -1;
    return aVal < bVal ? 1 : -1;
  });

  const toggleSort = (key: keyof Channel) => {
    if (sortKey === key) {
      setSortOrder((prev) => (prev === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortOrder("asc");
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this channel?")) return;
    try {
      const res = await fetch(`http://localhost:8000/admin/channels/${id}`, {
        method: "DELETE",
      });
      if (res.status === 204) {
        setChannels((prev) => prev.filter((ch) => ch.id !== id));
      } else {
        throw new Error("Delete failed");
      }
    } catch (err) {
      alert("Error deleting channel");
    }
  };

  if (loading)
    return (
      <p className="text-[#7a7a8c] text-lg font-medium p-6">Loading channels...</p>
    );

  if (error)
    return (
      <p className="text-red-500 bg-red-100 border border-red-300 rounded p-4 m-4">
        Error: {error}
      </p>
    );

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-podverse-secondary">
        Channels Overview
      </h2>
      <table className="w-full bg-white border border-gray-300 shadow rounded text-sm">
        <thead className="bg-podverse-highlight text-black font-semibold text-left">
          <tr>
            <th
              onClick={() => toggleSort("id")}
              className="p-3 border-b cursor-pointer hover:text-podverse-secondary transition"
            >
              ID
            </th>
            <th
              onClick={() => toggleSort("id_text")}
              className="p-3 border-b cursor-pointer hover:text-podverse-secondary transition"
            >
              Identifier
            </th>
            <th
              onClick={() => toggleSort("podcast_index_id")}
              className="p-3 border-b cursor-pointer hover:text-podverse-secondary transition"
            >
              Podcast Index ID
            </th>
            <th className="p-3 border-b">Actions</th>
          </tr>
        </thead>
        <tbody>
          {sortedChannels.map((channel, index) => (
            <tr
              key={channel.id}
              className={`transition ${
                index % 2 === 0 ? "bg-white" : "bg-[#fdf8ee]"
              } hover:bg-podverse-cream`}
            >
              <td className="p-3 border-b">{channel.id}</td>
              <td className="p-3 border-b">{channel.id_text || "n/a"}</td>
              <td className="p-3 border-b">{channel.podcast_index_id || "n/a"}</td>
              <td className="p-3 border-b">
                <button
                  onClick={() => handleDelete(channel.id)}
                  className="text-red-600 hover:text-red-800 hover:underline transition"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
