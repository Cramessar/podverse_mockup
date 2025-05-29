// pages/index.tsx
import Head from "next/head";
import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <>
      <Head>
        <title>Podverse – Discover Podcasts</title>
      </Head>
      <main className="bg-gray-950 text-white min-h-screen">
        {/* Hero */}
        <section className="px-8 py-20 text-center">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-4">
            Discover Your Next Favorite Podcast
          </h1>
          <p className="text-lg md:text-xl text-gray-400 mb-8">
            Browse trending shows, find hidden gems, and follow your favorite creators.
          </p>
          <Link href="/explore">
            <button className="bg-green-500 text-black font-semibold px-6 py-3 rounded-lg hover:bg-green-400 transition">
              Browse Podcasts
            </button>
          </Link>
        </section>

        {/* Trending Shows */}
        <section className="px-8 py-10">
          <h2 className="text-2xl font-bold mb-4">Trending Shows</h2>
          <div className="flex gap-4 overflow-x-auto pb-4">
            {[...Array(6)].map((_, i) => (
              <div
                key={i}
                className="min-w-[180px] bg-gray-800 rounded-lg p-4 flex-shrink-0 hover:bg-gray-700 transition"
              >
                <div className="aspect-square bg-gray-600 rounded mb-2" />
                <h3 className="text-lg font-medium">Podcast #{i + 1}</h3>
                <p className="text-sm text-gray-400">Host Name</p>
              </div>
            ))}
          </div>
        </section>

        {/* Categories */}
        <section className="px-8 py-10">
          <h2 className="text-2xl font-bold mb-4">Browse by Category</h2>
          <div className="flex flex-wrap gap-4">
            {["Tech", "Comedy", "True Crime", "Wellness", "News", "Education"].map((cat) => (
              <button
                key={cat}
                className="px-4 py-2 rounded-full border border-gray-600 text-sm hover:bg-gray-800"
              >
                {cat}
              </button>
            ))}
          </div>
        </section>

        {/* Featured Show */}
        <section className="px-8 py-10 bg-gray-900">
          <h2 className="text-2xl font-bold mb-6">Spotlight</h2>
          <div className="flex flex-col md:flex-row gap-8 items-center">
            <div className="w-64 h-64 bg-gray-700 rounded-lg" />
            <div>
              <h3 className="text-2xl font-semibold mb-2">The Mindful Mic</h3>
              <p className="text-gray-400 mb-4">
                A deep dive into conscious living, meditation, and mindful technology with host Jane Doe.
              </p>
              <Link href="/player/mindful-mic">
                <button className="bg-white text-black px-4 py-2 rounded-md font-medium hover:bg-gray-200">
                  Listen Now
                </button>
              </Link>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="px-8 py-6 text-center text-sm text-gray-500 border-t border-gray-800 mt-10">
          © {new Date().getFullYear()} Podverse. All rights reserved.
        </footer>
      </main>
    </>
  );
}
