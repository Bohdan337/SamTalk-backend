from django.urls import path
from . import views


urlpatterns = [   
    path('chats', views.ChatView.as_view(), name='chats'),
    path('chats/<int:pk>', views.ChatDetailView.as_view(), name='chatDeatils'),
    path('chats/<int:chat_id>/messages', views.MessageView.as_view(), name='chat_messages'),
    path('chats/<int:chat_id>/remove-member', views.RemoveChatMembersView.as_view(), name='remove_chat_members'),
]