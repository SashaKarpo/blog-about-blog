from django.contrib import admin, messages
from .models import Post, Category


class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', ' Замужем'),
            ('single', ' Не замужем'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        else:
            return queryset.filter(husband__isnull=True)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'content', 'cat', 'husband', 'tags')
#    readonly_fields = ('slug', )
    filter_horizontal = ('tags',)
    prepopulated_fields = {'slug': ('title', )}
    list_display = ('title', 'content', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    ordering = ('title',)
    list_editable = ('is_published',)
    list_per_page = 10
    actions = ('set_published', 'set_draft')
    search_fields = ('title', 'cat__name')
    list_filter = (MarriedFilter, 'cat__name', 'is_published')

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, post: Post):
        return f'Описание {len(post.content)} символов'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {count} статей')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Post.Status.DRAFT)
        self.message_user(request, f'Добавлено в черновик {count} статей', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

# admin.site.register(Post, PostAdmin)

# Register your models here.
