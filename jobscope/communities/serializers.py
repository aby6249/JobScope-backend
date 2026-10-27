from rest_framework import serializers
from .models import Community, Membership, Message, Notification, Comment, CommentLike


class CommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = "__all__"
        read_only_fields = ["created_by", "is_approved", "is_admin_only", "created_at"]


class MembershipSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = [
            "id",
            "user",
            "username",
            "community",
            "role",
            "is_blocked",
            "joined_at"
        ]

    def get_username(self, obj):

        if hasattr(obj.user, "username") and obj.user.username:
            return obj.user.username

        return obj.user.email.split("@")[0]


class MessageSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "username",
            "content",
            "image",
            "reply_to",
            "created_at"
        ]

    def get_username(self, obj):

        # if username field exists
        if hasattr(obj.user, "username") and obj.user.username:
            return obj.user.username

        # fallback → extract name from email
        if obj.user.email:
            return obj.user.email.split("@")[0]

        # last fallback
        return "user"



class NotificationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Notification

        fields = [
            "id",
            "user",
            "message",
            "related_community",
            "is_read",
            "created_at"
        ]

        read_only_fields = [
            "created_at"
        ]


class CommentSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()

    like_count = serializers.SerializerMethodField()

    class Meta:

        model = Comment

        fields = [
            "id",
            "message",
            "username",
            "content",
            "created_at",
            "like_count"
        ]


    def get_username(self, obj):

        if hasattr(obj.user, "username") and obj.user.username:

            return obj.user.username

        return obj.user.email.split("@")[0]


    def get_like_count(self, obj):

        return obj.likes.count()