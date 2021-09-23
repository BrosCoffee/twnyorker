from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('host', 'created_date', 'title', 'get_tags', 'note', 'get_members', 'start_time', 'end_time', 'signup_deadline', 'max_participants',)
    filter_horizontal = ('tags',)

    def get_tags(self, obj):
        return '\n'.join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = 'Tags'

    def get_members(self, obj):
        return '\n'.join([member.get_full_name() for member in obj.members.all()])

    get_members.short_description = 'Members'

admin.site.register(Event, EventAdmin)
