/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn-images-3.listennotes.com',
        port: '',
        pathname: '/**',  // allow all paths under this domain
      },
      {
        protocol: 'https',
        hostname: 'placehold.co',
        port: '',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'images.example.com',  // added hostname for external images
        port: '',
        pathname: '/**',
      },
    ],
  },
};

module.exports = nextConfig;
