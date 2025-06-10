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
  [key: string]: unknown; // works for vercel deployment.
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const jsonFilePath = path.join(process.cwd(), "public", "data", "trending_podcasts.json");
    const rawJson = fs.readFileSync(jsonFilePath, "utf-8");
    const jsonData = JSON.parse(rawJson);

    const podcastsArray: PodcastResult[] = [];

    // Explicitly type Object.entries() to fix no-explicit-any error
    for (const [category, podcasts] of Object.entries(jsonData.trending_podcasts) as [string, PodcastResult[]][]) {
      for (const podcast of podcasts) {
        podcastsArray.push({
          ...podcast,
          category,
        });
      }
    }

    res.status(200).json(podcastsArray);
  } catch (error: unknown) {
    console.error("Error loading trending podcasts:", error);
    res.status(500).json({ error: "Failed to load trending podcasts" });
  }
}
