from django.contrib import admin
from .models import Article, Tag

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_date', 'title', 'get_tags', 'introduction', 'content', 'slug',)
    filter_horizontal = ('tags',)
    prepopulated_fields = {'slug': ('title',)}

    def get_tags(self, obj):
        return '\n'.join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = 'Tags'

class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
