from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from available_skills.models import AvailableSkill
from available_skills.serializer import AvailableSkillSerializer

# Create your views here.
class PostJobView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id = None):
        if (request.user.user_type == "company"):
            available_skill = AvailableSkill.objects.all()
            available_skill_serializer = AvailableSkillSerializer(available_skill, many=True)
            return Response(available_skill_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)