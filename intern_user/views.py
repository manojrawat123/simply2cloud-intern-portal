from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from intern_user.renders import UserRenderer
from intern_user.serializers import MyUserRegisterSerializer, MyUserLoginSerializer, UserProfileSerializer, MyUserSerializers
from intern_user.models import InternUser
from intern_user.serializers import UserProfileSerializer
from skills.models import Skill
from skills.serializer import SkillsSerializer
from company.models import Company
from company.serializers import MyCompanySerializer, MyCompanyGetSerializer
from available_skills.models import AvailableSkill
from available_skills.serializer import AvailableSkillSerializer
from intern_profile_job.serializers import InternJobProfileSerializer,InternAuthenticatedCompanyProfileCompanyViewSerializer, InternUserJobProfileForCompanViewSerializer
from intern_profile_job.models import InternJobProfile
from job_categoery.models import JobCategory
from job_categoery.serializer import AvailableJobCategoerySerializer
from sub_categoery.models import SubCategory
from sub_categoery.serializer import SubCategoerySerializer
from intern_experience.models import JobExperience
from intern_experience.serializers import InternExperienceGetSerializer
import datetime
from dateutil import tz
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def EmailVerifyFunc(current_user, domain_name):

    configuration = sib_api_v3_sdk.Configuration()
    # Paste line here
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "Verification Email from Intern Monster"
    userid_encode = urlsafe_base64_encode(force_bytes(current_user.pk))
    token = default_token_generator.make_token(current_user)
    message = f'{domain_name}/accounts/activate/{userid_encode}/{token}'
    html_content =html_content = f'''<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        .container {{
         
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        h3 {{
            color: #333333;
        }}
        p {{
            color: #666666;
        }}
        a {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
        }}
        a:hover {{
            background-color: #0056b3;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h3>Dear Intern,</h3>
        <p>Please click on the below link to verify your email</p>
        <p><a href="{message}" style="color: #ffffff;">Click To Verify</a></p>
        <p>Thanks & Regards,</p>
        <p>Customer Care</p>
        <p>Intern Monster</p>
    </div>
</body>
</html>'''

    sender = {"name":"Intern Monster","email":"enquiry@simply2cloud.com"}
    to = [{"email": current_user.email,"name": current_user.name}]
    cc = [{"email":"enquiry@simply2cloud.com","name":"Intern Monster"}]
    bcc = [{"name":"John Doe","email":"positive.mind.123456789@gmail.com"}]
    reply_to = {"email":"enquiry@simply2cloud.com","name":"Intern Monster"}
    headers = {"Some-Custom-Name":"unique-id-1234"}
    params = {"parameter":"My param value","subject":"New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, bcc=bcc, cc=cc, reply_to=reply_to, headers=headers, html_content=html_content, sender=sender, subject=subject)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create Your Registration User Code Start Here
class UserRegistrationView(APIView):
    # renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = MyUserSerializers(data=request.data)
        email = request.data.get("email")
        phone = request.data.get("phone")
        domain_name = request.data.get("url")
        if serializer.is_valid():
            data = serializer.save()
            current_user = InternUser.objects.get(email = email)
            current_user.user_type = "user"
            current_user.save()
            EmailVerifyFunc(current_user, domain_name)
            return Response({"message": "Registration Successfully Verify link Send to Your Email"})
        else:
            try:
                current_user = InternUser.objects.get(Q(email = email) | Q(phone = phone))
                if current_user is not None:
                    if current_user.is_active:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        
                        EmailVerifyFunc(current_user, domain_name)
                        current_user.delete()
                        n_serializer = MyUserSerializers(data=request.data)
                        if n_serializer.is_valid():
                            n_serializer.save()
                            new_user = InternUser.objects.get(Q(email = email))
                            new_user.user_type = "user"
                            new_user.save()
                            return Response({"message": "Registration Successfully Verify link Send to Your Email"}, status=status.HTTP_200_OK)
                        else:
                            return Response(n_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class VerifybyEmail(APIView):
    def post(self , request, userid_encode = None,token = None):
        try:
            activate = request.data.get("activate")
            pk = urlsafe_base64_decode(userid_encode)
            user = InternUser.objects.get(pk= pk)
            if default_token_generator.check_token(user,token):
                user.is_active = activate
                user.save()
                return Response({"message": "Registration Sucessfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error" : "Not Authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
class MyLogin(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format = None):
        try:
            serializers = MyUserLoginSerializer(data=request.data)
            if serializers.is_valid(raise_exception=True):
                email = serializers.data.get("email")
                password = serializers.data.get("password")
                user = authenticate(email = email, password = password)
                if user is not None:
                    token = get_token_for_user(user)
                    return Response({'token': token,"user_type": user.user_type, 'msg': "User Login Sucessfully"})
                else:
                    try:
                        user_e = InternUser.objects.get(email = email)
                        if (user_e):
                            email = request.data.get("email")
                            domain_name = request.data.get("url")
                            mail_subject = "Please activate account" 
                            userid_encode = urlsafe_base64_encode(force_bytes(user_e.pk))
                            token = default_token_generator.make_token(user_e)
                            message = f'{domain_name}/accounts/activate/{userid_encode}/{token}'
                            # email = EmailMessage(mail_subject, message, 'simply2cloud@gmail.com',[email])
                            # email.send()
                            EmailVerifyFunc(user_e, domain_name=domain_name)
                            return Response({"error" : "Verify Your Email"}, status=status.HTTP_401_UNAUTHORIZED)
                        else:
                            return Response({"error" : "Email Not Exists"}, status=status.HTTP_400_BAD_REQUEST) 
                    except Exception as e:
                        return Response({"error" : "Email Not Exists"}, status=status.HTTP_400_BAD_REQUEST)     
        
                    # Response({ "error": "Invalid Data" }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                Response({"error": "Please data In Correct Foramt"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

                # Aviable Skills 
                skill_ids = [skill.skill_id.id for skill in skills]

                available_skill = AvailableSkill.objects.exclude(id__in=skill_ids)
                available_skill_serializer = AvailableSkillSerializer(available_skill, many=True)

                # Intern User Job Profile
                intern_job_profile = InternJobProfile.objects.filter(intern = request.user.id)
                intern_job_profile_serializers = InternAuthenticatedCompanyProfileCompanyViewSerializer(intern_job_profile, many=True)

                 # Available Job Categoeries
                available_categoery = JobCategory.objects.filter(is_active = True)
                available_categoery_serailzer = AvailableJobCategoerySerializer(available_categoery, many=True)

                # Sub Categoery
                subcategoery_data = SubCategory.objects.all()
                subcategoery_serializer = SubCategoerySerializer(subcategoery_data, many=True)

                # Experience Details
                user_experience_data = JobExperience.objects.filter(user = request.user.id)
                user_experience_serializer = InternExperienceGetSerializer(user_experience_data, many= True)
                
                return Response({
                    "user_details": user_serializer.data, 
                    "skills_detail": skills_serializer.data,
                    "intern_job_profile" : intern_job_profile_serializers.data,
                    "available_categoery": available_categoery_serailzer.data,
                    "available_sub_categoery" : subcategoery_serializer.data,
                    "avaiable_skill" : available_skill_serializer.data,
                    "experience_details" : user_experience_serializer.data,
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

                return Response({
                    "company_details": company_serializer.data, 
                    "aviable_skills": available_skill_serializer.data,
                    "categoery_option": available_categoery_serailzer.data,
                    "user_details": user_serializer.data, 
                    "intern_job_profile" : intern_job_profile_serializers.data, 
                }, status=status.HTTP_200_OK)
            
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
        

class UnAutProfView(APIView):
    def get(self, request, id=None):
        # Available Job Categoeries
        available_categoery = JobCategory.objects.filter(is_active = True)
        available_categoery_serailzer = AvailableJobCategoerySerializer(available_categoery, many=True)

        # Aviable Skills 
        available_skill = AvailableSkill.objects.all()
        available_skill_serializer = AvailableSkillSerializer(available_skill, many=True)
        
        # Sub Categoery
        subcategoery_data = SubCategory.objects.all()
        subcategoery_serializer = SubCategoerySerializer(subcategoery_data, many=True)
        return Response({
                        "avaliable_categoery" : available_categoery_serailzer.data,
                        "avaliable_subcategoery" : subcategoery_serializer.data,
                        "available_skill" : available_skill_serializer.data 
                        }, status=status.HTTP_200_OK)
