from rest_framework import serializers
from .models import JobPlatform, PlatformReview, PlatformReaction


class JobPlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobPlatform
        fields = "__all__"


class PlatformReviewSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = PlatformReview
        fields = [
            "id",
            "user",
            "platform",
            "rating",
            "comment",
            "created_at"
        ]

class PlatformReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlatformReaction
        fields = ["id", "platform", "reaction"]
    

