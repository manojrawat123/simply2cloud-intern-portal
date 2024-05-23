from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from intern_experience.serializers import InternExperienceSerializer
from intern_experience.models import JobExperience
from intern_profile_job.models import InternJobProfile

# Create your views here.
class InternExperienceView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id = None):
        if (request.user.user_type == "user"):
            intern_job_experience = InternExperienceSerializer(data=request.data)
            try:
                if intern_job_experience.is_valid():
                    saved_experience = intern_job_experience.save()
                    try:
                        user_profile = InternJobProfile.objects.get(intern = intern_job_experience.validated_data["user"].id)
                        user_profile.experience.add(saved_experience)
                        user_profile.save()
                    except Exception as e:
                        print("error")
                    return Response({"message": "Profile Added Sucessfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(intern_job_experience.errors , status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                    print(e)
                    return Response({"Internal Server Error"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
           return Response({"Internal Server Error"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, id = None):
        if id is None:
            return Response({"message": "Method Not Allowed"}, status= status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            user_experience = JobExperience.objects.filter(user=request.user.id)
            selected_experience = user_experience.get(id=id)
            
            # Use the serializer to delete the object
            selected_experience.delete()
            return Response({"message": "Skill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
