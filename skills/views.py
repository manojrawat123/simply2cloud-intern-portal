from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from skills.serializer import SkillsSerializer 
from skills.models import Skill


class MySkills(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        skills = Skill.objects.filter(intern = request.user)
        serializer = SkillsSerializer(skills, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
    def post(self, request, format=None):
        skill_serialzer = SkillsSerializer(data = request.data)
        if skill_serialzer.is_valid():
            skill_serialzer.save()
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
                
                # Use the serializer to delete the object
                selected_skill.delete()

                return Response({"message": "Skill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

            except Skill.DoesNotExist:
                return Response({"error": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": "Not Authenticated"}, status=status.HTTP_406_NOT_ACCEPTABLE)


