import Link from "next/link";
import PodcastCard from "@/components/PodcastCard";
import { useEffect, useState } from "react";
import FloatingHamburgerMenu from "@/components/FloatingHamburgerMenu";


interface Podcast {
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

interface Genre {
  id: number;
  name: string;
}

 function Home() {
  const [genres, setGenres] = useState<Genre[]>([]);
  const [trending, setTrending] = useState<Podcast[]>([]);
  const [livePodcasts, setLivePodcasts] = useState<Podcast[]>([]);
  const [loadingLive, setLoadingLive] = useState(true);

  useEffect(() => {
    fetch("/data/genres.json")
      .then((res) => res.json())
      .then(setGenres)
      .catch((err) => console.error("Failed to load genres", err));
  }, []);

  useEffect(() => {
    if (genres.length === 0) return;

    fetch("/api/trending")
      .then((res) => res.json())
      .then((data) => {
        setTrending(data);
      })
      .catch((err) => {
        console.error("Failed to load trending podcasts from API", err);

        // Fallback: Load from local JSON file
        fetch("/data/trending_podcasts.json")
          .then((res) => res.json())
          .then((fallbackData) => {
            if (fallbackData && fallbackData.trending_podcasts) {
              const fallbackPodcasts = Object.values(fallbackData.trending_podcasts).flat() as Podcast[];
              setTrending(fallbackPodcasts);
            } else {
              setTrending([]);
            }
          })
          .catch((err) => {
            console.error("Failed to load fallback trending podcasts", err);
            setTrending([]);
          });
      });
  }, [genres]);

  useEffect(() => {
    fetch("/data/live_podcasts.json")
      .then((res) => res.json())
      .then((data) => setLivePodcasts(data.results || []))
      .catch((err) => console.error("Failed to load live podcasts", err))
      .finally(() => setLoadingLive(false));
  }, []);

  // Group trending podcasts by category, allowing multiple podcasts per category
  const trendingByCategory = trending.reduce<Record<string, Podcast[]>>((acc, podcast) => {
    if (podcast.category) {
      if (!acc[podcast.category]) {
        acc[podcast.category] = [];
      }
      acc[podcast.category].push(podcast);
    }
    return acc;
  }, {});

  return (
    <>
      <FloatingHamburgerMenu categories={genres} />

      <main className="bg-podverse-background text-podverse-text min-h-screen p-6">
        {/* Hero Section */}
        <section className="gradient-bg section text-center">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-4">
            Discover Your Next Favorite Podcast
          </h1>
          <p className="text-lg md:text-xl text-white/80 mb-8">
            Browse trending shows by category and follow your favorite creators.
          </p>
          <Link href="/explore" className="btn">
            Browse
          </Link>
        </section>

        {/* Browse Categories */}
        {genres.length > 0 && (
          <section className="section">
            <h2 className="text-2xl font-bold mb-4">Browse by Category</h2>
            <div className="flex flex-wrap gap-4">
              {genres.map((genre) => (
                <button
                  key={genre.id}
                  className="px-4 py-2 rounded-full border border-podverse-border text-sm hover:bg-podverse-surface"
                >
                  {genre.name}
                </button>
              ))}
            </div>
          </section>
        )}

        {/* Trending Shows */}
        <section className="section">
          <h2 className="text-2xl font-bold mb-4">Trending Shows</h2>

          <div className="flex gap-4 overflow-x-auto pb-4">
            {Object.entries(trendingByCategory).map(([category, podcasts]) => (
              <div
                key={category}
                className="bg-podverse-surface rounded-lg p-4 shadow-md min-w-[220px] flex flex-col justify-between"
                style={{ minHeight: "380px" }}
              >
                <h3 className="font-semibold mb-3">{category}</h3>
                <div className="flex-grow space-y-4 overflow-y-auto max-h-[300px]">
                  {podcasts.map((podcast) => {
                    const title = podcast.title || podcast.title_original || "Unknown Title";
                    const publisher =
                      podcast.publisher || podcast.publisher_original || "Unknown Publisher";
                    const image =
                      podcast.image || podcast.thumbnail || "https://placehold.co/180x180?text=No+Image";
                    const episodeCount = podcast.episodeCount ?? podcast.total_episodes ?? 0;
                    const rating = podcast.rating ?? 0;

                    return (
                      <PodcastCard
                        key={podcast.id}
                        title={title}
                        host={publisher}
                        imageUrl={image}
                        episodeCount={episodeCount}
                        rating={rating}
                      />
                    );
                  })}
                </div>
                <Link
                  href={`/explore?category=${encodeURIComponent(category)}`}
                  className="btn mt-4 text-center"
                  style={{ width: "100%" }}
                >
                  Explore {category}
                </Link>
              </div>
            ))}
          </div>
        </section>

        {/* Live Episodes from API */}
        {!loadingLive && livePodcasts.length > 0 && (
          <section className="section">
            <h2 className="text-2xl font-bold mb-4">Live Star Wars Episodes</h2>
            <div className="flex gap-4 overflow-x-auto pb-4">
              {livePodcasts.map((podcast: Podcast, i: number) => (
                <PodcastCard
                  key={podcast.id || i}
                  title={podcast.title}
                  host={podcast.publisher || "Unknown Host"}
                  imageUrl={podcast.image || `https://placehold.co/180x180?text=No+Image`}
                  episodeCount={podcast.episodeCount || 0}
                  rating={podcast.rating || 0}
                />
              ))}
            </div>
          </section>
        )}

        {/* Spotlight Show */}
        <section className="section bg-podverse-surface">
          <h2 className="text-2xl font-bold mb-6">Spotlight</h2>
          <div className="flex flex-col md:flex-row gap-8 items-center">
            <div className="w-64 h-64 bg-podverse-border rounded-lg" />
            <div>
              <h3 className="text-2xl font-semibold mb-2">The Mindful Mic</h3>
              <p className="text-podverse-muted mb-4">
                A deep dive into conscious living, meditation, and mindful technology with host Jane Doe.
              </p>
              <Link href="/player/mindful-mic" className="btn bg-white text-black hover:bg-podverse-highlight">
                Listen Now
              </Link>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="px-8 py-6 text-center text-sm text-podverse-muted border-t border-podverse-border mt-10">
          © {new Date().getFullYear()} Podverse. All rights reserved. Chris Ramessar, Daniel Morris, Elif Erik, Garrett Cross, Mike Schappell, Noel Watters, and Tim Scherman – the most awesome team ever.
        </footer>
      </main>
    </>
  );
}
export default Home;