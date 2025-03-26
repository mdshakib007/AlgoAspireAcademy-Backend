from django.contrib import admin
from apps.account.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_admin', 'is_verified', 'is_active', 'is_deleted']
    list_display_links = ['username', 'email']
    list_filter = ['is_admin', 'is_verified', 'is_active', 'is_deleted']
    list_per_page = 20
    search_fields = ['username', 'email']

admin.site.register(User, UserAdmin)