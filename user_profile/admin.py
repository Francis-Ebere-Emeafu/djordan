from __future__ import unicode_literals

from django.contrib import admin
from user_profile.models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'usertype']
