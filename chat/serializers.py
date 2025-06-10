from rest_framework import serializers
from .models import Chat, Message
from  user.models import CustomUser
from django.conf import settings

class MessageSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    image = serializers.SerializerMethodField(required=False)

    class Meta:
        model=Message
        fields=['id', 'chat', 'author', 'content', 'image', 'created_at']

    def get_image(self, obj):
        if obj.image:
            return f'{settings.BACKEND_BASE_URL}/api{obj.image.url}'
        return None

class ChatMemberSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'image_url']

    def get_image_url(self, obj):
        return f'{settings.BACKEND_BASE_URL}/api{obj.profile_image.url}'

class ChatSerializer(serializers.ModelSerializer):
    members = ChatMemberSerializer(many=True)
    messages = MessageSerializer(many=True, read_only=True)
    is_admin = serializers.ReadOnlyField(source='is_admin.username')

    class Meta:
        model = Chat
        fields = ['id', 'members', 'messages', 'created_at', 'is_admin']

    


