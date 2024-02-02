from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from company.renders import CompanyRender
from company.serializers import MyCompanyUserSerializers, MyCompanySerializer
from intern_user.models import InternUser

# Create your views here.
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create Your Registration User Code Start Here
class CompanyRegistrationView(APIView):
    renderer_classes = [CompanyRender]
    def post(self, request, format=None):
        user_data = {
            "email": request.data["email"],
            "name": request.data["companyName"],
            "phone": request.data["phone"],
            "address" : request.data["location"],
            "user_type": request.data["user_type"],
            "s2c_certified" : True,
            "password": request.data["password"],
            "password2" : request.data["password2"]
          }
        serializer = MyCompanyUserSerializers(data=user_data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            current_user = InternUser.objects.get(email=request.data["email"])
            current_user.user_type = "company"
            current_user.is_active = True
            current_user.save() 
            id = current_user.id
            
            company_data = {
            "email": request.data["email"],
            "company_name": request.data["companyName"],
            "phone_number": request.data["phone"],
            "headquaters" : request.data["location"],
            "address" : request.data["location"],
            "website" : request.data["website"],
            "industry" : request.data["industry"],
            "founded_date" : request.data["founded_date"],
            "company_user" : id,
        }
            company_serializer = MyCompanySerializer(data=company_data)
            
            if company_serializer.is_valid():
                company_serializer.save()
            else:
                current_user.delete()
                return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg": "Registration Sucessfully"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

        
    
# class CompanyLogin(APIView):
#     renderer_classes = [CompanyRender]
#     def post(self, request, format = None):
#         serializers = MyUserLoginSerializer(data=request.data)
#         if serializers.is_valid(raise_exception=True):
#             email = serializers.data.get("email")
#             password = serializers.data.get("password")
#             user = authenticate(email = email, password = password)
#             if user is not None:
#                 token = get_token_for_user(user)
#                 return Response({'token': token, 'msg': "User Login Sucessfully"})
#             else:
#                 Response({ "error": "Invalid Data" }, status=status.HTTP_401_UNAUTHORIZED)

#             if user == None:
#                 return Response({"error": "Invalid Data"}, status = status.HTTP_400_BAD_REQUEST)
#         else:
#             Response({"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


# class CompanyProfile(APIView):
#     renderer_classes = [CompanyRender]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         user_details = InternUser.objects.get(id = request.user.id)
#         user_serializer = UserProfileSerializer(user_details)

#         skills = Skill.objects.filter(intern = request.user.id)
#         skills_serializer = SkillsSerializer(skills, many=True)

#         return Response({"user_details": user_serializer.data, "skills_detail": skills_serializer.data}, status=status.HTTP_200_OK)  
    

#     def put(self, request, id=None):
        
#         intern_user = InternUser.objects.get(id = request.user.id)
#         user_serializer = UserProfileSerializer(intern_user, data=request.data, partial = True)
#         if user_serializer.is_valid():
#             data = user_serializer.save()
#             return Response({"message": "Data Updated Sucessfully"},status=status.HTTP_200_OK)
#         else:
#             return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)