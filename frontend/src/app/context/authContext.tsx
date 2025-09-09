'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { apiCall } from '../lib/auth';

// User profile interface
export interface UserProfile {
  _id: string;
  name: string;
  email: string;
  role: 'buyer' | 'seller';
}

// Auth state interface
interface AuthState {
  isAuthenticated: boolean;
  userId: string | null;
  userProfile: UserProfile | null;
}

// Auth context interface
interface AuthContextType {
  user: AuthState | null;
  loading: boolean;
  error: string | null;

  login: (email: string, password: string) => Promise<void>;
  signup: (userData: { name: string; email: string; password: string; role: 'buyer' | 'seller' }) => Promise<void>;
  logout: () => void;

  getUserProfile: () => Promise<UserProfile | null>;
  updateUserProfile: (data: Partial<Pick<UserProfile, 'name' | 'email' | 'role'>>) => Promise<void>;

  clearError: () => void;
  getAuthToken: () => string | null;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<AuthState | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Initialize auth state
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const accessToken = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;
        const userId = typeof window !== 'undefined' ? localStorage.getItem('userId') : null;

        if (accessToken && userId) {
          try {
            const profile = await fetchUserProfile();
            setUser({ isAuthenticated: true, userId, userProfile: profile });
          } catch {
            clearAuthStorage();
            setUser(null);
          }
        } else {
          setUser(null);
        }
      } catch (err) {
        console.error('Auth initialization error:', err);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const clearAuthStorage = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('userId');
    }
  };

  // Fetch user profile with typed response
  const fetchUserProfile = async (): Promise<UserProfile> => {
    const data = await apiCall('/auth/me', { method: 'GET' });
    return data as UserProfile; // <-- type assertion fixes TS error
  };

  const clearError = () => setError(null);

  const getAuthToken = (): string | null => {
    return typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;
  };

  const login = async (email: string, password: string): Promise<void> => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiCall('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      }) as { accessToken: string; refreshToken: string; userId: string };

      if (typeof window !== 'undefined') {
        localStorage.setItem('accessToken', data.accessToken);
        localStorage.setItem('refreshToken', data.refreshToken);
        localStorage.setItem('userId', data.userId);
      }

      const profile = await fetchUserProfile();
      setUser({ isAuthenticated: true, userId: data.userId, userProfile: profile });
      router.push('/');
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Login failed';
      setError(msg);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const signup = async (userData: { name: string; email: string; password: string; role: 'buyer' | 'seller' }): Promise<void> => {
    setLoading(true);
    setError(null);
    try {
      await apiCall('/auth/signup', {
        method: 'POST',
        body: JSON.stringify(userData),
      });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Signup failed';
      setError(msg);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getUserProfile = async (): Promise<UserProfile | null> => {
    if (!user?.isAuthenticated) return null;
    try {
      setError(null);
      const profile = await fetchUserProfile();
      setUser(prev => prev ? { ...prev, userProfile: profile } : null);
      return profile;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to fetch profile';
      setError(msg);
      return null;
    }
  };

  const updateUserProfile = async (data: Partial<Pick<UserProfile, 'name' | 'email' | 'role'>>): Promise<void> => {
    if (!user?.isAuthenticated) throw new Error('Not authenticated');
    try {
      setError(null);
      setLoading(true);

      const updatedProfile = await apiCall('/auth/me', {
        method: 'PUT',
        body: JSON.stringify(data),
      }) as UserProfile;

      setUser(prev => prev ? { ...prev, userProfile: updatedProfile } : null);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to update profile';
      setError(msg);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    clearAuthStorage();
    setUser(null);
    setError(null);
    router.push('/login');
  };

  const value: AuthContextType = { user, loading, error, login, signup, logout, getUserProfile, updateUserProfile, clearError, getAuthToken };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
