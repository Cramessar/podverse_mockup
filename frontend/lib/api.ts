// File: frontend/lib/api.ts
export async function fetchChannels(params = {}) {
  const query = new URLSearchParams(params).toString();
  const res = await fetch(`http://localhost:8000/admin/channels?${query}`, {
    next: { revalidate: 10 },
  });
  if (!res.ok) throw new Error("Failed to fetch channels");
  return res.json();
}

export async function fetchFeeds(params = {}) {
  const query = new URLSearchParams(params).toString();
  const res = await fetch(`http://localhost:8000/admin/feeds?${query}`, {
    next: { revalidate: 10 },
  });
  if (!res.ok) throw new Error("Failed to fetch feeds");
  return res.json();
}

export async function fetchFeedLogs(feedId: number) {
  const res = await fetch(`http://localhost:8000/admin/feeds/${feedId}/logs`, {
    next: { revalidate: 10 },
  });
  if (!res.ok) throw new Error(`Failed to fetch logs for feed ID ${feedId}`);
  return res.json();
}
