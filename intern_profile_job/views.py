from jobs.models import Job
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from intern_profile_job.serializers import InternJobProfileSerializer
from intern_profile_job.models import InternJobProfile
from intern_profile_job.serializers import InternJobProfileSerializer, InternUserJobProfileForCompanViewSerializer,InternAuthenticatedCompanyProfileCompanyViewSerializer
from intern_experience.models import JobExperience
from intern_experience.serializers import InternExperienceGetSerializer
from rest_framework.exceptions import ValidationError

class InternJobProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id = None):
        intern_job_profile_serializers = InternJobProfileSerializer(data=request.data)
        try:
            if intern_job_profile_serializers.is_valid():
                intern_job_profile_serializers.save()
                return Response({"message": "Profile Added Sucessfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(intern_job_profile_serializers.errors , status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # print(f"An error occurred: {e}")
            return Response({"Internal Server Error": "An error occurred while processing your request."}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id = None):
        if id is None:
            return Response({"error" : "Method Not Allowed"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                print("Mai Chala")
                intern_profile_all = InternJobProfile.objects.filter(intern = request.user.id)
                intern_profile = intern_profile_all.get(id = id)
                intern_profile_serializer = InternJobProfileSerializer(intern_profile, data=request.data, partial=True)
                if intern_profile_serializer.is_valid():
                    intern_profile_serializer.save()
                    return Response({"message" : "User Updated Successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(intern_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"Internal Server Error"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InternJobUnAuthCompanyViewSearch(APIView):
    def get(self, request, id = None):
        # Intern User Job Profile
        if(id is not None):
            intern_job_profile = InternJobProfile.objects.get(id = id)
            intern_job_profile_serializers = InternUserJobProfileForCompanViewSerializer(intern_job_profile)

            
            # intern Experience Details
            user_id = intern_job_profile.intern.id
            user_experience_data = JobExperience.objects.filter(user = user_id)
            user_experience_serializer = InternExperienceGetSerializer(user_experience_data, many= True)
            return Response({"profile_details" : intern_job_profile_serializers.data, 
                                    "experience_details" : user_experience_serializer.data}, status=status.HTTP_200_OK)
        else:
            categoery_id = request.query_params.get("categoery")
            skills_id = request.query_params.get('skills')
            sub_cat_id = request.query_params.get('sub_categoery')
            if (categoery_id is not None):
                intern_job_profile = InternJobProfile.objects.filter(job_categoery = categoery_id)
            elif (skills_id is not None):
                print(skills_id)
                intern_job_profile = InternJobProfile.objects.filter(available_skills__in=[skills_id]).distinct()
                intern_job_profile = InternJobProfile.objects.filter(available_skills__in=[skills_id]).distinct()
            elif(sub_cat_id is not None):
                intern_job_profile = InternJobProfile.objects.filter(sub_categoery = sub_cat_id)            
            intern_job_profile_serializers = InternUserJobProfileForCompanViewSerializer(intern_job_profile, many=True)
            return Response({"intern_job_profile" : intern_job_profile_serializers.data}, status=status.HTTP_200_OK)
        

class AuthCompanyUserSearchView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        # Intern User Job Profile
        if request.user.user_type == "company":
            if(id is not None):
                intern_job_profile = InternJobProfile.objects.get(id = id)
                intern_job_profile_serializers = InternAuthenticatedCompanyProfileCompanyViewSerializer(intern_job_profile)

                # intern Experience Details
                user_id = intern_job_profile.intern.id
                user_experience_data = JobExperience.objects.filter(user = user_id)
                user_experience_serializer = InternExperienceGetSerializer(user_experience_data, many= True)
                return Response({"profile_details" : intern_job_profile_serializers.data, 
                                    "experience_details" : user_experience_serializer.data}, status=status.HTTP_200_OK)
            else:
                categoery_id = request.query_params.get("categoery")
                skills_id = request.query_params.get('skills')
                sub_cat_id = request.query_params.get('sub_categoery')
                if (categoery_id is not None):
                    intern_job_profile = InternJobProfile.objects.filter(job_categoery = categoery_id)
                elif (skills_id is not None):
                    print(skills_id)
                    intern_job_profile = InternJobProfile.objects.filter(available_skills__in=[skills_id]).distinct()
                    intern_job_profile = InternJobProfile.objects.filter(available_skills__in=[skills_id]).distinct()
                elif(sub_cat_id is not None):
                    intern_job_profile = InternJobProfile.objects.filter(sub_categoery = sub_cat_id)            
                intern_job_profile_serializers = InternAuthenticatedCompanyProfileCompanyViewSerializer(intern_job_profile, many=True)
                return Response({"intern_job_profile" : intern_job_profile_serializers.data}, status=status.HTTP_200_OK)
        else:
            if id is not None:
                try:
                    intern_job_profile_arr = InternJobProfile.objects.filter(intern = request.user.id)
                    intern_job_profile = intern_job_profile_arr.get(id = id)
                    intern_job_profile_serializers = InternAuthenticatedCompanyProfileCompanyViewSerializer(intern_job_profile)
                    
                    # Experience Details
                    user_id = intern_job_profile.intern.id
                    user_experience_data = JobExperience.objects.filter(user = user_id)
                    user_experience_serializer = InternExperienceGetSerializer(user_experience_data, many= True)
                    
                    return Response({"profile_details" : intern_job_profile_serializers.data, 
                                    "experience_details" : user_experience_serializer.data}, status=status.HTTP_200_OK)
                except Exception as e:
                    intern_job_profile = InternJobProfile.objects.get(id = id)
                    intern_job_profile_serializers = InternUserJobProfileForCompanViewSerializer(intern_job_profile)

                    # Experience Details
                    user_id = intern_job_profile.intern.id
                    user_experience_data = JobExperience.objects.filter(user = user_id)
                    user_experience_serializer = InternExperienceGetSerializer(user_experience_data, many= True)
                    return Response({"profile_details" : intern_job_profile_serializers.data, 
                                    "experience_details" : user_experience_serializer.data}, status=status.HTTP_200_OK)
            else:
                categoery_id = request.query_params.get("categoery")
                skills_id = request.query_params.get('skills')
                sub_cat_id = request.query_params.get('sub_categoery')
                if (categoery_id is not None):
                    intern_job_profile = InternJobProfile.objects.filter(job_categoery = categoery_id)
                elif (skills_id is not None):
                    print(skills_id)
                    intern_job_profile = InternJobProfile.objects.filter(available_skills__in=[skills_id]).distinct()
                    intern_job_profile = InternJobProfile.objects.filter(available_skills__in=[skills_id]).distinct()
                elif(sub_cat_id is not None):
                    intern_job_profile = InternJobProfile.objects.filter(sub_categoery = sub_cat_id)            
                intern_job_profile_serializers = InternUserJobProfileForCompanViewSerializer(intern_job_profile, many=True)
                return Response({"intern_job_profile" : intern_job_profile_serializers.data}, status=status.HTTP_200_OK)