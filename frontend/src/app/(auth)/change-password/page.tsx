'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Eye, EyeOff, Shield, CheckCircle } from 'lucide-react';
import { apiCall, requireAuth } from '@/app/lib/auth'; // Adjust path to your auth utilities

export default function ChangePasswordPage() {
  const [formData, setFormData] = useState({
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [errors, setErrors] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [showOldPassword, setShowOldPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  const router = useRouter();

  // Check authentication and handle client-side mounting
  useEffect(() => {
    setIsMounted(true);
    requireAuth();
    
    // SEO Meta Tags - only on client side
    document.title = 'Change Password | Secure Your Account';
    
    // Create meta tags
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription) {
      metaDescription.setAttribute('content', 'Update your account password securely. Change your current password to a new one with enhanced security.');
    } else {
      const meta = document.createElement('meta');
      meta.name = 'description';
      meta.content = 'Update your account password securely. Change your current password to a new one with enhanced security.';
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
    setSuccessMessage('');

    // Client-side validation
    const validationErrors: string[] = [];
    
    if (!formData.oldPassword) {
      validationErrors.push('Current password is required');
    }

    if (formData.newPassword.length < 6) {
      validationErrors.push('New password must be at least 6 characters long');
    }
    
    if (!/(?=.*[0-9])/.test(formData.newPassword)) {
      validationErrors.push('New password must contain at least one number');
    }

    if (formData.newPassword !== formData.confirmPassword) {
      validationErrors.push('New passwords do not match');
    }

    if (formData.oldPassword === formData.newPassword) {
      validationErrors.push('New password must be different from current password');
    }

    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      setIsLoading(false);
      return;
    }

    try {
      const response = await apiCall('/auth/change-password', {
        method: 'PUT',
        body: JSON.stringify({
          oldPassword: formData.oldPassword,
          newPassword: formData.newPassword,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to change password');
      }

      // Show success message
      setSuccessMessage('Password changed successfully! Redirecting...');
      
      // Clear form
      setFormData({
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      });

      // Redirect to home or profile page after 2 seconds
      setTimeout(() => {
        router.push('/');
      }, 2000);
      
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
      {/* Schema.org structured data for SEO */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Change Password",
            "description": "Secure password change form for user account",
            "url": typeof window !== 'undefined' ? window.location.href : '',
            "mainEntity": {
              "@type": "WebApplication",
              "name": "Password Change Form",
              "applicationCategory": "SecurityApplication"
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
          <div className="flex items-center space-x-3">
            <Shield className="w-6 h-6 text-orange-500" />
            <h1 className="text-xl font-semibold header-text">Change Password</h1>
          </div>
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

          {/* Success Message */}
          {successMessage && (
            <div className="mb-6 bg-green-50 dark:bg-green-900/50 border border-green-200 dark:border-green-500/50 rounded-lg p-4 flex items-center space-x-2" role="alert">
              <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0" />
              <p className="text-sm text-green-600 dark:text-green-200">{successMessage}</p>
            </div>
          )}

          {/* Header Section */}
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold header-text mb-2">Update Your Password</h2>
            <p className="text-gray-600 dark:text-gray-400">
              Choose a strong password to keep your account secure
            </p>
          </div>

          {/* Change Password Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Current Password */}
            <div>
              <label htmlFor="oldPassword" className="block text-sm font-medium label-text mb-2">
                Current Password
              </label>
              <div className="relative">
                <input
                  id="oldPassword"
                  name="oldPassword"
                  type={showOldPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  required
                  className="w-full px-4 py-3 pr-12 input-field rounded-full border-0 focus:outline-none focus:ring-2 focus:ring-orange-400 placeholder-gray-500 dark:placeholder-gray-400"
                  placeholder="Enter your current password"
                  value={formData.oldPassword}
                  onChange={handleInputChange}
                  aria-describedby="old-password-help"
                />
                <button
                  type="button"
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
                  onClick={() => setShowOldPassword(!showOldPassword)}
                  aria-label={showOldPassword ? 'Hide current password' : 'Show current password'}
                >
                  {showOldPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              <div id="old-password-help" className="sr-only">Enter your current account password for verification</div>
            </div>

            {/* New Password */}
            <div>
              <label htmlFor="newPassword" className="block text-sm font-medium label-text mb-2">
                New Password
              </label>
              <div className="relative">
                <input
                  id="newPassword"
                  name="newPassword"
                  type={showNewPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  required
                  className="w-full px-4 py-3 pr-12 input-field rounded-full border-0 focus:outline-none focus:ring-2 focus:ring-orange-400 placeholder-gray-500 dark:placeholder-gray-400"
                  placeholder="Choose a strong new password"
                  value={formData.newPassword}
                  onChange={handleInputChange}
                  aria-describedby="new-password-help"
                />
                <button
                  type="button"
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
                  onClick={() => setShowNewPassword(!showNewPassword)}
                  aria-label={showNewPassword ? 'Hide new password' : 'Show new password'}
                >
                  {showNewPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              <div id="new-password-help" className="text-xs text-gray-400 mt-1">
                Minimum 6 characters with at least one number
              </div>
            </div>

            {/* Confirm New Password */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium label-text mb-2">
                Confirm New Password
              </label>
              <div className="relative">
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  required
                  className="w-full px-4 py-3 pr-12 input-field rounded-full border-0 focus:outline-none focus:ring-2 focus:ring-orange-400 placeholder-gray-500 dark:placeholder-gray-400"
                  placeholder="Confirm your new password"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  aria-describedby="confirm-password-help"
                />
                <button
                  type="button"
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  aria-label={showConfirmPassword ? 'Hide password confirmation' : 'Show password confirmation'}
                >
                  {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              <div id="confirm-password-help" className="sr-only">Re-enter your new password to confirm</div>
            </div>

            {/* Security Tips */}
            <div className="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-500/30 rounded-lg p-4">
              <h3 className="text-sm font-medium text-orange-800 dark:text-orange-200 mb-2 flex items-center">
                <Shield className="w-4 h-4 mr-2" />
                Security Tips
              </h3>
              <ul className="text-xs text-orange-700 dark:text-orange-300 space-y-1">
                <li>• Use a combination of letters, numbers, and symbols</li>
                <li>• Make it different from your old password</li>
                <li>• Consider using a unique password for this account</li>
                <li>• Avoid using personal information like names or dates</li>
              </ul>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 custom-button font-semibold rounded-full transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-offset-2 focus:ring-offset-white dark:focus:ring-offset-gray-900 disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Changing Password...' : 'Change Password'}
            </button>
          </form>

          {/* Navigation Links */}
          <div className="mt-8 text-center space-y-4">
            <Link 
              href="/" 
              className="inline-flex items-center text-sm text-orange-500 hover:text-orange-400 font-medium transition-colors"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Home
            </Link>
            
            <div className="text-xs terms-text">
              <Link href="/help" className="text-orange-500 hover:text-orange-400 underline">
                Need help?
              </Link>
              {' • '}
              <Link href="/security" className="text-orange-500 hover:text-orange-400 underline">
                Security Center
              </Link>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}