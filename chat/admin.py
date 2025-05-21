from django.contrib import admin
from .models import Chat, Message
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter


class ChatAdmin(ModelAdmin):
    model = Chat
    list_display = ("id", "is_admin", "created_at")
    list_filter = ("is_admin", "created_at")  
    search_fields = ("members__username", "members__email")
    readonly_fields = ("created_at",)


class MessageAdmin(ModelAdmin):
    model = Message
    list_display = ("id", "chat", "author__username", "content", "created_at")
    list_filter = ("chat", "author", ("created_at", RangeDateTimeFilter))  
    search_fields = ("chat__members__username", "author__username", "content")
    readonly_fields = ("created_at",)

# Register your models here.
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)