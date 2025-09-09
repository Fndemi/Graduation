'use client';

import { apiCall } from "../lib/auth";
import toast from 'react-hot-toast';

// Define a type for a cart item
export type CartItem = {
  productId: { // Product object (populated)
    _id: string;
    name: string;
    initialPrice: number;
    discountedPrice?: number;
    image?: string;
    category?: string;
    niche?: string;
  };
  quantity: number;
};

// Add a product to the cart
export const addToCart = async (productId: string, quantity: number = 1): Promise<CartItem[]> => {
  try {
    const data = await apiCall('/cart', {
      method: "POST",
      body: JSON.stringify({ productId, quantity }),
    });

    return data as CartItem[]; // Type assertion
  } catch (err: any) {
    console.error("Add to cart error:", err);
    toast.error("Failed to add product to cart. Please try again.");
    throw err;
  }
};

// Fetch all items in the cart
export const fetchCart = async (): Promise<CartItem[]> => {
  try {
    const data = await apiCall('/cart');
    return data as CartItem[]; // Type assertion
  } catch (err: any) {
    console.error("Failed to fetch cart:", err);
    toast.error("Failed to fetch cart. Please try again.");
    return [];
  }
};

// Update the quantity of a cart item
export const updateCartItem = async (productId: string, quantity: number): Promise<CartItem[]> => {
  try {
    const data = await apiCall('/cart', {
      method: "PUT",
      body: JSON.stringify({ productId, quantity }),
    });

    return data as CartItem[]; // Type assertion
  } catch (err: any) {
    console.error("Failed to update cart item:", err);
    toast.error("Failed to update cart item. Please try again.");
    throw err;
  }
};

// Remove an item from the cart (set quantity to 0)
export const removeFromCart = async (productId: string): Promise<CartItem[]> => {
  try {
    const data = await apiCall('/cart', {
      method: "PUT",
      body: JSON.stringify({ productId, quantity: 0 }),
    });

    return data as CartItem[]; // Type assertion
  } catch (err: any) {
    console.error("Failed to remove item:", err);
    toast.error("Failed to remove item from cart. Please try again.");
    throw err;
  }
};

// Checkout cart (clears cart)
export const checkoutCart = async (): Promise<{ message: string }> => {
  try {
    const data = await apiCall('/cart/checkout', {
      method: "POST",
    });

    return data as { message: string }; // Type assertion
  } catch (err: any) {
    console.error("Failed to checkout:", err);
    toast.error("Failed to checkout. Please try again.");
    throw err;
  }
};
