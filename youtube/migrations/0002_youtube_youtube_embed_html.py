# Generated by Django 3.2.6 on 2021-10-21 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtube',
            name='youtube_embed_html',
            field=models.TextField(default='testing'),
            preserve_default=False,
        ),
    ]
