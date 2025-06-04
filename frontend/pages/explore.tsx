import { useEffect, useState } from "react";

export default function ExplorePage() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Placeholder for future fetch logic
    setLoading(false);
  }, []);

  return (
    <main className="p-6">
      <h1 className="text-3xl font-bold mb-4">Explore Podcasts</h1>
      {loading ? <p>Loading categories...</p> : <p>Categories will go here soon.</p>}
    </main>
  );
}
