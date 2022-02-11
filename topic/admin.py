from django.contrib import admin
from .models import Topic

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'votes', 'complete')

admin.site.register(Topic, TopicAdmin)
