export async function fetchChannels(params = {}) {
  const query = new URLSearchParams(params).toString();
  const res = await fetch(`http://localhost:8000/admin/channels?${query}`, {
    next: { revalidate: 10 },
  });
  if (!res.ok) throw new Error("Failed to fetch channels");
  return res.json();
}
