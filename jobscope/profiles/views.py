from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Skill, Stack, Profile
from .serializers import ProfileSerializer, UpdateProfileSerializer
from platforms.models import JobPlatform
from resume_tools.models import ResumeTool
from communities.models import Community
from dashboard.models import UserActivity as UnifiedUserActivity
from django.utils import timezone

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = UpdateProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"})
        return Response(serializer.errors, status=400)

class SkillSearchView(APIView):
    def get(self, request):
        query = request.GET.get("search", "")
        skills = Skill.objects.filter(name__icontains=query)[:10]
        data = [{"id": s.id, "name": s.name} for s in skills]
        return Response(data)

class StackSearchView(APIView):
    def get(self, request):
        query = request.GET.get("search", "")
        stacks = Stack.objects.filter(name__icontains=query)[:10]
        data = [{"id": s.id, "name": s.name} for s in stacks]
        return Response(data)

class ActivityCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        atype = request.data.get("activity_type")
        oid = request.data.get("object_id")

        if atype and oid:
            tmap = {
                'platform_visit': 'platform',
                'resume_tool_use': 'resume',
                'community_join': 'community',
                'community_visit': 'community',
                'platform': 'platform',
                'resume': 'resume'
            }
            norm = tmap.get(atype, atype)
            UnifiedUserActivity.objects.update_or_create(
                user=request.user,
                activity_type=norm,
                object_id=oid,
                defaults={'visited_at': timezone.now()}
            )
            return Response({"message": "Activity logged"})
        return Response({"error": "Data required"}, status=400)