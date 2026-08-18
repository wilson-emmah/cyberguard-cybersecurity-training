from django.db import migrations, models
import django.db.models.deletion


def create_profiles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("accounts", "Profile")
    for user in User.objects.all().iterator():
        Profile.objects.get_or_create(
            user_id=user.pk,
            defaults={
                "role": "admin" if user.is_staff or user.is_superuser else "user",
                "points": 0,
                "level": 1,
            },
        )


def reverse_profiles(apps, schema_editor):
    Profile = apps.get_model("accounts", "Profile")
    Profile.objects.all().delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("user", "User"), ("admin", "Admin")], default="user", max_length=20)),
                ("points", models.PositiveIntegerField(default=0)),
                ("level", models.PositiveIntegerField(default=1)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to="auth.user")),
            ],
        ),
        migrations.RunPython(create_profiles, reverse_profiles),
    ]
