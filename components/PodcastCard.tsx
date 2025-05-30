import React from "react";
import Image from "next/image";
import { AiFillStar, AiOutlineStar, AiTwotoneStar } from "react-icons/ai";

interface PostCardProps {
  title: string;
  host: string;
  imageUrl: string;
  episodeCount?: number;
  rating?: number; // e.g., 4.5
}

const PostCard: React.FC<PostCardProps> = ({
  title,
  host,
  imageUrl,
  episodeCount = 0,
  rating = 0,
}) => {
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating - fullStars >= 0.5;

  return (
    <div className="bg-podverse-surface rounded-lg p-4 shadow-md hover:shadow-lg transition group">
      <div className="relative w-full aspect-square mb-3 overflow-hidden rounded">
        <Image
          src={imageUrl}
          alt={title}
          fill
          style={{ objectFit: "cover" }}
          className="rounded"
        />
      </div>

      <h3 className="text-lg font-semibold text-white mb-1 truncate">{title}</h3>
      <p className="text-sm text-podverse-muted mb-2 truncate">Hosted by {host}</p>

      <div className="flex items-center justify-between text-sm text-podverse-muted">
        <span>{episodeCount} episodes</span>

        <div
          className="flex items-center group-hover:scale-105 transition-transform duration-200 ease-in-out"
          title={`Rated ${rating.toFixed(1)} out of 5`}
        >
          {[...Array(5)].map((_, i) => {
            if (i < fullStars) {
              return <AiFillStar key={i} className="text-yellow-400 w-4 h-4" />;
            } else if (i === fullStars && hasHalfStar) {
              return <AiTwotoneStar key={i} className="text-yellow-400 w-4 h-4" />;
            } else {
              return <AiOutlineStar key={i} className="text-gray-600 w-4 h-4" />;
            }
          })}
          <span className="ml-1">{rating.toFixed(1)}</span>
        </div>
      </div>
    </div>
  );
};

export default PostCard;
