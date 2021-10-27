from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Video(models.Model):
    author = models.ForeignKey('account.SiteUser', on_delete=models.CASCADE, limit_choices_to={'is_admin': True})    
    posted_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField('blog.Tag', blank=True)
    youtube_url = models.URLField(max_length=300)
    youtube_embed_html = models.TextField()
    youtube_embed_url = models.URLField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.title
