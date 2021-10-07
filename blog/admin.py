from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Article, Tag

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'view_article', 'created_date', 'title', 'get_tags', 'introduction', 'content', 'slug',)
    filter_horizontal = ('tags',)
    prepopulated_fields = {'slug': ('title',)}

    def get_tags(self, obj):
        return ', '.join([tag.title for tag in obj.tags.all()])

    def view_article(self, obj):
        return mark_safe('<a href="/blog/{}" target="_blank">view</a>'.format(obj.slug))

    get_tags.short_description = 'Tags'
    view_article.short_description = 'Article'

class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
