const rawBase = process.env.NEXT_PUBLIC_API_URL || 'https://cyberguard-cybersecurity-training.onrender.com/api';
export const API = rawBase.replace(/\/$/, '');

export const getToken = () =>
  typeof window === 'undefined' ? null : localStorage.getItem('access_token');

export const saveTokens = (data) => {
  if (typeof window === 'undefined') return;
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh || '');
};

export const logout = () => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

export async function api(path, options = {}) {
  const token = getToken();
  const headers = {
    Accept: 'application/json',
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${API}${path.startsWith('/') ? path : `/${path}`}`, {
    ...options,
    headers,
    cache: 'no-store',
  });

  const contentType = response.headers.get('content-type') || '';
  let data = null;

  if (contentType.includes('application/json')) {
    try {
      data = await response.json();
    } catch {
      data = null;
    }
  } else {
    try {
      const text = await response.text();
      data = text ? { detail: text.slice(0, 300) } : null;
    } catch {
      data = null;
    }
  }

  if (!response.ok) {
    const message =
      data?.detail ||
      Object.values(data || {})
        .flat()
        .join(' ') ||
      `API request failed (${response.status})`;
    throw new Error(message);
  }

  return data;
}
