from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.accounts.models import Profile


class Command(BaseCommand):
    help = "Create missing CyberGuard profiles for all existing users."

    def handle(self, *args, **options):
        created = 0
        for user in User.objects.all().iterator():
            _, was_created = Profile.objects.get_or_create(
                user_id=user.pk,
                defaults={
                    "role": "admin" if user.is_staff or user.is_superuser else "user",
                    "points": 0,
                    "level": 1,
                },
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Profile check complete. Created {created} missing profile(s).")
        )
