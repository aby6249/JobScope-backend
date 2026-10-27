from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from platforms.models import JobPlatform
from resume_tools.models import ResumeTool
from communities.models import Community
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .serializers import (
    AdminUserSerializer,
    AdminPlatformSerializer,
    AdminResumeToolSerializer,
    AdminCommunitySerializer,
    AdminPlatformDetailSerializer,
    AdminResumeToolDetailSerializer
)


User = get_user_model()



class AdminDashboardView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        data = {

            "total_users":
            User.objects.filter(is_staff=False).count(),

            "total_platforms":
            JobPlatform.objects.count(),

            "total_resume_tools":
            ResumeTool.objects.count(),

            "total_communities":
            Community.objects.count(),

            "pending_communities":
            Community.objects.filter(
                is_approved=False
            ).count(),


            "recent_users":
            list(
                User.objects
                .filter(is_staff=False)
                .order_by("-created_at")
                .values(
                    "id",
                    "email",
                    "username",
                    "created_at"
                )[:5]
            ),


            "recent_communities":
            [
                {
                    "id": c.id,
                    "name": c.name,
                    "created_by": {
                        "id": c.created_by.id,
                        "username": c.created_by.username
                    },
                    "is_approved": c.is_approved,
                    "created_at": c.created_at
                }

                for c in Community.objects
                .select_related("created_by")
                .order_by("-created_at")[:5]
            ]
        }

        return Response(data)




class AdminUserListView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        users = User.objects.all()

        serializer = AdminUserSerializer(
            users,
            many=True
        )

        return Response(serializer.data)



class AdminUserUpdateView(APIView):

    permission_classes = [IsAdminUser]

    def put(self, request, id):

        user = get_object_or_404(User, id=id)

        serializer = AdminUserSerializer(

            user,

            data=request.data,

            partial=True

        )

        if serializer.is_valid():

            serializer.save()

            return Response({

                "message":

                "User profile updated successfully"

            })

        return Response(serializer.errors)



class AdminUserDetailView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, id):

        user = get_object_or_404(

            User,

            id=id

        )

        serializer = AdminUserSerializer(user)

        return Response(serializer.data)


class BlockUserView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, id):

        user = get_object_or_404(User, id=id)

        user.is_active = False

        user.save()

        return Response({
            "message": "user blocked"
        })



class UnblockUserView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, id):

        user = get_object_or_404(User, id=id)

        user.is_active = True

        user.save()

        return Response({
            "message": "user unblocked"
        })




class AdminPlatformListView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        platforms = JobPlatform.objects.annotate(

            avg_rating=Avg("reviews__rating")

        )

        data = []

        for p in platforms:

            data.append({

                "id": p.id,

                "name": p.name,

                "website_url": p.website_url,

                "average_rating":

                round(p.avg_rating or 0, 1),

                "total_reviews":

                p.reviews.count(),

                "good_count":

                p.reactions.filter(

                    reaction="good"

                ).count(),

                "bad_count":

                p.reactions.filter(

                    reaction="bad"

                ).count()

            })

        return Response(data)




class AdminPlatformDetailView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, id):

        platform = get_object_or_404(

            JobPlatform,

            id=id

        )

        serializer = AdminPlatformDetailSerializer(

            platform

        )

        return Response(serializer.data)
    


class AdminPlatformCreateView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):

        serializer = AdminPlatformSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)



class AdminPlatformUpdateView(APIView):

    permission_classes = [IsAdminUser]

    def put(self, request, id):

        platform = get_object_or_404(
            JobPlatform,
            id=id
        )

        serializer = AdminPlatformSerializer(
            platform,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)



class AdminPlatformDeleteView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, id):

        platform = get_object_or_404(
            JobPlatform,
            id=id
        )

        platform.delete()

        return Response({
            "message": "platform deleted"
        })




class AdminResumeToolListView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        tools = ResumeTool.objects.annotate(

            avg_rating=Avg("reviews__rating")

        )

        data = []

        for t in tools:

            data.append({

                "id": t.id,

                "name": t.name,

                "website_url": t.website_url,

                "average_rating":

                round(t.avg_rating or 0, 1),

                "total_reviews":

                t.reviews.count(),

                "good_count":

                t.reactions.filter(

                    reaction="good"

                ).count(),

                "bad_count":

                t.reactions.filter(

                    reaction="bad"

                ).count()

            })

        return Response(data)


class AdminResumeToolDetailView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, id):

        tool = get_object_or_404(

            ResumeTool,

            id=id

        )

        serializer = AdminResumeToolDetailSerializer(

            tool

        )

        return Response(serializer.data)
    


class AdminResumeToolCreateView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):

        serializer = AdminResumeToolSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)



class AdminResumeToolUpdateView(APIView):

    permission_classes = [IsAdminUser]

    def put(self, request, id):

        tool = get_object_or_404(
            ResumeTool,
            id=id
        )

        serializer = AdminResumeToolSerializer(
            tool,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)



class AdminResumeToolDeleteView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, id):

        tool = get_object_or_404(
            ResumeTool,
            id=id
        )

        tool.delete()

        return Response({
            "message": "tool deleted"
        })



class PendingCommunityListView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        communities = Community.objects.filter(
            is_approved=False
        )

        serializer = AdminCommunitySerializer(
            communities,
            many=True
        )

        return Response(serializer.data)



class AllCommunityListView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        communities = Community.objects.filter(

            is_deleted=False

        )

        serializer = AdminCommunitySerializer(

            communities,

            many=True

        )

        return Response(serializer.data)
    


class DeleteCommunityAdminView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, id):

        community = get_object_or_404(

            Community,

            id=id

        )

        community.is_deleted = True

        community.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "global_notifications",
            {
                "type": "notify",
                "message": "A community has been archived"
            }
        )

        return Response({

            "message":

            "Community moved to archive"

        })
    


class RestoreCommunityView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, id):

        community = get_object_or_404(

            Community,

            id=id,

            is_deleted=True

        )

        community.is_deleted = False

        community.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "global_notifications",
            {
                "type": "notify",
                "message": "A community has been restored"
            }
        )

        return Response({

            "message":

            "Community restored"

        })
    


class ArchivedCommunityListView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        communities = Community.objects.filter(

            is_deleted=True

        )

        data = [

            {

                "id": c.id,

                "name": c.name,

                "created_by": c.created_by.username,

                "created_at": c.created_at

            }

            for c in communities

        ]

        return Response(data)