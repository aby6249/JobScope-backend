from django.contrib import admin
from .models import ResumeTool, ResumeToolReview, ResumeToolReaction


@admin.register(ResumeTool)
class ResumeToolAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "website_url", "created_at")


@admin.register(ResumeToolReview)
class ResumeToolReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "tool", "rating", "created_at")


admin.site.register(ResumeToolReaction)