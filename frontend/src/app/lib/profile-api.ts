import { apiCall } from './auth';

// Use the same UserProfile interface as AuthContext for consistency
export type UserProfile = {
  _id: string;
  name: string;
  email: string;
  role: string;
};

/**
 * Get user profile using centralized API call
 */
export async function getUserProfile(): Promise<UserProfile> {
  try {
    const data = await apiCall('/auth/me', { method: 'GET' });
    return data as UserProfile; // Type assertion
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to fetch user profile';
    throw new Error(errorMessage);
  }
}

/**
 * Update user profile using centralized API call
 */
export async function updateUserProfile(
  data: Partial<Pick<UserProfile, 'name' | 'email' | 'role'>>
): Promise<UserProfile> {
  try {
    const result = await apiCall('/auth/me', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
    return (result as any).user || (result as UserProfile); // Type assertion
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to update profile';
    throw new Error(errorMessage);
  }
}

/**
 * Legacy function - kept for backward compatibility
 */
export async function getUserProfileWithToken(token: string): Promise<UserProfile> {
  console.warn('getUserProfileWithToken is deprecated. Use AuthContext getUserProfile instead.');

  const currentToken = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;
  if (typeof window !== 'undefined') localStorage.setItem('accessToken', token);

  try {
    return await getUserProfile();
  } finally {
    if (typeof window !== 'undefined') {
      if (currentToken) localStorage.setItem('accessToken', currentToken);
      else localStorage.removeItem('accessToken');
    }
  }
}

/**
 * Legacy function - kept for backward compatibility
 */
export async function updateUserProfileWithToken(
  token: string,
  data: Partial<Pick<UserProfile, 'name' | 'email' | 'role'>>
): Promise<UserProfile> {
  console.warn('updateUserProfileWithToken is deprecated. Use AuthContext updateUserProfile instead.');

  const currentToken = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;
  if (typeof window !== 'undefined') localStorage.setItem('accessToken', token);

  try {
    return await updateUserProfile(data);
  } finally {
    if (typeof window !== 'undefined') {
      if (currentToken) localStorage.setItem('accessToken', currentToken);
      else localStorage.removeItem('accessToken');
    }
  }
}
