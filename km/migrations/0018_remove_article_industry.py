# Generated by Django 3.1 on 2021-05-15 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('km', '0017_article_industry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='industry',
        ),
    ]