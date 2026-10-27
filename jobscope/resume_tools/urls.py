from django.urls import path
from .views import ResumeToolListView, ResumeToolDetailView, CreateResumeToolReviewView, UpdateResumeToolReviewView ,DeleteResumeToolReviewView, ResumeToolReactionView


urlpatterns = [

    path("resume-tools/", ResumeToolListView.as_view()),
    path("resume-tools/<int:pk>/", ResumeToolDetailView.as_view()),
    path("resume-tools/review/", CreateResumeToolReviewView.as_view()),
    path("resume-tools/review/<int:pk>/update/", UpdateResumeToolReviewView.as_view()),
    path("resume-tools/review/<int:pk>/delete/", DeleteResumeToolReviewView.as_view()),
    path("resume-tools/reaction/", ResumeToolReactionView.as_view()),
]