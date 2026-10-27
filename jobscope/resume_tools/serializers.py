from rest_framework import serializers
from .models import ResumeTool, ResumeToolReview, ResumeToolReaction


class ResumeToolSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResumeTool
        fields = "__all__"


class ResumeToolReviewSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = ResumeToolReview
        fields = [
            "id",
            "user",
            "tool",
            "rating",
            "comment",
            "created_at"
        ]


class ResumeToolReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResumeToolReaction
        fields = ["id", "tool", "reaction"]