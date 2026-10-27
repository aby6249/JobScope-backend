from django.urls import path
from .views import ProfileView, SkillSearchView, StackSearchView, ActivityCreateView
from dashboard.views import UserDashboardView

urlpatterns = [
    path("profile/", ProfileView.as_view()),
    path("skills/", SkillSearchView.as_view()),
    path("stacks/", StackSearchView.as_view()),
    path("dashboard/", UserDashboardView.as_view()),
    path("activities/log/", ActivityCreateView.as_view()),
]