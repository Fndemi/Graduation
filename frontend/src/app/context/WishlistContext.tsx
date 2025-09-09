'use client';

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from 'react';
import toast from 'react-hot-toast';
import { useAuth } from './authContext';
import { apiCall } from '../lib/auth';

// Define the type for a product
export interface Product {
  _id: string;
  name: string;
  price: number;
  category: string;
  niche: string;
  image: string;
  discountedPrice?: number;
  initialPrice?: number;
}

// Wishlist item type
export type WishlistItem = Product;

// Context value type
interface WishlistContextType {
  wishlist: WishlistItem[];
  loading: boolean;
  toggleWishlist: (productId: string) => Promise<void>;
  isWishlisted: (productId: string) => boolean;
}

const WishlistContext = createContext<WishlistContextType | undefined>(
  undefined,
);

export const useWishlist = () => {
  const context = useContext(WishlistContext);
  if (context === undefined) {
    throw new Error('useWishlist must be used within a WishlistProvider');
  }
  return context;
};

export const WishlistProvider = ({ children }: { children: ReactNode }) => {
  const { user, loading: authLoading } = useAuth();
  const [wishlist, setWishlist] = useState<WishlistItem[]>([]);
  const [loading, setLoading] = useState(true);

  // Fetch wishlist
  const fetchWishlist = async () => {
    if (!user) {
      setWishlist([]);
      setLoading(false);
      return;
    }

    setLoading(true);
    try {
      const data = await apiCall('/wishlist');
      // Assert the type
      setWishlist(data as WishlistItem[]);
    } catch (error) {
      console.error('Failed to fetch wishlist:', error);
      toast.error('Failed to load wishlist. Please try again.');
      setWishlist([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!authLoading) {
      fetchWishlist();
    }
  }, [user, authLoading]);

  const toggleWishlist = async (productId: string) => {
    if (!user) {
      toast.error('Please log in to manage your wishlist.');
      return;
    }

    setLoading(true);
    try {
      const updatedWishlist = await apiCall(`/wishlist/${productId}`, {
        method: 'POST',
      });
      setWishlist(updatedWishlist as WishlistItem[]); // <-- type assertion
      toast.success(
        isWishlisted(productId)
          ? 'Item removed from wishlist.'
          : 'Item added to wishlist!',
      );
    } catch (error) {
      console.error('Failed to toggle wishlist item:', error);
      toast.error('Failed to update wishlist. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const isWishlisted = (productId: string) => {
    return wishlist.some((item) => item._id === productId);
  };

  const value: WishlistContextType = {
    wishlist,
    loading,
    toggleWishlist,
    isWishlisted,
  };

  return (
    <WishlistContext.Provider value={value}>
      {children}
    </WishlistContext.Provider>
  );
};
