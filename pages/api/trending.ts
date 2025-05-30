import type { NextApiRequest, NextApiResponse } from "next";

const API_KEY = process.env.LISTENNOTES_API_KEY;
const BASE_URL = "https://listen-api.listennotes.com/api/v2";

interface Category {
  id: number;
  name: string;
  parent_id: number;
}

interface PodcastResult {
  // Adjust these based on the ListenNotes response shape
  id: string;
  title: string;
  publisher: string;
  image: string;
  episode_count?: number;
  category: string;
  [key: string]: any;
}

const categories: Category[] = [
  { id: 144, name: "Personal Finance", parent_id: 67 },
  { id: 151, name: "Locally Focused", parent_id: 67 },
  { id: 111, name: "Education", parent_id: 67 },
  { id: 69, name: "Religion & Spirituality", parent_id: 67 },
  { id: 107, name: "Science", parent_id: 67 },
  { id: 100, name: "Arts", parent_id: 67 },
  { id: 135, name: "True Crime", parent_id: 67 },
  { id: 82, name: "Leisure", parent_id: 67 },
  { id: 122, name: "Society & Culture", parent_id: 67 },
  { id: 68, name: "TV & Film", parent_id: 67 },
  { id: 125, name: "History", parent_id: 67 },
  { id: 132, name: "Kids & Family", parent_id: 67 },
  { id: 134, name: "Music", parent_id: 67 },
  { id: 99, name: "News", parent_id: 67 },
  { id: 88, name: "Health & Fitness", parent_id: 67 },
  { id: 127, name: "Technology", parent_id: 67 },
  { id: 168, name: "Fiction", parent_id: 67 },
  { id: 77, name: "Sports", parent_id: 67 },
  { id: 133, name: "Comedy", parent_id: 67 },
  { id: 93, name: "Business", parent_id: 67 },
  { id: 117, name: "Government", parent_id: 67 },
];

// Helper to split array into chunks
function chunkArray<T>(array: T[], size: number): T[][] {
  const chunks: T[][] = [];
  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size));
  }
  return chunks;
}

async function fetchPodcastForCategory(cat: Category): Promise<PodcastResult | null> {
  const url = `${BASE_URL}/search?q=podcast&genre_ids=${cat.id}&sort_by_date=0&type=podcast&offset=0&len_min=0&len_max=9999&language=English&safe_mode=0&page_size=1`;

  try {
    const response = await fetch(url, {
      headers: { "X-ListenAPI-Key": API_KEY || "" },
    });
    const data = await response.json();

    if (data.results && data.results.length > 0) {
      return { ...data.results[0], category: cat.name };
    } else {
      console.warn(`No podcast results for category: ${cat.name}`);
      return null;
    }
  } catch (error) {
    console.error(`Fetch error for category ${cat.name}:`, error);
    return null;
  }
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (!API_KEY) {
    return res.status(500).json({ error: "Missing API key" });
  }

  try {
    const batchSize = 2; // number of concurrent requests per batch
    const batches = chunkArray(categories, batchSize);

    const results: PodcastResult[] = [];

    for (const batch of batches) {
      // Execute current batch in parallel
      const batchResults = await Promise.all(batch.map(fetchPodcastForCategory));

      // Add valid results to final list
      results.push(...batchResults.filter((r): r is PodcastResult => r !== null));

      // Pause before next batch to avoid hitting rate limits
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }

    res.status(200).json(results);
  } catch (error) {
    console.error("ListenNotes API error:", error);
    res.status(500).json({ error: "Failed to fetch trending podcasts" });
  }
}
