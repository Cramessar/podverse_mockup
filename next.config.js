/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: [
      'cdn-images-3.listennotes.com', // For real podcast images
      'placehold.co',                 // For mock placeholder images
    ],
  },
};

module.exports = nextConfig;
