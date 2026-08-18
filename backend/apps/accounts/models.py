from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("admin", "Admin"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.username
