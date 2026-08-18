'use client';

import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api, saveTokens } from '../../lib/api';

export default function Login() {
  const [error, setError] = useState('');
  const router = useRouter();

  async function submit(e) {
    e.preventDefault();
    setError('');

    const form = new FormData(e.currentTarget);

    try {
      // Get JWT tokens
      const tokens = await api('/auth/token/', {
        method: 'POST',
        body: JSON.stringify({
          username: form.get('username'),
          password: form.get('password'),
        }),
      });

      // Save tokens
      saveTokens(tokens);

      // Get logged-in user
      const user = await api('/auth/me/');

      // Redirect based on role
      if (user.role === 'admin') {
        router.push('/admin');
      } else {
        router.push('/dashboard');
      }

    } catch (err) {
      console.error('LOGIN ERROR:', err);
      setError(err.message || 'Unable to sign in. Please try again.');
    }
  }

  return (
    <main className="auth">
      <div className="authCard">

        <div className="brand">
          Cyber<span>Guard</span>
        </div>

        <p className="eyebrow">SIGN IN</p>

        <h1>Welcome back</h1>

        <form onSubmit={submit}>

          <label>
            Username
            <input
              name="username"
              autoComplete="username"
              required
            />
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

          <button className="button full" type="submit">
            Sign In
          </button>

        </form>

        {error && (
          <p className="error">
            {error}
          </p>
        )}

        <p>
          New user? <Link href="/register">Create an account</Link>
        </p>

      </div>
    </main>
  );
}
