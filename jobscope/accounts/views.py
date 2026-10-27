from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, VerifyOTPSerializer, LoginSerializer, ForgotPasswordSerializer, VerifyResetOTPSerializer, ResetPasswordSerializer,LogoutSerializer

from .google_auth import verify_google_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model



User = get_user_model()


class RegisterView(APIView):

    def post(self, request):
     

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({
                "message": "OTP sent to email"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):

    def post(self, request):


        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({
                "message": "Account verified successfully"
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)

        return Response(serializer.errors, status=400)
    




class ForgotPasswordView(APIView):

    def post(self, request):

        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyResetOTPView(APIView):

    def post(self, request):

        serializer = VerifyResetOTPSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):

    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            result = serializer.save()  
            return Response(result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class LogoutView(APIView):

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data)

        return Response(serializer.errors, status=400)
    



class GoogleLoginView(APIView):
    def post(self,request):

        token=request.data.get("token")

        if not token:
            return Response({"error":"Token required"},status=400)
        
        google_user=verify_google_token(token)

        if not google_user:
            return Response({"error":"Invalid Google token"},status=400)
        
        email= google_user["email"]
        name=google_user["name"]

        user,created= User.objects.get_or_create(
            email=email,
            defaults={
                "username":name,
                "is_verified": True,
                "is_active":True
            }
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh":str(refresh),
            "access": str(refresh.access_token),
            "email":user.email,
            "username":user.username
        })