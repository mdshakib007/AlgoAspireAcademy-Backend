from django.contrib import admin
from apps.course.models import Course, Module, Lesson, Quiz, Question, Assignment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_published', 'created_at', 'updated_at']
    list_display_links = ['code', 'name']
    list_filter = ['is_published', 'created_at']
    ordering = ['code', 'name', 'created_at', 'updated_at']
    search_fields = ['code', 'name']
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20

    actions = ['publish_courses']

    def publish_courses(self, request, queryset):
        """Custom admin action to mark selected courses as published."""
        queryset.update(is_published=True)
    publish_courses.short_description = "Mark selected courses as Published"


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'is_published', 'created_at', 'updated_at']
    list_display_links = ['course', 'title']
    list_filter = ['is_published', 'created_at']
    ordering = ['title', 'created_at']
    search_fields = ['course__name', 'title']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20

    inlines = []  # Can add inline related models if needed


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['module', 'title', 'lecture_type', 'is_published', 'created_at', 'updated_at']
    list_display_links = ['module', 'title']
    list_filter = ['lecture_type', 'is_published', 'created_at']
    ordering = ['title', 'created_at']
    search_fields = ['module__title', 'title', 'lecture_type']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'created_at', 'updated_at']
    search_fields = ['lesson__title']
    ordering = ['lesson']
    list_filter = ['created_at']
    list_per_page = 20

    inlines = [] 


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'title', 'created_at', 'updated_at']
    list_display_links = ['quiz', 'title']
    search_fields = ['quiz__lesson__title', 'title']
    ordering = ['quiz', 'title']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'question', 'total_mark', 'created_at']
    list_display_links = ['lesson', 'question']
    search_fields = ['lesson__title', 'question__title']
    ordering = ['lesson', 'question', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    list_per_page = 20
