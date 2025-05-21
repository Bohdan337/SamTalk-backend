from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('sign_up', views.RegisterView.as_view(), name='sign_up'),   
    path('profile', views.ProfileView.as_view(), name='profile'),   
    path('user/search', views.GetUser.as_view(), name='userGet'),
    path('user/verify', views.VerifyEmail.as_view(), name='verify_email'),

    # JWT token authentication
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]