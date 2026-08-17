'use client';

import Link from 'next/link';
import { useState } from 'react';
import { API, getErrorMessage, readResponse } from '../../lib/api';

export default function Register() {
  const [e, setE] = useState('');
  const [ok, setOk] = useState('');

  async function submit(x) {
    x.preventDefault();
    setE('');
    setOk('');

    const form = x.currentTarget;
    const f = new FormData(form);

    try {
      const r = await fetch(`${API}/auth/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: f.get('username'),
          email: f.get('email'),
          password: f.get('password')
        })
      });

      const { data, raw } = await readResponse(r);

      if (!r.ok) {
        throw new Error(
          getErrorMessage(
            data,
            raw,
            `Registration failed (HTTP ${r.status}).`
          )
        );
      }

      setOk('Account created. You can now sign in.');
      form.reset();
    } catch (a) {
      setE(a?.message || 'Unable to connect to the registration server.');
    }
  }

  return (
    <main className="auth">
      <div className="authCard">
        <div className="brand">Cyber<span>Guard</span></div>
        <p className="eyebrow">CREATE ACCOUNT</p>
        <h1>Start learning</h1>
        <p>No school affiliation is required.</p>

        <form onSubmit={submit}>
          <label>
            Username
            <input name="username" minLength="3" required />
          </label>

          <label>
            Email
            <input name="email" type="email" required />
          </label>

          <label>
            Password
            <input name="password" type="password" minLength="8" required />
          </label>

          <button className="button full">Create Account</button>
        </form>

        {ok && <p className="success">{ok}</p>}
        {e && <p className="error">{e}</p>}

        <p>
          Already registered? <Link href="/login">Sign in</Link>
        </p>
      </div>
    </main>
  );
}
