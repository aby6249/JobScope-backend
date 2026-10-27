from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, ForgotPasswordView, VerifyResetOTPView, ResetPasswordView,LogoutView, GoogleLoginView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('login/', LoginView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('verify-reset-otp/', VerifyResetOTPView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('logout/', LogoutView.as_view()),
    path("google-login/", GoogleLoginView.as_view()),
]