from django.core.management.base import BaseCommand
from django.db import connection

from apps.accounts.models import Profile


class Command(BaseCommand):
    help = "Create the Profile table if it is missing from the database."

    def handle(self, *args, **options):
        table_name = Profile._meta.db_table
        existing_tables = connection.introspection.table_names()

        if table_name in existing_tables:
            self.stdout.write(
                self.style.SUCCESS(f"Profile table exists: {table_name}")
            )
            return

        self.stdout.write(
            self.style.WARNING(
                f"Profile table is missing: {table_name}. Creating it now..."
            )
        )

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Profile)

        self.stdout.write(
            self.style.SUCCESS(f"Created table: {table_name}")
        )
