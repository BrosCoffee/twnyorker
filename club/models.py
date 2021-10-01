from django.db import models
from datetime import timedelta

RESTRICTION_CHOICES = (
    ('AD', 'Adult'),
    ('YO', 'Youth'),
    ('NR', 'No Restrictions'),
)

class Event(models.Model):
    host = models.ForeignKey('account.SiteUser', on_delete=models.CASCADE, limit_choices_to={'is_admin': True}, related_name='event_host')    
    created_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField('blog.Tag', blank=True)
    age_restrictions = models.CharField(max_length=2, choices=RESTRICTION_CHOICES, default='NR')
    note = models.TextField(blank=True)
    members = models.ManyToManyField('account.SiteUser', blank=True, related_name='event_members')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    signup_deadline = models.DateTimeField(null=True, blank=True, help_text='If leave blank, the default signup deadline is 24hr before the start time')
    max_participants = models.IntegerField(default=6)

    def __str__(self):
        return self.title

    # Default signup deadline is 24hr before the start time
    def save(self, *args, **kwargs):
        if self.start_time > self.end_time:
            self.start_time, self.end_time = self.end_time, self.start_time
        if not self.signup_deadline or self.signup_deadline > self.start_time:
            self.signup_deadline = self.start_time - timedelta(hours=24)
        return super().save(*args, **kwargs)
