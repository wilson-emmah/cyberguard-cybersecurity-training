'use client';

import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { API, getErrorMessage, readResponse, saveTokens } from '../../lib/api';

export default function Login() {
  const [e, setE] = useState('');
  const router = useRouter();

  async function submit(x) {
    x.preventDefault();
    setE('');

    const form = x.currentTarget;
    const f = new FormData(form);

    try {
      const a = await fetch(`${API}/auth/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: f.get('username'),
          password: f.get('password')
        })
      });

      const { data, raw } = await readResponse(a);

      if (!a.ok) {
        throw new Error(getErrorMessage(data, raw, 'Invalid login.'));
      }

      saveTokens(data);

      const mResponse = await fetch(`${API}/auth/me/`, {
        headers: { Authorization: `Bearer ${data.access}` },
        cache: 'no-store'
      });

      const { data: m, raw: mRaw } = await readResponse(mResponse);

      if (!mResponse.ok) {
        throw new Error(getErrorMessage(m, mRaw, 'Unable to load your account.'));
      }

      router.push(m.role === 'admin' ? '/admin' : '/dashboard');
    } catch (a) {
      setE(a?.message || 'Unable to connect to the login server.');
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
            <input name="username" required />
          </label>

          <label>
            Password
            <input name="password" type="password" required />
          </label>

          <button className="button full">Sign In</button>
        </form>

        {e && <p className="error">{e}</p>}

        <p>
          New user? <Link href="/register">Create an account</Link>
        </p>
      </div>
    </main>
  );
}
