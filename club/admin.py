from django.contrib import admin
from .models import Event
from pytz import timezone

class EventAdmin(admin.ModelAdmin):
    list_display = ('host', 'get_date', 'get_start_time', 'get_end_time', 'title', 'get_tags', 'age_restrictions', 'note', 'get_members', 'signup_deadline', 'max_participants',)
    filter_horizontal = ('tags',)

    def get_tags(self, obj):
        return ', '.join([tag.title for tag in obj.tags.all()])

    def get_members(self, obj):
        return ', '.join([member.get_full_name() for member in obj.members.all()])

    def get_date(self, obj):
        return obj.start_time.astimezone(timezone('Asia/Taipei')).strftime('%Y/%m/%d')

    def get_start_time(self, obj):
        return obj.start_time.astimezone(timezone('Asia/Taipei')).strftime('%I:%M %p')

    def get_end_time(self, obj):
        return obj.end_time.astimezone(timezone('Asia/Taipei')).strftime('%I:%M %p')

    get_tags.short_description       = 'Tags'
    get_members.short_description    = 'Members'
    get_date.short_description       = 'Date'
    get_start_time.short_description = 'Start Time'
    get_end_time.short_description   = 'End Time'

admin.site.register(Event, EventAdmin)
