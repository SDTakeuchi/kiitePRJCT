# Generated by Django 3.1 on 2021-07-17 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('km', '0024_comment_is_reply_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='name_is_shown',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
