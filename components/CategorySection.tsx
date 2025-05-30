// components/CategorySection.tsx
import React from 'react';
import Link from 'next/link';
import PodcastCard from './PodcastCard';

interface CategorySectionProps {
  category: string;
  podcasts: {
    title: string;
    host: string;
    imageUrl: string;
    episodeCount: number;
    rating: number;
  }[];
}

const CategorySection: React.FC<CategorySectionProps> = ({ category, podcasts }) => {
  return (
    <section className="section">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">{category}</h2>
        <Link href={`/explore?category=${encodeURIComponent(category)}`}>
          <a className="text-sm text-podverse-primary hover:underline">Explore All</a>
        </Link>
      </div>
      <div className="flex gap-4 overflow-x-auto pb-4">
        {podcasts.map((podcast, index) => (
          <PodcastCard
            key={index}
            title={podcast.title}
            host={podcast.host}
            imageUrl={podcast.imageUrl}
            episodeCount={podcast.episodeCount}
            rating={podcast.rating}
          />
        ))}
      </div>
    </section>
  );
};

export default CategorySection;
