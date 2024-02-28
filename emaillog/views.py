from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from emaillog.serializers import EmailLogSerializers

# Create your views here.
class SendEmailToStudent():
    permission_classes = [IsAuthenticated]
    def post(self, request, id = None):
        if (request.user.user_type == "company"):
            intern_job_experience = EmailLogSerializers(data=request.data)
            try:
                if intern_job_experience.is_valid():
                    intern_job_experience.save()
                    return Response({
                        "message": "Profile Added Sucessfully"
                        }, status=status.HTTP_201_CREATED)
                else:
                    return Response(intern_job_experience.errors , status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                    print(e)
                    return Response({"Internal Server Error"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
           return Response({"Internal Server Error"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)