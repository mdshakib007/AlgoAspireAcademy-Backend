from django.contrib import admin
from apps.enrollment.models import Enrollment, LessonCompletion

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'completed_percentage', 'is_completed', 'is_active')
    list_filter = ('is_completed', 'is_active', 'enrolled_at', 'course')
    search_fields = ('user__username', 'user__email', 'course__title')
    readonly_fields = ('enrolled_at', 'completed_percentage', 'completed_at', 'estimate_completion_date')
    list_per_page = 20
    ordering = ('-enrolled_at',)

@admin.register(LessonCompletion)
class LessonCompletionAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'completed_at')
    list_filter = ('completed_at', 'lesson__module', 'lesson')
    search_fields = ('enrollment__user__username', 'lesson__title')
    readonly_fields = ('completed_at',)
    list_per_page = 20
    ordering = ('-completed_at',)
