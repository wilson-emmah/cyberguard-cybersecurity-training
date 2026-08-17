# CyberGuard
Public cybersecurity training platform. Open to everyone; not school-specific.

## Frontend / Vercel
Root Directory: `frontend`
Framework: Next.js
Install: `npm install`
Build: `npm run build`
Output Directory: leave default for Next.js (`.next`). Do NOT set it to `public`.
Environment: `NEXT_PUBLIC_API_URL=https://cybersecurity-training-platform.onrender.com/api`

## Backend / Render
Root Directory: `backend`
Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
Start: `gunicorn config.wsgi:application`
Health: `/healthz/`

Required Render environment variables:
DJANGO_SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, DATABASE_URL, FRONTEND_URL

After first deployment run:
python manage.py migrate
python manage.py createsuperuser
