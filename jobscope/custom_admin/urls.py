from django.urls import path

from .views import (

    AdminDashboardView,

    AdminUserListView,
    AdminUserUpdateView,
    BlockUserView,
    UnblockUserView,
    AdminUserDetailView,

    AdminPlatformListView,
    AdminPlatformCreateView,
    AdminPlatformUpdateView,
    AdminPlatformDeleteView,
    AdminPlatformDetailView,

    AdminResumeToolListView,
    AdminResumeToolCreateView,
    AdminResumeToolUpdateView,
    AdminResumeToolDeleteView,
    AdminResumeToolDetailView,

    PendingCommunityListView,
    AllCommunityListView,
    DeleteCommunityAdminView,
    ArchivedCommunityListView,
    RestoreCommunityView
)


urlpatterns = [

    # dashboard
    path(
        "dashboard/",
        AdminDashboardView.as_view()
    ),


    # users
    path(
        "users/",
        AdminUserListView.as_view()
    ),

    path(
        "users/<int:id>/update/",
        AdminUserUpdateView.as_view()
    ),

    path(
        "users/<int:id>/block/",
        BlockUserView.as_view()
    ),

    path(
        "users/<int:id>/unblock/",
        UnblockUserView.as_view()
    ),


    path(
        "platforms/",
        AdminPlatformListView.as_view()
    ),

    path(
        "platforms/create/",
        AdminPlatformCreateView.as_view()
    ),

    path(
        "platforms/<int:id>/",
        AdminPlatformDetailView.as_view()
    ),

    path(
        "platforms/<int:id>/update/",
        AdminPlatformUpdateView.as_view()
    ),

    path(
        "platforms/<int:id>/delete/",
        AdminPlatformDeleteView.as_view()
    ),


    path(
        "resume-tools/",
        AdminResumeToolListView.as_view()
    ),

    path(
        "resume-tools/<int:id>/",
         AdminResumeToolDetailView.as_view()
    ),

    path(
        "resume-tools/create/",
        AdminResumeToolCreateView.as_view()
    ),

    path(
        "resume-tools/<int:id>/update/",
        AdminResumeToolUpdateView.as_view()
    ),

    path(
        "resume-tools/<int:id>/delete/",
        AdminResumeToolDeleteView.as_view()
    ),

    path(
        "communities/",
        AllCommunityListView.as_view()
    ),

    path(
        "communities/pending/",
        PendingCommunityListView.as_view()
    ),

    path(
        "users/<int:id>/",
         AdminUserDetailView.as_view()
    ),

    path(
        "communities/<int:id>/delete/",
        DeleteCommunityAdminView.as_view()
    ),

    path(
        "communities/archived/",
        ArchivedCommunityListView.as_view()
    ),

    path(
        "communities/<int:id>/restore/",
        RestoreCommunityView.as_view()
    ),
]