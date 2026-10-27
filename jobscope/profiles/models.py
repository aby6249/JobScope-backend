from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Stack(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):

    EXPERIENCE_CHOICES = [
        ("0-1", "0-1 Years"),
        ("1-2", "1-2 Years"),
        ("2-3", "2-3 Years"),
        ("3-4", "3-4 Years"),
        ("4-5", "4-5 Years"),
        ("5+", "5+ Years"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    bio = models.TextField(blank=True)

    stack = models.ForeignKey(Stack, on_delete=models.SET_NULL, null=True, blank=True)

    skills = models.ManyToManyField(Skill, blank=True)

    experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, blank=True)

    profile_picture = models.ImageField(upload_to="profiles/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class UserActivity(models.Model):

    ACTIVITY_TYPES = [
        ("platform_visit", "Visited Platform"),
        ("resume_tool_use", "Used Resume Tool"),
        ("community_join", "Joined Community"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")

    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)

    details = models.CharField(max_length=255)  # e.g., "Visited LinkedIn Platform"

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.details}"