from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Youtube(models.Model):
    author = models.ForeignKey('account.SiteUser', on_delete=models.CASCADE, limit_choices_to={'is_admin': True})    
    posted_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField('blog.Tag', blank=True)
    youtube_url = models.URLField(max_length=300)
    youtube_embed_html = models.TextField()
    youtube_embed_url = models.URLField(max_length=300)
    description = RichTextUploadingField(blank=True, null=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Remove the Google Cloud Storage credential url extention
        if '?X-Goog-Algorithm=' in self.description:
            description_list = self.description.split('?X-Goog-Algorithm=')
            description_str = description_list.pop(0) + '"'
            # Hard code removing the rest of the credential info
            for item in description_list:
                description_str += item[759::] + '"'
            self.description = description_str[:-1]
        return super().save(*args, **kwargs)
