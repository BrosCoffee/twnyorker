from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

class Article(models.Model):
    author = models.ForeignKey('account.SiteUser', on_delete=models.CASCADE, limit_choices_to={'is_admin': True})    
    created_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField('Tag', blank=True)
    introduction = models.TextField()
    content = RichTextUploadingField(blank=True, null=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Remove the Google Cloud Storage credential url extention
        if '?X-Goog-Algorithm=' in self.content:
            content_list = self.content.split('?X-Goog-Algorithm=')
            content_str = content_list.pop(0) + '"'
            # Hard code removing the rest of the credential info
            for item in content_list:
                content_str += item[759::] + '"'
            self.content = content_str[:-1]
        return super().save(*args, **kwargs)

class Tag(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title.replace('-', ' ').title()

    def save(self, *args, **kwargs):
        self.title = self.title.replace(' ', '-').lower()
        return super().save(*args, **kwargs)

class AboutArticle(Article):
    '''
    Utilize the Article model. The About page contents can be modified easily.
    '''
