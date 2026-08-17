const DEFAULT_API_URL = 'https://cybersecurity-training-platform.onrender.com/api';

export const API = (process.env.NEXT_PUBLIC_API_URL || DEFAULT_API_URL).replace(/\/+$/, '');

export const getToken = () =>
  typeof window === 'undefined' ? null : localStorage.getItem('access_token');

export const saveTokens = (d) => {
  localStorage.setItem('access_token', d.access);
  localStorage.setItem('refresh_token', d.refresh || '');
};

export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

export async function readResponse(r) {
  const contentType = r.headers.get('content-type') || '';
  const text = await r.text();

  if (contentType.includes('application/json')) {
    try {
      return { data: JSON.parse(text), raw: text };
    } catch {
      return { data: null, raw: text };
    }
  }

  return { data: null, raw: text };
}

export function getErrorMessage(data, raw, fallback = 'Request failed') {
  if (data?.detail) return String(data.detail);
  if (data && typeof data === 'object') {
    const values = Object.values(data).flat(Infinity).filter(Boolean);
    if (values.length) return values.join(' ');
  }
  if (raw && raw.trim().startsWith('<')) {
    return 'The server returned an HTML page instead of the CyberGuard API. Check NEXT_PUBLIC_API_URL and the backend deployment.';
  }
  return raw?.trim() || fallback;
}

export async function api(path, options = {}) {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  if (token) headers.Authorization = `Bearer ${token}`;

  const r = await fetch(`${API}${path}`, {
    ...options,
    headers,
    cache: 'no-store'
  });

  const { data, raw } = await readResponse(r);

  if (!r.ok) {
    throw new Error(getErrorMessage(data, raw));
  }

  return data;
}
