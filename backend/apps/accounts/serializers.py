from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'An account with this email already exists.'
            )
        return value.lower()

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        # Make sure every registered user has a profile
        Profile.objects.get_or_create(user=user)

        return user


class UserSerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'points', 'level', 'role']

    def get_profile(self, user):
        return Profile.objects.get_or_create(user=user)[0]

    def get_points(self, user):
        return self.get_profile(user).points

    def get_level(self, user):
        return self.get_profile(user).level

    def get_role(self, user):
        return self.get_profile(user).role
