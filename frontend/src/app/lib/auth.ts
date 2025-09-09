const API_BASE_URL = 'https://graduation-project-wenh.onrender.com/';

const refreshToken = async (): Promise<boolean> => {
  const refreshToken = typeof window !== 'undefined' ? localStorage.getItem('refreshToken') : null;
  if (!refreshToken) {
    return false;
  }
  try {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refreshToken }),
    });
    if (response.ok) {
      const tokens = await response.json();
      localStorage.setItem('accessToken', tokens.accessToken);
      localStorage.setItem('refreshToken', tokens.refreshToken);
      return true;
    }
  } catch (err) {
    console.error('Token refresh failed', err);
  }
  return false;
};

// ✅ Core API call with proper return typing
export const apiCall = async <T>(endpoint: string, options: RequestInit = {}): Promise<T> => {
  const accessToken = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;

  // 🛠️ IMPORTANT: Only set Content-Type to application/json if the body is not FormData
  const isFormData = options.body instanceof FormData;
  const headers: HeadersInit = {
    ...(accessToken && { Authorization: `Bearer ${accessToken}` }),
    ...(!isFormData && { 'Content-Type': 'application/json' }), // Conditionally set header
    ...(options.headers as object),
  };

  let response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401 && accessToken) {
    const refreshed = await refreshToken();
    if (refreshed) {
      const newAccessToken = localStorage.getItem('accessToken');
      headers.Authorization = `Bearer ${newAccessToken}`;
      response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
      });
    } else {
      throw new Error('Authentication failed. Please log in again.');
    }
  }

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || `API call to ${endpoint} failed with status ${response.status}`);
  }

  return data as T; // ✅ Only return payload, not { data: ... }
};