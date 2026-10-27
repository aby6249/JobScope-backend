from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Avg


from platforms.models import JobPlatform
from resume_tools.models import ResumeTool
from resume_tools.models import ResumeToolReview
from communities.models import Community
from platforms.models import PlatformReview

from profiles.models import Profile, Skill, Stack

User = get_user_model()



class AdminUserSerializer(serializers.ModelSerializer):

    bio = serializers.CharField(source="profile.bio", required=False)

    experience = serializers.CharField(
        source="profile.experience",
        required=False
    )

    stack = serializers.CharField(
        source="profile.stack.name",
        required=False
    )

    skills = serializers.SerializerMethodField()

    profile_picture = serializers.ImageField(
        source="profile.profile_picture",
        required=False
    )


    class Meta:

        model = User

        fields = [

            "id",

            "email",

            "username",

            "is_active",

            "is_verified",

            "created_at",

            "bio",

            "experience",

            "stack",

            "skills",

            "profile_picture"

        ]


    def get_skills(self, obj):

        if hasattr(obj, "profile"):

            return [

                skill.name

                for skill in obj.profile.skills.all()

            ]

        return []


    def update(self, instance, validated_data):

        profile_data = validated_data.pop(

            "profile",

            {}

        )


        instance.username = validated_data.get(

            "username",

            instance.username

        )

        instance.email = validated_data.get(

            "email",

            instance.email

        )

        instance.save()


        profile, created = Profile.objects.get_or_create(

            user=instance

        )


        profile.bio = profile_data.get(

            "bio",

            profile.bio

        )


        profile.experience = profile_data.get(

            "experience",

            profile.experience

        )


        stack_name = profile_data.get(

            "stack",

            None

        )

        if stack_name:

            stack, _ = Stack.objects.get_or_create(

                name=stack_name

            )

            profile.stack = stack


        skills_list = profile_data.get(

            "skills",

            None

        )

        if skills_list:

            skills = []

            for name in skills_list:

                skill, _ = Skill.objects.get_or_create(

                    name=name

                )

                skills.append(skill)

            profile.skills.set(skills)


        if "profile_picture" in profile_data:

            profile.profile_picture = profile_data[

                "profile_picture"

            ]


        profile.save()

        return instance



class AdminPlatformSerializer(serializers.ModelSerializer):

    class Meta:

        model = JobPlatform

        fields = "__all__"




class AdminPlatformDetailSerializer(serializers.ModelSerializer):

    average_rating = serializers.SerializerMethodField()

    total_reviews = serializers.SerializerMethodField()

    reviews = serializers.SerializerMethodField()

    good_count = serializers.SerializerMethodField()

    bad_count = serializers.SerializerMethodField()


    class Meta:

        model = JobPlatform

        fields = [

            "id",

            "name",

            "website_url",

            "description",

            "logo",

            "created_at",

            "average_rating",

            "total_reviews",

            "good_count",

            "bad_count",

            "reviews"

        ]


    def get_average_rating(self, obj):

        avg = obj.reviews.aggregate(

            avg=Avg("rating")

        )["avg"]

        return round(avg or 0, 1)


    def get_total_reviews(self, obj):

        return obj.reviews.count()


    def get_good_count(self, obj):

        return obj.reactions.filter(

            reaction="good"

        ).count()


    def get_bad_count(self, obj):

        return obj.reactions.filter(

            reaction="bad"

        ).count()


    def get_reviews(self, obj):

        reviews = PlatformReview.objects.filter(

            platform=obj

        )

        return [

            {

                "id": r.id,

                "user": r.user.username,

                "rating": r.rating,

                "comment": r.comment,

                "created_at": r.created_at

            }

            for r in reviews

        ]




class AdminResumeToolSerializer(serializers.ModelSerializer):

    class Meta:

        model = ResumeTool

        fields = "__all__"


class AdminResumeToolDetailSerializer(serializers.ModelSerializer):

    average_rating = serializers.SerializerMethodField()

    total_reviews = serializers.SerializerMethodField()

    reviews = serializers.SerializerMethodField()

    good_count = serializers.SerializerMethodField()

    bad_count = serializers.SerializerMethodField()


    class Meta:

        model = ResumeTool

        fields = [

            "id",

            "name",

            "website_url",

            "description",

            "logo",

            "created_at",

            "average_rating",

            "total_reviews",

            "good_count",

            "bad_count",

            "reviews"

        ]


    def get_average_rating(self, obj):

        avg = obj.reviews.aggregate(

            avg=Avg("rating")

        )["avg"]

        return round(avg or 0, 1)


    def get_total_reviews(self, obj):

        return obj.reviews.count()


    def get_good_count(self, obj):

        return obj.reactions.filter(

            reaction="good"

        ).count()


    def get_bad_count(self, obj):

        return obj.reactions.filter(

            reaction="bad"

        ).count()


    def get_reviews(self, obj):

        reviews = ResumeToolReview.objects.filter(

            tool=obj

        )

        return [

            {

                "id": r.id,

                "user": r.user.username,

                "rating": r.rating,

                "comment": r.comment,

                "created_at": r.created_at

            }

            for r in reviews

        ]



class AdminCommunitySerializer(serializers.ModelSerializer):

    created_by_username = serializers.CharField(

        source="created_by.username",

        read_only=True

    )

    class Meta:

        model = Community

        fields = [

            "id",

            "name",

            "bio",

            "reason",

            "logo",

            "is_approved",

            "is_admin_only",

            "created_at",

            "created_by_username"

        ]