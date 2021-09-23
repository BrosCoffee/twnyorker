from django.db import models

class Event(models.Model):
    host = models.ForeignKey('account.SiteUser', on_delete=models.CASCADE, limit_choices_to={'is_admin': True}, related_name='event_host')    
    created_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField('blog.Tag', blank=True)
    note = models.TextField(blank=True)
    members = models.ManyToManyField('account.SiteUser', blank=True, related_name='event_members')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    signup_deadline = models.DateField(null=True, blank=True)
    max_participants = models.IntegerField(default=10)

    def __str__(self):
        return self.title
