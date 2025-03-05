from django.contrib import admin
from apps.course.models import (
    Course,
    Module, 
    Lesson,
    Quiz,
    Question,
    Assignment
)


class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_published', 'created_at', 'updated_at']

admin.site.register(Course, CourseAdmin)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Assignment)