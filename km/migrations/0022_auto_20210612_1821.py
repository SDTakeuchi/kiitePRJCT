# Generated by Django 3.1 on 2021-06-12 09:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('km', '0021_comment_like_user_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='like_user_list',
            field=models.ManyToManyField(blank=True, related_name='like_user_list', to=settings.AUTH_USER_MODEL),
        ),
    ]