from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .utils import generate_otp, send_otp_email, store_otp_data, get_otp_data, delete_otp_data, store_reset_otp, get_reset_otp, delete_reset_otp
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



User = get_user_model()


class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")

        email = data['email'].lower()
        data['email'] = email

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User already exists")

        return data

    def create(self, validated_data):

        username = validated_data['username']
        email = validated_data['email']
        password = make_password(validated_data['password'])

        otp = generate_otp()

        store_otp_data(email, username, password, otp)

        send_otp_email(email, otp)

        return validated_data


class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):

        email = data['email'].lower()
        otp = data['otp']

        otp_data = get_otp_data(email)

        if not otp_data:
            raise serializers.ValidationError("OTP expired or not found")

        if otp_data['otp'] != otp:
            raise serializers.ValidationError("Invalid OTP")

        data['email'] = email
        data['otp_data'] = otp_data

        return data

    def create(self, validated_data):

        email = validated_data['email']
        otp_data = validated_data['otp_data']

        user = User.objects.create(
            email=email,
            username=otp_data['username'],
            password=otp_data['password'],
            is_verified=True,
            is_active=True
        )


        delete_otp_data(email)

        return user
    



class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        email = data['email'].lower()
        password = data['password']

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_verified:
            raise serializers.ValidationError("Account not verified")

        refresh = RefreshToken.for_user(user)

        return {
           "refresh": str(refresh),
           "access": str(refresh.access_token),
           "email": user.email,
           "username": user.username,
           "is_staff": user.is_staff,
           "is_superuser": user.is_superuser
        }
    

    

class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate(self, data):

        email = data['email'].lower()

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        otp = generate_otp()

        store_reset_otp(email, otp)

        send_otp_email(email, otp)

        return {"message": "OTP sent to email"}
    

class VerifyResetOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):

        email = data['email'].lower()
        otp = data['otp']

        stored_otp = get_reset_otp(email)

        if not stored_otp:
            raise serializers.ValidationError("OTP expired")

        if stored_otp != otp:
            raise serializers.ValidationError("Invalid OTP")

        return {"message": "OTP verified successfully"}
    


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):

        email = data['email'].lower()
        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        stored_otp = get_reset_otp(email)

        if not stored_otp:
            raise serializers.ValidationError("OTP verification required")

        data['email'] = email
        return data

    def create(self, validated_data):

        email = validated_data['email']
        new_password = validated_data['new_password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        user.set_password(new_password)
        user.save()

        delete_reset_otp(email)

        return {"message": "Password reset successful"}
    


from rest_framework_simplejwt.tokens import RefreshToken


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def validate(self, data):

        try:
            token = RefreshToken(data['refresh'])
            token.blacklist()

        except Exception:
            raise serializers.ValidationError("Invalid token")

        return {"message": "Logout successful"}
    


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()