from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Article, Tag, AboutArticle

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'view_article', 'created_date', 'title', 'get_tags', 'introduction', 'content', 'slug',)
    filter_horizontal = ('tags',) # TO-DO: The filter neither works nor shows.
    prepopulated_fields = {'slug': ('title',)}

    def get_tags(self, obj):
        return ', '.join([tag.title for tag in obj.tags.all()])

    def view_article(self, obj):
        return mark_safe('<a href="/blog/{}" target="_blank">view</a>'.format(obj.slug))

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        return qs.filter(aboutarticle__isnull=True)

    get_tags.short_description = 'Tags'
    view_article.short_description = 'Article'

class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)

class AboutArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_date', 'title', 'introduction', 'content', 'slug',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(AboutArticle, AboutArticleAdmin)
