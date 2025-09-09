import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
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
};

export default nextConfig;
