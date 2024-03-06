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
from intern_user.views import EmailVerifyFunc
from django.db.models import Q


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
        domain_name = request.data.get("url")
        user_data = {
            "email": request.data["email"],
            "name": request.data["companyName"],
            "phone": request.data["phone"],
            "address" : request.data["location"],
            "user_type": "company",
            "s2c_certified" : True,
            "password": request.data["password"],
            "password2" : request.data["password2"]
          }
        serializer = MyCompanyUserSerializers(data=user_data)
        if serializer.is_valid():
            data = serializer.save()
            current_user = InternUser.objects.get(email=request.data["email"])
            current_user.user_type = "company"
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
                EmailVerifyFunc(current_user, domain_name)
            else:
                current_user.delete()
                return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg": "Registration Sucessfully"})
        else:
            try:
                current_user = InternUser.objects.get(Q(email = request.data["email"]))
                if current_user is not None:
                    if current_user.is_active:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        current_user.delete()
                        c_serializer = MyCompanyUserSerializers(data=user_data)
                        if c_serializer.is_valid():
                            c_serializer.save()
                            new_user = InternUser.objects.get(Q(email = request.data["email"]))
                            new_user.user_type = "company"
                            new_user.save()
                            EmailVerifyFunc(new_user, domain_name)
                            return Response({"message": "Registration Successfully Verify link Send to Your Email"}, status=status.HTTP_200_OK)
                        else:
                            return Response(c_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    # return Response({"message": "Registration Successfully Verify link Send to Your Email"})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                print(e)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)