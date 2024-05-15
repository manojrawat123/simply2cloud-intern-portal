from jobs.models import Job
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from intern_job_application.models import JobApplication
from intern_job_application.serializers import InternJobApplyGetSerializer, InternJobApplyPostSerializer

# Create your views here.
class InternJobApplicationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        try:
            if (request.user.user_type == "user"):
                intern_applied_jobs = JobApplication.objects.filter(user = request.user.id)
                intern_job_apply_serializer = InternJobApplyGetSerializer(intern_applied_jobs,many=True)
                return Response(intern_job_apply_serializer.data, status=status.HTTP_200_OK)
            elif(request.user.user_type == "company"):
                status_params = request.query_params.get("status")
                if status_params is None:
                    intern_applied_jobs = JobApplication.objects.filter(Q(company_user = request.user) & Q(status="Pending"))
                else:
                    intern_applied_jobs = JobApplication.objects.filter(Q(company_user = request.user) & Q(status=status_params))
                intern_job_apply_serializer =InternJobApplyGetSerializer(intern_applied_jobs, many=True)
                
                return Response(intern_job_apply_serializer.data, status=status.HTTP_200_OK) 
            else:
                return Response({"error": "method not allowed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request, id = None):
        try:
            if (request.user.user_type == "user"):
                intern_job_apply_serializer = InternJobApplyPostSerializer(data=request.data)
                if intern_job_apply_serializer.is_valid():
                    intern_job_apply_serializer.save()
                    return Response({"message": "Applied Successfully!!"}, status=status.HTTP_200_OK)
                else:
                    return Response(intern_job_apply_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "method not allowed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request, id=None):
        try:
            if id is not None:
                intern_job_application = JobApplication.objects.get(id=id)
                intern_job_apply_serializer = InternJobApplyPostSerializer(intern_job_application, data=request.data, partial=True)
                if intern_job_apply_serializer.is_valid():
                    intern_job_apply_serializer.save()
                    return Response({"message": "Applied Successfully!!"}, status=status.HTTP_200_OK)
                else:
                    return Response(intern_job_apply_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except Exception as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



