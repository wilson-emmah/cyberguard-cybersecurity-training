from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate_username(self, value):
        value = value.strip()
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Profile.objects.get_or_create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "points", "level", "role"]

    @staticmethod
    def get_profile(user):
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={
                "role": "admin" if user.is_staff or user.is_superuser else "user"
            },
        )
        return profile

    def get_points(self, user):
        return self.get_profile(user).points

    def get_level(self, user):
        return self.get_profile(user).level

    def get_role(self, user):
        return self.get_profile(user).role
