# Generated by Django 3.2.6 on 2021-10-01 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='age_restrictions',
            field=models.CharField(choices=[('AD', 'Adult'), ('YO', 'Youth'), ('NR', 'No Restrictions')], default='NR', max_length=2),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_participants',
            field=models.IntegerField(default=6),
        ),
        migrations.AlterField(
            model_name='event',
            name='signup_deadline',
            field=models.DateTimeField(blank=True, help_text='If leave blank, the default signup deadline is 24hr before the start time', null=True),
        ),
    ]