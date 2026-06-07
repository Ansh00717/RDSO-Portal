from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for UserProfile.
    This is what you see when you go to /admin/ and click on 'User profiles'.
    """
    list_display = ('email', 'first_name', 'last_name', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


admin.site.register(UserProfile, UserProfileAdmin)