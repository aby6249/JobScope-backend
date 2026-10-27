from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from platforms.models import JobPlatform
from resume_tools.models import ResumeTool
from communities.models import Community

from .models import UserActivity


class UserDashboardView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = request.user

        total_platforms = JobPlatform.objects.count()
        total_resume_tools = ResumeTool.objects.count()
        total_communities = Community.objects.filter(is_approved=True, is_deleted=False).count()

        all_activity = UserActivity.objects.filter(
            user=user,
            activity_type__in=["platform", "resume", "platform_visit", "resume_visit", "resume_tool_use"]
        ).order_by("-visited_at")
        
        recent_items = []
        seen_keys = set()
        
        type_norm = {
            "platform_visit": "platform",
            "resume_visit": "resume",
            "resume_tool_use": "resume",
            "platform": "platform",
            "resume": "resume"
        }

        for act in all_activity:
            if len(recent_items) >= 5:
                break
            
            ntype = type_norm.get(act.activity_type, act.activity_type)
            key = (ntype, act.object_id)
            if key in seen_keys:
                continue
                
            try:
                if ntype == "platform":
                    obj = JobPlatform.objects.get(id=act.object_id)
                    recent_items.append({
                        "type": "platform", "id": obj.id, "name": obj.name,
                        "logo": obj.logo.url if obj.logo else None
                    })
                elif ntype == "resume":
                    obj = ResumeTool.objects.get(id=act.object_id)
                    recent_items.append({
                        "type": "resume", "id": obj.id, "name": obj.name,
                        "logo": obj.logo.url if obj.logo else None
                    })
                seen_keys.add(key)
            except: continue

        all_comm_act = UserActivity.objects.filter(
            user=user,
            activity_type__in=["community", "community_visit", "community_join"]
        ).order_by("-visited_at")
        
        recent_communities = []
        seen_comm_ids = set()
        
        for act in all_comm_act:
            if len(recent_communities) >= 5:
                break
                
            if act.object_id in seen_comm_ids:
                continue
                
            try:
                c = Community.objects.get(id=act.object_id, is_deleted=False)
                recent_communities.append({
                    "id": c.id, "name": c.name,
                    "logo": c.logo.url if c.logo else None
                })
                seen_comm_ids.add(act.object_id)
            except: continue

        return Response({
            "total_platforms": total_platforms,
            "total_resume_tools": total_resume_tools,
            "total_communities": total_communities,
            "recent_activity": recent_items,
            "recent_community": recent_communities
        })
