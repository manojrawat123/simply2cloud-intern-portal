from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from conversional.models import Conversation
from django.db.models import Q
from conversional.serializer import ConversionalGetSerializer
from rest_framework.response import Response
from rest_framework import status
from intern_profile_job.models import InternJobProfile
from company.models import Company
from datetime import datetime
from message.models import Message

class ConversitionalView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        try:
            conversiation = Conversation.objects.filter(Q(sender = request.user.id) | Q(receiver = request.user.id))
            conversiation_serializer = ConversionalGetSerializer(conversiation, many=True)
            for i in conversiation_serializer.data:                
                i["date"] = datetime.strptime(i["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%b %d, %Y")
                i["time"] = datetime.strptime(i["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%I:%M %p")
                last_message = Message.objects.filter(
                        conversation_id=i["id"]
                    ).order_by('-created_at').first()
                if last_message.sender.id == request.user.id:
                    i["show_message_count"] = False
                elif last_message.receiver.id == request.user.id:
                    i["show_message_count"] = True
                sender_id = i['sender']
                receiver_id = i['receiver']
                imgObj = {}
                if sender_id["id"] == request.user.id:
                    imgObj = {"id": receiver_id["id"], "user_type": receiver_id["user_type"]}
                elif receiver_id["id"] == request.user.id:
                    imgObj = {"id": sender_id["id"], "user_type": sender_id["user_type"]}
                if (imgObj["user_type"] == "user"):
                    profile_obj = InternJobProfile.objects.get(intern = imgObj["id"])
                    i["image"] = profile_obj.user_image.url
                    i["name"] =  profile_obj.intern.name
                    i["chat_user_id"] = profile_obj.intern.id
                elif (imgObj["user_type"] == "company"):
                    profile_obj = Company.objects.get(company_user= imgObj["id"])
                    i["image"] = profile_obj.logo.url if profile_obj.logo else None
                    i["name"] = profile_obj.company_name
                    i["chat_user_id"] = profile_obj.company_user.id                                
            return Response(conversiation_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error" : "Some Error Occured"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
