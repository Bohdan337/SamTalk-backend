from django.contrib import admin
from .models import CustomUser
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm


class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    model = CustomUser
    list_display = ("username", "email", "is_active", "is_staff", "profile_image")
    list_filter = ("is_active", "date_joined")  
    search_fields = ("email", "username")
    readonly_fields = ("date_joined",)  

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
