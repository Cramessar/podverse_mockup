import React from "react";
import Image from "next/image";
import { AiFillStar, AiOutlineStar } from "react-icons/ai";

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
  return (
    <div className="bg-podverse-surface rounded-lg p-4 shadow-md hover:shadow-lg transition group">
      <div className="relative w-full aspect-square mb-3 overflow-hidden rounded">
        <Image
          src={imageUrl}
          alt={title}
          fill
          className="rounded"
          style={{ objectFit: "cover" }}
          sizes="(max-width: 768px) 100vw, 180px"
        />
      </div>

      <h3 className="text-lg font-semibold text-white mb-1 truncate">{title}</h3>
      <p className="text-sm text-podverse-muted mb-2 truncate">Hosted by {host}</p>

      <div className="flex items-center justify-between text-sm text-podverse-muted">
        <span>{episodeCount} episodes</span>
        <div className="flex items-center">
          {[...Array(5)].map((_, i) =>
            i < Math.floor(rating) ? (
              <AiFillStar
                key={i}
                className="text-yellow-400 w-4 h-4 group-hover:scale-110 transition-transform"
              />
            ) : (
              <AiOutlineStar
                key={i}
                className="text-gray-600 w-4 h-4 group-hover:scale-105 transition-transform"
              />
            )
          )}
          <span className="ml-1">{typeof rating === "number" ? rating.toFixed(1) : "N/A"}</span>
        </div>
      </div>
    </div>
  );
};

export default PostCard;
