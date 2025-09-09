"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { fetchCart, removeFromCart, updateCartItem, CartItem } from "../lib/cart-api";
import CheckoutModal from '../components/CheckoutModal';
import toast, { Toaster } from 'react-hot-toast';

export default function CartPage() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [updatingProductId, setUpdatingProductId] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  async function loadCart() {
    try {
      setLoading(true);
      const data = await fetchCart();
      setCartItems(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to fetch cart:", err);
      setCartItems([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadCart();
  }, []);

  const handleRemove = async (productId: string) => {
    try {
      setUpdatingProductId(productId);
      const updatedCart = await removeFromCart(productId);
      setCartItems(Array.isArray(updatedCart) ? updatedCart : []);
      toast.success("Item removed successfully!");
    } catch (err) {
      console.error(err);
      toast.error("Failed to remove item.");
    } finally {
      setUpdatingProductId(null);
    }
  };

  const handleIncrease = async (productId: string, currentQty: number) => {
    try {
      setUpdatingProductId(productId);
      const updatedCart = await updateCartItem(productId, currentQty + 1);
      setCartItems(Array.isArray(updatedCart) ? updatedCart : []);
      toast.success("Quantity updated!");
    } catch (err) {
      console.error(err);
      toast.error("Failed to update quantity.");
    } finally {
      setUpdatingProductId(null);
    }
  };

  const handleDecrease = async (productId: string, currentQty: number) => {
    if (currentQty <= 1) {
      toast.error("Quantity cannot be less than 1.");
      return;
    }
    try {
      setUpdatingProductId(productId);
      const updatedCart = await updateCartItem(productId, currentQty - 1);
      setCartItems(Array.isArray(updatedCart) ? updatedCart : []);
      toast.success("Quantity updated!");
    } catch (err) {
      console.error(err);
      toast.error("Failed to update quantity.");
    } finally {
      setUpdatingProductId(null);
    }
  };

  const handleCheckoutSuccess = () => {
    setCartItems([]);
    setIsModalOpen(false);
    toast.success("Checkout successful! Your cart has been cleared.");
  };

  const totalPrice = Array.isArray(cartItems) && cartItems.length > 0
    ? cartItems.reduce((sum, item) => {
        const product = item.productId;
        if (!product || typeof product === 'string') return sum;
        const price = product.discountedPrice ?? product.initialPrice ?? 0;
        return sum + price * item.quantity;
      }, 0)
    : 0;

  if (loading) {
    return <p className="text-center mt-20">Loading cart...</p>;
  }

  if (!Array.isArray(cartItems) || cartItems.length === 0) {
    return (
      <div className="text-center mt-20">
        <p className="text-xl mb-4">Your cart is empty.</p>
        <button
          onClick={() => window.location.href = "/products"}
          className="custom-button px-6 py-3 rounded-lg"
        >
          Browse Products
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto py-10 px-4 mt-11">
      <Toaster />
      <h1 className="text-3xl font-bold mb-8">My Cart</h1>
      <div className="space-y-6">
        {cartItems.map((item, index) => {
          const product = item.productId;

          if (!product || typeof product === 'string') {
            return (
              <div key={index} className="text-red-500 p-4 border border-red-300 rounded">
                Error: Product data is missing or invalid.
              </div>
            );
          }

          const price = product.discountedPrice ?? product.initialPrice ?? 0;
          const itemTotal = price * item.quantity;
          const isUpdating = updatingProductId === product._id;

          return (
            <div
              key={product._id || index}
              className="flex items-center gap-4 border-b border-gray-700 pb-4"
            >
              <Image
                src={product.image || "/placeholder.png"}
                alt={product.name || "Product"}
                width={120}
                height={120}
                className="object-cover rounded-lg"
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120' fill='%23666'%3E%3Crect width='120' height='120' rx='8'/%3E%3Ctext x='50%25' y='50%25' text-anchor='middle' dy='0.3em' font-size='14' fill='%23999'%3ENo Image%3C/text%3E%3C/svg%3E";
                }}
              />
              <div className="flex-1">
                <h2 className="text-xl font-semibold">{product.name}</h2>
                <p className="text-gray-400">{product.category} • {product.niche}</p>
                <p className="text-green-400 font-bold mt-1">
                  Ksh {price.toLocaleString()} x {item.quantity} = Ksh {itemTotal.toLocaleString()}
                </p>
                <div className="flex gap-2 mt-2">
                  <button
                    onClick={() => handleDecrease(product._id, item.quantity)}
                    disabled={isUpdating || item.quantity <= 1}
                    className="px-3 py-1 bg-gray-700 text-white rounded-lg disabled:opacity-50"
                  >
                    -
                  </button>
                  <span className="px-3 py-1 border rounded-lg">{item.quantity}</span>
                  <button
                    onClick={() => handleIncrease(product._id, item.quantity)}
                    disabled={isUpdating}
                    className="px-3 py-1 bg-gray-700 text-white rounded-lg disabled:opacity-50"
                  >
                    +
                  </button>
                </div>
              </div>
              <button
                onClick={() => handleRemove(product._id)}
                disabled={isUpdating}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-500 disabled:opacity-50"
              >
                {isUpdating ? "Updating..." : "Remove"}
              </button>
            </div>
          );
        })}
      </div>

      <div className="mt-11 flex justify-between items-center">
        <h2 className="text-2xl font-bold">Total: Ksh {totalPrice.toLocaleString()}</h2>
        <button
          onClick={() => setIsModalOpen(true)}
          className="custom-button px-6 py-3 rounded-lg"
        >
          Checkout
        </button>
      </div>

      <CheckoutModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCheckoutSuccess={handleCheckoutSuccess}
      />
    </div>
  );
}
