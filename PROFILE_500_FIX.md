# CyberGuard: Profile 500 fix

This version specifically addresses the frontend error:

`Profile request failed (500)`

## Why

The login endpoint can successfully issue a JWT while `/api/auth/me/` fails when an authenticated user has no `Profile` row, or when an older database deployment has not backfilled profiles.

## What is included

- `apps/accounts/signals.py` creates a profile for new users.
- `apps/accounts/migrations/0001_initial.py` creates the Profile table and backfills users on a fresh migration.
- `apps/accounts/migrations/0002_backfill_profiles.py` backfills profiles on databases where migration 0001 was already applied.
- `ensure_profiles` management command provides an additional safe backfill step.
- Render build command runs `migrate`, `ensure_profiles`, then `collectstatic`.
- `UserSerializer` uses `get_or_create()` so missing profiles do not cause an AttributeError.
- JWT `/api/auth/me/` remains protected with `IsAuthenticated`.

## Render

Build command:

`pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py ensure_profiles && python manage.py collectstatic --noinput`

Start command:

`gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

## Vercel

Production environment variable:

`NEXT_PUBLIC_API_URL=https://cyberguard-cybersecurity-training.onrender.com/api`

After changing it, redeploy Vercel.

## Test

1. `GET /healthz/` -> HTTP 200 and `{"status":"ok"}`.
2. `POST /api/auth/token/` -> HTTP 200 with `access` and `refresh`.
3. Login through Vercel.
4. The frontend sends `Authorization: Bearer <access>` to `/api/auth/me/`.
5. `/api/auth/me/` should return `id`, `username`, `email`, `points`, `level`, and `role`.

## Security

Rotate any database password, Django secret, or Gemini API key that was exposed in screenshots or chat. Keep secrets only in Render/Vercel environment variables, never in GitHub.
