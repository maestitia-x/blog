from django.contrib import admin
from .models import Category, Post, Comment
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','category','published','created_at','views']
    list_filter = ['published','category','created_at']
    search_fields = ['title','content']
    prepopulated_fields = {'slug':('title',)}
    list_editable = ['published']
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author','post','created_at','active']
    list_filter = ['active', 'created_at']
    search_fields = ['author__username', 'content']
    list_editable = ['active']

