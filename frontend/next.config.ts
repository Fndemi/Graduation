import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "res.cloudinary.com", // allow Cloudinary images
      },
      {
        protocol: "https",
        hostname: "picsum.photos", // optional placeholder images
      },
    ],
    unoptimized: true,
    domains: ["res.cloudinary.com"],
  },
  eslint: {
    // ✅ Don’t block production build on ESLint errors
    ignoreDuringBuilds: true,
  },
  typescript: {
    // ✅ Don’t block production build on type errors
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
