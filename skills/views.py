from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from skills.serializer import SkillsSerializer 
from skills.models import Skill
from intern_profile_job.models import InternJobProfile
from django.db.models import Q

class MySkills(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        skills = Skill.objects.filter(intern = request.user)
        serializer = SkillsSerializer(skills, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
    def post(self, request, format=None):
        skill_serialzer = SkillsSerializer(data = request.data)
        if skill_serialzer.is_valid():
            skill_instances = skill_serialzer.save()
            profile_id = request.data.get("profile_id")
            if (profile_id is not None):
                user_profile = InternJobProfile.objects.get(Q(id = profile_id) & Q(intern = request.user.id))
                skill_ids = list(user_profile.skills.values_list('id', flat=True))
                available_skills_ids = list(user_profile.available_skills.values_list('id', flat=True))
                available_skills_ids.append(skill_instances.skill_id)
                user_profile.available_skills.set(available_skills_ids)
                skill_ids.append(skill_instances.id)
                user_profile.skills.set(skill_ids)
                print(skill_instances.id)
            return Response({"message": "Data Created Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(skill_serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id = None):
        if id is None:
            return Response({"message": "Method Not Allowed"}, status= status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            try:
                user_skills = Skill.objects.filter(intern=request.user.id)
                selected_skill = user_skills.get(id=id)
                profile_id = request.data.get("profile_id")
                print(profile_id)
                if (profile_id is not None):
                    user_profile = InternJobProfile.objects.get(Q(id = profile_id) & Q(intern = request.user.id))
                    skill_ids = list(user_profile.skills.values_list('id', flat=True))
                    available_skills_ids = list(user_profile.available_skills.values_list('id', flat=True))
                    available_skills_ids.remove(selected_skill.skill_id.id)
                    user_profile.available_skills.set(available_skills_ids)
                    skill_ids.remove(selected_skill.id)
                    user_profile.skills.set(skill_ids)
                
                # Use the serializer to delete the object
                selected_skill.delete()

                return Response({"message": "Skill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

            except Skill.DoesNotExist:
                return Response({"error": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(e)
                return Response({"error": "Not Authenticated"}, status=status.HTTP_406_NOT_ACCEPTABLE)


