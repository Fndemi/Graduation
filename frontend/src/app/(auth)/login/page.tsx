'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Eye, EyeOff, Facebook } from 'lucide-react';

const API_BASE_URL = 'http://localhost:3000'; 

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [errors, setErrors] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  const router = useRouter();

  // Handle client-side mounting and SEO
  useEffect(() => {
    setIsMounted(true);
    
    // SEO Meta Tags - only on client side
    document.title = 'Sign In | Welcome Back to Our Marketplace';
    
    // Create meta tags
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription) {
      metaDescription.setAttribute('content', 'Sign in to your account to access your marketplace dashboard. Secure login for buyers and sellers.');
    } else {
      const meta = document.createElement('meta');
      meta.name = 'description';
      meta.content = 'Sign in to your account to access your marketplace dashboard. Secure login for buyers and sellers.';
      document.head.appendChild(meta);
    }

    // Keywords meta tag
    const metaKeywords = document.querySelector('meta[name="keywords"]');
    if (metaKeywords) {
      metaKeywords.setAttribute('content', 'login, sign in, marketplace, account access, secure login, buyer login, seller login');
    } else {
      const meta = document.createElement('meta');
      meta.name = 'keywords';
      meta.content = 'login, sign in, marketplace, account access, secure login, buyer login, seller login';
      document.head.appendChild(meta);
    }

    // Open Graph tags
    const ogTitle = document.querySelector('meta[property="og:title"]');
    if (!ogTitle) {
      const meta = document.createElement('meta');
      meta.setAttribute('property', 'og:title');
      meta.content = 'Sign In | Welcome Back to Our Marketplace';
      document.head.appendChild(meta);
    }

    const ogDescription = document.querySelector('meta[property="og:description"]');
    if (!ogDescription) {
      const meta = document.createElement('meta');
      meta.setAttribute('property', 'og:description');
      meta.content = 'Sign in to your account to access your marketplace dashboard.';
      document.head.appendChild(meta);
    }
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear errors when user starts typing
    if (errors.length > 0) {
      setErrors([]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrors([]);

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Login failed');
      }

      // Store tokens in localStorage (SSR-safe)
      if (typeof window !== 'undefined') {
        localStorage.setItem('accessToken', data.accessToken);
        localStorage.setItem('refreshToken', data.refreshToken);
        localStorage.setItem('userId', data.userId);
      }

      // Redirect to root
      router.push('/');
      
    } catch (error) {
      setErrors([error instanceof Error ? error.message : 'An error occurred']);
    } finally {
      setIsLoading(false);
    }
  };

  // Don't render until mounted to avoid hydration issues
  if (!isMounted) {
    return null;
  }

  return (
    <>
      {/* Schema.org structured data for SEO - only render on client */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Sign In",
            "description": "Sign in to your marketplace account",
            "url": typeof window !== 'undefined' ? window.location.href : '',
            "mainEntity": {
              "@type": "WebApplication",
              "name": "Marketplace Login",
              "applicationCategory": "BusinessApplication"
            }
          })
        }}
      />

      <main className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white transition-colors">
        {/* Header */}
        <header className="flex items-center p-6 border-b border-gray-200 dark:border-gray-700">
          <button 
            onClick={() => router.back()}
            className="mr-4 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            aria-label="Go back to previous page"
          >
            <ArrowLeft className="w-6 h-6" />
          </button>
          <h1 className="text-xl font-semibold">Welcome Back</h1>
        </header>

        <div className="px-6 py-8 max-w-md mx-auto">
          {/* Error Messages */}
          {errors.length > 0 && (
            <div className="mb-6 bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-500/50 rounded-lg p-4" role="alert">
              {errors.map((error, index) => (
                <p key={index} className="text-sm text-red-600 dark:text-red-200">{error}</p>
              ))}
            </div>
          )}

          {/* Welcome Message */}
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold header-text mb-2">Sign In</h2>
            <p className="text-gray-600 dark:text-gray-400">Enter your credentials to access your account</p>
          </div>

          {/* Login Form */}
          <div className="space-y-6">
            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium label-text mb-2">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="w-full px-4 py-3 input-field rounded-full border-0 focus:outline-none focus:ring-2 focus:ring-orange-400 placeholder-gray-500 dark:placeholder-gray-400"
                placeholder="Example@Example.Com"
                value={formData.email}
                onChange={handleInputChange}
                aria-describedby="email-help"
              />
              <div id="email-help" className="sr-only">Enter the email address associated with your account</div>
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium label-text mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  required
                  className="w-full px-4 py-3 pr-12 input-field rounded-full border-0 focus:outline-none focus:ring-2 focus:ring-orange-400 placeholder-gray-500 dark:placeholder-gray-400"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={handleInputChange}
                  aria-describedby="password-help"
                />
                <button
                  type="button"
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              <div id="password-help" className="sr-only">Enter your account password</div>
            </div>

            {/* Change Password Link */}
            <div className="text-right">
              <Link href="/change-password" className="text-sm text-gray-700 dark:text-gray-300 hover:text-orange-500 underline transition-colors">
                Change Password
              </Link>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              onClick={handleSubmit}
              className="w-full py-3 custom-button font-semibold rounded-full transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-offset-2 focus:ring-offset-white dark:focus:ring-offset-gray-900"
            >
              {isLoading ? 'Signing In...' : 'Sign In'}
            </button>
          </div>

          {/* Divider */}
          <div className="my-8 text-center text-sm text-gray-400">
            or sign in with
          </div>

          {/* Social Login Buttons */}
          <div className="flex space-x-4 mb-8">
            <button 
              type="button"
              className="flex-1 flex items-center justify-center py-3 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500"
              aria-label="Sign in with Facebook (coming soon)"
            >
              <Facebook className="w-5 h-5 text-blue-500" />
            </button>
            <button 
              type="button"
              className="flex-1 flex items-center justify-center py-3 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500"
              aria-label="Sign in with Google (coming soon)"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
            </button>
          </div>

          {/* Signup Link */}
          <div className="text-center text-sm terms-text">
            Dont have an account?{' '}
            <Link href="/signup" className="text-orange-500 hover:text-orange-400 font-medium underline">
              Sign up
            </Link>
          </div>
        </div>
      </main>
    </>
  );
}