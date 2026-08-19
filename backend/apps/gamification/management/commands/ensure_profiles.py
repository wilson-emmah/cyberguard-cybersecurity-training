from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.accounts.models import Profile


class Command(BaseCommand):
    help = "Create missing profiles for existing users."

    def handle(self, *args, **options):
        created = 0
        for user in User.objects.all().iterator():
            _, was_created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    "role": "admin"
                    if user.is_staff or user.is_superuser
                    else "user"
                },
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Profiles created: {created}"
            )
        )
