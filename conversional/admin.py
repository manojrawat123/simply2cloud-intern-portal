# admin.py

from django.contrib import admin
from conversional.models import Conversation

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'last_message', 'unread_message_count', 'created_at']
    list_filter = ['sender', 'receiver', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'last_message']

    def last_message_truncated(self, obj):
        return obj.last_message[:50] + '...' if len(obj.last_message) > 50 else obj.last_message
    last_message_truncated.short_description = 'Last Message'
