export interface Podcast {
  id: string;
  title: string;
  title_original?: string;      // optional fallback
  publisher: string;
  publisher_original?: string;  // optional fallback
  image: string;
  thumbnail?: string;           // optional fallback
  episodeCount?: number;
  total_episodes?: number;      // optional fallback
  rating?: number;
  category?: string;
}

export interface Genre {
  id: number;
  name: string;
}