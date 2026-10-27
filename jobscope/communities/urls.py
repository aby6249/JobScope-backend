from django.urls import path

from .views import (

    CreateCommunityView,
    ApproveCommunityView,
    RejectCommunityView,

    ListCommunitiesView,
    CommunityDetailView,

    JoinCommunityView,
    LeaveCommunityView,

    UpdateCommunityView,

    BlockUserView,
    RemoveMemberView,

    MakeAdminView,

    AdminOnlyToggleView,

    CommunityMessagesView,
    CommunityMembersView,
    MembershipStatusView,
    UnblockUserView,
    DeleteCommunityView,
    UpdateMessageView,
    DeleteMessageView,
    RemoveAdminRoleView,

    CreateCommentView,
    MessageCommentsView,
    UpdateCommentView,
    DeleteCommentView,
    LikeCommentView
)


urlpatterns = [

    path("create/", CreateCommunityView.as_view()),

    path("", ListCommunitiesView.as_view()),

    path("<int:id>/", CommunityDetailView.as_view()),

    path("<int:id>/update/", UpdateCommunityView.as_view()),

    path("<int:id>/join/", JoinCommunityView.as_view()),

    path("<int:id>/leave/", LeaveCommunityView.as_view()),

    path("<int:community_id>/block/<int:user_id>/",BlockUserView.as_view()),

    path("<int:community_id>/remove/<int:user_id>/",RemoveMemberView.as_view()),

    path("<int:community_id>/make-admin/<int:user_id>/",MakeAdminView.as_view()),

    path("<int:id>/admin-only/",AdminOnlyToggleView.as_view()),

    path("<int:id>/approve/",ApproveCommunityView.as_view()),

    path("<int:id>/reject/",RejectCommunityView.as_view()),

    path("<int:id>/messages/", CommunityMessagesView.as_view()),

    path("<int:id>/members/", CommunityMembersView.as_view()),

    path("<int:id>/status/", MembershipStatusView.as_view()),

    path("<int:community_id>/unblock/<int:user_id>/",UnblockUserView.as_view()),

    path("<int:id>/delete/",DeleteCommunityView.as_view()),

    path("message/<int:message_id>/update/",UpdateMessageView.as_view()),

    path("message/<int:message_id>/delete/",DeleteMessageView.as_view()),

    path("<int:community_id>/remove-admin/<int:user_id>/",RemoveAdminRoleView.as_view()),

    path("message/<int:message_id>/comment/",CreateCommentView.as_view()),

    path("message/<int:message_id>/comments/",MessageCommentsView.as_view()),

    path("comment/<int:comment_id>/update/",UpdateCommentView.as_view()),

    path("comment/<int:comment_id>/delete/",DeleteCommentView.as_view()),

    path("comment/<int:comment_id>/like/",LikeCommentView.as_view()),

]