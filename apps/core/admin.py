from django.contrib import admin
from apps.core.models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_active', 'created_at']
    list_display_links = ['title']
    list_filter = ['is_active', 'created_at']
    ordering = ['id', 'created_at']
    search_fields = ['title']
    readonly_fields = ['id', 'created_at']
    list_per_page = 20