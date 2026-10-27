from django.urls import path
from .views import PlatformListView, PlatformDetailView, CreateReviewView, UpdateReviewView ,DeleteReviewView, PlatformReactionView

urlpatterns = [

    path("platforms/", PlatformListView.as_view()),
    path("platforms/<int:pk>/", PlatformDetailView.as_view()),
    path("platforms/review/", CreateReviewView.as_view()),
    path("platforms/review/<int:pk>/update/", UpdateReviewView.as_view()),
    path("platforms/review/<int:pk>/delete/", DeleteReviewView.as_view()),
    path("platforms/platform-reaction/", PlatformReactionView.as_view()),
]