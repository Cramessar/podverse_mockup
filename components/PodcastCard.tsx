import React, { useEffect, useState } from "react";
import Image from "next/image";

interface PostCardProps {
  title: string;
  host: string;
  imageUrl: string;
  episodeCount?: number;
  rating?: number;
}

const PostCard: React.FC<PostCardProps> = ({
  title,
  host,
  imageUrl,
  episodeCount = 0,
  rating = 0,
}) => {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  return (
    <div className="bg-podverse-surface rounded-lg p-4 shadow-md hover:shadow-lg transition group w-48 sm:w-56 flex-shrink-0">
      <div className="relative w-full h-48 mb-3 rounded overflow-hidden">
        <Image
          src={imageUrl}
          alt={title}
          layout="fill"
          objectFit="cover"
          className="rounded"
        />
      </div>

      <h3 className="text-md font-semibold text-white truncate">{title}</h3>
      <p className="text-xs text-podverse-muted truncate mb-2">Hosted by {host}</p>

      <div className="flex items-center justify-between text-xs text-podverse-muted">
        <span suppressHydrationWarning>{episodeCount} eps</span>
        <span className="text-yellow-400" suppressHydrationWarning>
          {isMounted ? rating.toFixed(1) : "–.–"} ★
        </span>
      </div>
    </div>
  );
};

export default PostCard;
