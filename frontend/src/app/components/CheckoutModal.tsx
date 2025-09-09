"use client";

import { checkoutCart } from '../lib/cart-api';
import toast from 'react-hot-toast'; // Import toast

interface CheckoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCheckoutSuccess: () => void;
}

export default function CheckoutModal({ isOpen, onClose, onCheckoutSuccess }: CheckoutModalProps) {
  if (!isOpen) return null;

  const handleConfirmCheckout = async () => {
    try {
      await checkoutCart();
      onCheckoutSuccess();
      toast.success("Checkout successful!");
    } catch (error) {
      console.error("Checkout failed:", error);
      toast.error("Checkout failed. Please try again.");
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg max-w-sm mx-auto">
        <h2 className="text-2xl font-bold mb-4 text-white">Confirm Order</h2>
        <p className="text-gray-300 mb-6">Are you sure you want to proceed with the checkout?</p>
        <div className="flex justify-end gap-4">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-500 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleConfirmCheckout}
            className="px-4 py-2 custom-button rounded-lg transition-colors"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}
