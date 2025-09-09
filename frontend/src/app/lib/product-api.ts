// Server-side product API functions - NO 'use client' directive

export type Review = {
  _id: string;
  userId: string;
  name?: string; // reviewer's name (optional if returned from backend)
  comment: string;
  rating: number;
  createdAt: string;
};

export type Product = {
  _id: string;
  name: string;
  description: string;
  initialPrice: number;
  discountPercent?: number;
  discountedPrice?: number;
  image?: string;
  niche: string;
  category: string;
  reviews?: Review[]; // 👈 added reviews
};

// ---------- Public Product APIs (Server-side safe) ----------

export const searchProducts = async (params: { search?: string; category?: string; niche?: string }) => {
  const query = new URLSearchParams(params as any).toString();
  const res = await fetch(`https://graduation-project-wenh.onrender.com/products?${query}`);
  return res.json();
};

export async function fetchProducts(): Promise<Product[]> {
  const res = await fetch("https://graduation-project-wenh.onrender.com/products", {
    cache: "no-store", // ensures fresh data every fetch
  });

  if (!res.ok) {
    throw new Error("Failed to fetch products");
  }

  return res.json();
}

export async function fetchProductById(id: string): Promise<Product> {
  const res = await fetch(`https://graduation-project-wenh.onrender.com/products/${id}`, {
    cache: "no-store", // ensures always fresh data
  });

  if (!res.ok) {
    throw new Error("Failed to fetch product");
  }

  return res.json();
}