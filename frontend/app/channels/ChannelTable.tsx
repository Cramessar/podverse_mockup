"use client";

import { useEffect, useState } from "react";
import ConfirmationModal from "@/components/ConfirmModal";

export interface Channel {
  id: number;
  id_text: string;
  title: string | null;
  sortable_title: string | null;
  podcast_index_id: number;
  feed_id: number;
  medium_id: number | null;
  podcast_guid: string | null;
  slug: string | null;
  has_podcast_index_value: boolean;
  has_value_time_splits: boolean;
}

export default function ChannelTable() {
  const [channels, setChannels] = useState<Channel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [sortKey, setSortKey] = useState<keyof Channel>("id");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");
  const [currentPage, setCurrentPage] = useState(1);
  const [rowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState("");
  const [editChannel, setEditChannel] = useState<Partial<Channel> | null>(null);
  const [showConfirm, setShowConfirm] = useState(false);

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

  const filteredChannels = channels.filter((ch) =>
    [ch.title, ch.slug, ch.id_text].join(" ").toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedChannels = [...filteredChannels].sort((a, b) => {
    const aVal = a[sortKey];
    const bVal = b[sortKey];
    if (aVal == null || bVal == null) return 0;
    return sortOrder === "asc" ? (aVal > bVal ? 1 : -1) : (aVal < bVal ? 1 : -1);
  });

  const paginatedChannels = sortedChannels.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );

  const totalPages = Math.ceil(sortedChannels.length / rowsPerPage);

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
    } catch {
      alert("Error deleting channel");
    }
  };

  const handleInlineEdit = (id: number, updates: Partial<Channel>) => {
    const original = channels.find((ch) => ch.id === id);
    if (!original) return;

    const hasChanges = Object.entries(updates).some(
      ([key, value]) => original[key as keyof Channel] !== value
    );

    if (!hasChanges) return;

    setEditChannel({ ...original, ...updates });
    setShowConfirm(true);
  };

  const handleConfirmUpdate = async () => {
    if (!editChannel?.id) return;

    try {
      const res = await fetch(`http://localhost:8000/admin/channels/${editChannel.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editChannel),
      });

      if (!res.ok) throw new Error("Update failed");

      const updated = await res.json();

      setChannels((prev) =>
        prev.map((ch) => (ch.id === updated.id ? updated : ch))
      );
    } catch (err) {
      alert("Error updating channel");
    } finally {
      setShowConfirm(false);
      setEditChannel(null);
    }
  };

  if (loading) return <p className="p-6 text-podverse-muted">Loading channels...</p>;

  if (error)
    return <p className="text-red-500 bg-red-100 p-4 rounded border">{error}</p>;

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-podverse-secondary">Channels Overview</h2>

      <input
        type="text"
        placeholder="Search by title, slug, or identifier"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="w-full p-2 border border-podverse-dark rounded bg-white text-black"
      />

      <table className="w-full bg-white border border-gray-300 shadow rounded text-sm">
        <thead className="bg-podverse-highlight text-black font-semibold text-left">
          <tr>
            <th className="p-3 border-b cursor-pointer" onClick={() => toggleSort("id")}>ID</th>
            <th className="p-3 border-b cursor-pointer" onClick={() => toggleSort("id_text")}>Identifier</th>
            <th className="p-3 border-b">Title</th>
            <th className="p-3 border-b">Slug</th>
            <th className="p-3 border-b">Podcast Index ID</th>
            <th className="p-3 border-b">Feed ID</th>
            <th className="p-3 border-b">Medium ID</th>
            <th className="p-3 border-b">Actions</th>
          </tr>
        </thead>
        <tbody>
          {paginatedChannels.map((ch, i) => (
            <tr
              key={ch.id}
              className={`${
                i % 2 === 0 ? "bg-white" : "bg-podverse-cream"
              } hover:bg-podverse-highlight`}
            >
              <td className="p-3 border-b">{ch.id}</td>
              <td className="p-3 border-b">{ch.id_text}</td>
              <td className="p-3 border-b">
                <input
                  className="w-full bg-transparent"
                  defaultValue={ch.title || ""}
                  onBlur={(e) => handleInlineEdit(ch.id, { title: e.target.value })}
                />
              </td>
              <td className="p-3 border-b">
                <input
                  className="w-full bg-transparent"
                  defaultValue={ch.slug || ""}
                  onBlur={(e) => handleInlineEdit(ch.id, { slug: e.target.value })}
                />
              </td>
              <td className="p-3 border-b">
                <input
                  className="w-full bg-transparent"
                  defaultValue={ch.podcast_index_id.toString()}
                  onBlur={(e) => handleInlineEdit(ch.id, { podcast_index_id: Number(e.target.value) })}
                />
              </td>
              <td className="p-3 border-b">
                <input
                  className="w-full bg-transparent"
                  defaultValue={ch.feed_id.toString()}
                  onBlur={(e) => handleInlineEdit(ch.id, { feed_id: Number(e.target.value) })}
                />
              </td>
              <td className="p-3 border-b">
                <input
                  className="w-full bg-transparent"
                  defaultValue={ch.medium_id?.toString() ?? ""}
                  onBlur={(e) => handleInlineEdit(ch.id, { medium_id: Number(e.target.value) || null })}
                />
              </td>
              <td className="p-3 border-b space-x-2">
                <button onClick={() => handleDelete(ch.id)} className="text-podverse-danger hover:underline">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="flex justify-between items-center mt-4">
        <button
          disabled={currentPage === 1}
          onClick={() => setCurrentPage((prev) => prev - 1)}
          className="px-4 py-2 border border-podverse-dark rounded disabled:opacity-50"
        >
          Previous
        </button>
        <span>Page {currentPage} of {totalPages}</span>
        <button
          disabled={currentPage === totalPages}
          onClick={() => setCurrentPage((prev) => prev + 1)}
          className="px-4 py-2 border border-podverse-dark rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>

      <ConfirmationModal
        isOpen={showConfirm}
        onClose={() => setShowConfirm(false)}
        onConfirm={handleConfirmUpdate}
        title="Confirm Update"
        message={`Are you sure you want to update this channel?`}
      />
    </div>
  );
}
