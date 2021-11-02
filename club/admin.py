from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Event
from pytz import timezone

class EventAdmin(admin.ModelAdmin):
    list_display = ('host', 'get_date', 'get_start_time', 'get_end_time', 'title', 'get_tags', 'age_restrictions', 'note', 'get_members', 'signup_deadline', 'max_participants', 'get_members_email', 'copy_emails',)
    filter_horizontal = ('tags',)

    class Media:
        js = ('account/js/copy-emails-btn.js',)

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

    def get_members_email(self, obj):
        return ', '.join([member.email for member in obj.members.all()])

    readonly_fields = (
        'copy_emails',
    )

    def copy_emails(self, obj):
        if obj.members.all():
            return mark_safe(
                f"""
                <a href="#" class="copy-btn">Copy Emails</a>
                """
            )
        else:
            return None

    get_tags.short_description          = 'Tags'
    get_members.short_description       = 'Members'
    get_date.short_description          = 'Date'
    get_start_time.short_description    = 'Start Time'
    get_end_time.short_description      = 'End Time'
    get_members_email.short_description = 'Participants Email'
    copy_emails.short_description       = 'Copy'


admin.site.register(Event, EventAdmin)
