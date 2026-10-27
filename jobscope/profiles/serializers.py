from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Skill, Stack

User = get_user_model()


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ["id", "name"]


class StackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stack
        fields = ["id", "name"]


class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source="user.username")

    email = serializers.EmailField(source="user.email", read_only=True)

    skills = SkillSerializer(many=True, read_only=True)

    stack = StackSerializer(read_only=True)

    is_profile_complete = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "username",
            "email",
            "bio",
            "stack",
            "skills",
            "experience",
            "profile_picture",
            "created_at",
            "is_profile_complete"
        ]

    def get_is_profile_complete(self, obj):

        if obj.bio and obj.stack and obj.skills.exists() and obj.experience:
            return True
        return False



class UpdateProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source="user.username", required=False)

    skill_names = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    stack_name = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = [
            "username",
            "bio",
            "stack_name",
            "skill_names",
            "experience",
            "profile_picture",
        ]

    def update(self, instance, validated_data):

        user_data = validated_data.pop("user", {})
        skill_names = validated_data.pop("skill_names", [])
        stack_name = validated_data.pop("stack_name", None)

        if "username" in user_data:
            instance.user.username = user_data["username"]
            instance.user.save()

        if stack_name:
            stack, _ = Stack.objects.get_or_create(name=stack_name)
            instance.stack = stack

        if skill_names:
            skills = []
            for name in skill_names:
                skill, _ = Skill.objects.get_or_create(name=name)
                skills.append(skill)

            instance.skills.set(skills)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance