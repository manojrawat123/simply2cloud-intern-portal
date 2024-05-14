from django.shortcuts import render
from rest_framework.views import APIView
from message.models import Message
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from message.serializers import MessageSerializer,MessageGetSerializer
from conversional.models import Conversation
from conversional.serializer import ConversionalSerializer
from rest_framework.response import Response
from rest_framework import status
from intern_profile_job.models import InternJobProfile
from company.models import Company
from datetime import datetime
from intern_user.models import InternUser
from intern_user.serializers import MyUserRegisterSerializer

# Create your views here.
class MessageView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,user_id1):
        try:

            if user_id1 is None:
                return Response({"error" : "No Id provided"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                profile_detail = InternUser.objects.get(id = user_id1)
                profile_serializer = MyUserRegisterSerializer(profile_detail)
                user_image = None
                if profile_detail.user_type == "user":
                    intern_prf = InternJobProfile.objects.get(intern = profile_detail.id)
                    user_image = intern_prf.user_image.url
                elif profile_detail.user_type == "company":
                    company_prf = Company.objects.get(company_user = profile_detail.id)
                    user_image = company_prf.logo.url if company_prf.logo else None
                message = Message.objects.filter( Q(sender_id=user_id1, receiver_id=request.user.id) |
        Q(sender_id=request.user.id, receiver_id=user_id1)).order_by('created_at')
                try:
                    conversation = Conversation.objects.get(
                        id = message.last().conversation_id.id
                )
                    if  message.last().receiver.id == request.user.id:
                        conversation.unread_message_count = 0
                        conversation.save()
                except Exception as e:
                    print(e)

                # conversation_serializer = ConversionalSerializer(conversation, many=True)
                message_serializer = MessageGetSerializer(message, many = True)
                for i in message_serializer.data:
                    i["name"] = i["sender"]["name"]
                    i["date"] = datetime.strptime(i["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%b %d, %Y")
                    i["time"] = datetime.strptime(i["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%I:%M %p")
                    if i["sender"]["user_type"] == "user":
                        profile_obj = InternJobProfile.objects.get(intern = i["sender"]["id"])
                        i["image"] = profile_obj.user_image.url
                    elif i["sender"]["user_type"] == "company":
                        profile_obj = Company.objects.get(company_user= i["sender"]["id"])
                        i["image"] = profile_obj.logo.url if profile_obj.logo else None
                
                return Response({"profile" : profile_serializer.data,"chats" : message_serializer.data, "user_image" : user_image}, status=status.HTTP_200_OK)
        except Exception as e: 
            print(e)
            return Response({"error" : "Some Error Occured!!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
    def post(self, request, id=None):
        try:
            sender_id = request.data.get("sender")
            receiver_id = request.data.get("receiver")
            sender_user = InternUser.objects.get(id=sender_id)
            receiver_user = InternUser.objects.get(id=receiver_id)
            try:
                conversational_message = Conversation.objects.get(
                    (Q(sender=sender_id) | Q(receiver = sender_id)) &
                    (Q(receiver=receiver_id) | Q(sender = receiver_id))
                )            
            except Conversation.DoesNotExist:
                conversational_message = None  
            print(conversational_message)  
            conversational_id = None
            if conversational_message is not None:
                conversational_message.last_message = request.data.get("text")
                conversational_message.sender = sender_user
                conversational_message.receiver = receiver_user # receiver_id
                conversational_message.unread_message_count += 1
                conversational_message.save()
                conversational_id = conversational_message.id
            else: 
                conversational_serializer = ConversionalSerializer(data=request.data)
                if conversational_serializer.is_valid():
                    conversation_instance = conversational_serializer.save()
                    conversational_id = conversation_instance.id 
                else:
                    return Response(conversational_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            request.data["conversation_id"] = conversational_id
            message_serializer = MessageSerializer(data=request.data)
            if message_serializer.is_valid():
                message_instance = message_serializer.save()
                return Response({"message": message_instance.text}, status=201)
            else:
                return Response(message_serializer.errors, status=400)
        except Exception as e:
            print(e)
            return Response({"error" : "Internal Server Error"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        