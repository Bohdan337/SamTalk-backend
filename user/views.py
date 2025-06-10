from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from .serializers import CustomUserSerializer
from .models import CustomUser
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
import jwt


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def send_verification_email(self, user):
        from rest_framework_simplejwt.tokens import RefreshToken
        from django.urls import reverse

        subject = 'Welcome to our service! Submit your email to verify your account.'
        from_email = settings.DEFAULT_FROM_EMAIL
        token = RefreshToken.for_user(user).access_token
        to_email = [user.email]
        verification_link = f"{settings.BACKEND_BASE_URL}{reverse('verify_email')}?token={str(token)}"

        html_content = render_to_string('welcome_email.html', {'username': user.username, 'verification_link': verification_link, 'user_image' : user.profile_image.url if user.profile_image else None})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, html_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")

        try:
            msg.send()
        except Exception as e:
            print("Email error:", e)


    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        

        if serializer.is_valid():
            user = serializer.save()
            self.send_verification_email(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [AllowAny] #disables permission

    def get(self, request):
        from django.shortcuts import redirect

        token = request.GET.get('token')
       
        print('Verification token:', token)
        if token:
            try:
                from rest_framework_simplejwt.tokens import AccessToken, UntypedToken
                access_token = AccessToken(token)
                # access_token.check_exp()

                print('Access token:', access_token)
                user_id = access_token['user_id']
                user = CustomUser.objects.get(id=user_id)
                user.is_verified = True
                user.save()
                # return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
                return redirect(settings.FRONTEND_URL + '/login') 
            
            except (TokenError, InvalidToken, AuthenticationFailed):
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
                user_id = decoded.get('user_id')

                if user_id:
                    user = CustomUser.objects.get(id=user_id)
                    user.delete()
                    print(f"User with ID {user_id} deleted due to invalid/expired token.")

                return redirect(settings.FRONTEND_URL + '/sign_up')
            
            except Exception as e:
                print("Verification error:", e)
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    # def get_authenticate_header(self, request):
    #     user=request.user
    #     return Response('User: ', user)ч  
    
    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        print(request.data)
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=False, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        userData = request.GET.get('query', None)

        if userData:
            users = None

            if userData.isdigit():
                users = CustomUser.objects.filter(id=userData)

            if users is None and '@' not in userData:
                users = CustomUser.objects.filter(username__icontains=userData)

            if users is None and '@' in userData:
                users = CustomUser.objects.filter(email__icontains=userData)

            # users_data = [{"username": user.username, "email": user.email} for user in users]
            # if users_data == [] or users_data is None:
            #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            users = users.exclude(id=request.user.id)

            serializer = CustomUserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

