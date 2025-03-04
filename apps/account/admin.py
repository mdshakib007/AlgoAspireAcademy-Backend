from django.contrib import admin
from apps.account.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_admin', 'is_verified', 'is_active']

admin.site.register(User, UserAdmin)