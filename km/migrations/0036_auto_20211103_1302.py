# Generated by Django 3.1.4 on 2021-11-03 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('km', '0035_auto_20211010_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='name_is_shown',
            new_name='user_is_anonymous',
        ),
    ]
