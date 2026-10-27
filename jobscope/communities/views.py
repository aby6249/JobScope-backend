from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import Community, Membership, Message, CommentLike, Comment
from .serializers import CommunitySerializer, MessageSerializer, MembershipSerializer, CommentSerializer
from dashboard.models import UserActivity

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



def send_notification(user_id, message):

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "notify",
            "message": message
        }
    )



class CreateCommunityView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CommunitySerializer(data=request.data)

        if serializer.is_valid():

            community = serializer.save(
                created_by=request.user
            )

            Membership.objects.get_or_create(
                user=request.user,
                community=community,
                defaults={
                    "role": "admin"
                }
            )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "global_notifications",
                {
                    "type": "notify",
                    "message": "A new community is pending approval!"
                }
            )

            return Response({
                "message": "Community created, waiting admin approval"
            })

        return Response(serializer.errors)



class ApproveCommunityView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, id):

        community = get_object_or_404(
            Community,
            id=id
        )

        community.is_approved = True
        community.save()

        send_notification(
            community.created_by.id,
            "Your community has been approved"
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "global_notifications",
            {
                "type": "notify",
                "message": "A community has been approved"
            }
        )

        return Response({
            "message": "approved"
        })



class RejectCommunityView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, id):

        community = get_object_or_404(
            Community,
            id=id
        )

        send_notification(
            community.created_by.id,
            "Your community request rejected"
        )

        community.delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "global_notifications",
            {
                "type": "notify",
                "message": "A community request has been rejected"
            }
        )

        return Response({
            "message": "rejected"
        })



class ListCommunitiesView(APIView):

    def get(self, request):

        communities = Community.objects.filter(
            is_approved=True,
            is_deleted=False
        )

        serializer = CommunitySerializer(
            communities,
            many=True
        )

        return Response(serializer.data)



class CommunityDetailView(APIView):

    def get(self, request, id):

        community = get_object_or_404(
            Community,
            id=id,
            is_approved=True,
            is_deleted=False
        )

        UserActivity.objects.create(

            user=request.user,

            activity_type="community",

            object_id=community.id

        )
        

        members_count = Membership.objects.filter(
            community=community
        ).count()

        data = CommunitySerializer(community).data

        data["members_count"] = members_count

        return Response(data)



class JoinCommunityView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        community = get_object_or_404(
            Community,
            id=id,
            is_approved=True
        )

        membership, created = Membership.objects.get_or_create(
            user=request.user,
            community=community
        )

        return Response({
            "message": "joined",
            "created": created
        })




class LeaveCommunityView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, id):

        community = get_object_or_404(
            Community,
            id=id
        )

        if community.created_by == request.user:

            return Response({
                "error": "Community creator cannot leave community"
            })

        Membership.objects.filter(
            user=request.user,
            community_id=id
        ).delete()

        return Response({
            "message": "left"
        })



class UpdateCommunityView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, id):

        community = get_object_or_404(
            Community,
            id=id
        )

        membership = Membership.objects.filter(
            user=request.user,
            community=community
        ).first()

        if not membership or membership.role != "admin":

            return Response({
                "error": "Only community admin allowed"
            })

        serializer = CommunitySerializer(
            community,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)



class MakeAdminView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, community_id, user_id):

        membership = Membership.objects.filter(
            user=request.user,
            community_id=community_id
        ).first()

        if not membership or membership.role != "admin":

            return Response({
                "error": "Only admin allowed"
            })

        target = Membership.objects.get(
            community_id=community_id,
            user_id=user_id
        )

        target.role = "admin"
        target.save()

        return Response({
            "message": "new admin added"
        })




class RemoveMemberView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, community_id, user_id):

        community = get_object_or_404(
            Community,
            id=community_id
        )

        membership = Membership.objects.filter(
            user=request.user,
            community_id=community_id
        ).first()

        if not membership or membership.role != "admin":

            return Response({
                "error": "Only admin allowed"
            })

        if community.created_by.id == user_id:

            return Response({
                "error": "Cannot remove community creator"
            })

        Membership.objects.filter(
            user_id=user_id,
            community_id=community_id
        ).delete()

        return Response({
            "message": "member removed"
        })




class BlockUserView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, community_id, user_id):

        community = get_object_or_404(
            Community,
            id=community_id
        )

        membership = Membership.objects.filter(
            user=request.user,
            community_id=community_id
        ).first()

        if not membership or membership.role != "admin":

            return Response({
                "error": "Only admin allowed"
            })

        if community.created_by.id == user_id:

            return Response({
                "error": "Cannot block community creator"
            })

        target = Membership.objects.get(
            community_id=community_id,
            user_id=user_id
        )

        target.is_blocked = True
        target.save()

        return Response({
            "message": "user blocked"
        })




class UnblockUserView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, community_id, user_id):

        membership = Membership.objects.filter(
            user=request.user,
            community_id=community_id
        ).first()

        if not membership or membership.role != "admin":

            return Response({
                "error": "Only admin allowed"
            })

        target = Membership.objects.filter(
            community_id=community_id,
            user_id=user_id
        ).first()

        if not target:

            return Response({
                "error": "User not found"
            })

        target.is_blocked = False
        target.save()

        return Response({
            "message": "user unblocked"
        })




class AdminOnlyToggleView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, id):

        membership = Membership.objects.filter(
            user=request.user,
            community_id=id
        ).first()

        if not membership or membership.role != "admin":

            return Response({
                "error": "Only admin allowed"
            })

        community = Community.objects.get(id=id)

        community.is_admin_only = not community.is_admin_only

        community.save()

        return Response({
            "admin_only": community.is_admin_only
        })




class CommunityMessagesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        messages = Message.objects.filter(
            community_id=id
        ).order_by("created_at")

        serializer = MessageSerializer(
            messages,
            many=True
        )

        return Response(serializer.data)




class CommunityMembersView(APIView):

    def get(self, request, id):

        members = Membership.objects.filter(
            community_id=id
        )

        serializer = MembershipSerializer(
            members,
            many=True
        )

        return Response(serializer.data)




class MembershipStatusView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        membership = Membership.objects.filter(
            user=request.user,
            community_id=id
        ).first()

        if not membership:

            return Response({
                "joined": False
            })

        return Response({
            "joined": True,
            "role": membership.role,
            "blocked": membership.is_blocked
        })




class DeleteCommunityView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, id):

        community = get_object_or_404(
            Community,
            id=id
        )

        if community.created_by != request.user:

            return Response({
                "error": "Only creator can delete community"
            })

        community.delete()

        return Response({
            "message": "community deleted"
        })
    



class UpdateMessageView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, message_id):

        try:
            message = Message.objects.get(id=message_id)

        except Message.DoesNotExist:
            return Response(
                {"error": "Message not found"},
                status=404
            )

        if message.user != request.user:

            return Response(
                {"error": "Not allowed"},
                status=403
            )

        serializer = MessageSerializer(
            message,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"community_{message.community_id}",
                {
                    "type": "chat_message",
                    "action": "update",
                    "message_id": message.id,
                    "content": serializer.data.get("content")
                }
            )

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )


class DeleteMessageView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, message_id):

        try:
            message = Message.objects.get(id=message_id)

        except Message.DoesNotExist:

            return Response(
                {"error": "Message not found"},
                status=404
            )

        if message.user != request.user:

            return Response(
                {"error": "Not allowed"},
                status=403
            )

        community_id = message.community_id
        message_id = message.id
        message.delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"community_{community_id}",
            {
                "type": "chat_message",
                "action": "delete",
                "message_id": message_id
            }
        )

        return Response(
            {"message": "Deleted successfully"}
        )


class RemoveAdminRoleView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, community_id, user_id):

        try:
            community = Community.objects.get(id=community_id)

            target_membership = Membership.objects.get(
                community_id=community_id,
                user_id=user_id
            )

            requester_membership = Membership.objects.get(
                community_id=community_id,
                user=request.user
            )

        except Membership.DoesNotExist:

            return Response(
                {"error": "Membership not found"},
                status=404
            )

        if requester_membership.role != "admin":

            return Response(
                {"error": "Only admin can change roles"},
                status=403
            )

        if community.created_by_id == user_id:

            return Response(
                {"error": "Cannot change creator role"},
                status=400
            )

        target_membership.role = "member"

        target_membership.save()

        return Response(
            {"message": "Admin role removed"}
        )
    

class CreateCommentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, message_id):

        try:

            message = Message.objects.get(id=message_id)

        except Message.DoesNotExist:

            return Response(
                {"error": "Message not found"},
                status=404
            )

        membership = Membership.objects.filter(
            user=request.user,
            community=message.community,
            is_blocked=False
        ).first()

        if not membership:

            return Response(
                {"error": "Not allowed"},
                status=403
            )

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(
                user=request.user,
                message=message
            )

            return Response(serializer.data)

        return Response(serializer.errors, status=400)



class MessageCommentsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, message_id):

        comments = Comment.objects.filter(
            message_id=message_id
        ).order_by("created_at")

        serializer = CommentSerializer(
            comments,
            many=True
        )

        return Response(serializer.data)



class UpdateCommentView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, comment_id):

        try:

            comment = Comment.objects.get(id=comment_id)

        except Comment.DoesNotExist:

            return Response(
                {"error": "Comment not found"},
                status=404
            )

        if comment.user != request.user:

            return Response(
                {"error": "Not allowed"},
                status=403
            )

        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=400)



class DeleteCommentView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):

        try:

            comment = Comment.objects.get(id=comment_id)

        except Comment.DoesNotExist:

            return Response(
                {"error": "Comment not found"},
                status=404
            )

        if comment.user != request.user:

            return Response(
                {"error": "Not allowed"},
                status=403
            )

        comment.delete()

        return Response(
            {"message": "Comment deleted"}
        )



class LikeCommentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):

        try:
            comment = Comment.objects.get(id=comment_id)

        except Comment.DoesNotExist:

            return Response(
                {"error": "Comment not found"},
                status=404
            )

        message = comment.message


        if message.user != request.user:

            return Response(
                {"error": "Only question owner can react"},
                status=403
            )

        existing_like = CommentLike.objects.filter(
            user=request.user,
            comment=comment
        ).first()


        if existing_like:

            existing_like.delete()

            return Response({
                "message": "unliked",
                "liked": False,
                "like_count": comment.likes.count()
            })

        CommentLike.objects.create(
            user=request.user,
            comment=comment
        )

        return Response({
            "message": "liked",
            "liked": True,
            "like_count": comment.likes.count()
        })