from django.contrib import admin
from .models import Tag, Post, Vote, Comment


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class VoteInline(admin.TabularInline):
    model = Vote
    extra = 0  # No extra empty forms

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'post_type', 'access', 'views', 'created_at')
    list_filter = ('post_type', 'access', 'created_at')
    search_fields = ('title', 'body', 'user__username')
    inlines = [VoteInline, CommentInline]
    ordering = ('-created_at',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    search_fields = ('user__username', 'post__title')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title', 'content')