# CyberGuard Migration Fix

The Render error `django.db.utils.ProgrammingError: relation "accounts_profile" does not exist`
means the Profile table was not present in PostgreSQL.

This package includes a deterministic `apps/accounts/migrations/0001_initial.py`
that creates `accounts_profile`, plus the `ensure_profiles` management command.

Render build command:
`pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py ensure_profiles && python manage.py collectstatic --noinput`

Important: if the old deployment has already recorded a broken `accounts` migration as applied,
do not manually delete the database. Inspect Render migration state first. If necessary,
the migration history may need to be repaired against the existing database before running
the new initial migration.

After deployment, verify `/healthz/`, then test `/api/auth/token/`, then `/api/auth/me/`
with a valid Bearer token.
