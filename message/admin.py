# admin.py

from django.contrib import admin
from message.models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'conversation_id', 'text', 'created_at', 'seen']
    list_filter = ['sender', 'receiver', 'created_at', 'seen']
    search_fields = ['sender__username', 'receiver__username', 'text']

    def conversation_id(self, obj):
        return obj.conversation_id.id
    conversation_id.short_description = 'Conversation ID'
