from django.shortcuts import render
from jobs.models import Job
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from jobs.serializers import JobPostSerializer
from jobs.models import Job
from jobs.serializers import JobGetSerializer


class JobPostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            if id is not None:    
                if (request.user.user_type == "company"):
                    job_data = Job.objects.filter(company = id)
                    job_serializer = JobGetSerializer(job_data, many=True)
                    return Response(job_serializer.data, status=status.HTTP_200_OK)
            else:
                job_data = Job.objects.all()
                job_serializer = JobGetSerializer(job_data, many=True)
                return Response(job_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id = None):
        try:
            if (request.user.user_type == "company"):
                job_serializer = JobPostSerializer(data=request.data)
                if job_serializer.is_valid():
                    job_serializer.save()
                    return Response({"message": "Job Posted Successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(job_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             
            else:
                return Response({"error": "method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            return Response({"error": "Internal Server Error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id=None):
        if id is not None:
            pass
        else:
            return Response({"error": "method not allowed"}, status=status.HTTP_400_BAD_REQUEST)
            

        
