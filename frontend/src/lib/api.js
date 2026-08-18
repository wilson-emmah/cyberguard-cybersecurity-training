export const API =
  process.env.NEXT_PUBLIC_API_URL ||
  'https://cyberguard-cybersecurity-training.onrender.com/api';

export const getToken = () =>
  typeof window === 'undefined'
    ? null
    : localStorage.getItem('access_token');

export const saveTokens = (data) => {
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh || '');
};

export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

export async function api(path, options = {}) {
  const token = getToken();

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API}${path}`, {
    ...options,
    headers,
    cache: 'no-store',
  });

  let data = null;

  try {
    data = await response.json();
  } catch {
    // Response was not JSON
  }

  if (!response.ok) {
    throw new Error(
      data?.detail ||
      Object.values(data || {}).flat().join(' ') ||
      `API request failed (${response.status})`
    );
  }

  return data;
}
