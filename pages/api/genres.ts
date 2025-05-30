import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const apiKey = process.env.LISTENNOTES_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: "API key not configured" });
  }

  try {
    const response = await fetch("https://listen-api.listennotes.com/api/v2/genres?top_level_only=1", {
      headers: {
        "X-ListenAPI-Key": apiKey,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      return res.status(response.status).json({ error: errorData });
    }

    const data = await response.json();
    return res.status(200).json(data.genres);
  } catch (error) {
    return res.status(500).json({ error: "Failed to fetch genres" });
  }
}
