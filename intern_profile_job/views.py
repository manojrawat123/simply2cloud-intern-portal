from jobs.models import Job
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from intern_profile_job.serializers import InternJobProfileSerializer
from intern_profile_job.models import InternJobProfile
from intern_profile_job.serializers import InternJobProfileSerializer, InternUserJobProfileForCompanViewSerializer


class InternJobProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id = None):
        intern_job_profile_serializers = InternJobProfileSerializer(data=request.data)
        print(request.data)
        try:
            if intern_job_profile_serializers.is_valid():
                intern_job_profile_serializers.save()
                return Response({"message": "Profile Added Sucessfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(intern_job_profile_serializers.errors , status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                print(e)
                return Response({"Internal Server Error"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class InternJobUnAuthCompanyViewSearch(APIView):
    def get(self, request, id = None):
        # Intern User Job Profile
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