from django.db import models

class Topic(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey('account.SiteUser', null=True, blank=True, on_delete=models.CASCADE, related_name='topic_creator')
    votes = models.IntegerField(default=0)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title
