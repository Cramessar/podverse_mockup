import type { NextApiRequest, NextApiResponse } from "next";
import fs from "fs";
import path from "path";

interface PodcastResult {
  id: string;
  title_original: string;
  publisher?: string;
  image?: string;
  episode_count?: number;
  category: string;
  [key: string]: any;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // Build path to the JSON file in public folder
    const jsonFilePath = path.join(process.cwd(), "public", "data", "trending_podcasts.json");

    // Read and parse JSON file
    const rawJson = fs.readFileSync(jsonFilePath, "utf-8");
    const jsonData = JSON.parse(rawJson);

    // Flatten the podcasts grouped by category into a single array with category property
    const podcastsArray: PodcastResult[] = [];

    for (const [category, podcasts] of Object.entries(jsonData.trending_podcasts)) {
      for (const podcast of podcasts as PodcastResult[]) {
        podcastsArray.push({
          ...podcast,
          category,
        });
      }
    }

    // Return the flattened array as JSON response
    res.status(200).json(podcastsArray);
  } catch (error) {
    console.error("Error loading trending podcasts:", error);
    res.status(500).json({ error: "Failed to load trending podcasts" });
  }
}
import type { NextApiRequest, NextApiResponse } from "next";
import fs from "fs";
import path from "path";

interface PodcastResult {
  id: string;
  title_original: string;
  publisher?: string;
  image?: string;
  episode_count?: number;
  category: string;
  [key: string]: unknown; // changed from any to unknown, testing to fix vercel build issues
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // Build path to the JSON file in public folder
    const jsonFilePath = path.join(process.cwd(), "public", "data", "trending_podcasts.json");

    // Read and parse JSON file
    const rawJson = fs.readFileSync(jsonFilePath, "utf-8");
    const jsonData = JSON.parse(rawJson);

    // Flatten the podcasts grouped by category into a single array with category property
    const podcastsArray: PodcastResult[] = [];

    for (const [category, podcasts] of Object.entries(jsonData.trending_podcasts)) {
      for (const podcast of podcasts as PodcastResult[]) {
        podcastsArray.push({
          ...podcast,
          category,
        });
      }
    }

    // Return the flattened array as JSON response
    res.status(200).json(podcastsArray);
  } catch (error: unknown) {
    console.error("Error loading trending podcasts:", error);
    res.status(500).json({ error: "Failed to load trending podcasts" });
  }
}
