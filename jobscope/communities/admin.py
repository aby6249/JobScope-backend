from django.contrib import admin

from .models import (
    Community,
    Membership,
    Message,
    Notification
)



@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "created_by",
        "is_approved",
        "created_at"
    )

    list_filter = (
        "is_approved",
        "created_at"
    )

    search_fields = (
        "name",
        "created_by__email"
    )

    actions = ["approve_community"]


    def approve_community(self, request, queryset):

        queryset.update(is_approved=True)



@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "community",
        "role",
        "is_blocked"
    )



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "community",
        "created_at"
    )



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "message",
        "is_read",
        "created_at"
    )