# Generated by Django 3.1.4 on 2021-11-07 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('km', '0038_auto_20211106_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usernotification',
            name='user',
        ),
        migrations.AddField(
            model_name='usernotification',
            name='user',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, to='km.customuser'),
            preserve_default=False,
        ),
    ]