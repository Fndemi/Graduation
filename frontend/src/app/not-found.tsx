"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function NotFound() {
  const router = useRouter();

  useEffect(() => {
    const timer = setTimeout(() => {
      router.push("/");
    }, 3000);

    return () => clearTimeout(timer);
  }, [router]);

  return (
    <div className="flex flex-col items-center justify-center h-screen text-center bg-gray-50 dark:bg-gray-800">
      <h1 className="text-6xl font-bold text-pink-500">404</h1>
      <p className="mt-2 text-gray-600 dark:text-white">Page not found. Redirecting you...</p>
    </div>
  );
}
