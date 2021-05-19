# Generated by Django 3.1 on 2021-05-15 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('km', '0019_article_industry'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='mentioned_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mentioned_user', to=settings.AUTH_USER_MODEL),
        ),
    ]