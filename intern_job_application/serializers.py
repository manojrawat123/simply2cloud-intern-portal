from rest_framework import serializers 
from intern_user.serializers import InternUserDetailCompanyViewSerializer,InternAuthCompanyUserViewSerializer
from intern_job_application.models import JobApplication
from jobs.serializers import JobGetSerializer

class InternJobApplyGetSerializer(serializers.ModelSerializer):
    user = InternAuthCompanyUserViewSerializer()
    job = JobGetSerializer()
    class Meta:
        model =  JobApplication
        fields = "__all__"

class InternJobApplyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model =  JobApplication
        fields = "__all__"