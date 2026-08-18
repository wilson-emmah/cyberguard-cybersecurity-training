# CyberGuard deployment fixes

This package fixes the Django/Next.js production authentication path.

## Render

Use the existing Render service and redeploy from GitHub. The build command runs:

`python manage.py migrate --noinput`

The package now contains initial migrations for `accounts`, `training`, and `gamification`, including a data migration that creates profiles for existing Django users.

Required Render variables:

- `DJANGO_SECRET_KEY` — keep private; rotate the old value if it was exposed.
- `DEBUG=False`
- `ALLOWED_HOSTS=cyberguard-cybersecurity-training.onrender.com`
- `FRONTEND_URL=https://cyberguard-cybersecurity-training.vercel.app`
- `DATABASE_URL=<your private Render PostgreSQL URL>`

## Vercel

Set this environment variable for Production (and Preview if desired):

`NEXT_PUBLIC_API_URL=https://cyberguard-cybersecurity-training.onrender.com/api`

Then redeploy the Vercel project.

## Test endpoints

- `GET /healthz/` should return `{"status":"ok"}`.
- `POST /api/auth/token/` should return `access` and `refresh` tokens.
- `GET /api/auth/me/` without a token should return HTTP 401. That is expected.
- With `Authorization: Bearer <access-token>`, `/api/auth/me/` should return the user profile.

## Important security note

Do not commit `DATABASE_URL`, `DJANGO_SECRET_KEY`, or `GEMINI_API_KEY` to GitHub. Rotate any credential that was exposed in screenshots, chat, logs, or source control.
