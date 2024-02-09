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
from company.models import Company
from company.serializers import MyCompanySerializer, MyCompanyGetSerializer
from available_skills.models import AvailableSkill
from available_skills.serializer import AvailableSkillSerializer
from intern_job_profile.serializers import InternJobProfileSerializer,InternJobProfileGetSerializer, InternUserJobProfileForCompanViewSerializer
from intern_job_profile.models import InternJobProfile
from job_categoery.models import JobCategory
from job_categoery.serializer import AvailableJobCategoerySerializer

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
        try:
            if (request.user.user_type == "user"):
                user_details = InternUser.objects.get(id = request.user.id)
                user_serializer = UserProfileSerializer(user_details)

                skills = Skill.objects.filter(intern = request.user.id)
                skills_serializer = SkillsSerializer(skills, many=True)

                # Intern User Job Profile
                intern_job_profile = InternJobProfile.objects.filter(intern = request.user.id)
                intern_job_profile_serializers = InternJobProfileGetSerializer(intern_job_profile, many=True)

                 # Available Job Categoeries
                available_categoery = JobCategory.objects.filter(is_active = True)
                available_categoery_serailzer = AvailableJobCategoerySerializer(available_categoery, many=True)

                return Response({
                    "user_details": user_serializer.data, 
                    "skills_detail": skills_serializer.data,
                    "intern_job_profile" : intern_job_profile_serializers.data,
                    "available_categoery": available_categoery_serailzer.data
                    }, status=status.HTTP_200_OK)  
            elif (request.user.user_type == "company"):
                try:
                    company_data = Company.objects.get(company_user = request.user)
                    company_serializer = MyCompanyGetSerializer(company_data)
                except Exception as e:
                    company_serializer = {"data": {"message":"No Data Of given Company"}}
                

                # User Details 
                user_details = InternUser.objects.get(id = request.user.id)
                user_serializer = UserProfileSerializer(user_details)

                # Aviable Skills 
                available_skill = AvailableSkill.objects.all()
                available_skill_serializer = AvailableSkillSerializer(available_skill, many=True)

                # Available Job Categoeries
                available_categoery = JobCategory.objects.filter(is_active = True)
                available_categoery_serailzer = AvailableJobCategoerySerializer(available_categoery, many=True)

                # Intern User Job Profile
                intern_job_profile = InternJobProfile.objects.all()
                intern_job_profile_serializers = InternUserJobProfileForCompanViewSerializer(intern_job_profile, many=True)

                return Response({"company_details": company_serializer.data, 
                                 "aviable_skills": available_skill_serializer.data,
                                   "user_details": user_serializer.data, 
                                   "categoery_option": available_categoery_serailzer.data,
                    "intern_job_profile" : intern_job_profile_serializers.data, }, status=status.HTTP_200_OK)
            
            else:
                return Response({"error": "Not a valid User"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)      
        
    

    def put(self, request, id=None):
        
        intern_user = InternUser.objects.get(id = request.user.id)
        user_serializer = UserProfileSerializer(intern_user, data=request.data, partial = True)
        if user_serializer.is_valid():
            data = user_serializer.save()
            return Response({"message": "Data Updated Sucessfully"},status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)