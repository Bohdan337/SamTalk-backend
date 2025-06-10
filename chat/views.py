from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from .serializers import MessageSerializer, ChatSerializer
from .models import Message, Chat, CustomUser
from django.db.models import Count
from django.shortcuts import get_object_or_404
import json
from django.conf import settings

class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer

    def get(self, request):
        chats = Chat.objects.filter(members=request.user).order_by('-created_at')
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def post(self, request):
    #     members = request.data.get('members', []) 
    #     members.append({'username': request.user.username, 'email': request.user.email, 'image_url': f'http://127.0.0.1:8000{request.user.profile_image.url}'})

    #     if len(members) == 0:
    #         return Response({"detail": "At least 1 members are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        
    #     chatFilter = Chat.objects.annotate(members_count=Count('members')).filter(members_count=len(members))
    #     for chat in chatFilter:
    #         chat_members = chat.members.values_list('username', flat=True)
    #         print('new_chat_members: ', members)
    #         print('chat_members: ', chat_members)
    #         if members[0]['username'] in chat_members and members[1]['username'] in chat_members:
    #             serializer = ChatSerializer(chat)
    #             print(serializer.data)
    #             return Response(serializer.data, status=status.HTTP_200_OK)

    #     serializer = ChatSerializer(data = request.data)
    #     if serializer.is_valid():
    #         serializer.save(is_admin=request.user)    
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


    def post(self, request):
        members_data = request.data.get('members', []) 
        members_data.append({
            'username': request.user.username,
            'email': request.user.email,
            'image_url': f'{settings.BACKEND_BASE_URL}{request.user.profile_image.url}'
        })

        if not members_data:
            return Response({"detail": "At least 1 member is required."}, status=status.HTTP_400_BAD_REQUEST)


        user_names = [member['username'] for member in members_data]
        users = CustomUser.objects.filter(username__in=user_names)

        if users.count() != len(user_names):
            return Response({"detail": "Some users not found."}, status=status.HTTP_400_BAD_REQUEST)

        chatFilter = Chat.objects.annotate(members_count=Count('members')).filter(members_count=len(users))
        for chat in chatFilter:
            chat_members = list(chat.members.values_list('username', flat=True))
            print('new_chat_members:', user_names)
            print('chat_members:', chat_members)
            if set(user_names) == set(chat_members):
                serializer = ChatSerializer(chat)
                return Response(serializer.data, status=status.HTTP_200_OK)

        chat = Chat.objects.create(is_admin=request.user)
        chat.members.set(users)

        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)





class ChatDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer

    def get(self, request, pk):
        try:
            chat = Chat.objects.get(id=pk, members=request.user)
            print(chat)
        except Chat.DoesNotExist:
            return Response({"detail": "Chat not found or access denied."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChatSerializer(chat)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            chat = Chat.objects.get(id=pk, members=request.user)
        except Chat.DoesNotExist:
            return Response({"message": "Chat not found or access denied."}, status=status.HTTP_404_NOT_FOUND)
        
        members_data = request.data.get('members', []) 

        user_names = [member['username'] for member in members_data]
        users = CustomUser.objects.filter(username__in=user_names)
        chat.members.set(users)

        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class RemoveChatMembersView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer

    def put(self, request, chat_id):
        user = request.data.get("user")

        try:
            user = CustomUser.objects.get(username=user['username'])
            chat = Chat.objects.get(id=chat_id)

            chat.members.remove(user) 
            chat.save()

            serialized_chat = ChatSerializer(chat)      
            return Response(serialized_chat.data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Chat.DoesNotExist:
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MessageView(APIView):         
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id, members=request.user)
        except Chat.DoesNotExist:
            return Response({"detail": "Chat not found or access denied."}, status=status.HTTP_404_NOT_FOUND)
        
        messages = Message.objects.filter(chat=chat).order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)