from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField()),
                ("category", models.CharField(max_length=100)),
                ("published", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Scenario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("scenario_type", models.CharField(choices=[("phishing", "Phishing"), ("url", "Suspicious URL"), ("password", "Password Security"), ("malware", "Malware")], max_length=20)),
                ("description", models.TextField()),
                ("prompt", models.TextField()),
                ("choices", models.JSONField(default=list)),
                ("correct_choice", models.PositiveIntegerField()),
                ("explanation", models.TextField()),
                ("points", models.PositiveIntegerField(default=100)),
                ("published", models.BooleanField(default=True)),
                ("course", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="training.course")),
            ],
        ),
        migrations.CreateModel(
            name="Attempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("selected_choice", models.PositiveIntegerField()),
                ("correct", models.BooleanField()),
                ("points_awarded", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("scenario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="training.scenario")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="auth.user")),
            ],
        ),
    ]
