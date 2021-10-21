from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Youtube

class YoutubeAdmin(admin.ModelAdmin):
    list_display = ('author', 'view_video', 'posted_date', 'title', 'get_tags', 'youtube_url', 'description', 'slug',)
    filter_horizontal = ('tags',) # TO-DO: The filter neither works nor shows.
    prepopulated_fields = {'slug': ('title',)}

    def get_tags(self, obj):
        return ', '.join([tag.title for tag in obj.tags.all()])

    def view_video(self, obj):
        return mark_safe('<a href="/youtube/{}" target="_blank">view</a>'.format(obj.slug))

    get_tags.short_description = 'Tags'
    view_video.short_description = 'Video'

admin.site.register(Youtube, YoutubeAdmin)
