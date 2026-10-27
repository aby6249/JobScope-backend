from django.contrib import admin
from .models import JobPlatform, PlatformReview, PlatformReaction


@admin.register(JobPlatform)
class JobPlatformAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "website_url", "created_at")


@admin.register(PlatformReview)
class PlatformReviewAdmin(admin.ModelAdmin):

    list_display = ("id", "user", "platform", "rating", "created_at")


admin.site.register(PlatformReaction)

