'use client';

import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { API, saveTokens } from '../../lib/api';

export default function Login() {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function submit(event) {
    event.preventDefault();
    setError('');
    setLoading(true);

    const form = new FormData(event.currentTarget);

    try {
      const tokenResponse = await fetch(`${API}/auth/token/`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: form.get('username'),
          password: form.get('password'),
        }),
      });

      const contentType = tokenResponse.headers.get('content-type') || '';
      const data = contentType.includes('application/json')
        ? await tokenResponse.json()
        : null;

      if (!tokenResponse.ok) {
        throw new Error(
          data?.detail ||
            `Login failed (${tokenResponse.status}). Check the Django API deployment.`
        );
      }

      if (!data?.access) {
        throw new Error('The API did not return an access token.');
      }

      saveTokens(data);

      const meResponse = await fetch(`${API}/auth/me/`, {
        headers: {
          Accept: 'application/json',
          Authorization: `Bearer ${data.access}`,
        },
        cache: 'no-store',
      });

      const meType = meResponse.headers.get('content-type') || '';
      const me = meType.includes('application/json')
        ? await meResponse.json()
        : null;

      if (!meResponse.ok) {
        throw new Error(
          me?.detail || `Profile request failed (${meResponse.status}).`
        );
      }

      router.replace(me.role === 'admin' ? '/admin' : '/dashboard');
    } catch (err) {
      setError(err.message || 'Unable to sign in.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth">
      <div className="authCard">
        <div className="brand">Cyber<span>Guard</span></div>
        <p className="eyebrow">SIGN IN</p>
        <h1>Welcome back</h1>

        <form onSubmit={submit}>
          <label>
            Username
            <input name="username" autoComplete="username" required />
          </label>

          <label>
            Password
            <input
              name="password"
              type="password"
              autoComplete="current-password"
              required
            />
          </label>

          <button className="button full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        {error && <p className="error">{error}</p>}

        <p>
          New user? <Link href="/register">Create an account</Link>
        </p>
      </div>
    </main>
  );
}
