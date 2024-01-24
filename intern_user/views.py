from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from intern_user.renders import UserRenderer
from intern_user.serializers import MyUserRegisterSerializer, MyUserLoginSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from intern_user.models import InternUser


# Create your views here.
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create Your Registration User Code Start Here
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = MyUserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return Response({"msg": "Registration Sucessfully"})
        return Response({"error": "Invalid Data" }, status=status.HTTP_400_BAD_REQUEST)
    
class MyLogin(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format = None):
        serializers = MyUserLoginSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            email = serializers.data.get("email")
            password = serializers.data.get("password")
            user = authenticate(email = email, password = password)
            if user is not None:
                token = get_token_for_user(user)
                return Response({'token': token, 'msg': "User Login Sucessfully"})
            else:
                Response({ "error": "Invalid Data" }, status=status.HTTP_401_UNAUTHORIZED)

            if user == None:
                return Response({"error": "Invalid Data"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            Response({"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


class MyProfile(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)  