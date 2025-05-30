import Head from "next/head";
import Link from "next/link";
import PodcastCard from "@/components/PodcastCard";
import CategorySection from "@/components/CategorySection";

const categories = [
  "Arts",
  "Business",
  "Comedy",
  "Education",
  "Fiction",
  "Government",
  "Health and Fitness",
  "History",
  "Kids and Family",
  "Leisure",
  "Music",
  "News",
  "Religion and Spirituality",
  "Science",
  "Society and Culture",
  "Sports",
  "Technology",
  "True Crime",
  "TV and Film",
];

const mockPodcasts = Array.from({ length: 6 }, (_, i) => ({
  title: `Podcast ${i + 1}`,
  host: `Host ${i + 1}`,
  imageUrl: `https://placehold.co/180x180?text=Pod+${i + 1}`,
  episodeCount: Math.floor(Math.random() * 100),
  rating: parseFloat((Math.random() * 5).toFixed(1)),
}));

export default function Home() {
  return (
    <>
      <Head>
        <title>Podverse – Discover Podcasts</title>
      </Head>

      <main className="bg-podverse-background text-podverse-text min-h-screen">

        {/* Hero */}
        <section className="gradient-bg section text-center">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-4">
            Discover Your Next Favorite Podcast
          </h1>
          <p className="text-lg md:text-xl text-white/80 mb-8">
            Browse trending shows, find hidden gems, and follow your favorite creators.
          </p>
          <Link href="/explore" className="btn">
            Browse
          </Link>
        </section>

        {/* Trending Shows */}
        <section className="section">
          <h2 className="text-2xl font-bold mb-4">Trending Shows</h2>
          <div className="flex gap-4 overflow-x-auto pb-4">
            {[...Array(6)].map((_, i) => (
              <PodcastCard
                key={i}
                title={`Podcast #${i + 1}`}
                host={`Host ${i + 1}`}
                imageUrl={`https://placehold.co/180x180?text=Pod+${i + 1}`}
                episodeCount={Math.floor(Math.random() * 100)}
                rating={parseFloat((Math.random() * 5).toFixed(1))}
              />
            ))}
          </div>
        </section>

        {/* Categories */}
        <section className="section">
          <h2 className="text-2xl font-bold mb-4">Browse by Category</h2>
          <div className="flex flex-wrap gap-4">
            {["Tech", "Comedy", "True Crime", "Wellness", "News", "Education"].map((cat) => (
              <button
                key={cat}
                className="px-4 py-2 rounded-full border border-podverse-border text-sm hover:bg-podverse-surface"
              >
                {cat}
              </button>
            ))}
          </div>
        </section>

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

        {/* Category Sections */}
        {categories.map((category) => (
          <CategorySection key={category} category={category} podcasts={mockPodcasts} />
        ))}

        {/* Footer */}
        <footer className="px-8 py-6 text-center text-sm text-podverse-muted border-t border-podverse-border mt-10">
          © {new Date().getFullYear()} Podverse. All rights reserved. Chris Ramessar, Daniel Morris, Elif Erik, Garrett Cross, Mike Schappell, Noel Watters, and Tim Scherman the most awesome team ever.
        </footer>
      </main>
    </>
  );
}
