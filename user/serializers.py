from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.models import User
from django.conf import settings

class CustomUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, required=False, min_length=8)
    image_url=serializers.SerializerMethodField(required=False)
    profile_image=serializers.ImageField(write_only=True, required=False)

    class Meta:
        model=CustomUser
        fields=("email","username","is_active","is_verified","is_staff","password","image_url", "profile_image")
        # read_only_fields = ['email']
    
    def get_image_url(self, obj):
        return f'{settings.BACKEND_BASE_URL}{obj.profile_image.url}'
    
    # def validate(self, data):
    #     if CustomUser.objects.filter(email=data['email']).exists():
    #         raise serializers.ValidationError("A user with this email already exists.")
    #     if CustomUser.objects.filter(username=data['username']).exists():
    #         raise serializers.ValidationError("A ts.")
    #     return data

    def validate_email(self, value):
        user_id = self.instance.id if self.instance else None
        if CustomUser.objects.exclude(id=user_id).filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):   
        user=CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user 
