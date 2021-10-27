from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = ('author', 'youtube', 'posted_date', 'title', 'get_tags', 'youtube_url', 'description',)
    filter_horizontal = ('tags',) # TO-DO: The filter neither works nor shows.

    def get_tags(self, obj):
        return ', '.join([tag.title for tag in obj.tags.all()])

    def youtube(self, obj):
        return mark_safe('<a href="{}" target="_blank">view</a>'.format(obj.youtube_url))

    get_tags.short_description = 'Tags'

admin.site.register(Video, VideoAdmin)
