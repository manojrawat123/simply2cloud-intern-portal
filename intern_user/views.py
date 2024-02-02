from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from intern_user.renders import UserRenderer
from intern_user.serializers import MyUserRegisterSerializer, MyUserLoginSerializer, UserProfileSerializer, MyUserSerializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from intern_user.models import InternUser
from intern_user.serializers import UserProfileSerializer
from skills.models import Skill
from skills.serializer import SkillsSerializer


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
        serializer = MyUserSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            current_user = InternUser.objects.get(email = request.data.get("email"))
            current_user.user_type = "user"
            current_user.is_active = True
            current_user.save()
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
                return Response({'token': token,"user_type": user.user_type, 'msg': "User Login Sucessfully"})
            else:
                Response({ "error": "Invalid Data" }, status=status.HTTP_401_UNAUTHORIZED)
            if user == None:
                return Response({"error": "No User Found"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            Response({"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


class MyProfile(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user_details = InternUser.objects.get(id = request.user.id)
        user_serializer = UserProfileSerializer(user_details)

        skills = Skill.objects.filter(intern = request.user.id)
        skills_serializer = SkillsSerializer(skills, many=True)

        return Response({"user_details": user_serializer.data, "skills_detail": skills_serializer.data}, status=status.HTTP_200_OK)  
    

    def put(self, request, id=None):
        
        intern_user = InternUser.objects.get(id = request.user.id)
        user_serializer = UserProfileSerializer(intern_user, data=request.data, partial = True)
        if user_serializer.is_valid():
            data = user_serializer.save()
            return Response({"message": "Data Updated Sucessfully"},status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)