from jobs.models import Job
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from intern_job_profile.serializers import InternJobProfileSerializer
from intern_job_profile.models import InternJobProfile



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
        except Exception as e:
                print(e)
                return Response({"Internal Server Error"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


