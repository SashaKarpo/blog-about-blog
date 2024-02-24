from django.contrib import admin
from .models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'time_create', 'is_published', 'cat')
    list_display_links = ('id', 'title')
    ordering = ('title',)
    list_editable = ('is_published', )
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

# admin.site.register(Post, PostAdmin)

# Register your models here.
