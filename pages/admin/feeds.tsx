// pages/admin/feeds.tsx
import { useAdminAuth } from "./hooks/useAdminAuth";
import { useEffect, useState } from "react";

interface Feed {
  id: string;
  title: string;
  description?: string;
  url: string;
}

export default function AdminFeeds() {
  const { user, loading } = useAdminAuth();
  const [feeds, setFeeds] = useState<Feed[]>([]);
  const [loadingFeeds, setLoadingFeeds] = useState(true);

  useEffect(() => {
    if (!user) return;

    async function fetchFeeds() {
      setLoadingFeeds(true);
      try {
        // TODO: Replace with your real admin feeds API endpoint
        const res = await fetch("/api/admin/feeds");
        if (!res.ok) throw new Error("Failed to load feeds");
        const data = await res.json();
        setFeeds(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoadingFeeds(false);
      }
    }

    fetchFeeds();
  }, [user]);

  if (loading || loadingFeeds) return <p>Loading...</p>;

  if (!user) return null; // Redirect handled in hook

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-6">Admin Feeds Management</h1>

      {feeds.length === 0 ? (
        <p>No feeds found.</p>
      ) : (
        <ul className="space-y-4">
          {feeds.map((feed) => (
            <li key={feed.id} className="border p-4 rounded-md shadow-sm">
              <h2 className="text-xl font-semibold">{feed.title}</h2>
              {feed.description && <p className="mt-1">{feed.description}</p>}
              <a
                href={feed.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline mt-2 inline-block"
              >
                Visit Feed
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
